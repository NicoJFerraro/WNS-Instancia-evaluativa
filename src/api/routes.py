# src/api/routes.py

from flask import jsonify, request
from src.database.json_db import JSONDatabase
from src.services.calculator import calculate_total_recipe_cost
from src.services.exchange_rate import get_exchange_rate_usd_to_ars, validate_date_within_last_30_days

db = JSONDatabase()

def configure_routes(app):
    @app.route('/api/recipes', methods=['GET'])
    def get_recipes():
        recipes = db.get_recipes()
        return jsonify({
            "recipes": recipes,
            "total": len(recipes)
        })
    
    @app.route('/api/recipes/<name>', methods=['GET'])
    def get_recipe_by_name(name):
        recipe = db.recipe_by_name(name)
        if not recipe:
            return jsonify({"error": "Recipe not found"}), 404
        return jsonify(recipe)
    
    @app.route('/api/calculate', methods=['POST'])
    def calculate_cost():
        data=request.json

        if not data or "recipe_name" not in data or "date" not in data:
            return jsonify({"error": "Missing recipe_name or date in request body"}), 400
        
        recipe = db.recipe_by_name(data["recipe_name"])
        if not recipe:
            return jsonify({"error": "Recipe not found"}), 404
        
        try:
            date = validate_date_within_last_30_days(data["date"])
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        try:
            exchange_rate = get_exchange_rate_usd_to_ars(date)
        except Exception as e:
            return jsonify({"error": f"Failed to get exchange rate: {str(e)}"}), 500
        
        db_data = db.load()
        prices = db_data.get("precios", {})

        result = calculate_total_recipe_cost(
            recipe,
            prices,
            exchange_rate
        )

        return jsonify({
            "recipe_name": data["recipe_name"],
            "calculation_date": date.isoformat(),
            "exchange_rate_usd_to_ars": exchange_rate,
            "cost_details": result
        })
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "ok"}), 200