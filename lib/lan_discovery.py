import socket
import sys
from time import sleep
from scapy.all import ARP, Ether, srp, conf

R = "\033[31m"
N = "\033[0m"

def red(text):
    print(f"{R}{text}{N}")
    sleep(0.01)

def red_input(prompt):
    sys.stdout.write(f"{R}{prompt}")
    sys.stdout.flush()
    value = input()
    sys.stdout.write(N)
    return value

def banner():
    red("")
    red("  ╔══════════════════════════════════════╗")
    red("  ║             LAN DISCOVERY            ║")
    red("  ║       arp-scan · device detection    ║")
    red("  ╚══════════════════════════════════════╝")
    red("")

def get_active_network_info():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    gateway = "Unknown"
    try:
        gw_route = conf.route.route("0.0.0.0")
        if gw_route and len(gw_route) > 1:
            gateway = gw_route[1]
    except Exception:
        pass

    iface_name = "Wi-Fi / Ethernet"
    try:
        for iface in conf.ifaces.values():
            if iface.ip == local_ip:
                iface_name = iface.name
                break
    except Exception:
        pass

    parts = local_ip.split('.')
    prefix = f"{parts[0]}.{parts[1]}.{parts[2]}"
    network_subnet = f"{prefix}.0/24"
    address_range = f"{prefix}.1 - {prefix}.254"

    return {
        "interface": iface_name,
        "ip": local_ip,
        "gateway": gateway,
        "network": network_subnet,
        "range": address_range,
        "prefix": prefix
    }

def active_lan_scan(prefix):
    target_range = f"{prefix}.0/24"
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp = ARP(pdst=target_range)
    packet = ether / arp

    try:
        result = srp(packet, timeout=3, verbose=0)[0]
        devices = []
        for sent, received in result:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})
        return devices
    except Exception:
        return []

def lan_discovery_menu():
    try:
        banner()
        red("[*] Detecting network...")
        
        net_info = get_active_network_info()

        red(f"[+] Your IP: {net_info['ip']}")
        red(f"[+] Address range: {net_info['range']}")
        
        red("[*] Checking local devices...")
        
        devices = active_lan_scan(net_info['prefix'])
        
        red("")
        print(f"{R}{'IP ADDRESS':<17}{'MAC ADDRESS'}{N}")
        
        for dev in devices:
            print(f"{R}{dev['ip']:<17}{dev['mac']}{N}")
            
        red("")
        red(f"[+] Devices responding: {len(devices)}")
        red("")

    except KeyboardInterrupt:
        red("")
        red("  [!] stopped")
        red("")
        sleep(0.5)
