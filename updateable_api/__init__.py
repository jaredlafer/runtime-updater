from flask import Flask, request
from extensions import logs
from datetime import datetime
import logging
import settings


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    from updateable_api.views import update_bp
    app.register_blueprint(update_bp)
    logs.init_app(app)

    @app.after_request
    def after_request(response):
        #Logging after every request
        logger = logging.getLogger("app")
        logger.info(
            "%s [%s] %s %s %s %s %s %s %s",
            request.remote_addr,
            datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
            request.method,
            request.path,
            request.scheme,
            response.status,
            response.content_length,
            request.referrer,
            request.user_agent,
        )

        return response

    return app


