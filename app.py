"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """ Homepage """

    return redirect('/users')

@app.route('/users')
def user_list():
    """ User Info"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    """ Show new user form """

    return render_template('new.html')

@app.route('/users/new', methods=["POST"])
def new_user():
    """ Submit new user form """

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def users_info(user_id):
    """ show user info """

    user = User.query.get_or_404(user_id)
    return render_template('show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """ shows user editing form """

    user= User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def user_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']  #! How to leave blank but keep default

    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def user_delete(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')