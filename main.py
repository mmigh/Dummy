from flask import Flask
import logging
import os

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Trang web đơn giản dùng Flask để giữ host</h1>"

@app.route("/favicon.ico")
def favicon():
    return '', 204

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)