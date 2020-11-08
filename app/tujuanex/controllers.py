from flask import Blueprint,jsonify,redirect,url_for,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from .models import User,Post,Comment
from app import db

main = Blueprint('main',__name__)

@main.route("/",methods=['GET','POST'])
def home():
    #show home for api
    return jsonify({"message":"home route"})

#***********************************#
#Posts

@main.route("/posts",methods=['GET'])
@jwt_required
def posts():
    if request.method == 'GET':
        posts = Post.query.all()
        res = [post.to_json() for post in posts]
        return jsonify({"msg":res})
    return jsonify({"msg":"invalid requests method"}),403

@main.route("/post/create",methods=['POST'])
@jwt_required
def createpost():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        post_body = request.json.get("body",None)
        if post is None: 
            return jsonify({"msg":"body field is missing"}),302
        #TODO accept image here from the post
        post = Post(body=post_body,author=current_user)
        try:
            post.save()
        except Exception as e:
            return jsonify({"msg":str(e)}),500
        return jsonify({"msg":"post created successfully"}),201
    return jsonify({"msg":"invalid request method"})

@main.route("/post/edit/<int:post_id>",methods=['PUT'])
@jwt_required
def editpost(post_id):
    post = Post.query.get(int(post_id))
    if request.method == 'PUT':
        #sure the method is put
        #now check if the user owns the post
        body = request.json.get("body")
        post.body = body
        try:
            post.save()
            return jsonify({"msg":"post updated successfully"})
        except Exception as e:
            return jsonfi({"msg":str(e)}),302
    return jsonify({"msg":"invalid request method"}),304

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
 
