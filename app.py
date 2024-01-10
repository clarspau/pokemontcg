"""Pokémon TCG Flask App"""

from flask import Flask, render_template, redirect, session, flash, request, jsonify
from models import connect_db, db, User, Like
from forms import LoginForm, RegisterForm, UserEditForm
import requests
import random
import json

app = Flask(__name__)
app.app_context().push()

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///pokemontcg"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "who-is-that-pokemon"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Pokemon TCG API Configuration
API_KEY = 'ce11a777-d3b8-4be0-a68a-c32d7d05a204'
BASE_URL = 'https://api.pokemontcg.io/v2/'

# Connect to the database and create tables
connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    """Redirect to the home page."""

    return redirect('/home')


@app.route('/home')
def show_home():
    """Show the home page with user information."""

    if 'curr_user' in session:
        id = session['curr_user']
        user = User.query.filter_by(id=id).first()
        return render_template('home.html', user=user)
    else:
        user = ''
        return render_template('home.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def show_login():
    """Show the login page and handle user authentication."""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['curr_user'] = user.id
            return redirect('/home')
        else:
            flash('Incorrect Username or Password!')
            return redirect('/login')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def show_register():
    """Show the registration page and handle user registration."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        profile_img = form.profile_img.data
        email = form.email.data
        about_me = form.about_me.data
        new_user = User.register(
            username, password, profile_img, email, about_me)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/home')

    return render_template('register.html', form=form)


@app.route('/<int:id>/likes')
def show_likes(id):
    """Show the liked cards for a specific user."""

    likes = Like.query.filter_by(user_id=id).all()
    like_ids = [like.card_id for like in likes]
    json_likes = json.dumps(like_ids)

    cards = []

    for like in likes:
        url = f'{BASE_URL}cards/{like.card_id}'
        headers = {'x-api-key': API_KEY}
        response = requests.get(url, headers=headers)
        raw_data = response.json()
        data = raw_data['data']

        # Check if the 'rarity' field is present in the data
        if 'rarity' in data:
            rarity = data['rarity']
        else:
            rarity = 'Common'

        # Check if the 'cardmarket' and 'averageSellPrice' fields are present in the data
        if 'cardmarket' in data and 'prices' in data['cardmarket'] and 'averageSellPrice' in data['cardmarket']['prices']:
            price = data['cardmarket']['prices']['averageSellPrice']
        else:
            price = None

        # Append the card information to the list of cards if both 'rarity' and 'price' are present
        cards.append({
            'id': data['id'],
            'name': data['name'],
            'image': data['images']['small'],
            'rarity': rarity,
            'price': price
        })

    return render_template('liked.html', cards=cards, like_ids=json_likes)


def get_setlist():
    """Get a list of card sets."""

    url = f'{BASE_URL}sets'
    sets = []
    headers = {'x-api-key': API_KEY}
    response = requests.get(url, headers=headers)
    raw_data = response.json()
    data = raw_data['data']
    for card_set in data:
        name = card_set['name']
        id = card_set['id']
        sets.append({
            'id': id,
            'name': name
        })
    return sets[:24]


def get_setlist_index():
    """Get a list of card sets for the index."""

    url = f'{BASE_URL}sets'
    sets = []
    headers = {'x-api-key': API_KEY}
    response = requests.get(url, headers=headers)
    raw_data = response.json()
    data = raw_data['data']
    for card_set in data:
        sets.append(card_set)
    return sets[:24]


@app.route('/index')
def show_index():
    """Show the index page with a list of card sets."""

    sets = get_setlist_index()
    return render_template('set_index.html', sets=sets)


@app.route('/index/<set_id>')
def show_set(set_id):
    """Show the cards for a specific card set."""

    if 'curr_user' in session:
        user_id = session['curr_user']
        likes = Like.query.filter_by(user_id=user_id).all()
        like_ids = [like.card_id for like in likes]
        json_likes = json.dumps(like_ids)

    sets = get_setlist()
    url = f'{BASE_URL}cards?q=set.id:{set_id}'
    cards = []
    headers = {'x-api-key': API_KEY}
    response = requests.get(url, headers=headers)
    raw_data = response.json()
    data = raw_data['data']
    for card in data:
        cards.append(card)
    random_cards = random.sample(cards, min(len(cards), 100))
    return render_template('index.html', sets=sets, cards=random_cards, like_ids=json_likes)


@app.route('/<int:id>')
def show_user(id):
    """Show the user's profile."""

    user = User.query.filter_by(id=id).first()
    return render_template('profile.html', user=user)


@app.route('/addlike', methods=['POST'])
def add_like():
    """Add a liked card to the user's collection."""

    data = request.get_json()
    card_id = data.get('card_id')
    if 'curr_user' in session:
        user_id = session['curr_user']
    else:
        return jsonify({'message': 'Nope.'}), 500
    like = Like(user_id=user_id, card_id=card_id)

    db.session.add(like)
    db.session.commit()

    return jsonify({'message': 'Like added to database.'}), 200


@app.route('/deletelike', methods=['POST'])
def delete_like():
    """Delete a liked card from the user's collection."""

    user_id = session['curr_user']
    data = request.get_json()
    card_id = data.get('card_id')

    like = Like.query.filter_by(user_id=user_id, card_id=card_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'message': 'Like deleted from database.'}), 200
    else:
        return jsonify({'message': 'Like not found in database.'}), 404


@app.route('/logout')
def logout():
    """Logout the user."""

    session.pop('curr_user', None)
    return redirect('/home')


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    """Show the edit user page and handle user profile updates."""

    user = User.query.filter_by(id=id).first()
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.profile_img = form.profile_img.data
        user.about_me = form.about_me.data

        db.session.commit()
        return redirect(f'/{id}')

    return render_template('edit_user.html', form=form, user=user)
