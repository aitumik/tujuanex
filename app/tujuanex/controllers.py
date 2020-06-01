from flask import Blueprint,jsonify,redirect,url_for,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from .models import User
from app import db

main = Blueprint('main',__name__)

@main.route("/",methods=['GET','POST'])
def home():
		#render the api documentation here
    return jsonify({"message":"home route"})

@main.route("/user/<username>",methods=['GET','POST'])
def user(username):
    user = User.query.filter_by(username=username).first()
    return jsonify(user.to_json())

@main.route("/users",methods=['GET','POST'])
def users():
    users = User.query.all()[:50]
    return jsonify({"count":len(users),"results":list([user.to_json() for user in users])})


#writing the route for editing profile of a user
@main.route("/edit-profile/<username>",methods=['GET','POST'])
@jwt_required
def edit_profile(username):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if current_user != user.username:
        return jsonify({"msg":"You are not allowed to edit this profile"}),401
    if not request.is_json:
        return jsonify({"msg":"You must provide json data"}),404
    username = request.json.get("username",user.username)
    email = request.json.get("email",user.email)
    phone = request.json.get("phone",user.phone_number)
    description = request.json.get("description",user.description)
    gender = request.json.get("gender",user.gender)
    try:
        user.username = username
        user.email = email
        user.phone_number = phone
        user.description = description
        user.gender = gender
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify({"msg":str(e)}),500
        db.session.rollback()
    return jsonify({"msg":"profile modified successfully"}),201
 
 
