## To-Do in topshoutout.com
- Install [JWT Authentication for WP REST API](https://it.wordpress.org/plugins/jwt-authentication-for-wp-rest-api/)
- [Hide related product](https://docs.woocommerce.com/document/remove-related-posts-output/): 
```php
remove_action( 'woocommerce_after_single_product_summary', 'woocommerce_output_related_products', 20 );
```
- [Show founded number](https://www.woocommerce-filter.com/hook/woof_print_content_before_search_form/)
```php
add_filter('woof_print_content_before_search_form', function($content) {
    global $WOOF;
    if ($WOOF->is_isset_in_request_data($WOOF->get_swoof_search_slug())){
        return $content . 'Found results: ' . do_shortcode('[woof_found_count]') . '<br /><br />' ;
    }
    return '';
});
```
- Install [YITH Infinite Scrolling](https://wordpress.org/plugins/yith-infinite-scrolling/) and [set-up](https://www.woocommerce-filter.com/make-infinite-scroll-for-filtered-products-also/) for replace woocommerce pagination.
- [Auto complete orders](https://docs.woocommerce.com/document/automatically-complete-orders/). Or replace the file [divi_functions.php](/wp_res/themes/Divi/functions.php). Remember to disable mail for _Processing Orders_
```php
add_action( 'woocommerce_thankyou', 'custom_woocommerce_auto_complete_order' );
function custom_woocommerce_auto_complete_order( $order_id ) { 
    if ( ! $order_id ) {
        return;
    }

    $order = wc_get_order( $order_id );
    $order->update_status( 'completed' );
}
```
- Put the sidebar on top (for mobile responsive). Replace the following function in file __wp-content/themes/Divi/functions.php_ or replace the file with [divi_functions.php](/wp_res/themes/Divi/functions.php)
```php
function et_divi_output_content_wrapper() {
	echo '
		<div id="main-content">
			<div class="container">
				<div id="content-area" class="clearfix">
					<div id="left-area">';
}

function et_divi_output_content_wrapper_end() {
	$default_sidebar_class = is_rtl() ? 'et_left_sidebar' : 'et_right_sidebar';

	echo '</div> <!-- #left-area -->';

	if (
		( is_product() && 'et_full_width_page' !== get_post_meta( get_the_ID(), '_et_pb_page_layout', true ) )
		||
		( ( is_shop() || is_product_category() || is_product_tag() ) && 'et_full_width_page' !== et_get_option( 'divi_shop_page_sidebar', $default_sidebar_class ) )
	) {
		woocommerce_get_sidebar();
	}

	echo '
				</div> <!-- #content-area -->
			</div> <!-- .container -->
		</div> <!-- #main-content -->';
}
```
```php
function et_divi_output_content_wrapper() {
	
	echo '
		<div id="main-content">
			<div class="container">
				<div id="content-area" class="clearfix">';

	$default_sidebar_class = is_rtl() ? 'et_left_sidebar' : 'et_right_sidebar';
	if (
		( is_product() && 'et_full_width_page' !== get_post_meta( get_the_ID(), '_et_pb_page_layout', true ) )
		||
		( ( is_shop() || is_product_category() || is_product_tag() ) && 'et_full_width_page' !== et_get_option( 'divi_shop_page_sidebar', $default_sidebar_class ) )
	) {
		woocommerce_get_sidebar();
	}

	echo '				<div id="left-area">';
}

function et_divi_output_content_wrapper_end() {
	
	echo '</div> <!-- #left-area -->';

	echo '
				</div> <!-- #content-area -->
			</div> <!-- .container -->
		</div> <!-- #main-content -->';
}
```
- Fix all menu
  - **Influencer Dashbord Menu**
    - Dashboard (page)
    - Add Instagram Page (page)
    - Edit account (page)
  - **Primary Menu**
    - Add dashboard (page) Show if Influencer, Hide if Company
    - Remove my account for influenzer
  - Edit page **Dashboard** [1/4 , 3/4] [Sidebar, Text], [Influencer Dashbord Menu, [wpuf_dashboard post_type="product"]]
  - Edit page **Edit** [1/4 , 3/4] [Sidebar, Text], [Influencer Dashbord Menu, [wpuf_edit]]
  - Edit page **Edit Account** [1/4 , 3/4] [Sidebar, Text], [Influencer Dashbord Menu, [wpuf_editprofile]]
- Disable (and delete):
  - [Ultimate CSV Importer](https://it.wordpress.org/plugins/wp-ultimate-csv-importer/)
  - [Wp All Import](http://www.wpallimport.com/)
  - [Mailgun for WordPress](https://it.wordpress.org/plugins/mailgun/)
- Install:
  - [WP Mail SMTP by WPForms](https://it.wordpress.org/plugins/wp-mail-smtp/)
  - [WP Mail Logging](https://it.wordpress.org/plugins/wp-mail-logging/)
- Update custom mail template.
