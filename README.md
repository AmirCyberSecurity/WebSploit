[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&pause=80&color=ff0000&center=true&vCenter=true&width=1000&lines=%24+WEB+SECURITY+TOOLKIT;%24+RECONNAISSANCE+%26+VULNERABILITY+ANALYSIS;%24+LINUX+%26+WINDOWS;%24+FOR+EDUCATIONAL+PURPOSES+ONLY)](https://git.io/typing-svg)

# WebSploit

WebSploit is a Python-based Web Security Toolkit for reconnaissance, vulnerability analysis, and network discovery. It combines multiple security modules in a single command-line interface.

## Features

- **Directory Fuzzing** - Discover accessible directories and web resources.
- **Subdomain Fuzzing** - Find subdomains associated with a domain.
- **Port Scanner** - Check network ports and service availability.
- **LAN Discovery** - Discover devices on a local network.
- **Web Fingerprinting** - Identify technologies used by web applications.
- **SQLi Scanner** - Check for potential SQL injection vulnerabilities.
- **XSS Scanner** - Probe web applications for potential XSS vulnerabilities.
- **L7 DoS** - Application-layer stress testing for isolated lab environments.

## Platform Support

- Linux
- Windows

## Installation

Clone the repository:

    git clone https://github.com/AmirCyberSecurity/WebSploit

Enter the project directory:

    cd WebSploit

Install dependencies:

    pip install -r requirements.txt

## Run

    python websploit.py

## Quick Start

Too lazy to remember two commands?

    python launch.py

The launcher automatically installs dependencies and starts WebSploit.

## Requirements

    requests
    dnspython
    scapy

Python 3 is required.

## Project Structure

    WebSploit/
    ├── lib/
    ├── lists/
    ├── image.png
    ├── launch.py
    ├── requirements.txt
    ├── websploit.py
    └── README.md

## Preview

<p align="center">
  <img src="./image.png" width="100%">
</p>

## Disclaimer

WebSploit is an educational project intended for authorized security testing and controlled lab environments.

Only use this toolkit on systems you own or have explicit permission to test. The author is not responsible for misuse or damage caused by unauthorized use.

**WebSploit** - Web Security Toolkit.
