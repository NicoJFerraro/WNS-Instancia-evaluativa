# src/database/json_db.py

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

class JSONDatabase:
    def __init__(self, db_path:str = "database/data.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    #Load data from JSON file
    def load(self) -> Dict[str, Any]:

        default_structure = {
            "recetas":[],
            "precios":{
                "carnes":{},
                "verduras":{}
            },
            "metadata":{}
        }

        if not self.db_path.exists():
            return default_structure
        
        try:
            with open(self.db_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Warning: JSON file is corrupted. Error: {e}")
            return default_structure
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return default_structure
    
    #Save data to JSON file
    def save(self, data: Dict[str, Any]) -> None:
        from datetime import datetime

        data["metadata"] = {
            "last_updated": datetime.now().isoformat(),
            "version": "1.0.0"
        }
        with open(self.db_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    
    #Get all recipes
    def get_recipes(self) -> List[Dict]:
        data = self.load()
        return data.get("recetas", [])
    
    #Get recipe by name
    def recipe_by_name(self, name:str) -> Optional[Dict]:
        recipes = self.get_recipes()
        for recipe in recipes:
            if recipe.get("nombre","").lower() == name.lower():
                return recipe
        return None
    
    def get_price(self, product: str, type: Optional[str] = None) -> Optional[float]:
        data = self.load()
        prices = data.get("precios",{})
        if type:
            type_prices = prices.get(type, {})
            return type_prices.get(product)
        else:
            for type_prices in prices.values():
                if product in type_prices:
                    return type_prices[product]
        return None
    
