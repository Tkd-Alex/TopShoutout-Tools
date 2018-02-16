#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, requests, shutil, random
import pandas as pd
import mysql.connector
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta

usernames = []
df = pd.read_excel('Influencer DB_20171109.xlsx')

for i in df.index:
    usernames.append( str(df['Profile name'][i]).strip().replace('@','') )

if not os.path.exists('image'):
    os.makedirs('image')

for user in usernames:
    url = "https://www.instagram.com/{}/?__a=1".format(user)
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        json = res.json()['user']
        # If user is private media array is empty
        print("Username: {}, Fullname: {}".format(json['username'].encode('utf-8'), json['full_name'].encode('utf-8')))
        print("Follower count: {}".format(json['followed_by']['count']))
        for media in json['media']['nodes']:
            imgurl = media['thumbnail_src']
            filename = '{}{}{}'.format(media['id'][:5], random.randint(1, 99), imgurl[-10:])
            response = requests.get(imgurl, stream=True)
            if response.status_code == 200:
                with open('image/{}'.format(filename), 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
            else:
                print("Cannot download image, response status: {}".format(response.status_code))
    else:
        print("Request errore, response status: {}".format(res.status_code))
