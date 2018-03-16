#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, _thread, functions
from pprint import pprint

class Endpoint:
    def __init__(self, wpapi):
        self.wpapi = wpapi
    
    def newInfluencer(self, request):
        status, message = functions.isInstagramValid(request.form['ig_name'])
        if status:
            try:
                _thread.start_new_thread( 
                    functions.fetchInstagramInfo, 
                    ( { 'username': request.form['ig_name'], 'post_id': request.form['post_id'] }, self.wpapi, ) 
                )
            except Exception as e:
                functions.writeError(e)
        return status, message