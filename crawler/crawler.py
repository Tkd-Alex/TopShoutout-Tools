#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, json
import pandas as pd
from pprint import pprint
from flask import Flask, request, Response

from wordpress import Wordpress
from endpoint import Endpoint

app = Flask(__name__)
wpapi = None
endpoint = None

@app.route('/new', methods=['POST'])
def newInfluencer():
    status, message = endpoint.newInfluencer(request)
    js = json.dumps({ 'result': status, 'message': message})
    return Response(js, status=200, mimetype='application/json')

if __name__ == '__main__':
    if not os.path.exists('image'):
        os.makedirs('image')
    if not os.path.exists('logs'):
        os.makedirs('logs')

    wpapi = Wordpress(
        wp_usr="TopShoutout", wp_psw="TopShoutout123!!", wp_host="http://localhost/topshoutup",
        db_usr="root", db_psw="root", db_host="localhost", db_name="topshoutout"
    )
    endpoint = Endpoint( sqllite="influencer.db", wpapi=wpapi )
    app.run(host='0.0.0.0', port=6565, threaded=True)
