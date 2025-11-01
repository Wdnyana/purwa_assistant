import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Direktori dan file yang akan diabaikan saat indexing
IGNORED_DIRS = {
    ".git", ".github", "__pycache__", "node_modules", "venv", ".venv", "env", ".env", "build", "dist", "target", "purwa_db", ".vscode", ".idea", "package-lock.json", "yarn.lock", ".DS_Store", ".gitignore", "application-properties", ".mvn", ".caches", ".dockerignore"
}

# Hanya file dengan ekstensi ini yang akan dibaca
SUPPORTED_FILES = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".cs", ".cpp", ".c",
    ".h", ".hpp", ".rb", ".php", ".swift", ".kt", ".md", ".txt", ".json",
    ".yml", ".yaml", ".toml", ".html", ".css", ".scss", ".sql", "Dockerfile"
}


def find_valid_files(project_path):
  """
  Berjalan di seluruh folder proyek dan mengembalikan daftar path file
  yang valid (tidak diabaikan dan didukung).
  """
  valid_files = []
  for root, dirs, files in os.walk(project_path, topdown=True):
      # Abaikan direktori yang ada di IGNORED_DIRS
    dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

    for file in files:
      # Hanya proses file yang didukung
      if any(file.endswith(ext) for ext in SUPPORTED_FILES):
        full_path = os.path.join(root, file)
        valid_files.append(full_path)

  return valid_files


def process_file_content(file_path):
  """
  Membaca satu file, memecahnya menjadi potongan (chunks),
  dan menyiapkan data untuk database vektor.

  Mengembalikan: (documents, metadatas, ids)
  """

  # Pemecah teks (text splitter) untuk kode
  # Dibuat di sini agar logikanya terisolasi
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=2000,      # Ukuran maksimum per potongan
      chunk_overlap=200,    # Berapa banyak karakter tumpang tindih
      separators=["\n\n", "\n", " ", ""]  # Prioritas pemisah
  )

  try:
    with open(file_path, 'r', encoding='utf-8') as f:
      content = f.read()

    # 1. Pecah file menjadi potongan (chunks)
    chunks = text_splitter.split_text(content)

    # 2. Siapkan data untuk ChromaDB
    documents = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
      if not chunk.strip():  # Lewati chunk yang kosong
        continue

      documents.append(chunk)
      # Metadata memberi tahu kita dari mana chunk ini berasal
      metadatas.append({"source": file_path})
      # ID unik untuk setiap chunk
      ids.append(f"{file_path}_{i}")

    return documents, metadatas, ids

  except Exception as e:
    print(f"[Peringatan] Gagal memproses file {file_path}: {e}")
    return None, None, None
