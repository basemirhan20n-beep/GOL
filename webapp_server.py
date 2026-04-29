"""
webapp_server.py — Maç Web App için mini HTTP sunucu
Bots çalışırken ayrı thread'de bu da çalışır.

Kullanım:
    python webapp_server.py
    veya bot.py içinden otomatik başlar.

Ortam değişkenleri:
    WEBAPP_PORT   → Dinlenecek port (varsayılan: 8080)
    WEBAPP_HOST   → Host (varsayılan: 0.0.0.0)
"""
import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="webapp")

WEBAPP_DIR = os.path.join(os.path.dirname(__file__), "webapp")


@app.route("/")
@app.route("/mac")
def index():
    return send_from_directory(WEBAPP_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(WEBAPP_DIR, filename)


def run_server(host="0.0.0.0", port=None):
    """Bot'tan thread olarak çağrılır."""
    # Railway PORT env'ini kullan, yoksa WEBAPP_PORT, yoksa 8080
    if port is None:
        port = int(os.getenv("PORT", os.getenv("WEBAPP_PORT", 8080)))
    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    port = int(os.getenv("PORT", os.getenv("WEBAPP_PORT", 8080)))
    host = os.getenv("WEBAPP_HOST", "0.0.0.0")
    print(f"🌐 Web App sunucu başlatıldı: http://{host}:{port}/mac")
    run_server(host, port)
