import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from src.core.vector_store import VectorStore


def list_indexed_files():
  """
  Mengambil dan menampilkan semua file unik yang telah diindeks
  langsung dari database vektor.
  """
  console = Console()

  with console.status("[bold green]Mengambil data dari database...[/bold green]"):
    try:
        # 1. Inisialisasi VectorStore
      store = VectorStore()

      # 2. Panggil metode baru untuk mendapatkan semua file
      # (Metode ini akan kita tambahkan di langkah berikutnya)
      file_list = store.get_all_source_files()

      if not file_list:
        console.print(Panel("[yellow]Database kosong. Tidak ada file yang ditemukan.[/yellow]",
                            title="[INFO]",
                            border_style="yellow"))

        return

    except Exception as e:
      console.print(
          f"[bold red]Gagal mengambil data dari VectorStore:[/bold red] {e}")
      console.print(
          "Pastikan Anda sudah menjalankan 'purwa index' setidaknya sekali.")
      sys.exit(1)

  # 3. Siapkan tampilan output yang rapi
  output_text = Text()
  for i, file_path in enumerate(file_list):
    output_text.append(f"{i+1}. {file_path}\n")

  console.print(Panel(
      output_text,
      title=f"[JAWABAN PURWA-ASSISTANT] - Total {len(file_list)} File Terindeks",
      border_style="cyan",
      title_align="left",
      padding=(1, 2)
  ))


if __name__ == "__main__":
  list_indexed_files()
