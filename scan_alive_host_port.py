import socket
import subprocess
import re


def system_exec(cmd: str):
    p = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if p.wait() == 0:
        return p.stdout.read().decode()
    else:
        print(p.stderr.read().decode())
        return None


def get_alive_host(sub_net: str):
    alive_host = []
    res = system_exec(f"nmap -sP -T4 --min-parallelism 50  {sub_net}")
    if res:
        alive_host = re.findall(
            re.compile(r"Nmap scan report for ([\d\.]*?)\nHost is up"), res
        )
        alive_host.remove(my_ip)
    return alive_host


def get_alive_host_open_port(ip_list: list):
    host_port_dict = {}
    for ip in ip_list:
        res = system_exec(f"nmap  -sS  -Pn  --min-parallelism 50 --open -T4 {ip}")
        if res:
            open_port = re.findall(re.compile(r"(\d*?)/tcp open"), res)
            if open_port:
                host_port_dict[ip] = open_port
    return host_port_dict


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
my_ip = s.getsockname()[0]
if my_ip.startswith("10"):
    net_work = "10.0.0.0/8"
elif my_ip.startswith("172"):
    net_work = ".".join(my_ip.split(".")[:-2]) + ".0.0/16"
else:
    net_work = ".".join(my_ip.split(".")[:-1]) + ".0/24"
alive_ip = get_alive_host(net_work)
if not alive_ip:
    exit(0)
host_port = get_alive_host_open_port(alive_ip)
if not host_port:
    exit(0)
print(host_port)
