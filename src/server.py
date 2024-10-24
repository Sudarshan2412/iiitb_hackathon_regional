import json
from flask import Flask, send_from_directory, render_template
from flask_cors import CORS
from .config import Config
from .product import product_bp
from .ai import chat_bp
from .db import db_instance


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app)

    @app.get("/")
    def index():
        products = db_instance.fetchProducts()
        return render_template("index.jinja", products=products)

    @app.get("/p/<id>")
    def product(id):
        prod = db_instance.getFullProduct(id)
        return render_template("product.jinja", product=prod, json=json.dumps(prod))

    @app.route("/static/<path:path>")
    def send_js(path):
        return send_from_directory("static", path)

    # Register the blueprint
    # app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(product_bp, url_prefix="/product")
    app.register_blueprint(chat_bp, url_prefix="/chat")

    # Set JSON as the default format
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
    app.config["DB_INSTANCE"] = db_instance

    return app


def main():
    print("MAIN")

    app = create_app()
    # Load configuration from Config class
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
