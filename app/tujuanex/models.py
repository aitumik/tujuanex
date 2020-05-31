from werkzeug.security import generate_password_hash,check_password_hash
from app import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    full_name = db.Column(db.String(128))
    email = db.Column(db.String(128),unique=True)
    phone_number = db.Column(db.String(128),unique=True)
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(10))
    
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

    def __repr__(self):
        return "<User {}".format(self.username)




