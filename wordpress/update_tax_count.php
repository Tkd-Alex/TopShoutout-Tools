<?php
	require_once("./wp-load.php");
	$get_terms_args = array('taxonomy' => 'niche','fields' => 'ids','hide_empty' => false);
    $update_terms = get_terms($get_terms_args);
    wp_update_term_count_now($update_terms, 'niche');
?>