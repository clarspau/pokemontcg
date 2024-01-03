"""SQLAlchemy models for Pokémon Trading Card app."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User model for storing user information."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    wishlist = db.relationship('PokemonWishlist', back_populates='user')
    collection = db.relationship('PokemonCollection', back_populates='user')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class PokemonWishlist(db.Model):
    """PokemonWishlist model for storing user wishlists."""

    __tablename__ = 'wishlists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='wishlist')
    pokemon_name = db.Column(db.String(100))
    date_added = db.Column(db.DateTime)
    acquired = db.Column(db.Boolean, default=False)


class PokemonCollection(db.Model):
    """PokemonCollection model for storing user collections."""
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='collection')
    pokemon_name = db.Column(db.String(100))
    date_added = db.Column(db.DateTime)


def connect_db(app):
    """Connect this database to the provided Flask app."""
    db.app = app
    db.init_app(app)
