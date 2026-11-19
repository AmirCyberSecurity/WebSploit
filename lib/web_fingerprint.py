import socket
import sys
import ssl
from urllib.parse import urlparse
from time import sleep

R = "\033[31m"
N = "\033[0m"

def red(text):
    print(f"{R}{text}{N}")
    sleep(0.01)

def red_input(prompt):
    sys.stdout.write(f"{R}{prompt}")
    sys.stdout.flush()
    value = input()
    sys.stdout.write(N)
    return value

def banner():
    red("")
    red("  ╔══════════════════════════════════════╗")
    red("  ║         WEB FINGERPRINTING           ║")
    red("  ║    deep recon · stack · security     ║")
    red("  ╚══════════════════════════════════════╝")
    red("")

def fetch_url(url, max_redirects=5):
    body_content = b""
    for _ in range(max_redirects):
        parsed = urlparse(url)
        hostname = parsed.hostname
        port = parsed.port
        is_https = parsed.scheme == "https"
        path = parsed.path if parsed.path else "/"
        if parsed.query:
            path += f"?{parsed.query}"

        if not port:
            port = 443 if is_https else 80

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)

        try:
            ip = socket.gethostbyname(hostname)
        except socket.gaierror:
            return None, None, b"", f"Could not resolve host: {hostname}"

        try:
            if is_https:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=hostname)

            s.connect((hostname, port))
            request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\nConnection: close\r\n\r\n"
            s.sendall(request.encode("utf-8"))

            response_data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response_data += chunk
            s.close()

            headers_raw, _, body_content = response_data.partition(b"\r\n\r\n")
            headers_lines = headers_raw.decode("utf-8", errors="ignore").split("\r\n")

            status_line = headers_lines[0] if headers_lines else "HTTP/1.1 Unknown"
            status_code = int(status_line.split()[1]) if len(status_line.split()) > 1 else 0

            headers = {}
            for line in headers_lines[1:]:
                if ":" in line:
                    key, val = line.split(":", 1)
                    headers[key.strip().lower()] = val.strip()

            if status_code in (301, 302, 307, 308) and "location" in headers:
                redirect_url = headers["location"]
                if redirect_url.startswith("/"):
                    redirect_url = f"{parsed.scheme}://{hostname}{redirect_url}"
                elif not redirect_url.startswith("http"):
                    redirect_url = f"{parsed.scheme}://{hostname}/{redirect_url}"
                red(f"[*] following redirect -> {redirect_url}")
                url = redirect_url
                continue

            return ip, headers, body_content, status_line

        except Exception as e:
            s.close()
            return None, None, b"", str(e)

    return None, None, b"", "Too many redirects"

def analyze_target(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    parsed = urlparse(url)
    red(f"[*] resolving host   {parsed.hostname}")
    
    ip, headers, body, status_info = fetch_url(url)

    if not headers:
        red(f"[!] connection error {status_info}")
        return

    red(f"[+] target ip      {ip}")
    red("[*] executing deep stack & vulnerability analysis...")
    sleep(0.03)

    red("")
    red(f"[-] Status Line    {status_info}")
    red(f"[-] Web Server     {headers.get('server', 'Not Disclosed / Hidden')}")
    red(f"[-] Powered-By     {headers.get('x-powered-by', 'Not Disclosed / Hidden')}")
    red(f"[-] Content-Type   {headers.get('content-type', 'Unknown')}")
    
    cookies = headers.get('set-cookie')
    if cookies:
        red("[-] Cookies Set:")
        for cookie in cookies.split(','):
            c_clean = cookie.strip()
            has_secure = 'secure' in c_clean.lower()
            has_httponly = 'httponly' in c_clean.lower()
            red(f"    [->] {c_clean}")
            red(f"         Secure: {has_secure} | HttpOnly: {has_httponly}")
    else:
        red("[-] Cookies Set    None / Not Explicit")

    red("")
    red("[*] Deep Tech Stack Signature Analysis:")
    body_str = body.decode("utf-8", errors="ignore").lower()
    detected_tech = []
    
    signatures = {
        "Next.js": ["__next", "_next/static", "next internal"],
        "React": ["react", "data-reactroot"],
        "Vue.js": ["vue", "data-v-"],
        "Angular": ["ng-version", "angular"],
        "WordPress": ["wp-content", "wordpress", "wp-includes"],
        "Bootstrap": ["bootstrap.min.css", "bootstrap"],
        "jQuery": ["jquery"],
        "Tailwind CSS": ["tailwindcss", "tailwind"],
        "Cloudflare": ["cf-ray", "cloudflare"],
        "Django": ["csrfmiddlewaretoken", "django"],
        "Laravel": ["laravel_session", "x-laravel"]
    }

    server_header = headers.get('server', '').lower()
    powered_header = headers.get('x-powered-by', '').lower()

    for tech, sigs in signatures.items():
        if any(s in body_str or s in server_header or s in powered_header for s in sigs):
            detected_tech.append(tech)

    if detected_tech:
        red(f"    [+] Identified     {', '.join(detected_tech)}")
    else:
        red("    [-] Identified     No explicit standard framework signatures found")

    red("")
    red("[*] Deep Security & Attack Surface Audit:")
    
    sec_headers = {
        'strict-transport-security': 'HSTS',
        'content-security-policy': 'CSP',
        'x-frame-options': 'X-Frame-Options',
        'x-content-type-options': 'X-Content-Type-Options',
        'x-xss-protection': 'X-XSS-Protection',
        'permissions-policy': 'Permissions-Policy',
        'cross-origin-opener-policy': 'COOP',
        'cross-origin-resource-policy': 'CORP'
    }

    vulns = []
    score = 0
    total_checks = len(sec_headers)

    for sh, name in sec_headers.items():
        if sh in headers:
            score += 1
            red(f"    [+] {name:<26} PRESENT")
        else:
            red(f"    [-] {name:<26} MISSING (Vulnerability Risk)")
            vulns.append(name)

    if 'x-frame-options' not in headers and 'content-security-policy' not in headers:
        vulns.append("Clickjacking Risk")
    if 'strict-transport-security' not in headers and parsed.scheme == "https":
        vulns.append("Insecure Transport (Missing HSTS)")
    if 'content-security-policy' not in headers:
        vulns.append("XSS Exposure (Missing CSP)")

    red("")
    red(f"[*] Total Security Score: {score}/{total_checks}")
    if vulns:
        red("[!] Potential Exposure Vectors:")
        for v in vulns:
            red(f"    [!] - {v}")
    else:
        red("[+] No critical header-level exposure vectors detected.")

    red("")
    red("[*] Fingerprinting completed successfully.")
    red("")

def web_fingerprint_menu():
    try:
        banner()
        red("")
        target_input = red_input("  target url / host > ").strip()
        
        if not target_input:
            red("  [-] empty target")
            return

        red("")
        analyze_target(target_input)

    except KeyboardInterrupt:
        red("")
        red("  [!] stopped")
        red("")
        sleep(0.5)

