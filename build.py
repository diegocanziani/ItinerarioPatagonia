"""Genera index.html (autónomo) a partir del .dc.html de la herramienta de diseño."""
import re
s=open("Itinerario Patagonia v2.dc.html",encoding='utf-8').read()
helmet=re.search(r'<helmet>(.*?)</helmet>',s,re.S).group(1)
helmet=re.sub(r'<script src="\./image-slot\.js"></script>\n?','',helmet)
body=re.search(r'</helmet>(.*?)</x-dc>',s,re.S).group(1)
body=re.sub(r'</?sc-if[^>]*>\n?','',body)
for n in '123': body=body.replace('onClick="{{ goB%s }}"'%n, "onclick=\"document.getElementById('base%s').scrollIntoView({behavior:'smooth'})\""%n)
first=[True]
def slot(m):
    a=dict(re.findall(r'([\w-]+)="([^"]*)"',m.group(0)))
    if 'src' not in a: return ''
    r=a.get('radius','0') if a.get('shape')=='rounded' else '0'
    load='fetchpriority="high"' if first[0] else 'loading="lazy"'; first[0]=False
    alt=a.get("placeholder","").split(": ",1)[-1]
    return (f'<figure class="ph" style="border-radius:{r}px"><img src="{a["src"]}" alt="{alt}" {load} decoding="async" referrerpolicy="no-referrer" onload="this.classList.add(\'on\')">'
            f'<a href="{a["credit-href"]}" target="_blank" rel="noopener">{a["credit"]}</a></figure>')
body,n=re.subn(r'<image-slot\b[^>]*></image-slot>',slot,body)
css='''<style>
.ph{position:relative;width:100%;height:100%;margin:0;overflow:hidden;background:#161c21}
.ph img{width:100%;height:100%;object-fit:cover;display:block;opacity:0;transform:scale(1.04);transition:opacity .9s ease,transform 1.6s ease}
.ph img.on{opacity:1;transform:none}
.ph a{position:absolute;right:8px;bottom:6px;font-size:10px;color:rgba(236,231,220,.75);text-decoration:none;background:rgba(13,17,20,.45);padding:2px 6px;border-radius:4px;pointer-events:auto}
header .ph a,section>div:first-child>div>.ph a{bottom:auto;top:56px}
</style>'''
open('index.html','w',encoding='utf-8').write(f'<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="robots" content="noindex,nofollow">\n<title>De sur a norte · Patagonia</title>{helmet}{css}\n</head>\n<body>{body}</body>\n</html>\n')
print(n,'fotos')
