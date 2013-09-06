import os
import pexpect
import time

from player import Player
from RPiAir.database import Movie
from RPiAir.messaging import create_jsonMessage


class OMXPlayer(Player):
    """class for control OMXPlayer instance (RPi)"""

    CMD  = "/usr/bin/omxplayer.bin"
    ARGS = "-o hdmi -b".split(' ')
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

    def run_command(self, cmd, s):
        """run command on player object

        :cmd: command to run (from OMXPlayer.KEYS
        :s: statuscode
        """
        player = self.get_currentPlayer()
        if not player:
            return create_jsonMessage(406)
        player.send(OMXPlayer.KEYS[cmd])

        return create_jsonMessage(s)

    def get_currentPlayer(self):
        """return current player object if still running"""
        curPlayer = super(OMXPlayer, self).get_currentPlayer()
        if curPlayer is not None:
            if not curPlayer.isalive():
                self.set_currentPlayer(None)
        return super(OMXPlayer, self).get_currentPlayer()

    def video_play(self, hash_id):
        """start omxplayer and play file"""
        #  get video filename
        item = Movie.query.filter_by(hash_id=hash_id).first()
        if not item:
            return create_jsonMessage(403, hash_id)
        filename = item.location

        #  check if videofile exists
        if not os.path.isfile(filename):
            return create_jsonMessage(404, filename)

        #  check if not already playing and exit if so
        curPlayer = self.get_currentPlayer()
        if curPlayer is not None:
            _ = self.exit_video()

        #  start playing video
        try:
            newPlayer = pexpect.spawn(OMXPlayer.CMD, OMXPlayer.ARGS + [filename])
        except pexpect.ExceptionPexpect:
            return create_jsonMessage(512, OMXPlayer.CMD)

        time.sleep(0.5) #  make sure omxplayer not immediately exits
        if not newPlayer.isalive():
            return create_jsonMessage(513)
        self.set_currentPlayer(newPlayer)
        return create_jsonMessage(210, filename)

    def video_exit(self):
        """exit current video"""
        return self.run_command('exit', 211)

    def video_pause(self):
        """pause current video"""
        return self.run_command('pause', 212)

    def video_volume(self, direction='up', amount=1):
        """adjust the volume of current player"""
        cmd = 'incrVolume' if direction == 'up' else 'decrVolume'

        for i in range(amount):
            msg = self.run_command(cmd, 213)
        return msg

    def video_position(self, direction='forward', amount='small'):
        """adjust the position of the player by amount in direction"""
        direction = '+' if direction == 'forward' else '-'
        amount = '30' if amount == 'small' else '600'

        return self.run_command('seek' + direction + amount, 214)



#  initialize player
player = OMXPlayer()
