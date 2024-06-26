from flask import Blueprint
from flask_graphql import GraphQLView
from app.schema import schema

bp = Blueprint('api', __name__)

bp.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)
