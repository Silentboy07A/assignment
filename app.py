from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load .env only in local dev (ignored on Azure)
load_dotenv()

app = Flask(__name__)

# Get TMDB API key from environment
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# If API key is missing, return error page instead of crashing
if not TMDB_API_KEY:
    @app.route("/")
    def missing_key():
        return "❌ TMDB_API_KEY not set. Please configure it in Azure App Settings.", 500
else:
    @app.route("/")
    def home():
        return "✅ Flask App is running with TMDB API Key set!"

    @app.route("/movies")
    def get_movies():
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify(response.json())
        return jsonify({"error": "Failed to fetch movies"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
