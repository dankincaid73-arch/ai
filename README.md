# Tarantula: AI Infant to AI Terminator

## 🚀 Quick Start Guide
Tarantula is built to run entirely inside Docker, keeping your local machine clean while managing the database, vector storage, and AI inference engine. 

### ⚙️ Prerequisites
Before running Tarantula, ensure your local environment has the following:
* **Docker** (and Docker Compose) running on your machine.
* **Git** installed for version control.

---

**1. Clone the Repository**
Pull the code to your local machine and navigate into the project directory.
~~~bash
git clone https://github.com/dankincaid73AI/ai.git
cd ai
~~~

**2. Configure the Environment**
Tarantula requires environment variables for configuration. Create your local `.env` file by renaming the provided example template.
~~~bash
cp .env.example .env
~~~
*(Alternatively, you can manually rename `.env.example` to `.env` in your file explorer).*

**3. Launch the Containers**
Use Docker Compose to build the application and start the backend services (MongoDB, ChromaDB, and Ollama). 
~~~bash
docker compose up -d --build
~~~

**4. Start the Application Interface**
Because the main application container runs in the background, you interact with the AI by executing the command-line interface script directly inside the running container:
~~~bash
docker exec -it tarantula_app python main.py
~~~
*(Note: On first run, the system will automatically pull the necessary LLM models and ingest sample data if your database is empty.)*

### 🖥️ What to Expect on First Run

When you execute the `main.py` script, the application handles its own initialization sequence before handing over control:

1. **Auto-Ingestion & Verification:** The system first checks the ChromaDB vector store. If the database is empty, Tarantula will automatically process and ingest a set of sample documents (a PDF, a text file, and a web scrape) to populate the RAG pipeline. On subsequent runs, it will simply verify the existing chunks and bypass ingestion.
2. **Persona Selection:** You will be prompted to select an interaction style for the AI (e.g., Default Research Assistant, Angry Old Man, etc.), demonstrating dynamic system prompting.
3. **The Query Engine:** Once initialized, you will enter the main loop where you can query the locally hosted vector data. Type `quit` or `exit` at any time to shut down the engine.

### 🔍 Querying the Engine (RAG in Action)

Once initialization is complete, Tarantula's vector database (ChromaDB) is pre-loaded with three distinct types of unstructured data to demonstrate the ingestion pipeline's versatility:

1. **Text Extraction:** A classic Paul Graham essay (`paul_graham_essay.txt`).
2. **Web Scraping (Playwright):** Dynamic web content pulled directly from `quotes.toscrape.com`.
3. **Complex PDF Parsing:** The seminal AI paper, *Attention Is All You Need* (`1706.03762v7.pdf`). 
    * *Architecture Note:* The `pdf_ingestion` script features a custom upgrade that extracts and injects **contextual metadata** alongside the raw text before the chunking phase. This ensures the vector embeddings maintain structural awareness (such as document origin and surrounding context), significantly improving retrieval accuracy over naive text chunking.

#### 🧪 Sample Prompts to Try
To see how the RAG architecture retrieves the ingested context to ground the LLM's answers, try pasting these test prompts into the CLI:

* **To test the PDF metadata pipeline:** 
  > *"What is the exact difference in computational complexity per layer between self-attention layers and recurrent layers?"*

* **To test the raw text ingestion:** 
  > *"Tell me about the Y Combinator"*

* **To test the web scraper:** 
  > *"Find me a quote from Albert Einstein that was scraped from the database."*

Watch the terminal output when you run these. You will see the engine successfully bypass its own training data hallucinations and ground its answers entirely in the local vector data you just ingested.

### 🕷️ Closing Thoughts
Building Tarantula has been an incredible deep dive into local AI architecture, spatial data constraints, and the nuances of custom data ingestion. The system as it stands is a robust proof-of-concept, but it is built on an architecture designed to scale into event-driven, multi-agent workflows. 

Thank you for taking the time to review the architecture and run the system. Enjoy your new Tarantula, and happy querying!

---

## The Story of Tarantula: Introduction
The software engineering market demands a complete reinvention of how we approach computing. After a major layoff from enterprise logistics giant Swift/Knight Transportation, I decided to channel my engineering background into solving the most critical bottleneck in modern tech: running high-performance AI locally, efficiently, and without massive cloud budgets.

This repository documents the chronological evolution of a locally deployed AI system. It is a completely transparent, public "proof of work" chronicle. You will see the messy, raw architectures of the early "Infant" phases evolve step-by-step into a highly optimized, high-throughput "Terminator" system. 

## The Core Stack & Frameworks
To build a fully local, responsive system, I am aggressively deploying a modern data and AI pipeline:
* **Core Language:** Python *(a powerful new addition to my engineering toolkit)*
* **Local Inference:** Ollama *(for managing and serving local LLMs)*
* **Database Layer:** MongoDB *(for structural operational data and user state)*
* **Vector Architecture:** ChromaDB *(for embedding storage and low-latency semantic indexing)*

## Technical Competencies Demonstrated
* **Vector & Semantic Search:** Designing high-accuracy similarity matching pipelines for Retrieval-Augmented Generation (RAG).
* **Spatial Placement Theory:** Applying advanced spatial data logic to map and optimize high-dimensional vector embeddings within local hardware constraints.

## Project Phases
* **Phase 1: The Infant** – Establishing baseline local inference, initial memory bottlenecks, and raw token generation.
* **Phase 2: Learning to Walk** – Optimizing VRAM usage, quantizing models, and fine-tuning context windows.
* **Phase 3: The Terminator** – Implemented agentic workflows, custom local memory retrieval, and maximum hardware efficiency.

## Future Roadmap: Tarantula V2.0 (The Apex Predator)
With the local engine functional, the next architectural iteration focuses on moving from a single-threaded local script to an optimized, event-driven pipeline:
* **Asynchronous Ingestion:** Transitioning the ingestion pipeline to `asyncio` to handle concurrent data streams into ChromaDB without blocking local model inference.
* **Vector Index Optimization:** Implementing advanced quantization and custom distance metrics to optimize high-dimensional vector lookups on tight VRAM budgets.
* **Agentic Multi-Tool Routing:** Allowing the core model to dynamically decide when to query MongoDB for structural state versus when to query ChromaDB for semantic context.