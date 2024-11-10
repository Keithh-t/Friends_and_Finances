from flask import Blueprint, request, jsonify
from app import db
from models import Group, GroupMember, User
from flask_jwt_extended import jwt_required, get_jwt_identity

groups_bp = Blueprint('groups_bp', __name__)

@groups_bp.route('/create', methods=['POST'])
@jwt_required()
def create_group():
    data = request.get_json()
    group_name = data.get('name')
    current_user_id = get_jwt_identity()

    group = Group(name=group_name, created_by=current_user_id)
    db.session.add(group)
    db.session.commit()

    # Add creator as a group member
    group_member = GroupMember(group_id=group.id, user_id=current_user_id)
    db.session.add(group_member)
    db.session.commit()

    return jsonify({'message': 'Group created successfully', 'group_id': group.id}), 201

@groups_bp.route('/<int:group_id>/add_member', methods=['POST'])
@jwt_required()
def add_member(group_id):
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        # Handle invitation logic here (out of scope for now)
        return jsonify({'message': 'User not found'}), 404

    group_member = GroupMember(group_id=group_id, user_id=user.id)
    db.session.add(group_member)
    db.session.commit()

    return jsonify({'message': 'Member added successfully'}), 200
