from wtforms import StringField, IntegerField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Email, email_validator
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """Creates a form to register users"""

    username = StringField("Username", validators=[InputRequired(
        message="Username is required"), Length(max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(message="Password is required")])
    email = EmailField("Email", validators=[InputRequired(message="Email is required"), Email(
        message="Please enter a valid email address"), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(
        message="First Name is required"), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(
        message="Last Name is required"), Length(max=30)])


class LoginForm(FlaskForm):
    """Creates a form to Login users"""

    username = StringField("Username", validators=[InputRequired(
        message="Username is required"), Length(max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(message="Password is required")])


class FeedbackForm(FlaskForm):
    """Creates a form for users to add and update feedback"""

    title = StringField("Title", validators=[InputRequired(
        message="Feedback title is required"), Length(max=100)])
    content = StringField("Content", validators=[InputRequired(
        message="Feedback content is required")])
