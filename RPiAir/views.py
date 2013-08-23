from flask import g, render_template, request
from RPiAir import app
from RPiAir.omxplayer import OMXPlayer
from RPiAir.database import database, Movie

#  init player
player = OMXPlayer()

#  initialize database
database.create_all()


#  views
@app.route('/')
def show_player():
    recentMovies = Movie.query.order_by(Movie.added_on.desc()).limit(16).all()
    return render_template('player.html', movies=recentMovies)

@app.route('/play')
def omx_play():
    #  spawn new process and store in cache
    f = request.args.get('filename')
    return player.play_file(f)

@app.route('/run')
def omx_pause():
    cmd = request.args.get('command')
    return player.run_command(cmd)
