#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, glob, requests, random
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
		'post_excerpt': '&nbsp;',
		'post_status': 'publish',
		'comment_status': 'closed',
		'ping_status': 'closed',
		'post_name': '{}_{}'.format(value['niche1'], userid),
		'guid': '{}/product/{}-{}'.format(HOST, value['niche1'], userid),
		'post_type': 'product'
	}
	cursor.execute(query, value)
	cnx.commit()
	return cursor.lastrowid

def updateMetaPost(cnx, productid, values):
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
		'_wpuf_form_id': '',
		'php_everywhere_code': '',
		'_manage_stock': 'no',
		'_product_attributes': 'a:0:{}',
		'_product_version': '3.3.1',
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
		'_et_pb_post_hide_nav': 'default',
		'_et_pb_post_layout': 'et_right_sidebar',
		'_et_pb_side_nav': 'off',
		'_et_pb_page_layout': 'et_right_sidebar',
		'_wc_average_rating': '0',
		'_wc_rating_count': 'a:0:{}',
		'_wc_review_count': '0',
		'total_sales': '0',
		'et_enqueued_post_fonts': 'a:2:{s:6:\"family\";a:0:{}s:6:\"subset\";a:2:{i:0;s:5:\"latin\";i:1;s:9:\"latin-ext\";}}',
		'_price': float(values['ct_24h_post_editor_cb97']),
		'_regular_price': float(values['ct_24h_post_editor_cb97']),
		'_product_image': '',
		'_thumbnail_id': '', 
		'_product_image_gallery': '',
		'ct_12h_post_text_39c1': '${}'.format(float(values['ct_12h_post_text_39c1'])),
		'ct_1h_post_text_d4d1': '${}'.format(float(values['ct_1h_post_text_d4d1'])),
		'ct_24h_post_editor_cb97': '${}'.format(float(values['ct_24h_post_editor_cb97'])),
		'ct_3h_post_text_2029': '${}'.format(float(values['ct_3h_post_text_2029'])),
		'ct_Instagram__text_846a': values['ct_Instagram__text_846a'],
		'ct_Link_in_bi_radio_a6bf': values['ct_Link_in_bi_radio_a6bf'],
		'ct_Permanent__text_f9d4': '${}'.format(float(values['ct_Permanent__text_f9d4'])),
		'ct_Story_text_fd6d': '${}'.format(float(values['ct_Story_text_fd6d']))
	}
	for i in value:
		cursor.execute(query, {
			'post_id': productid,
			'meta_key': i,
			'meta_value': value[i]
		})
		
	with open('idusername.txt', 'a') as logger:
		logger.write("{},{}\n".format(productid,values['ct_Instagram__text_846a']))
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
		print('{} founded id is: {}'.format(name, term_id[0]))
		return term_id[0]

def createTerm(cnx, name, type):
	print("Create taxonomy {} == {}".format(name, type))
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
	return termid

def createRelationship(cnx, postid, termid, type):
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
		print("Update term_taxonomy_id: {}, count: {} => {}".format(id, int(count), int(count)+1))
	else:
		query = ("INSERT INTO wppt_term_taxonomy"
			 "(term_id, taxonomy, count)"
			 "VALUES (%(term_id)s, %(taxonomy)s, 1)")
		cursor.execute(query, {'term_id': termid, 'taxonomy': type})
		cnx.commit()
		print("Taxonomy not exist, init with count 1. termid: {}, taxonomy: {}".format(termid, type))
		id = cursor.lastrowid
	
	cursor = cnx.cursor()
	query = ("INSERT INTO wppt_term_relationships"
			 "(object_id, term_taxonomy_id)"
			 "VALUES (%(object_id)s, %(term_taxonomy_id)s)")
	cursor.execute(query, {'object_id': postid, 'term_taxonomy_id': id})
	print("Create relationship, postid: {}, taxonomyid: {}, type: {}".format(postid, id, type))
	cnx.commit()
	
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
		'ct_Instagram__text_846a': str(df['Profile name'][i]).strip(),
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

for index in range (0, len(userValue)):
	print("Index: {}".format(index))
	userid = createUser(cnx, userValue[index])
	print("New user {} id: {}".format(userValue[index]['user_login'], userid))
	updateMetaUser(cnx, userid, userValue[index]['display_name'])
	print("Meta user updated for user id: {}".format(userid))
	print("----------------------------")

	postid = createPost(cnx, userid, additionalInfo[index])
	print("New post {}_{} id: {}".format(additionalInfo[index]['niche1'], userid, postid))
	updateMetaPost(cnx, postid, postValue[index])
	print("Meta post updated for post id: {}".format(postid))
	print("----------------------------")

	if not additionalInfo[index]['niche1'] == "" and not additionalInfo[index]['niche1'] == "nan" :
		createRelationship(cnx, postid, checkTerm(cnx, additionalInfo[index]['niche1'], 'niche'), 'niche')
		print("----------------------------")
	if not additionalInfo[index]['niche2'] == "" and not additionalInfo[index]['niche2'] == "nan" :
		createRelationship(cnx, postid, checkTerm(cnx, additionalInfo[index]['niche2'], 'niche'), 'niche')
		print("----------------------------")
	if not additionalInfo[index]['niche3'] == "" and not additionalInfo[index]['niche3'] == "nan" :
		createRelationship(cnx, postid, checkTerm(cnx, additionalInfo[index]['niche3'], 'niche'), 'niche')
		print("----------------------------")
	if not additionalInfo[index]['country'] == "" and not additionalInfo[index]['country'] == "nan" :
		createRelationship(cnx, postid, checkTerm(cnx, additionalInfo[index]['country'], 'location'), 'location')
		print("----------------------------")
	if not additionalInfo[index]['gender'] == "" and not additionalInfo[index]['gender'] == "nan" :
		createRelationship(cnx, postid, checkTerm(cnx, additionalInfo[index]['gender'], 'audience_gender'), 'audience_gender')
		print("----------------------------")

	# Wordpress simple and influenzer cat
	createRelationship(cnx, postid, checkTerm(cnx, 'simple', 'product_type'), 'product_type')
	createRelationship(cnx, postid, checkTerm(cnx, 'influenzer', 'product_cat'), 'product_cat') 

	print("Complete!\n----------------------------")
cnx.close()
