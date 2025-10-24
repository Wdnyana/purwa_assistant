import click
import os
from .utils import load_api_key
from .indexer import run_indexing
from .querier import run_query

@click.group()
def main():
    """
    Purwa-Assistant v0.1: Asisten AI yang sadar konteks proyek Anda.
    
    API Key akan dimuat dari file .env di direktori tempat Anda
    menjalankan perintah ini.
    """
    try:
        load_api_key()
    except ValueError as e:
        click.secho(str(e), fg='red')
        exit(1)

@main.command()
@click.option('--path', default='.', help='Path ke direktori proyek. Defaultnya adalah direktori saat ini.')
def index(path):
    """Meng-index sebuah proyek: Membaca dan menyimpan 'memori'-nya."""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
      click.secho("Error: GEMINI_API_KEY tidak ditemukan di Environtment variabel.", fg='red')
      exit(1)
      
    run_indexing(path, api_key)

@main.command()
@click.argument('question', nargs=-1)
def ask(question):
    """Mengajukan pertanyaan ke AI berdasarkan proyek yang sudah di-index."""
    if not question:
        click.echo("Anda harus memberikan pertanyaan.", err=True)
        
        return
        
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
      click.secho("Error: GEMINI_API_KEY tidak ditemukan di Environtment variabel.", fg='red')
      exit(1)
      
    question_text = " ".join(question)
    run_query(question_text, api_key)

if __name__ == "__main__":
    main()