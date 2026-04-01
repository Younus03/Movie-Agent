from openai import OpenAI
import os
from dotenv import load_dotenv

from scraper import check_movie_in_city, is_movie_now_playing
from bms_scraper import check_bookmyshow_selenium

# Load environment variables
load_dotenv()

# Initialize client (auto reads API key from .env)
client = OpenAI()


def extract_movie_name(user_input):
    """
    Extract movie name using OpenAI (NEW API)
    """
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=f"Extract ONLY the movie name from this sentence:\n\n{user_input}"
        )

        movie_name = response.output[0].content[0].text.strip()
        return movie_name

    except Exception as e:
        print("❌ Error extracting movie name:", e)
        return user_input  # fallback


def movie_agent(user_input):
    print("\n🧠 User Input:", user_input)

    # Step 1: Extract movie name
    movie_name = extract_movie_name(user_input)
    print("🎯 Extracted Movie:", movie_name)

    # Step 2: Check movie existence (STRICT MATCH)
    exist_check = check_movie_in_city(movie_name)

    # 🚨 Handle ambiguity
    if not exist_check.get("available"):
        return {
            "status": "clarification_needed",
            "message": exist_check.get("message"),
            "suggestions": exist_check.get("suggestions", [])
        }

    # Step 3: Use corrected movie name
    corrected_name = exist_check.get("movie", movie_name)
    print("✅ Corrected Movie Name:", corrected_name)

    # Step 4: Check if in theaters
    theater_check = is_movie_now_playing(corrected_name)

    # Step 5: Check BookMyShow
    bms_check = check_bookmyshow_selenium(corrected_name)

    # Step 6: Final structured response
    return {
        "status": "success",
        "movie": corrected_name,
        "exists": True,
        "in_theaters": theater_check.get("in_theaters"),
        "bookmyshow_available": bms_check.get("bms_available"),
        "details": {
            "tmdb": exist_check,
            "theaters": theater_check,
            "bookmyshow": bms_check
        }
    }