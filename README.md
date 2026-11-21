# WebSploit

<p align="center">
  <b>Reconnaissance. Vulnerability Analysis. Network Discovery.</b>
  <br>
  A unified security toolkit for exploring attack surfaces and analyzing web applications.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3-red?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-black?style=flat-square">
  <img src="https://img.shields.io/badge/Category-Web%20Security-red?style=flat-square">
</p>

---

## Overview

WebSploit is a Python-based Web Security Toolkit that brings reconnaissance, network discovery, and vulnerability analysis into a single command-line interface.

From discovering hidden web resources to identifying exposed ports and investigating potential vulnerabilities, WebSploit provides a centralized environment for security testing without unnecessary complexity.

```text
[ RECONNAISSANCE ]  [ NETWORK DISCOVERY ]
[ WEB ANALYSIS   ]  [ VULNERABILITY TESTING ]
```

## Features

- **Directory Fuzzing** — Discover accessible directories and web resources.
- **Subdomain Fuzzing** — Find subdomains associated with a domain.
- **Port Scanner** — Check open ports and service availability.
- **LAN Discovery** — Discover devices on a local network.
- **Web Fingerprinting** — Identify technologies used by web applications.
- **SQLi Scanner** — Check for potential SQL injection vulnerabilities.
- **XSS Scanner** — Probe web applications for potential cross-site scripting vulnerabilities.
- **L7 DoS** — Application-layer stress testing in isolated, authorized lab environments.

## Platform Support

- Linux
- Windows

## Installation

Clone the repository:

```bash
git clone https://github.com/AmirCyberSecurity/WebSploit.git
cd WebSploit
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Start WebSploit:

```bash
python websploit.py
```

### Quick Start

Prefer a single command?

```bash
python launch.py
```

The launcher automatically installs dependencies and starts WebSploit.

## Requirements

- Python 3
- requests
- dnspython
- scapy

## Project Structure

```text
WebSploit/
├── lib/
├── lists/
├── image.png
├── launch.py
├── requirements.txt
├── websploit.py
└── README.md
```

## Preview

<p align="center">
  <img src="./image.png" width="100%" alt="WebSploit Preview">
</p>

## Disclaimer

WebSploit is an educational project intended for authorized security testing and controlled laboratory environments.

Only use this toolkit on systems you own or have explicit permission to test. The author is not responsible for misuse or damage caused by unauthorized use.

---

<p align="center">
  <b>WebSploit</b> — Web Security Toolkit
  <br>
  <sub>Discover the surface. Analyze the exposure. Understand the risk.</sub>
</p>
