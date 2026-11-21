[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=24&pause=80&color=ff0000&center=true&vCenter=true&width=1000&lines=%24+WEBSPL0IT+%2F%2F+WEB+SECURITY+TOOLKIT;%24+RECONNAISSANCE+%26+VULNERABILITY+ANALYSIS;%24+NETWORK+DISCOVERY+%2F%2F+WEB+SCANNING;%24+LINUX+%26+WINDOWS;%24+AUTHORIZED+SECURITY+TESTING+ONLY)](https://git.io/typing-svg)

<h1 align="center">WebSploit</h1>

<p align="center">
  <b>Web Security Toolkit for Reconnaissance, Network Discovery & Vulnerability Analysis</b>
</p>

<p align="center">
  A Python-based security toolkit that brings multiple web reconnaissance and scanning modules together in one command-line interface.
</p>

<p align="center">
  <a href="https://github.com/AmirCyberSecurity/WebSploit">
    <img src="https://img.shields.io/github/stars/AmirCyberSecurity/WebSploit?style=for-the-badge&color=red" alt="GitHub Stars">
  </a>
  <a href="https://github.com/AmirCyberSecurity/WebSploit/network/members">
    <img src="https://img.shields.io/github/forks/AmirCyberSecurity/WebSploit?style=for-the-badge&color=red" alt="GitHub Forks">
  </a>
  <a href="https://github.com/AmirCyberSecurity/WebSploit/issues">
    <img src="https://img.shields.io/github/issues/AmirCyberSecurity/WebSploit?style=for-the-badge&color=red" alt="GitHub Issues">
  </a>
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-black?style=for-the-badge" alt="Platforms">
</p>

---

## `01 // OVERVIEW`

WebSploit is an educational Python-based Web Security Toolkit designed to bring reconnaissance, network discovery, and preliminary vulnerability checks into one interface.

Instead of switching between multiple standalone scripts, users can access several security-testing modules from a single toolkit.

### Core Objectives

- Simplify common web reconnaissance tasks.
- Provide a unified interface for security utilities.
- Support learning and experimentation in controlled environments.
- Help users understand basic web and network security testing.

## `02 // FEATURES`

| Module | Description |
|---|---|
| Directory Fuzzing | Discover accessible directories and web resources. |
| Subdomain Fuzzing | Search for subdomains using configured wordlists. |
| Port Scanner | Check port availability on authorized targets. |
| LAN Discovery | Identify devices on a local network. |
| Web Fingerprinting | Identify technologies used by web applications. |
| SQLi Scanner | Perform preliminary checks for potential SQL injection. |
| XSS Scanner | Perform preliminary checks for potential cross-site scripting. |
| L7 Stress Testing | Test application resilience in isolated, authorized lab environments. |

> Detection results are preliminary findings, not proof that a vulnerability exists. Verify results before reporting them.

## `03 // PLATFORM SUPPORT`

| Platform | Support |
|---|---|
| Linux | Supported |
| Windows | Supported |
| Python 3 | Required |

Compatibility may depend on Python version, operating system, permissions, and individual module dependencies.

## `04 // INSTALLATION`

### Prerequisites

- Python 3
- Git
- Internet connection for installing dependencies

### Linux

```bash
git clone https://github.com/AmirCyberSecurity/WebSploit.git
cd WebSploit
python3 -m pip install -r requirements.txt
python3 websploit.py
```

### Windows

```powershell
git clone https://github.com/AmirCyberSecurity/WebSploit.git
cd WebSploit
py -m pip install -r requirements.txt
py websploit.py
```

### Quick Launch

WebSploit also includes a launcher:

```bash
python launch.py
```

The launcher is intended to install dependencies and start the application automatically.

Review `launch.py` before running it, especially on systems containing sensitive data.

## `05 // DEPENDENCIES`

Current project dependencies:

```text
requests
dnspython
scapy
```

Install them with:

```bash
python -m pip install -r requirements.txt
```

Some network-discovery features may require additional operating-system permissions or configuration.

## `06 // PROJECT STRUCTURE`

```text
WebSploit/
├── lib/                 # Supporting modules
├── lists/               # Wordlists and related data
├── image.png            # Project screenshot
├── launch.py            # Quick launcher
├── requirements.txt     # Python dependencies
├── websploit.py         # Main application
└── README.md            # Documentation
```

## `07 // PREVIEW`

<p align="center">
  <img src="./image.png" width="95%" alt="WebSploit application preview">
</p>

<p align="center">
  <i>WebSploit — Web Security Toolkit</i>
</p>

## `08 // ROADMAP`

Planned improvements:

- [ ] Improve error handling and input validation.
- [ ] Expand platform compatibility testing.
- [ ] Improve scan result reporting.
- [ ] Add clearer documentation for individual modules.
- [ ] Add automated tests.
- [ ] Improve dependency management.
- [ ] Document known limitations and false-positive cases.

Have an idea? Open an issue to discuss a feature or improvement.

## `09 // CONTRIBUTING`

Contributions, bug reports, and documentation improvements are welcome.

1. Fork the repository.
2. Create a branch for your changes.
3. Make and test your changes.
4. Submit a pull request describing your contribution.

For bugs, include the operating system, Python version, steps to reproduce the issue, and relevant error messages. Remove credentials and sensitive target information before submitting logs.

## `10 // SECURITY & RESPONSIBLE USE`

WebSploit is intended for educational purposes and authorized security testing.

- Test only systems you own or have explicit permission to assess.
- Use stress-testing functionality exclusively in isolated labs or other explicitly authorized environments.
- Respect applicable laws, service rules, and third-party infrastructure.
- Do not interpret scanner output as a confirmed vulnerability without further verification.

The author does not encourage unauthorized access, disruption, or damage to third-party systems.

## `11 // AUTHOR`

**AmirCyberSecurity**

GitHub: [@AmirCyberSecurity](https://github.com/AmirCyberSecurity)

Project repository: [WebSploit](https://github.com/AmirCyberSecurity/WebSploit)

---

<p align="center">
  <b>WebSploit</b>
  <br>
  <code>RECONNAISSANCE // ANALYSIS // SECURITY</code>
  <br><br>
  <i>Built for learning. Designed for authorized testing.</i>
</p>
