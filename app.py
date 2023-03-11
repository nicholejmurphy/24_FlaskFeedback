from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'some_value'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.debug = True

app.app_context().push()

connect_db(app)


@app.route('/')
def main_page():
    """Shows home page"""

    feedback = Feedback.query.all()

    return render_template('base.html', feedback=feedback)


@app.route('/register', methods=["GET", "POST"])
def register():
    """Render register form and handles register submission."""
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password,
                             email=email, first_name=first_name, last_name=last_name)

        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username is not available.')
            return render_template('register.html', form=form)

        session['user_id'] = user.username

        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Renders a login form and handles login."""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username=username, password=password)

        if user:
            session['user_id'] = user.username

            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid login information."]

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def secret(username):
    """Renders a secret page only for logged in users"""

    if 'user_id' not in session:
        flash("You must be logged in to view!")
        redirect('/login')

    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.filter_by(username=user.username).all()

    return render_template("user.html", user=user, feedback=feedback)


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """Renders a secret page only for logged in users"""

    if 'user_id' not in session:
        flash("You must be logged in to continue!")
        redirect('/login')

    user = User.query.filter_by(username=username).first()

    session.pop('user_id')

    db.session.delete(user)
    db.session.commit()

    return redirect("/")


@app.route('/logout')
def logout():
    """Removes user from session and logs them out."""

    session.pop('user_id')

    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """Renders a create feedback form and handles submitted feedback."""

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect('/')

    return render_template('feedback_add.html', form=form)


@app.route('/feedback/<feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Renders form to update feedback but associated user."""

    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect('/')

    return render_template('feedback_update.html', form=form)


@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """Renders form to update feedback but associated user."""

    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()

    return redirect('/')
