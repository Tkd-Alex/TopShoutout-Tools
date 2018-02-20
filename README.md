# TopShoutout-Tools

## To-Do in topshoutout.com
- Install [JWT Authentication for WP REST API](https://it.wordpress.org/plugins/jwt-authentication-for-wp-rest-api/)
- [Hide related product](https://docs.woocommerce.com/document/remove-related-posts-output/): 
```php
remove_action( 'woocommerce_after_single_product_summary', 'woocommerce_output_related_products', 20 );
```
