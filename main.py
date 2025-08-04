from flask import Flask, request, jsonify
import time, requests
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
status_data = {}           # uid → last ping timestamp
webhook_url = "https://discord.com/api/webhooks/1396149633155334275/i6ZhDfay0Vt_OsSwyv_uD4K6Uy0QexqljLkJpxj69tMIg2inEZ1D1imcAkfWj0TZYzq0"  # ← Thay webhook thật của bạn

@app.route("/ping", methods=["GET"])
def ping():
    uid    = request.args.get("uid")
    source = request.args.get("source", "")

    if not uid:
        return jsonify({"status":"error","message":"Missing uid"}), 400

    now = time.time()
    status_data[uid] = now

    # Chỉ gửi webhook khi thực sự từ executor
    if source == "executor":
        key = f"_last_webhook_{uid}"
        if now - status_data.get(key, 0) > 60:
            try:
                requests.post(webhook_url, json={
                    "content": f"✅ Executor UID `{uid}` vừa online"
                }, timeout=5)
                status_data[key] = now
            except:
                pass  # giữ console sạch, không log lỗi

    return jsonify({"status":"ok"})

@app.route("/api/status/<uid>", methods=["GET"])
def status(uid):
    now  = time.time()
    last = status_data.get(uid)
    if last and now - last < 60:
        return jsonify({"uid":uid,"status":"online"})
    return jsonify({"uid":uid,"status":"offline"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)