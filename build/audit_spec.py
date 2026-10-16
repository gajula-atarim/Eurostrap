import asyncio, json, sys
from playwright.async_api import async_playwright
# (label, css selector, {prop: expected}) — values from "03 Eurostrap Home.dc.html"
H='.elementor-heading-title'
SPEC = [
 ('header box', '.es-header', {'top':'18px','border-top-left-radius':'16px','padding-top':'8px','background-color':'rgba(20, 20, 20, 0.28)','position':'absolute','width':'1280px'}),
 ('logo plate', '.es-logo .hfe-site-logo-set', {'background-color':'rgb(255, 255, 255)','border-top-left-radius':'10px','padding-top':'8px','padding-left':'16px'}),
 ('logo img', '.es-logo img', {'height':'52px'}),
 ('nav ul', '.es-nav ul.hfe-nav-menu', {'column-gap':'36px'}),
 ('nav link', '.es-nav .hfe-nav-menu > li:nth-child(2) > a', {'font-size':'14px','font-weight':'500','color':'rgba(255, 255, 255, 0.75)','padding-top':'14px'}),
 ('nav home', '.es-nav .hfe-nav-menu > li:first-child > a', {'color':'rgb(255, 255, 255)'}),
 ('cta group', '.es-header__ctas', {'column-gap':'22px','padding-left':'8px'}),
 ('header quote btn', '.es-header .es-btn--red .elementor-button', {'background-color':'rgb(217, 48, 44)','padding-top':'11px','padding-left':'26px','font-size':'14px','font-weight':'500'}),
 ('header help btn', '.es-btn--help .elementor-button', {'background-color':'rgba(255, 255, 255, 0.16)','padding-left':'24px'}),
 ('hero', '.es-hero--home', {'height':'640px','background-color':'rgb(20, 20, 20)'}),
 ('hero img', '.es-hero--home .es-hero__img img', {'object-fit':'cover','object-position':'100% 60%'}),
 ('hero outline', '.es-hero__outline '+H, {'font-family':'"Bebas Neue", "Arial Narrow", sans-serif','font-size':'180px','line-height':'144px','-webkit-text-stroke-width':'1.5px'}),
 ('hero content', '.es-hero--home .es-hero__content', {'max-width':'520px','row-gap':'16px'}),
 ('eyebrow', '.es-hero--home .es-eyebrow '+H, {'font-size':'13px','font-weight':'500','letter-spacing':'2.34px','color':'rgb(227, 227, 227)'}),
 ('h1', '.es-hero--home .es-hero__title '+H, {'font-size':'86px','line-height':'75.68px','white-space':'nowrap','text-transform':'uppercase','color':'rgb(255, 255, 255)'}),
 ('h1 span', '.es-hero--home .es-hero__title '+H+' span', {'color':'rgb(217, 48, 44)'}),
 ('hero lead', '.es-hero--home .es-hero__lead', {'max-width':'440px'}),
 ('hero lead p', '.es-hero--home .es-hero__lead p', {'font-size':'18px','font-weight':'300','line-height':'26.1px','color':'rgb(232, 232, 232)'}),
 ('hero ctas', '.es-hero--home .es-hero__ctas', {'column-gap':'28px','margin-top':'8px','padding-top':'6px'}),
 ('hero btn', '.es-hero--home .es-btn .elementor-button', {'padding-top':'14px','padding-left':'34px','font-size':'14px'}),
 ('explore link', '.es-underline .elementor-button', {'font-size':'14px','padding-bottom':'4px','border-bottom-color':'rgba(255, 255, 255, 0.4)'}),
 ('machines wrap', '.es-wrap--machines', {'max-width':'1120px','padding-top':'110px','padding-left':'32px','row-gap':'48px'}),
 ('tab', '.es-tab:not(.es-tab--active) .elementor-button', {'padding-top':'14px','padding-left':'20px','font-size':'14px','font-weight':'600','border-top-left-radius':'4px'}),
 ('tab active', '.es-tab--active .elementor-button', {'background-color':'rgb(217, 48, 44)'}),
 ('tabs more', '.es-tabs__more .elementor-button', {'width':'58px','height':'48px'}),
 ('mgrid', '.es-mgrid', {'display':'grid','column-gap':'22px'}),
 ('mgrid h2', '.es-mgrid__intro '+H, {'font-size':'46px','line-height':'46px'}),
 ('mgrid p', '.es-mgrid__intro p', {'font-size':'15px','color':'rgb(90, 90, 90)'}),
 ('mcard', '.es-mcard.is-shown', {'border-top-left-radius':'6px','border-top-color':'rgb(236, 236, 236)'}),
 ('mcard media', '.es-mcard.is-shown .es-mcard__media', {'height':'250px','background-color':'rgb(235, 235, 235)','padding-top':'22px'}),
 ('mcard body', '.es-mcard.is-shown .es-mcard__body', {'padding-top':'18px','row-gap':'11px'}),
 ('mcard title', '.es-mcard.is-shown .es-mcard__title '+H, {'font-size':'20px'}),
 ('spec row', '.es-mcard.is-shown .es-specs p', {'font-size':'13px'}),
 ('spec row gap', '.es-mcard.is-shown .es-specs p + p', {'margin-top':'6px'}),
 ('explore title', '.es-explore__title '+H, {'font-size':'22px','font-weight':'600'}),
 ('sq btn', '.es-sq .elementor-button', {'width':'48px','height':'48px'}),
 ('view all', '.es-btn-rect .elementor-button', {'padding-top':'14px','padding-left':'22px','font-weight':'700'}),
 ('industries', '.es-industries', {'background-color':'rgb(244, 244, 244)'}),
 ('industries wrap', '.es-wrap--industries', {'padding-top':'110px','row-gap':'44px'}),
 ('ind h2', '.es-industries .es-h--48 '+H, {'font-size':'48px'}),
 ('ind lead', '.es-industries .es-lead p', {'font-size':'16px'}),
 ('igrid', '.es-igrid', {'grid-template-rows':'240px 240px','column-gap':'14px'}),
 ('tile', '.es-tile--1', {'border-top-left-radius':'16px'}),
 ('tile label', '.es-tile__label', {'top':'14px','padding-top':'12px','padding-left':'14px','border-top-left-radius':'12px'}),
 ('tile t', '.es-tile__t '+H, {'font-size':'14px'}),
 ('tile d', '.es-tile__d p', {'font-size':'12px'}),
 ('tile arrow', '.es-tile__arrow '+H, {'width':'40px','height':'40px','border-top-left-radius':'10px'}),
 ('trust wrap', '.es-wrap--trust', {'padding-top':'120px','padding-bottom':'110px','row-gap':'64px'}),
 ('trust h2', '.es-trust__title '+H, {'font-size':'150px','line-height':'126px','column-gap':'28px'}),
 ('trust robot', '.es-trust__robot', {'width':'420px','height':'400px'}),
 ('trust lead', '.es-trust__lead '+H, {'font-size':'34px','font-weight':'300'}),
 ('trust copy', '.es-trust__copy', {'max-width':'500px'}),
 ('trust copy p', '.es-trust__copy p', {'font-size':'15px','color':'rgb(122, 122, 122)'}),
 ('trust media', '.es-trust__media', {'border-top-left-radius':'24px'}),
 ('stats', '.es-stats', {'max-width':'1000px','column-gap':'64px'}),
 ('stat v', '.es-stat__v '+H, {'font-size':'64px','font-weight':'400'}),
 ('stat l', '.es-stat__l p', {'font-size':'13px','color':'rgb(107, 107, 107)'}),
 ('reviews', '.es-reviews', {'background-color':'rgb(20, 20, 20)'}),
 ('reviews wrap', '.es-wrap--reviews', {'padding-top':'120px','row-gap':'48px'}),
 ('pill', '.es-pill '+H, {'font-size':'12px','font-weight':'600','padding-top':'7px','padding-left':'14px'}),
 ('review', '.es-review', {'padding-top':'28px','border-top-left-radius':'20px','row-gap':'18px'}),
 ('review q', '.es-review__q p', {'font-size':'17px'}),
 ('stars', '.es-review__stars '+H, {'font-size':'16px','color':'rgb(255, 90, 79)'}),
 ('avatar', '.es-review__av '+H, {'width':'40px','font-size':'14px','font-weight':'800'}),
 ('news wrap', '.es-wrap--news', {'padding-top':'110px','row-gap':'48px'}),
 ('news h2', '.es-news .es-h--44 '+H, {'font-size':'44px'}),
 ('news kicker', '.es-news .es-kicker '+H, {'font-size':'12px','letter-spacing':'1.44px'}),
 ('posts grid', '.es-articles .hfe-posts-grid', {'column-gap':'24px'}),
 ('post card', '.es-articles .hfe-post-card', {'background-color':'rgba(0, 0, 0, 0)','row-gap':'14px'}),
 ('post image', '.es-articles .hfe-post-image', {'height':'380px','border-top-left-radius':'16px'}),
 ('post title', '.es-articles .hfe-post-title', {'font-size':'18px','font-weight':'600'}),
 ('post meta', '.es-articles .hfe-post-meta', {'font-size':'13px'}),
 ('post tag', '.es-post-tag', {'font-size':'11px','font-weight':'700','padding-top':'7px','padding-left':'12px'}),
 ('suppliers wrap', '.es-wrap--suppliers', {'padding-top':'72px','padding-bottom':'64px','row-gap':'36px'}),
 ('suppliers kicker', '.es-suppliers .es-kicker '+H, {'color':'rgb(217, 48, 44)','letter-spacing':'2.16px'}),
 ('logos', '.es-logos', {'column-gap':'16px'}),
 ('logo tile', '.es-logo-tile', {'height':'110px','border-top-left-radius':'14px','padding-top':'18px'}),
 ('logo img', '.es-logo-tile img', {'max-height':'60px'}),
 ('cta wrap', '.es-wrap--cta', {'padding-top':'120px','row-gap':'20px'}),
 ('cta h2', '.es-cta .es-h--60 '+H, {'font-size':'60px','line-height':'55.2px'}),
 ('cta p', '.es-cta .es-lead p', {'font-size':'16px'}),
 ('cta lead', '.es-cta .es-lead', {'max-width':'520px'}),
 ('btnrow', '.es-btnrow', {'column-gap':'28px'}),
 ('cta img', '.es-cta__img', {'margin-top':'-40px','margin-bottom':'-14px'}),
 ('footer', '.es-footer', {'background-color':'rgb(10, 10, 10)'}),
 ('footer wrap', '.es-wrap--footer', {'padding-top':'80px','padding-bottom':'28px','row-gap':'64px'}),
 ('fgrid', '.es-fgrid', {'column-gap':'40px'}),
 ('flogo', '.es-flogo img', {'height':'60px'}),
 ('fnav link', '.es-fnav a.hfe-menu-item', {'font-size':'14px','color':'rgb(227, 227, 227)','padding-top':'0px'}),
 ('fhead', '.es-fhead '+H, {'font-size':'12px','color':'rgb(107, 107, 107)'}),
 ('newsletter', '.es-nl', {'padding-top':'5px','border-top-left-radius':'12px'}),
 ('subscribe', '.es-newsletter input[type=submit]', {'background-color':'rgb(217, 48, 44)','font-size':'13px','font-weight':'700','border-top-left-radius':'8px'}),
 ('wordmark e', '.es-wordmark__e '+H, {'width':'150px','height':'150px','font-size':'140px','border-top-left-radius':'24px'}),
 ('wordmark', '.es-wordmark__t '+H, {'font-size':'200px'}),
 ('copyright', '.es-copy .hfe-copyright-wrapper', {'font-size':'12px'}),
]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        pg = await b.new_page(viewport={'width':1440,'height':900}, reduced_motion='reduce')
        await pg.goto('file://'+sys.argv[1]); await pg.wait_for_timeout(2500)
        res = await pg.evaluate('''(spec)=>spec.map(([l,s,exp])=>{const e=document.querySelector(s); if(!e) return [l,s,'MISSING',null];
          const cs=getComputedStyle(e); const out={}; for(const k in exp){ let v=k==='width'||k==='height'?Math.round(e.getBoundingClientRect()[k])+'px':cs.getPropertyValue(k); out[k]=[exp[k],v]; } return [l,s,'ok',out];})''', SPEC)
        bad=0
        for l,s,st,out in res:
            if st!='ok': print('MISSING', l, s); bad+=1; continue
            for k,(e,v) in out.items():
                norm=lambda x: x.replace(' ','')
                if norm(e)!=norm(v):
                    try:
                        if abs(float(e.rstrip('px'))-float(v.rstrip('px')))<0.6: continue
                    except: pass
                    print(f'DIFF {l:18} {k:24} expected {e:28} got {v}'); bad+=1
        print('checked', sum(len(x[3] or {}) for x in res), 'props; mismatches', bad)
        sw = await pg.evaluate('document.documentElement.scrollWidth'); print('scrollWidth', sw)
        await b.close()
asyncio.run(main())
