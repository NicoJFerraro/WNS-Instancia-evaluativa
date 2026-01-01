# src/api/app.py

from flask import Flask, send_from_directory
from pathlib import Path
from src.api.routes import configure_routes

def create_app():
    app = Flask(__name__)
    
    # CORS headers to allow requests from frontend
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Configure API routes first (they have priority)
    configure_routes(app)
    
    # Serve static files from frontend (after API routes)
    frontend_path = Path(__file__).parent.parent.parent / 'frontend'
    
    @app.route('/')
    def index():
        return send_from_directory(frontend_path, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        # Don't intercept API routes (already handled by configure_routes)
        if path.startswith('api/'):
            from flask import abort
            abort(404)
        # Serve static files (CSS, JS) from frontend
        if path in ['style.css', 'app.js']:
            return send_from_directory(frontend_path, path)
        # For any other route, serve index.html (SPA routing)
        return send_from_directory(frontend_path, 'index.html')
    
    return app

if __name__ == "__main__":
    app = create_app()
    # Using port 5001 because port 5000 is used by macOS AirPlay Receiver
    app.run(debug=True, host='0.0.0.0', port=5001)