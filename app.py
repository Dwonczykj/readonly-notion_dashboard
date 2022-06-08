from __future__ import annotations, print_function

import json
import logging
import os
from datetime import date
from enum import Enum
from http import HTTPStatus
from typing import Any, TextIO, Tuple

from colorama import Fore, Style
from flask import Flask, jsonify, make_response, render_template, request
from flask.wrappers import Response

from notion import (getRecentPages, notion_request_headers,
                    notion_request_payload)

use_https = False
app = Flask(__name__)

# Flask App Configuration Settings
app.config['GEMBER_HTTPS_KEYFILE'] = '/private/etc/ssl/localhost/localhost.key'
app.config['GEMBER_HTTPS_CERTFILE'] = '/private/etc/ssl/localhost/localhost.crt'
app.config['GEMBER_BIND_HOST'] = '127.0.0.1'
app.config['GEMBER_PORT'] = 8444
app.secret_key = os.urandom(24)

# Flask App Routes
def wrap_CORS_response(response: Response):
    response.headers['Access-Control-Allow-Origin'] = request.origin
    return response

@app.route('/')
def index():
    return wrap_CORS_response(response=Response('flask app connected over http',status=HTTPStatus.OK))


@app.route('/name/<name>')
def indexwName(name:str):
    return wrap_CORS_response(response=Response(f'hi {name}', status=HTTPStatus.OK))


@app.route('/my-notion', methods=['GET','POST'])
def my_notion():
    query = ""
    filter = ""

    # TODO: Turn the below page_names into Tiles in the index.html that contain Title, Image, Properties, Last Editted
    # TODO: Add a search input field that debounce searches notion for the current input string and loads pages (max 10) in the results
    (data, page_names) = getRecentPages(
        payload={
            **notion_request_payload,
            **({
                "query": "",
                } if query else {}),
            **({
                "filter": "",
                } if filter else {}),
            },
        headers=notion_request_headers
        )
    response = wrap_CORS_response(make_response(render_template(
        'index.html', name='Joey', data=data, page_names=page_names)))
    response.headers['X-Notion-Bearer-Token'] = 'parachutes are cool'
    return response
    


# Run the Flask App
HOST = app.config['GEMBER_BIND_HOST']  # or try '0.0.0.0'
PORT = app.config['GEMBER_PORT']

ssl_args = {}
if use_https:
    ssl_args = {
        'keyfile': app.config.get('GEMBER_HTTPS_KEYFILE'),
        'certfile': app.config.get('GEMBER_HTTPS_CERTFILE')
    }

# https://kracekumar.com/post/54437887454/ssl-for-flask-local-development/

httpEchoApplication = app
 
# Link to the original issue with Socket-IO using flutter: https://stackoverflow.com/questions/60348534/connecting-flask-socket-io-server-and-flutter
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger().addHandler(logging.FileHandler('gpAppLog.log'))

if __name__=="__main__":
    app.run(host=HOST, port=PORT,
            **ssl_args
            )
