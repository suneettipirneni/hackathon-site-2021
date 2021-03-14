# -*- coding: utf-8 -*-
"""
    src
    ~~~
    Initialize the Flask App and its extensions + blueprints

    Functions:

        create_app() -> Flask

    Variables:

        schema
        swagger_template
        db
        app

"""
from os import path, getenv, environ
from flask import Flask
from werkzeug.exceptions import HTTPException
from flasgger import Swagger
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from src.tasks import make_celery
import yaml


# Init Extensions
db = MongoEngine()
mail = Mail()
bcrypt = Bcrypt()

# Load the Schema Definitions
schemapath = path.join(path.abspath(path.dirname(__file__)), "schemas.yml")
schemastream = open(schemapath, "r")
schema = yaml.load(schemastream, Loader=yaml.FullLoader)
schemastream.close()

swagger_template = {
    "openapi": "3.0.3",
    "swagger": "3.0.3",
    "info": {
        "title": "Knight Hacks Backend API",
        "description": "Backend API for Knight Hacks",
        "contact": {
            "responsibleOrganization": "Knight Hacks",
            "responsibleDeveloper": "Knight Hacks Dev Team",
            "email": "webmaster@knighthacks.org",
            "url": "https://knighthacks.org"
        },
        "version": "0.0.1"
    },
    "basePath": "/api",
    "schemes": [
        "http",
        "https"
    ],
    "components": {
        "schemas": schema,
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization"
            },
            "CookieAuth": {
                "type": "apiKey",
                "in": "cookie",
                "name": "sid"
            }
        }
    }
}
swagger = Swagger(template=swagger_template)


def create_app():
    """Initialize the App"""
    app = Flask(__name__, static_url_path="/static")

    # Flask Config
    app_settings = getenv("APP_SETTINGS", "src.config.ProductionConfig")
    app.config.from_object(app_settings)

    """Set FLASK_ENV and FLASK_DEBUG cause that doesn't happen auto anymore"""
    if app.config.get("DEBUG"):
        environ["FLASK_ENV"] = "development"
        environ["FLASK_DEBUG"] = "1"

    """Setup Extensions"""
    CORS(app)
    db.init_app(app)
    swagger.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    from src.common.json import JSONEncoderBase
    app.json_encoder = JSONEncoderBase

    """Register Blueprints"""
    from src.api.hackers import hackers_blueprint
    from src.api.stats import stats_blueprint
    from src.api.sponsor import sponsors_blueprint
    from src.api.events import events_blueprint
    from src.api.groups import groups_blueprint
    from src.api.club_events import club_events_blueprint
    from src.api.categories import categories_blueprint
    from src.api.email_verification import email_verify_blueprint
    from src.api.auth import auth_blueprint

    app.register_blueprint(hackers_blueprint, url_prefix="/api")
    app.register_blueprint(stats_blueprint, url_prefix="/api")
    app.register_blueprint(sponsors_blueprint, url_prefix="/api")
    app.register_blueprint(events_blueprint, url_prefix="/api")
    app.register_blueprint(groups_blueprint, url_prefix="/api")
    app.register_blueprint(club_events_blueprint, url_prefix="/api")
    app.register_blueprint(categories_blueprint, url_prefix="/api")
    app.register_blueprint(email_verify_blueprint, url_prefix="/api")
    app.register_blueprint(auth_blueprint, url_prefix="/api")

    """Register Error Handlers"""
    from src.common import error_handlers

    app.register_error_handler(HTTPException, error_handlers.handle_exception)

    """Initialize Celery"""
    celery = make_celery(app)

    return app, celery


app, celery = create_app()
