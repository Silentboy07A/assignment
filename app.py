from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# ✅ Load .env only in local dev (ignored on Azure)
load_dotenv()

app = Flask(__name__)

# ✅ Get TMDB API key from environment
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise RuntimeError("❌ TMDB_API_KEY not set. Please configure it as an environment variable.")

# ----------------------------
# Home Page
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ----------------------------
# Movie Search API
# ----------------------------
@app.route("/search", methods=["GET"])
def search_movies():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch from TMDB"}), 500

    data = response.json()
    return jsonify(data)

# ----------------------------
# Popular Movies API
# ----------------------------
@app.route("/popular", methods=["GET"])
def popular_movies():
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch popular movies"}), 500

    data = response.json()
    return jsonify(data)

# ----------------------------
# Flask Entry Point
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
