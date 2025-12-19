from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import os

model_path = "./fastembed_cache"


print("Downloading model for build...")
model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
print("Model downloaded successfully!")