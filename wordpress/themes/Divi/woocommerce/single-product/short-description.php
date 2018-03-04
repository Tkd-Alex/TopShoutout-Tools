<?php
/**
 * Single product short description
 *
 * This template can be overridden by copying it to yourtheme/woocommerce/single-product/short-description.php.
 *
 * HOWEVER, on occasion WooCommerce will need to update template files and you
 * (the theme developer) will need to copy the new files to your theme to
 * maintain compatibility. We try to do this as little as possible, but it does
 * happen. When this occurs the version of the template file will be bumped and
 * the readme will list any important changes.
 *
 * @see 	    https://docs.woocommerce.com/document/template-structure/
 * @author 		WooThemes
 * @package 	WooCommerce/Templates
 * @version     1.6.4
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly
}

global $post;

/*
if ( ! $post->post_excerpt ) {
	return;
}
*/

?>
<div class="woocommerce-product-details__short-description">
    <?php echo apply_filters( 'woocommerce_short_description', $post->post_excerpt ); ?>
</div>

<?php echo do_shortcode('[custom_fields_block]'); ?>

<?php echo do_shortcode('[tax id="niche" before="Niche: " separator=", " after=""]'); ?> <br>
<?php echo do_shortcode('[tax id="account_size" before="Account Size: " separator=", " after=""]'); ?> <br>
<?php echo do_shortcode('[tax id="location" before="Location: " separator=", " after=""]'); ?> <br>
<?php echo do_shortcode('[tax id="audience_gender" before="Audience Gender: " separator=", " after=""]'); ?> 