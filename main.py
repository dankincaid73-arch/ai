import asyncio
import os
import time
import chromadb
import ollama
from dotenv import find_dotenv, load_dotenv
from src.ingestion.pdf_ingestion import process_pdf_pipeline
from src.ingestion.text_ingestion import ingest_text_file
from src.ingestion.url_ingestion import process_url_pipeline
from src.query.query_engine import query_tarantula

PERSONAS = {
    "1": "research assistant",
    "2": "angry rude old man",
    "3": "overly enthusiastic game show host",
}


def choose_persona(cyan, green, reset):
    """Displays persona menu."""
    print(f"\n{cyan}--- Select Tarantula Persona ---{reset}")
    for key, name in PERSONAS.items():
        print(f"[{key}] {name.title()}")
    print("[Any other key] Default (Research Assistant)")

    choice = input(f"\n{cyan}Enter choice: {reset}").strip()
    selected = PERSONAS.get(choice, "research assistant")

    msg = f"\n{green}✅ Persona locked in: {selected.upper()}{reset}"
    print(msg)
    return selected


def ensure_ollama_model(cyan, green, yellow, reset, model_name="llama3:8b"):
    """Checks model and pulls if missing."""
    print(f"{yellow}Checking model status ({model_name})...{reset}")

    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    client = ollama.Client(host=ollama_host)

    try:
        resp = client.list()

        if hasattr(resp, "models"):
            existing = [m.model for m in resp.models]
        else:
            existing = []

        # Loop prevents Black from merging the any() check
        exists = False
        for m in existing:
            is_exact = m == model_name
            is_latest = m == f"{model_name}:latest"
            is_prefix = m.startswith(model_name)

            if is_exact or is_latest or is_prefix:
                exists = True
                break

        if not exists:
            msg = f"{yellow}Model '{model_name}' missing. Pulling...{reset}"
            print(msg)
            client.pull(model_name)
            print(f"{green}✅ Model downloaded.{reset}")
        else:
            print(f"{green}✅ Model ready.{reset}")

    except Exception as e:
        print(f"❌ {yellow}Ollama setup error: {str(e)}{reset}")


def auto_ingest_samples(cyan, green, yellow, reset):
    """Auto-ingests sample sources if empty."""
    print(f"\n{cyan}--- System Initialization ---{reset}")

    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    if dotenv_path:
        project_root = os.path.dirname(dotenv_path)
    else:
        project_root = os.getcwd()

    # Split variables to prevent Black from merging lines
    raw_chroma = os.getenv("CHROMA_PATH", "./chroma_data")
    joined_path = os.path.join(project_root, raw_chroma)
    locked_chroma_path = os.path.abspath(joined_path)

    ensure_ollama_model(cyan, green, yellow, reset, model_name="llama3:8b")

    print(f"{yellow}Checking ChromaDB status...{reset}")
    try:
        client = chromadb.PersistentClient(path=locked_chroma_path)
        collection = client.get_or_create_collection(name="tarantula_docs")

        if collection.count() == 0:
            msg = f"{yellow}Database empty. Auto-ingesting...{reset}"
            print(msg)

            # Split paths to avoid length violations
            pdf_rel = "data/raw/pdf/1706.03762v7.pdf"
            pdf_path = os.path.join(project_root, pdf_rel)

            txt_rel = "data/raw/text/paul_graham_essay.txt"
            text_path = os.path.join(project_root, txt_rel)

            sample_url = "https://quotes.toscrape.com"

            if os.path.exists(pdf_path):
                process_pdf_pipeline(pdf_path)
            if os.path.exists(text_path):
                ingest_text_file(text_path)

            print(f"{yellow}Scraping URL: {sample_url}...{reset}")
            asyncio.run(process_url_pipeline(sample_url))

            print(f"{green}✅ Ingestion complete.{reset}")
        else:
            count = collection.count()
            msg = f"{green}✅ Database ready: {count} chunks.{reset}"
            print(msg)
    except Exception as e:
        print(f"❌ {yellow}DB init error: {str(e)}{reset}")


def run_cli():
    """Main CLI interaction loop."""
    cyan = "\033[96m"
    green = "\033[92m"
    yellow = "\033[93m"
    reset = "\033[0m"

    msg = f"{green}Tarantula Engine Online (type 'quit' to exit){reset}"
    print(msg)
    print("-" * 45)

    auto_ingest_samples(cyan, green, yellow, reset)
    print("-" * 45)

    current_persona = choose_persona(cyan, green, reset)
    print("-" * 45)

    while True:
        question = input(f"\n{cyan}Ask Tarantula: {reset}").strip()

        if question.lower() in ["quit", "exit"]:
            print(f"{yellow}Shutting down engine...{reset}")
            break

        if not question:
            continue

        print(f"{yellow}Thinking...{reset}")
        start_time = time.time()

        try:
            answer = query_tarantula(question, persona=current_persona)
            end_time = time.time()
            duration = round(end_time - start_time, 2)

            print(f"\n💡 {green}Answer:{reset} {answer}")
            print(f"{cyan}(Generated in {duration}s){reset}")

        except Exception as e:
            print(f"\n❌ {yellow}Engine Error: {str(e)}{reset}")


if __name__ == "__main__":
    run_cli()
