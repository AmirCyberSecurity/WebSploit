import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS = os.path.join(BASE_DIR, "requirements.txt")
SCRIPT = os.path.join(BASE_DIR, "websploit.py")


def main():
    print("[*] Initializing WebSploit...")

    if not os.path.isfile(REQUIREMENTS):
        print("[!] requirements.txt not found.")
        sys.exit(1)

    if not os.path.isfile(SCRIPT):
        print("[!] websploit.py not found.")
        sys.exit(1)

    print("[*] Installing dependencies...")

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS],
            check=True,
            cwd=BASE_DIR
        )
    except subprocess.CalledProcessError:
        print("[!] Failed to install dependencies.")
        sys.exit(1)

    print("[+] Dependencies installed.")

    os.system("cls" if os.name == "nt" else "clear")

    print("[*] Starting WebSploit...")

    try:
        subprocess.run(
            [sys.executable, SCRIPT],
            cwd=BASE_DIR
        )
    except OSError as error:
        print(f"[!] Failed to launch WebSploit: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
