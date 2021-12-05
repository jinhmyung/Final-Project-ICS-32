# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

import json
from collections import namedtuple
import time

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
Response = namedtuple('Response', ['type', 'message', 'messages', 'token'])


class DSProtocalException(Exception):
    """
    error in decoding and encoding between string and json
    """
    pass


def extract_json(json_msg: str) -> Response:
    '''
    Call the json.loads function on a json string and convert it to a Response object

    TODO: replace the pseudo placeholder keys with actual DSP protocol keys
    '''
    try:
        json_obj = json.loads(json_msg)
        type = json_obj['response']['type']
        if type != "ok":
            raise DSProtocalException("request not ok.")

        token, message = None, None
        messages = []
        if 'messages' in json_obj['response'].keys():
            messages = json_obj['response']['messages']
        elif 'message' in json_obj['response'].keys():
            message = json_obj['response']['message']
        if 'token' in json_obj['response'].keys():
            token = json_obj['response']['token']

    except json.JSONDecodeError:
        raise DSProtocalException("Json cannot be decoded.")

    return Response(type, message, messages, token)


def to_json(send_command: str = 'join', usr: str = None, pwd: str = None,
            token: str = '', entry: str = '', timestamp: str = '', recipient: str = None) -> str:
    '''
    convert namedtuple to json message

    :param send_command: one of the command 'join','directmessage','new', or 'all'
    :param usr: username for the join command
    :param pwd: password for the join command
    :param token: user's token received when joining the server
    :param entry: entry for post or bio
    :param timestamp: timestamp for post or bio
    '''
    command_map = {
        "join": {"join": {"username": usr, "password": pwd, "token": token}},
        "directmessage": {"token": token, "directmessage": {"entry": entry, "recipient": recipient, "timestamp": timestamp}},
        "new": {"token": token, "directmessage": "new"},
        "all": {"token": token, "directmessage": "all"}
    }
    try:
        # debug(command_map[send_command])
        return json.dumps(command_map[send_command])
    except KeyError:
        raise DSProtocalException('Not a valid message to be send to the server')

# def #debug(msg):
#     print(msg)