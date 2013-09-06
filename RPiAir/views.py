from flask import jsonify, render_template, request
from RPiAir import app
from RPiAir.players.omxplayer import player
from RPiAir.database import database, Movie
from RPiAir.library import library


#  initialize database
database.create_all()


"""
Default
"""
@app.route('/')
def show_player():
    return render_template('player.html', debug=app.config['DEBUG'])


"""
Video commands
"""
@app.route('/video/play/<hash_id>')
def video_play(hash_id):
    return player.video_play(hash_id)

@app.route('/video/exit')
def video_exit():
    return player.video_exit()

@app.route('/video/pause')
def video_pause():
    return player.video_pause()

@app.route('/video/volume/<direction>/<int:amount>')
def video_volume(direction, amount):
    return player.video_volume(direction, amount)

@app.route('/video/position/<direction>/<amount>')
def video_position(direction, amount):
    return player.video_position(direction, amount)


"""
Library commands
"""
@app.route('/library/offset/<int:offset>')
def get_library(offset):
    movies = Movie.query.order_by(Movie.added_on.desc()).slice(offset, 20)
    return jsonify(movies=[m.serialize() for m in movies.all()])

@app.route('/library/search/<qry>')
def search_library(qry):
    movies = Movie.query.filter(database.or_(Movie.title.like('%' + qry + '%'), Movie.location.like('%' + qry + '%'))).order_by(Movie.added_on.desc())
    return jsonify(movies=[m.serialize() for m in movies.all()])

@app.route('/library/rescan')
def rescan_library():
    library.rescan()
    return get_library(0)


""" DEBUG """
@app.route('/thumbs/delete')
def create_thumbs():
    return library.delete_thumbs()
