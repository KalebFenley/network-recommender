"""
FastAPI application for the Network Hardware Recommendation Engine.
"""
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from recommender.models import Questionnaire, Product
from recommender.database import load_products
from recommender.scoring import score_products, ScoredProduct

app = FastAPI(title="Network Hardware Recommendation Engine")

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load products once at startup
PRODUCTS_DIR = Path(os.environ.get("PRODUCTS_DIR", Path(__file__).parent.parent / "products"))
_loaded_products: List[Product] = []

@app.on_event("startup")
def startup_event():
    global _loaded_products
    try:
        _loaded_products = load_products(PRODUCTS_DIR)
        print(f"Loaded {len(_loaded_products)} products.")
    except Exception as e:
        print(f"Failed to load products: {e}")

@app.post("/api/recommend", response_model=List[ScoredProduct])
def recommend(questionnaire: Questionnaire):
    """
    Receive questionnaire answers and return ranked product recommendations.
    """
    if not _loaded_products:
        raise HTTPException(status_code=500, detail="Product database is empty or failed to load.")
        
    return score_products(questionnaire, _loaded_products)

@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "products_loaded": len(_loaded_products)}
