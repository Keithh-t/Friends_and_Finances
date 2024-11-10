from flask import Blueprint, jsonify
from app import db
from models import ExpenseSplit, Expense
from flask_jwt_extended import jwt_required, get_jwt_identity

balances_bp = Blueprint('balances_bp', __name__)

@balances_bp.route('/<int:group_id>', methods=['GET'])
@jwt_required()
def get_balances(group_id):
    # Get all expenses for the group
    expenses = Expense.query.filter_by(group_id=group_id).all()

    # Get all group members
    group_members = GroupMember.query.filter_by(group_id=group_id).all()
    user_ids = [member.user_id for member in group_members]

    # Map user IDs to user details
    users = User.query.filter(User.id.in_(user_ids)).all()
    user_map = {user.id: user for user in users}

    # Initialize balances dictionary
    balances = {user_id: 0.0 for user_id in user_ids}

    # Iterate over each expense
    for expense in expenses:
        payer_id = expense.paid_by
        amount = expense.amount

        # Get splits for the expense
        splits = ExpenseSplit.query.filter_by(expense_id=expense.id).all()

        # Update the payer's balance
        balances[payer_id] += amount

        # Update balances based on splits
        for split in splits:
            user_id = split.user_id
            split_amount = split.amount

            # Each user owes split_amount
            balances[user_id] -= split_amount

    # Separate creditors and debtors
    creditors = []
    debtors = []

    for user_id, balance in balances.items():
        if balance > 0.01:
            creditors.append({'user_id': user_id, 'balance': balance})
        elif balance < -0.01:
            debtors.append({'user_id': user_id, 'balance': balance})

    # Sort creditors and debtors
    creditors.sort(key=lambda x: x['balance'], reverse=True)
    debtors.sort(key=lambda x: x['balance'])

    transactions = []

    i = 0  # Index for debtors
    j = 0  # Index for creditors

    while i < len(debtors) and j < len(creditors):
        debtor = debtors[i]
        creditor = creditors[j]

        debt_amount = -debtor['balance']
        credit_amount = creditor['balance']

        settlement_amount = min(debt_amount, credit_amount)

        transactions.append({
            'from_user_id': debtor['user_id'],
            'to_user_id': creditor['user_id'],
            'amount': round(settlement_amount, 2)
        })

        # Update balances
        debtor['balance'] += settlement_amount
        creditor['balance'] -= settlement_amount

        # Move to next debtor or creditor if balance is settled
        if abs(debtor['balance']) < 0.01:
            i += 1
        if creditor['balance'] < 0.01:
            j += 1

    # Enhance transactions with user info
    result = []
    for tx in transactions:
        from_user = user_map[tx['from_user_id']]
        to_user = user_map[tx['to_user_id']]

        result.append({
            'from_user_id': tx['from_user_id'],
            'from_user_name': from_user.name,
            'to_user_id': tx['to_user_id'],
            'to_user_name': to_user.name,
            'amount': tx['amount']
        })

    return jsonify({'transactions': result}), 200
