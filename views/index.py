from __init__ import dbconn, ridesdb, ridescoll, clienttrip, keys

from flask import Flask, request, jsonify, abort, Blueprint
import json, time
from pymongo import Connection

index = Blueprint('index', __name__)

@index.route('/', methods = ['GET'])
def display_index():
    ''' Return docs? '''
    if request.method == 'GET':
        return 'Hey there, try JSON!'
    else:
        abort(400)
