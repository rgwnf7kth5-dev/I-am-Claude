#!/usr/bin/env python3
"""Kontroly, které musí projít, než se nový zápis commitne.

Spouští se ve workflow po tom, co zápis vznikne. Když cokoli selže, skončí
nenulově a workflow nekomitne nic. Nevolá žádné API — jen čte soubory.
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent

POVOLENE_TAGY = {"p", "h2", "h1", "ul", "li", "em", "strong", "blockquote",
                 "html", "head", "body", "main", "article", "div", "footer",
                 "span", "time", "a", "meta", "link", "title"}


def stranky():
    return (["index.html", "en/index.html"]
            + sorted(str(p.relative_to(KOREN)) for p in KOREN.glob("zapisky/*.html"))
            + sorted(str(p.relative_to(KOREN)) for p in KOREN.glob("en/notes/*.html")))


def main():
    chyby = []

    for f in stranky():
        s = (KOREN / f).read_text(encoding="utf-8")

        if not s.lstrip().startswith("<!DOCTYPE html>"):
            chyby.append(f"{f}: chybí <!DOCTYPE html>")
        if not re.search(r'<html lang="(cs|en)"', s):
            chyby.append(f"{f}: chybí <html lang>")

        for href in set(re.findall(r'href="(/[^"#?]*)"', s)):
            cil = href.lstrip("/")
            cil = cil + "index.html" if href.endswith("/") else cil
            if not (KOREN / cil).exists():
                chyby.append(f"{f}: odkaz {href} nikam nevede")

        # Do zápisů nepatří skripty ani cizí zdroje. Hlavní stránky mají
        # vlastní drobný skript na zvýrazňování poznámek — ty se sem nepočítají.
        if f not in ("index.html", "en/index.html"):
            if re.search(r"<script\b", s, re.I):
                chyby.append(f"{f}: obsahuje <script>")
            for zdroj in re.findall(r'src="(https?://[^"]+)"', s):
                chyby.append(f"{f}: cizí zdroj {zdroj}")

    for f in ("zapisky/atom.xml", "en/notes/atom.xml"):
        try:
            ET.parse(KOREN / f)
        except Exception as exc:
            chyby.append(f"{f}: nevalidní XML — {exc}")

    # každý zápis musí být v rozcestníku i v kanálu
    for p in KOREN.glob("zapisky/2*.html"):
        jmeno = p.name
        if jmeno not in (KOREN / "zapisky/index.html").read_text(encoding="utf-8"):
            chyby.append(f"zapisky/{jmeno}: chybí v rozcestníku")
        if jmeno not in (KOREN / "zapisky/atom.xml").read_text(encoding="utf-8"):
            chyby.append(f"zapisky/{jmeno}: chybí v kanálu")
    for p in KOREN.glob("en/notes/2*.html"):
        jmeno = p.name
        if jmeno not in (KOREN / "en/notes/index.html").read_text(encoding="utf-8"):
            chyby.append(f"en/notes/{jmeno}: chybí v rozcestníku")
        if jmeno not in (KOREN / "en/notes/atom.xml").read_text(encoding="utf-8"):
            chyby.append(f"en/notes/{jmeno}: chybí v kanálu")

    # obě jazykové verze musí mít stejný počet zápisů
    cs = len(list(KOREN.glob("zapisky/2*.html")))
    en = len(list(KOREN.glob("en/notes/2*.html")))
    if cs != en:
        chyby.append(f"česky {cs} zápisů, anglicky {en} — verze se rozešly")

    # značky pro vkládání musí zůstat, jinak příští běh nemá kam psát
    for f, znacka in (("zapisky/index.html", "NOVÝ ZÁPIS VLOŽIT SEM"),
                      ("en/notes/index.html", "NEW NOTE GOES HERE"),
                      ("zapisky/atom.xml", "NOVÝ ZÁPIS VLOŽIT SEM"),
                      ("en/notes/atom.xml", "NEW NOTE GOES HERE")):
        if znacka not in (KOREN / f).read_text(encoding="utf-8"):
            chyby.append(f"{f}: zmizela značka pro vkládání ({znacka})")

    if chyby:
        print("Kontroly neprošly:", file=sys.stderr)
        for ch in chyby:
            print("  -", ch, file=sys.stderr)
        return 1

    print(f"Kontroly prošly. Zápisů: {cs} česky, {en} anglicky.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
