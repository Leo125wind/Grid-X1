# 🏢 Grid-X Marketplace Server (Registry)

The central brain of the Grid-X network. This server tracks active hosts, handles heartbeats, and hosts the Web Dashboard for users.

## 🚀 Quick Start
1.  **Double-Click `Start_Registry.bat`**
2.  **Copy the Ngrok URL:**
    * The terminal will display a public URL (e.g., `http://5a2b.ngrok-free.app`).
    * **CRITICAL:** You must copy this URL and paste it into `gridx_service.py` (on Hosts) and `tenant.py` (on Clients) so they know where to connect.
3.  **Open the Dashboard:**
    * Visit the URL in your browser to see the live marketplace.

## 🔧 Troubleshooting
* **"Url not found":** Ensure `templates/index.html` exists in the `templates` folder.
* **Ngrok Error:** If the tunnel closes, restart the batch file to get a new URL (or use a static domain if you have a paid Ngrok plan).