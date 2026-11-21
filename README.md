<div align="center">

<a href="https://git.io/typing-svg">
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&duration=2500&pause=800&color=FF0000&center=true&vCenter=true&repeat=true&width=900&height=100&lines=%24+WEBS PLOIT+SECURITY+TOOLKIT;%24+RECONNAISSANCE+%26+VULNERABILITY+ANALYSIS;%24+LINUX+%26+WINDOWS;%24+FOR+EDUCATIONAL+PURPOSES+ONLY" alt="WebSploit Banner">
</a>

# WebSploit

### Web Security Toolkit

A Python-based toolkit for web reconnaissance, vulnerability analysis, and network discovery.

<br>

<a href="https://github.com/AmirCyberSecurity/WebSploit">
<img src="https://img.shields.io/github/stars/AmirCyberSecurity/WebSploit?style=for-the-badge&color=red&label=STARS" alt="GitHub Stars">
</a>
<a href="https://github.com/AmirCyberSecurity/WebSploit/issues">
<img src="https://img.shields.io/github/issues/AmirCyberSecurity/WebSploit?style=for-the-badge&color=red&label=ISSUES" alt="GitHub Issues">
</a>
<a href="https://www.python.org/">
<img src="https://img.shields.io/badge/PYTHON-3.x-red?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</a>
<img src="https://img.shields.io/badge/PLATFORM-LINUX%20%7C%20WINDOWS-black?style=for-the-badge" alt="Platform">

<br><br>

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Preview](#preview) • [Disclaimer](#disclaimer)

</div>

---

## Overview

WebSploit combines multiple security testing modules in a single command-line interface.

Designed for cybersecurity enthusiasts, penetration testers, and security researchers, it provides tools for reconnaissance, network discovery, and preliminary web vulnerability analysis.

## Features

| Module | Description |
|:--|:--|
| Directory Fuzzing | Discover accessible directories and web resources |
| Subdomain Fuzzing | Identify potential subdomains |
| Port Scanner | Scan ports and check service availability |
| LAN Discovery | Discover devices on local networks |
| Web Fingerprinting | Identify web technologies |
| SQLi Scanner | Check for potential SQL injection vulnerabilities |
| XSS Scanner | Probe for potential cross-site scripting vulnerabilities |
| L7 DoS | Conduct controlled application-layer stress testing in isolated labs |

## Platform Support

<div align="center">

| Operating System | Status |
|:--|:--:|
| Linux | Supported |
| Windows | Supported |

</div>

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/AmirCyberSecurity/WebSploit.git
```

**2. Enter the project directory**

```bash
cd WebSploit
```

**3. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

## Usage

<div align="center">

### Standard Launch

</div>

```bash
python websploit.py
```

<div align="center">

### Quick Launch

</div>

```bash
python launch.py
```

The launcher is designed to install dependencies and start the application automatically.

Review the launcher's behavior before running it.

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

<div align="center">

<img src="./image.png" width="90%" alt="WebSploit command-line interface">

WebSploit command-line interface

</div>

## Use Cases

<div align="center">

| Application | Purpose |
|:--|:--|
| Reconnaissance | Collect information about authorized targets |
| Network Discovery | Identify devices on local networks |
| Web Analysis | Identify technologies and potential vulnerabilities |
| Security Education | Practice security testing in controlled environments |

</div>

## Disclaimer

WebSploit is intended for educational purposes, authorized security assessments, and controlled laboratory environments.

Only test systems you own or have explicit permission to assess. Unauthorized access, service disruption, and unlawful use are prohibited.

The L7 stress-testing module must only be used against isolated lab targets with explicit authorization.

The author is not responsible for damage or misuse resulting from unauthorized activity.

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

Open an issue to report a problem or submit a pull request to propose an improvement.

## Support

<div align="center">

If you find WebSploit useful, consider starring the repository.

<a href="https://github.com/AmirCyberSecurity/WebSploit">
<img src="https://img.shields.io/badge/STAR%20THIS%20PROJECT-181717?style=for-the-badge&logo=github&logoColor=white" alt="Star WebSploit">
</a>

<br><br>

**WebSploit**

Web Security Toolkit

</div>
