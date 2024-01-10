"""Models for the app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = 'users'

    # User Model Fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    profile_img = db.Column(
        db.Text,
        # Set the default image URL here
        default='https://i.etsystatic.com/29758262/r/il/5244a5/4041853302/il_570xN.4041853302_jg3g.jpg'
    )
    email = db.Column(db.Text, nullable=False)
    about_me = db.Column(db.Text, nullable=True)

    # Relationship with Like Model
    likes = db.relationship('Like', backref='user', lazy=True)

    @classmethod
    def register(cls, username, password, email, about_me, profile_img=None):
        # Hash the password before storing it
        hashed = bcrypt.generate_password_hash(password)
        hash_str = hashed.decode("utf8")
        return cls(
            username=username,
            password=hash_str,
            profile_img=profile_img or 'default_image_url.jpg',  # Use default if not provided
            email=email,
            about_me=about_me
        )

    @classmethod
    def authenticate(cls, username, password):
        # Authenticate user by comparing hashed password
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    def __repr__(self):
        # String representation of User instance
        return f"<User id={self.id}, username={self.username}, email={self.email}>"


class Like(db.Model):
    __tablename__ = 'likes'

    # Like Model Fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    card_id = db.Column(db.Text, nullable=False)
