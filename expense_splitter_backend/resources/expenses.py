from flask import Blueprint, request, jsonify
from app import db
from models import Expense, ExpenseSplit, GroupMember
from flask_jwt_extended import jwt_required, get_jwt_identity

expenses_bp = Blueprint('expenses_bp', __name__)

@expenses_bp.route('/add', methods=['POST'])
@jwt_required()
def add_expense():
    data = request.get_json()
    group_id = data.get('group_id')
    description = data.get('description')
    amount = data.get('amount')
    paid_by = data.get('paid_by')
    split_among = data.get('split_among')  # List of user_ids

    expense = Expense(
        group_id=group_id,
        description=description,
        amount=amount,
        paid_by=paid_by
    )
    db.session.add(expense)
    db.session.commit()

    # Calculate split amounts (equal split for simplicity)
    split_amount = amount / len(split_among)
    for user_id in split_among:
        expense_split = ExpenseSplit(
            expense_id=expense.id,
            user_id=user_id,
            amount=split_amount
        )
        db.session.add(expense_split)
    db.session.commit()

    return jsonify({'message': 'Expense added successfully'}), 201

@expenses_bp.route('/<int:group_id>', methods=['GET'])
@jwt_required()
def get_expenses(group_id):
    expenses = Expense.query.filter_by(group_id=group_id).all()
    # Serialize expenses (use Marshmallow or custom serialization)
    return jsonify({'expenses': [expense.serialize() for expense in expenses]}), 200
