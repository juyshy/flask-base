from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for, jsonify
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from app import  csrf
from flask_rq2 import RQ

from app.schema.user import UserSchema

get_queue = RQ().get_queue

from app.models import User

account = Blueprint('account', __name__)


@account.route('/api-login', methods=['POST'])
@csrf.exempt
def api_login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    user = User.query.filter_by(email=email).first()
    #user = User.query.filter_by(email=email, password=password).first()
    if user is not None and user.password_hash is not None and  user.verify_password(password):
        access_token = create_access_token(identity=email)
        user_schema= UserSchema()
        user_data = user_schema.dump(user)
        return jsonify(message="Login succeeded", access_token=access_token, user=user_data)
    else:
        return jsonify(message="bad email or password"), 401


@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

