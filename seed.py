from app import app, db
from models import User, Like

db.drop_all()
db.create_all()

# create test users
u1 = User.register('mike3', 'asdasd', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWZutqeP6MC5d1naQif-HEGq9LwFWRrQax-g&usqp=CAU', 'testuser1@gmail.com', 'About me for test user')
u2 = User.register('mike2', 'asdasd', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWZutqeP6MC5d1naQif-HEGq9LwFWRrQax-g&usqp=CAU', 'testuser2@gmail.com', 'Blah Blah Blah')

db.session.add_all([u1, u2])
db.session.commit()

# create test likes
l1 = Like(user_id=u1.id, card_id='base1-1')
l2 = Like(user_id=u1.id, card_id='base1-2')
l3 = Like(user_id=u2.id, card_id='base1-3')

db.session.add_all([l1, l2, l3])
db.session.commit()