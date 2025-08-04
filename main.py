from flask import Flask, request, jsonify
import time, requests
import os 

app = Flask(__name__)
status_data = {}
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1396149633155334275/i6ZhDfay0Vt_OsSwyv_uD4K6Uy0QexqljLkJpxj69tMIg2inEZ1D1imcAkfWj0TZYzq0"  # thay link webhook thật

@app.route("/api/ping", methods=["POST"])
def ping():
    data = request.json
    uid = str(data.get("uid"))
    if uid:
        status_data[uid] = time.time()
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "error", "reason": "no uid"}), 400

@app.route("/api/status/<uid>", methods=["GET"])
def status(uid):
    last = status_data.get(uid)
    if last and time.time() - last < 120:
        return jsonify({"uid": uid, "status": "online"}), 200
    return jsonify({"uid": uid, "status": "offline"}), 200

@app.route("/api/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        uid = data["uid"]
        username = data["username"]
        game = data.get("game", "Unknown")
        place = data.get("place", 0)

        embed = {
            "title": "✅ Executor Injected",
            "description": f"**Username:** `{username}`\n**UserID:** `{uid}`\n**Game:** `{game}`\n**PlaceID:** `{place}`",
            "color": 65280
        }

        requests.post(DISCORD_WEBHOOK, json={"embeds": [embed]})
        return jsonify({"status": "sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route("/")
def root():
    return "✅ Flask HTTPS API is running."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
