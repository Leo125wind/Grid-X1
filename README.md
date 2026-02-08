# 🌍 Grid-X: Decentralized Compute Network

**Grid-X** is an open-source "Airbnb for Computing Power." It allows users to securely rent out their idle GPU/CPU resources to others for tasks like AI training, rendering, or heavy computations.

The system uses **Docker Containers** for isolation, **Ngrok** for tunneling (no port forwarding required), and a central **Flask Registry** to manage the marketplace.


---

## 📂 Repository Structure

This repository is divided into three main components:

| Folder | Role | Description |
| :--- | :--- | :--- |
| **`GridX_Host`** | **Provider** | The software for people sharing their computer. Runs a secure Docker container and connects to the registry. |
| **`GridX_Registry`** | **Server** | The central marketplace. Tracks active nodes and provides the Web Dashboard. |
| **`GridX_User`** | **Client** | Tools for renters to connect (CLI Client + SSH scripts). |

---

## 🚀 Getting Started

To run a complete network, you need at least one **Registry** (Server) and one **Host** (Provider).

### Prerequisites
* **Python 3.x**
* **Docker Desktop** (Required for Hosts)
* **Ngrok Account** (Free tier works, but requires unique tokens for multiple nodes)

---

### 1️⃣ Setup the Registry (The Marketplace)
*Run this first to create the network.*

1.  Navigate to the `GridX_Registry` folder.
2.  **Windows:** Double-click `Start_Registry.bat`.
3.  **Linux/Mac:** Run `python3 registry.py`.
4.  **Copy the URL:** The terminal will display a public URL (e.g., `http://5a2b.ngrok-free.app`).
    * ⚠️ **IMPORTANT:** You must share this URL with your Hosts and Users.

---

### 2️⃣ Setup a Host (The Provider)
*Run this on the machine with the powerful GPU/CPU.*

1.  Navigate to the `GridX_Host` folder.
2.  **Configuration:**
    * Open `gridx_service.py` in a text editor.
    * Find `REGISTRY_URL = "http://127.0.0.1:5000"`.
    * **Replace it** with the Public URL from the Registry (Step 1).
3.  **Launch:**
    * **Windows:** Double-click `Start_Host.bat`.
    * **Linux:** Run `./Start_Host.sh` (ensure permissions with `chmod +x`).
4.  **Verify:**
    * A green icon will appear in your System Tray.
    * The node should now be visible on the Registry Dashboard.

**Features:**
* **Auto-GPU Detection:** Passes NVIDIA GPUs to the container automatically.
* **Busy Status:** Hides connection details when a user is logged in.
* **Self-Healing:** Automatically restarts the container if it crashes.

---

### 3️⃣ Connect as a User (The Renter)
*Access the compute power and transfer files.*

#### Method A: Web Dashboard (Easiest)
1.  Open the **Registry URL** in your browser.
2.  Find a node with status **READY 🟢**.
3.  **Connect (SSH):**
    * Click **[📋 COPY SSH]**.
    * Paste the command into your terminal:
      ```bash
      ssh renter@0.tcp.in.ngrok.io -p 12345
      ```
    * Enter the **Password** displayed on the dashboard card.

4.  **Transfer Files (SCP):**
    * Click **[📂 COPY SCP]** (The orange button).
    * It copies a template command like:
      ```bash
      scp -P 12345 "YOUR_FILE" renter@0.tcp.in.ngrok.io:/home/renter/
      ```
    * Paste it into your terminal, replace `"YOUR_FILE"` with your actual file path (drag and drop the file into the terminal), and hit Enter.

#### Method B: CLI Tool (Advanced)
1.  Navigate to `GridX_User`.
2.  Update `tenant.py` with the `REGISTRY_URL`.
3.  Run `Start_Client.bat` (Windows) or `./Start_Client.sh` (Linux).
4.  Use the arrow keys to select a node and connect instantly.
   
---

## 🛡️ Security Features

Grid-X is built with safety in mind for the Host:

1.  **Docker Isolation:** Users are trapped inside a container. They cannot access your host files (`C:\` or `/home`).
2.  **Time Bomb Containers:** Every session has a 24-hour lease. The container self-destructs afterwards to wipe data.
3.  **One-Time Passwords (OTP):** Every session generates a new random password.
4.  **Graceful Exit:** If the Host quits the app, the node is immediately removed from the marketplace.

---

## 🧪 Testing GPU Capabilities

To verify that the Host's GPU is accessible inside the container:

1.  Connect via SSH.
2.  Upload the `gpu_benchmark.py` script (found in `GridX_User`).
3.  Run it:
    ```bash
    python3 gpu_benchmark.py
    ```
4.  It will install PyTorch (if missing) and run a matrix multiplication stress test.

---

## ⚠️ Known Limitations (Free Tier)
* **Ngrok Limits:** Free Ngrok accounts allow only **1 active tunnel**. You cannot run the Registry AND a Host on the same computer using the same Ngrok Auth Token simultaneously.
* **Persistence:** Files created inside the container are lost when the session ends (Container is ephemeral).

---
