# 💻 Grid-X Client Portal (Renter)

Access high-performance compute nodes from anywhere. You can connect via the Web Dashboard or the Command Line Interface (CLI).

## 🔌 Method 1: Web Dashboard (Easiest)
1.  Ask the Admin for the **Marketplace URL**.
2.  Open it in your browser.
3.  Click **[COPY SSH]** next to a machine you like.
4.  Paste the command into your terminal (PowerShell, Command Prompt, or Terminal).
5.  Enter the **Password** shown on the dashboard card.

## ⌨️ Method 2: CLI Tool (Advanced)
1.  **Double-Click `Start_Client.bat`**.
2.  Select a node from the list using your arrow keys.
3.  The tool will auto-connect you via SSH.

## 📂 File Transfers
* **Upload:** Use the **[SCP]** button on the dashboard to get the upload command.
    * `scp -P <PORT> <YOUR_FILE> renter@<HOST_IP>:/home/renter/`
* **GUI:** Use **FileZilla** or **WinSCP**.
    * **Host:** `sftp://<HOST_IP>`
    * **Port:** `<PORT>`
    * **User:** `renter`
    * **Pass:** `<DASHBOARD_PASSWORD>`