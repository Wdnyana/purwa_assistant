import sys
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

from src.core import file_processor
from src.core.vector_store import VectorStore


def run_indexing(project_path):
  """
  Fungsi utama untuk menjalankan proses indexing
  dengan tampilan CLI yang bagus dan arsitektur yang benar.
  """
  console = Console()
  console.print(Panel(f"[bold cyan]Memulai Indexing Proyek:[/bold cyan]\n[yellow]{project_path}[/yellow]",
                      title="Purwa-Assistant Indexer",
                      border_style="blue"))

  try:
    # 1. Inisialisasi VectorStore
    store = VectorStore()

    # 2. HAPUS database lama dan buat ulang
    # Kita panggil metode 'reset' baru yang sudah kita buat
    store.reset()

    # 3. Cari semua file yang valid
    console.print("Mencari file yang valid...")
    valid_files = file_processor.find_valid_files(project_path)

    if not valid_files:
      console.print(
          "[yellow]Tidak ada file yang didukung ditemukan di path tersebut.[/yellow]")
      return

    console.print(
        f"Ditemukan [bold green]{len(valid_files)}[/bold green] file yang akan diindeks.")

    # 4. Proses file dengan progress bar
    with Progress(console=console) as progress:
      task = progress.add_task(
          "[green]Mengindeks file...", total=len(valid_files))

      for file_path in valid_files:
        # 4a. Baca & Pecah file
        docs, metas, ids = file_processor.process_file_content(file_path)

        # 4b. Tambahkan ke database menggunakan 'store'
        if docs:
          try:
            store.add_batch(documents=docs, metadatas=metas, ids=ids)
          except Exception as e:
            console.print(
                f"\n[Kuning] Gagal menambahkan batch untuk {file_path}: {e}[/Kuning]")

        progress.update(
            task, advance=1, description=f"Memproses [cyan]{file_path.split('/')[-1]}[/cyan]")

    console.print(Panel(f"[bold green]Indexing Selesai![/bold green]\nTotal [bold]{len(valid_files)}[/bold] file telah diproses.",
                        title="Purwa-Assistant Indexer",
                        border_style="green"))

  except Exception as e:
    console.print(f"[bold red]Error besar saat indexing:[/bold red] {e}")


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("\n[Penggunaan]")
    print("python main_index.py <path_ke_folder_proyek_anda>")
    print("\n[Contoh]")
    print("python main_index.py /path/to/my/project\n")
  else:
    project_to_index = sys.argv[1]
    run_indexing(project_to_index)
