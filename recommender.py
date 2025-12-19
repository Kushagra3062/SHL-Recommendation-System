import os
import json
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings 
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pinecone import Pinecone
from functools import lru_cache

load_dotenv()

@lru_cache(maxsize=1)
def get_cached_embeddings():
    print("Loading Hugging Face API Embeddings (Lightweight)...")
    
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not api_key:
        raise ValueError("HUGGINGFACEHUB_API_TOKEN is missing from environment variables!")

    return FastEmbedEmbeddings(
        api_key=api_key,
        model_name="BAAI/bge-small-en-v1.5"
    )

class SHLRecommender:
    def __init__(self):
        self.index_name = "shl-index"
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        self.embeddings = get_cached_embeddings()
        
        self.vectorstore = PineconeVectorStore(
            index_name=self.index_name,
            embedding=self.embeddings,
            pinecone_api_key=self.pinecone_api_key
        )
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.0,
            max_tokens=200,
            google_api_key=self.google_api_key
        )

    def decompose_query(self, query):
        """
        Robustly splits query using a pipe delimiter.
        """
        template = """
        You are an expert HR assistant. Analyze the user's hiring requirement.
        
        Task:
        1. Identify if the query requires different types of assessments (e.g., Technical Skills AND Personality/Behavior).
        2. If yes, split it into distinct, specific search phrases.
        3. If no, keep the original query.
        
        Output Format:
        Return ONLY the search phrases separated by a pipe character (|). Do not add bullet points or explanations.
        
        Example Input: "Need a Java developer who leads well"
        Example Output: Java Developer skills|Leadership personality test
        
        User Query: "{query}"
        
        Output:
        """
        try:
            prompt = PromptTemplate.from_template(template)
            chain = prompt | self.llm
            response = chain.invoke({"query": query})
            
            content = response.content.strip()
            sub_queries = [s.strip() for s in content.split("|") if s.strip()]
            
            return sub_queries if sub_queries else [query]
            
        except Exception as e:
            print(f"Query Decomposition Failed: {e}. Using original query.")
            return [query]

    def get_recommendations(self, query, k=10):
        sub_queries = self.decompose_query(query)
        print(f"Processed Queries: {sub_queries}")
        
        all_results = {}
        
        limit_per_query = max(5, k // len(sub_queries) + 1)
        
        for q in sub_queries:
            try:
                docs = self.vectorstore.similarity_search_with_score(q, k=limit_per_query)
                
                for doc, score in docs:
                    url = doc.metadata.get('url')
                
                    if url and url not in all_results:
                        all_results[url] = {
                            "Assessment Name": doc.metadata.get('name', 'Unknown'),
                            "URL": url,
                            "Type": doc.metadata.get('test_type_full', 'General'),
                            "Score": score,
                            "Matched Query": q 
                        }
            except Exception as e:
                print(f"Search error for query '{q}': {e}")
  
        sorted_results = sorted(all_results.values(), key=lambda x: x['Score'], reverse=True)
        return sorted_results[:k]

if __name__ == "__main__":
    rec = SHLRecommender()
    res = rec.get_recommendations("Need a Java developer who is good in collaborating")
    import pandas as pd
    print(pd.DataFrame(res))