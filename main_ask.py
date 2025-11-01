import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from src.core.pipeline import PurwaPipeline


def ask_single_question(question_string):
  """
  Mengajukan satu pertanyaan ke pipeline, 
  mencetak pertanyaan dan jawaban dalam panel, lalu keluar.
  """
  console = Console()

  console.print(Panel(question_string,
                      title="[PERTANYAAN DEVELOPER]",
                      border_style="yellow",
                      title_align="left",
                      padding=(0, 1)))

  try:
    pipeline = PurwaPipeline()
  except Exception as e:
    console.print(f"[bold red]Gagal memulai Purwa-Assistant:[/bold red] {e}")
    sys.exit(1)

  with console.status("[bold green]Purwa-Assistant sedang menganalisis konteks...[/bold green]", spinner="dots") as status:
    jawaban_md = pipeline.ask(question_string)

  console.print(Panel(Markdown(jawaban_md),
                      title="[JAWABAN PURWA-ASSISTANT]",
                      border_style="cyan",
                      title_align="left",
                      padding=(1, 2)))


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("[Error] Skrip 'main_ask.py' ini membutuhkan pertanyaan sebagai argumen.")
    print("Harap gunakan 'purwa ask \"pertanyaan Anda\"' untuk menjalankannya.")
    sys.exit(1)

  question = " ".join(sys.argv[1:])
  ask_single_question(question)
