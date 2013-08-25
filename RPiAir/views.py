from flask import render_template, request
from RPiAir import app
from RPiAir.omxplayer import player
from RPiAir.database import database, Movie
from RPiAir.library import library


#  initialize database
database.create_all()

def get_urlData(r):
    """retuns dict with parsed data from url """
    return eval(r.args.get('data'))

#  views
@app.route('/')
def show_player():
    recentMovies = Movie.query.order_by(Movie.added_on.desc()).limit(20).all()
    return render_template('player.html', movies=recentMovies, debug=app.config['DEBUG'])

@app.route('/play')
def omx_play():
    #  spawn new process and store in cache
    filename = get_urlData(request)['f']
    return player.play_file(filename)

@app.route('/run')
def omx_run():
    cmd = get_urlData(request)['cmd']
    return player.run_command(cmd)

@app.route('/rescan')
def rescan_library():
    return library.rescan()

@app.route('/thumbs')
def create_thumbs():
    return library.delete_thumbs()
