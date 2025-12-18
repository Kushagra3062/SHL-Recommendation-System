import os
import time
import pandas as pd
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")  
INDEX_NAME = "shl-index"

def index_data():
  
    if not os.path.exists("shl_assessments_preprocessed.csv"):
        print("Error: Preprocessed CSV not found. Run preprocess_data.py first.")
        return

    df = pd.read_csv("shl_assessments_preprocessed.csv")
    print(f"Loaded {len(df)} assessments.")

    
    print("Loading Embedding Model (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

   
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    existing_indexes = [i.name for i in pc.list_indexes()]
    if INDEX_NAME not in existing_indexes:
        print(f"Creating index '{INDEX_NAME}'...")
        try:
            pc.create_index(
                name=INDEX_NAME,
                dimension=384,
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
            time.sleep(10) 
        except Exception as e:
            print(f"Index creation failed: {e}")
            return
    else:
        print(f"Index '{INDEX_NAME}' found.")

    
    print("Preparing data for indexing...")
   
    texts = df['combined_text'].tolist()
    
    
    metadatas = df[['name', 'url', 'test_type_full']].to_dict('records')

   
    print("Uploading to Pinecone (this may take a minute)...")
    try:
        PineconeVectorStore.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas,
            index_name=INDEX_NAME,
            pinecone_api_key=PINECONE_API_KEY
        )
        print("SUCCESS: Data indexed successfully!")
    except Exception as e:
        print(f"Error during upload: {e}")

if __name__ == "__main__":
    index_data()