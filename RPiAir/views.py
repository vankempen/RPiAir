from flask import render_template, request
from RPiAir import app
from RPiAir.omxplayer import OMXPlayer

#  init Player object
player = OMXPlayer()

#  views
@app.route('/')
def show_player():
    return render_template('player.html')

@app.route('/play')
def omx_play():
    #  spawn new process and store in cache
    f = request.args.get('filename')
    return player.play_file(f)

@app.route('/run')
def omx_pause():
    cmd = request.args.get('command')
    return player.run_command(cmd)

