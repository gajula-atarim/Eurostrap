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

/**
 * Machine category pages to show under an article, picked by the article's category.
 */
function eurostrap_related_machines( $cat_slug ) {
	$map = [
		'buying-guide' => [ 'wrapping-machines', 'consumables', 'strapping' ],
		'strapping'    => [ 'strapping', 'consumables', 'wrapping-machines' ],
		'automation'   => [ 'robotic-palletisers', 'palletisers', 'consultation-and-design' ],
	];
	$img = [
		'wrapping-machines'       => 'equipment-wrapping',
		'consumables'             => 'equipment-consumables',
		'strapping'               => 'equipment-strapping',
		'robotic-palletisers'     => 'equipment-robotic-palletisers',
		'palletisers'             => 'equipment-palletisers',
		'consultation-and-design' => 'equipment-consultation',
	];
	$slugs  = $map[ $cat_slug ] ?? [ 'wrapping-machines', 'strapping', 'robotic-palletisers' ];
	$assets = eurostrap_asset_urls();
	$out    = [];
	foreach ( $slugs as $slug ) {
		$page = get_page_by_path( 'machines/' . $slug );
		if ( ! $page ) {
			continue;
		}
		$out[] = [
			'name' => get_the_title( $page ),
			'url'  => get_permalink( $page ),
			'img'  => $assets[ $img[ $slug ] ] ?? '',
		];
	}
	return $out;
}

/**
 * Meta descriptions from the sitemap's SEO focus, unless an SEO plugin handles them.
 */
add_action( 'wp_head', function () {
	if ( defined( 'WPSEO_VERSION' ) || defined( 'RANK_MATH_VERSION' ) || defined( 'AIOSEO_VERSION' ) ) {
		return;
	}
	$desc = '';
	if ( is_front_page() ) {
		$desc = 'Stretch wrappers and strapping machines in Australia. Eurostrap Packaging Systems: specialists in end-of-line load securement, with machines, consumables and local technical support.';
	} elseif ( is_page() ) {
		$key  = get_post_meta( get_queried_object_id(), '_es_key', true );
		$map  = [
			'about'    => 'End-of-line packaging specialists in Australia. Wholly Australian owned, 20+ years in load securement and exclusive distributor of Atlanta Stretch, Area Packaging and Messersi.',
			'machines' => 'Stretch wrapping machines, strapping machines and pallet wrappers, plus palletisers, hooding, case packing and consumables from Eurostrap Packaging Systems.',
			'articles' => 'Guides and news on stretch wrapping, strapping and end-of-line automation, including how to choose a stretch wrapper.',
			'contact'  => 'Contact Eurostrap Packaging Systems, 5 Braemar Dr, Wamberal NSW 2260. Call (02) 4384 2567 for a quote or to book service.',
		];
		$desc = $map[ $key ] ?? '';
		if ( ! $desc && 0 === strpos( (string) $key, 'cat-' ) ) {
			$desc = get_the_title() . ' from Eurostrap Packaging Systems: supplied, installed and supported in Australia, with matched consumables.';
		}
	} elseif ( is_single() ) {
		$desc = wp_strip_all_tags( get_the_excerpt() );
	}
	if ( $desc ) {
		echo '<meta name="description" content="' . esc_attr( $desc ) . '">' . "\n";
	}
}, 2 );
