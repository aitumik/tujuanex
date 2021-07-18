from werkzeug.security import generate_password_hash,check_password_hash
from flask import current_app,request,url_for
from app import db
from datetime import datetime
import json

#associtation table
followers = db.Table("followers",
        db.Column("follower_id",db.Integer,db.ForeignKey("users.id")),
        db.Column("followed_id",db.Integer,db.ForeignKey("users.id")),
)

class Permission:
    ADMIN = 16
    MODERATOR = 8
    NORMAL = 4

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    description = db.Column(db.String(100))
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        data = {"name":self.name,"description":self.description}
        return data

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    full_name = db.Column(db.String(128))
    email = db.Column(db.String(128),unique=True)
    phone_number = db.Column(db.String(128),unique=True)
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    location = db.Column(db.String(100))
    bio = db.Column(db.Text())
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    posts = db.relationship("Post",backref="author",lazy="dynamic")
    description = db.Column(db.Text())
    image = db.Column(db.String(100))

    # New feature(yeeey....)
    profile_visits = db.Column(db.Integer,default=0)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 2

    #follow
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    #unfollow
    def unfollow(user):
        if self.is_following(user):
            self.followed.remove(user)

    def like(self,post):
       pass 

    def unlike(self,post):
        pass

    def to_json(self):
        json_user = {
            "id":self.id,
            "url":url_for('main.user',username=self.username,_external=True),
            "username": self.username,
            "email":self.email,
            "phone":self.phone_number,
            "gender":self.gender,
            "description":self.description,
            "followers":len(self.followers.all()),
            "following":len(self.followed.all()),
            "posts":[post.to_json() for post in self.posts.all()],
        }

        return json_user

    def toJson(self):
        return json.dumps(self,default=lambda o:
                o.__dict__,sort_keys=True,indent=4)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        data = {
            "id":self.id,
            "url":url_for('main.user',username=self.username,_external=True),
            "username": self.username,
            "email":self.email,
            "phone":self.phone_number,
            "gender":self.gender,
            "description":self.description,
            "followers":len(self.followers.all()),
            "following":len(self.followed.all()),
            "posts":[post.to_json() for post in self.posts.all()],
        }
        return data

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    #one to many relationship
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship("Comment",backref="post",lazy="dynamic")
    likes = db.relationship("Like",lazy="dynamic")
    image = db.Column(db.String(255))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        data = {
            "id":self.id,
            "body":self.body,
            "timestamp":self.timestamp,
            "user_id": self.author.id,
            "comments": [c.to_json() for c in self.comments]
            }
        return data

    def __repr__(self):
        return "<Post {}>".format(self.body)

class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer,primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"))

    def to_json(self):
        data = {}
        return data

    def save(self):
        db.session.add(self)
        db.session.commit()

class Comment(db.Model): 
    __tablename__ = "comments" 

    id = db.Column(db.Integer,primary_key=True) 
    body = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    updated = db.Column(db.DateTime)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"))
    blocked = db.Column(db.Boolean,default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        data = {
            "body": self.body
            }
        return data

    def __repr__(self):
        return "<Comment {}>".format(self.body)

class Image(db.Model):
    __tablename__ = "images"

    id  = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(255),unique=True)

    def to_json(self):
        data = \
        {
            "url":self.url
        }
        return data

    def save(self):
        db.session.add(self)
        db.session.commit()

class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        data = {}
        return data












