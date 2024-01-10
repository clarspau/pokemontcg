"""Seed file to make sample data for db."""

from app import app, db
from models import User, Like

# Drop and recreate the database tables
db.drop_all()
db.create_all()

# Create test users
u1 = User.register('ash', 'asdasd', 'https://mir-s3-cdn-cf.behance.net/projects/404/d51aa2187231133.Y3JvcCwyMDQ1LDE2MDAsNDAwLDA.jpg',
                   'testuser1@emaill.com', 'I''m Ash Ketchum!')
u2 = User.register('gary', 'asdasd', 'https://64.media.tumblr.com/f44d3377893db327a2df174ce24402d7/0dc4ad9bc471e48e-fc/s400x600/035b55b85e4a440709a5a66ab791fddeff690d62.png',
                   'testuser2@email.com', 'I''m Gary Oak!')

# Add users to the session and commit changes to the database
db.session.add_all([u1, u2])
db.session.commit()

# Create test likes
l1 = Like(user_id=u1.id, card_id='base1-1')
l2 = Like(user_id=u1.id, card_id='base1-2')
l3 = Like(user_id=u2.id, card_id='base1-3')

# Add likes to the session and commit changes to the database
db.session.add_all([l1, l2, l3])
db.session.commit()
