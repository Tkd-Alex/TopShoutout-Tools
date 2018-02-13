#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob
import pandas as pd
import mysql.connector
from pprint import pprint
from datetime import date, datetime, timedelta

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

stringInsert = ("INSERT INTO wp_users"
             	"(user_login, user_pass, user_nicename, user_email, display_name, user_registered)"
              	"VALUES (%(user_login)s, md5(%(user_pass)s), %(user_nicename)s, %(user_email)s, %(display_name)s, %(user_registered)s)")
insertValue = []
today = datetime.now().date()

for i in df.index:
	insertValue.append({
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

cursor = cnx.cursor()
cursor.execute(stringInsert, insertValue[4])
cnx.commit()
print("ID: {}".format(cursor.lastrowid))
cursor.close()
cnx.close()
