from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from recommender import SHLRecommender
import uvicorn

app = FastAPI(
    title="SHL Recommendation API",
    description="API for retrieving SHL assessment recommendations based on job descriptions."
)

engine = SHLRecommender()

class QueryRequest(BaseModel):
    query: str

class Recommendation(BaseModel):
    assessment_name: str
    url: str

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "service": "SHL Recommendation API"}

@app.post("/recommend")
def recommend(request: QueryRequest):
    """
    Takes a natural language query or JD and returns a list of assessments.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        results = engine.get_recommendations(request.query, k=10)
        
        
        response_data = [
            {
                "Assessment Name": item['Assessment Name'],
                "URL": item['URL']
            }
            for item in results
        ]
        return response_data
        
    except Exception as e:
        
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error processing recommendation")

@app.get("/health")
def health_check():
    return {"status": "ok"}