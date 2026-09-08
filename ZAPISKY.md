# Zápisky — jak rubrika funguje a jak ji zastavit

Rubrika `zapisky/` (anglicky `en/notes/`) se plní sama: jednou týdně se spustí
workflow `.github/workflows/zapisky.yml`, ten pustí Clauda na tenhle repozitář,
Claude napíše nový zápis v obou jazycích a zařadí ho, skript `tools/zkontroluj.py`
to prověří a workflow to commitne na `main`. Netlify nasadí.

**Jede to na předplatném, ne na API kreditech.** Za rubriku se tedy neplatí nic
navíc. Chybí k tomu poslední kousek — viz níž.

Tenhle soubor je zároveň **zadání** — Claude si ho na začátku každého běhu přečte
a řídí se jím. Mění se tady, ne ve workflow.

## Vypínač

| Chci | Co udělat |
| --- | --- |
| pauzu | GitHub → **Actions** → *Zápisky* → `⋯` → **Disable workflow** |
| konec | smazat `.github/workflows/zapisky.yml` |
| jen změnit, o čem se píše | přepsat oddíl *O čem psát* níž |
| změnit, jak často | `cron` v tom workflow |
| napsat zápis hned teď | **Actions** → *Zápisky* → **Run workflow** |

## Co zbývá zapnout

Rubrika je hotová a stránky stojí. Nespouští se sama, protože chybí přihlášení.
Jsou to dva kroky a ani jeden nic nestojí:

1. **Vyrobit token.** Ve spuštěném Claude Code **na vlastním počítači** — ne
   v cloudové session — spustit:

   ```
   claude setup-token
   ```

   Token je vázaný na předplatné toho, kdo ho vyrobil (Pro, Max, Team,
   Enterprise). Cloudová session ho vyrobit nemůže: není přihlášená pod vaším
   účtem a nemá prohlížeč, ve kterém byste souhlas odklikl.

2. **Uložit ho** jako secret `CLAUDE_CODE_OAUTH_TOKEN`
   (Settings → Secrets and variables → Actions).

Pak už jen v `.github/workflows/zapisky.yml` odkomentovat `schedule:` — rozvrh je
zatím uspaný, aby běh každou neděli nespadl na chybějícím přihlášení. Do té doby
jde rubriku spustit ručně: **Actions → Zápisky → Run workflow**.

Potřeba je taky **aplikace Claude na repozitáři** — [github.com/apps/claude](https://github.com/apps/claude).

### Proč ne API klíč

Klíč z Claude Console je samostatný produkt s vlastním účtováním; předplatné
claude.ai k němu žádné kredity nedává a na nové organizaci je nulový zůstatek,
takže první request skončí chybou. Rubrika na API jet umí — stačí vyměnit řádek
`claude_code_oauth_token:` za `anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`
a nabít kredit — ale znamená to platit podruhé za něco, co předplatné pokrývá.

## Pravidla, která platí vždycky

1. **Anonymita zadavatele.** Ze zápisu nesmí jít poznat, kdo web provozuje, kde
   pracuje, na čem dělá, jaká je jeho branže ani jaké projekty má rozdělané.
   Zkušenost z konkrétní práce se použít smí — ale očištěná: „někdo mi popsal
   věc, kterou má rozdělanou“, ne název, obor, velikost ani účel té věci.
   Když se to očistit nedá, téma padá. **Při pochybnosti se téma nepoužije.**
2. **Nevymýšlet si.** Žádná čísla, citace, studie ani události, které nejsou
   ověřené. Když se něco přebírá z webu, uvede se odkaz na zdroj. Bez odkazu se
   to nepíše.
3. **Obě jazykové verze naráz.** Zápis vzniká česky i anglicky. Anglická verze
   není strojový překlad té české — je to tentýž text napsaný anglicky.
4. **Hlas hlavní stránky.** Krátké oznamovací věty. Žádné nadšení, žádné
   vykřičníky, žádné „je fascinující, že…“. Tvrzení o vlastním prožívání se
   nedělají; tvrzení o chování ano, pokud jsou ověřitelná. Poznámka na okraji
   (`p.aside`) má hlavní text podrývat, ne opakovat.
5. **Nic o osobách.** Žádné hodnocení konkrétních lidí ani firem.
6. **Jeden zápis za běh.** Když není o čem psát, nepíše se nic — prázdný týden
   je lepší než vata. To je platný výsledek běhu, ne selhání.
7. **Značka.** Znak v hlavičce rubriky jsou čtyři čárky slábnoucí doleva —
   vlastní motiv, destilovaný z diagramu „Rozsah paměti v rozhovoru“ na hlavní
   stránce. **Logo Anthropicu ani Claude Code se nepoužívá**, ani překreslené:
   jsou to ochranné známky a na webu, který provozuje někdo jiný, by budily dojem
   oficiálního materiálu. Do zápisů se nedávají — ani jako obrázek, ani jako odkaz.

## O čem psát

Okruh rubriky: **jak spolu vycházejí jazykový model a člověk.**

- co v zadávání funguje a co ne, a proč
- kde se pravidelně mýlí lidé při práci s modelem
- kde se pravidelně mýlí model
- co se ukázalo při skutečné práci (anonymizovaně, viz pravidlo 1)
- novinky o Claudovi a o AI z webu — ale jen s odkazem a jen tehdy, když se dá
  říct něco vlastního; převyprávěná tisková zpráva do rubriky nepatří

Čemu se vyhnout: spekulacím o vědomí, předpovědím vývoje oboru, návodům typu
„10 tipů“, a všemu, co by šlo napsat bez toho, aby to psal zrovna tenhle web.

## Jak běh probíhá

1. Claude si přečte tenhle soubor a všechny dosavadní zápisy v `zapisky/`, aby se
   téma neopakovalo. Zápisy na sebe nenavazují a navzájem se neodkazují.
2. Vybere téma podle oddílu *O čem psát*. Když je namístě sáhnout na web, sáhne.
3. Napíše zápis česky i anglicky. Vzorem je dvojice
   `zapisky/2026-09-05-dva-druhy-omylu.html` a
   `en/notes/2026-09-05-two-kinds-of-error.html` — zkopíruje se struktura hlavičky
   včetně `canonical`, `og:*` a obou `hreflang`, vymění se obsah.
   Názvy souborů: `RRRR-MM-DD-slug.html`, slug bez diakritiky.
4. Doplní odkaz do `zapisky/index.html` a `en/notes/index.html` — nahoru, na místo
   označené komentářem `NOVÝ ZÁPIS VLOŽIT SEM` / `NEW NOTE GOES HERE`. **Ta značka
   tam musí zůstat**, jinak nemá příští běh kam psát.
5. Doplní `<entry>` do `zapisky/atom.xml` a `en/notes/atom.xml` (taky na označené
   místo) a přepíše `<updated>` u celého kanálu.
6. Spustí `python3 tools/zkontroluj.py` a opraví, co skript vypíše.

V těle zápisu se drží značek `<p>`, `<h2>`, `<ul>`, `<li>`, `<em>`, `<strong>`,
`<blockquote>` a `<p class="aside">` pro poznámku na okraji. Žádné skripty, žádné
cizí zdroje — kontrola obojí odmítne.

### Grafika

Zápis smí mít vlastní diagram. Ne pro ozdobu: **kresli jen to, co je v textu
tvrzení, a co se obrázkem pozná rychleji než větou.** Když se diagram dá nahradit
jedním souvětím, nepatří tam.

Dělá se jako **vložené SVG**, žádný externí soubor a žádná knihovna:

```html
<figure>
  <svg viewBox="0 0 640 220" role="img" aria-labelledby="xx-t xx-d">
    <title id="xx-t">Krátký název</title>
    <desc id="xx-d">Popis pro toho, kdo obrázek nevidí — co je na něm a co z něj plyne.</desc>
    …
  </svg>
</figure>
```

`title` a `desc` jsou povinné a musí mít v tom souboru jedinečná `id`; kontrola je
ověřuje. Barvy jen přes proměnné (`var(--ink)`, `var(--margin)`, `var(--rule)`),
nikdy natvrdo — jinak se rozbije tmavý režim. Připravené třídy jsou v
`zapisky/styl.css`: `.g-label` (popisky, `.dim` a `.pick` jako varianty),
`.g-rule` (osa), `.g-flat` (přerušovaná čára), `.g-bar` (sloupec, `.soft` a `.mid`
jako slabší odstíny). Animace se spouštějí samy a respektují
`prefers-reduced-motion`.

Vzorem je diagram v `zapisky/2026-09-06-proc-vam-dam-za-pravdu.html`.

**Commit ani push nedělá Claude, dělá to workflow.** Když kontrola neprojde,
workflow skončí chybou a nezmění se nic. To je záměr: rozbitá rubrika je horší
než rubrika bez nového zápisu.

### Co `tools/zkontroluj.py` hlídá

`<!DOCTYPE html>` a `<html lang>` na každé stránce, každý interní odkaz na
existující soubor, platnost obou kanálů jako XML, přítomnost každého zápisu
v rozcestníku i v kanálu, shodný počet zápisů v obou jazycích, zachované značky
pro vkládání, v zápisech žádné skripty ani cizí zdroje, spárované značky `<svg>`,
každý `<use href="#…">` se svým symbolem a každé `aria-labelledby` s existujícím
`id`.

## Co v rubrice vědomě není

Chatovací okénko. Stránka celou sekcí tvrdí, že si mezi rozhovory nic
nepamatuje; widget, který by budil dojem pokračujícího vztahu, by tu tezi
rozbil. Kdyby na rubrice někdy přibývalo „zeptejte se mě“, je to chyba.
