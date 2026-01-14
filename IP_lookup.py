import tkinter as tk
from tkinter import messagebox, filedialog
import socket
import requests
import os
import datetime
import threading
import time
import subprocess

nmap_path = None

# Custom Colors
BG_COLOR = "#440000"
FG_COLOR = "#ffffff"
BTN_COLOR = "#000000"
BTN_HOVER = "#A38585"


def get_ip_info():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_ip = requests.get('https://api.ipify.org').text
        return local_ip, public_ip
    except Exception as e:
        return "Error", str(e)

def scan_ports(ip, log_file, status_label):
    try:
        start_time = time.time()
        open_ports = []
        for port in range(1, 1025):
            status_label.config(text=f"Scanning port {port}...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()

        duration = round(time.time() - start_time, 2)

        with open(log_file, 'a') as f:
            f.write(f"\n--- Scan Results for {ip} at {datetime.datetime.now()} ---\n")
            if open_ports:
                for port in open_ports:
                    f.write(f"[+] Port {port} is open\n")
            else:
                f.write("[-] No open ports found.\n")
            f.write(f"Scan Duration: {duration} seconds\n")
            f.write("------------------------------------------\n")

        status_label.config(text=f"Scan complete in {duration} seconds.")
        messagebox.showinfo("Scan Complete", f"Scan finished in {duration} seconds. Results saved to {log_file}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def locate_nmap():
    global nmap_path
    default_paths = [
        r"C:\\Program Files (x86)\\Nmap\\nmap.exe",
        r"C:\\Program Files\\Nmap\\nmap.exe"
    ]
    for path in default_paths:
        if os.path.exists(path):
            nmap_path = path
            return path

    nmap_path = filedialog.askopenfilename(title="Select nmap.exe", filetypes=[("Executable", "*.exe")])
    return nmap_path

def run_nmap(ip, log_file, status_label):
    try:
        global nmap_path
        if not nmap_path:
            found = locate_nmap()
            if not found:
                messagebox.showerror("Error", "Nmap not found or not selected.")
                return

        start_time = time.time()
        status_label.config(text=f"Running Nmap scan on {ip}...")

        nmap_cmd = [nmap_path, "-Pn", "-sT", "-sV", ip]
        result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        duration = round(time.time() - start_time, 2)

        with open(log_file, 'a') as f:
            f.write(f"\n--- Nmap Scan for {ip} at {datetime.datetime.now()} ---\n")
            f.write(result.stdout)
            f.write(f"\nScan Duration: {duration} seconds\n")
            f.write("------------------------------------------\n")

        status_label.config(text=f"Nmap scan complete in {duration} seconds.")
        messagebox.showinfo("Nmap Scan Complete", f"Nmap scan finished. Results saved to {log_file}")

    except Exception as e:
        messagebox.showerror("Nmap Error", str(e))


def create_logs_folder():
    if not os.path.exists("logs"):
        os.makedirs("logs")

class App:
    def __init__(self, root):
        self.root = root
        root.title("Network Tool")
        root.geometry("320x260")
        root.configure(bg=BG_COLOR)
        root.resizable(False, False)

        tk.Label(root, text="Select an Option", font=("Arial", 12, "bold"), fg=FG_COLOR, bg=BG_COLOR).pack(pady=10)

        self.add_button(root, "Get IP Address", self.show_ip_info)
        self.add_button(root, "Port Scanner", self.port_scanner_interface)
        self.add_button(root, "Thorestic", self.button_thor_thorestic)

    def add_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command, width=25, bg=BTN_COLOR, fg=FG_COLOR, activebackground=BTN_HOVER)
        btn.pack(pady=5)

    def show_ip_info(self):
        local_ip, public_ip = get_ip_info()
        messagebox.showinfo("IP Information", f"Local IP: {local_ip}\nPublic IP: {public_ip}")

    def button_thor_thorestic(self):
        messagebox.showinfo("CopyRight ©", "All rights reserved to Thorestic.©")

    def port_scanner_interface(self):
        win = tk.Toplevel(self.root)
        win.title("Port Scanner")
        win.geometry("350x280")
        win.configure(bg=BG_COLOR)

        tk.Label(win, text="Enter IP to Scan:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        ip_entry = tk.Entry(win)
        ip_entry.pack(pady=5)

        status_label = tk.Label(win, text="Status: Idle", bg=BG_COLOR, fg=FG_COLOR)
        status_label.pack(pady=5)

        def start_custom_scan():
            ip = ip_entry.get()
            if not ip:
                messagebox.showwarning("Input Error", "Please enter a valid IP address.")
                return
            create_logs_folder()
            log_path = os.path.join("logs", "scan_log.txt")
            threading.Thread(target=scan_ports, args=(ip, log_path, status_label), daemon=True).start()

        def start_nmap_scan():
            ip = ip_entry.get()
            if not ip:
                messagebox.showwarning("Input Error", "Please enter a valid IP address.")
                return
            create_logs_folder()
            log_path = os.path.join("logs", "scan_log.txt")
            threading.Thread(target=run_nmap, args=(ip, log_path, status_label), daemon=True).start()

        self.add_button(win, "Start Custom Port Scan", start_custom_scan)
        self.add_button(win, "Run Nmap Scan", start_nmap_scan)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
