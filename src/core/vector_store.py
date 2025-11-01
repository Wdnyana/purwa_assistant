import sys
from src.config import CHROMA_CLIENT, COLLECTION_NAME, EMBEDDING_FUNCTION


class VectorStore:
  """
  Kelas 'wrapper' terpusat untuk mengelola semua interaksi dengan ChromaDB.
  """

  def __init__(self):
    self.client = CHROMA_CLIENT
    self.collection_name = COLLECTION_NAME
    self.embedding_function = EMBEDDING_FUNCTION
    self.collection = None  # Dimulai sebagai None (lazy load)

  def _get_or_create_collection(self):
    """
    Metode internal untuk memuat koleksi saat pertama kali dibutuhkan.
    """
    if self.collection:
      return self.collection

    try:
      # Ini akan mengambil koleksi yang ada atau membuatnya jika belum ada
      self.collection = self.client.get_or_create_collection(
          name=self.collection_name,
          embedding_function=self.embedding_function
      )

      return self.collection
    except Exception as e:
      print(f"[Error VectorStore] Gagal mendapatkan/membuat koleksi: {e}")
      raise RuntimeError(f"Gagal mendapatkan/membuat koleksi: {e}")

  def reset(self):
    """
    Menghapus koleksi lama dan membuat yang baru yang bersih.
    Ini adalah fungsi inti untuk proses indexing.
    """
    try:
      self.client.delete_collection(name=self.collection_name)
      print(f"[Info] Koleksi '{self.collection_name}' lama dihapus.")
    except Exception as e:
        # Ini normal jika koleksi belum ada
      print(f"[Info] Koleksi lama tidak ditemukan, membuat baru.")

    try:
      self.collection = self.client.create_collection(
          name=self.collection_name,
          embedding_function=self.embedding_function
      )

      print(f"[Info] Koleksi '{self.collection_name}' berhasil dibuat ulang.")
    except Exception as e:
      print(f"[Error VectorStore] Gagal membuat ulang koleksi: {e}")
      raise RuntimeError(f"Gagal membuat ulang koleksi: {e}")

  def add_batch(self, documents, metadatas, ids):
    """
    Menambahkan sekumpulan dokumen ke database vektor.
    """
    if not documents:
      return

    try:
        # Pastikan koleksi ada sebelum menambah
      col = self._get_or_create_collection()
      col.add(documents=documents, metadatas=metadatas, ids=ids)
    except Exception as e:
      print(f"[Error VectorStore] Error saat menambahkan batch: {e}")

  def query(self, query_text, n_results=7):
    """
    Mengambil 'n_results' chunk yang paling relevan dari database
    dan memformatnya menjadi string konteks.
    """
    try:
      col = self._get_or_create_collection()
      results = col.query(
          query_texts=[query_text],
          n_results=n_results
      )

      context_str = ""

      if not results or not results.get('documents') or not results['documents'][0]:
        return "Tidak ada konteks yang relevan ditemukan di database."

      sources = [meta.get('source', 'unknown')
                 for meta in results['metadatas'][0]]
      chunks = results['documents'][0]

      for i, (source, chunk) in enumerate(zip(sources, chunks)):
        context_str += f"--- Konteks {i+1} dari file: {source} ---\n"
        context_str += chunk + "\n\n"

      if not context_str:
        return "Konteks ditemukan tetapi kosong setelah diproses."

      return context_str

    except Exception as e:
      print(
          f"[Error Query Internal] Error saat melakukan query ke ChromaDB: {e}")
      return f"Error internal saat mengambil konteks: {e}"

  def get_all_source_files(self):
    """
    Mengambil semua metadata dari koleksi dan mengembalikan
    daftar unik dari 'source' (nama file).
    """
    try:
      col = self._get_or_create_collection()
      data = col.get(include=["metadatas"])

      if not data or not data.get('metadatas'):
        return []

      all_sources = [meta['source'] for meta in data['metadatas']]

      unique_sources = list(dict.fromkeys(all_sources))
      unique_sources.sort()

      return unique_sources

    except Exception as e:
      print(f"[Error VectorStore] Error saat mengambil semua metadata: {e}")
      return []
