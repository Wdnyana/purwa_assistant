import os
import chromadb
from dotenv import load_dotenv

from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

load_dotenv()

EMBED_MODEL_NAME = "mxbai-embed-large"
GENERATION_MODEL_NAME = "deepseek-coder:6.7b"

CHROMA_PATH = "./purwa_db"
COLLECTION_NAME = "purwa_collection_local"

try:
  EMBEDDING_FUNCTION = OllamaEmbeddingFunction(
      url="http://localhost:11434/api/embeddings",
      model_name=EMBED_MODEL_NAME
  )
  print(
      f"[Info] Embedding Function (Chroma-Native: {EMBED_MODEL_NAME}) berhasil dimuat.")
except Exception as e:
  raise RuntimeError(f"Gagal inisialisasi Ollama Embedding Function: {e}")

try:
  CHROMA_CLIENT = chromadb.PersistentClient(path=CHROMA_PATH)
  print(f"[Info] Klien ChromaDB berhasil dimuat di: {CHROMA_PATH}")
except Exception as e:
  raise RuntimeError(f"Gagal inisialisasi Klien ChromaDB: {e}")
