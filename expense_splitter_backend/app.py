from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
expenses = []
app = Flask(__name__)

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

@app.route("/api/expenses/add", methods=["POST"])
def add_expense():
    data = request.get_json()
    name = data.get("name")
    amount = data.get("amount")
    expenses.append({"name": name, "amount": amount})
    return jsonify({"message": "Expense added successfully"}), 201

@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    return jsonify(expenses)

@app.route("/api/expenses/split", methods=["GET"])
def calculate_split():
    if not expenses:
        return jsonify([])  # Return empty list if no expenses

    total = sum(expense["amount"] for expense in expenses)
    split_amount = total / len(expenses)

    balance_summary = []
    for expense in expenses:
        balance = expense["amount"] - split_amount
        balance_summary.append({"name": expense["name"], "balance": balance})

    return jsonify(balance_summary)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
