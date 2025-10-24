import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from .config import SECRET_PATTERNS

def load_api_key():
    """Memuat GEMINI_API_KEY dari .env dan mengonfigurasinya."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY tidak ditemukan. Mohon set di .env file.")
    genai.configure(api_key=api_key)

def sanitize_content(content: str) -> str:
    """Membersihkan konten dari rahasia sebelum dikirim ke AI."""
    sanitized_content = content
    for pattern in SECRET_PATTERNS:
        sanitized_content = pattern.sub(r'\1="[REDACTED]"', sanitized_content)
    return sanitized_content