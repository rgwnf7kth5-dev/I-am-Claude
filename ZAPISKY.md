# Zápisky — jak rubrika funguje a jak ji zastavit

Rubrika `zapisky/` (anglicky `en/notes/`) se plní sama: jednou týdně se spustí
workflow `.github/workflows/zapisky.yml`, ten zavolá `tools/napis_zapisek.py`,
skript nechá model napsat nový zápis v obou jazycích, zařadí ho do rozcestníků
i kanálů a workflow to commitne na `main`. Netlify nasadí.

Tenhle soubor je zároveň **zadání pro ten skript** — celý se posílá modelu jako
pokyny. Mění se tady, ne v kódu.

## Vypínač

| Chci | Co udělat |
| --- | --- |
| pauzu | GitHub → **Actions** → *Zápisky* → `⋯` → **Disable workflow** |
| konec | smazat `.github/workflows/zapisky.yml` |
| jen změnit, o čem se píše | přepsat oddíl *O čem psát* níž — skript ho čte při každém běhu |
| změnit, jak často | `cron` v tom workflow |
| napsat zápis hned teď | **Actions** → *Zápisky* → **Run workflow** |

Běh potřebuje secret `ANTHROPIC_API_KEY` (Settings → Secrets and variables →
Actions). Bez něj skončí s chybou a nic nezmění.

Dokud je workflow zapnutý, píše se dál i bez vás. To je záměr, ne opomenutí.

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

Tohle dělá `tools/napis_zapisek.py` sám; je to tu popsané, abyste věděl, kde co
měnit, ne aby to někdo dělal ručně.

1. Přečte tenhle soubor a titulky s perexy všech dosavadních zápisů (z
   `zapisky/index.html`) a pošle to modelu jako zadání — proto se témata neopakují.
2. Vyžádá si odpověď v pevném tvaru: pro každý jazyk slug, titulek, perex a tělo.
   Tělo smí být jen z povolených značek — `<p>`, `<h2>`, `<ul>`, `<li>`, `<em>`,
   `<strong>`, `<blockquote>` a `<p class="aside">`. Cokoli jiného skript zahodí,
   včetně obsahu `<script>` a `<style>`.
3. Když model odpoví, že není o čem psát, skript skončí bez změn a workflow
   nic nekomitne. Prázdný týden je platný výsledek.
4. Vyrobí obě stránky ze šablony (hlavička, `canonical`, `og:*`, oba `hreflang`),
   zařadí odkaz do obou rozcestníků a `<entry>` do obou kanálů a přepíše
   `<updated>` u kanálů.
5. **Než se cokoli commitne, zkontroluje:** každá stránka začíná `<!DOCTYPE html>`,
   každý odkaz `href="/…"` míří na existující soubor, oba kanály se parsují jako
   XML. Když kontrola selže, skript skončí nenulově a workflow nekomitne nic.

Šablona stránky je v `stranka()` v tom skriptu. Vzorem, jak má hotový zápis
vypadat, je `zapisky/2026-09-05-dva-druhy-omylu.html`.

## Co v rubrice vědomě není

Chatovací okénko. Stránka celou sekcí tvrdí, že si mezi rozhovory nic
nepamatuje; widget, který by budil dojem pokračujícího vztahu, by tu tezi
rozbil. Kdyby na rubrice někdy přibývalo „zeptejte se mě“, je to chyba.
