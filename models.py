"""SQLAlchemy models for Pokémon Trading Card app."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User model for storing user information."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    image_url = db.Column(
        db.String,
        default='https://cdn.dribbble.com/users/2192291/screenshots/7482012/media/e829a380ecd3b768f4c6c7a4e3dd63cb.jpg?resize=1600x1200&vertical=center'
    )
    wishlist = db.relationship('PokemonWishlist', back_populates='user')
    collection = db.relationship('PokemonCollection', back_populates='user')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    def set_password(self, password):
        """Set user password."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def register(cls, username, email, password, image_url=None):
        """Register a new user."""
        hashed = bcrypt.generate_password_hash(password)

        hash_str = hashed.decode("utf8")

        return cls(username=username, email=email, password=hash_str, image_url=image_url)

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate a user by username and password."""
        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class PokemonWishlist(db.Model):
    """PokemonWishlist model for storing user wishlists."""

    __tablename__ = 'wishlists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='wishlist')
    pokemon_name = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime)
    acquired = db.Column(db.Boolean, default=False)


class PokemonCollection(db.Model):
    """PokemonCollection model for storing user collections."""

    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='collection')
    pokemon_name = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime)


def connect_db(app):
    """Connect this database to the provided Flask app."""
    db.app = app
    db.init_app(app)
