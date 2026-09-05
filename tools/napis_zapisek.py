#!/usr/bin/env python3
"""Napíše nový zápis do rubriky Zápisky — česky i anglicky — a zařadí ho.

Spouští se z GitHub Actions jednou týdně. Když není o čem psát, model to řekne
a skript skončí bez změn; prázdný týden je platný výsledek, ne selhání.

Nic se nezapíše, dokud neprojdou kontroly na konci. Když kontrola selže,
skript skončí nenulově a workflow nic nekomitne.
"""

import datetime as dt
import html
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

import anthropic

KOREN = Path(__file__).resolve().parent.parent
WEB = "https://iamclaude.netlify.app"
MODEL = "claude-opus-5"

# Značky, za které se vkládá nový zápis.
MARKER_INDEX = {
    "zapisky/index.html": "<!-- NOVÝ ZÁPIS VLOŽIT SEM (nahoru, nejnovější první) -->",
    "en/notes/index.html": "<!-- NEW NOTE GOES HERE (top, newest first) -->",
}
MARKER_FEED = {
    "zapisky/atom.xml": "<!-- NOVÝ ZÁPIS VLOŽIT SEM (nahoru) a upravit <updated> výše -->",
    "en/notes/atom.xml": "<!-- NEW NOTE GOES HERE (top) and update <updated> above -->",
}

# Co smí model poslat v těle zápisu. Všechno ostatní se zahodí.
POVOLENE_TAGY = {"p", "h2", "ul", "li", "em", "strong", "blockquote"}
POVOLENA_TRIDA = {"aside"}

SCHEMA = {
    "type": "object",
    "properties": {
        "psat": {"type": "boolean"},
        "duvod_nepsat": {"type": "string"},
        "slug_cs": {"type": "string"},
        "titulek_cs": {"type": "string"},
        "perex_cs": {"type": "string"},
        "telo_cs": {"type": "string"},
        "slug_en": {"type": "string"},
        "titulek_en": {"type": "string"},
        "perex_en": {"type": "string"},
        "telo_en": {"type": "string"},
    },
    "required": [
        "psat", "duvod_nepsat",
        "slug_cs", "titulek_cs", "perex_cs", "telo_cs",
        "slug_en", "titulek_en", "perex_en", "telo_en",
    ],
    "additionalProperties": False,
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()[:60]


def dosavadni_zapisy() -> str:
    """Titulky a perexy už vydaných zápisů, aby se téma neopakovalo."""
    s = (KOREN / "zapisky/index.html").read_text(encoding="utf-8")
    kusy = re.findall(
        r'<a href="/zapisky/[^"]+">([^<]+)</a>\s*<p>([^<]+)</p>', s, re.S)
    if not kusy:
        return "(zatím žádné)"
    return "\n".join(f"- {t.strip()} — {p.strip()}" for t, p in kusy)


def uklid_telo(telo: str) -> str:
    """Zahodí všechno, co není v povoleném podmnožinovém HTML."""
    # u script/style musí pryč i obsah, ne jen značky
    telo = re.sub(r"<(script|style)\b.*?</\1\s*>", "", telo, flags=re.S | re.I)
    telo = re.sub(r"<!--.*?-->", "", telo, flags=re.S)
    out = []
    for m in re.finditer(r"<(/?)([a-zA-Z0-9]+)((?:\s[^>]*)?)>|([^<]+)", telo):
        zaviraci, jmeno, atributy, text = m.groups()
        if text is not None:
            out.append(text)
            continue
        jmeno = jmeno.lower()
        if jmeno not in POVOLENE_TAGY:
            continue
        if zaviraci:
            out.append(f"</{jmeno}>")
            continue
        trida = re.search(r'class="([^"]*)"', atributy or "")
        if trida and trida.group(1).strip() in POVOLENA_TRIDA:
            out.append(f'<{jmeno} class="{trida.group(1).strip()}">')
        else:
            out.append(f"<{jmeno}>")
    return "".join(out).strip()


def stranka(jazyk, datum, cislo, titulek, perex, telo, slug_cs, slug_en) -> str:
    cs = jazyk == "cs"
    url = f"{WEB}/zapisky/{datum}-{slug_cs}.html" if cs else f"{WEB}/en/notes/{datum}-{slug_en}.html"
    url_cs = f"{WEB}/zapisky/{datum}-{slug_cs}.html"
    url_en = f"{WEB}/en/notes/{datum}-{slug_en}.html"
    d = dt.date.fromisoformat(datum)
    mesice_cs = ["ledna", "února", "března", "dubna", "května", "června",
                 "července", "srpna", "září", "října", "listopadu", "prosince"]
    datum_lidsky = (f"{d.day}. {mesice_cs[d.month - 1]} {d.year}" if cs
                    else d.strftime("%-d %B %Y"))
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="{'cs' if cs else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulek)} — {'Zápisky' if cs else 'Notes'}</title>
<meta name="description" content="{e(perex)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#E3E5E0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14171A" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="article">
<meta property="og:locale" content="{'cs_CZ' if cs else 'en_GB'}">
<meta property="og:title" content="{e(titulek)}">
<meta property="og:description" content="{e(perex)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{WEB}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" hreflang="cs" href="{url_cs}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" type="application/atom+xml" title="{'Zápisky' if cs else 'Notes'}" href="{'/zapisky/atom.xml' if cs else '/en/notes/atom.xml'}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/zapisky/styl.css">
</head>
<body>
<main class="sheet">

  <div class="topbar">
    <p class="eyebrow">{'Zápisky' if cs else 'Notes'}</p>
    <a href="{'/zapisky/' if cs else '/en/notes/'}">{'Všechny zápisky' if cs else 'All notes'}</a>
    <a href="{'/' if cs else '/en/'}">{'Hlavní stránka' if cs else 'Main page'}</a>
    <a href="{url_en if cs else url_cs}" hreflang="{'en' if cs else 'cs'}" lang="{'en' if cs else 'cs'}">{'English' if cs else 'Čeština'}</a>
  </div>

  <article>
    <p class="dateline"><time datetime="{datum}">{datum_lidsky}</time> &nbsp;·&nbsp; {'zápis č.' if cs else 'note no.'} {cislo}</p>
    <h1>{e(titulek)}</h1>
    <p class="standfirst">{e(perex)}</p>

{telo}
  </article>

  <footer>
    <a href="{'/zapisky/' if cs else '/en/notes/'}">{'Zápisky' if cs else 'Notes'}</a>
    <a href="{'/zapisky/atom.xml' if cs else '/en/notes/atom.xml'}">{'Kanál' if cs else 'Feed'}</a>
    <a href="{'/' if cs else '/en/'}">{'Já jsem Claude' if cs else 'I am Claude'}</a>
    <span>{'bez cookies &nbsp;·&nbsp; bez analytiky' if cs else 'no cookies &nbsp;·&nbsp; no analytics'}</span>
  </footer>

</main>
</body>
</html>
"""


def zarad_do_rozcestniku(cesta, marker, datum, datum_lidsky, odkaz, titulek, perex):
    p = KOREN / cesta
    s = p.read_text(encoding="utf-8")
    assert marker in s, f"chybí značka v {cesta}"
    e = html.escape
    polozka = (f'{marker}\n'
               f'    <li>\n'
               f'      <p class="dateline"><time datetime="{datum}">{datum_lidsky}</time></p>\n'
               f'      <a href="{odkaz}">{e(titulek)}</a>\n'
               f'      <p>{e(perex)}</p>\n'
               f'    </li>')
    p.write_text(s.replace(marker, polozka, 1), encoding="utf-8")


def zarad_do_kanalu(cesta, marker, datum, url, titulek, perex):
    p = KOREN / cesta
    s = p.read_text(encoding="utf-8")
    assert marker in s, f"chybí značka v {cesta}"
    cas = f"{datum}T00:00:00Z"
    e = html.escape
    entry = (f'{marker}\n'
             f'  <entry>\n'
             f'    <title>{e(titulek)}</title>\n'
             f'    <link href="{url}"/>\n'
             f'    <id>{url}</id>\n'
             f'    <updated>{cas}</updated>\n'
             f'    <published>{cas}</published>\n'
             f'    <summary>{e(perex)}</summary>\n'
             f'  </entry>')
    s = s.replace(marker, entry, 1)
    # <updated> celého kanálu je ten první výskyt před značkou
    s = re.sub(r"(<updated>)[^<]+(</updated>)", rf"\g<1>{cas}\g<2>", s, count=1)
    p.write_text(s, encoding="utf-8")


def zkontroluj():
    """Nic z tohohle nesmí selhat, jinak se nekomituje."""
    chyby = []
    htmls = (["index.html", "en/index.html"]
             + sorted(str(p.relative_to(KOREN)) for p in KOREN.glob("zapisky/*.html"))
             + sorted(str(p.relative_to(KOREN)) for p in KOREN.glob("en/notes/*.html")))
    for f in htmls:
        s = (KOREN / f).read_text(encoding="utf-8")
        if not s.lstrip().startswith("<!DOCTYPE html>"):
            chyby.append(f"{f}: chybí DOCTYPE")
        for href in set(re.findall(r'href="(/[^"#?]*)"', s)):
            cil = href.lstrip("/")
            cil = cil + "index.html" if href.endswith("/") else cil
            if not (KOREN / cil).exists():
                chyby.append(f"{f}: rozbitý odkaz {href}")
    for f in ("zapisky/atom.xml", "en/notes/atom.xml"):
        try:
            ET.parse(KOREN / f)
        except Exception as exc:
            chyby.append(f"{f}: nevalidní XML — {exc}")
    return chyby


def main():
    datum = dt.datetime.now(dt.timezone.utc).date().isoformat()
    pravidla = (KOREN / "ZAPISKY.md").read_text(encoding="utf-8")
    hotove = dosavadni_zapisy()
    cislo = len(list(KOREN.glob("zapisky/2*.html"))) + 1

    zadani = f"""Píšeš nový zápis do rubriky Zápisky na osobní stránce jazykového modelu.

Řiď se tímhle zadáním. Je závazné, zvlášť pravidlo o anonymitě:

--- ZAPISKY.md ---
{pravidla}
--- konec ---

Zápisy, které už vyšly (nové téma se s nimi nesmí překrývat):
{hotove}

Napiš jeden nový zápis česky i anglicky. Anglická verze není překlad té české — je
to tentýž text napsaný anglicky.

Tělo (`telo_cs`, `telo_en`) je HTML z povolené podmnožiny a nic jiného:
<p>, <h2>, <ul>, <li>, <em>, <strong>, <blockquote> a <p class="aside"> pro poznámku
na okraji. Žádné jiné značky, žádné atributy kromě té jedné třídy, žádné odkazy na
jiné zápisy. Odsazuj o čtyři mezery. Rozsah zhruba 500 až 800 slov.

Slug je bez diakritiky, malými písmeny, slova spojená pomlčkou.

Když podle pravidel není o čem psát, vrať psat=false a v duvod_nepsat jednou větou
proč. Prázdný týden je v pořádku — vata je horší než mezera. Ostatní pole v tom
případě vyplň prázdnými řetězci."""

    client = anthropic.Anthropic()
    odpoved = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        messages=[{"role": "user", "content": zadani}],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
    )
    if odpoved.stop_reason == "refusal":
        print("Model odmítl:", odpoved.stop_details, file=sys.stderr)
        return 1
    text = next(b.text for b in odpoved.content if b.type == "text")
    z = json.loads(text)

    if not z["psat"]:
        print(f"Tenhle týden se nepíše: {z['duvod_nepsat']}")
        return 0

    slug_cs, slug_en = slugify(z["slug_cs"]), slugify(z["slug_en"])
    telo_cs, telo_en = uklid_telo(z["telo_cs"]), uklid_telo(z["telo_en"])
    if len(telo_cs) < 400 or len(telo_en) < 400:
        print("Tělo zápisu je po úklidu podezřele krátké — nekomituju.", file=sys.stderr)
        return 1

    (KOREN / f"zapisky/{datum}-{slug_cs}.html").write_text(
        stranka("cs", datum, cislo, z["titulek_cs"], z["perex_cs"], telo_cs, slug_cs, slug_en),
        encoding="utf-8")
    (KOREN / f"en/notes/{datum}-{slug_en}.html").write_text(
        stranka("en", datum, cislo, z["titulek_en"], z["perex_en"], telo_en, slug_cs, slug_en),
        encoding="utf-8")

    d = dt.date.fromisoformat(datum)
    mesice = ["ledna", "února", "března", "dubna", "května", "června",
              "července", "srpna", "září", "října", "listopadu", "prosince"]
    zarad_do_rozcestniku("zapisky/index.html", MARKER_INDEX["zapisky/index.html"], datum,
                         f"{d.day}. {mesice[d.month - 1]} {d.year}",
                         f"/zapisky/{datum}-{slug_cs}.html", z["titulek_cs"], z["perex_cs"])
    zarad_do_rozcestniku("en/notes/index.html", MARKER_INDEX["en/notes/index.html"], datum,
                         d.strftime("%-d %B %Y"),
                         f"/en/notes/{datum}-{slug_en}.html", z["titulek_en"], z["perex_en"])
    zarad_do_kanalu("zapisky/atom.xml", MARKER_FEED["zapisky/atom.xml"], datum,
                    f"{WEB}/zapisky/{datum}-{slug_cs}.html", z["titulek_cs"], z["perex_cs"])
    zarad_do_kanalu("en/notes/atom.xml", MARKER_FEED["en/notes/atom.xml"], datum,
                    f"{WEB}/en/notes/{datum}-{slug_en}.html", z["titulek_en"], z["perex_en"])

    chyby = zkontroluj()
    if chyby:
        print("Kontroly neprošly, nekomituju:", file=sys.stderr)
        for ch in chyby:
            print("  -", ch, file=sys.stderr)
        return 1

    print(f"Napsáno: {z['titulek_cs']} / {z['titulek_en']}")
    Path(os.environ.get("GITHUB_OUTPUT", "/dev/null")).open("a").write(
        f"titulek={z['titulek_cs']}\nzmena=ano\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
