from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import os

print("⏳ Downloading FastEmbed model to local cache...")

FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    cache_dir="./fastembed_cache"
)

print("✅ Model downloaded successfully!")