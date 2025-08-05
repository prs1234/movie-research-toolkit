import os
from dotenv import load_dotenv

# Load from .env
env_path = os.path.join(os.path.dirname(__file__), "..", "key.env")
load_dotenv(dotenv_path=env_path)

# Force set USER_AGENT into OS environment for other libraries
os.environ["USER_AGENT"] = os.getenv("USER_AGENT", "Mozilla/5.0")

from langchain_community.document_loaders import WebBaseLoader  # Import after setting env var

def load_documents():
    urls = [
        "https://www.hollywoodreporter.com/movies/movie-news/dune-2-imax-release-date-1235545878/",
        "https://www.empireonline.com/movies/news/",
        "https://variety.com/c/film-reviews/",
        "https://www.theguardian.com/film/news"
    ]

    user_agent = os.environ["USER_AGENT"]
    print("✅ USER_AGENT being used:", repr(user_agent))

    loader = WebBaseLoader(
    urls,
    requests_kwargs={"headers": {"User-Agent": user_agent}}
    )
    return loader.load()
