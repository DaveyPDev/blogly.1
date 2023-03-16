"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """ Homepage """

    return redirect('/users')

@app.route('/users')
def user_id():
    """ User Info"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('/users/userlist.html')

@app.route('/users/new', methods=["GET"])
def new_user_form():
    """ Show new user form """

    return render_template('/users/new.html')

@app.route('/users/new', methods=["POST"])
def new_user():
    """ Submit new user form """

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.sessino.commit()

    return redirect('/users')

@app.route('/users/<int: user_id>')
def users_info(user_id):
    """ show user info """

    user = User.query_get_or_404(user_id)
