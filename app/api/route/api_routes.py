from flask import Blueprint, jsonify, request

from app.api.model.welcome import WelcomeModel
from app.models.book import Book
from app.models.photo import Photo
from app.schema.book import BookSchema
from app.schema.photo import PhotoSchema
from app.schema.welcome import WelcomeSchema
from  datetime import datetime
api = Blueprint('api', __name__)

books_schema = BookSchema(many=True)

from app import db, csrf

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




@api.route('/photo/<int:photo_id>', methods=['GET'])
def photo(photo_id: int):
    photo = Photo.query.filter_by(id=photo_id).first()
    if photo:
        result = photo_schema.dump(photo)
        return jsonify(result)
    else:
        return jsonify(message="Photo was not found for id: " + str(photo_id)), 404



@api.route('/add_photo', methods=['POST'])
#@jwt_required()
@csrf.exempt # todo: remove this
def add_photo():
    id = request.json['id']
    user_id = request.json['user_id']
    pagenum = request.json['pagenum']
    pageOne = None if request.json['pageOne'] == 'null' else request.json['pageOne']
    aml = None if  request.json['aml'] == 'null' else  request.json['aml']
    name = request.json['name']
    filePath = request.json['filePath']
    casetteNums = None if  request.json['casetteNums'] == 'null' else request.json['casetteNums']
    notes = None if request.json['notes'] == 'null' else request.json['notes']
    taken = datetime.strptime(request.json['taken'], '%Y-%m-%d %H:%M:%S')
    created_at = datetime.strptime(request.json['created_at'][:19], '%Y-%m-%dT%H:%M:%S'),
    updated_at = datetime.strptime(request.json['updated_at'][:19], '%Y-%m-%dT%H:%M:%S'),
    rotation = None if request.json['rotation'] == 'null' else request.json['rotation']
    created_at = created_at[0]
    updated_at = updated_at[0]

    new_photo = Photo(id=id,
                  user_id=user_id,
                  pagenum=pagenum,
                  pageOne=pageOne,
                  aml=aml,
                  name=name,
                  filePath=filePath,
                  casetteNums=casetteNums,
                  notes=notes,
                  taken=taken,
                  created_at=created_at,
                  updated_at=updated_at,
                  rotation=rotation)
    db.session.add(new_photo)
    db.session.commit()
    return jsonify(message="Photo added"), 201

