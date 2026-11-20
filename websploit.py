import sys
import io
import os
from time import sleep
import webbrowser

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

from lib.directory_fuzz import directory_fuzz_menu
from lib.subdomain_fuzz import subdomain_fuzz_menu
from lib.port_scanner import port_scanner_menu
from lib.lan_discovery import lan_discovery_menu
from lib.web_fingerprint import web_fingerprint_menu
from lib.sqli_scanner import sqli_scanner_menu
from lib.dos_attack import dos_attack_menu
from lib.xss_probe import xss_probe_menu

R = "\033[31m"
N = "\033[0m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")
    sys.stdout.write("\033[3J")
    sys.stdout.flush()

def red_input(prompt):
    sys.stdout.write(f"{R}{prompt}")
    sys.stdout.flush()
    value = input()
    sys.stdout.write(N)
    return value

BANNER_LINES = [
    "\033[0;97m \033[0;31m█\033[0;97;41m▀\033[0;97m   \033[0;31m█░\033[0;37m \033[0;31m▓\033[0;97;41m ▄▄\033[0;31m██\033[0;37m   \033[0;31m▄▄▄▄\033[0;37m      \033[0;97;41m ▄▄\033[0;31m██\033[0;37m    \033[0;31m██▒███\033[0;37m    \033[0;31m██▓\033[0;37m      \033[0;31m▓█\033[0;97;41m▄▄\033[0;31m██\033[0;37m    \033[0;31m██▓\033[0;37m \033[0;31m▄▄▄█\033[0;97;41m▄\033[0;31m███▓\033[0m",
    "\033[0;31m▓█\033[0;97;41m█\033[0;31m▓█▒█░\033[0;37m \033[0;31m▓\033[0;97;41m█ \033[0;97m  \033[0;31m▀\033[0;37m  \033[0;31m▓█\033[0;97;41m▄ \033[0;31m██▄\033[0;37m  \033[0;31m▒\033[0;97;41m ▀\033[0;97m   \033[0;31m▒\033[0;37m   \033[0;31m▓\033[0;97;41m█\033[0;31m█░\033[0;97m  \033[0;31m██▓\033[0;37m \033[0;31m▓██▒\033[0;37m     \033[0;31m▓█\033[0;97;41m█\033[0;31m▒\033[0;97m  \033[0;31m██▓\033[0;37m \033[0;31m▓\033[0;97;41m▐\033[0;31m█▒\033[0;37m \033[0;31m▓\033[0;97m  \033[0;97;41m█\033[0;31m█▒\033[0;97m \033[0;31m▓▒\033[0m",
    "\033[0;31m▒█\033[0;97;41m█\033[0;31m▒█░█\033[0;37m  \033[0;31m▒\033[0;97;41m█ \033[0;31m█\033[0;37m    \033[0;31m▒\033[0;97;41m█\033[0;31m█▒\033[0;37m \033[0;31m▄██\033[0;37m \033[0;31m░\033[0;97m \033[0;31m▓██▄\033[0;37m    \033[0;31m▓\033[0;97;41m█\033[0;31m█░ ██▓▒\033[0;37m \033[0;31m▒\033[0;97;41m█\033[0;31m█░\033[0;37m     \033[0;31m▒█\033[0;97;41m█\033[0;31m░\033[0;97m  \033[0;97;41m█\033[0;31m█▒\033[0;37m \033[0;31m▒\033[0;97;41m \033[0;31m█▒\033[0;37m \033[0;31m▒\033[0;97m \033[0;31m▓\033[0;97;41m█\033[0;31m█░\033[0;97m \033[0;31m▒░\033[0m",
    "\033[0;31m░▒█░█\033[0;97m \033[0;31m█\033[0;37m  \033[0;31m▒▓█\033[0;97m  \033[0;31m▄\033[0;37m  \033[0;31m▒\033[0;97;41m▄ \033[0;31m░█▀\033[0;37m     \033[0;31m▒\033[0;97m \033[0;97;41m▄\033[0;31m█▓\033[0;37m \033[0;31m▒\033[0;97;41m▄ \033[0;31m▄█▒▓\033[0;97m \033[0;31m▒\033[0;37m \033[0;31m▒\033[0;97;41m█ \033[0;31m░\033[0;37m     \033[0;31m▒██\033[0;97m    \033[0;97;41m▄▀\033[0;31m▒░\033[0;37m \033[0;31m░\033[0;97;41m▐ \033[0;31m░\033[0;37m \033[0;31m░\033[0;97m \033[0;31m▓\033[0;97;41m▄\033[0;31m█▓\033[0;97m \033[0;31m░\033[0;37m \033[0m",
    "\033[0;31m░░██▒██▓\033[0;37m \033[0;31m░▒████▒\033[0;37m \033[0;31m░▓█\033[0;37m   \033[0;31m█▓\033[0;37m \033[0;31m▓███\033[0;97;41m▄▄▀\033[0;31m▒▒\033[0;37m \033[0;31m▒██▒\033[0;97m \033[0;31m░\033[0;97m  \033[0;31m░\033[0;37m \033[0;31m░\033[0;97;41m▄\033[0;31m█████▒\033[0;37m \033[0;31m░\033[0;97m \033[0;31m█\033[0;97;41m▀▀ \033[0;31m▓▒░\033[0;37m \033[0;31m░\033[0;97;41m▐\033[0;31m█░\033[0;37m   \033[0;31m▒██▒\033[0;97m \033[0;31m░\033[0;37m \033[0m",
    "\033[0;97m \033[0;31m░\033[0;97m \033[0;31m▓░▒\033[0;97m \033[0;31m▒\033[0;37m \033[0;31m░░\033[0;97m \033[0;31m▒░\033[0;97m \033[0;31m░\033[0;37m \033[0;31m░▒▒███▀▒\033[0;37m \033[0;31m▒\033[0;97m \033[0;31m▒▓▒\033[0;97m \033[0;31m▒\033[0;97m \033[0;31m░\033[0;37m \033[0;31m▒▓▒░\033[0;97m \033[0;31m░\033[0;97m  \033[0;31m░\033[0;37m \033[0;31m░\033[0;97m \033[0;31m▒░▓\033[0;97m  \033[0;31m░\033[0;37m \033[0;31m░\033[0;97m \033[0;31m▒░▓░▓░\033[0;37m  \033[0;31m░▓\033[0;37m     \033[0;31m▒\033[0;97m \033[0;31m░░\033[0;37m   \033[0m",
    "\033[0;97m   \033[0;31m▒\033[0;97m \033[0;31m░\033[0;97m \033[0;31m░\033[0;37m \033[0;31m ░\033[0;97m \033[0;31m░\033[0;97m  \033[0;31m░\033[0;37m \033[0;31m▒░▒\033[0;37m   \033[0;31m░\033[0;37m  \033[0;31m░\033[0;97m \033[0;31m░▒\033[0;97m  \033[0;31m░\033[0;97m \033[0;31m░\033[0;37m \033[0;31m░▒\033[0;97m \033[0;31m░\033[0;37m      \033[0;31m░\033[0;97m \033[0;31m░\033[0;97m \033[0;31m▒\033[0;97m  \033[0;31m░\033[0;37m   \033[0;31m░\033[0;97m \033[0;31m▒\033[0;97m \033[0;31m▒░\033[0;37m   \033[0;31m▒\033[0;97m \033[0;31m░\033[0;37m     \033[0;31m░\033[0;37m    \033[0m",
    "\033[0;97m   \033[0;31m░\033[0;97m   \033[0;31m░\033[0;37m \033[0;31m \033[0;97m  \033[0;31m░\033[0;37m     \033[0;31m░\033[0;37m    \033[0;31m░\033[0;37m  \033[0;31m░\033[0;97m \033[0;31m ░\033[0;97m  \033[0;31m░\033[0;37m   \033[0;31m░░\033[0;37m          \033[0;31m░\033[0;97m \033[0;31m░\033[0;37m    \033[0;31m░\033[0;97m \033[0;31m░\033[0;97m \033[0;31m░\033[0;97m \033[0;31m▒\033[0;37m   \033[0;31m▒\033[0;97m \033[0;31m░\033[0;37m   \033[0;31m░\033[0;37m      \033[0m",
    "\033[0;97m     \033[0;31m░\033[0;37m       \033[0;31m░\033[0;97m  \033[0;31m░\033[0;37m  \033[0;31m░\033[0;37m       \033[0;97m      \033[0;31m░\033[0;37m               \033[0;31m░\033[0;97m  \033[0;31m░\033[0;37m     \033[0;31m░\033[0;97m \033[0;31m░\033[0;37m   \033[0;31m░\033[0;37m            \033[0m"
]

MENU_LINES = [
    f"",
    f"{R}╭─────────────────────╮   ╭─────────────────────╮   ╭──────────────────────╮{N}",
    f"{R}│ 1. Directory Fuzz   │   │ 5. Web Fingerprint  │   │ 9. Other Projects    │{N}",
    f"{R}│ 2. Subdomain Fuzz   │   │ 6. SQLi Scanner     │   │ 10. About Project    │{N}",
    f"{R}│ 3. Port Scanner     │   │ 7. L7 DoS Attack    │   │ 11. Author Github    │{N}",
    f"{R}│ 4. LAN Discovery    │   │ 8. XSS Scanner      │   │ 12. Exit             │{N}",
    f"{R}╰─────────────────────╯   ╰─────────────────────╯   ╰──────────────────────╯{N}",
    f""
]

ABOUT_LINES = [
    f"{R}  WebSploit - Modular Web Security Framework{N}",
    f"{R}  A Python-based toolkit built for web security assessment,{N}",
    f"{R}  reconnaissance, vulnerability analysis, and network discovery.{N}",
    "",
    f"{R}  The framework combines multiple security modules{N}",
    f"{R}  into a unified command-line interface, providing a{N}",
    f"{R}  centralized environment for security testing.{N}",
    "",
    f"{R}  Its modular architecture supports independent components{N}",
    f"{R}  for analyzing web applications, network services,{N}",
    f"{R}  and potential security weaknesses.{N}",
    "",
    f"{R}  Designed for authorized penetration testing,{N}",
    f"{R}  security research, and controlled lab environments.{N}",
]

OTHER_PROJECTS_LINES = [
    f"{R}  [01] AVERON{N}",
    f"{R}  Django-based OSINT framework for IP, phone,{N}",
    f"{R}  MAC, ,domain, username, and directory lookup.{N}",
    f"{R}  Python, Django, public APIs, and black-gold UI.{N}",
    f"{R}  github.com/AmirCyberSecurity/AVERON{N}",
    "",
    f"{R}  [02] TonFlood{N}",
    f"{R}  Asynchronous HTTP stress-testing framework.{N}",
    f"{R}  Django, aiohttp, JavaScript, and RPS metrics.{N}",
    f"{R}  github.com/AmirCyberSecurity/TonFlood{N}",
    "",
    f"{R}  [03] FSOCIETY Cyber Deck{N}",
    f"{R}  Python and Flet-based cybersecurity application.{N}",
    f"{R}  Combines OSINT utilities, DoS with spoofed IP headers.{N}",
    f"{R}  github.com/AmirCyberSecurity/FSOCIETY{N}",
    "",
    f"{R}  [04] ADDoS{N}",
    f"{R}  Asynchronous Python DoS and IP Bomb utility.{N}",
    f"{R}  Developed for educational purposes.{N}",
    f"{R}  github.com/AmirCyberSecurity/ADDoS{N}"
]

def main_menu():
    while True:
        clear()

        for line in BANNER_LINES:
            sys.stdout.write(line + "\n")
            sys.stdout.flush()
            sleep(0.015)

        for line in MENU_LINES:
            print(line, flush=True)
            sleep(0.03)

        try:
            choice = red_input("root@websploit > ").strip()
        except KeyboardInterrupt:
            print(f"\n{R}[!] exit{N}")
            sleep(0.5)
            sys.exit(0)

        if choice == "1":
            directory_fuzz_menu()
            red_input("  Press enter to continue...")
            clear()

        elif choice == "2":
            subdomain_fuzz_menu()
            red_input("  Press enter to continue...")
            clear()

        elif choice == "3":
            port_scanner_menu()
            red_input("  Press enter to continue...")
            clear()

        elif choice == "4":
            lan_discovery_menu()
            red_input("  Press enter to continue...")
            clear()

        elif choice == "5":
            web_fingerprint_menu()
            red_input("  Press enter to continue...")
            clear()

        elif choice == "6":
            sqli_scanner_menu()
            red_input("  Press enter to continue...")
            clear()

        elif choice == "7":
            dos_attack_menu()
            red_input("  Press enter to continue...")
            clear()

        elif choice == "8":
            xss_probe_menu()
            red_input("  Press enter to continue...")
            clear()

        elif choice == "9":
            for line in OTHER_PROJECTS_LINES:
                if line == "":
                    print(line, flush=True)
                    sleep(2)

                else:    
                    print(line, flush=True)
                    sleep(0.03) 

            print("", flush=True)
            red_input("  Press enter to continue...")
            clear()

        elif choice == "10":
            for line in ABOUT_LINES:
                if line == "":
                    print(line, flush=True)
                    sleep(2)

                else:    
                    print(line, flush=True)
                    sleep(0.03)  

            print("", flush=True)
            red_input("  Press enter to continue...")
            clear()

        elif choice == "11":
            webbrowser.open(url="https://github.com/AmirCyberSecurity")
            print(f"  {R}https://github.com/AmirCyberSecurity{N}")
            red_input("  Press enter to continue...")
            clear()

        elif choice == "12":
            print(f"{R} Goodbye!{N}") 
            sleep(1)
            break

        else:
            clear()
            continue

if __name__ == "__main__":
    main_menu()
