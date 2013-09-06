from datetime import datetime
from hashlib import md5
import os
import time

from flask.ext.sqlalchemy import SQLAlchemy
from RPiAir import app


#  database
database = SQLAlchemy(app)


class Movie(database.Model):
    """Docstring for Movie. """

    hash_id = database.Column(database.CHAR(8), primary_key=True)
    location = database.Column(database.String(200))
    title = database.Column(database.String(80))
    thumb = database.Column(database.Boolean())
    added_on = database.Column(database.DateTime, index=True)
    checked_on = database.Column(database.Integer()) #  for rescanning library

    def __init__(self, location, title=None, added_on=None, checked_on=None):
        """
        :location: path to movie
        :title: name of movie
        :added_on: optional date (from epoch) movie is added to the list
        :checked_on: epochtime of last time checked

        """
        self.location = location

        if title is None:
            title = os.path.basename(location)
        self.title = title

        if added_on is None:
            added_on = datetime.utcnow()
        self.added_on = added_on

        if checked_on is None:
            checked_on = int(time.time())
        self.checked_on = checked_on

        self.hash_id = md5(self.location).hexdigest()[:8]
        self.thumb = False

    def __repr__(self):
        return '<Movie %r>' % self.title

    def serialize(self):
        return {
                 'hash_id': self.hash_id,
                 'title': self.title,
                 'thumb': self.thumb,
               }

    def insert_or_update(self):
        """inserts movie if it does not yet exist, else update just_checked flag
        :returns: @todo

        """
        item = self.query.filter_by(hash_id=self.hash_id).first()
        if not item:
            database.session.add(self)
        else:
            item.checked_on = self.checked_on

