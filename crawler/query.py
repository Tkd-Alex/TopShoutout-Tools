# SQL WORDPRESS QUERY
UPDATE_THUMBNAIL = "UPDATE wppt_postmeta SET meta_value = '%s' WHERE meta_key = '_thumbnail_id' AND post_id = '%s' "
UPDATE_IMG_GALLERY = "UPDATE wppt_postmeta SET meta_value = '%s' WHERE meta_key = '_product_image_gallery' AND post_id = '%s' "
UPDATE_FOLLOWER = "UPDATE wppt_postmeta SET meta_value = '%s' WHERE meta_key = 'ct_Followers_text_2365' AND post_id = '%s' "
UPDATE_ENGAGEMENT_RATE = "UPDATE wppt_postmeta SET meta_value = '%s' WHERE meta_key = 'ct_Engagement_text_2863' AND post_id = '%s' "
UPDATE_POST_INFO = "UPDATE wppt_posts SET post_modified = '%(today)s', post_modified_gmt = '%(today)s', post_status='publish', guid = '%(guid)s', post_name = '%(post_name)s' WHERE ID = '%(post_id)s' "

GET_POST_TITLE = "SELECT post_title FROM wppt_posts WHERE ID = '%s' "

#SQL LITE QUERY
INIT_TABLE = '''CREATE TABLE IF NOT EXISTS influencers ( ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, POST_ID INTEGER UNIQUE NOT NULL, IG_NAME CHAR(255) NOT NULL, THUMB_ID CHAR(50), GALLERY_IDS CHAR(50) );'''
NEW_INFLUENCER = "INSERT INTO influencers (POST_ID, IG_NAME, THUMB_ID, GALLERY_IDS) VALUES (%d, '%s', '%s', '%s' )"
UPDATE_INFLUENCER = "UPDATE influencers SET IG_NAME, THUMB_ID, GALLERY_IDS VALUES (%d, '%s', '%s') WHERE POST_ID = '%s' "
DELETE_INFLUENCER = "DELETE FROM influencers WHERE POST_ID = '%s' "
GET_IGNAME = "SELECT IG_NAME FROM influencers WHERE POST_ID = '%s' "