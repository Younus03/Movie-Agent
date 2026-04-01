import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


def check_movie_in_city(movie_name, city="hyderabad"):
    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": API_KEY,
        "query": movie_name
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {"error": "API request failed"}

    data = response.json()

    if not data["results"]:
        return {
            "available": False,
            "message": "No movies found"
        }

    # Normalize input
    input_clean = movie_name.lower().strip()

    exact_match = None
    suggestions = []

    for movie in data["results"]:
        title = movie["title"]
        title_clean = title.lower().strip()

        # ✅ Exact match
        if input_clean == title_clean:
            exact_match = movie
            break

        # ⚠️ Partial match → collect suggestions
        if input_clean in title_clean:
            suggestions.append(title)

    # ✅ If exact match found
    if exact_match:
        return {
            "available": True,
            "movie": exact_match["title"],
            "release_date": exact_match.get("release_date"),
            "message": "Exact match found"
        }

    # ⚠️ If only suggestions exist
    if suggestions:
        return {
            "available": False,
            "suggestions": suggestions[:3],
            "message": "No exact match. Did you mean?"
        }

    return {
        "available": False,
        "message": "Movie not found"
    }


def is_movie_now_playing(movie_name):
    url = "https://api.themoviedb.org/3/movie/now_playing"

    params = {
        "api_key": API_KEY,
        "region": "IN"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {"error": "Now playing API failed"}

    data = response.json()

    for movie in data["results"]:
        if movie_name.lower() in movie["title"].lower():
            return {
                "in_theaters": True,
                "movie": movie["title"],
                "release_date": movie.get("release_date")
            }

    return {
        "in_theaters": False,
        "movie": movie_name
    }