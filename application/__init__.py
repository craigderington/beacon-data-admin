from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from config import config
from flask_admin.contrib.sqla import ModelView
from forms import SearchForm
from celery import Celery
from flask_login import LoginManager
from flask.cli import FlaskGroup


db = SQLAlchemy()
celery = Celery(__name__, broker=config["development"])
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config["development"])

    db.init_app(app)
    celery.conf.update(app.config)
    login_manager.init_app(app)
   

    with app.app_context():
        from . import routes
        from .home import routes as homeroutes
        from .customer import routes as customerroutes
        from .search import routes as searchroutes
        from . import auth
        

        app.register_blueprint(customerroutes.customer_bp)
        app.register_blueprint(homeroutes.home_bp)
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(searchroutes.search_bp)

        @app.shell_context_processor
        def shell_context():
            return {'app': app, 'db': db}

        return app

cli = FlaskGroup(create_app=create_app)

@cli.command
def custom_command():
    pass

if __name__ == '__main__':
    cli()