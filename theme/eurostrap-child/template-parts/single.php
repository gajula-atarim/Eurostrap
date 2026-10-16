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
	$eurostrap_related = eurostrap_related_machines( $eurostrap_cats ? $eurostrap_cats[0]->slug : '' );
	if ( $eurostrap_related ) :
		?>
	<section class="es-sec es-related">
		<div class="es-wrap">
			<div class="es-sechead">
				<div class="es-kicker es-kicker--red"><div class="elementor-heading-title"><?php esc_html_e( 'RELATED MACHINES', 'eurostrap' ); ?></div></div>
				<h2 class="es-h es-h--48"><span class="elementor-heading-title"><?php esc_html_e( 'Machines mentioned in this article', 'eurostrap' ); ?></span></h2>
			</div>
			<div class="es-rel">
				<?php foreach ( $eurostrap_related as $eurostrap_m ) : ?>
					<a class="es-mcard es-tilt" href="<?php echo esc_url( $eurostrap_m['url'] ); ?>">
						<div class="es-mcard__media"><div class="es-mcard__img"><img src="<?php echo esc_url( $eurostrap_m['img'] ); ?>" alt="<?php echo esc_attr( $eurostrap_m['name'] ); ?>" loading="lazy"></div></div>
						<div class="es-mcard__body">
							<h3 class="es-mcard__title"><span class="elementor-heading-title"><?php echo esc_html( $eurostrap_m['name'] ); ?></span></h3>
							<div class="es-mcard__price"><p><span><?php esc_html_e( 'Price', 'eurostrap' ); ?></span> <strong><?php esc_html_e( 'On request', 'eurostrap' ); ?> <em>→</em></strong></p></div>
						</div>
					</a>
				<?php endforeach; ?>
			</div>
		</div>
	</section>
	<?php endif; ?>

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
