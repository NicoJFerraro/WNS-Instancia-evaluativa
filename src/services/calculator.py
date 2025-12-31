# src/services/calculator.py

import math
from typing import Dict

def ceil_to_multiple_of_250(grams: float) -> int:
    # Round up to the nearest multiple of 250 grams

    if grams <= 0:
        return 0
    
    multiples = math.ceil(grams / 250)
    return int(multiples * 250)

def calculate_total_recipe_cost(
        recipe:Dict,
        prices: Dict[str, Dict[str, float]],
        exchange_rate_usd_to_ars: float
        ) -> Dict:
    
    if not isinstance(recipe, dict):
        raise ValueError("Recipe must be a dictionary")
    
    if "ingredientes" not in recipe:
        raise ValueError("Recipe must contain 'ingredientes' key")
    
    if not isinstance(prices, dict):
        raise ValueError("Prices must be a dictionary")
    
    if "carnes" not in prices or "verduras" not in prices:
        raise ValueError("Prices must contain 'carnes' and 'verduras' keys")
    
    if exchange_rate_usd_to_ars <= 0:
        raise ValueError("Exchange rate must be greater than 0")

    price_details = []
    total_cost_ars = 0.0

    for ingredient in recipe.get("ingredientes", []):
        name = ingredient.get('nombre')
        if name:
            name = name.strip()
        quantity_grams = ingredient.get('cantidad', 0)

        if not isinstance(quantity_grams, (int, float)):
            price_details.append({
                "name": name,
                "quantity_grams": quantity_grams,
                "quantity_to_buy_grams": None,
                "price_per_kg_ars": None,
                "cost_ars": None,
                "error": "Invalid quantity: must be a number"
            })
            continue

        if quantity_grams < 0:
            price_details.append({
                "name": name,
                "quantity_grams": quantity_grams,
                "quantity_to_buy_grams": None,
                "price_per_kg_ars": None,
                "cost_ars": None,
                "error": "Quantity cannot be negative"
            })
            continue

        if not name:
            price_details.append({
                "name": None,
                "quantity_grams": quantity_grams,
                "quantity_to_buy_grams": ceil_to_multiple_of_250(quantity_grams),
                "price_per_kg_ars": None,
                "cost_ars": None,
                "error": "Ingredient name is missing"
            })
            continue

        quantity_to_buy = ceil_to_multiple_of_250(quantity_grams)

        price_per_kg_ars = None
        for category, items in prices.items():
            if not isinstance(items, dict):
                continue
            for item_name, item_price in items.items():
                if item_name.strip().lower() == name.lower():
                    price_per_kg_ars = item_price
                    break
            if price_per_kg_ars is not None:
                break
        if price_per_kg_ars is None:
            price_details.append({
                "name": name,
                "quantity_grams": quantity_grams,
                "quantity_to_buy_grams": quantity_to_buy,
                "price_per_kg_ars": None,
                "cost_ars": None,
                "error": "Price not found"
            })
            continue
        
        quantity_kg = quantity_to_buy / 1000.0
        ingredient_cost_ars = quantity_kg * price_per_kg_ars
        total_cost_ars += ingredient_cost_ars

        price_details.append({
            "name": name,
            "quantity_grams": quantity_grams,
            "quantity_to_buy_grams": quantity_to_buy,
            "price_per_kg_ars": price_per_kg_ars,
            "cost_ars": ingredient_cost_ars
            })
        
    return {
        "total_cost_ars": total_cost_ars,
        "total_cost_usd": total_cost_ars / exchange_rate_usd_to_ars,
        "details": price_details}

    
