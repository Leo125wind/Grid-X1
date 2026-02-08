import cmd
import requests
import os
import sys
import time
import platform

def clear_screen():
    """Clears the terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_servers(registry_url):
    """Fetches the list of active nodes from the Registry"""
    try:
        resp = requests.get(f"{registry_url}/list", timeout=5)
        return resp.json()
    except requests.exceptions.RequestException:
        return None

def file_transfer_menu(target):
    """Sub-menu for uploading/downloading files via SCP"""
    while True:
        print(f"\n📂 FILE MANAGER ({target['address']})")
        print("   [1] Upload File (Local -> Remote)")
        print("   [2] Download File (Remote -> Local)")
        print("   [3] Back")
        
        choice = input("\n> ").strip()
        
        if choice == '3': return
        
        password_hint = "   (Password: gridx)"
        
        # Windows scp requires special handling for paths
        scp_cmd = "scp"
        
        if choice == '1':
            local_path = input("   Path to local file: ").strip().strip('"')
            remote_path = "/home/renter/" # Default upload folder
            
            # Construct SCP command
            cmd = f'{scp_cmd} -P {target["port"]} -o StrictHostKeyChecking=no "{local_path}" renter@{target["address"]}:{remote_path}'
            
            print(f"\n🚀 Uploading...")
            print(password_hint)
            os.system(cmd)
            
        elif choice == '2':
            remote_file = input("   Name of remote file (e.g., results.txt): ").strip()
            local_path = "." # Current directory
            
            cmd = f'{scp_cmd} -P {target["port"]} -o StrictHostKeyChecking=no renter@{target["address"]}:/home/renter/{remote_file} "{local_path}"'
            
            print(f"\n⬇️  Downloading...")
            print(password_hint)
            os.system(cmd)
            
        input("\n[Press Enter to continue]")

def main():
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║         🌍 GRID-X CLIENT (v2.1)          ║")
    print("╚══════════════════════════════════════════╝")
    
    # --- 1. CONFIGURATION ---
    # Ask user for the Lobby URL (Shared by Admin)
    print("\n[?] Enter the Registry URL provided by the Admin")
    registry_input = input("    (e.g., https://xyz.ngrok-free.app): ").strip().strip("/")
    
    if not registry_input:
        print("❌ URL cannot be empty.")
        sys.exit(1)
        
    if not registry_input.startswith("http"):
        registry_url = "https://" + registry_input
    else:
        registry_url = registry_input

    # --- 2. MAIN LOOP ---
    while True:
        clear_screen()
        print(f"📡 Connected to Lobby: {registry_url}")
        print("─"*50)
        
        servers = get_servers(registry_url)
        
        if servers is None:
            print("\n❌  Could not reach Lobby Registry.")
            print("    Check your internet or the URL.")
            input("\n[Press Enter to retry]")
            continue
            
        nodes = list(servers.items())
        
        if not nodes:
            print("\n🔍  Scanning for active nodes...")
            print("    No servers online right now.")
            print("\n    [R] Refresh   [Q] Quit")
        else:
            print(f"\n✅  Found {len(servers)} Active Nodes:\n")
            print(f"    {'#':<4} {'ID':<10} {'SPECS':<40} {'STATUS'}")
            print("    " + "─"*60)
            
            for i, (nid, data) in enumerate(nodes):
                # Highlight GPU nodes
                specs = data.get('specs', 'Unknown')
                gpu_tag = "🚀 GPU" if "GPU" in specs and "None" not in specs else "💻 CPU"
                
                print(f"    {i+1:<4} {nid:<10} {specs:<40} 🟢 Online")
                
            print("\n    [#] Connect   [T] Transfer Files   [R] Refresh   [Q] Quit")

        choice = input("\n> ").strip().lower()
        
        if choice == 'q': break
        if choice == 'r': continue
        
        # --- CONNECT LOGIC ---
        if choice.isdigit():
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(nodes):
                    target = nodes[idx][1]
                    
                    print(f"\n🚀 Initiating Secure Link to Node {nodes[idx][0]}...")
                    time.sleep(1)
                    # Updated SSH command with X11 Forwarding and Compression

                    # -Y Enable X11 Forwarding (Trusted)
                    # -C Enable Compression (Faster Graphics)
                    cmd = f"ssh -Y -C -o StrictHostKeyChecking=no renter@{target['address']} -p {target['port']}"

                    # Update the print statements to reflect the new Security
                    print(f"    Executing: {cmd}")
                    print("    (🔑 Ask Host for the 6-digit Session PIN)") # Password is no longer 'gridx'
                    print("    ------------------------------------------")
                    
                    os.system(cmd)
                    
                    input("\n[Session Ended. Press Enter to return to menu]")
            except (ValueError, IndexError):
                pass
        
        # --- FILE TRANSFER LOGIC ---
        elif choice == 't':
            srv_idx = input("    Which Server #? ")
            try:
                idx = int(srv_idx) - 1
                if 0 <= idx < len(nodes):
                    target = nodes[idx][1]
                    file_transfer_menu(target)
            except (ValueError, IndexError):
                print("❌ Invalid selection.")
                time.sleep(1)

if __name__ == "__main__":
    main()