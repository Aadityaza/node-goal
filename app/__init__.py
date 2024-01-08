from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import routes
    from .views.graph_routes import graph_blueprint

    # Register blueprints
    app.register_blueprint(graph_blueprint, url_prefix='/graph')

    return app
