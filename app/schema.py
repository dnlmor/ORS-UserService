import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import User as UserModel
from app import db, bcrypt
from flask_jwt_extended import create_access_token

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, username, email, password):
        user = UserModel(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user)

class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    access_token = graphene.String()

    def mutate(self, info, username, password):
        user = UserModel.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=username)
            return Login(access_token=access_token)
        raise Exception('Invalid username or password')

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login = Login.Field()

class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(User, id=graphene.Int())

    def resolve_users(self, info):
        return UserModel.query.all()

    def resolve_user(self, info, id):
        return UserModel.query.get(id)

schema = graphene.Schema(query=Query, mutation=Mutation)
