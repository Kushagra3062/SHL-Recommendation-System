from sentence_transformers import SentenceTransformer
import os

model_path = "./model_cache"


print("Downloading model for build...")
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=model_path)
print("Model downloaded successfully!")