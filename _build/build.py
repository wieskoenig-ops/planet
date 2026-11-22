#!/usr/bin/env python3
"""Erzeugt planet.emergenz.art (deutsch unter /, englisch unter /en/).

Inhalte: _build/essays/<lang>/<slug_de>.html (Textkörper), Metadaten unten in ESSAYS.
Aufruf:  python3 _build/build.py
Jekyll veröffentlicht _build nicht (Unterstrich-Ordner).
"""
import html, json, pathlib, re
from datetime import date
from email.utils import format_datetime
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / '_build' / 'essays'
BASE = 'https://planet.emergenz.art'
EMERGENZ = 'https://emergenz.art'

RUBRIKEN = {
    'klima':   {'de': 'Klima',   'en': 'Climate'},
    'politik': {'de': 'Politik', 'en': 'Politics'},
    'technik': {'de': 'Technik', 'en': 'Technology'},
    'maerkte': {'de': 'Märkte',  'en': 'Markets'},
}

# Neueste zuerst nicht nötig – wird nach Datum sortiert.
ESSAYS = [
    {
        'id': 'overshoot', 'rubrik': 'klima', 'datum': '2026-11-22', 'motiv': 'overshoot',
        'related': ['hysterese', 'elektrifizierung', 'amoc'],
        'de': {'slug': 'overshoot', 'titel': 'Überschreiten ist kein Ort',
               'dek': 'Der letzte Entwurf der COP31 hätte eingeräumt, dass 1,5 Grad fallen, und auf den Rückweg gesetzt. Beschlossen wurde nichts. Was die Hysterese dazu sagt.',
               'desc': 'Der letzte Entwurf der COP31 hätte eingeräumt, dass 1,5 Grad fallen, und auf den Rückweg per CO₂-Entnahme gesetzt. Beschlossen wurde nichts. Ein Essay über Overshoot, Hysterese und die Frage, was zurückkommt.',
               'teaser': 'Die Temperatur kann zurückkommen, das Klima, das sie hervorgebracht hat, nicht. Über Overshoot, Hysterese und die Wette auf die CO₂-Entnahme.'},
        'en': {'slug': 'overshoot', 'titel': 'Overshoot is not a place',
               'dek': 'The final COP31 draft would have conceded that 1.5 degrees will be breached, and bet on the way back. Nothing was adopted. What hysteresis has to say about it.',
               'desc': 'The final COP31 draft would have conceded that 1.5 degrees will be breached and relied on carbon removal for the way back. Nothing was adopted. An essay on overshoot, hysteresis and the question of what returns.',
               'teaser': 'The temperature can come back; the climate that produced it cannot. On overshoot, hysteresis and the bet on carbon removal.'},
    },
    {
        'id': 'elektrifizierung', 'rubrik': 'technik', 'datum': '2026-11-22', 'motiv': 'elektrifizierung',
        'related': ['overshoot', 'kreislauf', 'hysterese'],
        'de': {'slug': 'elektrifizierung', 'titel': 'Der Engpass liegt in der Leitung',
               'dek': 'Die COP31 wollte, dass Strom ein gutes Drittel unserer Energie liefert. Der Beschluss ist gescheitert. Netze, Kupfer und Zeit waren ohnehin noch nicht so weit.',
               'desc': 'Elektrifizierung war das konkreteste Ziel der COP31, und der Beschluss ist gescheitert. Ein Essay über Netze, Kupfer und die Frage, was zwischen Ziel und Steckdose liegt.',
               'teaser': 'Ein Ziel lässt sich in einer Nacht beschließen, ein Transformator braucht bis zu vier Jahre. Über Netze, Kupfer und das Tempo zweier Systeme.'},
        'en': {'slug': 'electrification', 'titel': 'The bottleneck is in the wires',
               'dek': 'COP31 wanted electricity to supply a good third of our energy. The decision failed. Grids, copper and time were not ready anyway.',
               'desc': 'Electrification was the most concrete goal of COP31, and the decision failed. An essay on grids, copper and what lies between a target and the socket.',
               'teaser': 'A target can be agreed in one night; a transformer takes up to four years. On grids, copper and two systems running at different speeds.'},
    },
    {
        'id': 'wasser', 'rubrik': 'klima', 'datum': '2026-11-22', 'motiv': 'wasser',
        'related': ['overshoot', 'hysterese', 'amoc'],
        'de': {'slug': 'wasser', 'titel': 'Das Sparkonto',
               'dek': 'Gletscher, Grundwasser und das Wort, das gerade seine Bedeutung wechselt.',
               'desc': 'Von der Wasserkrise zum Wasserbankrott: Was Gletscher und Grundwasserleiter über Kipppunkte und Hysterese erzählen.',
               'teaser': 'Von der Wasserkrise zum Wasserbankrott: was Gletscher und Grundwasserleiter über Kipppunkte und Hysterese erzählen.'},
        'en': {'slug': 'water', 'titel': 'The savings account',
               'dek': 'Glaciers, groundwater and a word that is changing its meaning.',
               'desc': 'From water crisis to water bankruptcy: what glaciers and aquifers tell us about tipping points and hysteresis.',
               'teaser': 'From water crisis to water bankruptcy: what glaciers and aquifers tell us about tipping points and hysteresis.'},
    },
    {
        'id': 'kreislauf', 'rubrik': 'klima', 'datum': '2026-11-22', 'motiv': 'kreislauf',
        'related': ['wasser', 'elektrifizierung', 'overshoot'],
        'de': {'slug': 'kreislauf', 'titel': 'Kaskade, nicht Kreislauf',
               'dek': 'Fünf Recyclingquoten zwischen 6 und 69 Prozent, und die Frage hinter den 15 Prozent von Antalya.',
               'desc': 'Die COP31-Präsidentschaft wollte Kreislaufwirtschaft, der Abschlusstext ist gescheitert. Am Beispiel Plastik: Es gibt viele Zahlen, aber keine, die Qualität misst.',
               'teaser': 'Am Beispiel Plastik: Es gibt viele Recyclingzahlen, aber keine, die Qualität misst. Ein Kreislauf verliert nichts, eine Kaskade bei jeder Stufe.'},
        'en': {'slug': 'recycling', 'titel': 'A cascade, not a cycle',
               'dek': 'Five recycling rates between 6 and 69 per cent, and the question behind the 15 per cent of Antalya.',
               'desc': 'The COP31 presidency wanted a circular economy; the final text failed. Plastic as an example: there are many figures, but none that measures quality.',
               'teaser': 'Plastic as an example: there are many recycling figures, but none that measures quality. A cycle loses nothing; a cascade loses something at every step.'},
    },
    {
        'id': 'kippt-hier-etwas', 'rubrik': 'maerkte', 'datum': '2026-11-08', 'motiv': 'kippt-hier-etwas',
        'related': ['ki', 'hysterese', 'politik'],
        'de': {'slug': 'kippt-hier-etwas', 'titel': 'Kippt hier etwas?',
               'dek': 'Der Einbruch der KI-Aktien nach den US-Zwischenwahlen 2026, geprüft an den Merkmalen eines Kipppunkts.',
               'teaser': 'Sandhaufen, Reflexivität, gekoppelte Kipppunkte und Hysterese: Was der Börsensturz nach der Wahl über Kipppunkte verrät – und was nicht.'},
        'en': {'slug': 'is-something-tipping', 'titel': 'Is something tipping here?',
               'dek': 'The slump in AI stocks after the 2026 US midterms, tested against the hallmarks of a tipping point.',
               'teaser': 'Sandpiles, reflexivity, coupled tipping points and hysteresis: what the post-election crash reveals about tipping points – and what it does not.'},
    },
    {
        'id': 'ki', 'rubrik': 'technik', 'datum': '2026-11-05', 'motiv': 'ki',
        'related': ['kippt-hier-etwas', 'hysterese', 'politik'],
        'de': {'slug': 'ki', 'titel': 'Die Schwelle, die niemand sieht',
               'dek': 'Ein Essay über künstliche Intelligenz, Emergenz und die Frage, ob es einen Kipppunkt gibt.',
               'teaser': 'Über Fähigkeiten, die niemand programmiert hat, Sprünge im Inneren neuronaler Netze und die Frage, ob AGI ein Kipppunkt ist.'},
        'en': {'slug': 'ai', 'titel': 'The threshold no one sees',
               'dek': 'An essay on artificial intelligence, emergence and the question of whether there is a tipping point.',
               'teaser': 'On abilities nobody programmed, jumps inside neural networks and the question of whether AGI is a tipping point.'},
    },
    {
        'id': 'politik', 'rubrik': 'politik', 'datum': '2026-11-05', 'motiv': 'politik',
        'related': ['amoc', 'hysterese', 'kippt-hier-etwas'],
        'de': {'slug': 'politik', 'titel': 'Zwei Uhren',
               'dek': 'Ein Essay über Klimapolitik, Kipppunkte und die Verantwortung für Prozesse, die länger dauern als eine Legislaturperiode.',
               'teaser': 'Die Uhr der Politik misst Legislaturperioden, die Uhr des Klimas Jahrhunderte. Über Kompromisse, die Physik nicht kennt, und Verantwortung.'},
        'en': {'slug': 'politics', 'titel': 'Two clocks',
               'dek': 'An essay on climate policy, tipping points and responsibility for processes that outlast a legislative term.',
               'teaser': 'The political clock measures legislative terms, the climate clock centuries. On compromises physics does not recognise, and on responsibility.'},
    },
    {
        'id': 'planetare-kognition', 'rubrik': 'technik', 'datum': '2026-11-04', 'motiv': 'planetare-kognition',
        'related': ['ki', 'kippt-hier-etwas', 'politik'],
        'de': {'slug': 'planetare-kognition', 'titel': 'Kein Moment',
               'dek': 'Eine These über planetare Kognition, die Technosphäre und die falsche Frage der AGI-Debatte.',
               'desc': 'Kein Neuron hat je bemerkt, dass es Teil eines Geistes wurde. Über planetare Kognition, die Technosphäre und die falsche Frage der AGI-Debatte.',
               'teaser': 'Kein Neuron hat je bemerkt, dass es Teil eines Geistes wurde. Warum die Frage nach dem Tag der AGI die falsche ist, und welche Zukunft die Technosphäre vorwegnimmt.'},
        'en': {'slug': 'planetary-cognition', 'titel': 'No moment',
               'dek': 'A thesis on planetary cognition, the technosphere and the wrong question of the AGI debate.',
               'desc': 'No neuron ever noticed that it had become part of a mind. On planetary cognition, the technosphere and the wrong question of the AGI debate.',
               'teaser': 'No neuron ever noticed that it had become part of a mind. Why asking for the day of AGI is the wrong question, and which future the technosphere anticipates.'},
    },
    {
        'id': 'hysterese', 'rubrik': 'klima', 'datum': '2026-11-04', 'motiv': 'hysterese',
        'related': ['amoc', 'politik', 'kippt-hier-etwas'],
        'de': {'slug': 'hysterese', 'titel': 'Der Weg zurück ist ein anderer',
               'dek': 'Ein Essay über Hysterese, Attraktoren und das Gedächtnis komplexer Systeme.',
               'teaser': 'Warum ein gekipptes System nicht zurückkehrt, wenn die Ursache verschwindet – vom Klarwassersee über das Eis bis zur Gesellschaft.'},
        'en': {'slug': 'hysteresis', 'titel': 'The way back is a different one',
               'dek': 'An essay on hysteresis, attractors and the memory of complex systems.',
               'teaser': 'Why a system that has tipped does not return when the cause disappears – from clear lakes to ice sheets to societies.'},
    },
    {
        'id': 'amoc', 'rubrik': 'klima', 'datum': '2026-06-16', 'motiv': 'amoc',
        'related': ['hysterese', 'politik', 'ki'],
        'de': {'slug': 'amoc', 'titel': 'Das Förderband stirbt leise',
               'dek': 'Ein Essay über die AMOC, die Physik der Unumkehrbarkeit und das Versagen des linearen Denkens.',
               'teaser': 'Die Atlantische Umwälzzirkulation schwächelt. Frühwarnzeichen, Hysterese und eine Politik, die ihre Messinstrumente abbaut.'},
        'en': {'slug': 'amoc', 'titel': 'The conveyor belt dies quietly',
               'dek': 'An essay on the AMOC, the physics of irreversibility and the failure of linear thinking.',
               'teaser': 'The Atlantic overturning circulation is weakening. Early warning signs, hysteresis, and a policy that dismantles its own instruments.'},
    },
]
BY_ID = {e['id']: e for e in ESSAYS}

T = {
    'de': {
        'html_lang': 'de', 'locale': 'de_DE', 'prefix': '',
        'tagline': 'Essays darüber, wo Systeme kippen',
        'site_desc': 'planet – Essays über Kipppunkte, Hysterese und Emergenz in Klima, Politik, Technik und Märkten. Ein Ableger von emergenz.art.',
        'nav_essays': 'Essays', 'nav_about': 'Über', 'other_lang': 'English', 'other_code': 'en',
        'lead': 'Wann kippt ein System – und gibt es danach einen Weg zurück? <strong>planet</strong> sammelt Essays über Kipppunkte in Klima, Politik, Technik und Märkten.',
        'latest': 'Neueste Ausgabe', 'all_essays': 'Alle Essays', 'by_topic': 'Nach Themen', 'read': 'Weiterlesen →',
        'essays_title': 'Essays', 'essays_intro': 'Alle Texte, nach Themen geordnet. Grundbegriffe erklärt das <a href="https://emergenz.art/glossar/">Glossar auf emergenz.art</a>.',
        'minutes': '{} Min. Lesezeit', 'further': 'Weiterlesen',
        'months': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
        'datefmt': '{d}. {m} {y}',
        'footer_sister': 'Ein Ableger von <a href="https://emergenz.art/">emergenz.art</a>',
        'contact': 'Kontakt', 'imprint': 'Impressum', 'privacy_url': 'https://emergenz.art/impressum/#datenschutz',
        'feed': 'RSS-Feed', 'translated': '',
        'skip': 'Zum Inhalt',
    },
    'en': {
        'html_lang': 'en', 'locale': 'en_GB', 'prefix': '/en',
        'tagline': 'Essays on where systems tip',
        'site_desc': 'planet – essays on tipping points, hysteresis and emergence in climate, politics, technology and markets. An offshoot of emergenz.art.',
        'nav_essays': 'Essays', 'nav_about': 'About', 'other_lang': 'Deutsch', 'other_code': 'de',
        'lead': 'When does a system tip – and is there a way back afterwards? <strong>planet</strong> collects essays on tipping points in climate, politics, technology and markets.',
        'latest': 'Latest essay', 'all_essays': 'All essays', 'by_topic': 'By topic', 'read': 'Read on →',
        'essays_title': 'Essays', 'essays_intro': 'All texts, ordered by topic. Key terms are explained in the <a href="https://emergenz.art/glossar/" hreflang="de">glossary on emergenz.art</a> (in German).',
        'minutes': '{} min read', 'further': 'Read on',
        'months': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        'datefmt': '{d} {m} {y}',
        'footer_sister': 'An offshoot of <a href="https://emergenz.art/">emergenz.art</a>',
        'contact': 'Contact', 'imprint': 'Legal notice', 'privacy_url': 'https://emergenz.art/impressum/#datenschutz',
        'feed': 'RSS feed', 'translated': 'Translated from the <a href="{de_url}" hreflang="de" lang="de">German original</a>.',
        'skip': 'Skip to content',
    },
}

ABOUT = {
    'de': {'slug': 'ueber', 'title': 'Über planet', 'body': '''
<p><strong>planet</strong> ist der Ort für Essays über Kipppunkte: über Systeme, die lange stabil wirken und dann in einen anderen Zustand springen – und über die Frage, ob es von dort einen Weg zurück gibt.</p>
<p>Die Texte kommen aus vier Feldern: <strong>Klima</strong> (Atlantikströmung, Eisschilde, Hysterese), <strong>Politik</strong> (Verantwortung für Prozesse, die länger dauern als eine Legislaturperiode), <strong>Technik</strong> (Emergenz in künstlicher Intelligenz) und <strong>Märkte</strong> (Rückkopplung, Reflexivität, Kaskaden).</p>
<h2>Verhältnis zu emergenz.art</h2>
<p><a href="https://emergenz.art/">emergenz.art</a> ist die ruhige, erklärende Schwesterseite: Was ist Emergenz, wie zeigt sie sich in den Wissenschaften und in der Kunst? Dort stehen auch die Grundlagen, auf die sich die Essays hier stützen – die Seite über <a href="https://emergenz.art/emergenz/kippunkte/">Kipppunkte</a> und das <a href="https://emergenz.art/glossar/">Glossar</a>.</p>
<p>planet ist der Teil, in dem es um die Gegenwart geht. Die Texte sind datiert; wo sich die Lage ändert, bekommen sie einen Nachtrag mit Stand.</p>
<h2>Haltung</h2>
<p>Die Essays beschreiben Systemdynamik. Sie suchen keine Schuldigen, sie bewerten keine Parteien und sie geben keine Anlageempfehlungen. Zahlen und Studien sind belegt; die Quellen stehen am Ende jedes Textes.</p>
<p>Die englischen Fassungen sind Übersetzungen der deutschen Originale.</p>
<h2>Kontakt und Impressum</h2>
<p>planet wird zusammen mit emergenz.art betrieben. <a href="https://emergenz.art/kontakt/">Kontakt</a> und <a href="https://emergenz.art/impressum/">Impressum mit Datenschutzhinweisen</a> gelten für beide Seiten. Neue Texte gibt es auch als <a href="/feed.xml">RSS-Feed</a>.</p>
'''},
    'en': {'slug': 'about', 'title': 'About planet', 'body': '''
<p><strong>planet</strong> is a home for essays on tipping points: on systems that seem stable for a long time and then jump into a different state – and on the question of whether there is a way back.</p>
<p>The essays come from four fields: <strong>climate</strong> (the Atlantic circulation, ice sheets, hysteresis), <strong>politics</strong> (responsibility for processes that outlast a legislative term), <strong>technology</strong> (emergence in artificial intelligence) and <strong>markets</strong> (feedback, reflexivity, cascades).</p>
<h2>Relation to emergenz.art</h2>
<p><a href="https://emergenz.art/" hreflang="de">emergenz.art</a> is the calm, explanatory sister site (in German): what is emergence, and how does it appear in the sciences and in art? It also holds the foundations these essays build on – the page on <a href="https://emergenz.art/emergenz/kippunkte/" hreflang="de">tipping points</a> and the <a href="https://emergenz.art/glossar/" hreflang="de">glossary</a>.</p>
<p>planet is the part that deals with the present. The essays are dated; where the situation changes, they receive an update with a date.</p>
<h2>Approach</h2>
<p>The essays describe system dynamics. They do not look for culprits, they do not judge parties and they give no investment advice. Figures and studies are referenced; the sources are listed at the end of each essay.</p>
<p>The English versions are translations of the German originals.</p>
<h2>Contact and legal notice</h2>
<p>planet is run together with emergenz.art. <a href="https://emergenz.art/kontakt/" hreflang="de">Contact</a> and the <a href="https://emergenz.art/impressum/" hreflang="de">legal notice and privacy information</a> (in German) apply to both sites. New essays are also available as an <a href="/en/feed.xml">RSS feed</a>.</p>
'''},
}


def esc(s):
    return html.escape(s, quote=True)


def fmt_date(iso, lang):
    d = date.fromisoformat(iso)
    t = T[lang]
    return t['datefmt'].format(d=d.day, m=t['months'][d.month - 1], y=d.year)


def url(lang, *parts):
    p = T[lang]['prefix'] + '/' + '/'.join(x for x in parts if x)
    return p + ('/' if parts and parts[-1] else '')


def essay_url(e, lang):
    return url(lang, e[lang]['slug'])


def body_of(e, lang):
    f = SRC / lang / f"{e['id']}.html"
    return f.read_text() if f.exists() else None


def langs_of(e):
    return [l for l in ('de', 'en') if body_of(e, l)]


def minutes(text, lang):
    words = len(re.sub(r'<[^>]+>', ' ', text).split())
    return max(1, round(words / (200 if lang == 'de' else 230)))


GOAT = '''<script>window.goatcounter = { path: function (p) { return location.host + p } }</script>
<script data-goatcounter="https://emergenz.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'''


def page(lang, *, title, desc, path, alt, body, current=None, og_type='website', head_extra='', scripts=''):
    """alt: dict lang -> path (für hreflang und Sprachumschalter)."""
    t = T[lang]
    other = t['other_code']
    links = ''.join(f'\n  <link rel="alternate" hreflang="{l}" href="{BASE}{p}">' for l, p in alt.items())
    if 'de' in alt:
        links += f'\n  <link rel="alternate" hreflang="x-default" href="{BASE}{alt["de"]}">'
    switch = (f'<a class="lang" href="{alt[other]}" hreflang="{other}" lang="{other}">{T[lang]["other_lang"]}</a>'
              if other in alt else '')
    feed = url(lang, 'feed.xml').rstrip('/')
    nav = [(url(lang), 'planet', 'home'), (url(lang, 'essays'), t['nav_essays'], 'essays'),
           (url(lang, ABOUT[lang]['slug']), t['nav_about'], 'about')]
    navhtml = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if c == current else ""}>{esc(n)}</a>'
                      for h, n, c in nav[1:])
    full_title = title if title.startswith('planet') else f'{title} — planet'
    return f'''<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(full_title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{BASE}{path}">{links}
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="planet.emergenz.art">
  <meta property="og:locale" content="{t['locale']}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{BASE}{path}">
  <meta property="og:image" content="{BASE}/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#f6f3ed" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#15130f" media="(prefers-color-scheme: dark)">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="alternate" type="application/rss+xml" title="planet ({lang})" href="{feed}">
  <link rel="preload" href="/fonts/literata-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/style.css">{head_extra}
</head>
<body>
  <a class="skip" href="#main">{t['skip']}</a>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="{url(lang)}" aria-label="planet – {esc(t['tagline'])}">planet<span class="dot">.</span></a>
      <nav class="site-nav" aria-label="Navigation">{navhtml}{switch}<a href="https://emergenz.art/" class="ext">emergenz.art ↗</a></nav>
    </div>
  </header>
  <main id="main">
{body}
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <p style="margin:0"><span class="brand-small">planet<span class="dot">.</span></span> {t['footer_sister']}</p>
      <ul>
        <li><a href="{feed}">{t['feed']}</a></li>
        <li><a href="https://emergenz.art/kontakt/">{t['contact']}</a></li>
        <li><a href="https://emergenz.art/impressum/">{t['imprint']}</a></li>
      </ul>
    </div>
  </footer>
{scripts}{GOAT}
</body>
</html>
'''


def meta_line(e, lang, text=None):
    t = T[lang]
    parts = [f'<span><time datetime="{e["datum"]}">{fmt_date(e["datum"], lang)}</time></span>']
    if text:
        parts.append(f'<span>{t["minutes"].format(minutes(text, lang))}</span>')
    return f'<p class="meta">{"".join(parts)}</p>'


def card(e, lang, h='h3'):
    L = e[lang]
    body = body_of(e, lang)
    return f'''      <article class="card">
        <a class="kicker" href="{url(lang, 'essays')}#{e['rubrik']}">{RUBRIKEN[e['rubrik']][lang]}</a>
        <{h}><a href="{essay_url(e, lang)}">{esc(L['titel'])}</a></{h}>
        <p>{esc(L['teaser'])}</p>
        {meta_line(e, lang, body)}
      </article>'''


def motif_scripts(e):
    return f'<script src="/motiv.js"></script>\n<script src="/motive/{e["motiv"]}.js"></script>\n'


def build_essay(e, lang):
    t, L = T[lang], e[lang]
    body = body_of(e, lang)
    alt = {l: essay_url(e, l) for l in langs_of(e)}
    note = ''
    if lang == 'en' and t['translated']:
        note = f'<p class="meta translated">{t["translated"].format(de_url=essay_url(e, "de"))}</p>'
    related = [BY_ID[r] for r in e['related'] if lang in langs_of(BY_ID[r])][:3]
    further = ''
    if related:
        further = f'''
    <aside class="further wrap" aria-labelledby="further-h">
      <div class="section-head"><h2 id="further-h">{t['further']}</h2></div>
      <div class="grid">
{chr(10).join(card(r, lang) for r in related)}
      </div>
    </aside>'''
    ld = {
        '@context': 'https://schema.org', '@type': 'Article', 'headline': L['titel'], 'description': L.get('desc', L['dek']),
        'datePublished': e['datum'], 'inLanguage': lang, 'url': BASE + essay_url(e, lang),
        'publisher': {'@type': 'Organization', 'name': 'emergenz.art', 'url': EMERGENZ},
    }
    main = f'''    <div class="article-art" aria-hidden="true"><canvas id="bg-canvas" class="motif"></canvas></div>
    <article class="article">
      <header class="article-head">
        <a class="kicker" href="{url(lang, 'essays')}#{e['rubrik']}">{RUBRIKEN[e['rubrik']][lang]}</a>
        <h1>{esc(L['titel'])}</h1>
        <p class="dek">{esc(L['dek'])}</p>
        {meta_line(e, lang, body)}
        {note}
      </header>
      <div class="prose">
{body}
      </div>
    </article>{further}'''
    head = f'\n  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    return page(lang, title=L['titel'], desc=L.get('desc', L['dek']), path=essay_url(e, lang), alt=alt, body=main,
                og_type='article', head_extra=head, scripts=motif_scripts(e))


def sorted_essays(lang):
    return sorted([e for e in ESSAYS if lang in langs_of(e)], key=lambda e: e['datum'], reverse=True)


def build_home(lang):
    t = T[lang]
    es = sorted_essays(lang)
    top, rest = es[0], es[1:]
    L = top[lang]
    main = f'''    <div class="wrap">
      <section class="lead-question"><p>{t['lead']}</p></section>
      <section class="hero" aria-labelledby="hero-h">
        <div class="hero-text">
          <span class="kicker">{t['latest']} · {RUBRIKEN[top['rubrik']][lang]}</span>
          <h2 id="hero-h"><a href="{essay_url(top, lang)}">{esc(L['titel'])}</a></h2>
          <p class="teaser">{esc(L['dek'])} {esc(L['teaser'])}</p>
          {meta_line(top, lang, body_of(top, lang))}
          <a class="more" href="{essay_url(top, lang)}">{t['read']}</a>
        </div>
        <div class="hero-art" aria-hidden="true"><canvas id="bg-canvas" class="motif"></canvas></div>
      </section>
      <div class="section-head"><h2>{t['all_essays']}</h2><a href="{url(lang, 'essays')}">{t['by_topic']} →</a></div>
      <div class="grid">
{chr(10).join(card(e, lang) for e in rest)}
      </div>
    </div>'''
    title = f"planet — {t['tagline']}"
    alt = {l: url(l) for l in ('de', 'en')}
    return page(lang, title=title, desc=t['site_desc'], path=url(lang), alt=alt, body=main, current='home',
                scripts=motif_scripts(top))


def build_essays_index(lang):
    t = T[lang]
    es = sorted_essays(lang)
    blocks = []
    for key, names in RUBRIKEN.items():
        items = [e for e in es if e['rubrik'] == key]
        if not items:
            continue
        lis = ''.join(f'''
          <li><a href="{essay_url(e, lang)}">{esc(e[lang]['titel'])}</a>
            <p>{esc(e[lang]['teaser'])}</p>
            {meta_line(e, lang, body_of(e, lang))}</li>''' for e in items)
        blocks.append(f'''      <section class="topic" id="{key}">
        <h2 class="kicker">{names[lang]}</h2>
        <ul>{lis}
        </ul>
      </section>''')
    main = f'''    <div class="wrap">
      <h1 class="page-title">{t['essays_title']}</h1>
      <p class="page-intro">{t['essays_intro']}</p>
      <div class="topics">
{chr(10).join(blocks)}
      </div>
    </div>'''
    alt = {l: url(l, 'essays') for l in ('de', 'en')}
    return page(lang, title=t['essays_title'], desc=t['site_desc'], path=url(lang, 'essays'), alt=alt, body=main,
                current='essays')


def build_about(lang):
    a = ABOUT[lang]
    main = f'''    <div class="page prose">
      <h1>{a['title']}</h1>
{a['body']}
    </div>'''
    alt = {l: url(l, ABOUT[l]['slug']) for l in ('de', 'en')}
    return page(lang, title=a['title'], desc=T[lang]['site_desc'], path=url(lang, a['slug']), alt=alt, body=main,
                current='about')


def build_404():
    main = '''    <div class="page prose">
      <h1>Seite nicht gefunden</h1>
      <p>Diese Adresse gibt es auf planet nicht (mehr). Vielleicht hilft die <a href="/essays/">Übersicht aller Essays</a> oder die <a href="/">Startseite</a>.</p>
      <p lang="en">This page does not exist. Try the <a href="/en/essays/">list of all essays</a> or the <a href="/en/">English home page</a>.</p>
    </div>'''
    out = page('de', title='Seite nicht gefunden', desc='Seite nicht gefunden', path='/404.html', alt={}, body=main)
    return out.replace('<head>', '<head>\n  <meta name="robots" content="noindex">', 1)


def build_feed(lang):
    t = T[lang]
    items = []
    for e in sorted_essays(lang):
        L = e[lang]
        d = datetime.fromisoformat(e['datum']).replace(hour=9, tzinfo=timezone.utc)
        link = BASE + essay_url(e, lang)
        items.append(f'''    <item>
      <title>{esc(L['titel'])}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{format_datetime(d)}</pubDate>
      <category>{RUBRIKEN[e['rubrik']][lang]}</category>
      <description>{esc(L['dek'] + ' ' + L['teaser'])}</description>
    </item>''')
    self_url = BASE + url(lang, 'feed.xml').rstrip('/')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>planet — {esc(t['tagline'])}</title>
    <link>{BASE}{url(lang)}</link>
    <atom:link href="{self_url}" rel="self" type="application/rss+xml"/>
    <description>{esc(t['site_desc'])}</description>
    <language>{lang}</language>
{chr(10).join(items)}
  </channel>
</rss>
'''


def build_sitemap(pages):
    """pages: list of dicts lang->path (Gruppen von Übersetzungen)."""
    out = []
    for group in pages:
        for lang, p in group.items():
            alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{BASE}{q}"/>' for l, q in group.items())
            out.append(f'  <url>\n    <loc>{BASE}{p}</loc>{alts}\n  </url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + '\n'.join(out) + '\n</urlset>\n')


def write(path, text):
    f = ROOT / path.lstrip('/')
    if path.endswith('/'):
        f = f / 'index.html'
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text)


def main():
    groups = []
    for lang in ('de', 'en'):
        write(url(lang), build_home(lang))
        write(url(lang, 'essays'), build_essays_index(lang))
        write(url(lang, ABOUT[lang]['slug']), build_about(lang))
        write(url(lang, 'feed.xml').rstrip('/'), build_feed(lang))
    groups += [{l: url(l) for l in ('de', 'en')}, {l: url(l, 'essays') for l in ('de', 'en')},
               {l: url(l, ABOUT[l]['slug']) for l in ('de', 'en')}]
    for e in ESSAYS:
        for lang in langs_of(e):
            write(essay_url(e, lang), build_essay(e, lang))
        groups.append({l: essay_url(e, l) for l in langs_of(e)})
    write('/404.html', build_404())
    write('/sitemap.xml', build_sitemap(groups))
    write('/robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
    write('/CNAME', 'planet.emergenz.art\n')
    missing = [f"{e['id']}/{l}" for e in ESSAYS for l in ('de', 'en') if not body_of(e, l)]
    print('fertig.', 'fehlende Fassungen: ' + ', '.join(missing) if missing else 'alle Fassungen da.')


if __name__ == '__main__':
    main()
