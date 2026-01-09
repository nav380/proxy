from flask import Flask, request, jsonify
import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.get("/fetch")
def fetch():
    target_url = request.args.get("url")
    if not target_url:
        return jsonify({"error": "Missing 'url' query parameter"}), 400

    try:
        result = urlparse(target_url)
        if not all([result.scheme, result.netloc]):
            return jsonify({"error": "Invalid URL"}), 400
    except Exception:
        return jsonify({"error": "Invalid URL"}), 400

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Python Proxy Server)"}
        resp = requests.get(target_url, headers=headers, timeout=15)
        try:
            return jsonify(resp.json())
        except:
            return jsonify({
                "error": "Invalid JSON from target",
                "status_code": resp.status_code,
                "content": resp.text[:500]
            }), 502

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/")
def index():
    return jsonify("test")

# 👇 IMPORTANT FOR VERCEL
def handler(request):
    return app(request.environ, lambda status, headers: None)
