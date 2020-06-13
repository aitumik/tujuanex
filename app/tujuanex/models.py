from werkzeug.security import generate_password_hash,check_password_hash
from flask import current_app,request,url_for
from app import db

class Permission:
    ADMIN = 16
    MODERATOR = 8
    NORMAL = 4

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean,default=False,index=True)

    users = db.relationship('User',backref='role',lazy='dynamic')


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    full_name = db.Column(db.String(128))
    email = db.Column(db.String(128),unique=True)
    phone_number = db.Column(db.String(128),unique=True)
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(10))

    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    #other attributes
    description = db.Column(db.Text())

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    #Generate fake users
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        seed()
        for i in range(count):
            u = User(
                username=forgery_py.internet.user_name(True),
                full_name=forgery_py.name.full_name(),
                email = forgery_py.internet.email_address(),
                password_hash = forgery_py.lorem_ipsum.word()
            )
            db.session.add(u)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()

    def to_json(self):
        json_user = {
            "id":self.id,
            "url":url_for('main.user',username=self.username,_external=True),
            "username": self.username,
            "email":self.email,
            "phone":self.phone_number,
            "gender":self.gender,
            "description":self.description,
        }

        return json_user

    def __repr__(self):
        return "<User {}".format(self.username)

class Likes(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer,primary_key=True)
