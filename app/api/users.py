from flask import jsonify, request
from app import db
from app.models import User
from app.api import bp

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Must include username, email and password'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Please use a different username'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Please use a different email address'}), 400
    user = User()
    user.username = data['username']
    user.email = data['email']
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)
