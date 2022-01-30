import os 

from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv, find_dotenv
login_manager = LoginManager()
login_manager.login_view = "auth.load_wallet"

load_dotenv(find_dotenv())

def create_app():
    app = Flask(__name__)
    # app.config.from_object(config)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    login_manager.init_app(app)

    from .auth.routes import auth
    # from .view.routes import view
    # from .network.routes import network

    app.register_blueprint(auth)
    # app.register_blueprint(view)
    # app.register_blueprint(network)

    return app