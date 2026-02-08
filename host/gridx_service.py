import threading
import time
import subprocess
import requests
import uuid
import sys
import os
import shutil
import random
import string
from pyngrok import ngrok, conf
from pystray import Icon as TrayIcon, Menu, MenuItem as Item
from PIL import Image, ImageDraw

# --- CONFIGURATION ---
REGISTRY_URL = "http://127.0.0.1:5000\""  # CHANGE THIS TO YOUR PUBLIC URL, IF UNAWARE ASK YOUR ADMIN TO PROVIDE IT
RENTAL_PORT = 2222
NODE_ID = str(uuid.uuid4())[:8]

# Global Flags
running = True
current_otp = "LOADING..." # Store password here

def create_image():
    width = 64; height = 64
    image = Image.new('RGB', (width, height), "black")
    dc = ImageDraw.Draw(image)
    dc.ellipse((10, 10, 54, 54), fill="#00ff00")
    return image

def force_cleanup():
    subprocess.run(["docker", "rm", "-f", "gridx_session"], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_specs():
    import multiprocessing
    cpu = multiprocessing.cpu_count()
    gpu = "None"
    if shutil.which("nvidia-smi"):
        try:
            gpu = subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], encoding='utf-8').strip()
        except: pass
    return f"{cpu} CPU | {gpu}"

def get_gpu_flag():
    """Checks if NVIDIA GPU is available and returns the Docker flag"""
    # 1. Try running nvidia-smi directly
    try:
        subprocess.check_output("nvidia-smi", shell=True, stderr=subprocess.STDOUT)
        return ["--gpus", "all"] # <--- This is the magic key
    except:
        return []

def is_busy():
    """Checks if an SSH connection is active on port 2222"""
    try:
        # Windows/Linux compatible netstat check
        if os.name == 'nt':
            output = subprocess.check_output("netstat -an | findstr :2222", shell=True).decode()
        else:
            output = subprocess.check_output("netstat -an | grep :2222", shell=True).decode()
            
        if "ESTABLISHED" in output:
            return True
    except: pass
    return False

def is_container_running():
    try:
        out = subprocess.check_output(["docker", "ps", "-q", "-f", "name=gridx_session"]).strip()
        return bool(out)
    except: return False

def launch_container():
    """Launches the container and saves the password"""
    global current_otp
    force_cleanup()
    
    # 1. Generate New Password
    current_otp = ''.join(random.choices(string.digits, k=6))

    docker_flags = get_gpu_flag()
    
    # 2. Launch Docker
    cmd = [
        "docker", "run", "-d", "--rm",
        "--name", "gridx_session",
        "-p", f"{RENTAL_PORT}:22",
        "--cpus", "1.0", "--memory", "2g",
        "-e", f"OTP={current_otp}",
        "-e", "LEASE_SECONDS=3600", #1 Hour Lease (Not enforced in this MVP, but can be used by the registry for cleanup)
    ] + docker_flags + [ 
        "gridx-secure-unit" 
    ]
    subprocess.run(cmd)

def unregister_node():
    """Tells the Registry to remove us immediately"""
    try:
        print(f"[*] Unregistering Node {NODE_ID}...")
        requests.post(f"{REGISTRY_URL}/unregister", json={"id": NODE_ID}, timeout=2)
    except Exception as e:
        print(f"[!] Could not reach registry to unregister: {e}")

def start_container_logic():
    global active_session
    try:
        conf.get_default().region = "in"
        conf.get_default().monitor_thread = False
        public_url = ngrok.connect(RENTAL_PORT, "tcp").public_url
        ssh_cmd = public_url.replace("tcp://", "")
        host_addr, port = ssh_cmd.split(":")
    except Exception as e:
        return 

    print("[*] Initializing Fresh Session...")
    launch_container()
    while running:
        # Ensure container is up
        if not is_container_running():
             launch_container()
        

        # Check if someone is connected via SSH and update status accordingly
        busy = is_busy()
        status_text = "BUSY 🔴" if busy else "READY 🟢"
        safe_password = "🔒 IN USE" if busy else current_otp

        # Ping Registry with PASSWORD included
        try:
            payload = {
                "id": NODE_ID,
                "address": host_addr,
                "port": port,
                "specs": get_specs(),
                "status": status_text,
                "password": safe_password  # <--- SENDING PASSWORD NOW
            }
            requests.post(f"{REGISTRY_URL}/register", json=payload, timeout=2)
        except: pass
                 
        time.sleep(10)

def on_quit(icon, item):
    """The Shutdown Sequence"""
    global running
    running = False
    
    # 1. Stop the Icon
    icon.stop()
    
    # 2. Kill the Tunnel
    print("[*] Killing Ngrok...")
    ngrok.kill()
    
    # 3. Clean Docker
    print("[*] Cleaning Container...")
    force_cleanup()
    
    # 4. CRITICAL: Tell Registry we are leaving
    unregister_node()
    
    sys.exit(0)

def main():
    t = threading.Thread(target=start_container_logic, daemon=True)
    t.start()
    icon = TrayIcon("Grid-X", create_image(), menu=Menu(
        Item('Status: Online', lambda: None, enabled=False),
        Item('Quit Grid-X', on_quit)
    ))
    icon.run()

if __name__ == "__main__":
    main()