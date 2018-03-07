#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, _thread, sqlite3, pymysql, query, functions
from pprint import pprint

class Endpoint:
    def __init__(self, sqllite, wpapi):
        self.sqllite = sqllite
        self.wpapi = wpapi
    
    def newInfluencer(self, request):
        status, message = functions.isInstagramValid(request.form['ig_name'])
        if status:
            conn = sqlite3.connect(self.sqllite)
            conn.execute((query.NEW_INFLUENCER % ( 
                int(request.form['post_id']), 
                request.form['ig_name'], 
                request.form['thumbnail_id'], 
                request.form['product_image_gallery']) 
            ))
            conn.commit()
            try:
                _thread.start_new_thread( 
                    functions.fetchInstagramInfo, 
                    ( { 'username': request.form['ig_name'], 'post_id': request.form['post_id'] }, self.wpapi, ) 
                )
            except Exception as e:
                pprint(e)
                functions.writeError(e)
        return status, message