<?php
/**
 * My Account Dashboard
 *
 * Shows the first intro screen on the account dashboard.
 *
 * This template can be overridden by copying it to yourtheme/woocommerce/myaccount/dashboard.php.
 *
 * HOWEVER, on occasion WooCommerce will need to update template files and you
 * (the theme developer) will need to copy the new files to your theme to
 * maintain compatibility. We try to do this as little as possible, but it does
 * happen. When this occurs the version of the template file will be bumped and
 * the readme will list any important changes.
 *
 * @see         https://docs.woocommerce.com/document/template-structure/
 * @author      WooThemes
 * @package     WooCommerce/Templates
 * @version     2.6.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly
}
?>
<table class="items-table product" cellspacing="0" cellpadding="0">
        <thead>
            <tr class="items-list-header">
                <th style="width: 28%;">Influencers Image</th>
                <th>Influencers Name</th>
                <th>Price</th>
                <th>View Detail</th>
            </tr>
        </thead>
        <tbody>
<?php
 global $wpdb;
$iduser=get_current_user_id();
$post_id1 = $wpdb->get_results("SELECT * FROM `wppt_postmeta` WHERE (meta_key = '_customer_user' AND `meta_value` = '". $iduser ."')");
   foreach($post_id1 as $postd) {
$pids[]=$postd->post_id;
}
if($pids != "")
{

 $commaList = implode(',', $pids);
$post_id2 = $wpdb->get_results("SELECT * FROM `wppt_woocommerce_order_items` WHERE `order_id` IN (". $commaList .")");
   foreach($post_id2 as $postd1) {
$orderid[]=$postd1->order_item_id;
}

 $orderid1= implode(',', $orderid);
$post_id3 = $wpdb->get_results("SELECT * FROM `wppt_woocommerce_order_itemmeta` WHERE (meta_key = '_product_id' AND `order_item_id` IN (". $orderid1."))");
   foreach($post_id3 as $postd2) {
$orderidnew[]=$postd2->meta_value;
}

$orderidnews= implode(',', $orderidnew);
$post_id4 = $wpdb->get_results("SELECT * FROM `wppt_posts` WHERE ( `ID` IN (".$orderidnews."))");
   foreach($post_id4 as $postd3) {
$userdet=$postd3->ID;

$post_id5 = $wpdb->get_results("SELECT * FROM `wppt_posts` WHERE ( `post_parent` = '".$userdet."') LIMIT 1");
   foreach($post_id5 as $postd4) {
$userdetnew=$postd4->guid;

}
?>
                            <tr>
                  <td>

<?php 
        echo get_the_post_thumbnail( $postd3->ID, 'thumbnail' ); 
         ?>
</td>

                     <td><?php echo $postd3->post_title; ?></td>
                              <td>$<?php echo get_post_meta( $postd3->ID , '_regular_price', true); ?></td>                  
                  
                    <td>
                                            
                                                    <a href="https://topshoutout.com/product/<?php echo $postd3->post_name; ?>/">View</a>
                                            </td>
                </tr>
                
        
<?php
}
}
?>
</tbody>
    </table>
<?php
	/**
	 * My Account dashboard.
	 *
	 * @since 2.6.0
	 */
	do_action( 'woocommerce_account_dashboard' );

	/**
	 * Deprecated woocommerce_before_my_account action.
	 *
	 * @deprecated 2.6.0
	 */
	do_action( 'woocommerce_before_my_account' );

	/**
	 * Deprecated woocommerce_after_my_account action.
	 *
	 * @deprecated 2.6.0
	 */
	do_action( 'woocommerce_after_my_account' );

/* Omit closing PHP tag at the end of PHP files to avoid "headers already sent" issues. */
