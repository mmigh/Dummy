from flask import Flask, request, jsonify
import time

app = Flask(__name__)
status_data = {}  # uid -> timestamp

@app.route("/ping", methods=["GET"])
def simple_ping():
    uid = request.args.get("uid")
    if uid:
        status_data[uid] = time.time()
        print(f"[Server] Ping nhận được từ UID: {uid}")
        return jsonify({"status": "ok", "uid": uid})
    return jsonify({"status": "error", "message": "Thiếu uid"}), 400

@app.route("/api/status/<uid>", methods=["GET"])
def check_status(uid):
    now = time.time()
    last_ping = status_data.get(uid)
    if last_ping and now - last_ping < 60:
        return jsonify({"uid": uid, "status": "online"})
    else:
        return jsonify({"uid": uid, "status": "offline"})