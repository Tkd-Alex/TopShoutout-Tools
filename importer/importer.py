#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, requests
import pandas as pd
import mysql.connector
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta

HOST = "http://localhost/wordpress"
USER_TABLE = "wp_users"
USER_META_TABLE = "wp_usermeta"

def uploadImage(username, password, imagePath):
	print("Login with: {}".format(username))
	# Get JWT-Token
	res = requests.post(url = "{}/wp-json/jwt-auth/v1/token".format(HOST),
						data = { 'username': username, 'password': password})

	token = res.json()['token']
	print("Login complete, token: {}".format(token))
	data = open(imagePath, 'rb').read()
	fileName = os.path.basename(imagePath)
	res = requests.post(url = '{}/wp-json/wp/v2/media'.format(HOST),
						data = data,
						headers = {
							'Authorization':"Bearer " + token,
							'Content-Type': 'image/jpg',
							'Content-Disposition' : 'attachment; filename=%s'% fileName
					})
	return res.json()['id']

def createUser(cnx, value):
	query = ("INSERT INTO " + USER_TABLE +
			 "(user_login, user_pass, user_nicename, user_email, display_name, user_registered)"
			 "VALUES (%(user_login)s, md5(%(user_pass)s), %(user_nicename)s, %(user_email)s, %(display_name)s, %(user_registered)s)")
	cursor = cnx.cursor()
	cursor.execute(query, value)
	cnx.commit()
	return cursor.lastrowid

def updateMetaUser(cnx, userid, nickname):
	query = ("INSERT INTO wp_usermeta"
			 "(user_id, meta_key, meta_value)"
			 "VALUES (%(user_id)s, %(meta_key)s, %(meta_value)s)")
	value = {
		'first_name': '',
		'last_name': '',
		'description': '',
		'rich_editing': 'true',
		'syntax_highlighting': 'true',
		'comment_shortcuts': 'false',
		'admin_color': 'fresh',
		'use_ssl': '0',
		'show_admin_bar_front': 'true',
		'locale': '',
		'wppt_capabilities': 'a:1:{s:10:\"influencer\";b:1;}',
		'wppt_user_level': '0'
	}
	cursor = cnx.cursor()
	cursor.execute(query, {
		'user_id': userid,
		'meta_key': 'nickname',
		'meta_value': nickname
	})
	cnx.commit()

	for i in value:
		cursor.execute(query, {
			'user_id': userid,
			'meta_key': i,
			'meta_value': value[i]
		})
		cnx.commit()

	cursor.close()

xlsfiles = []
index = 0
filelist = ""

for file in os.listdir('xls'):
	xlsfiles.append(file) 
	filelist += "[{}] File: {}\n".format(index+1, file)
	index = index + 1 

fileindex = input('Select file number:\n' + filelist )
print("Hai scelto: {}".format(xlsfiles[int(fileindex)-1]))

df = pd.read_excel('xls/{}'.format(xlsfiles[int(fileindex)-1]))

newUserValue = []
today = datetime.now().date()

for i in df.index:
	newUserValue.append({
		'user_login': str(df['Profile name'][i]).strip().replace('@',''), 
		'user_pass': str(df['Profile name'][i]).strip().replace('@',''), 
		'user_nicename': str(df['Profile name'][i]).strip().replace('@',''), 
		'user_email': str(df['email'][i]).strip(), 
		'display_name': str(df['Profile name'][i]).strip().replace('@',''),
		'user_registered': today
	})

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='wordpress')
index = 3
userid = createUser(cnx, newUserValue[index])
print("New user id: {}".format(userid))
updateMetaUser(cnx, userid, newUserValue[index]['display_name'])
cnx.close()

print("Image ID: {}".format(uploadImage('root', 'root', '/home/alessandro/Immagini/Schermata da 2018-02-03 14-56-26.png')))
