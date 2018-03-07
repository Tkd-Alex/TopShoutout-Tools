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
            curs = conn.cursor()
            curs.execute((query.NEW_INFLUENCER % ( 
                int(request.form['post_id']), 
                request.form['ig_name'], 
                request.form['thumbnail_id'], 
                request.form['product_image_gallery']) 
            ))
            curs.commit()
            try:
                _thread.start_new_thread( 
                    functions.fetchInstagramInfo, 
                    ( { 'username': request.form['ig_name'], 'post_id': request.form['post_id'] }, self.wpapi, ) 
                )
            except Exception as e:
                functions.writeError(e)
        return status, message

    def updateInfluencer(self, request):
        conn = sqlite3.connect(self.sqllite)
        curs = conn.cursor()
        curs.execute((query.GET_IGNAME % (int(request.form['post_id'])) ))
        igname = curs.fetchone
        # This post_id not exist in out db. simulate such as new influencer.
        if igname == None:
            self.newInfluencer(request)
        else:
            if igname == request.form['ig_name']:
                curs.execute((query.UPDATE_INFLUENCER % ( 
                    int(request.form['post_id']), 
                    request.form['ig_name'], 
                    request.form['thumbnail_id'], 
                    request.form['product_image_gallery']) 
                ))
            else:
                status, message = functions.isInstagramValid(request.form['ig_name'])
                if status:
                    curs.execute((query.UPDATE_INFLUENCER % ( 
                        int(request.form['post_id']), 
                        request.form['ig_name'], 
                        request.form['thumbnail_id'], 
                        request.form['product_image_gallery']) 
                    ))
                else:
                    return status, message
            curs.commit()
            return True, "Influencer has been updated"

    def deleteInfluencer(self, request):
        conn = sqlite3.connect(self.sqllite)
        curs = conn.cursor()
        curs.execute((query.GET_IGNAME % (int(request.form['post_id'])) ))
        igname = curs.fetchone
        if igname != None:
            curs.execute((query.DELETE_INFLUENCER % (int(request.form['post_id'])) ))
            curs.commit()
