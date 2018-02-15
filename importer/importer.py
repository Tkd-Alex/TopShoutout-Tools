#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, requests
import pandas as pd
import mysql.connector
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta

HOST = "http://localhost/topshoutup"
USER_TABLE = "wppt_users"
USER_META_TABLE = "wppt_usermeta"
POST_TABLE = "wppt_posts"
POST_META_TABLE = "wppt_postmeta"

def uploadImage(username, password, imagePaths):
	# Using: https://it.wordpress.org/plugins/jwt-authentication-for-wp-rest-api/
	print("Login with: {}".format(username))
	# Get JWT-Token
	res = requests.post(url = "{}/wp-json/jwt-auth/v1/token".format(HOST),
						data = { 'username': username, 'password': password})

	token = res.json()['token']
	print("Login complete, token: {}".format(token))
	imagesids = []
	for image in imagePaths:
		data = open(image, 'rb').read()
		fileName = os.path.basename(image)
		res = requests.post(url = '{}/wp-json/wp/v2/media'.format(HOST),
							data = data,
							headers = {
								'Authorization':"Bearer " + token,
								'Content-Type': 'image/jpg',
								'Content-Disposition' : 'attachment; filename=%s'% fileName
						})
		imagesids.append(res.json()['id'])
		return imagesids

def createUser(cnx, value):
	cursor = cnx.cursor()
	query = ("INSERT INTO " + USER_TABLE +
			 "(user_login, user_pass, user_nicename, user_email, display_name, user_registered)"
			 "VALUES (%(user_login)s, md5(%(user_pass)s), %(user_nicename)s, %(user_email)s, %(display_name)s, %(user_registered)s)")
	cursor.execute(query, value)
	cnx.commit()
	return cursor.lastrowid

def createPost(cnx, userid, value):
	cursor = cnx.cursor()
	today = datetime.now().date()
	query =	("INSERT INTO " + POST_TABLE +
			"(post_author, post_date, post_date_gmt, post_title, post_excerpt, post_status, comment_status, ping_status, post_name, guid, post_type)"
			"VALUES (%(post_author)s, %(post_date)s, %(post_date_gmt)s, %(post_title)s, %(post_excerpt)s, %(post_status)s, %(comment_status)s, %(ping_status)s, %(post_name)s, %(guid)s, %(post_type)s)")
	value = {
		'post_author': userid,
		'post_date': today,
		'post_date_gmt': today,
		'post_title': '{}_{}'.format(value['niche1'], userid),
		'post_excerpt': '',
		'post_status': 'publish',
		'comment_status': 'open',
		'ping_status': 'closed',
		'post_name': '{}_{}'.format(value['niche1'], userid),
		'guid': '{}/product/{}-{}'.format(HOST, value['niche1'], userid),
		'post_type': 'product'
	}
	cursor.execute(query, value)
	cnx.commit()
	return cursor.lastrowid

def updateMetaPost(cnx, productid, imageids, values):
	cursor = cnx.cursor()
	query = ("INSERT INTO " + POST_META_TABLE + 
			 "(post_id, meta_key, meta_value)"
			 "VALUES (%(post_id)s, %(meta_key)s, %(meta_value)s)")
	value = {
		'_backorders': 'no',
		'_crosssell_ids': 'a:0:{}',
		'_default_attributes': 'a:0:{}',
		'_download_expiry': '-1',
		'_download_limit': '-1',
		'_downloadable': 'no',
		'_downloadable_files': 'a:0:{}',
		'_height': '',
		'_length': '',
		'_weight': '',
		'_width': '',
		'_manage_stock': 'no',
		'_product_attributes': 'a:0:{}',
		'_product_version': '1',
		'_purchase_note': '',
		'_sale_price': '',
		'_sale_price_dates_from': '',
		'_sale_price_dates_to': '',
		'_sku': '',
		'_sold_individually': 'no',
		'_stock_status': 'instock',
		'_tax_class': '',
		'_tax_status': 'taxable',
		'_upsell_ids': 'a:0:{}',
		'_virtual': 'yes',
		'_wc_average_rating': '0',
		'_wc_rating_count': 'a:0:{}',
		'_wc_review_count': '0',
		'total_sales': '0',
		'et_enqueued_post_fonts': 'a:2:{s:6:\"family\";a:0:{}s:6:\"subset\";a:2:{i:0;s:5:\"latin\";i:1;s:9:\"latin-ext\";}}',
		'_price': values['ct_24h_post_editor_cb97'],
		'_regular_price': values['ct_24h_post_editor_cb97'],
		'_product_image': imageids[0],
		'_thumbnail_id': imageids[0],
		'_product_image_gallery': ','.join([str(x) for x in imageids]),
		'ct_12h_post_text_39c1': values['ct_12h_post_text_39c1'],
		'ct_1h_post_text_d4d1': values['ct_1h_post_text_d4d1'],
		'ct_24h_post_editor_cb97': values['ct_24h_post_editor_cb97'],
		'ct_3h_post_text_2029': values['ct_3h_post_text_2029'],
		'ct_Instagram__text_846a': values['ct_Instagram__text_846a'],
		'ct_Link_in_bi_radio_a6bf': values['ct_Link_in_bi_radio_a6bf'],
		'ct_Permanent__text_f9d4': values['ct_Permanent__text_f9d4'],
		'ct_Story_text_fd6d': values['ct_Story_text_fd6d']
	}
	for i in value:
		cursor.execute(query, {
			'post_id': productid,
			'meta_key': i,
			'meta_value': value[i]
		})
		cnx.commit()

	cursor.close()
	
def updateMetaUser(cnx, userid, nickname):
	cursor = cnx.cursor()
	query = ("INSERT INTO " + USER_META_TABLE + 
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

def checkTerm(cnx, name, type):
	query = ("SELECT DISTINCT term_id FROM wppt_terms WHERE name = '%s' " %(name))
	cursor = cnx.cursor()
	cursor.execute(query)
	term_id = cursor.fetchone()
	if term_id == None:
		print("Term not found")
		return createTerm(cnx, name, type)	
	else:
		return term_id[0]

def createTerm(cnx, name, type):
	cursor = cnx.cursor()
	query = ("INSERT INTO wppt_terms"
			 "(name, slug)"
			 "VALUES (%(name)s, %(slug)s)")
	cursor.execute(query, {'name': name, 'slug': name.lower().replace(' ','-')})
	cnx.commit()
	termid = cursor.lastrowid
	print("Created new term with id: {}".format(termid))
	query = ("INSERT INTO wppt_term_taxonomy"
			 "(term_id, taxonomy)"
			 "VALUES (%(term_id)s, %(taxonomy)s)")
	cursor.execute(query, {'term_id': termid, 'taxonomy': type})
	cnx.commit()
	print("Create taxonomy")
	return termid

def createRelationship(cnx, postid, termid, type):
	cursor = cnx.cursor()
	query = ("INSERT INTO wppt_term_relationships"
			 "(object_id, term_taxonomy_id)"
			 "VALUES (%(object_id)s, %(term_taxonomy_id)s)")
	cursor.execute(query, {'object_id': postid, 'term_taxonomy_id': termid})
	cnx.commit()
	query = ("SELECT DISTINCT count, term_taxonomy_id FROM wppt_term_taxonomy WHERE term_id=%s AND taxonomy='%s'" % (termid, type))
	cursor = cnx.cursor()
	cursor.execute(query)
	row = cursor.fetchone()
	id = count = None
	while row is not None:
		count = row[0]
		id = row[1]
		row = cursor.fetchone()
	if not count == None and not id == None:
		query = ("UPDATE wppt_term_taxonomy "
			 	"SET count = %d "
			 	"WHERE term_taxonomy_id = %d " % (int(count)+1, id) ) 
		cursor.execute(query)
		cnx.commit()
		print("Update term_taxonomy_id count: {} => {}".format(int(count), int(count)+1))
	else:
		query = ("INSERT INTO wppt_term_taxonomy"
			 "(term_id, taxonomy)"
			 "VALUES (%(term_id)s, %(taxonomy)s)")
		cursor.execute(query, {'term_id': termid, 'taxonomy': type})
		cnx.commit()
		print("Create taxonomy")
	
xlsfiles = []
index = 0
filelist = ""

for file in os.listdir('xls'):
	xlsfiles.append(file) 
	filelist += "[{}] File: {}\n".format(index+1, file)
	index = index + 1 

fileindex = input('Select file number:\n' + filelist )
print("Choose: {}".format(xlsfiles[int(fileindex)-1]))

df = pd.read_excel('xls/{}'.format(xlsfiles[int(fileindex)-1]))

userValue = []
postValue = []
additionalInfo = []
today = datetime.now().date()

for i in df.index:
	userValue.append({
		'user_login': str(df['Profile name'][i]).strip().replace('@',''), 
		'user_pass': str(df['Profile name'][i]).strip().replace('@',''), 
		'user_nicename': str(df['Profile name'][i]).strip().replace('@',''), 
		'user_email': str(df['email'][i]).strip(), 
		'display_name': str(df['Profile name'][i]).strip().replace('@',''),
		'user_registered': today
	})
	postValue.append({
		'ct_12h_post_text_39c1': '5',
		'ct_1h_post_text_d4d1': '5',
		'ct_24h_post_editor_cb97': str(df['1 post 24h'][i]).strip(),
		'ct_3h_post_text_2029': '5',
		'ct_Instagram__text_846a': '', #str(df['Profile name'][i]).strip()
		'ct_Link_in_bi_radio_a6bf': 'Yes',
		'ct_Permanent__text_f9d4': str(df['1 post (permanent post)'][i]).strip(),
		'ct_Story_text_fd6d': str(df['1 story'][i]).strip()
	})
	additionalInfo.append({
		'country': str(df['Followers country'][i]).strip(), 
		'gender': str(df['Follower female'][i]).strip(), 
		'niche1': str(df['Niche 1'][i]).strip(),
		'niche2': str(df['Niche 2'][i]).strip(),
		'niche3': str(df['Niche 3'][i]).strip()
	})


cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='topshoutout')

index = 0
userid = createUser(cnx, userValue[index])
print("New user id: {}".format(userid))
updateMetaUser(cnx, userid, userValue[index]['display_name'])
print("Meta user updated for user id: {}".format(userid))
imagesids = (uploadImage('TopShoutout', 'TopShoutout123!!', 
	['/home/alessandro/Immagini/Kidult_235/231533Kidult_162017114839.jpeg', 
	 '/home/alessandro/Immagini/Kidult_235/231526Kidult_162017114811.jpeg', 
	 '/home/alessandro/Immagini/Kidult_235/231527Kidult_162017120252.jpeg']))
postid = createPost(cnx, userid, additionalInfo[index])
print("New post id: {}".format(postid))
updateMetaPost(cnx, postid, imagesids, postValue[index])
print("Meta post updated for post id: {}".format(postid))
if not additionalInfo[index]['niche1'] == "" and not additionalInfo[index]['niche1'] == "nan" :
	createRelationship(cnx, postid, checkTerm(cnx, additionalInfo[index]['niche1'], 'niche'), 'niche')
	print("Relationship create for {} <-- niche1 --> {}".format(postid, additionalInfo[index]['niche1']))
if not additionalInfo[index]['niche2'] == "" and not additionalInfo[index]['niche2'] == "nan" :
	createRelationship(cnx, postid, checkTerm(cnx, additionalInfo[index]['niche2'], 'niche'), 'niche')
	print("Relationship create for {} <-- niche2 --> {}".format(postid, additionalInfo[index]['niche2']))
if not additionalInfo[index]['niche3'] == "" and not additionalInfo[index]['niche3'] == "nan" :
	createRelationship(cnx, postid, checkTerm(cnx, additionalInfo[index]['niche3'], 'niche'), 'niche')
	print("Relationship create for {} <-- niche3 --> {}".format(postid, additionalInfo[index]['niche3']))
if not additionalInfo[index]['country'] == "" and not additionalInfo[index]['country'] == "nan" :
	createRelationship(cnx, postid, checkTerm(cnx, additionalInfo[index]['country'], 'location'), 'location')
	print("Relationship create for {} <-- country --> {}".format(postid, additionalInfo[index]['country']))
if not additionalInfo[index]['gender'] == "" and not additionalInfo[index]['gender'] == "nan" :
	createRelationship(cnx, postid, checkTerm(cnx, additionalInfo[index]['gender'], 'audience_gender'), 'audience_gender')
	print("Relationship create for {} <-- gender --> {}".format(postid, additionalInfo[index]['gender']))

print("Complete!")
cnx.close()

