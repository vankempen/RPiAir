import os
import time

from RPiAir import app
from RPiAir.database import database, Movie


class Library(object):
    """Docstring for Library. """

    #  Supported movie extensions for OMXPlayer
    movieExtensions = ['.mp4', '.avi', '.mkv', '.mov', '.mpg', '.flv', '.m4v']

    def __init__(self, root):
        """@todo: to be defined1. """
        self.root = root

    def movies_in_path(self, path=None, exts=None):
        """finds all movies recursively in path with extensions listed in exts

        :path: path to recursively search for movies
        :exts: allowed extensions of movie files

        :yields absolute path to movie with filename

        """
        if path is None:
            path = self.root

        if exts is None:
            exts = Library.movieExtensions

        for dirpath, _, files in os.walk(path):
            for f in files:
                lower_f = f.lower()
                for ext in exts:
                    if lower_f.endswith(ext):
                        yield dirpath, f
                        continue

    def rescan(self):
        """rescans root recursively, adds movies to db and removes non existing ones from db

        :returns: if completed

        """
        #  insert new files and update checked_on of old ones
        timestamp = int(time.time())
        for dname, fname in self.movies_in_path():
            m = Movie(location=os.path.join(dname, fname), title=fname, checked_on=timestamp)
            m.insert_or_update()
        database.session.commit()

        #  remove obselete items from database
        Movie.query.filter(Movie.checked_on != timestamp).delete()
        database.session.commit()

        return 'Rescanned'





#  initialize library
library = Library(app.config['LIBRARY_DIR'])
