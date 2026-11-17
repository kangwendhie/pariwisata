from bs4 import BeautifulSoup
from pathlib import Path
p=Path('/mnt/data')
old=BeautifulSoup((p/'jelajah-jateng/index.html').read_text(encoding='utf8'),'html.parser')
target=p/'ruang-jelajah-tailwind/index.html'
html=target.read_text(encoding='utf8')
blocks=[]
for i, data in enumerate([('borobudur','borobudur'),('karimunjawa','karimunjawa'),('dieng','dieng'),('kota-lama','semarang')],1):
    slug,photo=data
    article=old.select_one('article.guide-card#'+slug)
    assert article, slug
    kicker=article.select_one('.guide-kicker')
    title=article.select_one('h3')
    desc=article.select_one('.guide-summary')
    facts=article.select_one('.guide-facts')
    alert=article.select_one('.guide-alert')
    links=article.select_one('.guide-links')
    assert kicker and title and desc and facts and alert and links
    # original content and original source URLs are retained verbatim
    for a in links.select('a'):
        a['class']=['guide-link'] + (['guide-link-primary'] if 'primary' in a.get('class',[]) else [])
    # CSS class for the source fact list
    block=f'''<article class="guide-panel mb-6" id="{slug}" aria-labelledby="{title.get('id')}">
      <div class="guide-visual photo-{photo}" role="img" aria-label="Ilustrasi destinasi {title.get_text(' ', strip=True)}">
        <div class="absolute inset-0 bg-gradient-to-t from-ink/75 via-transparent to-transparent"></div>
        <div class="absolute bottom-8 left-7 right-7 text-white">
          <span class="inline-flex items-center gap-2 rounded-full border border-white/30 bg-white/15 px-3 py-2 text-[10px] font-bold uppercase tracking-widest backdrop-blur-md">0{i} / Destinasi Jawa Tengah</span>
          <p class="mt-3 font-display text-[25px] font-extrabold tracking-[-.05em] sm:text-[31px]">{title.get_text(' ', strip=True)}</p>
        </div>
      </div>
      <div class="guide-detail">
        {str(kicker)}
        {str(title)}
        {str(desc)}
        {str(facts)}
        {str(alert)}
        {str(links)}
      </div>
    </article>'''
    blocks.append(block)
html=html.replace('__GUIDES__','\n'.join(blocks))
assert '__GUIDES__' not in html
# Catch duplicate ids
soup=BeautifulSoup(html,'html.parser')
from collections import Counter
ids=[x.get('id') for x in soup.select('[id]')]
print('duplicate ids:',[k for k,v in Counter(ids).items() if v>1]); assert len(ids)==len(set(ids))
for a in soup.select('a[href^="#"]'):
    href=a['href'][1:]
    if href and href not in ids: print('BROKEN LINK',href)
target.write_text(html,encoding='utf8')
print('new HTML:', len(html),'chars, guides:',len(blocks))
