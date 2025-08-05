# test_env.py
import os
from dotenv import load_dotenv

load_dotenv("movie_toolkit/key.env")
print("USER_AGENT:", os.getenv("USER_AGENT"))
