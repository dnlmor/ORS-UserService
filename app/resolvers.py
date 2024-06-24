# app/resolvers.py

from .services import UserService

def resolve_create_user(info, username, email, password):
    return UserService.register_user(username, email, password)

def resolve_login_user(info, email, password):
    user = UserService.authenticate_user(email, password)
    if user:
        token = UserService.generate_auth_token(user)
        return {'user': user, 'token': token}
    return None

def resolve_get_user(info, id):
    return UserService.get_user_by_id(id)

def resolve_update_user(info, user_id, username=None, email=None):
    return UserService.update_user_profile(user_id, username, email)

def resolve_change_password(info, user_id, old_password, new_password):
    return UserService.change_password(user_id, old_password, new_password)

def resolve_delete_user(info, user_id):
    return UserService.delete_user(user_id)

def resolve_list_users(info, page=1, per_page=10):
    return UserService.list_users(page, per_page)

def resolve_search_users(info, query):
    return UserService.search_users(query)
