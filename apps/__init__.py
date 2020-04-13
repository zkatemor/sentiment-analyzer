def create_app():
    import os

    from flask import Flask
    from apps.admin_panel import admin
    from db import session

    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    admin.init_app(app)
    session.init_app(app)

    from models.dictionary import Dictionary, Word
    return app
