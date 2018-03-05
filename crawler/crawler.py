#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, requests, shutil, random, sqlite3, _thread, pymysql
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from joblib import Parallel, delayed
from ballpark import ballpark

from flask import Flask, request
app = Flask(__name__)

#HOST = "https://topshoutout.com"
HOST = "http://localhost/topshoutup"
conn = None
token = None

@app.route('/new', methods=['POST'])
def newProduct():
    query = ("INSERT INTO influencers (POST_ID, IG_NAME, THUMB_ID, GALLERY_IDS) "
            "VALUES (%d, '%s', '%s', '%s' )" % ( int(request.form['post_id']), request.form['ig_name'], request.form['thumbnail_id'], request.form['product_image_gallery']) )
    conn.execute(query)
    conn.commit()
    try:
        _thread.start_new_thread( fetchUserInfo, ('{},{}'.format(int(request.form['post_id']), request.form['ig_name']), ) )
    except Exception as error:
        print ("Error: unable to start thread")
        print(error)
    return "True"

def login(username, password):
	# Using: https://it.wordpress.org/plugins/jwt-authentication-for-wp-rest-api/
	print("Login with: {}".format(username))
	# Get JWT-Token
	res = requests.post(url = "{}/wp-json/jwt-auth/v1/token".format(HOST),
						data = { 'username': username, 'password': password})

	token = res.json()['token']
	return token

def uploadImage(image):
    data = open('image/{}'.format(image), 'rb').read()
    fileName = os.path.basename('image/{}'.format(image))
    print("Uploading: {}".format(image))
    res = requests.post(url = '{}/wp-json/wp/v2/media'.format(HOST),
                        data = data,
                        headers = {
                            'Authorization':"Bearer " + token,
                            'Content-Type': 'image/jpg',
                            'Content-Disposition' : 'attachment; filename=%s'% fileName
                        })
    return res.json()['id']

def updateUserWP(user, imageids, nfollower, averangelikes):
    post_id = user.split(',')[0]
    #cnx = pymysql.connect(user='topshout_import', password='passwordIMPORTER#2018', host='topshoutout.com', database='topshout_wp217')
    cnx = pymysql.connect(user='root', password='root', host='localhost', database='topshoutout')
    cursor = cnx.cursor()

    query = ("UPDATE wppt_postmeta "
            "SET meta_value = '%s' "
            "WHERE meta_key = '_thumbnail_id' AND post_id = '%s' " % (imageids[0], post_id) ) 
    cursor.execute(query)

    query = ("UPDATE wppt_postmeta "
            "SET meta_value = '%s' "
            "WHERE meta_key = '_product_image_gallery' AND post_id = '%s' " % (','.join([str(x) for x in imageids[-4:]]), post_id) ) 
    cursor.execute(query)

    post_excerpt = '<div>{} Followers</div><div>{}% Engagement Rate</div>'.format(ballpark(nfollower),  str(round(float( averangelikes / int(nfollower) ) * 100, 2)) )
    today = datetime.now().date()
    query = ("UPDATE wppt_posts "
            "SET post_excerpt = '%s', post_modified = '%s', post_modified_gmt = '%s', post_status='publish' "
            "WHERE ID = '%s' " % (post_excerpt, today, today, post_id) ) 
    cursor.execute(query)

    cnx.commit()

def downloadImage(imgurl, filename):
    if not os.path.exists('image'):
        os.makedirs('image')
    try:
        response = requests.get(imgurl, stream=True)
        if response.status_code == 200:
            with open('image/{}'.format(filename), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
                return filename
        else:
            print("Cannot download image, response status: {}".format(response.status_code))
    except Exception as error:
        print("Error with media")
        with open('urlerror.txt', 'a') as errfile:
            errfile.write("{}\n".format(imgurl))
            print(error)

def fetchUserInfo(user):
    username = user.split(',')[1].strip().replace('@','')
    url = "https://www.instagram.com/{}/?__a=1".format(username)
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        try: 
            json = res.json()
            with open('lastjson.json', 'w') as lastjson:
                lastjson.write(str(json))
            json = json['user']
            print("Username: {}".format(json['username'].encode('utf-8')))
            if json['is_private'] == False:
                nfollower = json['followed_by']['count']
                print("Follower count: {}".format(nfollower))
                imgurls = []
                sumlikes = 0
                for media in json['media']['nodes'][:12]:
                    sumlikes += int(media['likes']['count'])
                averangelikes = float(int(sumlikes) / 12)
                for media in json['media']['nodes'][:5]:
                    url = media['thumbnail_src']
                    filename = '{}{}{}'.format(media['id'][:5], random.randint(1, 99), url[-10:])
                    imgurls.append(downloadImage(url, filename))
                imgids = Parallel(n_jobs=3, backend="threading")(delayed(uploadImage)(imgurl) for imgurl in imgurls)
                updateUserWP(user, imgids, nfollower, averangelikes)
            else:
                print("Private page")
                with open('privatepage.txt', 'a') as privatefile:
                    privatefile.write("{}\n".format(url))
        except Exception as error:
            print("Error with url: {}".format(url))
            with open('urlerror.txt', 'a') as errfile:
                errfile.write("{}\n".format(url))
            print(error)
    else:
        print("Request error, response status: {}".format(res.status_code))

if __name__ == '__main__':
    conn = sqlite3.connect('influencer.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS influencers
         (
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            POST_ID INTEGER UNIQUE NOT NULL,
            IG_NAME CHAR(255) NOT NULL,
            THUMB_ID CHAR(50),
            GALLERY_IDS CHAR(50)
        );''')

    token = login('TopShoutout', 'TopShoutout123!!')
    app.run(host='0.0.0.0', port=6565, threaded=True)
    
    '''
    with open("../importer/idusername.txt") as f:
        usernames = f.readlines()
    for user in usernames:
        fetchUserInfo(user)
        print("-------------------")
    '''
