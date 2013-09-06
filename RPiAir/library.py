from hashlib import md5
import os
import subprocess
import time

from flask import jsonify, url_for
from RPiAir import app
from RPiAir.database import database, Movie


#  Supported movie extensions for OMXPlayer
MOVIE_EXTS = ['.mp4', '.avi', '.mkv', '.mov', '.mpg', '.flv', '.m4v']

THUMB_DIR = './RPiAir/static/thumbs/' #  directory for thumbnails
THUMB_EXT = '.jpg' #  image extension for thumbnails

#  program used for making thumbnails
THUMB_BIN = '/usr/bin/ffmpegthumbnailer'
THUMB_ARGS = '-q 90 -t 30% -s 256'.split(' ')

#  command to generate thumbnails (inputfile still has to be added
def get_thumb_cmd(ifile, ofile):
    """returns command to generate thumbnails as list

    :ifile: inputfile
    :ofile: outputfile
    :returns: list with command and args to use in subprocess.Popen

    """
    cmd = [THUMB_BIN] + THUMB_ARGS
    cmd += ['-i', ifile, '-o', ofile]
    return cmd


class Library(object):
    """Handler for movie library"""

    def __init__(self, root):
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
            exts = MOVIE_EXTS

        for dirpath, _, files in os.walk(path):
            for f in files:
                lower_f = f.lower()
                for ext in exts:
                    if lower_f.endswith(ext):
                        yield dirpath, f
                        continue

    def rescan(self, thumbs=True):
        """rescans root recursively, adds movies to db and removes non existing ones from db

        :thumbs: also generate thumbnails
        :returns: if completed

        """
        #  insert new files and update checked_on of old ones
        timestamp = int(time.time())
        for dname, fname in self.movies_in_path():
            m = Movie(location=os.path.join(dname, fname), title=fname, checked_on=timestamp)
            m.insert_or_update()
        database.session.commit()

        #  remove obselete items from database
        for m in Movie.query.filter(Movie.checked_on != timestamp).all():
            if m.thumb is not False:
                thumb = os.path.join(THUMB_DIR, m.hash_id + THUMB_EXT)
                if os.path.isfile(thumb):
                    os.remove(thumb)
            database.session.delete(m)
        database.session.commit()

        if thumbs:
            _ = self.create_thumbs()

        return jsonify(message='Rescanned')

    def create_thumbs(self):
        """Selects rows from database where no thumbnail is available and creates one in the thumbs directory

        :returns: @todo

        """
        for m in Movie.query.filter(Movie.thumb == False).all():
            tname = m.hash_id + THUMB_EXT
            tname_full = os.path.join(THUMB_DIR, tname)
            p = subprocess.Popen(get_thumb_cmd(m.location, tname_full), \
                                 stdout=subprocess.PIPE).communicate()
            if os.path.isfile(tname_full):
                if os.path.getsize(tname_full) > 10000:
                    m.thumb = True
                else:
                    os.remove(tname_full)
        database.session.commit()
        return 'Created thumbnails'

    def delete_thumbs(self):
        """ for debugging """
        for m in Movie.query.all():
            if m.thumb is True:
                thumb = os.path.join(THUMB_DIR, m.thumb)
                if os.path.isfile(thumb):
                    os.remove(thumb)
            m.thumb = False
        database.session.commit()
        return "Consider it done"


#  initialize library
library = Library(app.config['LIBRARY_DIR'])
