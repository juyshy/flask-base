from flask import Blueprint, jsonify

from app.api.model.welcome import WelcomeModel
from app.models.book import Book
from app.schema.book import BookSchema
from app.schema.welcome import WelcomeSchema

home_api = Blueprint('api', __name__)

books_schema = BookSchema(many=True)

@home_api.route('/home_welcome')
def welcome():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = WelcomeModel()
    return WelcomeSchema().dump(result), 200


@home_api.route('/books')
def super_simple():
    books_list = Book.query.all()
    result = books_schema.dump(books_list)
    return jsonify(result)
