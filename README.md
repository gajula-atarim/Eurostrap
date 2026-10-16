# Eurostrap website build

WordPress build for https://eurostrap.wsdfy.com/ from the Eurostrap brand kit.

- `theme/eurostrap-child/`: Hello Elementor child theme (brand tokens, typography, responsive rules, motion).
- `build/`: generator that writes every page, plus the UAE header and footer, as native Elementor JSON (`python3 build/build.py`). `preview.py` renders a local approximation for visual checks.
- `assets/`: web-optimised brand-kit images, sideloaded into the media library.
- `installer/install.php`: idempotent installer run on the server (plugins, child theme, media, Contact Form 7 forms, pages, menus, UAE templates, articles, settings).

Stack: Hello Elementor + Elementor, Ultimate Addons for Elementor (header/footer, nav menus, posts, copyright), Contact Form 7.
