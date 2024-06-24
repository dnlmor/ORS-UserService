from .models import User
from .database import db_session
from .utils import hash_password, verify_password, generate_token
from sqlalchemy.exc import IntegrityError
from flask import current_app
import jwt
from datetime import datetime, timedelta

class UserService:
    @staticmethod
    def register_user(username, email, password):
        try:
            hashed_password = hash_password(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db_session.add(new_user)
            db_session.commit()
            return new_user
        except IntegrityError:
            db_session.rollback()
            raise ValueError("Username or email already exists")

    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and verify_password(password, user.password):
            return user
        return None

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update_user_profile(user_id, username=None, email=None):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        if username:
            user.username = username
        if email:
            user.email = email
        
        try:
            db_session.commit()
            return user
        except IntegrityError:
            db_session.rollback()
            raise ValueError("Username or email already exists")

    @staticmethod
    def change_password(user_id, old_password, new_password):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        if not verify_password(old_password, user.password):
            raise ValueError("Incorrect old password")
        
        user.password = hash_password(new_password)
        db_session.commit()
        return True

    @staticmethod
    def generate_auth_token(user):
        expiration = datetime.utcnow() + timedelta(days=1)
        payload = {
            'user_id': user.id,
            'exp': expiration
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

    @staticmethod
    def verify_auth_token(token):
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
            return User.query.get(user_id)
        except jwt.ExpiredSignatureError:
            return None  # Token has expired
        except jwt.InvalidTokenError:
            return None  # Invalid token

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        db_session.delete(user)
        db_session.commit()
        return True

    @staticmethod
    def list_users(page=1, per_page=10):
        return User.query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def search_users(query):
        return User.query.filter(
            (User.username.ilike(f'%{query}%')) | (User.email.ilike(f'%{query}%'))
        ).all()

