<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&duration=2500&pause=1000&color=FF3030&center=true&vCenter=true&width=1000&height=100&lines=%24+WEBSPLOIT;%24+WEB+SECURITY+TOOLKIT;%24+RECONNAISSANCE+%26+VULNERABILITY+ANALYSIS;%24+LINUX+%26+WINDOWS" alt="WebSploit Banner">

<br>

# WebSploit

**Web Security Toolkit**

Reconnaissance • Vulnerability Analysis • Network Discovery

<br>

<a href="https://github.com/AmirCyberSecurity/WebSploit/stargazers">
<img src="https://img.shields.io/github/stars/AmirCyberSecurity/WebSploit?style=for-the-badge&logo=github&logoColor=white&label=STARS&labelColor=151515&color=ff3030" alt="GitHub Stars">
</a>
<a href="https://github.com/AmirCyberSecurity/WebSploit/issues">
<img src="https://img.shields.io/github/issues/AmirCyberSecurity/WebSploit?style=for-the-badge&logo=github&logoColor=white&label=ISSUES&labelColor=151515&color=ff8c00" alt="GitHub Issues">
</a>
<a href="https://www.python.org/">
<img src="https://img.shields.io/badge/PYTHON-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=151515" alt="Python">
</a>
<a href="https://github.com/AmirCyberSecurity/WebSploit">
<img src="https://img.shields.io/badge/PLATFORM-LINUX%20%2F%20WINDOWS-2ea44f?style=for-the-badge&logo=linux&logoColor=white&labelColor=151515" alt="Platform">
</a>

<br><br>

<a href="#overview"><img src="https://img.shields.io/badge/OVERVIEW-151515?style=flat-square&logo=readme&logoColor=ff3030" alt="Overview"></a>
<a href="#features"><img src="https://img.shields.io/badge/FEATURES-151515?style=flat-square&logo=hackthebox&logoColor=ff3030" alt="Features"></a>
<a href="#installation"><img src="https://img.shields.io/badge/INSTALLATION-151515?style=flat-square&logo=linux&logoColor=ff3030" alt="Installation"></a>
<a href="#usage"><img src="https://img.shields.io/badge/USAGE-151515?style=flat-square&logo=gnubash&logoColor=ff3030" alt="Usage"></a>
<a href="#preview"><img src="https://img.shields.io/badge/PREVIEW-151515?style=flat-square&logo=github&logoColor=ff3030" alt="Preview"></a>

</div>

---

## Overview

WebSploit is a Python-based Web Security Toolkit that combines reconnaissance, network discovery, and vulnerability analysis in a single command-line interface.

Designed for cybersecurity enthusiasts, penetration testers, and security researchers, WebSploit provides a convenient environment for exploring web technologies, discovering network services, and testing for potential web application vulnerabilities.

## Features

| Module | Description |
|:--|:--|
| Directory Fuzzing | Discover accessible directories and web resources |
| Subdomain Fuzzing | Identify potential subdomains associated with a target domain |
| Port Scanner | Scan network ports and check service availability |
| LAN Discovery | Discover devices on a local network |
| Web Fingerprinting | Identify technologies used by web applications |
| SQLi Scanner | Check for potential SQL injection vulnerabilities |
| XSS Scanner | Probe web applications for potential cross-site scripting vulnerabilities |
| L7 DoS | Perform controlled application-layer stress testing in isolated lab environments |

## Platform Support

<div align="center">

<img src="https://img.shields.io/badge/KALI_LINUX-SUPPORTED-557C94?style=for-the-badge&logo=kalilinux&logoColor=white" alt="Kali Linux">
<img src="https://img.shields.io/badge/LINUX-SUPPORTED-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux">
<img src="https://img.shields.io/badge/WINDOWS-SUPPORTED-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows">

</div>

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AmirCyberSecurity/WebSploit.git
```

### 2. Enter the Project Directory

```bash
cd WebSploit
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## Usage

### Standard Launch

```bash
python websploit.py
```

### Quick Launch

```bash
python launch.py
```

The launcher is designed to install dependencies and start WebSploit automatically.

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

<div align="center">

<img src="./image.png" width="90%" alt="WebSploit Command-Line Interface">

<br>

**WebSploit Command-Line Interface**

</div>

## Use Cases

- Web application reconnaissance
- Network discovery in authorized environments
- Web technology identification
- Preliminary vulnerability analysis
- Cybersecurity education and research
- Penetration testing in controlled laboratory environments

## Contributing

Contributions, bug reports, and feature suggestions are welcome.

1. Fork the repository.
2. Create a branch for your changes.
3. Implement and test your improvements.
4. Submit a pull request.

## Disclaimer

WebSploit is an educational project intended for security research and authorized penetration testing.

Only use this toolkit on systems you own or have explicit permission to test. Unauthorized access, service disruption, and unlawful use are prohibited.

The Layer 7 stress-testing module must only be used in isolated laboratory environments with explicit authorization.

The author is not responsible for damage or misuse resulting from unauthorized activity.

## Support

<div align="center">

If WebSploit is useful to you, consider supporting the project with a GitHub star.

<a href="https://github.com/AmirCyberSecurity/WebSploit/stargazers">
<img src="https://img.shields.io/badge/STAR_ON_GITHUB-ff3030?style=for-the-badge&logo=github&logoColor=white&labelColor=151515" alt="Star WebSploit on GitHub">
</a>

<br><br>

**WEBSPLOIT**

<sub>Web Security Toolkit for Authorized Security Research</sub>

</div>
