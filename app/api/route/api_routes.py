from flask import Blueprint, jsonify, request

from app.api.model.welcome import WelcomeModel
from app.models.book import Book
from app.models.photo import Photo
from app.schema.book import BookSchema
from app.schema.photo import PhotoSchema
from app.schema.welcome import WelcomeSchema

api = Blueprint('api', __name__)

books_schema = BookSchema(many=True)

@api.route('/home_welcome')
def welcome():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    result = WelcomeModel()
    return WelcomeSchema().dump(result), 200


@api.route('/books')
def super_simple():
    books_list = Book.query.all()
    result = books_schema.dump(books_list)
    return jsonify(result)


photo_schema = PhotoSchema()
photos_schema = PhotoSchema(many=True)

@api.route('/photo', methods=['GET'])
def photo_list():
    page = int(request.args.get('page'))
    perPage = int(request.args.get('perPage'))
    if perPage > 2000:
        return jsonify(message="too much!"), 400
    else:
        photos_list = Photo.query.paginate(page=page, per_page= perPage)
        result = photos_schema.dump(photos_list.items)
        return jsonify(result)
