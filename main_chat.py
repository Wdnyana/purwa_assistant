import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from src.core.pipeline import PurwaPipeline


def start_interactive_chat():
  """
  Memulai sesi chat interaktif dengan ingatan (history).
  """
  console = Console()
  console.print(Panel("[bold cyan]Purwa-Assistant (Mode Chat Interaktif)[/bold cyan]",
                      title="🤖 Purwa-Assistant",
                      subtitle="Ketik 'exit' atau 'keluar' untuk berhenti.",
                      border_style="magenta")),
  title_align = "center",

  try:
    pipeline = PurwaPipeline()
  except Exception as e:
    console.print(f"[bold red]Gagal memulai Purwa-Assistant:[/bold red] {e}")

    return

  chat_history = []

  while True:
    try:
      question = console.input("[bold yellow]Anda:[/bold yellow] ")

      if question.lower() in ['exit', 'keluar', 'q']:
        console.print(
            "[italic magenta]Purwa-Assistant nonaktif. Sampai jumpa![/italic magenta]")
        break

      if not question.strip():
        continue

      with console.status("[bold green]Purwa-Assistant sedang berpikir...[/bold green]", spinner="dots") as status:

        response_text = pipeline.generate_response(question, chat_history)

        console.print(Panel(Markdown(response_text),
                            title="[JAWABAN PURWA-ASSISTANT]",
                            border_style="cyan",
                            title_align="left",
                            padding=(1, 2)))

        # 4. Simpan ke "Ingatan"
        chat_history.append({'role': 'user', 'content': question})
        chat_history.append({'role': 'assistant', 'content': response_text})

    except KeyboardInterrupt:
      console.print(
          "\n[italic magenta]Purwa-Assistant nonaktif. Sampai jumpa![/italic magenta] \n")

      break
    except Exception as e:
      console.print(f"[bold red]Terjadi error saat chat:[/bold red] {e}")

      break


if __name__ == "__main__":
  start_interactive_chat()
