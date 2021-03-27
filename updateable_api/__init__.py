from flask import Flask
from config import Config
import logging
import datetime as dt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from updateable_api.views import update_bp
    app.register_blueprint(update_bp)


    # @app.after_request
    # def after_request(response):
    #     """ Logging after every request. """
    #     logger = logging.getLogger("app.access")
    #     logger.info(
    #         "%s [%s] %s %s %s %s %s %s %s",
    #         request.remote_addr,
    #         dt.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
    #         request.method,
    #         request.path,
    #         request.scheme,
    #         response.status,
    #         response.content_length,
    #         request.referrer,
    #         request.user_agent,
    #     )
    #     return response

    return app



def register_extensions(app):
    logs.init_app(app)
    return None

def register_blueprints(app):
    app.register_blueprint(public.views.bp)
    return None