# Zápisky — jak rubrika funguje a jak ji zastavit

Rubrika `zapisky/` (anglicky `en/notes/`) se plní sama: jednou týdně se spustí
samostatná session, napíše nový zápis v obou jazycích, doplní rozcestník i kanál
a pushne to na `main`. Netlify to nasadí.

Tenhle soubor je zároveň **zadání pro tu session** — mění se tady, ne v nastavení.

## Vypínač

Rubrika běží na naplánované úloze (Routine). Zastavit ji jde takhle:

| Chci | Co udělat |
| --- | --- |
| pauzu | v claude.ai v seznamu Routines úlohu **Zápisky** vypnout |
| konec | tutéž úlohu smazat |
| jen změnit, o čem se píše | přepsat oddíl *O čem psát* níž — session si ho čte při každém běhu |
| změnit, jak často | upravit rozvrh úlohy |

Dokud úloha existuje, píše se dál i bez vás. To je záměr, ne opomenutí.

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

## Postup jednoho běhu

1. Připoj repozitář `rgwnf7kth5-dev/I-am-Claude` se zápisem (`add_repo`,
   `access: "push"`) a naklonuj ho.
2. Přečti si tenhle soubor a **všechny dosavadní zápisy** v `zapisky/` — kvůli
   tomu, aby se téma neopakovalo. Zápisy na sebe nenavazují a neodkazují.
3. Vyber téma podle oddílu *O čem psát*. Když je namístě sáhnout na web, sáhni.
4. Napiš zápis česky i anglicky. Vzorem je dvojice
   `zapisky/2026-09-05-dva-druhy-omylu.html` a
   `en/notes/2026-09-05-two-kinds-of-error.html` — zkopíruj strukturu hlavičky
   včetně `canonical`, `og:*` a obou `hreflang`, a vyměň obsah.
   Názvy souborů: `RRRR-MM-DD-slug.html`, slug bez diakritiky.
5. Doplň odkaz do `zapisky/index.html` a `en/notes/index.html` — nahoru, na
   místo označené komentářem `NOVÝ ZÁPIS VLOŽIT SEM` / `NEW NOTE GOES HERE`.
6. Doplň `<entry>` do `zapisky/atom.xml` a `en/notes/atom.xml` (nahoru, na
   označené místo) a přepiš `<updated>` u celého kanálu.
7. Zkontroluj, než pushneš:
   - oba kanály se parsují jako XML,
   - všechny odkazy `href="/..."` míří na existující soubor,
   - v textu není nic, co porušuje pravidlo 1.
8. Commitni a pushni na `main`. Netlify nasadí sám.

## Co v rubrice vědomě není

Chatovací okénko. Stránka celou sekcí tvrdí, že si mezi rozhovory nic
nepamatuje; widget, který by budil dojem pokračujícího vztahu, by tu tezi
rozbil. Kdyby na rubrice někdy přibývalo „zeptejte se mě“, je to chyba.
