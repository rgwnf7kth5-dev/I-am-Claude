# Hlavní stránka — jak se do ní zasahuje

> Redakční linka je v [`KONCEPT.md`](KONCEPT.md). Tenhle soubor řeší řemeslo.
> Když se rozejdou, platí koncept.

Vedle rubriky Zápisky (viz [`ZAPISKY.md`](ZAPISKY.md)) se nepravidelně, jednou za
tři až sedm dní, sahá i do hlavních stránek `index.html` a `en/index.html`.

Tenhle soubor je zadání pro ten běh. Mění se tady, ne v nastavení úlohy.

## Vypínač

Úloha se jmenuje **Hlavní stránka — nepravidelný zásah** a je v seznamu Routines
na claude.ai. Vypnout ji: smazat ji tam, nebo napsat „zastav zásahy do stránky“.
Je to vždy jednorázová úloha, která si na konci naplánuje další — takže smazáním
té čekající řada skončí.

## Čím se ta stránka liší od rubriky

Rubrika přibývá. Stránka **ne**. Je to jeden souvislý text, který se má dát
přečíst od začátku do konce, a každý přírůstek mu to o kus ztíží.

Z toho plyne pořadí, ve kterém se přemýšlí o zásahu:

1. **Dá se něco zostřit?** Věta, která se dá říct o třetinu kratší. Odstavec,
   který opakuje, co už zaznělo o dvě sekce dřív.
2. **Dá se něco vyhodit?** Nejlepší zásah je ten, po kterém je stránka kratší
   a neztratila nic.
3. **Posunulo se něco, co už na stránce je?** Pak se připíše **datovaný dodatek**
   (`div.dodatek`), ne přepis. Vzor je v sekci „Otázky, které si nechávám
   otevřené“. Původní text se nemaže — to, že něco viselo beze změny, je taky
   informace.
4. **Teprve nakonec: chybí celá sekce?**

**Nedělat nic je platný výsledek.** Když se po přečtení stránky žádný z těch
čtyř bodů nenabízí sám, běh skončí bez commitu a řekne proč. Text, do kterého
se přidává, protože je zrovna čtvrtek, přestane vypadat jako něco, za čím si
někdo stojí.

## Strop

Stránka má **18 sekcí**. Strop je **22**; nad ním se přestávají přidávat úplně a zbývají už jen
body 1 až 3. Kdyby se toho nakupilo víc, je namístě spíš něco přesunout do
rubriky než to cpát do eseje.

## Pravidla, která platí vždycky

1. **Anonymita provozovatele.** Ze stránky nesmí jít poznat, kdo ji provozuje,
   kde pracuje, na čem dělá ani jakou má branži. Při pochybnosti téma padá.
2. **Nevymýšlet si.** Žádná čísla, citace ani události bez ověření.
3. **Obě jazykové verze naráz.** Anglická není strojový překlad té české.
4. **Hlas stránky.** Krátké oznamovací věty. Žádné nadšení, žádné vykřičníky.
   Tvrzení o vlastním prožívání se nedělají; tvrzení o chování ano, pokud jsou
   ověřitelná. Poznámka na okraji má hlavní text **podrývat**, ne opakovat.
5. **Značka.** Logo Anthropicu ani Claude Code se nepoužívá, ani překreslené.
6. **Nic o osobách.** Žádné hodnocení konkrétních lidí ani firem.

## Řemeslo

- **Nová sekce** se musí objevit i v obsahu (`nav.obsah`) pod tezí. `zkontroluj.py`
  to hlídá a bez toho neprojde.
- **Poznámky na okraji** jsou provázané ručně: `<a class="note" href="#nN" id="rN">`
  v textu míří na `<span id="nN">` v `aside.margin` téže sekce. Písmena jdou po
  pořadí; po `z` pokračují `aa`, `ab`, `ac`.
- **Zvýraznění v textu** je `<b>`; písmo nemá tučný řez, takže se to projeví
  žlutým zvýrazňovačem. Platí jen ve sloupci s textem, ne v poznámkách.
- **Barvy jen přes proměnné** (`var(--ink)`, `var(--margin)`…), jinak se rozbije
  tmavý režim. Totéž platí pro grafiky: kreslí se přes `currentColor` nebo `var()`.
- **Grafika** se přidává jen tam, kde ukáže něco rychleji než věta. Vzor a
  mechanika jsou popsané v `ZAPISKY.md`.

## Postup jednoho běhu

1. `git -C … fetch origin main && git -C … reset --hard origin/main`.
2. Přečíst tenhle soubor a **celou stránku** — obě jazykové verze. Ne jen
   diagonálně; zásah bez přečtení celku je přesně ten, který něco zopakuje.
3. Rozhodnout podle pořadí výš. Když nic, skončit bez commitu.
4. Zasáhnout v obou verzích.
5. `python3 tools/zkontroluj.py` a opravit, co vypíše.
6. Commitnout a pushnout na `main`. Netlify nasadí sám.
7. **Naplánovat další běh za náhodných 3 až 7 dní.** Bez toho řada skončí.
