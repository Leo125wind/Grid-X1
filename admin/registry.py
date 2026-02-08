from flask import Flask, request, jsonify, render_template
import time
import threading
import logging
import sys
from pyngrok import ngrok, conf

# Force India Region
conf.get_default().region = "in"

# Disable default logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Initialize Flask
app = Flask(__name__)
active_nodes = {}

def cleanup_loop():
    """Removes dead nodes"""
    while True:
        now = time.time()
        dead_nodes = [nid for nid, data in active_nodes.items() if now - data['last_seen'] > 60]
        for nid in dead_nodes:
            print(f" [!] Pruning Inactive Node: {nid}")
            del active_nodes[nid]
        time.sleep(10)

# --- ROUTES ---

@app.route('/')
def home():
    """The Web Dashboard"""
    # This looks for 'templates/index.html'
    return render_template('index.html', nodes=active_nodes)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    node_id = data.get('id')
    if not node_id: return jsonify({"error": "No ID"}), 400
    
    active_nodes[node_id] = {
        "address": data.get('address'),
        "port": data.get('port'),
        "specs": data.get('specs'),
        "status": data.get('status', 'ONLINE'),
        "password": data.get('password', 'Unknown'), # <--- SAVE PASSWORD
        "last_seen": time.time()
    }
    return jsonify({"status": "registered"})

@app.route('/unregister', methods=['POST'])
def unregister():
    data = request.json
    node_id = data.get('id')
    if node_id in active_nodes:
        del active_nodes[node_id]
        print(f" [-] Node Offline: {node_id}")
    return jsonify({"status": "removed"})

@app.route('/list', methods=['GET'])
def list_nodes():
    return jsonify(active_nodes)

if __name__ == '__main__':
    # 1. Start Cleanup Thread
    t = threading.Thread(target=cleanup_loop, daemon=True)
    t.start()

    # 2. Open Public Tunnel
    try:
        # We explicitly bind to port 5000
        public_url = ngrok.connect(5000).public_url
        print("="*60)
        print(f"🌍 GRID-X DASHBOARD ONLINE")
        print(f"   👉 CLICK HERE: {public_url}")
        print("="*60)
    except Exception as e:
        print(f"❌ Ngrok Error: {e}")
        sys.exit(1)
    
    # 3. Start Flask
    app.run(host='0.0.0.0', port=5000)