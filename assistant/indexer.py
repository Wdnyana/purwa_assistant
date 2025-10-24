import click
import shutil
from pathlib import Path
from tqdm import tqdm

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from .config import (
  VECTOR_DB_PATH, IGNORE_DIRS, IGNORE_FILES,
  EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
)
from .utils import sanitize_content

def _load_project_documents(project_path: Path):
  """Fungsi helper internal untuk memuat dan mensanitasi file."""
  click.echo(f"Memulai pemindaian di: {project_path}")
  
  all_files = []
  for ext in ["*.java", "*.py", "*.js", "*.ts", "*.svelte", "*.properties", "*.md", "*.sql", "*.xml", "*.yml"]:
      all_files.extend(project_path.rglob(ext))

  docs = []
  for file_path in tqdm(all_files, desc="Memuat file"):
      in_ignored_dir = any(ignored in file_path.parts for ignored in IGNORE_DIRS)
      if in_ignored_dir or file_path.name in IGNORE_FILES:
          continue
          
      try:
          with open(file_path, 'r', encoding='utf-8') as f:
              content = f.read()
              
          sanitized_content = sanitize_content(content)
          
          loader = TextLoader(str(file_path), encoding='utf-8')
          doc = loader.load()[0]
          doc.page_content = sanitized_content
          docs.append(doc)
          
      except Exception as e:
          click.echo(f"Peringatan: Gagal membaca {file_path}: {e}", err=True)
          
  return docs

def run_indexing(path: str, api_key: str):
  """Fungsi utama yang dipanggil oleh CLI untuk menjalankan indexing."""
  project_path = Path(path).resolve()
  db_path = project_path / VECTOR_DB_PATH
  
  if db_path.exists():
      click.echo(f"Peringatan: Database di {db_path} sudah ada. Menghapus yang lama.")
      shutil.rmtree(db_path)

  documents = _load_project_documents(project_path)
  if not documents:
      click.echo("Tidak ada dokumen yang ditemukan untuk di-index.", err=True)
      return

  click.echo(f"Ditemukan {len(documents)} file yang relevan.")

  click.echo("Memecah dokumen menjadi potongan (chunks)...")
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=CHUNK_SIZE, 
      chunk_overlap=CHUNK_OVERLAP
  )
  doc_chunks = text_splitter.split_documents(documents)
  click.echo(f"Total potongan yang akan di-index: {len(doc_chunks)}")

  click.echo("Membuat embeddings dan menyimpan ke database vektor (ChromaDB)...")
  embeddings = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=api_key

  )
  
  db = Chroma.from_documents(
      doc_chunks, 
      embeddings, 
      persist_directory=str(db_path)
  )
  db.persist()

  click.secho(f"✅ Sukses! Proyek '{project_path.name}' telah di-index di {db_path}", fg='green')