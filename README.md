[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&pause=80&color=FF0000&center=true&vCenter=true&width=1000&lines=%24+WEBS PLOIT+SECURITY+TOOLKIT;%24+RECONNAISSANCE+%26+VULNERABILITY+ANALYSIS;%24+LINUX+%26+WINDOWS;%24+FOR+EDUCATIONAL+PURPOSES+ONLY)](https://git.io/typing-svg)

# WebSploit

**WebSploit** is a Python-based Web Security Toolkit for reconnaissance, vulnerability analysis, and network discovery. It combines multiple security modules in a single command-line interface.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-black?style=flat-square)](https://github.com/AmirCyberSecurity/WebSploit)
[![GitHub Stars](https://img.shields.io/github/stars/AmirCyberSecurity/WebSploit?style=flat-square&color=red)](https://github.com/AmirCyberSecurity/WebSploit/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/AmirCyberSecurity/WebSploit?style=flat-square&color=red)](https://github.com/AmirCyberSecurity/WebSploit/issues)

## Overview

WebSploit provides a collection of security testing modules designed for educational purposes, authorized penetration testing, and controlled laboratory environments.

The toolkit brings together web reconnaissance, network discovery, and vulnerability analysis in one place, providing a convenient interface for security research.

## Features

| Module | Description |
| :--- | :--- |
| Directory Fuzzing | Discover accessible directories and web resources. |
| Subdomain Fuzzing | Identify potential subdomains associated with a target domain. |
| Port Scanner | Scan network ports and check service availability. |
| LAN Discovery | Discover devices on a local network. |
| Web Fingerprinting | Identify technologies used by web applications. |
| SQLi Scanner | Test for potential SQL injection vulnerabilities. |
| XSS Scanner | Probe web applications for potential cross-site scripting vulnerabilities. |
| L7 DoS | Perform application-layer stress testing in isolated lab environments. |

## Platform Support

- Linux
- Windows

## Installation

Clone the repository:

```bash
git clone https://github.com/AmirCyberSecurity/WebSploit.git
```

Navigate to the project directory:

```bash
cd WebSploit
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Start WebSploit:

```bash
python websploit.py
```

## Quick Start

Run the launcher to install dependencies and start the application:

```bash
python launch.py
```

Review the launcher's behavior before executing it.

## Requirements

- Python 3
- requests
- dnspython
- scapy

Install all dependencies:

```bash
python -m pip install -r requirements.txt
```

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
  <img src="./image.png" width="100%" alt="WebSploit CLI Preview">
</p>

## Use Cases

- Web application reconnaissance
- Network discovery in authorized environments
- Web technology identification
- Security testing in laboratory environments
- Learning common web vulnerabilities
- Practicing penetration testing techniques

## Disclaimer

WebSploit is an educational project intended for security research and authorized testing.

Only use this toolkit on systems you own or have explicit permission to test. Do not use it to disrupt services or access unauthorized systems.

The L7 stress-testing module must only be used in isolated environments with explicit authorization.

The author is not responsible for damage or misuse resulting from unauthorized activity.

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

If you find an issue or have an idea for improvement, open an issue or submit a pull request through GitHub.

## Support

If you find WebSploit useful, consider starring the repository to support its development.

**WebSploit** | Web Security Toolkit
