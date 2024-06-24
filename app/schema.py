import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import User as UserModel
from .resolvers import (
    resolve_create_user, resolve_login_user, resolve_get_user,
    resolve_update_user, resolve_change_password, resolve_delete_user,
    resolve_list_users, resolve_search_users
)

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class Query(graphene.ObjectType):
    get_user = graphene.Field(User, id=graphene.Int(required=True))
    list_users = graphene.List(User, page=graphene.Int(), per_page=graphene.Int())
    search_users = graphene.List(User, query=graphene.String(required=True))

    def resolve_get_user(self, info, id):
        return resolve_get_user(info, id)

    def resolve_list_users(self, info, page=1, per_page=10):
        return resolve_list_users(info, page, per_page)

    def resolve_search_users(self, info, query):
        return resolve_search_users(info, query)

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, username, email, password):
        return resolve_create_user(info, username, email, password)

class LoginUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(lambda: User)
    token = graphene.String()

    def mutate(self, info, email, password):
        return resolve_login_user(info, email, password)

class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        username = graphene.String()
        email = graphene.String()

    user = graphene.Field(lambda: User)

    def mutate(self, info, user_id, username=None, email=None):
        return resolve_update_user(info, user_id, username, email)

class ChangePassword(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, user_id, old_password, new_password):
        success = resolve_change_password(info, user_id, old_password, new_password)
        return ChangePassword(success=success)

class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, user_id):
        success = resolve_delete_user(info, user_id)
        return DeleteUser(success=success)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    update_user = UpdateUser.Field()
    change_password = ChangePassword.Field()
    delete_user = DeleteUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
