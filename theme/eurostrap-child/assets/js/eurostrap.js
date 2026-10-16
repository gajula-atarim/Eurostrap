/**
 * Eurostrap front-end behaviour.
 * Content lives in Elementor; this file only adds motion and interaction:
 * hero entrance, Ken Burns, scroll reveals, parallax, card tilt, the "On"
 * ellipse, button outline strokes, the machines rotator, the mega menu
 * (built from the WordPress "Machines" sub-menu) and the mobile drawer.
 */
(function () {
	'use strict';

	var doc = document;
	var body = doc.body;
	var ES = window.ESData || { assets: {}, home: '/' };
	var EDITOR = body.classList.contains('elementor-editor-active');
	var REDUCE = (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) || typeof IntersectionObserver === 'undefined';
	var EASE = 'cubic-bezier(.2,.7,.2,1)';

	function $(sel, ctx) { return (ctx || doc).querySelector(sel); }
	function $$(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }
	function el(tag, cls, html) { var n = doc.createElement(tag); if (cls) n.className = cls; if (html != null) n.innerHTML = html; return n; }
	function isDesktop() { return window.innerWidth > 1024; }

	if (!REDUCE && !EDITOR) body.classList.add('es-motion');

	/* ------------------------------------------------ button outline strokes */
	var SVG_NS = 'http://www.w3.org/2000/svg';
	function strokeSvg(mod) {
		var s = doc.createElementNS(SVG_NS, 'svg');
		s.setAttribute('aria-hidden', 'true');
		s.setAttribute('class', 'es-btn__line es-btn__line--' + mod);
		[['0', '50%', '14', '0'], ['14', '0', '46%', '0']].forEach(function (p) {
			var l = doc.createElementNS(SVG_NS, 'line');
			l.setAttribute('x1', p[0]); l.setAttribute('y1', p[1]); l.setAttribute('x2', p[2]); l.setAttribute('y2', p[3]);
			s.appendChild(l);
		});
		return s;
	}
	function decorateButtons(ctx) {
		$$('.elementor-widget.es-btn', ctx).forEach(function (btn) {
			var w = btn.querySelector('.elementor-button-wrapper') || btn;
			if (w.querySelector('.es-btn__line')) return;
			w.insertBefore(strokeSvg('b'), w.firstChild);
			w.insertBefore(strokeSvg('a'), w.firstChild);
		});
	}
	decorateButtons();

	/* ------------------------------------------------ "On" ellipse */
	$$('.es-on').forEach(function (on) {
		if (on.querySelector('.es-ellipse')) return;
		on.insertAdjacentHTML('beforeend', '<svg class="es-ellipse" viewBox="0 0 200 120" preserveAspectRatio="none" aria-hidden="true"><ellipse cx="100" cy="60" rx="96" ry="54" pathLength="1" transform="rotate(-6 100 60)"></ellipse></svg>');
	});

	/* ------------------------------------------------ hero entrance */
	if (!REDUCE && !EDITOR) {
		$$('.es-hero').forEach(function (hero) {
			$$('.es-anim-hero', hero).forEach(function (n, i) { n.style.animationDelay = (150 + i * 120) + 'ms'; });
		});
	}

	/* ------------------------------------------------ scroll reveal */
	var io = null;
	function reveal(n, animate) {
		if (io) io.unobserve(n);
		if (!n.classList.contains('es-hidden')) return;
		n.classList.remove('es-hidden');
		if (!animate) { n.classList.add('es-revealed'); return; }
		n.style.animationDelay = (n.dataset.delay || 0) + 'ms';
		n.classList.add('es-in', 'es-revealed');
	}
	if (!REDUCE && !EDITOR) {
		io = new IntersectionObserver(function (entries) {
			entries.forEach(function (e) { if (e.isIntersecting) reveal(e.target, true); });
		}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
		var groups = new Map();
		$$('.es-reveal').forEach(function (n) {
			if (n.getBoundingClientRect().top < window.innerHeight) { n.classList.add('es-revealed'); return; }
			var p = n.parentElement; var i = groups.get(p) || 0; groups.set(p, i + 1);
			n.dataset.delay = Math.min(i, 6) * 80;
			n.classList.add('es-hidden');
			io.observe(n);
		});
		window.addEventListener('beforeprint', function () { $$('.es-hidden').forEach(function (n) { reveal(n, false); }); });
		setTimeout(function () {
			$$('.es-hidden').forEach(function (n) { if (n.getBoundingClientRect().top < window.innerHeight) reveal(n, false); });
		}, 1600);
	} else {
		$$('.es-reveal').forEach(function (n) { n.classList.add('es-revealed'); });
	}

	/* ------------------------------------------------ parallax + header state */
	var header = $('.es-header');
	var parallax = $$('.es-parallax').map(function (n) {
		var m = n.className.match(/es-px-(-?)(\d+)/);
		return { el: n, f: m ? (m[1] ? -1 : 1) * parseInt(m[2], 10) / 100 : 0 };
	});
	var ticking = false;
	function scrollFx() {
		ticking = false;
		var vh = window.innerHeight;
		if (!REDUCE && !EDITOR && window.innerWidth > 767) {
			parallax.forEach(function (p) {
				var r = p.el.parentElement.getBoundingClientRect();
				var d = (r.top + r.height / 2) - vh / 2;
				p.el.style.transform = 'translate3d(0,' + (d * p.f).toFixed(1) + 'px,0)';
			});
		}
		if (header) header.classList.toggle('es-header--solid', window.scrollY > 640 || body.classList.contains('es-menu-open'));
	}
	window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(scrollFx); } }, { passive: true });
	window.addEventListener('resize', function () { if (!ticking) { ticking = true; requestAnimationFrame(scrollFx); } });
	scrollFx();

	/* ------------------------------------------------ card tilt */
	if (!REDUCE && !EDITOR && window.matchMedia('(hover: hover)').matches) {
		var lastTilt = null;
		doc.addEventListener('mousemove', function (e) {
			var card = e.target.closest ? e.target.closest('.es-tilt') : null;
			if (lastTilt && lastTilt !== card) lastTilt.style.transform = '';
			lastTilt = card;
			if (!card) return;
			var r = card.getBoundingClientRect();
			var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
			card.style.transform = 'perspective(900px) rotateX(' + (-y * 6).toFixed(2) + 'deg) rotateY(' + (x * 8).toFixed(2) + 'deg) translateY(-4px)';
		});
	}

	/* ------------------------------------------------ machines rotator */
	$$('.es-machines').forEach(function (sec) {
		var grid = $('.es-mgrid', sec);
		if (!grid || EDITOR) return;
		var cards = $$(':scope > .es-mcard', grid);
		var N = cards.length;
		if (N < 5) return;
		var tabs = $$('.es-tabs__row .es-tab:not(.es-tab--active)', sec);
		var dotsWrap = $('.es-dots', sec);
		var pages = Math.ceil(N / 4) || 1;
		var dots = [];
		if (dotsWrap) {
			for (var i = 0; i < Math.min(pages, 3); i++) { var d = el('span'); dotsWrap.appendChild(d); dots.push(d); }
		}
		var tab = 0, hold = false, timer = null;
		var AUTOPLAY_MS = 4500;
		function render(animate, dir) {
			var visible = [0, 1, 2, 3].map(function (k) { return (tab + k) % N; });
			cards.forEach(function (c, i) {
				var on = visible.indexOf(i) !== -1;
				c.classList.toggle('is-shown', on);
				c.classList.toggle('is-hidden', !on);
				c.style.order = on ? String(visible.indexOf(i) + 1) : '';
				c.classList.remove('es-card-in', 'es-card-in--back');
			});
			tabs.forEach(function (t, i) { t.classList.toggle('es-tab--on', visible.indexOf(i) !== -1); });
			var page = Math.floor(tab / 4) % dots.length;
			dots.forEach(function (d, i) { d.classList.toggle('is-on', i === page); });
			if (animate && !REDUCE) {
				// Cards slide in from the side they are coming from, staggered left to right.
				visible.map(function (i) { return cards[i]; }).forEach(function (c, i) {
					void c.offsetWidth;
					c.style.animationDelay = (i * 70) + 'ms';
					c.classList.add(dir < 0 ? 'es-card-in--back' : 'es-card-in');
				});
			}
		}
		var intro = $('.es-mgrid__intro', grid), explore = $('.es-mgrid__explore', grid);
		if (intro) intro.style.order = '0';
		if (explore) explore.style.order = '9';
		function go(delta) { tab = ((tab + delta) % N + N) % N; render(true, delta); }
		// Autoplay always runs (reduced-motion visitors get the swap without the slide);
		// it only pauses while the pointer is on a machine card.
		function start() { clearInterval(timer); timer = setInterval(function () { if (!hold && !doc.hidden) go(4); }, AUTOPLAY_MS); }
		cards.forEach(function (c) {
			c.addEventListener('mouseenter', function () { hold = true; });
			c.addEventListener('mouseleave', function () { hold = false; });
			c.addEventListener('focusin', function () { hold = true; });
			c.addEventListener('focusout', function () { hold = false; });
		});
		var next = $('.es-sq--next a', sec), prev = $('.es-sq--prev a', sec);
		if (next) next.addEventListener('click', function (e) { e.preventDefault(); go(4); start(); });
		if (prev) prev.addEventListener('click', function (e) { e.preventDefault(); go(-4); start(); });
		var row = $('.es-tabs__row', sec), more = $('.es-tabs__more a', sec);
		if (row && more) more.addEventListener('click', function (e) {
			e.preventDefault();
			if (row.scrollLeft + row.clientWidth >= row.scrollWidth - 4) row.scrollTo({ left: 0 }); else row.scrollBy({ left: 320 });
		});
		render(false);
		start();
	});

	/* Jump-link tab rows without a rotator still need the scroll button. */
	$$('.es-jump .es-tabs').forEach(function (t) {
		var row = $('.es-tabs__row', t), more = $('.es-tabs__more a', t);
		if (row && more) more.addEventListener('click', function (e) {
			e.preventDefault();
			if (row.scrollLeft + row.clientWidth >= row.scrollWidth - 4) row.scrollTo({ left: 0 }); else row.scrollBy({ left: 320 });
		});
	});

	/* ------------------------------------------------ mega menu */
	function buildMega() {
		if (!header || EDITOR) return;
		var li = $('.es-nav li.es-mega', header);
		var sub = li && $(':scope > .sub-menu', li);
		if (!sub) return;
		var panel = el('div', 'es-mega-panel');
		var inner = el('div', 'es-mega-panel__inner');
		panel.appendChild(inner);
		$$(':scope > li', sub).forEach(function (col) {
			var c = el('div', 'es-mega-col');
			var a = $(':scope > a, :scope > .hfe-has-submenu-container > a', col);
			var label = a ? a.textContent.trim() : '';
			if (col.classList.contains('es-mega-feature') && a) {
				var f = el('a', 'es-mega-col__feature', '<span></span><i>→</i>');
				f.href = a.href; f.firstChild.textContent = label;
				c.appendChild(f);
			} else {
				var l = el('span', 'es-mega-col__label'); l.textContent = label; c.appendChild(l);
			}
			$$(':scope > .sub-menu > li > a, :scope > .sub-menu > li > .hfe-has-submenu-container > a', col).forEach(function (link) {
				var m = el('a', 'es-mega-link', '<i>›</i><span></span>');
				m.href = link.href; m.lastChild.textContent = link.textContent.trim();
				c.appendChild(m);
			});
			inner.appendChild(c);
		});
		var promo = el('a', 'es-mega-promo');
		promo.href = (ES.home || '/') + 'contact/';
		promo.innerHTML = (ES.assets && ES.assets['wrapping-warehouse'] ? '<img src="' + ES.assets['wrapping-warehouse'] + '" alt="" loading="lazy">' : '') +
			'<span class="es-mega-promo__txt"><span class="es-mega-promo__t">Not sure which machine you need?</span><span class="es-mega-promo__c">Talk to a specialist <i>→</i></span></span>';
		inner.appendChild(promo);
		header.appendChild(panel);

		var t = null;
		function open() { if (!isDesktop()) return; clearTimeout(t); panel.classList.add('is-open'); li.classList.add('es-mega-open'); }
		function close() { clearTimeout(t); t = setTimeout(function () { panel.classList.remove('is-open'); li.classList.remove('es-mega-open'); }, 120); }
		[li, panel].forEach(function (n) { n.addEventListener('mouseenter', open); n.addEventListener('mouseleave', close); });
		li.addEventListener('focusin', open);
		panel.addEventListener('focusin', open);
		panel.addEventListener('focusout', close);
		doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') { panel.classList.remove('is-open'); li.classList.remove('es-mega-open'); } });
		$$('a', panel).forEach(function (a) { a.addEventListener('click', function () { panel.classList.remove('is-open'); }); });
	}
	buildMega();

	/* ------------------------------------------------ mobile drawer */
	function buildDrawer() {
		if (!header || EDITOR) return;
		var burger = $('.es-burger a', header);
		var menu = $('.es-nav ul.hfe-nav-menu', header);
		if (!burger || !menu) return;
		var drawer = el('div', 'es-drawer');
		drawer.id = 'es-drawer';
		var nav = el('nav');
		nav.setAttribute('aria-label', 'Mobile');
		var ul = el('ul');
		function copyItems(srcUl, dstUl, depth) {
			$$(':scope > li', srcUl).forEach(function (src, idx) {
				var li = el('li');
				var a = $(':scope > a, :scope > .hfe-has-submenu-container > a', src);
				var row = el('div', 'es-drawer__row');
				if (a) {
					var na = el('a'); na.href = a.getAttribute('href') || '#';
					na.textContent = (a.childNodes[0] && a.childNodes[0].textContent || a.textContent).trim();
					row.appendChild(na);
				}
				li.appendChild(row);
				var sub = $(':scope > .sub-menu', src);
				if (sub) {
					if (depth === 0) {
						var b = el('button', 'es-drawer__toggle', '▼');
						b.type = 'button'; b.setAttribute('aria-expanded', 'false'); b.setAttribute('aria-label', 'Show sub-menu');
						b.addEventListener('click', function () {
							var o = li.classList.toggle('is-open'); b.setAttribute('aria-expanded', o ? 'true' : 'false');
						});
						row.appendChild(b);
					}
					var nu = el('ul', 'sub-menu');
					copyItems(sub, nu, depth + 1);
					li.appendChild(nu);
				}
				if (depth === 0) li.style.transitionDelay = (80 + idx * 50) + 'ms';
				dstUl.appendChild(li);
			});
		}
		copyItems(menu, ul, 0);
		nav.appendChild(ul);
		drawer.appendChild(nav);
		var ctas = el('div', 'es-drawer__ctas');
		ctas.innerHTML = '<a class="is-red" href="' + (ES.home || '/') + 'contact/">Get a quote</a><a class="is-glass" href="tel:' + (ES.phone || '+61243842567') + '">Expert help · (02) 4384 2567</a>';
		drawer.appendChild(ctas);
		body.appendChild(drawer);

		burger.setAttribute('aria-controls', 'es-drawer');
		burger.setAttribute('aria-expanded', 'false');
		burger.setAttribute('aria-label', 'Open menu');
		function setOpen(o) {
			body.classList.toggle('es-menu-open', o);
			burger.setAttribute('aria-expanded', o ? 'true' : 'false');
			scrollFx();
		}
		burger.addEventListener('click', function (e) { e.preventDefault(); setOpen(!body.classList.contains('es-menu-open')); });
		drawer.addEventListener('click', function (e) { if (e.target.tagName === 'A') setOpen(false); });
		doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
		window.addEventListener('resize', function () { if (isDesktop()) setOpen(false); });
	}
	buildDrawer();

	/* Keep Elementor's lightbox off the logo link. */
	$$('.es-logo a[data-elementor-open-lightbox]').forEach(function (a) { a.setAttribute('data-elementor-open-lightbox', 'no'); });
})();
