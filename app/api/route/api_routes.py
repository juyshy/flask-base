from flask import Blueprint, jsonify, request

from app.api.model.welcome import WelcomeModel
from app.models.book import Book
from app.models.photo import Photo
from app.models.ocr_data import OcrData
from app.schema.book import BookSchema
from app.schema.photo import PhotoSchema
from app.schema.ocr_data import OcrDataSchema
from app.schema.welcome import WelcomeSchema
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

from  datetime import datetime
api = Blueprint('api', __name__)

books_schema = BookSchema(many=True)
ocr_data_schema = OcrDataSchema()
ocr_datas_schema = OcrDataSchema(many=True)

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
@cross_origin()
def photo_list():
    page = int(request.args.get('page'))
    perPage = int(request.args.get('perPage'))
    if perPage > 2000:
        return jsonify(message="too much!"), 400
    else:
        photos_list = Photo.query.paginate(page=page, per_page= perPage)
        result = photos_schema.dump(photos_list.items)
        return jsonify({"current_page": page, "data":result})




@api.route('/photo/<int:photo_id>', methods=['GET'])
@cross_origin()
def photo(photo_id: int):
    photo = Photo.query.filter_by(id=photo_id).first()
    if photo:
        result = photo_schema.dump(photo)
        return jsonify(result)
    else:
        return jsonify(message="Photo was not found for id: " + str(photo_id)), 404



@api.route('/ocrdata/<int:id>', methods=['GET'])
@cross_origin()
def ocrdata(id: int):
    photo = Photo.query.filter_by(id=id).first()
    ocr_data = OcrData.query.filter_by(photo_id=photo.id).first()
    if ocr_data:
        result = ocr_data_schema.dump(ocr_data)
        return jsonify(result)
    else:
        return jsonify(message="Photo was not found for id: " + str(id)), 404


@api.route('/ocrdata/<int:id>', methods=['PATCH'])
@cross_origin()
@csrf.exempt
def ocrdata_patch_saveselection(id: int):
    ocrData = OcrData.query.filter_by(id=id).first()
    saved_selection = request.json['saved_selection']
    user_id = request.json['user_id']

    # $user_id = $request->user_id; !!!! TODO
    if saved_selection:
        ocrData.saved_selection = saved_selection
        ocrData.user_id = user_id
        db.session.commit()
        return 'ocrdata updated'
    else:
        return 'nothing to update'



@api.route('/ocrdata/nosavedselection', methods=['GET'])
@cross_origin()
def noSavedSelection():
    ocrDatasId = OcrData.query.filter_by(saved_selection=None)
    if ocrDatasId:
        mymodelschema = OcrDataSchema(many=True, only=['id','photo_id'])
        output = mymodelschema.dump(ocrDatasId)
        return jsonify(output)
    else:
        return jsonify(message="No ocr data was not found with no saved selection."  ), 404


@api.route('/ocrdata/latest', methods=['GET'])
@cross_origin()
def latest_ocrdata():
    #$ocrDatasId= DB::table('ocr_data')->select('id', 'photo_id')->whereRaw('saved_selection is not NULL')->orderBy('id','desc')->limit(1)->get();
    ocrDatasId = OcrData.query.filter(OcrData.saved_selection!=None).order_by(OcrData.id.desc()).limit(1).all()
    if ocrDatasId:
        mymodelschema = OcrDataSchema(many=True, only=['id','photo_id'])
        output = mymodelschema.dump(ocrDatasId)
        return jsonify(output)
    else:
        return jsonify(message="No ocr data was not found."  ), 404

@api.route('/photo/missingdata', methods=['GET'])
@cross_origin()
def photo_missingdata():
    photos = Photo.query.filter((Photo.casetteNums==None) |  ( Photo.pagenum==None) | ((Photo.pagenum > 1) & (Photo.pageOne == None)))
    if photos:
        mymodelschema = PhotoSchema(many=True, only=['id'])
        output = mymodelschema.dump(photos)
        return jsonify(output)
    else:
        return jsonify(message="No photo ids was not found with missing data. " ), 404

@api.route('/photo/missingAllMetadata', methods=['GET'])
@cross_origin()
def missingAllMetadata():
    photos = Photo.query.filter((Photo.casetteNums==None) & ( Photo.pagenum==None) & (Photo.pageOne==None) & (Photo.notes == None))
    if photos:
        mymodelschema = PhotoSchema(many=True, only=['id'])
        output = mymodelschema.dump(photos)
        return jsonify(output)
    else:
        return jsonify(message="No photo ids was not found with missing data. " ), 404


@api.route('/add_photo', methods=['POST'])
@cross_origin()
@jwt_required()
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


@api.route('/update_photo/<int:id>', methods=['PUT'])
@cross_origin()
#@jwt_required()
@csrf.exempt
def update_photo(id: int):
    photo = Photo.query.filter_by(id = id).first()
    if photo:
        photo.updated_at = datetime.now()
        #photo.user_id =  #

        if 'notes' in  request.json:
            photo.notes = request.json['notes']
        if 'pagenum' in  request.json:
            photo.pagenum = request.json['pagenum']
        if 'pageOne' in  request.json:
            photo.pageOne = request.json['pageOne']
        if 'aml' in  request.json:
            photo.aml = request.json['aml']
        if 'name' in  request.json:
            photo.name = request.json['name']
        if 'filePath' in  request.json:
            photo.filePath = request.json['filePath']
        if 'casetteNums' in  request.json:
            photo.casetteNums = request.json['casetteNums']
        if 'notes' in  request.json:
            photo.notes = request.json['notes']
        if 'taken' in  request.json:
            photo.taken = request.json['taken']
        if 'rotation' in  request.json:
            photo.rotation = request.json['rotation']
        db.session.commit()
        return jsonify(message="Photo data was updated"), 202
    else:
        return jsonify(message="Photo was not found."), 404



@api.route('/delete_photo/<int:id>', methods=['DELETE'])
#@jwt_required()
@csrf.exempt
def delete_photo(id: int):
    photo = Photo.query.filter_by(id=id).first()
    if photo:
        db.session.delete(photo)
        db.session.commit()
        return jsonify(message="Photo was deleted"), 202
    else:
        return jsonify(message="Photo was not found."), 404

