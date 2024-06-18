import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import User
from app import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        user = User(username=username, email=email)
        user.password = password
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user)

class AuthenticateUser(graphene.Mutation):
    access_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return AuthenticateUser(access_token=access_token)
        return AuthenticateUser(access_token='')

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    def resolve_user(self, info, id):
        return User.query.get(id)

    def resolve_users(self, info):
        return User.query.all()

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    authenticate_user = AuthenticateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
