# SQL WORDPRESS QUERY
UPDATE_THUMBNAIL = "UPDATE wppt_postmeta SET meta_value = '%s' WHERE meta_key = '_thumbnail_id' AND post_id = '%s' "
UPDATE_IMG_GALLERY = "UPDATE wppt_postmeta SET meta_value = '%s' WHERE meta_key = '_product_image_gallery' AND post_id = '%s' "
UPDATE_FOLLOWER = "UPDATE wppt_postmeta SET meta_value = '%s' WHERE meta_key = 'ct_Followers_text_2365' AND post_id = '%s' "
UPDATE_ENGAGEMENT_RATE = "UPDATE wppt_postmeta SET meta_value = '%s' WHERE meta_key = 'ct_Engagement_text_2863' AND post_id = '%s' "
UPDATE_POST_INFO = "UPDATE wppt_posts SET post_modified = '%(today)s', post_modified_gmt = '%(today)s', post_status='publish', guid = '%(guid)s', post_name = '%(post_name)s' WHERE ID = '%(post_id)s' "

GET_POST_TITLE = "SELECT post_title FROM wppt_posts WHERE ID = '%s' "
GET_IMAGE_ID = "SELECT meta_value, meta_key FROM wppt_postmeta WHERE ( meta_key = '_product_image_gallery' OR meta_key = '_thumbnail_id' ) AND post_id = '%s' "
GET_IMAGE_TITLE = "SELECT ID, post_title FROM wppt_posts WHERE post_type = 'attachment' AND ID IN ( %s )"

GET_INSTAGRAM_PAGE = "SELECT wppt_posts.ID, wppt_postmeta.meta_value FROM wppt_posts INNER JOIN wppt_postmeta ON wppt_posts.ID = wppt_postmeta.post_id WHERE wppt_posts.post_type = 'product' AND wppt_posts.post_status = 'publish' AND wppt_postmeta.meta_key = 'ct_Instagram__text_846a' "