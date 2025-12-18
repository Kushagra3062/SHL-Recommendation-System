# SHL Intelligent Assessment Recommendation System

## Overview
Hiring managers often struggle to map complex Job Descriptions (JDs) to the correct pre-employment assessments. This project is an **AI-powered Recommendation Engine** that takes a natural language query or JD and returns the most relevant **SHL Individual Test Solutions**.

Unlike simple keyword searches, this system uses a **Retrieval-Augmented Generation (RAG)** pipeline with **Query Decomposition**. It intelligently splits complex requirements (e.g., *"Java Developer with Leadership skills"*) into distinct search components to ensure the recommendations cover both **Hard Skills** (Technical) and **Soft Skills** (Behavioral).

## Key Features
* **Custom Data Pipeline:** Automated scraper (`scraper.py`) that indexes 377+ assessments from the SHL catalog, filtering out pre-packaged solutions.
* **Intelligent Search:** Uses **Google Gemini 2.5 Flash** to decompose user queries, ensuring a balanced mix of assessments.
* **Vector Search:** Powered by **Pinecone** and **HuggingFace Embeddings** (`all-MiniLM-L6-v2`) for high-accuracy semantic retrieval.
* **API First:** Fully functional REST API built with **FastAPI**.
* **Interactive UI:** User-friendly dashboard built with **Streamlit**.

## Tech Stack
* **LLM:** Google Gemini 2.5 Flash
* **Vector DB:** Pinecone
* **Orchestration:** LangChain
* **Backend:** FastAPI
* **Frontend:** Streamlit
* **Scraping:** Selenium & BeautifulSoup

## Project Structure
* `recommender.py`: Core RAG engine with query decomposition logic.
* `scraper.py`: Data ingestion pipeline for the SHL catalog.
* `api.py`: FastAPI backend exposing the `/recommend` endpoint.
* `frontend.py`: Streamlit web interface.
* `evaluate.py`: Script to generate predictions on the test set.

##  Getting Started
1.  **Clone the repo:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/SHL-Recommendation-System.git](https://github.com/YOUR_USERNAME/SHL-Recommendation-System.git)
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the API:**
    ```bash
    uvicorn api:app --reload
    ```
4.  **Run the Frontend:**
    ```bash
    streamlit run frontend.py
    ```