# 🌍 Grid-X Host Node (Provider)

Turn your idle computer into a secure, money-making cloud server. This package installs the background service that connects your machine to the Grid-X network.

## 🚀 Quick Start
1.  **Install Docker Desktop:** [Download Here](https://www.docker.com/products/docker-desktop/)
    * *Windows Users:* Ensure "Use WSL 2 based engine" is checked in Settings.
2.  **Double-Click `Start_Host.bat`**
    * This will verify Python, install libraries, and build the secure container.
3.  **Look for the Green Icon** in your System Tray (bottom right).
    * You are now online! Users can rent your compute power.

## ⚙️ Configuration
* **Registry URL:** If the main server changes, open `gridx_service.py` and update the `REGISTRY_URL` variable.
* **GPU Support:** Ensure you have the latest NVIDIA drivers installed. The system auto-detects GPUs.

## 🛑 How to Stop
Right-click the **Grid-X Icon** in your system tray and select **"Quit Grid-X"**. This ensures a graceful exit from the marketplace.