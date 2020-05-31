from flask import Blueprint,jsonify,redirect,url_for,request

main = Blueprint('main',__name__)

@main.route("/",methods=['GET','POST'])
def home():
    return jsonify({"message":"home route"})


