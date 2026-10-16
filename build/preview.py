"""Local preview: renders build/out/*.json into approximate Elementor/UAE markup so the
child-theme CSS/JS can be checked in a browser without WordPress.

python3 build/preview.py  -> build/preview/<page>.html
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'build', 'out')
PREV = os.path.join(ROOT, 'build', 'preview')
ASSETS = json.load(open(os.path.join(OUT, 'assets.json')))
MANIFEST = json.load(open(os.path.join(OUT, 'manifest.json')))

SHIM = """
.e-con{--display:flex;--flex-direction:column;--width:100%;--gap:20px;display:var(--display);flex-direction:var(--flex-direction);
 position:relative;width:var(--width);gap:var(--gap);padding:var(--padding-top,0) var(--padding-right,0) var(--padding-bottom,0) var(--padding-left,0);
 flex-wrap:var(--flex-wrap,nowrap)}
.e-con>.elementor-widget{max-width:100%}
.e-con[data-dir=row]{--flex-direction:row}
.elementor-widget{position:relative}
.elementor-widget-image{text-align:center}
.elementor-widget-image img{vertical-align:middle;display:inline-block;max-width:100%;height:auto}
.elementor-heading-title{padding:0;margin:0;line-height:1}
.elementor-button{display:inline-block;line-height:1;background-color:#69727d;font-size:15px;padding:12px 24px;border-radius:3px;color:#fff;fill:#fff;text-align:center;transition:all .3s}
.elementor-button-wrapper{display:block}
.hfe-nav-menu{list-style:none;margin:0;padding:0}
.hfe-nav-menu li{position:relative}
.hfe-posts-grid{display:grid;grid-template-columns:repeat(3,1fr)}
.hfe-post-card{background:#F6F6F6}
.hfe-post-content{padding:20px}
body{margin:0}
h1,h2,h3{font-weight:500}
p{margin-block-end:.9rem}
"""

MENU = [
    ('Home', '#', []), ('About', '#', []),
    ('Machines', '#', [
        ('Wrapping Machines', '#', [('Automatic In-Line Stretch Wrapping Machines', '#'), ('Semi-Automatic Stretch Wrapping Machines', '#'), ('Self-Propelled Semi-automatic Stretch Wrapping Machines', '#'), ('Horizontal Stretch Machines', '#')], 'es-mega-feature'),
        ('Solutions', '#', [('Bag Filling', '#'), ('Palletisers', '#'), ('Consultation & Design', '#'), ('Consumables', '#'), ('Robotic Palletisers', '#')], 'es-mega-label'),
        ('More Machines', '#', [('Strapping', '#'), ('Carton Sealing', '#'), ('Shrink/Stretch Hooding', '#'), ('Case Packing', '#')], 'es-mega-label'),
    ]),
    ('Articles', '#', []), ('Contact', '#', []),
]


def asset_url(key):
    a = ASSETS.get(key)
    if not a:
        return ''
    src = a['sources'][-1]
    return '../../' + src


def nav_html(slug, layout):
    if slug == 'eurostrap-primary':
        items = ''
        for t, u, subs in MENU:
            if subs:
                inner = ''
                for st, su, ss, cls in subs:
                    li3 = ''.join(f'<li class="menu-item"><a class="hfe-sub-menu-item" href="{u3}">{html.escape(t3)}</a></li>' for t3, u3 in ss)
                    inner += (f'<li class="menu-item menu-item-has-children {cls} hfe-has-submenu"><div class="hfe-has-submenu-container"><a class="hfe-sub-menu-item" href="{su}">{html.escape(st)}'
                              f"<span class='hfe-menu-toggle sub-arrow hfe-menu-child-1'><i class='fa'></i></span></a></div><ul class=\"sub-menu\">{li3}</ul></li>")
                items += (f'<li class="menu-item menu-item-has-children parent es-mega hfe-has-submenu"><div class="hfe-has-submenu-container"><a class="hfe-menu-item" href="{u}">{t}'
                          f"<span class='hfe-menu-toggle sub-arrow hfe-menu-child-0'><i class='fa'></i></span></a></div><ul class=\"sub-menu\">{inner}</ul></li>")
            else:
                cur = ' current-menu-item' if t == 'Home' else ''
                items += f'<li class="menu-item parent{cur}"><a class="hfe-menu-item" href="{u}">{t}</a></li>'
    else:
        names = {'eurostrap-footer-solutions': ['Wrapping Machines', 'Bag Filling', 'Palletisers', 'Robotic Palletisers', 'Strapping'],
                 'eurostrap-footer-more': ['Carton Sealing', 'Shrink/Stretch Hooding', 'Case Packing', 'Consumables', 'Consultation & Design'],
                 'eurostrap-footer-company': ['About', 'Articles', 'Contact']}[slug]
        items = ''.join(f'<li class="menu-item parent"><a class="hfe-menu-item" href="#">{html.escape(n)}</a></li>' for n in names)
    return (f'<div class="hfe-nav-menu hfe-layout-{layout} hfe-nav-menu-layout {layout}"><div role="button" class="hfe-nav-menu__toggle elementor-clickable"></div>'
            f'<nav class="hfe-nav-menu__layout-{layout} hfe-nav-menu__submenu-arrow"><ul class="hfe-nav-menu">{items}</ul></nav></div>')


def posts_html(n):
    cards = ''
    for a in MANIFEST['articles'][:min(n, 3)]:
        img = asset_url(a['img'])
        cards += (f'<article class="hfe-post-card"><div class="hfe-post-image"><a href="#"><img src="{img}" alt=""></a><span class="es-post-tag">{a["cat"]}</span></div>'
                  f'<div class="hfe-post-content"><h3 class="hfe-post-title"><a href="#">{a["title"]}</a></h3><div class="hfe-post-meta"><span class="hfe-post-date">5 min read</span></div></div></article>')
    return f'<div class="hfe-posts-grid">{cards}</div>'


def cf7(code):
    if 'newsletter' in code:
        return '<div class="wpcf7"><form class="wpcf7-form"><div class="es-nl"><span class="wpcf7-form-control-wrap"><input type="email" placeholder="Enter your email..."></span><input type="submit" value="Subscribe" class="wpcf7-submit"></div></form></div>'
    opts = ''.join(f'<option>{c["name"]}</option>' for c in MANIFEST['categories'])
    f = lambda lab, inp, full='': f'<label class="es-field {full}"><span>{lab}</span><span class="wpcf7-form-control-wrap">{inp}</span></label>'
    return ('<div class="wpcf7"><form class="wpcf7-form"><div class="es-formgrid">' + f('Name *', '<input type="text">') + f('Company', '<input type="text">') +
            f('Phone *', '<input type="tel">') + f('Email *', '<input type="email">') +
            f('Machine interest', f'<select><option>Select a machine or service</option>{opts}</select>', 'es-field--full') +
            f('Message', '<textarea placeholder="Tell us about your loads, output and timing"></textarea>', 'es-field--full') +
            '</div><div class="es-formfoot"><input type="submit" value="Send enquiry" class="wpcf7-submit"><span class="es-formfoot__note">We reply within one business day.</span></div></form></div>')


def render(e):
    if e['elType'] == 'container':
        s = e['settings']
        tag = s.get('html_tag') or 'div'
        attrs = f' class="e-con e-con-full e-flex {s.get("css_classes", "")}"'
        if s.get('flex_direction') == 'row':
            attrs += ' data-dir="row"'
        if s.get('_element_id'):
            attrs += f' id="{s["_element_id"]}"'
        if tag == 'a':
            attrs += f' href="{s["link"]["url"]}"'
        inner = ''.join(render(c) for c in e['elements'])
        return f'<{tag}{attrs}>{inner}</{tag}>'
    w = e['widgetType']
    s = e['settings']
    cls = s.get('_css_classes', '')
    body = ''
    if w == 'heading':
        t = s['title']
        if s.get('link'):
            t = f'<a href="{s["link"]["url"]}">{t}</a>'
        tag = s.get('header_size', 'h2')
        body = f'<{tag} class="elementor-heading-title elementor-size-default">{t}</{tag}>'
    elif w == 'text-editor':
        body = s['editor']
    elif w == 'image':
        key = s['image']['url'][6:-2]
        img = f'<img src="{asset_url(key)}" alt="{html.escape(s["image"].get("alt", ""))}">'
        if s.get('link'):
            img = f'<a href="{s["link"]["url"]}">{img}</a>'
        body = img
    elif w == 'button':
        body = (f'<a class="elementor-button elementor-button-link elementor-size-sm" href="{s["link"]["url"]}">'
                f'<span class="elementor-button-content-wrapper"><span class="elementor-button-text">{s["text"]}</span></span></a>')
    elif w == 'shortcode':
        body = f'<div class="elementor-shortcode">{cf7(s["shortcode"])}</div>'
    elif w == 'google_maps':
        body = '<div class="elementor-custom-embed"><iframe style="background:#ddd" src="about:blank"></iframe></div>'
    elif w == 'site-logo':
        body = f'<div class="hfe-site-logo"><a href="#"><div class="hfe-site-logo-set"><div class="hfe-site-logo-container"><img class="hfe-site-logo-img" src="{asset_url("eurostrap-logo")}" alt=""></div></div></a></div>'
    elif w == 'navigation-menu':
        body = nav_html(s['menu'], s['layout'])
    elif w == 'hfe-basic-posts':
        body = posts_html(s['posts_per_page'])
    elif w == 'copyright':
        body = f'<div class="hfe-copyright-wrapper"><span>{s["shortcode"].replace("[hfe_current_year]", "2026")}</span></div>'
    if w in ('site-logo', 'navigation-menu', 'hfe-basic-posts', 'copyright'):
        body = f'<div class="elementor-widget-container">{body}</div>'
    return f'<div class="elementor-element elementor-widget elementor-widget-{w} {cls}">{body}</div>'


def page(key):
    data = json.load(open(os.path.join(OUT, f'{key}.json')))
    header = json.load(open(os.path.join(OUT, 'header.json')))
    footer = json.load(open(os.path.join(OUT, 'footer.json')))
    assets = {k: asset_url(k) for k in ASSETS}
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{SHIM}</style><link rel="stylesheet" href="../../theme/eurostrap-child/assets/css/eurostrap.css"></head>
<body class="es-site">
<header id="masthead">{''.join(render(e) for e in header)}</header>
<div class="elementor">{''.join(render(e) for e in data)}</div>
<footer id="colophon">{''.join(render(e) for e in footer)}</footer>
<script>window.ESData={{home:'/',assets:{json.dumps(assets)},phone:'+61243842567'}};</script>
<script src="../../theme/eurostrap-child/assets/js/eurostrap.js"></script></body></html>"""


if __name__ == '__main__':
    os.makedirs(PREV, exist_ok=True)
    for d in MANIFEST['docs']:
        if d['type'] == 'page':
            with open(os.path.join(PREV, d['key'] + '.html'), 'w') as f:
                f.write(page(d['key']))
    print('preview written to', PREV)
