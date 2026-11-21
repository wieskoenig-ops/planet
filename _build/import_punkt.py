#!/usr/bin/env python3
"""Einmaliger Import der Punkt-Essays von emergenz.art (liest nur, ändert dort nichts).

Schreibt _build/essays/<slug>.html (Textkörper) und motive/<slug>.js (Hintergrundmotiv).
"""
import re, pathlib, html

SRC = pathlib.Path(__file__).resolve().parents[2] / 'emergenz-art' / 'punkt'
OUT = pathlib.Path(__file__).resolve().parent / 'essays' / 'de'
MOT = pathlib.Path(__file__).resolve().parents[1] / 'motive'

H2 = {
  'amoc': ['Die Maschine', 'Der Fingerabdruck', 'Das kritische Verlangsamen', 'Das Gesetz der Hysterese',
           '2055 bis 2063', 'Der Blindflug', 'Das Versagen des linearen Denkens', 'Koda: Was bleibt'],
  'hysterese': ['Das Wort', 'Zwei Wege', 'Attraktoren', 'Gedächtnis', 'See, Eis, Ozean',
                'Die Hysterese der Gesellschaft', 'Koda: Der Preis der Rückkehr'],
  'politik': ['Vierzig Jahre', 'Die Logik des Kompromisses', 'Zwei Uhren', 'Das fehlende Wort',
              'Deutschland', 'Verantwortung', 'Koda: Die Physik verhandelt nicht'],
  'ki': ['Was niemand programmiert hat', 'Sprünge im Inneren', 'Der Streit um die Sprünge',
         'Ist AGI ein Kipppunkt?', 'Der Weg zurück', 'Verantwortung', 'Koda: Ein Text über sich selbst'],
  'kippt-hier-etwas': ['Der Donnerstag', 'Sandkorn und Lawine', 'Die Schleife',
                       'Ein Kipppunkt stößt den anderen an', 'Gleichlauf', 'Die Probe', 'Koda: Nähe, nicht Ort'],
}


def fix_links(s):
    def rep(m):
        url = m.group(1)
        if url == '/punkt/':
            url = '/'
        elif url.startswith('/punkt/'):
            url = url[len('/punkt'):]
        elif url.startswith('/'):
            url = 'https://emergenz.art' + url
        return f'href="{url}"'
    s = re.sub(r'href="([^"]*)"', rep, s)
    s = re.sub(r'target="_blank"(?! rel)', 'target="_blank" rel="noopener"', s)
    s = s.replace(' title="im Glossar"', ' title="Im Glossar auf emergenz.art"')
    return s


def blocks(content):
    """Zerlegt den Inhalt in die Top-Level-<div>-Blöcke."""
    out, i = [], 0
    while True:
        m = re.compile(r'<div class="([^"]*)">').search(content, i)
        if not m:
            return out
        depth, j = 1, m.end()
        while depth:
            n = re.compile(r'<(/?)div\b').search(content, j)
            depth += -1 if n.group(1) else 1
            j = n.end()
        inner = content[m.end():content.rfind('</div', 0, j)]
        out.append((m.group(1), inner.strip()))
        i = j


def convert(slug):
    src = (SRC / slug / 'index.html').read_text()
    content = src.split('<div id="content">', 1)[1].split('<nav class="site-footer"', 1)[0]
    heads = iter(H2[slug])
    parts = []
    for cls, inner in blocks(content):
        if cls in ('section-label', 'essay-title'):
            continue
        if 'statement' in cls:
            parts.append(f'<blockquote class="statement">\n  {inner}\n</blockquote>')
        elif cls.startswith('block'):
            roman = re.search(r'<span class="roman">([^<]*)</span>', inner).group(1)
            body = re.sub(r'\s*<span class="roman">[^<]*</span>\s*<h2>[^<]*</h2>\s*', '', inner)
            body = '\n  '.join(l.strip() for l in body.splitlines() if l.strip())
            extra = ' class="coda"' if 'coda' in cls else ''
            parts.append(f'<section{extra}>\n  <h2><span class="num">{roman}</span>{html.escape(next(heads), quote=False)}</h2>\n  {body}\n</section>')
        elif cls == 'quellen':
            ul = inner.split('</h3>', 1)[1].strip()
            ul = '\n'.join('  ' + l.strip() for l in ul.splitlines())
            parts.append(f'<section class="quellen">\n  <h2>Quellen und weiterführende Literatur</h2>\n{ul}\n</section>')
        else:
            raise SystemExit(f'{slug}: unbekannter Block {cls}')
    assert next(heads, None) is None, slug
    (OUT / f'{slug}.html').write_text(fix_links('\n\n'.join(parts)) + '\n')

    js = re.search(r'<script>\n(.*?)</script>', src, re.S).group(1)
    js = js.replace('window.innerWidth', 'canvas.clientWidth').replace('window.innerHeight', 'canvas.clientHeight')
    js = js.replace('requestAnimationFrame(draw)', 'PLANET.next(draw)')
    js = re.sub(r"'rgba\(232,224,208,([^)']*)\)'", r"`rgba(${PLANET.ink},\1)`", js)
    js = js.replace('rgba(232,224,208,', 'rgba(${PLANET.ink},')
    assert 'requestAnimationFrame' not in js and '232,224,208' not in js, slug
    (MOT / f'{slug}.js').write_text(f'/* Hintergrundmotiv „{slug}“, übernommen von emergenz.art/punkt/{slug}/ */\n' + js)


for slug in H2:
    convert(slug)
    print('ok', slug)
