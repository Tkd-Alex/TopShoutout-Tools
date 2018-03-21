#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, glob, requests, shutil, pymysql, query, functions, subprocess
from pprint import pprint
from slugify import slugify
from datetime import date, datetime, timedelta

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
        os.remove('image/{}'.format(image))
        return res.json()['id']

    def getInstagramPage(self):
        cnx = pymysql.connect(
            user=self.dbconfig['user'], password=self.dbconfig['password'], 
            host=self.dbconfig['host'], database=self.dbconfig['database']
        )
        cursor = cnx.cursor()
        cursor.execute(( query.GET_INSTAGRAM_PAGE ))
        ig_pages = cursor.fetchall()
        return ig_pages

    def getImageAlreadyUpload(self, post_id):
        cnx = pymysql.connect(
            user=self.dbconfig['user'], password=self.dbconfig['password'], 
            host=self.dbconfig['host'], database=self.dbconfig['database']
        )
        cursor = cnx.cursor()
        
        cursor.execute((query.GET_IMAGE_ID % (post_id) ))
        image_ids = cursor.fetchall()
        ids = []
        for img in image_ids:
            if ',' in img[0] and img[0] != '':
                ids += img[0].split(',')
            elif img[0] != '':
                ids.append(img[0])
        
        titles = []
        if len(ids) > 0:
            cursor.execute( (query.GET_IMAGE_TITLE % (','.join([str(x) for x in ids])) ) )
            image_titles = cursor.fetchall()
            for title in image_titles:
                titles.append(title[1]) 

        return titles

    def updateUserWP(self, post_id, imageids, nfollower, averangelikes):
        cnx = pymysql.connect(
            user=self.dbconfig['user'], password=self.dbconfig['password'], 
            host=self.dbconfig['host'], database=self.dbconfig['database']
        )
        cursor = cnx.cursor()
        
        data = {}

        # Get all image alredy setted
        cursor.execute((query.GET_IMAGE_ID % (post_id) ))
        image_ids = cursor.fetchall()

        saved_ids = []

        for img in image_ids:
            if img[0] != '':
                cursor.execute((query.GET_IMAGE_TITLE % (img[0]) ))
                if img[1] == '_thumbnail_id': # If the image is thumbnail
                    image_title = cursor.fetchone()
                    if image_title != None: # Exist
                        if 'MEDIA_BOT' in image_title[1]: # Is upload by bot can be update.
                            #cursor.execute((query.UPDATE_THUMBNAIL % (imageids[0], post_id) ))
                            data['_thumbnail_id'] = imageids[0];
                else: # Image is in gallery
                    image_titles = cursor.fetchall()
                    for img_title in image_titles:
                        if not 'MEDIA_BOT' in img_title[1]:
                            saved_ids.append(img_title[0])
            else:
                #cursor.execute((query.UPDATE_THUMBNAIL % (imageids[0], post_id) ))
                data['_thumbnail_id'] = imageids[0];
        
        if len(saved_ids) < 4: # If saved ids are less that four concat this id with our uploaded
            imageids = saved_ids + imageids[ : ( 4-len(saved_ids )) ]
        
        img_ids = ','.join([str(x) for x in imageids])
        #cursor.execute((query.UPDATE_IMG_GALLERY % (img_ids, post_id) ))
        #cursor.execute((query.UPDATE_FOLLOWER % (nfollower, post_id) ))

        engagementrate = str(round(float( averangelikes / int(nfollower) ) * 100, 2)) 
        #cursor.execute((query.UPDATE_ENGAGEMENT_RATE % (engagementrate, post_id) ))
        
        data['post_id'] = post_id
        data['ct_Followers_text_2365'] = nfollower
        data['ct_Engagement_text_2863'] = engagementrate
        data['_product_image_gallery'] = img_ids
        
        cursor.execute((query.GET_POST_TITLE) % post_id)
        post_title = cursor.fetchone()
        if post_title != None:
            post_name = slugify(str(post_title))
        else: 
            post_name = ""

        guid = '{}/product/{}'.format(self.wpconfig['host'], post_name)

        cursor.execute((query.UPDATE_POST_INFO % ({'guid': guid, 'post_name': post_name, 'post_id': post_id}) ))
        cnx.commit()
        
        r = requests.post(self.wpconfig['host'] + "/crawler_update.php", data=data)
        print("[{}] Finish".format(post_id))
        