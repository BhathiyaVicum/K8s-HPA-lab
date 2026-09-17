from flask import Flask, jsonify
import time
import os
import threading

app = Flask(__name__)

STATE = {"healthy": True, "ready": True}

@app.route("/")
def index():
    return jsonify({"message": "Hello from Kubernetes HPA lab", "pod": os.uname().nodename})

@app.route("/healthz")
def healthz():
    if STATE["healthy"]:
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "unhealthy"}), 500

@app.route("/readyz")
def readyz():
    if STATE["ready"]:
        return jsonify({"status": "ready"}), 200
    return jsonify({"status": "not ready"}), 503

@app.route("/work")
def work():
    end = time.time() + 0.3
    x = 0
    while time.time() < end:
        x += sum(i * i for i in range(1000))
    return jsonify({"result": x})

@app.route("/toggle/health")
def toggle_health():
    STATE["healthy"] = not STATE["healthy"]
    return jsonify(STATE)

@app.route("/toggle/ready")
def toggle_ready():
    STATE["ready"] = not STATE["ready"]
    return jsonify(STATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)