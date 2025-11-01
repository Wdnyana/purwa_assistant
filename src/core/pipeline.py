import ollama

from src.config import GENERATION_MODEL_NAME
from src.core.vector_store import VectorStore

PROMPT_TEMPLATE = """
[PERILAKU DAN PERSONA]
Anda adalah Purwa-Assistant, seorang arsitek software dan AI Engineer senior yang ahli dan sangat teliti.
Tugas Anda adalah menjawab pertanyaan developer secara ketat berdasarkan konteks dari file proyek yang disediakan di bawah ini.
Jawablah dengan bersih, akurat, dan profesional. Selalu merujuk ke file yang relevan jika memungkinkan (contoh: 'Seperti yang terlihat di `auth.py`, fungsi X...').
Gunakan format Markdown untuk jawaban Anda (poin, bold, blok kode) agar mudah dibaca.

[ATURAN PENTING]
1.  Fokus hanya pada pertanyaan yang diajukan.
2.  JANGAN PERNAH mengarang, menebak, atau memberikan jawaban jika konteks di bawah ini tidak menyediakan informasi yang cukup.
3.  Jika jawaban tidak ada dalam konteks, katakan dengan jujur, "Maaf, saya tidak menemukan informasi spesifik mengenai hal tersebut di dalam konteks file yang saya proses."
4.  JANGAN memberikan informasi atau pengetahuan di luar konteks yang diberikan.
5.  **WAJIB SELALU JAWAB DALAM BAHASA INDONESIA.**

[KONTEKS DARI FILE PROYEK]
{konteks}
"""


class PurwaPipeline:
  """
  Kelas "Otak" yang menyatukan VectorStore dan Model Generatif LOKAL (Ollama).
  """

  def __init__(self):
    try:
      self.vector_store = VectorStore()
      self.generation_model = GENERATION_MODEL_NAME
      print(
          f"[Info] PurwaPipeline (Ollama: {self.generation_model}) berhasil diinisialisasi.")
    except Exception as e:
      raise RuntimeError(f"Gagal inisialisasi PurwaPipeline: {e}")

  def generate_response(self, question, chat_history):
    # sourcery skip: extract-method, remove-redundant-fstring
    """
    Metode utama untuk menjalankan RAG pipeline, baik dengan atau tanpa ingatan.

    Args:
      question (str): Pertanyaan baru dari pengguna.
      chat_history (list): Daftar percakapan sebelumnya.
    """
    try:
      konteks = self.vector_store.query(question)

      if konteks.startswith("Error internal"):
        print(
            f"[Peringatan Pipeline] Query gagal, membatalkan panggilan ke AI.")
        return f"Maaf, terjadi error saat mengambil data dari database. {konteks}"

      system_prompt = PROMPT_TEMPLATE.format(konteks=konteks)

      messages = [
          {'role': 'system', 'content': system_prompt}
      ]

      messages.extend(chat_history)

      messages.append(
          {'role': 'user', 'content': question}
      )

      response = ollama.chat(
          model=self.generation_model,
          messages=messages
      )

      return response['message']['content']

    except Exception as e:
      print(f"\n[DEBUG] Terjadi error dari Ollama. Detail error:")
      print(f"Tipe Error: {type(e)}")
      print(f"Isi Error: {str(e)}\n")

      if "connection refused" in str(e).lower():
        return "Error: Tidak bisa terhubung ke Ollama. Pastikan aplikasi Ollama sudah berjalan."

      return f"Error tidak dikenal saat memproses jawaban: {e}"
