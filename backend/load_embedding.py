from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()


def get_embedding_function():
    OPEN_AI_KEY = os.environ.get("OPEN_AI_KEY")
    if not OPEN_AI_KEY:
        raise ValueError("OpenAI API key not found in environment variables.")

    embedding = OpenAIEmbeddings(api_key=OPEN_AI_KEY, model="text-embedding-3-small")

    return embedding
