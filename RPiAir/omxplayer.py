import pexpect
import time
from flask import jsonify


class OMXPlayer():
    #
    CMD  = "/usr/bin/omxplayer.bin"
    ARGS = "-o hdmi -b"
    KEYS = {
            'decrSpeed': '1',
            'incrSpeed': '2',
            'rewind': '<',
            'fastForward': '>',
            'showInfo': 'z',
            'prevAudio': 'j',
            'nextAudio': 'k',
            'prevChapter': 'i',
            'nextChapter': 'o',
            'prevSubtitle': 'n',
            'nextSubtitle': 'm',
            'toggleSubtitle': 's',
            'decrSubtitleDelay': 'd',
            'incrSubtitleDelay': 'f',
            'exit': 'q',
            'togglePlay': 'p',
            'decrVolume': '-',
            'incrVolume': '+',
            'seek-30':'\x1b\x5b\x44',
            'seek+30':'\x1b\x5b\x43',
            'seek-600':'\x1b\x5b\x42',
            'seek+600':'\x1b\x5b\x41',
    }

    def __init__(self):
        self.currentPlayer = None

    def set_currentPlayer(self, omx):
        #  set current player obj
        self.currentPlayer = omx
        return 1

    def get_currentPlayer(self):
        #  return current player obj if still running
        if self.currentPlayer:
            if not self.currentPlayer.isalive():
                self.currentPlayer = None
        return self.currentPlayer

    def json_message(self, msg):
        #return jsonified message
        return jsonify(message=msg)

    def run_command(self, cmd):
        # run command on player obj
        player = self.get_currentPlayer()
        if not player:
            return self.json_message("No instance of omxplayer running!")
        player.send(OMXPlayer.KEYS[cmd])
        return self.json_message("Successfully executed Command '%s'!" % cmd)

    def play_file(self, filename):
        #  start omxplayer and play file
        player = self.get_currentPlayer() #  first check if not already playing
        if player:
            _ = self.run_command('exit')
        new_player = pexpect.spawn(' '.join([OMXPlayer.CMD, OMXPlayer.ARGS, filename]))

        time.sleep(0.5) #  make sure omxplayer not immediately exits
        if new_player.isalive():
            self.set_currentPlayer(new_player)
            return self.json_message("Successfully started playing file '%s'!" % filename)
        else:
            return self.json_message("Failed to play file '%s'!'")


#  initialize player
player = OMXPlayer()
