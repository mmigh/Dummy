from flask import Flask, request, jsonify
import time, requests, logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

status_data = {}   # uid → last ping timestamp
webhook_url = "https://discord.com/api/webhooks/1396149633155334275/i6ZhDfay0Vt_OsSwyv_uD4K6Uy0QexqljLkJpxj69tMIg2inEZ1D1imcAkfWj0TZYzq0"  # đổi webhook của bạn

@app.route("/ping", methods=["GET"])
def ping():
    uid    = request.args.get("uid")
    source = request.args.get("source", "")

    if source == "uptime":
        # chỉ để uptime robot ping server, không ảnh hưởng status
        return jsonify({"status":"ok","message":"uptime ping"}), 200

    if not uid:
        return jsonify({"status":"error","message":"Missing uid"}), 400

    now = time.time()
    status_data[uid] = now

    # chỉ gửi webhook khi thực sự từ executor
    if source == "executor":
        key = f"_last_webhook_{uid}"
        if now - status_data.get(key, 0) > 60:  # mỗi uid báo 1 lần / phút
            try:
                requests.post(webhook_url, json={
                    "content": f"✅ Executor UID `{uid}` vừa online"
                }, timeout=5)
                status_data[key] = now
            except:
                pass

    return jsonify({"status":"ok"})

@app.route("/api/status/<uid>", methods=["GET"])
def status(uid):
    now  = time.time()
    last = status_data.get(uid, 0)

    if last and now - last < 60:  # ping < 60s coi như online
        return jsonify({"uid":uid,"status":"online"})
    else:
        return jsonify({"uid":uid,"status":"offline"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
