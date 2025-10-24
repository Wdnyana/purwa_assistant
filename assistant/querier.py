import click
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain


from .config import (
    VECTOR_DB_PATH, EMBEDDING_MODEL, CHAT_MODEL, 
    RETRIEVER_K_VALUE, PROMPT_TEMPLATE
)

def run_query(question_text: str, api_key: str):
    """Fungsi utama yang dipanggil oleh CLI untuk menjalankan query."""
    project_path = Path.cwd().resolve()
    db_path = project_path / VECTOR_DB_PATH

    if not db_path.exists():
        click.secho(f"Proyek ini belum di-index! Jalankan 'purwa-cli index' terlebih dahulu.", fg='red')
        return

    click.echo("Memuat 'memori' proyek...")
    embeddings = GoogleGenerativeAIEmbeddings(
      model=EMBEDDING_MODEL,
      google_api_key=api_key
    )
    
    db = Chroma(persist_directory=str(db_path), embedding_function=embeddings)

    click.echo("Mencari konteks yang relevan dengan pertanyaan Anda...")
    retriever = db.as_retriever(search_kwargs={"k": RETRIEVER_K_VALUE}) 
    relevant_docs = retriever.get_relevant_documents(question_text)

    if not relevant_docs:
        click.echo("Tidak ditemukan konteks yang relevan di proyek ini.", err=True)
        return

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE, input_variables=["context", "question"]
    )

    click.echo("Mengirim pertanyaan dan konteks ke Gemini...")
    model = ChatGoogleGenerativeAI(
      model=CHAT_MODEL, 
      temperature=0.2,
      google_api_key=api_key
    )
    
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    
    response = chain.invoke(
        {"input_documents": relevant_docs, "question": question_text}, 
        return_only_outputs=True
    )
    
    click.secho("\n--- Jawaban Purwa-Assistant ---", fg='cyan')
    click.echo(response['output_text'])