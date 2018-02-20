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
- Install [YITH Infinite Scrolling](https://wordpress.org/plugins/yith-infinite-scrolling/) and [set-up](https://www.woocommerce-filter.com/make-infinite-scroll-for-filtered-products-also/) for replace woocommerce pagination 
