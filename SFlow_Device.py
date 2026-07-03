import socket
import time
import re

HOST = "192.168.168.1"
PORT = 23

USERNAME = "admin"
PASSWORD = "admin"


try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)

        s.connect((HOST, PORT))

        time.sleep(1)
        s.recv(4096)

        s.send((USERNAME + "\n").encode())

        time.sleep(1)
        s.recv(4096)

        s.send((PASSWORD + "\n").encode())

        time.sleep(2)
        s.recv(8192)

        s.send(b"show version\n")

        time.sleep(3)

        output = ""

        while True:

            try:

                chunk = s.recv(8192).decode(errors="ignore")

                if not chunk:
                    break

                output += chunk

                if "#" in chunk:
                    break

            except:
                break

        device_info = {}

        hostname_match = re.search(r"^\s*(\S+)\s+Device", output, re.MULTILINE)
        if hostname_match:
            device_info["hostname"] = hostname_match.group(1)

        location_match = re.search(r"sysLocation\s+(.+)", output)
        if location_match:
            device_info["location"] = location_match.group(1).strip()

        cpu_mac_match = re.search(r"CPU Mac\s+([0-9a-fA-F:]+)", output)
        if cpu_mac_match:
            device_info["cpu_mac"] = cpu_mac_match.group(1)

        vlan_mac_match = re.search(r"Vlan MAC\s+([0-9a-fA-F:]+)", output)
        if vlan_mac_match:
            device_info["vlan_mac"] = vlan_mac_match.group(1)

        software_match = re.search(r"SoftWare Package Version\s+(.+)", output)
        if software_match:
            device_info["software_version"] = software_match.group(1).strip()

        bootrom_match = re.search(r"BootRom Version\s+(.+)", output)
        if bootrom_match:
            device_info["bootrom_version"] = bootrom_match.group(1).strip()

        hardware_match = re.search(r"HardWare Version\s+(.+)", output)
        if hardware_match:
            device_info["hardware_version"] = hardware_match.group(1).strip()

        cpld_match = re.search(r"CPLD Version\s+(.+)", output)
        if cpld_match:
            device_info["cpld_version"] = cpld_match.group(1).strip()

        serial_match = re.search(r"Serial No\.:(.+)", output)
        if serial_match:
            device_info["serial_number"] = serial_match.group(1).strip()

        uptime_match = re.search(r"Uptime is (.+)", output)
        if uptime_match:
            device_info["uptime"] = uptime_match.group(1).strip()

        device_info["device_ip"] = HOST

except Exception as e:

        print("ERROR :", e)

        time.sleep(10)