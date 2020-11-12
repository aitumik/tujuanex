from app import db
from app.tujuanex.models import User
from flask import Blueprint, jsonify, redirect, request, url_for
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required)

auth = Blueprint('auth',__name__)

@auth.route("/login",methods=['GET','POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get("username",None)
    password = request.json.get("password",None)

    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"msg":"Bad username or password"}),401
    if not user.verify_password(password):
        return jsonify({"msg":"Bad username or password"}),401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token),200
    
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

@auth.route("/forgot-password",methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.json.get("email",None):
        if not email:
            return jsonify({"msg":"email is required"}),500
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg":"user does not exists"}),404
        reset_token = ""
        return jsonify({"msg":"an email with password reset link has been sent to you"})
    return jsonify({"msg":"invalid request method"}),401

@auth.route("/reset-password/<token>",methods=['GET','POST'])
def reset_password(token):
    #TODO Check the token if its valid
    user_id = token #get user id based on token
    return jsonify({"msg":"password reset successfully"})


