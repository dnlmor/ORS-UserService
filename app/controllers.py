# app/controllers.py
from flask import Blueprint
from flask_graphql import GraphQLView
from .schema import schema

user_blueprint = Blueprint('user', __name__)

user_blueprint.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)
