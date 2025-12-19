from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import os

print("⏳ Downloading FastEmbed model to local cache...")

cache_path = "/app/model_cache"

FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    cache_dir=cache_path
)

print("✅ Model downloaded successfully!")