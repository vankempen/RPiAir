

class Player(object):

    """Docstring for Player. """

    def __init__(self):
       self.currentPlayer = None

    def set_currentPlayer(self, p):
        """set current player obj"""
        self.currentPlayer = p

    def get_currentPlayer(self):
        """return current player object """
        return self.currentPlayer

    #All the next functions have to be implemented
    def video_play(self, filename):
        """start playing a video

        :filename: video file to play (absolute path)
        :returns: player object
        """
        raise NotImplementedError

    def video_exit(self):
        """exit video

        :returns: json message with status
        """
        raise NotImplementedError

    def video_pause(self):
        """toggle pause of video

        :returns: json message with status
        """
        raise NotImplementedError

    def video_volume(self, direction, amount):
        """adjust the volume of current player

        :direction: 'up' or 'down'
        :amount: amount of adjustment
        :returns: json message with status

        """
        raise NotImplementedError

    def video_position(self, direction, amount):
        """ajdust relative playing position of current player

        :direction: 'back' or 'forward'
        :amount: 'small' or 'big'
        :returns: json message with status

        """
        raise NotImplementedError

