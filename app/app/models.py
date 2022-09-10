from datetime import datetime
from hashlib import md5
#from msilib.schema import tables
from time import time
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import app, db, login
from flask import url_for


#followers = db.Table(
#    'followers',
#    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
    
#)


class User(UserMixin, db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bmiwerte = db.relationship('Bmi', backref='user', lazy='dynamic')
    kommentareintrag = db.relationship('Kommentar', backref='userkommentar', lazy='dynamic')
    
    #posts = db.relationship('Post', backref='author', lazy='dynamic')
    #about_me = db.Column(db.String(140))
    #last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    #followed = db.relationship(
    #    'User', secondary=followers,
    #    primaryjoin=(followers.c.follower_id == id),
    #    secondaryjoin=(followers.c.followed_id == id),
    #    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    #def follow(self, user):
    #    if not self.is_following(user):
    #        self.followed.append(user)

    #def unfollow(self, user):
    #    if self.is_following(user):
    #        self.followed.remove(user)

    #def is_following(self, user):
    #    return self.followed.filter(
    #        followers.c.followed_id == user.id).count() > 0

    # def followed_posts(self):
    #    followed = Post.query.join(
    #        followers, (followers.c.followed_id == Post.user_id)).filter(
    #            followers.c.follower_id == self.id)
    #    own = Post.query.filter_by(user_id=self.id)
    #    return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def to_dict(self, include_email=False):
        data = {
        'id': self.id,
        'username': self.username,
        'bmiposts_count': self.bmiwerte.count(),
        'kommentare_count': self.kommentareintrag.count(),
        '_links': {
        'self': url_for('get_user', id=self.id),
        'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data


    def followers_to_collection(self):
        data = {'items': [item.to_dict() for item in self.followers]}
        return data

    def followed_to_collection(self):
        data = {'items': [item.to_dict() for item in self.followed]}
        return data

    def posts_to_collection(self):
        data = {'items': [item.to_dict() for item in self.posts]}
        return data

    @staticmethod
    def to_collection():
        users = User.query.all()
        data = {'items': [item.to_dict() for item in users]}
        return(data)

  

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Bmi(db.Model):
    __tablename__='bmi'
    id = db.Column(db.Integer, primary_key=True)
    gewicht = db.Column(db.Float)
    groesse = db.Column(db.Float)
    bmiwert = db.Column(db.Float)
    beschreibung = db.Column(db.Text(1000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __init__(self, gewicht, groesse, bmiwert, beschreibung, timestamp, user_id):
        self.gewicht = gewicht
        self.groesse = groesse
        self.bmiwert = bmiwert
        self.beschreibung = beschreibung
        self.timestamp = timestamp
        self.user_id = user_id
        
    def get_kommentare(self):
        print(self.id)
        kommentare = Kommentar.query.filter(Kommentar.bmi_id==self.id)
        return kommentare
       


class Kommentar(db.Model):
    __tablename__='kommentar'
    id = db.Column(db.Integer, primary_key=True)
    kommentar = db.Column(db.Text(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bmi_id = db.Column(db.Integer, db.ForeignKey('bmi.id'))

    def __init__(self, kommentar, user_id, bmi_id):
        self.kommentar = kommentar
        self.user_id = user_id
        self.bmi_id = bmi_id
        
    def get_user(self):
        username = User.query.get(self.user_id)
        return username.username

    def __repr__(self):
        return '<Bmi {}>'.format(self.body)

    def to_dict(self):
        data = {
            'id' : self.id,
            'url': url_for('get_posts', id=self.id, _external=True),
            'body': self.body,
            'timestamp': self.timestamp,
            'author': url_for('get_user', id=self.user_id, _external=True)
            }

        return data



    @staticmethod
    def to_collection():
        resources = Rezepteintrag.query.all()
        data = {'items': [item.to_dict() for item in resources]}
        return(data)

