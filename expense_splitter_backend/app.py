from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    # Register Blueprints here
    from resources.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from resources.groups import groups_bp
    app.register_blueprint(groups_bp, url_prefix='/api/groups')

    from resources.expenses import expenses_bp
    app.register_blueprint(expenses_bp, url_prefix='/api/expenses')

    from resources.balances import balances_bp
    app.register_blueprint(balances_bp, url_prefix='/api/balances')

    from resources.payments import payments_bp
    app.register_blueprint(payments_bp, url_prefix='/api/payments')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
