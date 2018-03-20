<?php
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
	
	require_once("./wp-load.php");

	update_post_meta($_POST['post_id'], 'ct_Followers_text_2365', $_POST['ct_Followers_text_2365']);
	update_post_meta($_POST['post_id'], 'ct_Engagement_text_2863', $_POST['ct_Engagement_text_2863']);
	update_post_meta($_POST['post_id'], '_product_image_gallery', $_POST['_product_image_gallery']);

	if (isset($_POST['_thumbnail_id']))
		update_post_meta($_POST['post_id'], '_thumbnail_id', $_POST['_thumbnail_id']);

	wp_publish_post($_POST['post_id']);

	$cat_id = get_cat_ID('Influencer');
	wp_set_post_categories($_POST['post_id'], $cat_id);
	
	$get_terms_args = array('taxonomy' => 'niche','fields' => 'ids','hide_empty' => false);
    $update_terms = get_terms($get_terms_args);
    wp_update_term_count_now($update_terms, 'niche');
?>