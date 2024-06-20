from flask import Flask
from .extensions import db, bcrypt
from .schema import schema
from flask_graphql import GraphQLView

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    bcrypt.init_app(app)

    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

    with app.app_context():
        db.create_all()

    return app
