from datetime import datetime
from hashlib import md5

from flask.ext.sqlalchemy import SQLAlchemy
from RPiAir import app


#  database
database = SQLAlchemy(app)

class Movie(database.Model):
    """Docstring for Movie. """

    hash_id = database.Column(database.Binary(8), primary_key=True)
    location = database.Column(database.String(200))
    title = database.Column(database.String(80))
    added_on = database.Column(database.DateTime, index=True)
    thumb = database.Column(database.String(), nullable=True)

    def __init__(self, location, title, added_on=None, thumb=None):
        """@todo: to be defined1.

        :location: path to movie
        :title: name of movie
        :added_on: optional date (from epoch) movie is added to the list
        :thumb: location of thumbnail

        """

        self.location = location
        self.title = title
        if added_on is None:
            added_on = datetime.utcnow()
        self.added_on = added_on
        if thumb is None:
            pass #  @TODO implement thumbnail creator
        self.thumb = thumb
        self.hash_id = md5(self.location).digest()[:8]

    def __repr__(self):
        return '<Movie %r>' % self.title
