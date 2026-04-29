"""
Validation script for product YAML files.
"""
import sys
from pathlib import Path
import yaml
from pydantic import ValidationError

from recommender.models import Product

def validate_all_products(directory: Path) -> bool:
    """Validate all YAML products in a directory."""
    success = True
    count = 0
    
    if not directory.exists() or not directory.is_dir():
        print(f"Directory not found: {directory}")
        return False
        
    for file_path in directory.glob("*.yaml"):
        if file_path.name.startswith("_"):
            continue
            
        count += 1
        print(f"Validating {file_path.name}...")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data:
                    Product.model_validate(data)
                    print(f"  [OK] {file_path.name} is valid.")
        except ValidationError as e:
            print(f"  [ERROR] Validation failed for {file_path.name}:")
            for error in e.errors():
                loc = " -> ".join(str(l) for l in error["loc"])
                print(f"    - {loc}: {error['msg']}")
            success = False
        except Exception as e:
            print(f"  [ERROR] Could not read {file_path.name}: {e}")
            success = False
            
    if count == 0:
        print("No product files found to validate.")
        
    return success

if __name__ == "__main__":
    products_dir = Path(__file__).parent.parent / "products"
    is_valid = validate_all_products(products_dir)
    sys.exit(0 if is_valid else 1)
