"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):
    """ User """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text(30), nullable = False)
    last_name = db.Column(db.text(30), nullable = False)
    image_url = db.Column(db.text, nullable = False, default= DEFAULT_IMAGE_URL)

    @classmethod
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"
    
    def connect_db(app):
        """ Connect to Database """

        db.app = app
        db.init_app(app)