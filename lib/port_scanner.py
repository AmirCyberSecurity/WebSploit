import socket
import sys
import random
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from scapy.all import IP, TCP, sr1, conf

conf.verb = 0
TIMEOUT = 2.0
THREADS = 50

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
    red("  ║         STEALTH SYN SCANNER          ║")
    red("  ║    adaptive timing · raw sockets     ║")
    red("  ╚══════════════════════════════════════╝")
    red("")

def one_request(target_ip, port, service):
    try:
        sport = random.randint(1024, 65535)
        pkt = IP(dst=target_ip) / TCP(sport=sport, dport=port, flags="S", options=[('MSS', 1460)])
        resp = sr1(pkt, timeout=TIMEOUT, verbose=0)
        
        if resp is None:
            return port, service, False
        
        if resp.haslayer(TCP):
            flags = resp.getlayer(TCP).flags
            if flags == 0x12:
                rst = IP(dst=target_ip) / TCP(sport=sport, dport=port, flags="R")
                sr1(rst, timeout=0.3, verbose=0)
                return port, service, True
            elif flags == 0x14:
                return port, service, False
                
        return port, service, False
    except Exception:
        sleep(random.uniform(0.1, 0.4))
        return port, service, "ERROR"

def check_target(target_ip):
    red("[*] verifying host availability via TCP ping...")
    try:
        pkt = IP(dst=target_ip) / TCP(dport=80, flags="S")
        resp = sr1(pkt, timeout=1.5, verbose=0)
        if resp is not None:
            red(f"[+] target responsive | {target_ip}")
            return True
        else:
            red(f"[!] host did not reply, proceeding anyway...")
            return True
    except Exception as e:
        red(f"[!] target anomaly detected: {type(e).__name__}")
        red("[+] switching to adaptive stealth timings")
        return True

def run_fuzz(target_ip, wordlist_path):
    if not wordlist_path.exists():
        red(f"[-] wordlist missing : {wordlist_path}")
        return

    with open(wordlist_path, encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith("#")]

    ports_data = []
    seen_ports = set()
    for line in lines:
        parts = line.split(maxsplit=1)
        try:
            p = int(parts[0])
            if 1 <= p <= 65535 and p not in seen_ports:
                seen_ports.add(p)
                s = parts[1] if len(parts) > 1 else ""
                ports_data.append((p, s))
        except ValueError:
            continue

    if not ports_data:
        red("[-] wordlist is empty or invalid")
        return

    total = len(ports_data)

    red("")
    red(f"[*] launching stealth scan | targets: {total} | threads: {THREADS}")
    red("[*] press Ctrl+C to stop")
    red("─" * 48)

    found = 0
    pool = None

    try:
        if not check_target(target_ip):
            return

        pool = ThreadPoolExecutor(max_workers=THREADS)
        futs = []
        
        for port, service in ports_data:
            futs.append(pool.submit(one_request, target_ip, port, service))

        for future in as_completed(futs):
            res = future.result()
            if res is None:
                continue
            port, service, status = res

            if status is True:
                found += 1
                srv_str = f"({service})" if service else ""
                red(f"[+] {str(port)+'/tcp':<10} OPEN    {srv_str}")

        red("─" * 48)
        red(f"[*] finished | stealth open ports: {found}")
        red("")

    except KeyboardInterrupt:
        red("")
        red("[!] stopped by user")
        red("")

    finally:
        if pool is not None:
            pool.shutdown(wait=False, cancel_futures=True)

def port_scanner_menu():
    try:
        banner()

        red("  ──────────────────────────────")
        red("  [1] Quick Scan  (Top Ports)")
        red("  [2] Standard Scan (Common)")
        red("  [3] Deep Scan   (Full Range)")
        red("  [0] Back")
        red("  ──────────────────────────────")
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

        target_input = red_input("  target ip / host > ").strip()

        if not target_input:
            red("  [-] empty target")
            return

        try:
            target_ip = socket.gethostbyname(target_input)
        except socket.gaierror:
            red(f"  [!] Could not resolve hostname: {target_input}")
            return

        red("")

        wordlist = Path(__file__).resolve().parent.parent / "port_list" / mapping[choice]

        if not wordlist.exists():
            wordlist = Path("lists/port_list") / mapping[choice]

        if not wordlist.exists():
            wordlist = Path(mapping[choice])

        red(f"  wordlist : {mapping[choice]}")
        red(f"  target   : {target_input} ({target_ip})")
        red("")

        run_fuzz(target_ip, wordlist)

    except KeyboardInterrupt:
        red("")
        red("  [!] stopped")
        red("")
        sleep(0.5)
