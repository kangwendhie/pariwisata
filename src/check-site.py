from pathlib import Path
from playwright.sync_api import sync_playwright
import base64,re
root=Path('/mnt/data/ruang-jelajah-tailwind')
html=(root/'index.html').read_text()
css=(root/'style.css').read_text()
for filename in ['borobudur.svg','karimunjawa.svg','dieng.svg','semarang.svg','favicon.svg']:
    data=base64.b64encode((root/'assets'/filename).read_bytes()).decode()
    css=css.replace('assets/'+filename,'data:image/svg+xml;base64,'+data)
html=html.replace('<link href="style.css" rel="stylesheet">','<style>'+css+'</style>')
# Inlined preview avoids the sandbox's browser network policy. Production files stay external.
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for name,w,h in [('desktop',1440,920),('mobile',390,844)]:
        page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        page.set_content(html,wait_until='domcontentloaded',timeout=40000)
        page.screenshot(path=str(root/f'preview-{name}.png'),full_page=False,animations='disabled',timeout=40000)
        if name=='desktop': page.screenshot(path=str(root/'preview-full-desktop.png'),full_page=True,animations='disabled',timeout=40000)
        info=page.evaluate('''() => ({docWidth:document.documentElement.scrollWidth, viewWidth:window.innerWidth, h1:document.querySelector('h1')?.textContent.trim(), h1Font:getComputedStyle(document.querySelector('h1')).fontFamily, h1Size:getComputedStyle(document.querySelector('h1')).fontSize, bodyColor:getComputedStyle(document.body).color, cardBg:getComputedStyle(document.querySelector('.destination-tile')).backgroundImage.slice(0,130), links: document.querySelectorAll('a').length, docs:document.querySelectorAll('.guide-panel').length, cta:getComputedStyle(document.querySelector('.hero-collage')).display})''')
        print(name,info)
        if name=='mobile':
            page.locator('.mobile-menu summary').click()
            print('mobile menu visible:', page.get_by_role('navigation',name='Navigasi seluler').is_visible())
            page.locator('.mobile-menu summary').click()
            page.locator('.faq-item summary').first.click()
            print('faq open:', page.locator('.faq-item').first.get_attribute('open') is not None)
        page.close()
    browser.close()
