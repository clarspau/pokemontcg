from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=5)])
    image_url = StringField('Profile Image Link')
    email = StringField('Email', validators=[DataRequired()])


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=5)])


class UserEditForm(FlaskForm):

    username = StringField('Username')
    email = StringField('Email')
    image_url = StringField('Profile Image')
