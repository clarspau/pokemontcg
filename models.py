from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()


bcrypt = Bcrypt()


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    profile_img = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, nullable=False)
    about_me = db.Column(db.Text, nullable=True)


    likes = db.relationship('Like', backref='user', lazy=True)

    @classmethod
    def register(cls, username, password, profile_img, email, about_me):
        hashed = bcrypt.generate_password_hash(password)

        hash_str = hashed.decode("utf8")

        return cls(username=username, password=hash_str, profile_img=profile_img, email=email, about_me=about_me)

    @classmethod
    def authenticate(cls, username, password):
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False


class Like(db.Model):

    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    card_id = db.Column(db.Text, nullable=False)


def connect_db(app):
    db.app = app
    db.init_app(app)
