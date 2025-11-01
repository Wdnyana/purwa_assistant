import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from src.core.vector_store import VectorStore
from pathlib import Path


def build_tree(file_paths):
  """
  Membangun struktur tree (nested dict) dari daftar path file.
  """
  tree = {}

  if not file_paths:
    return tree, ""

  common_path = Path(os.path.commonpath([Path(p).parent for p in file_paths]))

  for path_str in file_paths:
    return _extracted_from_build_tree_13(path_str, common_path, tree)


# TODO Rename this here and in `build_tree`
def _extracted_from_build_tree_13(path_str, common_path, tree):
  path = Path(path_str)
  try:
    relative_path = path.relative_to(common_path)
  except ValueError:
    relative_path = path

  parts = relative_path.parts
  current_level = tree

  for i, part in enumerate(parts):
    if i == len(parts) - 1:
      current_level[part] = "file"
    else:
      if part not in current_level:
        current_level[part] = {}
      current_level = current_level[part]

  return tree, common_path.name


def format_tree(tree_dict, prefix=""):
  """
  Memformat nested dict menjadi string tree dengan ASCII.
  """
  entries = list(tree_dict.keys())
  output = Text()

  for i, entry in enumerate(entries):
    is_last = (i == len(entries) - 1)
    connector = "┗━━ " if is_last else "┣━━ "

    output.append(f"{prefix}{connector}")

    if tree_dict[entry] == "file":
      output.append(f"📄 {entry}\n", style="green")
    else:
      output.append(f"📁 {entry}\n", style="blue bold")
      extension = "    " if is_last else "┃   "
      output.append(format_tree(tree_dict[entry], prefix + extension))

  return output


def list_files_as_tree():
  """
  Mengambil semua file dari DB dan menampilkannya sebagai tree.
  """
  console = Console()

  with console.status("[bold green]Mengambil data dari database...[/bold green]"):
    try:
      store = VectorStore()
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

  tree_data, root_name = build_tree(file_list)

  header = Text(f"📦 {root_name}\n", style="bold magenta")
  tree_text = format_tree(tree_data)
  header.append(tree_text)

  console.print(Panel(
      header,
      title=f"[JAWABAN PURWA-ASSISTANT] - Total {len(file_list)} File Terindeks",
      border_style="cyan",
      title_align="left",
      padding=(1, 2)
  ))


if __name__ == "__main__":
  import os
  list_files_as_tree()
