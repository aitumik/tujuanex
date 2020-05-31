from flask import Blueprint
from flask import jsonify,request,url_for,redirect

from app.tujuanex.models import User
from app import db

auth = Blueprint('auth',__name__)

@auth.route("/login",methods=['GET','POST'])
def login():
    return jsonify({"message":"login successful"})

@auth.route("/register",methods=['GET','POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    #get the username and password from the json body
    username = request.json.get("username",None)
    password = request.json.get("password",None)
    email = request.json.get("email",None)
    phone_number = request.json.get("phone",None)

    if not username:
        return jsonify({"msg":"Missing username parameter"}),400
    if not password:
        return jsonify({"msg":"Missing password parameter"}),400
    if not email:
        return jsonify({"msg":"Missing email parameter"}),400

    user = User.query.filter_by(username=username).first()
    if user is not None:
        return jsonify({"msg":"username already exists"})

    user = User.query.filter_by(email=email).first()
    if user is not None:
        return jsonify({"msg":"email already registered"})

    #register the user
    user = User(username=username,email=email)
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify({"msg":str(e)}),500
    return jsonify({"msg":"user created successfully"}),201


