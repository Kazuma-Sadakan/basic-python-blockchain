# from flask import Flask
# from flask_login import LoginManager
# from config.config import config 
# login_manager = LoginManager()
# login_manager.login_view = "auth.signin"

# def create_app(config):
#     app = Flask(__name__)
#     app.config.from_object(config)
#     login_manager.init_app(app)

#     from .auth.routes import auth
#     from .view.routes import view
#     from .network.routes import network

#     app.register_blueprint(auth)
#     app.register_blueprint(view)
#     app.register_blueprint(network)

#     return app