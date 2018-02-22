# TopShoutout-Tools

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
- Put the sidebar on top (for mobile responsive). Replace the following function in file __wp-content/themes/Divi/functions.php_ or replace the file with [divi_functions.php](/wp_res/divi_functions.php)
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
