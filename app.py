from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load .env locally (ignored in Azure)
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")

# Get TMDB API key from environment
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise RuntimeError("❌ TMDB_API_KEY not set. Please configure it as an environment variable.")

# Home route -> serves frontend
@app.route("/")
def home():
    return render_template("index.html")

# Search movie by name
@app.route("/search", methods=["GET"])
def search_movie():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch from TMDB"}), 500

    return jsonify(response.json())

# Recommend similar movies
@app.route("/recommend", methods=["GET"])
def recommend_movies():
    movie_id = request.args.get("movie_id")
    if not movie_id:
        return jsonify({"error": "No movie_id provided"}), 400

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={TMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch recommendations"}), 500

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
