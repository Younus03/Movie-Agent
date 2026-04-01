from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


def normalize(text):
    """
    Normalize text for flexible matching
    """
    return text.lower().replace(":", "").replace("-", "").strip()


def check_bookmyshow_selenium(movie_name, city="hyderabad"):
    options = Options()
    options.add_argument("--headless")  # run in background
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        url = f"https://in.bookmyshow.com/explore/movies-{city}"
        print("Opening URL:", url)

        driver.get(url)

        # initial wait
        time.sleep(3)

        # 🔥 Scroll multiple times to load dynamic contents
        print("Scrolling to load all movies...")

        for i in range(4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        page_source = driver.page_source

        # Normalize content
        normalized_page = normalize(page_source)
        normalized_movie = normalize(movie_name)

        print("Searching for:", normalized_movie)

        # 🔍 Basic match is been done
        if normalized_movie in normalized_page:
            return {
                "bms_available": True,
                "movie": movie_name,
                "message": "Movie found on BookMyShow (after scroll)"
            }

        # 🔍 Fallback: partial word matching
        movie_words = normalized_movie.split()
        match_count = sum(1 for word in movie_words if word in normalized_page)

        if match_count >= max(1, len(movie_words) // 2):
            return {
                "bms_available": True,
                "movie": movie_name,
                "match_score": f"{match_count}/{len(movie_words)}",
                "message": "Partial match found on BookMyShow"
            }

        return {
            "bms_available": False,
            "movie": movie_name,
            "match_score": f"{match_count}/{len(movie_words)}",
            "message": "Movie not found on BookMyShow"
        }

    except Exception as e:
        return {
            "bms_available": False,
            "error": str(e)
        }

    finally:
        driver.quit()