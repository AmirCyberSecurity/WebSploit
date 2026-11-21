<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&duration=2500&pause=1000&color=FF2020&center=true&vCenter=true&width=1000&height=100&lines=%24+WEBSPLOIT;%24+WEB+SECURITY+TOOLKIT;%24+RECONNAISSANCE+%26+VULNERABILITY+ANALYSIS;%24+LINUX+%26+WINDOWS" alt="WebSploit Banner">

<br>

# WebSploit

**Web Security Toolkit for Reconnaissance & Vulnerability Analysis**

A Python-based toolkit for web reconnaissance, vulnerability analysis, and network discovery.

<br>

<a href="https://github.com/AmirCyberSecurity/WebSploit/stargazers"><img src="https://img.shields.io/github/stars/AmirCyberSecurity/WebSploit?style=flat-square&color=red&label=STARS" alt="GitHub Stars"></a>
<a href="https://github.com/AmirCyberSecurity/WebSploit/issues"><img src="https://img.shields.io/github/issues/AmirCyberSecurity/WebSploit?style=flat-square&color=red&label=ISSUES" alt="GitHub Issues"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/PYTHON-3.x-black?style=flat-square&logo=python&logoColor=red" alt="Python"></a>
<img src="https://img.shields.io/badge/PLATFORM-LINUX%20%7C%20WINDOWS-black?style=flat-square" alt="Platform">

<br><br>

<a href="#overview">Overview</a> &nbsp; | &nbsp;
<a href="#features">Features</a> &nbsp; | &nbsp;
<a href="#installation">Installation</a> &nbsp; | &nbsp;
<a href="#usage">Usage</a> &nbsp; | &nbsp;
<a href="#preview">Preview</a>

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

| Operating System | Support |
|:--|:--:|
| Linux | Supported |
| Windows | Supported |

</div>

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AmirCyberSecurity/WebSploit.git
```

### 2. Navigate to the Project Directory

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

The launcher is designed to install the required dependencies and start WebSploit automatically.

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

<img src="./image.png" width="90%" alt="WebSploit Command-Line Interface">

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

Please ensure that contributions include appropriate documentation when necessary.

## Disclaimer

WebSploit is an educational project intended for security research and authorized penetration testing.

Only use this toolkit on systems you own or have explicit permission to test. Unauthorized access, service disruption, and unlawful use are prohibited.

The Layer 7 stress-testing module must only be used in isolated laboratory environments with explicit authorization.

The author is not responsible for damage or misuse resulting from unauthorized activity.

## Support

<div align="center">

If you find WebSploit useful, consider starring the repository.

<a href="https://github.com/AmirCyberSecurity/WebSploit">
<img src="https://img.shields.io/badge/STAR_THIS_PROJECT-181818?style=for-the-badge&logo=github&logoColor=white" alt="Star WebSploit">
</a>

<br><br>

**WEBSPLOIT**

Web Security Toolkit

</div>
