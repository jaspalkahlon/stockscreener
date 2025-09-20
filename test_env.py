from dotenv import load_dotenv
import os

load_dotenv()
print("Loaded key:", os.getenv("HF_API_KEY"))

