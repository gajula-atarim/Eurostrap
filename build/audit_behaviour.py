import asyncio, sys
from playwright.async_api import async_playwright
URL='file://'+sys.argv[1]
ok=[];bad=[]
def check(name,cond,detail=''):
    (ok if cond else bad).append(f'{name} {detail}')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        pg=await b.new_page(viewport={'width':1440,'height':900})
        await pg.goto(URL); await pg.wait_for_timeout(600)
        r=await pg.evaluate('''()=>{const a=[...document.querySelectorAll('.es-hero--home .es-anim-hero')].map(e=>[getComputedStyle(e).animationName,e.style.animationDelay]);
          const o=getComputedStyle(document.querySelector('.es-hero__outline .elementor-heading-title'));
          const k=getComputedStyle(document.querySelector('.es-kenburns'));
          return {a, o:[o.animationName,o.animationDuration], k:[k.animationName,k.animationDuration], motion:document.body.classList.contains('es-motion'),
           lines:document.querySelectorAll('.es-btn__line').length, btns:document.querySelectorAll('.elementor-widget.es-btn').length,
           ell:!!document.querySelector('.es-on .es-ellipse'), hidden:document.querySelectorAll('.es-hidden').length, reveal:document.querySelectorAll('.es-reveal').length}}''')
        check('motion class',r['motion'])
        check('hero entrance stagger',[x[0] for x in r['a']]==['es-heroIn']*4 and [x[1] for x in r['a']]==['150ms','270ms','390ms','510ms'],str(r['a']))
        check('outline letter-spacing anim',r['o']==['es-outlineIn','1.8s'],str(r['o']))
        check('ken burns 9s',r['k']==['es-kenburns','9s'],str(r['k']))
        check('button strokes (2 per button)',r['lines']==2*r['btns'],f"{r['lines']} lines / {r['btns']} buttons")
        check('ellipse injected',r['ell'])
        check('below-fold reveals hidden',r['hidden']>10,f"{r['hidden']}/{r['reveal']}")
        # rotator
        s1=await pg.evaluate("[...document.querySelectorAll('.es-mcard.is-shown .es-mcard__title')].map(e=>e.textContent.trim())")
        on1=await pg.evaluate("document.querySelectorAll('.es-tab.es-tab--on').length")
        dots=await pg.evaluate("[...document.querySelectorAll('.es-dots span')].map(d=>d.className)")
        await pg.wait_for_timeout(4800)
        s2=await pg.evaluate("[...document.querySelectorAll('.es-mcard.is-shown .es-mcard__title')].map(e=>e.textContent.trim())")
        check('rotator shows 4 cards',len(s1)==4,str(s1)); check('rotator auto-advances by 4 after 4s',s2!=s1 and len(s2)==4,str(s2))
        check('4 category tabs outlined red',on1==4,str(on1)); check('3 page dots, first active',len(dots)==3 and dots[0]=='is-on',str(dots))
        await pg.click('.es-sq--next a'); await pg.wait_for_timeout(300)
        s3=await pg.evaluate("[...document.querySelectorAll('.es-mcard.is-shown .es-mcard__title')].map(e=>e.textContent.trim())")
        check('next arrow advances',s3!=s2,str(s3))
        await pg.click('.es-sq--prev a'); await pg.wait_for_timeout(300)
        s4=await pg.evaluate("[...document.querySelectorAll('.es-mcard.is-shown .es-mcard__title')].map(e=>e.textContent.trim())")
        check('prev arrow goes back',s4==s2,str(s4))
        # hovering the arrows must not stop autoplay
        await pg.hover('.es-sq--prev a'); await pg.wait_for_timeout(4800)
        s4b=await pg.evaluate("[...document.querySelectorAll('.es-mcard.is-shown .es-mcard__title')].map(e=>e.textContent.trim())")
        check('autoplay continues while hovering arrows',s4b!=s4,str(s4b))
        s4=s4b
        # hover pause on a card
        await pg.hover('.es-mcard.is-shown'); await pg.wait_for_timeout(4800)
        s5=await pg.evaluate("[...document.querySelectorAll('.es-mcard.is-shown .es-mcard__title')].map(e=>e.textContent.trim())")
        check('rotator pauses on hover',s5==s4)
        t=await pg.evaluate("document.querySelector('.es-mcard.is-shown').style.transform")
        check('card tilt on mousemove','perspective(900px)' in t,t)
        # mega menu
        await pg.mouse.move(10,10); await pg.wait_for_timeout(300)
        await pg.hover('.es-nav li.es-mega > .hfe-has-submenu-container > a, .es-nav li.es-mega > a'); await pg.wait_for_timeout(500)
        m=await pg.evaluate('''()=>{const p=document.querySelector('.es-mega-panel');return p?{open:p.classList.contains('is-open'),cols:p.querySelectorAll('.es-mega-col').length,links:p.querySelectorAll('.es-mega-link').length,feat:p.querySelector('.es-mega-col__feature')?.textContent.trim(),labels:[...p.querySelectorAll('.es-mega-col__label')].map(x=>x.textContent),promo:!!p.querySelector('.es-mega-promo img'),op:getComputedStyle(p).opacity, caret:document.querySelector('.es-nav li.es-mega').classList.contains('es-mega-open')}:null}''')
        check('mega menu opens on hover',m and m['open'],str(m))
        check('mega layout: feature + 2 label cols + promo',m and m['cols']==3 and m['labels']==['Solutions','More Machines'] and m['promo'] and m['links']==13,str(m))
        await pg.mouse.move(700,800); await pg.wait_for_timeout(600)
        mc=await pg.evaluate("document.querySelector('.es-mega-panel').classList.contains('is-open')")
        check('mega menu closes on leave',not mc)
        # scroll: header solid, parallax, reveal
        px0=await pg.evaluate("document.querySelector('.es-trust__robot').style.transform")
        await pg.evaluate("window.scrollTo(0, document.querySelector('.es-trust').offsetTop-200)"); await pg.wait_for_timeout(1200)
        r2=await pg.evaluate('''()=>({solid:document.querySelector('.es-header').classList.contains('es-header--solid'),px:document.querySelector('.es-trust__robot').style.transform,
           title:[...document.querySelector('.es-trust__title').classList], anim:getComputedStyle(document.querySelector('.es-trust__title')).animationName,
           ell:getComputedStyle(document.querySelector('.es-ellipse ellipse')).animationName})''')
        check('header turns solid after 640px',r2['solid'])
        check('parallax moves on scroll',r2['px']!=px0 and 'translate3d' in r2['px'],f"{px0} -> {r2['px']}")
        check('reveal animation fires',r2['anim']=='es-revealIn' and 'es-in' in r2['title'],str(r2['anim']))
        check('ellipse draws on reveal',r2['ell']=='es-draw',r2['ell'])
        await pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); await pg.wait_for_timeout(1500)
        left=await pg.evaluate("document.querySelectorAll('.es-hidden').length")
        check('all reveals shown after full scroll',left==0,str(left))
        # mobile drawer
        m=await b.new_page(viewport={'width':390,'height':844})
        await m.goto(URL); await m.wait_for_timeout(600)
        v=await m.evaluate('''()=>({nav:getComputedStyle(document.querySelector('.es-nav')).display, burger:getComputedStyle(document.querySelector('.es-burger')).display, logo:Math.round(document.querySelector('.es-logo img').getBoundingClientRect().width), outline:getComputedStyle(document.querySelector('.es-hero__outline')).display})''')
        check('mobile: nav hidden, burger shown',v['nav']=='none' and v['burger']!='none',str(v))
        check('mobile logo >= 160px wide (brand kit)',v['logo']>=160,str(v['logo']))
        await m.click('.es-burger a'); await m.wait_for_timeout(500)
        d=await m.evaluate('''()=>({open:document.body.classList.contains('es-menu-open'), vis:getComputedStyle(document.querySelector('.es-drawer')).visibility, items:[...document.querySelectorAll('.es-drawer > nav > ul > li > .es-drawer__row > a')].map(a=>a.textContent)})''')
        check('mobile drawer opens with 5 items',d['open'] and d['vis']=='visible' and d['items']==['Home','About','Machines','Articles','Contact'],str(d))
        await m.click('.es-drawer__toggle'); await m.wait_for_timeout(200)
        sub=await m.evaluate("[...document.querySelectorAll('.es-drawer li.is-open .sub-menu a')].length")
        check('drawer Machines accordion lists sub-items',sub>=16,str(sub))
        await m.keyboard.press('Escape'); await m.wait_for_timeout(200)
        check('Escape closes drawer',not await m.evaluate("document.body.classList.contains('es-menu-open')"))
        # reduced motion
        rm=await b.new_page(viewport={'width':1440,'height':900}, reduced_motion='reduce')
        await rm.goto(URL); await rm.wait_for_timeout(600)
        rr=await rm.evaluate("({m:document.body.classList.contains('es-motion'),h:document.querySelectorAll('.es-hidden').length})")
        check('prefers-reduced-motion disables motion',not rr['m'] and rr['h']==0,str(rr))
        a1=await rm.evaluate("[...document.querySelectorAll('.es-mcard.is-shown .es-mcard__title')].map(e=>e.textContent.trim())")
        await rm.wait_for_timeout(4800)
        a2=await rm.evaluate("[...document.querySelectorAll('.es-mcard.is-shown .es-mcard__title')].map(e=>e.textContent.trim())")
        check('autoplay still runs with reduced motion',a1!=a2,str(a2))
        await b.close()
    print('PASS',len(ok)); [print('  +',x) for x in ok]
    print('FAIL',len(bad)); [print('  -',x) for x in bad]
asyncio.run(main())
