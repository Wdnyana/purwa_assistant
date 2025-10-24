import re
from pathlib import Path

# --- Path & Nama ---
VECTOR_DB_PATH = ".purwa-cli-cache"

# --- Model Config ---
EMBEDDING_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-1.5-pro-latest"

# --- Indexer Config (Prinsip Keamanan) ---
IGNORE_DIRS = {
    ".git", "node_modules", "target", "build", "dist",
    ".vscode", ".idea", "__pycache__", "venv",
    VECTOR_DB_PATH  # Penting: Jangan index cache-nya sendiri!
}

IGNORE_FILES = {
    ".env", ".env.example", "package-lock.json", "yarn.lock", "poetry.lock",
    "Pipfile.lock", "dump.sql"
}

# --- Sanitizer Config (Prinsip Keamanan) ---
SECRET_PATTERNS = [
    re.compile(r'(password|secret|key|token)\s*=\s*.*', re.IGNORECASE),
    re.compile(r'("password"|"secret"|"key"|"token")\s*:\s*".*"', re.IGNORECASE)
]

# --- LangChain Config ---
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150
RETRIEVER_K_VALUE = 5 # Ambil 5 potongan (chunks) paling relevan

# --- Prompt Template ---
PROMPT_TEMPLATE = """
Anda adalah Purwa-Assistant, seorang arsitek software AI yang ahli dan teliti.
Tugas Anda adalah menjawab pertanyaan developer berdasarkan konteks dari proyek mereka.
Jawablah dengan bersih, akurat, dan merujuk ke file yang relevan jika memungkinkan.
JANGAN PERNAH mengarang jawaban jika konteks tidak menyediakan informasi.

KONTEKS YANG RELEVAN DARI PROYEK:
{context}

PERTANYAAN:
{question}

JAWABAN ANDA:
"""