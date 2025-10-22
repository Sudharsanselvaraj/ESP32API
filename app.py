from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Store the latest ESP32-CAM detection
latest_result = {"fruit": "None", "confidence": 0}

# Endpoint ESP32 will POST to
@app.route("/api/results", methods=["POST"])
def receive_result():
    global latest_result
    data = request.get_json()
    latest_result = data
    print("Received:", latest_result)
    return jsonify({"status": "ok"}), 200

# Endpoint to GET latest detection (for front-end)
@app.route("/api/latest", methods=["GET"])
def get_latest():
    return jsonify(latest_result)

# Simple live-updating webpage
@app.route("/")
def index():
    html = """
    <h1>🍎 ESP32-CAM Live Fruit Detection</h1>
    <div id="data">Waiting for data...</div>
    <script>
      async function update() {
        try {
          const res = await fetch('/api/latest');
          const d = await res.json();
          document.getElementById('data').innerText =
            d.fruit + ' (' + (d.confidence*100).toFixed(1) + '%)';
        } catch(err) {
          console.error(err);
        }
      }
      setInterval(update, 1000); // update every second
    </script>
    """
    return render_template_string(html)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render sets the PORT automatically
    app.run(host="0.0.0.0", port=port)
