# src/api/app.py

from flask import Flask
from src.api.routes import configure_routes

def create_app():
    app = Flask(__name__)
    configure_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)