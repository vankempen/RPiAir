from flask import jsonify

statusCodes = {
        ##success
        200: 'success',
        #player success
        210: 'success: started playing video "{0}"',
        211: 'success: exited current video',
        212: 'Success: toggled pause on current video',
        213: 'success: adjusted volume of current video',
        214: 'success: adjusted position of current video',

        ##client errors
        400: 'client error',
        403: 'client error: hash_id "{0}" not found in database',
        404: 'client error: file "{0}" not found',
        405: 'client error: command "{0}" to allowed',
        406: 'client error: no current player running',

        ##server errors
        500: 'server error',
        501: 'server error: function "{0}" not implemented',
        #player errors
        511: 'server error: player command not set',
        512: 'server error: player command "{0}" not found',
        513: 'server error: player exited immediately',
        #library errors
        521: 'server error: no library set',
}

def create_jsonMessage(s=200, args=None):
    """return a json object with message and status

    :s: statuscode of message"""
    try:
        return jsonify(message=(statusCodes[s].format(args)), status=s)
    except IndexError:
        print "Not enough args supplied for status code {0}!".format(s)
        raise IndexError

