#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, glob, requests, shutil, pymysql, query
from pprint import pprint
from datetime import date, datetime, timedelta
from ballpark import ballpark

class Wordpress:
    def __init__(self, wp_usr, wp_psw, wp_host, db_usr, db_psw, db_host, db_name):
        self.token = ''
        self.wpconfig = {
            'username': wp_usr,
            'password': wp_psw,
            'host': wp_host
        }
        self.dbconfig = {
            'user': db_usr,
            'password': db_psw,
            'host': db_host,
            'database': db_name
        }
        self.login()

    def login(self):
        res = requests.post(url = "{}/wp-json/jwt-auth/v1/token".format(self.wpconfig['host']),
                            data = { 
                                'username': self.wpconfig['username'], 
                                'password': self.wpconfig['password']
                                }
                            )

        self.token = res.json()['token']

    def uploadImage(self, image):
        data = open('image/{}'.format(image), 'rb').read()
        filename = os.path.basename('image/{}'.format(image))
        res = requests.post(url = '{}/wp-json/wp/v2/media'.format(self.wpconfig['host']),
                            data = data,
                            headers = {
                                'Authorization':"Bearer " + self.token,
                                'Content-Type': 'image/jpg',
                                'Content-Disposition' : 'attachment; filename=%s'% filename
                            })
        return res.json()['id']

    def updateUserWP(self, post_id, imageids, nfollower, averangelikes):
        cnx = pymysql.connect(
            user=self.dbconfig['user'], password=self.dbconfig['password'], 
            host=self.dbconfig['host'], database=self.dbconfig['database']
        )
        cursor = cnx.cursor()

        cursor.execute((query.UPDATE_THUMBNAIL % (imageids[0], post_id) ))

        imageids = ','.join([str(x) for x in imageids[-4:]])
        cursor.execute((query.UPDATE_IMG_GALLERY % (imageids, post_id) ))

        '''
        cursor.execute((query.UPDATE_FOLLOWER % (nfollower, post_id) ))

        engagementrate = str(round(float( averangelikes / int(nfollower) ) * 100, 2)) 
        cursor.execute((query.UPDATE_ENGAGEMENT_RATE % (engagementrate, post_id) ))
        '''
        '''
        post_excerpt = '<div>{} Followers</div><div>{}% Engagement Rate</div>'.format(ballpark(nfollower),  str(round(float( averangelikes / int(nfollower) ) * 100, 2)) )
        today = datetime.now().date()
        query = ("UPDATE wppt_posts "
                "SET post_excerpt = '%s', post_modified = '%s', post_modified_gmt = '%s', post_status='publish' "
                "WHERE ID = '%s' " % (post_excerpt, today, today, post_id) ) 
        cursor.execute(query)
        '''
        
        cnx.commit()