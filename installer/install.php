<?php
/**
 * Eurostrap site installer. Idempotent: safe to run again after a rebuild.
 *
 * Expects ES_RAW (raw GitHub base URL ending in "/") and optionally $ES_STAGES
 * (array of stage names) to be defined by the caller before this file is eval'd.
 *
 * Stages: plugins, theme, media, cf7, pages, menus, hf, posts, settings, flush
 */

if ( ! defined( 'ABSPATH' ) || ! defined( 'ES_RAW' ) ) {
	return 'missing context';
}

@set_time_limit( 0 );
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/plugin.php';
require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
require_once ABSPATH . 'wp-admin/includes/plugin-install.php';
require_once ABSPATH . 'wp-admin/includes/nav-menu.php';

$es_log    = [];
$es_stages = isset( $ES_STAGES ) && is_array( $ES_STAGES ) ? $ES_STAGES : [ 'plugins', 'theme', 'media', 'cf7', 'pages', 'menus', 'hf', 'posts', 'settings', 'flush' ];
$es_run    = function ( $s ) use ( $es_stages ) { return in_array( $s, $es_stages, true ); };

$es_get = function ( $path ) {
	$r = wp_remote_get( ES_RAW . $path, [ 'timeout' => 60 ] );
	if ( is_wp_error( $r ) || 200 !== (int) wp_remote_retrieve_response_code( $r ) ) {
		throw new Exception( 'Could not fetch ' . $path . ( is_wp_error( $r ) ? ': ' . $r->get_error_message() : ' (HTTP ' . wp_remote_retrieve_response_code( $r ) . ')' ) );
	}
	return wp_remote_retrieve_body( $r );
};

$manifest = json_decode( $es_get( 'build/out/manifest.json' ), true );
update_option( 'es_install_log', [ 'time' => current_time( 'mysql' ), 'stages' => $es_stages, 'log' => 'started' ], false );

/* ------------------------------------------------------------------ plugins */
if ( $es_run( 'plugins' ) ) {
	WP_Filesystem();
	$skin = new Automatic_Upgrader_Skin();
	foreach ( [
		'elementor'               => 'elementor/elementor.php',
		'header-footer-elementor' => 'header-footer-elementor/header-footer-elementor.php',
		'contact-form-7'          => 'contact-form-7/wp-contact-form-7.php',
	] as $slug => $file ) {
		if ( ! file_exists( WP_PLUGIN_DIR . '/' . $file ) ) {
			$api  = plugins_api( 'plugin_information', [ 'slug' => $slug, 'fields' => [ 'sections' => false ] ] );
			$link = ( ! is_wp_error( $api ) && ! empty( $api->download_link ) ) ? $api->download_link : 'https://downloads.wordpress.org/plugin/' . $slug . '.latest-stable.zip';
			$up   = new Plugin_Upgrader( $skin );
			$res  = $up->install( $link );
			if ( true !== $res ) {
				// Newest releases may need a newer PHP than the host runs: step back through known versions.
				$fallbacks = 'contact-form-7' === $slug ? [ '6.1.4', '6.1.3', '6.1.1', '6.0.6', '5.9.8' ] : [];
				foreach ( $fallbacks as $ver ) {
					$res = ( new Plugin_Upgrader( $skin ) )->install( 'https://downloads.wordpress.org/plugin/' . $slug . '.' . $ver . '.zip' );
					if ( true === $res ) {
						$es_log['plugins'][ $slug . '_version' ] = $ver;
						break;
					}
				}
			}
			$es_log['plugins'][ $slug ] = is_wp_error( $res ) ? $res->get_error_message() : $res;
			$es_log['plugins'][ $slug . '_skin' ] = $skin->get_upgrade_messages();
			wp_clean_plugins_cache( true );
		}
		$res = activate_plugin( $file );
		$es_log['plugins'][ $slug . '_active' ] = is_wp_error( $res ) ? $res->get_error_message() : is_plugin_active( $file );
	}
}

/* ------------------------------------------------------------------ child theme */
if ( $es_run( 'theme' ) ) {
	$dir   = get_theme_root() . '/eurostrap-child';
	$files = array_filter( array_map( 'trim', explode( "\n", $es_get( 'theme/files.txt' ) ) ) );
	foreach ( $files as $rel ) {
		$target = $dir . '/' . $rel;
		wp_mkdir_p( dirname( $target ) );
		file_put_contents( $target, $es_get( 'theme/eurostrap-child/' . $rel ) );
	}
	$es_log['theme']['files'] = count( $files );
	if ( get_stylesheet() !== 'eurostrap-child' ) {
		switch_theme( 'eurostrap-child' );
	}
	$es_log['theme']['active'] = get_stylesheet();
}

/* ------------------------------------------------------------------ media */
$es_asset_id = function ( $key ) {
	$q = get_posts( [ 'post_type' => 'attachment', 'post_status' => 'inherit', 'meta_key' => '_es_asset_key', 'meta_value' => $key, 'fields' => 'ids', 'posts_per_page' => 1 ] );
	return $q ? (int) $q[0] : 0;
};

if ( $es_run( 'media' ) ) {
	$assets = json_decode( $es_get( 'build/out/assets.json' ), true );
	foreach ( $assets as $key => $a ) {
		if ( $es_asset_id( $key ) ) {
			continue;
		}
		$tmp = false;
		foreach ( $a['sources'] as $src ) {
			$url = 0 === strpos( $src, 'http' ) ? $src : ES_RAW . $src;
			$tmp = download_url( $url, 120 );
			if ( ! is_wp_error( $tmp ) ) {
				break;
			}
			$tmp = false;
		}
		if ( ! $tmp ) {
			$es_log['media'][ $key ] = 'download failed';
			continue;
		}
		$id = media_handle_sideload( [ 'name' => $a['filename'], 'tmp_name' => $tmp ], 0, $a['alt'] );
		if ( is_wp_error( $id ) ) {
			@unlink( $tmp );
			$es_log['media'][ $key ] = $id->get_error_message();
			continue;
		}
		update_post_meta( $id, '_es_asset_key', $key );
		update_post_meta( $id, '_wp_attachment_image_alt', $a['alt'] );
		$es_log['media'][ $key ] = $id;
	}
	$logo = $es_asset_id( 'eurostrap-logo' );
	if ( $logo ) {
		set_theme_mod( 'custom_logo', $logo );
	}
	delete_transient( 'eurostrap_asset_urls' );
}

/* ------------------------------------------------------------------ Contact Form 7 */
if ( $es_run( 'cf7' ) && class_exists( 'WPCF7_ContactForm' ) ) {
	$host   = wp_parse_url( home_url(), PHP_URL_HOST );
	$sender = '[_site_title] <wordpress@' . $host . '>';
	$cats   = array_map( function ( $c ) { return '"' . $c['name'] . '"'; }, $manifest['categories'] );
	$forms  = [
		'enquiry'    => [
			'title' => 'Eurostrap enquiry',
			'form'  => "<div class=\"es-formgrid\">\n<label class=\"es-field\"><span>Name *</span>[text* your-name autocomplete:name]</label>\n<label class=\"es-field\"><span>Company</span>[text your-company autocomplete:organization]</label>\n<label class=\"es-field\"><span>Phone *</span>[tel* your-phone autocomplete:tel]</label>\n<label class=\"es-field\"><span>Email *</span>[email* your-email autocomplete:email]</label>\n<label class=\"es-field es-field--full\"><span>Machine interest</span>[select your-machine first_as_label \"Select a machine or service\" " . implode( ' ', $cats ) . " \"Not sure yet\"]</label>\n<label class=\"es-field es-field--full\"><span>Message</span>[textarea your-message x5 placeholder \"Tell us about your loads, output and timing\"]</label>\n</div>\n<div class=\"es-formfoot\">[submit \"Send enquiry\"]<span class=\"es-formfoot__note\">We reply within one business day.</span></div>",
			'mail'  => [
				'subject'            => 'Website enquiry from [your-name] ([your-company])',
				'sender'             => $sender,
				'recipient'          => '[_site_admin_email]',
				'body'               => "Name: [your-name]\nCompany: [your-company]\nPhone: [your-phone]\nEmail: [your-email]\nMachine interest: [your-machine]\n\nMessage:\n[your-message]\n\n-- \nSent from the enquiry form on [_site_url]",
				'additional_headers' => 'Reply-To: [your-email]',
				'attachments'        => '',
				'use_html'           => false,
				'exclude_blank'      => false,
			],
		],
		'newsletter' => [
			'title' => 'Eurostrap newsletter',
			'form'  => "<div class=\"es-nl\">[email* your-email placeholder \"Enter your email...\"][submit \"Subscribe\"]</div>",
			'mail'  => [
				'subject'            => 'New specials subscriber: [your-email]',
				'sender'             => $sender,
				'recipient'          => '[_site_admin_email]',
				'body'               => "Please add this address to the specials email list:\n[your-email]\n\n-- \nSent from the footer form on [_site_url]",
				'additional_headers' => 'Reply-To: [your-email]',
				'attachments'        => '',
				'use_html'           => false,
				'exclude_blank'      => false,
			],
		],
	];
	$ids = (array) get_option( 'es_cf7', [] );
	foreach ( $forms as $key => $f ) {
		$cf = ! empty( $ids[ $key ] ) ? wpcf7_contact_form( $ids[ $key ] ) : null;
		if ( ! $cf ) {
			$cf = WPCF7_ContactForm::get_template( [ 'title' => $f['title'] ] );
		}
		$cf->set_title( $f['title'] );
		$props             = $cf->get_properties();
		$props['form']     = $f['form'];
		$props['mail']     = array_merge( (array) $props['mail'], $f['mail'] );
		$props['mail_2']   = array_merge( (array) $props['mail_2'], [ 'active' => false ] );
		$props['messages'] = array_merge( (array) $props['messages'], [ 'mail_sent_ok' => $key === 'newsletter' ? 'Subscribed, thanks.' : 'Thanks, your enquiry has been sent. We will be in touch within one business day.' ] );
		$cf->set_properties( $props );
		$ids[ $key ] = $cf->save();
	}
	update_option( 'es_cf7', $ids );
	$es_log['cf7'] = $ids;
}

/* ------------------------------------------------------------------ Elementor documents */
$es_fill = function ( $json ) use ( $es_asset_id ) {
	$json = preg_replace_callback( '/"__ID_([a-z0-9-]+)__"/', function ( $m ) use ( $es_asset_id ) {
		return (string) $es_asset_id( $m[1] );
	}, $json );
	$json = preg_replace_callback( '/__URL_([a-z0-9-]+)__/', function ( $m ) use ( $es_asset_id ) {
		$id = $es_asset_id( $m[1] );
		return $id ? str_replace( '/', '\\/', wp_get_attachment_url( $id ) ) : '';
	}, $json );
	$ids  = (array) get_option( 'es_cf7', [] );
	$json = str_replace( [ '__CF7_enquiry__', '__CF7_newsletter__' ], [ (string) ( $ids['enquiry'] ?? 0 ), (string) ( $ids['newsletter'] ?? 0 ) ], $json );
	return $json;
};

$es_find = function ( $type, $key ) {
	$q = get_posts( [ 'post_type' => $type, 'post_status' => 'any', 'meta_key' => '_es_key', 'meta_value' => $key, 'fields' => 'ids', 'posts_per_page' => 1 ] );
	return $q ? (int) $q[0] : 0;
};

$es_save_doc = function ( $doc, $post_type, $parent = 0, $template = 'elementor_header_footer' ) use ( $es_get, $es_fill, $es_find ) {
	$json = $es_fill( $es_get( 'build/out/' . $doc['file'] ) );
	if ( null === json_decode( $json ) ) {
		throw new Exception( 'Invalid JSON for ' . $doc['key'] );
	}
	$id = $es_find( $post_type, $doc['key'] );
	if ( ! $id && 'page' === $post_type && ! empty( $doc['slug'] ) ) {
		// Adopt an existing page with the same slug (e.g. WordPress's draft Privacy Policy).
		$existing = get_page_by_path( $doc['slug'] );
		if ( $existing && ! get_post_meta( $existing->ID, '_es_key', true ) ) {
			$id = $existing->ID;
			update_post_meta( $id, '_es_key', $doc['key'] );
		}
	}
	$args = [
		'post_type'    => $post_type,
		'post_title'   => $doc['title'],
		'post_status'  => 'publish',
		'post_parent'  => $parent,
		'post_content' => '',
	];
	if ( ! empty( $doc['slug'] ) ) {
		$args['post_name'] = $doc['slug'];
	}
	if ( $id ) {
		$args['ID'] = $id;
		wp_update_post( $args );
	} else {
		$id = wp_insert_post( $args );
		update_post_meta( $id, '_es_key', $doc['key'] );
	}
	update_post_meta( $id, '_elementor_edit_mode', 'builder' );
	update_post_meta( $id, '_elementor_template_type', 'page' === $post_type ? 'wp-page' : 'wp-post' );
	update_post_meta( $id, '_elementor_version', defined( 'ELEMENTOR_VERSION' ) ? ELEMENTOR_VERSION : '3.0.0' );
	update_post_meta( $id, '_wp_page_template', $template );
	update_post_meta( $id, '_elementor_page_settings', [ 'hide_title' => 'yes' ] );
	update_post_meta( $id, '_elementor_data', wp_slash( $json ) );
	delete_post_meta( $id, '_elementor_css' );
	delete_post_meta( $id, '_elementor_element_cache' );
	return $id;
};

if ( $es_run( 'pages' ) ) {
	$page_ids = [];
	foreach ( $manifest['docs'] as $doc ) {
		if ( 'page' !== $doc['type'] || ! empty( $doc['parent'] ) ) {
			continue;
		}
		$page_ids[ $doc['key'] ] = $es_save_doc( $doc, 'page' );
	}
	foreach ( $manifest['docs'] as $doc ) {
		if ( 'page' !== $doc['type'] || empty( $doc['parent'] ) ) {
			continue;
		}
		$page_ids[ $doc['key'] ] = $es_save_doc( $doc, 'page', $page_ids[ $doc['parent'] ] ?? 0 );
	}
	update_option( 'es_pages', $page_ids );
	if ( ! empty( $page_ids['privacy'] ) ) {
		update_option( 'wp_page_for_privacy_policy', (int) $page_ids['privacy'] );
	}
	$es_log['pages'] = $page_ids;

	// Remove the WordPress starter content on this fresh install.
	$sample = get_page_by_path( 'sample-page' );
	if ( $sample && ! get_post_meta( $sample->ID, '_es_key', true ) ) {
		wp_trash_post( $sample->ID );
	}
	$hello = get_page_by_path( 'hello-world', OBJECT, 'post' );
	if ( $hello ) {
		wp_trash_post( $hello->ID );
	}
}

/* ------------------------------------------------------------------ menus */
if ( $es_run( 'menus' ) ) {
	$pages = (array) get_option( 'es_pages', [] );
	$purl  = function ( $key ) use ( $pages ) { return isset( $pages[ $key ] ) ? get_permalink( $pages[ $key ] ) : home_url( '/' ); };
	$menu  = function ( $name ) {
		$m = wp_get_nav_menu_object( $name );
		$id = $m ? $m->term_id : wp_create_nav_menu( $name );
		foreach ( (array) wp_get_nav_menu_items( $id ) as $item ) {
			wp_delete_post( $item->ID, true );
		}
		return $id;
	};
	$add = function ( $menu_id, $title, $url_or_page, $parent = 0, $classes = '' ) {
		$args = [
			'menu-item-title'     => $title,
			'menu-item-status'    => 'publish',
			'menu-item-parent-id' => $parent,
			'menu-item-classes'   => $classes,
		];
		if ( is_int( $url_or_page ) ) {
			$args['menu-item-object-id'] = $url_or_page;
			$args['menu-item-object']    = 'page';
			$args['menu-item-type']      = 'post_type';
		} else {
			$args['menu-item-url']  = $url_or_page;
			$args['menu-item-type'] = 'custom';
		}
		return wp_update_nav_menu_item( $menu_id, 0, $args );
	};
	$cat = [];
	foreach ( $manifest['categories'] as $c ) {
		$cat[ $c['name'] ] = (int) ( $pages[ 'cat-' . $c['slug'] ] ?? 0 );
	}

	$primary = $menu( 'Eurostrap Primary' );
	$add( $primary, 'Home', (int) $pages['home'] );
	$add( $primary, 'About', (int) $pages['about'] );
	$m = $add( $primary, 'Machines', (int) $pages['machines'], 0, 'es-mega' );
	$w = $add( $primary, 'Wrapping Machines', $cat['Wrapping Machines'], $m, 'es-mega-feature' );
	$wurl = get_permalink( $cat['Wrapping Machines'] );
	$add( $primary, 'Automatic In-Line Stretch Wrapping Machines', $wurl . '#automatic-in-line', $w );
	$add( $primary, 'Semi-Automatic Stretch Wrapping Machines', $wurl . '#semi-automatic', $w );
	$add( $primary, 'Self-Propelled Semi-automatic Stretch Wrapping Machines', $wurl . '#self-propelled', $w );
	$add( $primary, 'Horizontal Stretch Machines', $wurl . '#horizontal', $w );
	$s = $add( $primary, 'Solutions', get_permalink( $pages['machines'] ) . '#range', $m, 'es-mega-label' );
	foreach ( [ 'Bag Filling', 'Palletisers', 'Consultation & Design', 'Consumables', 'Robotic Palletisers' ] as $n ) {
		$add( $primary, $n, $cat[ $n ], $s );
	}
	$mm = $add( $primary, 'More Machines', get_permalink( $pages['machines'] ) . '#range', $m, 'es-mega-label' );
	foreach ( [ 'Strapping', 'Carton Sealing', 'Shrink/Stretch Hooding', 'Case Packing' ] as $n ) {
		$add( $primary, $n, $cat[ $n ], $mm );
	}
	$add( $primary, 'Articles', (int) $pages['articles'] );
	$add( $primary, 'Contact', (int) $pages['contact'] );

	$fs = $menu( 'Eurostrap Footer Solutions' );
	foreach ( [ 'Wrapping Machines', 'Bag Filling', 'Palletisers', 'Robotic Palletisers', 'Strapping' ] as $n ) {
		$add( $fs, $n, $cat[ $n ] );
	}
	$fm = $menu( 'Eurostrap Footer More' );
	foreach ( [ 'Carton Sealing', 'Shrink/Stretch Hooding', 'Case Packing', 'Consumables', 'Consultation & Design' ] as $n ) {
		$add( $fm, $n, $cat[ $n ] );
	}
	$fc = $menu( 'Eurostrap Footer Company' );
	$add( $fc, 'About', (int) $pages['about'] );
	$add( $fc, 'Articles', (int) $pages['articles'] );
	$add( $fc, 'Contact', (int) $pages['contact'] );

	$loc               = (array) get_theme_mod( 'nav_menu_locations', [] );
	$loc['es-primary'] = $primary;
	$loc['menu-1']     = $primary;
	set_theme_mod( 'nav_menu_locations', $loc );
	$es_log['menus'] = [ 'primary' => $primary, 'footer' => [ $fs, $fm, $fc ] ];
}

/* ------------------------------------------------------------------ UAE header & footer */
if ( $es_run( 'hf' ) ) {
	foreach ( $manifest['docs'] as $doc ) {
		if ( ! in_array( $doc['type'], [ 'header', 'footer' ], true ) ) {
			continue;
		}
		$id = $es_save_doc( $doc, 'elementor-hf', 0, 'default' );
		update_post_meta( $id, 'ehf_template_type', 'type_' . $doc['type'] );
		update_post_meta( $id, 'ehf_target_include_locations', [ 'rule' => [ 'basic-global' ], 'specific' => [] ] );
		update_post_meta( $id, 'ehf_target_exclude_locations', [] );
		update_post_meta( $id, 'ehf_target_user_roles', [] );
		$es_log['hf'][ $doc['type'] ] = $id;
	}
}

/* ------------------------------------------------------------------ articles (posts) */
if ( $es_run( 'posts' ) ) {
	$i = 0;
	foreach ( $manifest['articles'] as $a ) {
		$term = term_exists( $a['cat'], 'category' );
		if ( ! $term ) {
			$term = wp_insert_term( $a['cat'], 'category' );
		}
		$blocks = '';
		foreach ( $a['body'] as $b ) {
			if ( 'p' === $b[0] ) {
				$blocks .= "<!-- wp:paragraph -->\n<p>" . esc_html( $b[1] ) . "</p>\n<!-- /wp:paragraph -->\n\n";
			} elseif ( 'h2' === $b[0] ) {
				$blocks .= "<!-- wp:heading -->\n<h2 class=\"wp-block-heading\">" . esc_html( $b[1] ) . "</h2>\n<!-- /wp:heading -->\n\n";
			} elseif ( 'ul' === $b[0] ) {
				$blocks .= "<!-- wp:list -->\n<ul class=\"wp-block-list\">";
				foreach ( $b[1] as $li ) {
					$blocks .= "<!-- wp:list-item -->\n<li>" . esc_html( $li ) . "</li>\n<!-- /wp:list-item -->";
				}
				$blocks .= "</ul>\n<!-- /wp:list -->\n\n";
			}
		}
		$existing = get_page_by_path( $a['slug'], OBJECT, 'post' );
		$args     = [
			'post_type'     => 'post',
			'post_status'   => 'publish',
			'post_title'    => $a['title'],
			'post_name'     => $a['slug'],
			'post_excerpt'  => $a['excerpt'],
			'post_content'  => $blocks,
			'post_category' => [ (int) $term['term_id'] ],
			'post_date'     => wp_date( 'Y-m-d H:i:s', time() - ( $i * 9 + 1 ) * DAY_IN_SECONDS ),
		];
		if ( $existing ) {
			$args['ID']            = $existing->ID;
			$args['post_date_gmt'] = get_gmt_from_date( $args['post_date'] );
			$args['edit_date']     = true;
			$pid = wp_update_post( $args );
		} else {
			$pid = wp_insert_post( $args );
		}
		$thumb = $es_asset_id( $a['img'] );
		if ( $thumb ) {
			set_post_thumbnail( $pid, $thumb );
		}
		$es_log['posts'][ $a['slug'] ] = $pid;
		$i++;
	}
}

/* ------------------------------------------------------------------ settings */
if ( $es_run( 'settings' ) ) {
	$pages = (array) get_option( 'es_pages', [] );
	update_option( 'blogname', 'Eurostrap Packaging Systems' );
	update_option( 'blogdescription', 'Specialists in End-Of-Line Load Securement and Packaging Solutions' );
	update_option( 'show_on_front', 'page' );
	if ( ! empty( $pages['home'] ) ) {
		update_option( 'page_on_front', (int) $pages['home'] );
	}
	update_option( 'page_for_posts', 0 );
	update_option( 'permalink_structure', '/%postname%/' );
	update_option( 'elementor_disable_color_schemes', 'yes' );
	update_option( 'elementor_disable_typography_schemes', 'yes' );
	update_option( 'elementor_cpt_support', [ 'page', 'post', 'elementor-hf' ] );
	update_option( 'elementor_experiment-container', 'active' );
	update_option( 'elementor_unfiltered_files_upload', '' );
	update_option( 'hello_elementor_settings_description_meta_tag', 'true' );
	flush_rewrite_rules( false );
	$es_log['settings'] = 'ok';
}

/* ------------------------------------------------------------------ Elementor kit: brand colours + type */
if ( $es_run( 'kit' ) ) {
	$kit_id = (int) get_option( 'elementor_active_kit' );
	if ( $kit_id ) {
		$ks = (array) get_post_meta( $kit_id, '_elementor_page_settings', true );
		$ks['system_colors'] = [
			[ '_id' => 'primary', 'title' => 'Eurostrap Red', 'color' => '#D9302C' ],
			[ '_id' => 'secondary', 'title' => 'Charcoal', 'color' => '#4A4A4A' ],
			[ '_id' => 'text', 'title' => 'Body Text', 'color' => '#5A5A5A' ],
			[ '_id' => 'accent', 'title' => 'Accent Red', 'color' => '#D9302C' ],
		];
		$ks['custom_colors'] = [
			[ '_id' => 'es_ink', 'title' => 'Ink', 'color' => '#141414' ],
			[ '_id' => 'es_steel', 'title' => 'Steel Grey', 'color' => '#6B6B6B' ],
			[ '_id' => 'es_blueprint', 'title' => 'Blueprint Grey', 'color' => '#E3E3E3' ],
			[ '_id' => 'es_mist', 'title' => 'Mist', 'color' => '#F4F4F4' ],
			[ '_id' => 'es_red_dark', 'title' => 'Red Hover', 'color' => '#B5231F' ],
			[ '_id' => 'es_white', 'title' => 'White', 'color' => '#FFFFFF' ],
		];
		$type = function ( $id, $title, $family, $weight ) {
			return [ '_id' => $id, 'title' => $title, 'typography_typography' => 'custom', 'typography_font_family' => $family, 'typography_font_weight' => $weight ];
		};
		$ks['system_typography'] = [
			$type( 'primary', 'Headings (Bebas Neue)', 'Bebas Neue', '400' ),
			$type( 'secondary', 'Subheadings (Roboto 500)', 'Roboto', '500' ),
			$type( 'text', 'Body (Roboto 400)', 'Roboto', '400' ),
			$type( 'accent', 'Buttons (Roboto 500)', 'Roboto', '500' ),
		];
		update_post_meta( $kit_id, '_elementor_page_settings', $ks );
		$es_log['kit'] = $kit_id;
	}
}

/* ------------------------------------------------------------------ flush */
if ( $es_run( 'flush' ) ) {
	if ( class_exists( '\Elementor\Plugin' ) ) {
		\Elementor\Plugin::$instance->files_manager->clear_cache();
	}
	delete_transient( 'eurostrap_asset_urls' );
	wp_cache_flush();
	$es_log['flush'] = 'ok';
}

/* ------------------------------------------------------------------ snapshot (rendered pages for auditing) */
if ( $es_run( 'snapshot' ) ) {
	$up  = wp_upload_dir();
	$dir = $up['basedir'] . '/es-audit';
	wp_mkdir_p( $dir );
	$pages = (array) get_option( 'es_pages', [] );
	$urls  = [ 'home' => home_url( '/' ) ];
	foreach ( [ 'about', 'machines', 'articles', 'contact', 'privacy', 'cat-wrapping-machines' ] as $k ) {
		if ( ! empty( $pages[ $k ] ) ) {
			$urls[ $k ] = get_permalink( $pages[ $k ] );
		}
	}
	$post = get_page_by_path( 'choosing-a-semi-automatic-stretch-wrapper', OBJECT, 'post' );
	if ( $post ) {
		$urls['post'] = get_permalink( $post );
	}
	foreach ( $urls as $k => $u ) {
		$r = wp_remote_get( add_query_arg( 'es_audit', time(), $u ), [ 'timeout' => 30, 'sslverify' => false ] );
		$es_log['snapshot'][ $k ] = is_wp_error( $r ) ? $r->get_error_message() : file_put_contents( $dir . '/' . $k . '.html', wp_remote_retrieve_body( $r ) );
	}
}

update_option( 'es_install_log', [ 'time' => current_time( 'mysql' ), 'stages' => $es_stages, 'log' => $es_log ], false );
return $es_log;
