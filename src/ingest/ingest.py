# src/ingest/ingest.py

from pathlib import Path
from src.parsers import parse_recipes, parse_meat_prices, parse_vegetables_prices
from src.database.json_db import JSONDatabase

def make_ingest():
    
    base_path = Path(__file__).parent.parent.parent

    print("="*60)
    print("Ingesting recipes...")
    print("="*60)

    # Parse all files
    print("\n[1/3] Parsing recipes...")
    recipes = parse_recipes(base_path / 'inputs' / 'Recetas.md')
    print(f"✓ {len(recipes)} recipes parsed")
    
    print("\n[2/3] Parsing prices of meats and fish...")
    meat_prices = parse_meat_prices(base_path / 'inputs' / 'Carnes y Pescados.xlsx')
    print(f"✓ {len(meat_prices)} prices of meats/fish parsed")
    
    print("\n[3/3] Parsing prices of vegetables...")
    vegetable_prices = parse_vegetables_prices(base_path / 'inputs' / 'verduleria.pdf')
    print(f"✓ {len(vegetable_prices)} prices of vegetables parsed")
    parsed_data = {
        "recetas": recipes,
        "precios": {
            "carnes": meat_prices,
            "verduras": vegetable_prices
        }
    }

    db = JSONDatabase()
    db.save(parsed_data)

    print("\n" + "="*60)
    print(f"✓ Data saved in {db.db_path}")
    print("✓ Ingestion completed successfully!")
    print("="*60)

if __name__ == '__main__':
    make_ingest()
