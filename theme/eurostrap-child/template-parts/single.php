<?php
/**
 * Single article: dark hero (matches the page heroes), readable body, then the
 * reusable "Related" block. Header and footer come from the UAE templates.
 *
 * @package Eurostrap
 */

defined( 'ABSPATH' ) || exit;

while ( have_posts() ) :
	the_post();
	$eurostrap_cats  = get_the_category();
	$eurostrap_thumb = get_the_post_thumbnail_url( get_the_ID(), 'full' );
	if ( ! $eurostrap_thumb ) {
		$eurostrap_assets = eurostrap_asset_urls();
		$eurostrap_thumb  = $eurostrap_assets['warehouse-pallets'] ?? '';
	}
	?>
<main id="content" <?php post_class( 'site-main es-single' ); ?>>
	<section class="es-hero es-hero--page es-single-hero">
		<div class="es-hero__bg">
			<?php if ( $eurostrap_thumb ) : ?>
				<div class="es-hero__img es-kenburns"><img src="<?php echo esc_url( $eurostrap_thumb ); ?>" alt="" fetchpriority="high"></div>
			<?php endif; ?>
		</div>
		<div class="es-hero__inner">
			<div class="es-hero__content">
				<div class="es-eyebrow es-anim-hero"><div class="elementor-heading-title"><?php esc_html_e( 'Industry insights', 'eurostrap' ); ?></div></div>
				<h1 class="es-hero__title-raw es-anim-hero"><?php the_title(); ?></h1>
				<div class="es-meta es-anim-hero">
					<?php if ( $eurostrap_cats ) : ?>
						<a href="<?php echo esc_url( get_category_link( $eurostrap_cats[0] ) ); ?>"><?php echo esc_html( $eurostrap_cats[0]->name ); ?></a>
					<?php endif; ?>
					<span><?php echo esc_html( get_the_date() ); ?> · <?php echo esc_html( eurostrap_reading_time( get_the_ID() ) ); ?></span>
				</div>
			</div>
		</div>
	</section>

	<article class="es-article">
		<?php the_content(); ?>
	</article>

	<?php
	$eurostrap_cta = get_page_by_path( 'articles' );
	?>
	<section class="es-sec es-cta">
		<div class="es-wrap es-wrap--cta">
			<h2 class="es-h es-h--60"><span class="elementor-heading-title"><?php esc_html_e( 'Have a question about your line?', 'eurostrap' ); ?></span></h2>
			<p class="es-lead"><?php esc_html_e( 'Our specialists can help you choose the right machine, strap or film.', 'eurostrap' ); ?></p>
			<div class="es-btnrow">
				<div class="es-btn es-btn--red elementor-widget"><div class="elementor-button-wrapper"><a class="elementor-button" href="<?php echo esc_url( home_url( '/contact/' ) ); ?>"><?php esc_html_e( 'Talk to a specialist', 'eurostrap' ); ?></a></div></div>
				<div class="es-btn es-btn--white elementor-widget"><div class="elementor-button-wrapper"><a class="elementor-button" href="<?php echo esc_url( $eurostrap_cta ? get_permalink( $eurostrap_cta ) : home_url( '/articles/' ) ); ?>"><?php esc_html_e( 'More articles', 'eurostrap' ); ?></a></div></div>
			</div>
		</div>
	</section>
</main>
	<?php
endwhile;
