"""Tiny helpers that emit Elementor (legacy container) JSON.

Every element carries a CSS class from the Eurostrap child theme; layout, type
sizes, colours and motion are defined there so the content stays editable in the
Elementor panel. Image URLs/IDs and form IDs are placeholders the installer
swaps for real media-library values.
"""
import hashlib
import itertools

_counter = itertools.count()
_scope = ['es']


def scope(name):
    """Reset the ID seed per document so IDs are stable across rebuilds."""
    global _counter
    _counter = itertools.count()
    _scope[0] = name


def eid():
    n = next(_counter)
    return hashlib.md5(f'{_scope[0]}-{n}'.encode()).hexdigest()[:7]


ZERO = {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}
GAP0 = {'column': '0', 'row': '0', 'isLinked': True, 'unit': 'px', 'size': 0}


def link(url):
    ext = 'on' if url.startswith('http') else ''
    return {'url': url, 'is_external': ext, 'nofollow': '', 'custom_attributes': ''}


def con(cls, *children, tag=None, href=None, el_id=None, direction='column'):
    s = {
        'content_width': 'full',
        'flex_direction': direction,
        'padding': dict(ZERO),
        'flex_gap': dict(GAP0),
        'css_classes': cls,
    }
    if href:
        s['html_tag'] = 'a'
        s['link'] = link(href)
    elif tag:
        s['html_tag'] = tag
    if el_id:
        s['_element_id'] = el_id
    return {'id': eid(), 'elType': 'container', 'isInner': False,
            'settings': s, 'elements': [c for c in children if c]}


def widget(wtype, settings, cls=''):
    s = dict(settings)
    if cls:
        s['_css_classes'] = cls
    return {'id': eid(), 'elType': 'widget', 'widgetType': wtype,
            'settings': s, 'elements': []}


def heading(text, tag='h2', cls='', href=None):
    s = {'title': text, 'header_size': tag}
    if href:
        s['link'] = link(href)
    return widget('heading', s, cls)


def text(html, cls=''):
    return widget('text-editor', {'editor': html}, cls)


def img(key, cls='', alt='', href=None, size='full'):
    s = {
        'image': {'url': f'__URL_{key}__', 'id': f'__ID_{key}__', 'alt': alt, 'source': 'library', 'size': ''},
        'image_size': size,
    }
    if href:
        s['link_to'] = 'custom'
        s['link'] = link(href)
    return widget('image', s, cls)


def button(label, url, cls=''):
    return widget('button', {'text': label, 'link': link(url), 'size': 'sm'}, cls)


def shortcode(code, cls=''):
    return widget('shortcode', {'shortcode': code}, cls)


def gmap(address, cls='', zoom=15, height=440):
    return widget('google_maps', {
        'address': address,
        'zoom': {'unit': 'px', 'size': zoom, 'sizes': []},
        'height': {'unit': 'px', 'size': height, 'sizes': []},
    }, cls)


# --- UAE (Header Footer Elementor) widgets -------------------------------

def uae_logo(cls=''):
    return widget('site-logo', {
        'site_logo_fallback': 'no',
        'site_logo_size_size': 'full',
        'align': 'left',
        'link_to': 'default',
    }, cls)


def uae_nav(menu_slug, cls='', layout='horizontal'):
    return widget('navigation-menu', {
        'menu': menu_slug,
        'layout': layout,
        'dropdown': 'none',
        'navmenu_align': 'left' if layout == 'vertical' else 'center',
        'submenu_icon': 'arrow',
        'pointer': 'none',
        'menu_last_item': 'none',
    }, cls)


def uae_posts(count, cls=''):
    return widget('hfe-basic-posts', {
        'posts_per_page': count,
        'columns': '3',
        'columns_tablet': '2',
        'columns_mobile': '1',
        'orderby': 'date',
        'order': 'desc',
        'show_image': 'yes',
        'image_size': 'large',
        'show_title': 'yes',
        'title_tag': 'h3',
        'show_meta': 'yes',
        'show_date': 'yes',
        'show_author': '',
        'show_comments': '',
        'meta_separator': '',
        'show_excerpt': '',
        'show_read_more': '',
    }, cls)


def uae_copyright(textline, cls=''):
    return widget('copyright', {'shortcode': textline}, cls)
