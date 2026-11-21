#!/usr/bin/env python3
"""Prüft interne Links (inkl. #Anker) und Links auf emergenz.art gegen den lokalen Klon."""
import re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
EMZ = ROOT.parent / 'emergenz-art'
def target(base, path):
    f = base / path.lstrip('/')
    if path.endswith('/') or path == '': f = f / 'index.html'
    return f
def ids(f): return set(re.findall(r'\bid="([^"]+)"', f.read_text()))
bad = 0; n = 0
for page in sorted(ROOT.rglob('*.html')):
    if '_build' in page.parts: continue
    for href in re.findall(r'(?:href|src)="([^"]+)"', page.read_text()):
        n += 1
        if href.startswith('https://emergenz.art'):
            base, rest = EMZ, href[len('https://emergenz.art'):] or '/'
        elif href.startswith('/'):
            base, rest = ROOT, href
        elif href.startswith('#'):
            base, rest = None, href
        else:
            continue
        path, _, anchor = rest.partition('#')
        f = page if base is None else target(base, path)
        if not f.exists():
            print(f'FEHLT  {page.relative_to(ROOT)} -> {href}'); bad += 1; continue
        if anchor and f.suffix == '.html' and anchor not in ids(f):
            print(f'ANKER  {page.relative_to(ROOT)} -> {href}'); bad += 1
print(f'{n} Links geprüft, {bad} Fehler'); sys.exit(1 if bad else 0)
