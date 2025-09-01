from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Load API key from environment variable
API_KEY = os.getenv("05e8ec32191444924c28496f371ecabe")
BASE_URL = "https://api.themoviedb.org/3"

@app.route("/")
def home():
    if not API_KEY:
        return "❌ TMDB_API_KEY not set. Please configure it as an environment variable."
    
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=en-US&page=1"
    response = requests.get(url).json()
    movies = response.get('results', [])
    return render_template("index.html", movies=movies)

@app.route("/search", methods=["POST"])
def search():
    if not API_KEY:
        return "❌ TMDB_API_KEY not set. Please configure it as an environment variable."
    
    query = request.form.get("query")
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}"
    response = requests.get(url).json()
    movies = response.get('results', [])
    return render_template("index.html", movies=movies, query=query)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
