from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    profile_img = StringField('Profile Image Link')
    email = StringField('Email', validators=[DataRequired()])
    about_me = TextAreaField('Tell us about yourself')


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserEditForm(FlaskForm):

    username = StringField('Username')
    email = StringField('Email')
    profile_img = StringField('Profile Image')
    about_me = TextAreaField('Tell us about yourself')