"""Seed file to make sample data for db."""

from app import app, db
from models import User, Like

db.drop_all()
db.create_all()

# create test users
u1 = User.register('ash', 'asdasd', 'https://pngimg.com/d/pokeball_PNG21.png',
                   'testuser1@gmail.com', 'Hi, I am Ash!')
u2 = User.register('gary', 'asdasd', 'https://pngimg.com/d/pokeball_PNG21.png',
                   'testuser2@gmail.com', 'Hi, I am Gary!')

db.session.add_all([u1, u2])
db.session.commit()

# create test likes
l1 = Like(user_id=u1.id, card_id='base1-1')
l2 = Like(user_id=u1.id, card_id='base1-2')
l3 = Like(user_id=u2.id, card_id='base1-3')

db.session.add_all([l1, l2, l3])
db.session.commit()
