<?php
/**
 * Asset helpers. The installer tags every brand-kit image in the media library with
 * the `_es_asset_key` meta so templates and scripts can find them by a stable key.
 *
 * @package Eurostrap
 */

defined( 'ABSPATH' ) || exit;

function eurostrap_asset_urls() {
	$cached = get_transient( 'eurostrap_asset_urls' );
	if ( is_array( $cached ) ) {
		return $cached;
	}
	$urls  = [];
	$posts = get_posts( [
		'post_type'      => 'attachment',
		'post_status'    => 'inherit',
		'posts_per_page' => 200,
		'meta_key'       => '_es_asset_key',
		'fields'         => 'ids',
	] );
	foreach ( $posts as $id ) {
		$urls[ get_post_meta( $id, '_es_asset_key', true ) ] = wp_get_attachment_url( $id );
	}
	set_transient( 'eurostrap_asset_urls', $urls, DAY_IN_SECONDS );
	return $urls;
}

add_action( 'add_attachment', function () {
	delete_transient( 'eurostrap_asset_urls' );
} );
