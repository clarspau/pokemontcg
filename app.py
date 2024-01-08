"""Pokémon TCG app."""

import json
import random
import requests
from flask import Flask, render_template, redirect, session, flash, request, jsonify
from models import connect_db, db, User, Wishlist, Collection
from forms import LoginForm, RegisterForm, UserEditForm

app = Flask(__name__)
app.app_context().push()

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///pokemon"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "mikeisabeast"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Pokemon TCG API Configuration
API_KEY = ' '  # Enter your API key here
BASE_URL = 'https://api.pokemontcg.io/v2/'

# Connect to the database
connect_db(app)
db.create_all()

# Debug Toolbar (commented out for now)
# toolbar = DebugToolbarExtension(app)


@app.route('/')
def homepage():
    return redirect('/home')


@app.route('/home')
def show_home():
    if 'curr_user' in session:
        id = session['curr_user']
        user = User.query.get(id)
        return render_template('home.html', user=user)
    else:
        user = None
        return render_template('home.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def show_login():
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
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        image_url = form.image_url.data
        new_user = User.register(
            username=username, email=email, password=password, image_url=image_url)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/home')

    return render_template('register.html', form=form)


@app.route('/<int:user_id>/wishlist')
def show_wishlist(user_id):
    user = User.query.get(user_id)
    wishlist = Wishlist.query.filter_by(user_id=user_id).all()

    return render_template('wishlist.html', user=user, wishlist=wishlist)


@app.route('/<int:user_id>/collection')
def show_collection(user_id):
    user = User.query.get(user_id)
    collection = Collection.query.filter_by(user_id=user_id).all()

    return render_template('collection.html', user=user, collection=collection)


def get_setlist():
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
    sets = get_setlist_index()
    return render_template('set_index.html', sets=sets)


@app.route('/index/<set_id>')
def show_set(set_id):
    if 'curr_user' in session:
        user_id = session['curr_user']
        wishlist = Wishlist.query.filter_by(user_id=user_id).all()
        collection = Collection.query.filter_by(user_id=user_id).all()

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
    return render_template('index.html', sets=sets, cards=random_cards, wishlist=wishlist, collection=collection)


@app.route('/<int:user_id>/add_to_wishlist', methods=['POST'])
def add_to_wishlist(user_id):
    data = request.get_json()
    card_id = data.get('card_id')

    wishlist_item = Wishlist(user_id=user_id, card_id=card_id)

    db.session.add(wishlist_item)
    db.session.commit()

    return jsonify({'message': 'Added to wishlist successfully.'}), 200


@app.route('/<int:user_id>/add_to_collection', methods=['POST'])
def add_to_collection(user_id):
    data = request.get_json()
    card_id = data.get('card_id')

    collection_item = Collection(user_id=user_id, card_id=card_id)

    db.session.add(collection_item)
    db.session.commit()

    return jsonify({'message': 'Added to collection successfully.'}), 200


@app.route('/<int:user_id>/remove_from_wishlist', methods=['POST'])
def remove_from_wishlist(user_id):
    data = request.get_json()
    card_id = data.get('card_id')

    wishlist_item = Wishlist.query.filter_by(
        user_id=user_id, card_id=card_id).first()

    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        return jsonify({'message': 'Removed from wishlist successfully.'}), 200
    else:
        return jsonify({'message': 'Item not found in wishlist.'}), 404


@app.route('/<int:user_id>/remove_from_collection', methods=['POST'])
def remove_from_collection(user_id):
    data = request.get_json()
    card_id = data.get('card_id')

    collection_item = Collection.query.filter_by(
        user_id=user_id, card_id=card_id).first()

    if collection_item:
        db.session.delete(collection_item)
        db.session.commit()
        return jsonify({'message': 'Removed from collection successfully.'}), 200
    else:
        return jsonify({'message': 'Item not found in collection.'}), 404


@app.route('/logout')
def logout():
    session.pop('curr_user', None)
    return redirect('/home')


@app.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.image_url = form.image_url.data

        db.session.commit()
        return redirect(f'/{user_id}')

    return render_template('edit_user.html', form=form, user=user)


if __name__ == '__main__':
    app.run(debug=True)
