import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import User

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    users = graphene.List(UserObject)

    def resolve_users(self, info):
        query = UserObject.get_query(info)
        return query.all()

schema = graphene.Schema(query=Query)
