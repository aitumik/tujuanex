from flask import Blueprint,jsonify,redirect,url_for,request
from flask_jwt_extended import jwt_required,get_jwt_identity

main = Blueprint('main',__name__)

@main.route("/",methods=['GET','POST'])
def home():
    return jsonify({"message":"home route"})

@main.route("/users",methods=['GET','POST'])
@jwt_required
def users():
    current_user = get_jwt_identity()
    return jsonify({"msg":"You are good to go"})
