"""Pokémon TCG app."""

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import User, PokemonWishlist, PokemonCollection, connect_db, db, bcrypt
from seed import seed_database

app = Flask(__name__)

# Configure the Flask app with your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri_here'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'whos-that-pokemon'

# Connect the database to the Flask app
connect_db(app)

# Initialize Bcrypt for password hashing
bcrypt.init_app(app)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
