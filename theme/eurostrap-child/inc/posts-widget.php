<?php
/**
 * Article cards: the UAE "Basic Posts" widget renders the cards. When the widget
 * carries the `es-articles` CSS class we add the category pill over the image and
 * show an estimated reading time in place of the date, matching the design.
 *
 * @package Eurostrap
 */

defined( 'ABSPATH' ) || exit;

$GLOBALS['eurostrap_in_articles'] = false;

add_action( 'elementor/widget/before_render_content', function ( $widget ) {
	if ( 'hfe-basic-posts' !== $widget->get_name() ) {
		return;
	}
	$classes = (string) $widget->get_settings( '_css_classes' );
	$GLOBALS['eurostrap_in_articles'] = false !== strpos( $classes, 'es-articles' );
} );

add_filter( 'elementor/widget/render_content', function ( $content, $widget ) {
	if ( 'hfe-basic-posts' === $widget->get_name() ) {
		$GLOBALS['eurostrap_in_articles'] = false;
	}
	return $content;
}, 10, 2 );

function eurostrap_reading_time( $post_id ) {
	$words = str_word_count( wp_strip_all_tags( get_post_field( 'post_content', $post_id ) ) );
	return max( 1, (int) ceil( $words / 200 ) ) . ' min read';
}

add_filter( 'post_thumbnail_html', function ( $html, $post_id ) {
	if ( empty( $GLOBALS['eurostrap_in_articles'] ) || ! $html ) {
		return $html;
	}
	$cats = get_the_category( $post_id );
	if ( $cats ) {
		$html .= '<span class="es-post-tag">' . esc_html( $cats[0]->name ) . '</span>';
	}
	return $html;
}, 10, 2 );

add_filter( 'get_the_date', function ( $date, $format, $post ) {
	if ( empty( $GLOBALS['eurostrap_in_articles'] ) ) {
		return $date;
	}
	return eurostrap_reading_time( $post ? $post->ID : get_the_ID() );
}, 10, 3 );
