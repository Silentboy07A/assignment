import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Get TMDB API Key from environment variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Root route - health check
@app.route("/")
def home():
    if not TMDB_API_KEY:
        return "❌ TMDB_API_KEY not set. Please configure it as an environment variable.", 500
    return "✅ Flask App is running with TMDB API Key set!"

# Trending Movies
@app.route("/trending")
def trending():
    if not TMDB_API_KEY:
        return jsonify({"error": "TMDB_API_KEY not set"}), 500
    
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

# Search Movies
@app.route("/search")
def search():
    if not TMDB_API_KEY:
        return jsonify({"error": "TMDB_API_KEY not set"}), 500
    
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400
    
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    return jsonify(response.json())

# Movie Recommendations
@app.route("/recommend")
def recommend():
    if not TMDB_API_KEY:
        return jsonify({"error": "TMDB_API_KEY not set"}), 500
    
    movie_id = request.args.get("movie_id")
    if not movie_id:
        return jsonify({"error": "Missing 'movie_id' parameter"}), 400
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
