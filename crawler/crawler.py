#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, json, configparser, query, sqlite3
import pandas as pd
from pprint import pprint
from flask import Flask, request, Response
from datetime import datetime
from wordpress import Wordpress
from endpoint import Endpoint

app = Flask(__name__)
wpapi = None
endpoint = None

@app.route('/new', methods=['POST'])
def newInfluencer():
    status, message = endpoint.newInfluencer(request)
    js = json.dumps({ 'result': status, 'message': message })
    return Response(js, status=200, mimetype='application/json')

@app.route('/',  methods=['GET', 'POST'])
def hello():
    message = "TopShoutout-Api Working on: {}".format(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    return Response(message, status=200, mimetype='application/json')

if __name__ == '__main__':
    if not os.path.exists('image'):
        os.makedirs('image')
    if not os.path.exists('logs'):
        os.makedirs('logs')

    config = configparser.ConfigParser()
    config.read('config.ini')

    conn = sqlite3.connect("influencer.db")
    conn.execute(query.INIT_TABLE)

    wpapi = Wordpress(
        wp_usr=config.get('wordpress','username'), wp_psw=config.get('wordpress','password'), wp_host=config.get('wordpress','host'),
        db_usr=config.get('database','username'), db_psw=config.get('database','password'), db_host=config.get('database','host'), db_name=config.get('database','name')
    )
    endpoint = Endpoint( sqllite="influencer.db", wpapi=wpapi )
    app.run(host='0.0.0.0', port=6565, threaded=True)
    