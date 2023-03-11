from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model to create user accounts on app."""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    fb = db.relationship('Feedback', backref='user',
                         cascade="all,delete-orphan")

    def __repr__(self):
        """Returns a more specific representation of user instance"""
        u = self
        return f"< User username={u.username} >"

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Registers user with hashed password and returns user. Return user if valid, else - return False."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Authenticates user information on login"""

        u = User.query.filter_by(username=username).first()
        hash = bcrypt.generate_password_hash(password)

        if bcrypt.check_password_hash(hash, password):
            return u
        else:
            return False


class Feedback(db.Model):
    """Feedback model for users' feedback - each assigned to a user."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey(
        'users.username'), nullable=False)

    def __repr__(self):
        """Returns a more specific representation of user instance"""
        f = self
        return f"< User title={f.title} username={f.username}>"
