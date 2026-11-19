from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from html.parser import HTMLParser
import sys
import threading
from time import sleep
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException

R = "\033[31m"
N = "\033[0m"

MARKER = "wxprobe941"

PROBES: tuple[tuple[str, str], ...] = (
    ("plain", MARKER),
    ("attr-dquote", f'{MARKER}" data-ctx="{MARKER}'),
    ("attr-squote", f"{MARKER}' data-ctx='{MARKER}"),
    ("tag", f"<{MARKER} data-ctx=\"{MARKER}\">"),
    ("script", f"</script><script data-ctx=\"{MARKER}\">"),
)

COMMON_PARAMS: tuple[str, ...] = ("s", "q", "search", "query", "id", "name", "page", "cat")


def red(text: str) -> None:
    print(f"{R}{text}{N}")
    sleep(0.01)


def red_input(prompt: str) -> str:
    sys.stdout.write(f"{R}{prompt}")
    sys.stdout.flush()
    val = input()
    sys.stdout.write(N)
    return val


def banner() -> None:
    red("")
    red("  ╔══════════════════════════════════════╗")
    red("  ║         XSS DEEP CONTEXT PROBE       ║")
    red("  ║    reflection · potential · proof    ║")
    red("  ╚══════════════════════════════════════╝")
    red("")


@dataclass(frozen=True)
class ScanConfig:
    target_url: str
    delay: float = 0.75
    workers: int = 4
    timeout: float = 8.0
    verify_tls: bool = True
    user_agent: str = "Mozilla/5.0 WebSploit"


@dataclass(frozen=True)
class FormField:
    name: str
    field_type: str
    value: str


@dataclass(frozen=True)
class ParsedForm:
    action: str
    method: str
    fields: tuple[FormField, ...]


@dataclass(frozen=True)
class Finding:
    confidence: str
    url: str
    proof: str


def _is_escaped_at(text: str, index: int) -> bool:
    slashes = 0
    pos = index - 1
    while pos >= 0 and text[pos] == "\\":
        slashes += 1
        pos -= 1
    return (slashes % 2) == 1


class _HtmlInspector(HTMLParser):
    def __init__(self, needle: str, payload: str) -> None:
        super().__init__(convert_charrefs=False)
        self.needle = needle
        self.payload = payload
        self.stack: list[tuple[str, str]] = []
        self.forms: list[ParsedForm] = []
        self._form: dict | None = None
        self.inputs: list[str] = []
        self.hits: list[tuple[str, str]] = []

    def _current_tag(self) -> tuple[str, str]:
        return self.stack[-1] if self.stack else ("body", "")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        t = tag.lower()
        amap = {k.lower(): (v or "") for k, v in attrs}

        if t == "form":
            self._form = {
                "action": amap.get("action", ""),
                "method": (amap.get("method", "GET") or "GET").upper(),
                "fields": [],
            }
        elif t in ("input", "textarea", "select"):
            name = amap.get("name", "").strip()
            ftype = amap.get("type", t).lower()
            if name and ftype not in ("submit", "button", "reset", "image", "hidden"):
                fld = FormField(name=name, field_type=ftype, value=amap.get("value", ""))
                if self._form is not None:
                    self._form["fields"].append(fld)
                else:
                    self.inputs.append(name)

        if t != "link":
            for aname, aval in amap.items():
                if self.needle in aval:
                    clean_val = " ".join(aval.split())[:45]
                    if aname.startswith("on"):
                        self.hits.append(("Potential XSS", f"event {t}.{aname}: {clean_val}"))
                    elif aname in ("href", "src", "action") and aval.strip().lower().startswith("javascript:"):
                        self.hits.append(("Potential XSS", f"js-url {t}.{aname}: {clean_val}"))
                    else:
                        self.hits.append(("Reflection", f"attr {t}.{aname}: {clean_val}"))

        if t == self.needle:
            parent_name, _ = self._current_tag()
            if parent_name not in ("script", "style", "textarea", "title"):
                self.hits.append(("Potential XSS", f"new tag <{t}> in body"))
            else:
                self.hits.append(("Reflection", f"tag-like text <{t}> in <{parent_name}>"))

        script_type = amap.get("type", "").strip().lower() if t == "script" else ""
        self.stack.append((t, script_type))

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t == "form" and self._form is not None:
            self.forms.append(
                ParsedForm(
                    action=self._form["action"],
                    method=self._form["method"],
                    fields=tuple(self._form["fields"]),
                )
            )
            self._form = None

        for idx in range(len(self.stack) - 1, -1, -1):
            if self.stack[idx][0] == t:
                del self.stack[idx:]
                break

    def handle_data(self, data: str) -> None:
        if self.needle not in data:
            return
        parent, script_type = self._current_tag()
        snippet = " ".join(data.split())
        idx = snippet.find(self.needle)
        start = max(0, idx - 20)
        end = min(len(snippet), idx + len(self.needle) + 20)
        short = snippet[start:end]

        if parent == "script":
            is_json_block = "json" in script_type
            raw_idx = data.find(self.needle)
            unescaped_quote = False
            if '"' in self.payload and '"' in data:
                q_pos = data.find('"', max(0, raw_idx - len(self.payload) - 2))
                if q_pos != -1 and not _is_escaped_at(data, q_pos):
                    unescaped_quote = True
            if "'" in self.payload and "'" in data:
                q_pos = data.find("'", max(0, raw_idx - len(self.payload) - 2))
                if q_pos != -1 and not _is_escaped_at(data, q_pos):
                    unescaped_quote = True

            if not is_json_block and unescaped_quote:
                self.hits.append(("Potential XSS", f"<script> body: {short}"))
            else:
                self.hits.append(("Reflection", f"<script> data: {short}"))
        else:
            self.hits.append(("Reflection", f"<{parent}> text: {short}"))


class _SessionPool:
    def __init__(self, config: ScanConfig) -> None:
        self._config = config
        self._local = threading.local()

    def client(self) -> requests.Session:
        sess = getattr(self._local, "session", None)
        if sess is None:
            sess = requests.Session()
            sess.verify = self._config.verify_tls
            sess.headers.update({"User-Agent": self._config.user_agent})
            adapter = HTTPAdapter(pool_connections=4, pool_maxsize=4)
            sess.mount("http://", adapter)
            sess.mount("https://", adapter)
            self._local.session = sess
        return sess

    def close(self) -> None:
        sess = getattr(self._local, "session", None)
        if sess is not None:
            sess.close()
            self._local.session = None


class XSSScanner:
    def __init__(self, config: ScanConfig) -> None:
        self.config = config
        self.stop_event = threading.Event()
        self._lock = threading.Lock()
        self._pool = _SessionPool(config)

    def out(self, line: str) -> None:
        if self.stop_event.is_set():
            return
        with self._lock:
            print(f"{R}{line}{N}")

    @staticmethod
    def _set_param(url: str, param: str, val: str) -> str:
        parsed = urlparse(url)
        q = dict(parse_qsl(parsed.query, keep_blank_values=True))
        q[param] = val
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, urlencode(q), parsed.fragment))

    def _evaluate_body(self, status: int, body: str, baseline_body: str, payload: str) -> tuple[str, str] | None:
        if not body or MARKER in baseline_body or MARKER not in body:
            return None

        inspector = _HtmlInspector(needle=MARKER, payload=payload)
        try:
            inspector.feed(body)
            inspector.close()
        except Exception:
            return None

        if not inspector.hits:
            return None

        for level, proof in inspector.hits:
            if level == "Potential XSS":
                return level, f"HTTP {status} | {proof}"

        level, proof = inspector.hits[0]
        return level, f"HTTP {status} | {proof}"

    def _check_get(self, url: str, param: str, payload: str, baseline_body: str) -> Finding | None:
        if self.stop_event.is_set():
            return None
        target = self._set_param(url, param, payload)
        try:
            r = self._pool.client().get(target, timeout=self.config.timeout, allow_redirects=True)
            verdict = self._evaluate_body(r.status_code, r.text or "", baseline_body, payload)
            self.stop_event.wait(timeout=self.config.delay)
            if verdict is None:
                return None
            level, proof = verdict
            return Finding(confidence=level, url=r.url or target, proof=f"{param}: {proof}")
        except RequestException as exc:
            self.stop_event.wait(timeout=self.config.delay)
            self.out(f"  [-] {target} | err: {type(exc).__name__}")
            return None

    def _check_form(
        self,
        base_url: str,
        form: ParsedForm,
        field_name: str,
        payload: str,
        baseline_body: str,
    ) -> Finding | None:
        if self.stop_event.is_set():
            return None
        action = urljoin(base_url, form.action) if form.action else base_url
        method = form.method if form.method in ("GET", "POST") else "POST"
        data: dict[str, str] = {}
        for f in form.fields:
            if f.name == field_name:
                data[f.name] = payload
            elif f.field_type == "email":
                data[f.name] = f.value or "test@example.local"
            else:
                data[f.name] = f.value or MARKER

        try:
            sess = self._pool.client()
            if method == "GET":
                r = sess.get(action, params=data, timeout=self.config.timeout, allow_redirects=True)
                target_label = r.url or action
            else:
                r = sess.post(action, data=data, timeout=self.config.timeout, allow_redirects=True)
                target_label = f"{action} [{field_name}]"
            verdict = self._evaluate_body(r.status_code, r.text or "", baseline_body, payload)
            self.stop_event.wait(timeout=self.config.delay)
            if verdict is None:
                return None
            level, proof = verdict
            return Finding(confidence=level, url=target_label, proof=f"{method} {field_name}: {proof}")
        except RequestException as exc:
            self.stop_event.wait(timeout=self.config.delay)
            self.out(f"  [-] {action} | err: {type(exc).__name__}")
            return None

    def run(self) -> list[Finding]:
        results: list[Finding] = []
        seen: set[tuple[str, str, str]] = set()
        try:
            base = self._pool.client().get(self.config.target_url, timeout=self.config.timeout, allow_redirects=True)
        except RequestException as exc:
            self.out(f"  [-] baseline error: {exc}")
            return results

        final_url = base.url or self.config.target_url
        baseline_body = base.text or ""

        inspector = _HtmlInspector(needle=MARKER, payload=MARKER)
        try:
            inspector.feed(baseline_body)
            inspector.close()
        except Exception as exc:
            self.out(f"  [-] parse error: {exc}")
            return results

        q_keys = list(dict(parse_qsl(urlparse(final_url).query, keep_blank_values=True)).keys())
        params = list(dict.fromkeys(q_keys + inspector.inputs + list(COMMON_PARAMS)))
        form_targets = [(frm, fld.name) for frm in inspector.forms for fld in frm.fields]

        self.out(f"  [*] target={final_url} | params={len(params)} | forms={len(inspector.forms)}")
        self.out("  Press Ctrl + C to stop...")
        self.out("")

        executor = ThreadPoolExecutor(max_workers=self.config.workers)
        try:
            futures = []
            for p in params:
                for _, payload in PROBES:
                    if self.stop_event.is_set():
                        break
                    futures.append(executor.submit(self._check_get, final_url, p, payload, baseline_body))
            for frm, fname in form_targets:
                for _, payload in PROBES:
                    if self.stop_event.is_set():
                        break
                    futures.append(executor.submit(self._check_form, final_url, frm, fname, payload, baseline_body))

            for fut in as_completed(futures):
                if self.stop_event.is_set():
                    break
                item = fut.result()
                if item is not None:
                    key = (item.confidence, item.url, item.proof)
                    if key not in seen:
                        seen.add(key)
                        results.append(item)
                        self.out(f"  [{item.confidence}] {item.url} -> {item.proof}")
        except KeyboardInterrupt:
            self.stop_event.set()
            try:
                executor.shutdown(wait=False, cancel_futures=True)
            except TypeError:
                executor.shutdown(wait=False)
            raise
        finally:
            if not self.stop_event.is_set():
                executor.shutdown(wait=True)
            self._pool.close()

        return results


def xss_probe_menu() -> None:
    try:
        banner()
        raw_url = red_input("  target url > ").strip()
        if not raw_url:
            red("  [-] empty url")
            return
        if not raw_url.startswith(("http://", "https://")):
            raw_url = "https://" + raw_url

        delay_in = red_input("  delay per check sec [0.75] > ").strip()
        try:
            delay = max(0.1, min(5.0, float(delay_in) if delay_in else 0.75))
        except ValueError:
            delay = 0.75

        tls_in = red_input("  verify TLS certs [Y/n] > ").strip().lower()
        verify_tls = tls_in not in ("n", "no", "0", "false")

        scanner = XSSScanner(ScanConfig(target_url=raw_url, delay=delay, verify_tls=verify_tls))
        red("")
        red(f"  [*] baseline -> {raw_url} (verify_tls={verify_tls})...")
        findings = scanner.run()

        pot = sum(1 for f in findings if f.confidence == "Potential XSS")
        ref = sum(1 for f in findings if f.confidence == "Reflection")
        red("")
        red(f"  [*] done: potential_xss={pot} | reflection={ref} | confirmed_xss=0")
        red("")

    except KeyboardInterrupt:
        red("")
        red("  [!] stopped")
        red("")
        sleep(0.3)