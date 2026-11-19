import requests
import random
import string
import sys
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

requests.packages.urllib3.disable_warnings()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0",
    "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
] 

TIMEOUT = (3.0, 5.0)
THREADS = 20
PROBES = 4

R = "\033[31m"
N = "\033[0m"

def red(text):
    print(f"{R}{text}{N}")
    sleep(0.03)

def red_input(prompt):
    sys.stdout.write(f"{R}{prompt}")
    sys.stdout.flush()
    value = input()
    sys.stdout.write(N)
    return value

def banner():
    red("")
    red("  ╔══════════════════════════════════════╗")
    red("  ║           DIRECTORY FUZZER           ║")
    red("  ║      soft-404 aware · ua-rotate      ║")
    red("  ╚══════════════════════════════════════╝")
    red("")

def rand_path(n=11):
    return "/" + "".join(random.choices(string.ascii_lowercase + string.digits, k=n))

def make_session():
    s = requests.Session()
    s.verify = False
    s.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    })
    return s

def one_request(session, url):
    session.headers["User-Agent"] = random.choice(USER_AGENTS)
    try:
        r = session.get(url, timeout=TIMEOUT, allow_redirects=False)
        return r.status_code, url, len(r.content)
    except Exception as e:
        return f"ERR:{type(e).__name__}", url, 0

def check_target(session, base):
    red("[*] checking target...")
    try:
        r = session.get(base, timeout=TIMEOUT, allow_redirects=False)
        red(f"[+] target alive  |  status: {r.status_code}  |  size: {len(r.content)}b")
        return True
    except Exception as e:
        red(f"[!] target unreachable: {type(e).__name__}")
        red("[!] abort")
        return False

def probe(session, base):
    codes, lengths, errors = [], [], 0
    red("[*] calibrating against non-existent paths")
    for _ in range(PROBES):
        url = base.rstrip("/") + rand_path()
        status, _, length = one_request(session, url)
        if isinstance(status, str):
            errors += 1
            red(f"    {status:<18} {url}")
        else:
            codes.append(status)
            lengths.append(length)
            red(f"    {status:<6} {length:>6}b   {url}")

    if errors == PROBES:
        red("")
        red("[!] all probes failed - abort")
        return None, None

    if 200 in codes:
        red("")
        red("[!] non-existent path returns 200")
        red("[!] soft-404 detected - fuzzing aborted")
        red("")
        return None, None

    code_bl = set(codes)
    red(f"[+] status blacklist : {sorted(code_bl) or 'empty'}")
    return code_bl, set()

def run_fuzz(base_url, wordlist_path):
    if not wordlist_path.exists():
        red(f"[-] wordlist missing : {wordlist_path}")
        return

    paths = [l.strip() for l in open(wordlist_path, encoding="utf-8") if l.strip()]
    session = make_session()
    pool = None

    try:
        if not check_target(session, base_url):
            return

        code_bl, len_bl = probe(session, base_url)
        if code_bl is None:
            return

        urls = [f"{base_url.rstrip('/')}/{p.lstrip('/')}" for p in paths]
        total = len(urls)
        red("")
        red(f"[*] starting fuzz  |  targets: {total}  |  threads: {THREADS}")
        red("[*] press Ctrl+C to stop")
        red("─" * 48)

        found = 0
        pool = ThreadPoolExecutor(max_workers=THREADS)
        futs = [pool.submit(one_request, session, u) for u in urls]

        for f in as_completed(futs):
            status, url, length = f.result()
            if isinstance(status, str):
                continue
            if status in code_bl:
                continue
            found += 1
            red(f"[{status}] {length:>6}b   {url}")

        red("─" * 48)
        red(f"[*] finished  |  interesting hits: {found}")
        red("")

    except KeyboardInterrupt:
        red("")
        red("[!] stopped by user")
        red("")
    finally:
        if pool is not None:
            pool.shutdown(wait=False, cancel_futures=True)

def directory_fuzz_menu():
    try:
        banner()
        red("  ────────────────")
        red("  [1]  small.txt")
        red("  [2]  medium.txt")
        red("  [3]  large.txt")
        red("  ────────────────")
        red("")
        choice = red_input("  root@websploit > ").strip()

        if choice == "0" or choice not in ("1", "2", "3"):
            return

        mapping = {
            "1": "small.txt",
            "2": "medium.txt",
            "3": "large.txt",
        }

        red("")
        base = red_input("  target url > ").strip()
        if not base:
            red("  [-] empty url")
            return
        if not base.startswith(("http://", "https://")):
            base = "https://" + base

        wordlist = Path(__file__).resolve().parent.parent / "directory_list" / mapping[choice]
        if not wordlist.exists():
            wordlist = Path("lists/directory_list") / mapping[choice]
        if not wordlist.exists():
            wordlist = Path(mapping[choice])

        red("")
        red(f"  wordlist : {mapping[choice]}")
        red(f"  target   : {base}")
        red("")
        run_fuzz(base, wordlist)

    except KeyboardInterrupt:
        red("")
        red("  [!] stopped")
        red("")
        sleep(0.5)
