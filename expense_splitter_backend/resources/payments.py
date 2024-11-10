from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

payments_bp = Blueprint('payments_bp', __name__)

@payments_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_payment_link():
    data = request.get_json()
    amount = data.get('amount')
    to_user_email = data.get('to_user_email')

    # Generate a payment link (e.g., PayPal.me link)
    payment_link = f'https://www.paypal.me/{to_user_email}/{amount}'

    return jsonify({'payment_link': payment_link}), 200
