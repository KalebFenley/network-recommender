"""
Database module for loading products from YAML files.
"""
import yaml
from pathlib import Path
from typing import List

from recommender.models import Product

PRODUCTS_DIR = Path(__file__).parent.parent / "products"

def load_products(directory: Path = PRODUCTS_DIR) -> List[Product]:
    """Load all product YAML files from the specified directory."""
    products = []
    
    if not directory.exists() or not directory.is_dir():
        return products
        
    for file_path in directory.glob("*.yaml"):
        # Skip template files
        if file_path.name.startswith("_"):
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)
                if data:
                    product = Product.model_validate(data)
                    products.append(product)
            except Exception as e:
                raise ValueError(f"Failed to load product from {file_path}: {e}")
                
    return products
