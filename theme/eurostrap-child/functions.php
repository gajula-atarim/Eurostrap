<?php
/**
 * Eurostrap child theme for Hello Elementor.
 *
 * @package Eurostrap
 */

defined( 'ABSPATH' ) || exit;

define( 'EUROSTRAP_VERSION', '1.0.0' );
define( 'EUROSTRAP_DIR', get_stylesheet_directory() );
define( 'EUROSTRAP_URI', get_stylesheet_directory_uri() );

require_once EUROSTRAP_DIR . '/inc/helpers.php';
require_once EUROSTRAP_DIR . '/inc/posts-widget.php';

/**
 * Asset version: bump with file modification time so caches refresh after a deploy.
 */
function eurostrap_asset_ver( $rel ) {
	$path = EUROSTRAP_DIR . '/' . $rel;
	return file_exists( $path ) ? EUROSTRAP_VERSION . '.' . filemtime( $path ) : EUROSTRAP_VERSION;
}

add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style(
		'eurostrap-fonts',
		'https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@300;400;500;600;700;800;900&display=swap',
		[],
		null
	);

	$deps = [ 'eurostrap-fonts' ];
	foreach ( [ 'hello-elementor', 'hello-elementor-theme-style', 'elementor-frontend', 'hfe-style', 'hfe-widgets-style' ] as $handle ) {
		if ( wp_style_is( $handle, 'registered' ) ) {
			$deps[] = $handle;
		}
	}
	wp_enqueue_style( 'eurostrap', EUROSTRAP_URI . '/assets/css/eurostrap.css', $deps, eurostrap_asset_ver( 'assets/css/eurostrap.css' ) );

	wp_enqueue_script( 'eurostrap', EUROSTRAP_URI . '/assets/js/eurostrap.js', [], eurostrap_asset_ver( 'assets/js/eurostrap.js' ), true );
	wp_localize_script( 'eurostrap', 'ESData', [
		'home'   => home_url( '/' ),
		'assets' => eurostrap_asset_urls(),
		'phone'  => '+61243842567',
	] );
}, 30 );

add_action( 'wp_head', function () {
	echo '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
}, 1 );

add_filter( 'body_class', function ( $classes ) {
	$classes[] = 'es-site';
	if ( is_front_page() ) {
		$classes[] = 'es-home';
	}
	return $classes;
} );

add_action( 'after_setup_theme', function () {
	add_theme_support( 'custom-logo', [ 'height' => 80, 'width' => 257, 'flex-width' => true, 'flex-height' => true ] );
	add_theme_support( 'post-thumbnails' );
	register_nav_menus( [
		'es-primary' => __( 'Eurostrap primary', 'eurostrap' ),
	] );
}, 20 );

/* Hello Elementor: keep the page title out of Elementor-built pages. */
add_filter( 'hello_elementor_page_title', function ( $show ) {
	return is_singular( 'post' ) ? false : $show;
} );

/* Excerpt length for article cards. */
add_filter( 'excerpt_length', function () {
	return 24;
}, 99 );

/* Contact Form 7: markup is laid out in the form templates themselves. */
add_filter( 'wpcf7_autop_or_not', '__return_false' );
