"""Build Elementor JSON for every Eurostrap page and the UAE header/footer.

Run: python3 build/build.py  -> writes build/out/*.json and build/out/manifest.json
"""
import json
import os

from data import ARTICLES, CATEGORIES, INDUSTRIES, PHONE, PHONE_TEL, REVIEWS, STATS, SUPPLIERS
from el import (button, con, gmap, heading, img, scope, shortcode, text, uae_copyright,
                uae_logo, uae_nav, uae_posts)

OUT = os.path.join(os.path.dirname(__file__), 'out')


def cat_url(c):
    return f"/machines/{c['slug']}/"


# ---------------------------------------------------------------- shared parts

def specs_html(specs):
    return ''.join(f'<p><span>{k}</span> <strong>{v}</strong></p>' for k, v in specs)


def btn(label, url, variant='red', extra=''):
    return button(label, url, f'es-btn es-btn--{variant} {extra}'.strip())


def sechead(kicker, title, lead=None, cls='', kicker_cls='es-kicker', title_cls='es-h es-h--48', center=True):
    kids = []
    if kicker:
        kids.append(heading(kicker, 'div', kicker_cls))
    kids.append(heading(title, 'h2', title_cls))
    if lead:
        kids.append(text(f'<p>{lead}</p>', 'es-lead'))
    return con(f"es-sechead {'es-sechead--center' if center else ''} es-reveal {cls}".strip(), *kids)


def page_hero(eyebrow, title, lead, image, buttons=(), cls=''):
    ctas = [btn(*b) if len(b) == 2 else btn(b[0], b[1], b[2]) for b in buttons]
    return con(
        f'es-hero es-hero--page {cls}'.strip(),
        con('es-hero__bg', img(image, 'es-hero__img es-kenburns', alt='')),
        con('es-hero__inner',
            con('es-hero__content',
                heading(eyebrow, 'div', 'es-eyebrow es-anim-hero'),
                heading(title, 'h1', 'es-hero__title es-anim-hero'),
                text(f'<p>{lead}</p>', 'es-hero__lead es-anim-hero'),
                con('es-hero__ctas es-anim-hero', *ctas) if ctas else None)),
        tag='section')


def machine_card(c):
    return con(
        'es-mcard es-tilt',
        con('es-mcard__media', img(c['img'], 'es-mcard__img', alt=c['name'])),
        con('es-mcard__body',
            heading(c['name'], 'h3', 'es-mcard__title'),
            text(specs_html(c['specs']), 'es-specs'),
            text('<p><span>Price</span> <strong>On request <em>→</em></strong></p>', 'es-mcard__price')),
        href=cat_url(c))


def item_card(c, item, link=None):
    """Machine card. With `link`, the title links there and covers the whole card
    (stretched link), leaving the Enquire link clickable on top."""
    name, op, specs, anchor = item
    return con(
        'es-icard es-reveal' + (' es-icard--link' if link else ''),
        con('es-icard__media', img(c['img'], 'es-icard__img', alt=name)),
        con('es-icard__body',
            heading(f"{c['brand']} · {op}", 'div', 'es-label'),
            heading(name, 'h3', 'es-icard__title', href=link),
            text(specs_html(specs), 'es-specs'),
            heading('Enquire about this machine →', 'div', 'es-textlink', href='/contact/#enquiry')),
        el_id=anchor or None)


def stats_row(cls=''):
    return con(f'es-stats {cls}'.strip(), *[
        con('es-stat es-reveal',
            heading(f'{v}<span>{suf}</span>' if suf else v, 'div', 'es-stat__v'),
            text(f'<p>{label}</p>', 'es-stat__l'))
        for v, suf, label in STATS])


def suppliers_section(cls=''):
    return con(
        f'es-sec es-suppliers {cls}'.strip(),
        con('es-wrap es-wrap--suppliers',
            sechead('TRUSTED EUROPEAN MANUFACTURERS', 'Suppliers of', kicker_cls='es-kicker es-kicker--red'),
            con('es-logos', *[img(k, 'es-logo-tile es-reveal', alt=a) for k, a in SUPPLIERS])),
        tag='section')


def cta_section(title='Upgrade your end-of-line with confidence',
                lead='Get expert recommendations, transparent pricing and dependable after-sales support.',
                with_image=True, el_id='contact'):
    return con(
        'es-sec es-cta',
        con('es-wrap es-wrap--cta',
            heading(title, 'h2', 'es-h es-h--60 es-reveal'),
            text(f'<p>{lead}</p>', 'es-lead es-reveal'),
            con('es-btnrow es-reveal',
                btn('Talk to a specialist', PHONE_TEL, 'red'),
                btn('Request pricing', '/contact/#enquiry', 'white')),
            img('cta-machines', 'es-cta__img es-reveal', alt='Automatic pallet wrapping line and pallet strapping machine') if with_image else None),
        tag='section', el_id=el_id)


def articles_section(count=3, title='Expert packaging advice, machine guides, <span>and industry best practice</span>', cls=''):
    return con(
        f'es-sec es-news {cls}'.strip(),
        con('es-wrap es-wrap--news',
            con('es-news__head es-reveal',
                heading('INDUSTRY INSIGHTS', 'div', 'es-kicker'),
                heading(title, 'h2', 'es-h es-h--44')),
            uae_posts(count, 'es-articles')),
        tag='section', el_id='news')


# ---------------------------------------------------------------- home

def home():
    scope('home')
    tabs = [button('All machines', '/machines/', 'es-tab es-tab--active')]
    tabs += [button(c['name'], cat_url(c), 'es-tab') for c in CATEGORIES]
    return [
        con('es-hero es-hero--home',
            con('es-hero__bg', img('hero-wrapper-blueprint', 'es-hero__img es-kenburns', alt='Automatic ring stretch wrapper on a conveyor line')),
            con('es-hero__inner',
                heading('EUROSTRAP', 'div', 'es-hero__outline es-parallax es-px-20'),
                con('es-hero__content',
                    heading('EUROSTRAP PACKAGING SYSTEMS', 'div', 'es-eyebrow es-anim-hero'),
                    heading('Load securement<br><span>for every line</span>', 'h1', 'es-hero__title es-anim-hero'),
                    text('<p>Specialists in all forms of End-Of-Line Load Securement and Packaging Solutions.</p>', 'es-hero__lead es-anim-hero'),
                    con('es-hero__ctas es-anim-hero',
                        btn('Get a quote →', '/contact/', 'red', 'es-btn--lg'),
                        button('Explore machines →', '#machines', 'es-underline')))),
            tag='section'),

        con('es-sec es-machines',
            con('es-wrap es-wrap--machines',
                con('es-tabs es-reveal',
                    con('es-tabs__row', *tabs),
                    button('→', '#machines', 'es-tabs__more')),
                con('es-mgrid',
                    con('es-mgrid__intro',
                        heading('Machines built for demanding dispatch floors', 'h2', 'es-h es-h--46'),
                        text('<p>From basic hand applications and semi-automatic machines through to in-line, high-speed, fully automatic machines and turn-key systems.</p>', 'es-body es-body--15')),
                    *[machine_card(c) for c in CATEGORIES],
                    con('es-mgrid__explore',
                        heading('Explore full range', 'div', 'es-explore__title'),
                        con('es-explore__arrows',
                            button('←', '#machines', 'es-sq es-sq--prev'),
                            button('→', '#machines', 'es-sq es-sq--next')),
                        con('es-dots'),
                        button('View all machines →', '/machines/', 'es-btn-rect')))),
            tag='section', el_id='machines'),

        con('es-sec es-industries',
            con('es-wrap es-wrap--industries',
                sechead(None, 'Securing loads across key industries',
                        'From food and beverage to building products, our machines and services help teams ship faster, safer and with less waste.'),
                con('es-igrid', *[
                    con(f'es-tile es-tile--{i + 1} es-reveal',
                        con('es-tile__media es-zoom', img(key, 'es-tile__img', alt=t)),
                        con('es-tile__label',
                            heading(t, 'div', 'es-tile__t'),
                            text(f'<p>{d}</p>', 'es-tile__d')),
                        heading('→', 'div', 'es-tile__arrow'),
                        href=url)
                    for i, (t, d, key, url) in enumerate(INDUSTRIES)]),
                btn('View industry use cases', '/contact/', 'red')),
            tag='section'),

        con('es-sec es-trust',
            con('es-wrap es-wrap--trust',
                con('es-trust__head',
                    con('es-trust__robot es-parallax es-px--12', img('ec301-robot', 'es-trust__robotimg', alt='EC301 robotic palletiser')),
                    heading('<span>Built</span> <span class="es-on">On</span> <span>Trust</span>', 'h2', 'es-trust__title es-reveal'),
                    heading('Keeping your loads secure with proven European machines.', 'p', 'es-trust__lead es-reveal'),
                    text("<p>A wholly Australian owned company and Australasia's exclusive distributor of Atlanta Stretch, Area Packaging and Messersi, with over 20 years in end-of-line load securement.</p>", 'es-trust__copy es-reveal'),
                    btn('Learn about our company', '/about/', 'red')),
                con('es-trust__media es-reveal', img('wrapping-warehouse', 'es-trust__img', alt='Automatic stretch wrapping machine on a conveyor line')),
                stats_row()),
            tag='section', el_id='trust'),

        con('es-sec es-reviews',
            con('es-reviews__bg es-parallax es-px-15', img('strapping-warehouse', 'es-reviews__img', alt='')),
            con('es-wrap es-wrap--reviews',
                con('es-sechead es-sechead--center es-reveal',
                    heading('Client reviews', 'div', 'es-pill'),
                    heading('See what our clients say about us', 'h2', 'es-h es-h--48')),
                con('es-rgrid', *[
                    con('es-review es-reveal',
                        heading('★★★★★', 'div', 'es-review__stars'),
                        text(f'<p>{q}</p>', 'es-review__q'),
                        con('es-review__by',
                            heading(ini, 'div', 'es-review__av'),
                            con('es-review__who',
                                heading(n, 'div', 'es-review__n'),
                                heading(c, 'div', 'es-review__c'))))
                    for q, n, c, ini in REVIEWS]),
                text('<p>Sample reviews. Replace with real client feedback before launch.</p>', 'es-note')),
            tag='section'),

        articles_section(),
        suppliers_section(),
        cta_section(),
    ]


# ---------------------------------------------------------------- about

def about():
    scope('about')
    values = [
        ('Secure', 'Every message comes back to loads that arrive intact. Steady, dependable, never flashy.'),
        ('Expert', 'Two decades of end-of-line know-how. We speak in specifics: machine, film, strap, throughput.'),
        ('Complete', 'Machines, consumables and support from one supplier. The Total Solution.'),
        ('Local + European', 'Australian owned and supported, backed by Italian engineering partners.'),
    ]
    partners = [
        ('Atlanta Stretch', 'suppliers-atlanta', 'Stretch wrapping', 'Pallet wrappers from mobile robots such as the Atlanta Sfera to fully automatic ring and rotary arm machines, plus Atlanta case packers.', '/machines/wrapping-machines/'),
        ('Area Packaging', 'suppliers-area', 'Horizontal wrapping', 'Horizontal and orbital stretch wrapping machines for long products, profiles, panels and bundles.', '/machines/wrapping-machines/#horizontal'),
        ('Messersi', None, 'Strapping', 'Pallet and bundle strapping systems built around the Messersi MS300 head, running PP and PET strap.', '/machines/strapping/'),
    ]
    rng = [
        ('01', 'Hand tools', 'Battery and manual strapping tools and hand stretch film for low volumes.', '/machines/strapping/'),
        ('02', 'Semi-automatic', 'Turntable and self-propelled wrappers, semi-auto strappers and case sealers.', '/machines/wrapping-machines/#semi-automatic'),
        ('03', 'Fully automatic', 'In-line, high-speed wrapping, strapping, hooding and case packing.', '/machines/wrapping-machines/#automatic-in-line'),
        ('04', 'Turn-key systems', 'Complete end-of-line design and integration, from bag filling to dispatch.', '/machines/consultation-and-design/'),
    ]
    service = [
        ('Installation & commissioning', 'Our technicians install, commission and set up every machine we supply, then train your operators.'),
        ('Technical support', 'Local service, preventive maintenance and stocked spare parts keep your line running.'),
        ('Consumables supply', 'PP, PET and steel strap and stretch film matched to your machines, delivered when you need it.'),
    ]
    return [
        page_hero('ABOUT EUROSTRAP', 'Australian owned.<br><span>European engineered.</span>',
                  'Over 20 years in end-of-line load securement, and Australasia’s exclusive distributor of Atlanta Stretch, Area Packaging and Messersi.',
                  'wrapping-warehouse', [('Contact us', '/contact/'), ('View machines', '/machines/', 'glass')]),

        con('es-sec es-story',
            con('es-wrap es-wrap--split',
                con('es-split__left es-reveal',
                    heading('01 — OUR STORY', 'div', 'es-kicker es-kicker--red'),
                    heading('We believe in offering a Total Solution.', 'h2', 'es-h es-h--56')),
                con('es-split__right es-reveal',
                    text('<p>Eurostrap Packaging Systems is a wholly Australian owned company and Australasia’s exclusive distributor of Atlanta Stretch, Area Packaging and Messersi Packaging products and services.</p>'
                         '<p>The range covers plastic and steel strapping, stretch-wrapping and shrink-wrapping: from basic hand applications and semi-automatic machines through to in-line, high-speed, fully automatic machines and turn-key systems, plus consumables and technical support.</p>', 'es-body es-body--18'))),
            con('es-wrap es-wrap--stats', stats_row()),
            tag='section'),

        con('es-sec es-values',
            con('es-wrap es-wrap--1280',
                sechead('02 — HOW WE WORK', 'Secure, expert and complete', kicker_cls='es-kicker es-kicker--red'),
                con('es-vgrid', *[
                    con('es-vcard es-reveal',
                        heading(f'0{i + 1}', 'div', 'es-vcard__n'),
                        heading(t, 'h3', 'es-vcard__t'),
                        text(f'<p>{d}</p>', 'es-vcard__d'))
                    for i, (t, d) in enumerate(values)])),
            tag='section'),

        con('es-sec es-partners',
            con('es-wrap es-wrap--1280',
                sechead('03 — PARTNERS', 'Exclusive distributor partnerships',
                        'Proven European machines, sold, installed and supported by a local Australian team.', kicker_cls='es-kicker es-kicker--red'),
                con('es-pgrid', *[
                    con('es-pcard es-cardlink es-reveal',
                        con('es-pcard__logo', img(logo, 'es-pcard__img', alt=n) if logo else heading(n, 'div', 'es-pcard__wordmark')),
                        heading(tag, 'div', 'es-label'),
                        heading(n, 'h3', 'es-pcard__t'),
                        text(f'<p>{d}</p>', 'es-pcard__d'),
                        heading('View machines →', 'div', 'es-textlink'),
                        href=url)
                    for n, logo, tag, d, url in partners])),
            tag='section'),

        con('es-sec es-range',
            con('es-wrap es-wrap--split es-wrap--range',
                con('es-range__media es-reveal', img('robot-palletiser', 'es-range__img', alt='Robotic palletiser')),
                con('es-range__body',
                    sechead('04 — THE RANGE', 'From hand tools to turn-key systems', center=False, kicker_cls='es-kicker es-kicker--red'),
                    con('es-steps', *[
                        con('es-step es-cardlink es-reveal',
                            heading(n, 'div', 'es-step__n'),
                            con('es-step__body',
                                heading(t, 'h3', 'es-step__t'),
                                text(f'<p>{d}</p>', 'es-step__d')),
                            href=url)
                        for n, t, d, url in rng]),
                    btn('Explore the machines', '/machines/', 'red'))),
            tag='section'),

        con('es-sec es-service',
            con('es-service__bg es-parallax es-px-15', img('strapping-warehouse', 'es-reviews__img', alt='')),
            con('es-wrap es-wrap--reviews',
                con('es-sechead es-sechead--center es-reveal',
                    heading('Service & support', 'div', 'es-pill'),
                    heading('Service, installation and technical support', 'h2', 'es-h es-h--48')),
                con('es-rgrid', *[
                    con('es-review es-reveal',
                        heading(f'0{i + 1}', 'div', 'es-review__stars'),
                        heading(t, 'h3', 'es-service__t'),
                        text(f'<p>{d}</p>', 'es-review__q'))
                    for i, (t, d) in enumerate(service)])),
            tag='section'),

        suppliers_section(),
        cta_section('Talk to the Eurostrap team', 'Tell us about your loads and output. We will recommend the right machine, consumables and support.'),
    ]


# ---------------------------------------------------------------- machines

def machines():
    scope('machines')
    jump = [button('All machines', '#range', 'es-tab es-tab--active')]
    jump += [button(c['name'], f"#{c['slug']}", 'es-tab') for c in CATEGORIES]
    sections = []
    for i, c in enumerate(CATEGORIES):
        sections.append(con(
            f"es-sec es-cat {'es-cat--alt' if i % 2 else ''}".strip(),
            con('es-wrap es-wrap--1280',
                con('es-cat__head es-reveal',
                    con('es-cat__title',
                        heading(f"{i + 1:02d} — {c['brand'].upper()}", 'div', 'es-kicker es-kicker--red'),
                        heading(c['name'], 'h2', 'es-h es-h--48')),
                    con('es-cat__intro',
                        text(f"<p><strong>{c['lead']}.</strong> {c['intro']}</p>", 'es-body es-body--16'),
                        heading(f"View {c['name'].lower()} →", 'div', 'es-textlink', href=cat_url(c)))),
                con('es-igrid4', *[item_card(c, it, cat_url(c) + (f"#{it[3]}" if it[3] else '')) for it in c['items']])),
            tag='section', el_id=c['slug']))
    return [
        page_hero('THE MACHINE RANGE', 'Machines for<br><span>every end-of-line</span>',
                  'Stretch wrapping, strapping, hooding, palletising and case packing from Atlanta Stretch, Area Packaging, Messersi and partners, with consumables and local support.',
                  'hero-wrapper-blueprint', [('Request a quote', '/contact/#enquiry'), ('Call ' + PHONE, PHONE_TEL, 'glass')]),
        con('es-sec es-jump',
            con('es-wrap es-wrap--1280', con('es-tabs es-tabs--sticky', con('es-tabs__row', *jump), button('→', '#range', 'es-tabs__more'))),
            tag='section', el_id='range'),
        *sections,
        con('es-sec es-enquire',
            con('es-wrap es-wrap--split es-wrap--enquire',
                con('es-enquire__info es-reveal',
                    heading('SPEC SHEETS & ENQUIRIES', 'div', 'es-kicker es-kicker--red'),
                    heading('Enquire about a machine', 'h2', 'es-h es-h--48'),
                    text('<p>Tell us the machine or application you are interested in and we will send the specification sheet, pricing and lead time. Not sure which machine suits your loads? Describe them and our specialists will recommend one.</p>', 'es-body es-body--16'),
                    con('es-contactlist',
                        con('es-citem', heading('Phone', 'div', 'es-label'), heading(PHONE, 'div', 'es-citem__v', href=PHONE_TEL)),
                        con('es-citem', heading('Hours', 'div', 'es-label'), heading('Mon–Fri 8:00am–5:00pm · Sat by appointment', 'div', 'es-citem__v')))),
                con('es-formcard es-reveal',
                    heading('Send an enquiry', 'h3', 'es-formcard__t'),
                    shortcode('[contact-form-7 id="__CF7_enquiry__" title="Eurostrap enquiry"]', 'es-form'))),
            tag='section', el_id='enquiry'),
    ]


def category_page(c):
    scope('cat-' + c['slug'])
    others = [o for o in CATEGORIES if o is not c][:4]
    return [
        page_hero(c['brand'].upper(), f"{c['name']}<br><span>{c['lead']}</span>", c['intro'], c['photo'],
                  [('Enquire about this machine', '/contact/#enquiry'), ('Call ' + PHONE, PHONE_TEL, 'glass')]),
        con('es-sec es-cat',
            con('es-wrap es-wrap--1280',
                con('es-cat__head es-reveal',
                    con('es-cat__title',
                        heading('THE RANGE', 'div', 'es-kicker es-kicker--red'),
                        heading(f"{c['name']} from Eurostrap", 'h2', 'es-h es-h--48')),
                    con('es-cat__intro',
                        text(f"<p>{c['intro']} Every machine is supplied, installed and supported by our local team, with matched consumables.</p>", 'es-body es-body--16'),
                        text(specs_html(c['specs']), 'es-specs es-specs--wide'))),
                con('es-igrid4', *[item_card(c, it) for it in c['items']])),
            tag='section'),
        con('es-sec es-machines es-machines--related',
            con('es-wrap es-wrap--1280',
                sechead('MORE MACHINES', 'Explore the full range', center=False),
                con('es-rel', *[machine_card(o) for o in others])),
            tag='section'),
        cta_section('Not sure which machine you need?', 'Talk to a specialist. We will match the machine and consumables to your loads and output.', with_image=False),
    ]


# ---------------------------------------------------------------- articles

def articles_page():
    scope('articles')
    return [
        page_hero('INDUSTRY INSIGHTS', 'Articles<br><span>&amp; guides</span>',
                  'News, buying guides and best practice for stretch wrapping, strapping and end-of-line automation.',
                  'warehouse-pallets', []),
        con('es-sec es-news es-news--page',
            con('es-wrap es-wrap--news',
                con('es-news__head es-reveal',
                    heading('LATEST ARTICLES', 'div', 'es-kicker'),
                    heading('Expert packaging advice, machine guides, <span>and industry best practice</span>', 'h2', 'es-h es-h--44')),
                uae_posts(12, 'es-articles es-articles--page', read_more='Read article →')),
            tag='section', el_id='news'),
        cta_section('Have a question about your line?', 'Our specialists can help you choose the right machine, strap or film.', with_image=False),
    ]


# ---------------------------------------------------------------- contact

def contact():
    scope('contact')
    items = [
        ('Phone', PHONE, PHONE_TEL),
        ('Fax', '+61 2 4384 2566', None),
        ('Address', '5 Braemar Dr, Wamberal NSW 2260', 'https://www.google.com/maps/search/?api=1&query=5+Braemar+Dr+Wamberal+NSW+2260'),
        ('Hours', 'Mon–Fri 8:00am–5:00pm<br>Sat by appointment', None),
    ]
    return [
        page_hero('CONTACT', 'Talk to a<br><span>packaging specialist</span>',
                  'Get a quote, book a service visit or ask about consumables. We reply within one business day.',
                  'strapping-warehouse', [('Call ' + PHONE, PHONE_TEL)]),
        con('es-sec es-contact',
            con('es-wrap es-wrap--split es-wrap--contact',
                con('es-formcard es-reveal',
                    heading('ENQUIRY FORM', 'div', 'es-kicker es-kicker--red'),
                    heading('Send an enquiry', 'h2', 'es-h es-h--48'),
                    text('<p>Tell us about your loads, output and the machines you are interested in.</p>', 'es-body es-body--16'),
                    shortcode('[contact-form-7 id="__CF7_enquiry__" title="Eurostrap enquiry"]', 'es-form')),
                con('es-contact__side',
                    *[con('es-ccard es-reveal',
                          heading(k, 'div', 'es-label'),
                          heading(v, 'div', 'es-ccard__v', href=u))
                      for k, v, u in items],
                    con('es-ccard es-ccard--dark es-reveal',
                        heading('Eurostrap Packaging Systems Pty Ltd', 'div', 'es-ccard__v'),
                        heading('ABN 49 105 977 151', 'div', 'es-label')))),
            tag='section', el_id='enquiry'),
        con('es-sec es-mapsec',
            con('es-wrap es-wrap--1280', gmap('5 Braemar Dr, Wamberal NSW 2260', 'es-map es-reveal')),
            tag='section'),
    ]


# ---------------------------------------------------------------- privacy

def privacy():
    scope('privacy')
    body = (
        '<p>Eurostrap Packaging Systems Pty Ltd (ABN 49 105 977 151) respects your privacy. This page explains what information this website collects and how we use it.</p>'
        '<h2>What we collect</h2>'
        '<p>When you send an enquiry we collect the details you enter: your name, company, phone number, email address, the machine or service you are interested in and your message. When you subscribe to specials we collect your email address.</p>'
        '<h2>How we use it</h2>'
        '<p>We use these details only to respond to your enquiry, prepare quotes, arrange service and, if you subscribed, send you specials by email. We do not sell your details.</p>'
        '<h2>Third-party services</h2>'
        '<p>This site uses Google Maps to show our location and Google Fonts for typography. These services may receive your IP address when the page loads.</p>'
        '<h2>Access and contact</h2>'
        '<p>To ask what information we hold about you, correct it or unsubscribe, call (02) 4384 2567 or write to 5 Braemar Dr, Wamberal NSW 2260.</p>'
    )
    return [
        page_hero('LEGAL', 'Privacy<br><span>policy</span>', 'How Eurostrap handles the information you share through this website.', 'warehouse-pallets', []),
        con('es-sec es-legal', con('es-wrap es-wrap--legal', text(body, 'es-legaltext')), tag='section'),
    ]


# ---------------------------------------------------------------- header / footer

def header():
    scope('header')
    return [
        con('es-header',
            uae_logo('es-logo'),
            uae_nav('eurostrap-primary', 'es-nav'),
            con('es-header__ctas',
                btn('Expert help', PHONE_TEL, 'glass', 'es-btn--sm es-btn--help'),
                btn('Get a quote', '/contact/', 'red', 'es-btn--sm'),
                button('Menu', '#menu', 'es-burger')),
            direction='row'),
    ]


def footer():
    scope('footer')
    return [
        con('es-footer',
            con('es-wrap es-wrap--footer',
                con('es-fgrid',
                    con('es-fcol es-fcol--brand',
                        img('eurostrap-logo', 'es-flogo', alt='Eurostrap', href='/'),
                        text('<p>Specialists in all forms of End-Of-Line Load Securement and Packaging Solutions.</p>', 'es-ftext'),
                        text('<p>Exclusive distributor of Atlanta Stretch, Area Packaging and Messersi.</p>', 'es-ftext es-ftext--partners')),
                    con('es-fcol', heading('Solutions', 'div', 'es-fhead'), uae_nav('eurostrap-footer-solutions', 'es-fnav', 'vertical')),
                    con('es-fcol', heading('More', 'div', 'es-fhead'), uae_nav('eurostrap-footer-more', 'es-fnav', 'vertical')),
                    con('es-fcol',
                        heading('Company', 'div', 'es-fhead'),
                        uae_nav('eurostrap-footer-company', 'es-fnav', 'vertical'),
                        text('<p><a href="tel:+61243842567">Tel: +61 2 4384 2567</a><br>Fax: +61 2 4384 2566</p>', 'es-fcontact')),
                    con('es-fcol es-fcol--sub',
                        heading('Get specials by email', 'div', 'es-fsub__t'),
                        shortcode('[contact-form-7 id="__CF7_newsletter__" title="Eurostrap newsletter"]', 'es-newsletter'))),
                con('es-wordmark es-reveal',
                    heading('e', 'div', 'es-wordmark__e'),
                    heading('Eurostrap', 'div', 'es-wordmark__t')),
                text('<p>5 Braemar Dr, Wamberal NSW 2260 <span>·</span> Mon–Fri 8:00am–5:00pm, Sat by appointment <span>·</span> ABN 49 105 977 151 <span>·</span> <a href="/privacy-policy/">Privacy policy</a></p>', 'es-fmeta'),
                uae_copyright('© [hfe_current_year] Eurostrap Packaging Systems Pty Ltd. All rights reserved.', 'es-copy')),
            tag='footer'),
    ]


# ---------------------------------------------------------------- write

def main():
    os.makedirs(OUT, exist_ok=True)
    docs = [
        {'key': 'home', 'type': 'page', 'title': 'Home', 'slug': 'home', 'data': home()},
        {'key': 'about', 'type': 'page', 'title': 'About', 'slug': 'about', 'data': about()},
        {'key': 'machines', 'type': 'page', 'title': 'Machines', 'slug': 'machines', 'data': machines()},
        {'key': 'articles', 'type': 'page', 'title': 'Articles', 'slug': 'articles', 'data': articles_page()},
        {'key': 'contact', 'type': 'page', 'title': 'Contact', 'slug': 'contact', 'data': contact()},
        {'key': 'privacy', 'type': 'page', 'title': 'Privacy Policy', 'slug': 'privacy-policy', 'data': privacy()},
    ]
    for c in CATEGORIES:
        docs.append({'key': 'cat-' + c['slug'], 'type': 'page', 'title': c['name'], 'slug': c['slug'],
                     'parent': 'machines', 'data': category_page(c)})
    docs.append({'key': 'header', 'type': 'header', 'title': 'Eurostrap Header', 'data': header()})
    docs.append({'key': 'footer', 'type': 'footer', 'title': 'Eurostrap Footer', 'data': footer()})

    manifest = {'docs': [], 'articles': ARTICLES,
                'categories': [{'name': c['name'], 'slug': c['slug'], 'items': [i[3] for i in c['items'] if i[3]]} for c in CATEGORIES]}
    for d in docs:
        fn = f"{d['key']}.json"
        with open(os.path.join(OUT, fn), 'w') as f:
            json.dump(d['data'], f, ensure_ascii=False, separators=(',', ':'))
        meta = {k: v for k, v in d.items() if k != 'data'}
        meta['file'] = fn
        manifest['docs'].append(meta)
    with open(os.path.join(OUT, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print('wrote', len(docs), 'documents')


if __name__ == '__main__':
    main()


# ---------------------------------------------------------------- media + theme file lists

ALT = {
    'hero-wrapper-blueprint': 'Automatic ring stretch wrapper on a conveyor line',
    'cta-machines': 'Automatic pallet wrapping line and pallet strapping machine',
    'ec301-robot': 'EC301 robotic palletiser',
    'wrapping-warehouse': 'Automatic stretch wrapping machine on a conveyor line',
    'strapping-warehouse': 'Pallet strapping machine in a warehouse',
    'warehouse-pallets': 'Wrapped pallets in a warehouse',
    'robot-palletiser': 'Robotic palletiser',
    'eurostrap-logo': 'Eurostrap Packaging Systems',
}
PX = 'https://images.pexels.com/photos/{0}/pexels-photo-{0}.jpeg?auto=compress&cs=tinysrgb&w={1}'
PEXELS = {
    'pexels-food': ([PX.format(18631424, 1400)], 'photos-case-packing', 'Food and beverage packing line'),
    'pexels-art-1': ([PX.format(17229385, 1200)], 'wrapping-warehouse', 'Stretch wrapped pallets'),
    'pexels-art-2': ([PX.format(1267338, 1200)], 'strapping-warehouse', 'Strapped load'),
    'pexels-art-3': ([PX.format(18471441, 1200)], 'photos-robotic-palletising', 'Robotic palletising cell'),
}


def write_lists():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets = {}
    adir = os.path.join(root, 'assets')
    for fn in sorted(os.listdir(adir)):
        key = fn.rsplit('.', 1)[0]
        name = key.split('-', 1)[-1].replace('-', ' ').capitalize() if key.startswith(('equipment-', 'photos-', 'suppliers-')) else key.replace('-', ' ').capitalize()
        assets[key] = {'filename': 'eurostrap-' + fn, 'alt': ALT.get(key, name), 'sources': ['assets/' + fn]}
    for key, (urls, fallback, alt) in PEXELS.items():
        fb = assets[fallback]['sources'][0]
        assets[key] = {'filename': f'eurostrap-{key}.jpg', 'alt': alt, 'sources': urls + [fb]}
    with open(os.path.join(OUT, 'assets.json'), 'w') as f:
        json.dump(assets, f, indent=1)
    tdir = os.path.join(root, 'theme', 'eurostrap-child')
    files = []
    for dp, _, fns in os.walk(tdir):
        for fn in fns:
            files.append(os.path.relpath(os.path.join(dp, fn), tdir))
    with open(os.path.join(root, 'theme', 'files.txt'), 'w') as f:
        f.write('\n'.join(sorted(files)) + '\n')
    print('assets', len(assets), 'theme files', len(files))


write_lists()
