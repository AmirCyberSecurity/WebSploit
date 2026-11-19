import dns.resolver
import dns.exception
import random
import string
import sys
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

TIMEOUT = 3.0
THREADS = 20 
PROBES = 3

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
    red("  ║           SUBDOMAIN FUZZER           ║")
    red("  ║       dns-aware · wildcard-check     ║")
    red("  ╚══════════════════════════════════════╝")
    red("")

def rand_path(n=11):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))

def make_session():
    resolver = dns.resolver.Resolver()
    resolver.timeout = TIMEOUT
    resolver.lifetime = TIMEOUT
    return resolver

def one_request(session, hostname):
    try:
        answers = session.resolve(hostname, "A")
        addresses = sorted({answer.address for answer in answers})
        return addresses, hostname

    except dns.resolver.NXDOMAIN:
        return None, hostname

    except dns.resolver.NoAnswer:
        return None, hostname

    except dns.exception.DNSException:
        return "ERROR", hostname

def check_target(session, base):
    red("[*] checking target...")

    try:
        session.resolve(base, "SOA")
        red(f"[+] domain verified | {base}")
        return True

    except Exception as e:
        red(f"[!] target verification failed: {type(e).__name__}")
        red("[!] abort")
        return False

def probe(session, base):
    errors = 0

    red("[*] checking wildcard DNS")

    for _ in range(PROBES):
        hostname = f"{rand_path()}.{base}"
        addresses, _ = one_request(session, hostname)

        if addresses == "ERROR":
            errors += 1
            red(f"    DNS ERROR       {hostname}")

        elif addresses:
            red(f"    WILDCARD        {hostname}")
            red("")
            red("[!] wildcard DNS detected")
            red("[!] results may contain false positives")
            red("[!] fuzzing aborted")
            return False

        else:
            red(f"    NXDOMAIN        {hostname}")

    if errors == PROBES:
        red("")
        red("[!] all probes failed - abort")
        return False

    return True

def run_fuzz(base, wordlist_path):
    if not wordlist_path.exists():
        red(f"[-] wordlist missing : {wordlist_path}")
        return

    with open(wordlist_path, encoding="utf-8") as file:
        words = [
            line.strip().lower()
            for line in file
            if line.strip() and not line.startswith("#")
        ]

    words = list(dict.fromkeys(words))

    if not words:
        red("[-] wordlist is empty")
        return

    session = make_session()
    pool = None

    try:
        if not check_target(session, base):
            return

        if not probe(session, base):
            return

        hosts = [f"{word}.{base}" for word in words]

        total = len(hosts)

        red("")
        red(f"[*] starting fuzz | targets: {total} | threads: {THREADS}")
        red("[*] press Ctrl+C to stop")
        red("─" * 48)

        found = 0

        pool = ThreadPoolExecutor(max_workers=THREADS)

        futs = [
            pool.submit(one_request, session, hostname)
            for hostname in hosts
        ]

        for future in as_completed(futs):
            addresses, hostname = future.result()

            if not addresses or addresses == "ERROR":
                continue

            found += 1

            red(f"[+] {hostname:<35} {', '.join(addresses)}")

        red("─" * 48)
        red(f"[*] finished | resolved subdomains: {found}")
        red("")

    except KeyboardInterrupt:
        red("")
        red("[!] stopped by user")
        red("")

    finally:
        if pool is not None:
            pool.shutdown(wait=False, cancel_futures=True)

def subdomain_fuzz_menu():
    try:
        banner()

        red("  ────────────────")
        red("  [1]  small.txt")
        red("  [2]  medium.txt")
        red("  [3]  large.txt")
        red("  [0]  back")
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

        base = red_input("  target domain > ").strip().lower().rstrip(".")

        if base.lower().startswith(("http://", "https://")):
            red("  [!] Enter domain only, without HTTP/HTTPS.")
            red("  [!] Example: example.com")
            return
        
        if not base:
            red("  [-] empty domain")
            return

        red("")
        wordlist = Path(__file__).resolve().parent.parent / "lists/subdomain_list" / mapping[choice]

        if not wordlist.exists():
            wordlist = Path("subdomain_list") / mapping[choice]

        if not wordlist.exists():
            wordlist = Path(mapping[choice])

        red(f"  wordlist : {mapping[choice]}")
        red(f"  target   : {base}")
        red("")

        run_fuzz(base, wordlist)

    except KeyboardInterrupt:
        red("")
        red("  [!] stopped")
        red("")
        sleep(0.5)

