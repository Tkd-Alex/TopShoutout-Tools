#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, requests, shutil, random
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from joblib import Parallel, delayed

def writeError(error):
    with open('logs/error.log', 'a') as _file:
        _file.write("{}\n".format(error))

def downloadImage(imgurl, filename):
    #try:
    response = requests.get(imgurl, stream=True)
    if response.status_code == 200:
        with open('image/{}'.format(filename), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            return filename
    else:
        writeError("Cannot download image, response status: {}\nUrl image: {}".format(response.status_code, imgurl))
    #except Exception as e:
    #    writeError(e)

def isInstagramValid(username):
    url = "https://www.instagram.com/{}/?__a=1".format(username.strip().replace('@',''))
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        try:
            json = res.json()['user']
            if json['is_private'] == True:
                return False, "The {} page it does not seem to be public.".format(username)
        except Exception as error:
            writeError(error)  
            return False, "Unable to check {} page.".format(username)
    elif res.status_code == 404:
        return False, "The {} page it does not seem to exist.".format(username)
    else:
        return False, "Unable to check {} page.".format(username)
    return True, "Your page has been inserted and is under review."

def fetchInstagramInfo(user, wpapi):
    username = user['username'].strip().replace('@','')
    post_id = user['post_id'].strip()
    
    url = "https://www.instagram.com/{}/?__a=1".format(username)
    res = requests.get(url, stream=True)
    
    if res.status_code == 200:
        #try: 
        json = res.json()['user']
        if json['is_private'] == False:
            nfollower = json['followed_by']['count']
            imgurls = []
            
            sumlikes = 0
            for media in json['media']['nodes'][:12]:
                sumlikes += int(media['likes']['count'])
            
            averangelikes = float(int(sumlikes) / 12)
            
            for media in json['media']['nodes'][:5]:
                url = media['thumbnail_src']
                filename = 'MEDIA_BOT_{}.jpg'.format(media['id'])
                imgurls.append(downloadImage(url, filename))
            
            imgids = Parallel(n_jobs=3, backend="threading")(delayed(wpapi.uploadImage)(imgurl) for imgurl in imgurls)
            wpapi.updateUserWP(post_id, imgids, nfollower, averangelikes)
        else:
            with open('privatepage.txt', 'a') as privatefile:
                privatefile.write("{}\n".format(url))
        #except Exception as e:
        #    writeError(e)
    else:
        writeError("Request error, response status: {}\nUrl: {}".format(res.status_code, url))
