#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La Loi Avec Moi — générateur de site statique.

Projet SÉPARÉ (ne se mélange pas avec competeiq).
Source de vérité UNIQUE : data/belgium/*.json (faits déjà certifiés/sourcés).
Le site ne peut donc jamais afficher autre chose que ce qui est vérifié.

Aucune dépendance externe : tourne avec Python 3 seul.
Sortie : apps/loi-avec-moi/dist/  (HTML statique, déployable Vercel/Netlify/Pages).
"""
import json
import html
import pathlib
import datetime

# --- chemins (repo-root-relatifs, robustes) ---
HERE = pathlib.Path(__file__).resolve().parent          # apps/loi-avec-moi
REPO = HERE.parent.parent                                # racine du repo
DATA = REPO / "data" / "belgium"
DIST = HERE / "dist"

# Ordre d'affichage des modules sur la page d'accueil
ORDRE_MODULES = [
    "bail_wallonie", "bail_bruxelles", "bail_flandre",
    "surendettement_reglement_collectif_dettes",
]

# Étiquette lisible par juridiction
REGION_LABEL = {
    "BE-WAL": "Wallonie", "BE-BRU": "Bruxelles", "BE-VLG": "Flandre",
    "BE": "Belgique (fédéral)",
}


def esc(s):
    return html.escape(str(s if s is not None else ""))


def charger_modules():
    """Charge tous les modules JSON et renvoie une liste de dicts."""
    modules = []
    for fp in sorted(DATA.glob("*.json")):
        if fp.name.startswith("_"):
            continue  # fichiers techniques (ex. _catalogue.json), pas des modules
        with open(fp, encoding="utf-8") as f:
            d = json.load(f)
        d["_slug"] = fp.stem
        d["_module"] = d.get("module", fp.stem)
        modules.append(d)
    # tri selon ORDRE_MODULES puis alpha
    def cle(m):
        mod = m.get("_module", "")
        return (ORDRE_MODULES.index(mod) if mod in ORDRE_MODULES else 999, m.get("titre", ""))
    return sorted(modules, key=cle)


# --- gabarit HTML commun ---
CSS = """
:root{--bleu:#0b3d6e;--bleu2:#11578f;--gris:#f4f6f9;--txt:#1c2733;--muted:#5b6b7b;--bord:#e2e8f0;--ok:#0a7d4f}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--txt);line-height:1.6;background:#fff}
a{color:var(--bleu2);text-decoration:none}
a:hover{text-decoration:underline}
header.site{background:linear-gradient(135deg,var(--bleu),var(--bleu2));color:#fff;padding:1.1rem 1.25rem}
header.site .wrap{max-width:920px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}
header.site a{color:#fff}
.brand{font-weight:700;font-size:1.15rem;letter-spacing:.2px}
.brand small{display:block;font-weight:400;opacity:.85;font-size:.72rem}
nav.top a{margin-left:1rem;font-size:.92rem;opacity:.95}
main{max-width:920px;margin:0 auto;padding:1.5rem 1.25rem 3rem}
.hero{padding:1.5rem 0 .5rem}
.hero h1{font-size:1.8rem;margin:.2rem 0 .4rem;color:var(--bleu)}
.hero p{color:var(--muted);font-size:1.05rem;max-width:640px}
.disclaimer{background:#fff8e6;border:1px solid #f3e2a8;border-radius:10px;padding:.8rem 1rem;margin:1rem 0;font-size:.9rem;color:#6b5710}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1rem;margin-top:1rem}
.card{border:1px solid var(--bord);border-radius:12px;padding:1.1rem;background:#fff;transition:.15s;display:block}
.card:hover{border-color:var(--bleu2);box-shadow:0 4px 18px rgba(11,61,110,.08);text-decoration:none}
.card h3{margin:.1rem 0 .35rem;color:var(--bleu)}
.card .meta{color:var(--muted);font-size:.85rem}
.badge{display:inline-block;background:var(--gris);border:1px solid var(--bord);border-radius:999px;padding:.05rem .55rem;font-size:.74rem;color:var(--muted);margin-right:.3rem}
.fait{border:1px solid var(--bord);border-radius:12px;padding:1.1rem 1.2rem;margin:1rem 0;background:#fff}
.fait h3{margin:.1rem 0 .5rem;color:var(--bleu);font-size:1.12rem}
.fait .ref{font-size:.86rem;color:var(--muted);margin:.5rem 0}
.fait .src{font-size:.86rem;margin-top:.5rem}
.fait .src ul{margin:.3rem 0 0;padding-left:1.1rem}
.fait .date{font-size:.78rem;color:var(--muted);margin-top:.5rem}
.src-officiel{color:var(--ok);font-weight:600}
.alerte{background:#fdecec;border:1px solid #f3b4b4;border-left:5px solid #c0392b;border-radius:8px;padding:.6rem .8rem;margin:.6rem 0;font-size:.9rem;color:#7a1f1f}
.alerte strong{color:#c0392b}
.urgent-card{border:1px solid #f3b4b4;border-left:5px solid #c0392b;border-radius:12px;padding:1rem 1.1rem;margin:1rem 0;background:#fff}
.urgent-card h3{margin:.1rem 0 .4rem;color:#c0392b;font-size:1.05rem}
.urgent-card .lien{font-size:.85rem;margin-top:.4rem}
.contacts{background:#eef6ff;border:1px solid #bcd9f5;border-left:5px solid var(--bleu2);border-radius:8px;padding:.6rem .8rem;margin:.6rem 0;font-size:.9rem}
.contacts ul{margin:.3rem 0 0;padding-left:1.1rem}
.contacts .contact-meta{color:var(--muted);font-size:.85rem}
.search{margin:1.2rem 0}
.search input{width:100%;padding:.7rem .9rem;border:1px solid var(--bord);border-radius:10px;font-size:1rem}
footer.site{border-top:1px solid var(--bord);background:var(--gris);color:var(--muted);font-size:.85rem}
footer.site .wrap{max-width:920px;margin:0 auto;padding:1.3rem 1.25rem}
.back{display:inline-block;margin-bottom:1rem;font-size:.9rem}
h2.sec{color:var(--bleu);border-bottom:2px solid var(--bord);padding-bottom:.3rem;margin-top:2rem}
/* --- Accessibilité (WCAG 2.2) --- */
.skip-link{position:absolute;left:-9999px;top:0;background:#fff;color:var(--bleu);padding:.6rem 1rem;border:2px solid var(--bleu);border-radius:0 0 8px 0;z-index:1000;font-weight:700}
.skip-link:focus{left:0}
a:focus-visible,button:focus-visible,input:focus-visible,[tabindex]:focus-visible{outline:3px solid #ffbf47;outline-offset:2px;border-radius:4px}
.visually-hidden{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.search input{min-height:44px}
.card,.back,nav.top a{min-height:24px}
@media (prefers-reduced-motion: reduce){*{transition:none !important;scroll-behavior:auto !important}}
@media (prefers-color-scheme: dark){
  body{background:#0f1620;color:#e6edf3}
  .card,.fait{background:#161f2b;border-color:#2a3746}
  .badge{background:#1d2733;border-color:#2a3746;color:#aab8c6}
  .card h3,.fait h3,.hero h1,h2.sec{color:#7fb2e6}
  a{color:#7fb2e6}
  footer.site{background:#0c121a;color:#aab8c6}
}
.btn-print{display:inline-block;background:var(--bleu);color:#fff;border:0;border-radius:8px;padding:.55rem 1rem;font-size:.95rem;cursor:pointer;margin:.5rem 0}
.btn-print:hover{background:var(--bleu2)}
/* --- Fiche à emporter : impression propre --- */
@media print{
  header.site,nav.top,footer.site,.search,.skip-link,.back,.btn-print,.disclaimer{display:none !important}
  body{background:#fff;color:#000;font-size:12pt}
  main{max-width:100%;padding:0}
  .fait,.urgent-card{break-inside:avoid;border:1px solid #999}
  .fait a[href^="http"]::after,.src a[href^="http"]::after{content:" — " attr(href);font-size:9pt;color:#333;word-break:break-all}
  h1{font-size:18pt}
  .print-foot{display:block !important;margin-top:1rem;font-size:9pt;color:#333;border-top:1px solid #999;padding-top:.5rem}
}
.print-foot{display:none}
"""

AVERTISSEMENT_GLOBAL = (
    "Information juridique générale, à jour à la date indiquée pour chaque réponse. "
    "Ne constitue pas un conseil juridique individualisé. Pour une situation précise, "
    "consultez un professionnel (avocat, médiateur de dettes agréé, CPAS, Justice de paix)."
)


def page(titre, contenu, actif=""):
    annee = datetime.date.today().year
    def navlink(href, label, key):
        cls = ' style="font-weight:700"' if key == actif else ""
        return f'<a href="{href}"{cls}>{esc(label)}</a>'
    nav = (
        navlink("index.html", "Accueil", "accueil")
        + navlink("urgences.html", "Urgences & délais", "urgences")
        + navlink("specialistes.html", "Nos spécialistes", "specialistes")
        + navlink("textes.html", "Textes de loi", "textes")
        + navlink("sources.html", "Nos sources", "sources")
        + navlink("lexique.html", "Lexique", "lexique")
        + navlink("transparence.html", "Transparence", "transparence")
        + navlink("accessibilite.html", "Accessibilité", "accessibilite")
    )
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(titre)} — La Loi Avec Moi</title>
<meta name="description" content="Informations juridiques belges fiables et sourcées : bail, surendettement, justice.">
<style>{CSS}</style>
</head>
<body>
<a class="skip-link" href="#contenu">Aller au contenu principal</a>
<header class="site"><div class="wrap">
  <a href="index.html" aria-label="La Loi Avec Moi — accueil"><span class="brand">La Loi Avec Moi<small>Le droit belge, clair et sourcé</small></span></a>
  <nav class="top" aria-label="Navigation principale">{nav}</nav>
</div></header>
<main id="contenu" tabindex="-1">
{contenu}
</main>
<footer class="site"><div class="wrap" role="contentinfo">
  <strong>Avertissement.</strong> {esc(AVERTISSEMENT_GLOBAL)}<br><br>
  © {annee} La Loi Avec Moi · Chaque réponse cite ses sources officielles · Contenu généré à partir d'une base vérifiée.
</div></footer>
</body>
</html>"""


def rendre_fait(fait):
    srcs = []
    for s in fait.get("sources", []):
        typ = s.get("type", "")
        cls = "src-officiel" if typ == "officiel" else ""
        tag = "officiel" if typ == "officiel" else "complément"
        srcs.append(
            f'<li><a href="{esc(s.get("url"))}" target="_blank" rel="noopener">{esc(s.get("intitule"))}'
            f'<span class="visually-hidden"> (s\'ouvre dans un nouvel onglet)</span></a> '
            f'<span class="{cls}">[{tag}]</span></li>'
        )
    src_html = ""
    if srcs:
        src_html = '<div class="src"><strong>Sources :</strong><ul>' + "".join(srcs) + "</ul></div>"
    ref = fait.get("reference_legale", "")
    ref_html = f'<div class="ref">⚖️ {esc(ref)}</div>' if ref else ""
    date = fait.get("date_verification", "")
    date_html = f'<div class="date">Vérifié le {esc(date)}</div>' if date else ""
    alerte = fait.get("alerte_delai", "")
    alerte_html = (f'<div class="alerte" role="note">⏱ <strong>À ne pas tarder.</strong> '
                   f'{esc(alerte)}</div>') if alerte else ""
    contacts = fait.get("contacts", [])
    contacts_html = ""
    if contacts:
        items = []
        for c in contacts:
            nom = esc(c.get("nom", ""))
            num = c.get("numero")
            lien = c.get("lien")
            dispo = c.get("dispo")
            pour = c.get("pour")
            tete = f'<strong>{nom}</strong>'
            if num:
                tete += f' — <a href="tel:{esc(num)}">{esc(num)}</a>'
            elif lien:
                tete += (f' — <a href="{esc(lien)}" target="_blank" rel="noopener">site officiel'
                         f'<span class="visually-hidden"> (s\'ouvre dans un nouvel onglet)</span></a>')
            extra = []
            if pour:
                extra.append(esc(pour))
            if dispo:
                extra.append(esc(dispo))
            suff = f' <span class="contact-meta">({" · ".join(extra)})</span>' if extra else ""
            items.append(f"<li>{tete}{suff}</li>")
        contacts_html = ('<div class="contacts"><strong>📞 Qui contacter :</strong><ul>'
                         + "".join(items) + "</ul></div>")
    q = esc(fait.get("question"))
    r = esc(fait.get("reponse"))
    return (
        f'<article class="fait" data-q="{q.lower()}">'
        f"<h3>{q}</h3><p>{r}</p>{alerte_html}{contacts_html}{ref_html}{src_html}{date_html}</article>"
    )


def construire():
    DIST.mkdir(parents=True, exist_ok=True)
    modules = charger_modules()

    # --- page d'accueil ---
    cartes = []
    total_faits = 0
    for m in modules:
        nf = len(m.get("faits", []))
        total_faits += nf
        region = REGION_LABEL.get(m.get("juridiction", ""), m.get("juridiction", ""))
        cartes.append(
            f'<a class="card" href="{esc(m["_slug"])}.html">'
            f'<h3>{esc(m.get("titre", m["_slug"]))}</h3>'
            f'<div class="meta"><span class="badge">{esc(region)}</span>'
            f'<span class="badge">{nf} réponses sourcées</span></div></a>'
        )
    hero = (
        '<section class="hero">'
        "<h1>Le droit belge, clair et sourcé</h1>"
        "<p>Des réponses fiables à vos questions de tous les jours — bail, loyer, "
        "surendettement — chacune accompagnée de sa source officielle et de sa date de vérification.</p>"
        "</section>"
        f'<div class="disclaimer" role="note">ℹ️ {esc(AVERTISSEMENT_GLOBAL)}</div>'
        '<div class="search"><label for="q" class="visually-hidden">Rechercher une thématique</label>'
        '<input id="q" type="search" '
        'aria-label="Rechercher une thématique" '
        'placeholder="Rechercher une question (ex. garantie locative, saisie, préavis)…" '
        'oninput="filtrer()"></div>'
        f'<h2 class="sec">Thématiques ({total_faits} réponses)</h2>'
        f'<div class="cards" id="cards">{"".join(cartes)}</div>'
        # mini recherche client : redirige la frappe vers une page de résultats simple
        "<script>function filtrer(){var v=document.getElementById('q').value.toLowerCase();"
        "var cs=document.querySelectorAll('#cards .card');cs.forEach(function(c){"
        "c.style.display = c.textContent.toLowerCase().indexOf(v)>=0?'':'none';});}</script>"
    )
    (DIST / "index.html").write_text(page("Accueil", hero, actif="accueil"), encoding="utf-8")

    # --- une page par module ---
    for m in modules:
        region = REGION_LABEL.get(m.get("juridiction", ""), m.get("juridiction", ""))
        base = m.get("base_legale_principale", {})
        base_html = ""
        if base:
            url = base.get("source_officielle", "")
            lien = (f' — <a href="{esc(url)}" target="_blank" rel="noopener">source officielle'
                    f'<span class="visually-hidden"> (s\'ouvre dans un nouvel onglet)</span></a>') if url else ""
            base_html = (
                f'<div class="ref">Base légale principale : {esc(base.get("intitule",""))}{lien}</div>'
            )
        faits_html = "".join(rendre_fait(f) for f in m.get("faits", []))
        contenu = (
            '<a class="back" href="index.html">← Toutes les thématiques</a>'
            f'<h1 style="color:#0b3d6e">{esc(m.get("titre", m["_slug"]))}</h1>'
            f'<div class="meta"><span class="badge">{esc(region)}</span>'
            f'<span class="badge">{len(m.get("faits", []))} réponses</span></div>'
            f"{base_html}"
            '<button class="btn-print" onclick="window.print()" '
            'aria-label="Imprimer cette fiche pour l\'emporter">🖨️ Imprimer / emporter cette fiche</button>'
            '<div class="search"><label for="qf" class="visually-hidden">Filtrer les questions de cette page</label>'
            '<input id="qf" type="search" aria-label="Filtrer les questions de cette page" '
            'placeholder="Filtrer dans cette page…" '
            'oninput="var v=this.value.toLowerCase();document.querySelectorAll(\'.fait\').forEach('
            "function(a){a.style.display=a.dataset.q.indexOf(v)>=0?'':'none';});\"></div>"
            f"{faits_html}"
            '<div class="print-foot">La Loi Avec Moi — information générale vérifiée à partir de '
            "sources officielles. Ne remplace pas un conseil juridique individualisé. "
            "Les versions officielles des textes font foi.</div>"
        )
        (DIST / f"{m['_slug']}.html").write_text(
            page(m.get("titre", m["_slug"]), contenu), encoding="utf-8"
        )

    # --- page transparence ---
    nb_off = nb_sec = 0
    for m in modules:
        for f in m.get("faits", []):
            for s in f.get("sources", []):
                if s.get("type") == "officiel":
                    nb_off += 1
                else:
                    nb_sec += 1
    transp = (
        '<a class="back" href="index.html">← Accueil</a>'
        '<h1 style="color:#0b3d6e">Transparence & fiabilité</h1>'
        "<p>Nous croyons qu'une information juridique n'a de valeur que si elle est "
        "<strong>traçable</strong>. Voici nos règles, sans rien cacher.</p>"
        '<h2 class="sec">Nos engagements</h2>'
        "<ul>"
        "<li>Chaque réponse cite <strong>au moins une source officielle</strong> (texte de loi, "
        "administration publique) et porte une <strong>date de vérification</strong>.</li>"
        "<li>Les sources sont classées : <span class='src-officiel'>[officiel]</span> "
        "(loi, service public) ou [complément] (sources secondaires de qualité, en appui).</li>"
        "<li>Le site est généré <strong>automatiquement à partir d'une base vérifiée</strong> : "
        "il ne peut pas afficher une information non sourcée.</li>"
        "</ul>"
        f'<h2 class="sec">Comptage des sources</h2>'
        f"<p>{nb_off} sources officielles · {nb_sec} sources de complément.</p>"
        '<h2 class="sec">Limites (en toute honnêteté)</h2>'
        "<ul>"
        "<li>Le droit évolue : certaines dates d'entrée en vigueur peuvent être réajustées. "
        "En cas de doute, la source officielle liée fait foi.</li>"
        "<li>Ce site donne une information <strong>générale</strong>, pas un conseil "
        "individualisé. Pour votre cas précis, consultez un professionnel.</li>"
        "</ul>"
        f'<div class="disclaimer">⚖️ {esc(AVERTISSEMENT_GLOBAL)}</div>'
    )
    (DIST / "transparence.html").write_text(
        page("Transparence", transp, actif="transparence"), encoding="utf-8"
    )

    # --- page déclaration d'accessibilité ---
    today = datetime.date.today().isoformat()
    acc = (
        '<a class="back" href="index.html">← Accueil</a>'
        '<h1 style="color:#0b3d6e">Déclaration d\'accessibilité</h1>'
        "<p>Nous voulons que <strong>toute personne</strong>, y compris en situation de "
        "handicap, puisse accéder à l'information juridique. L'accessibilité n'est pas une "
        "option : c'est une question de dignité — et, en Europe, une <strong>obligation légale</strong>.</p>"
        '<h2 class="sec">Cadre légal (ce à quoi on se réfère)</h2>'
        "<ul>"
        "<li><strong>European Accessibility Act</strong> (directive UE 2019/882), applicable "
        "depuis le 28 juin 2025 : de nombreux services numériques doivent être accessibles.</li>"
        "<li><strong>WCAG 2.2</strong> (niveau AA visé) et la norme européenne <strong>EN 301 549</strong>.</li>"
        "</ul>"
        '<h2 class="sec">Ce qui est déjà en place</h2>'
        "<ul>"
        "<li>Langue de la page déclarée, structure par titres, repères (<code>main</code>, navigation, pied de page).</li>"
        "<li>Lien « aller au contenu », focus clairement visible au clavier, cibles tactiles agrandies.</li>"
        "<li>Champs de recherche avec étiquettes ; liens ouvrant un nouvel onglet signalés aux lecteurs d'écran.</li>"
        "<li>Respect du « mouvement réduit » et prise en charge du <strong>mode sombre</strong> (confort visuel).</li>"
        "<li>Texte agrandissable (zoom non bloqué), contrastes renforcés.</li>"
        "<li>Un <strong>audit d'accessibilité automatique</strong> est lancé à chaque génération du site.</li>"
        "</ul>"
        '<h2 class="sec">Limites & engagement (honnêtement)</h2>'
        "<ul>"
        "<li>Notre audit automatique ne remplace pas un test par de vraies personnes "
        "(lecteur d'écran, navigation clavier, handicap cognitif) : c'est notre prochaine étape.</li>"
        "<li>Si une page vous pose problème, dites-le nous : nous corrigerons en priorité.</li>"
        "</ul>"
        f"<p style='color:var(--muted);font-size:.85rem'>Déclaration revue le {esc(today)}. "
        "Objectif visé : WCAG 2.2 niveau AA.</p>"
    )
    (DIST / "accessibilite.html").write_text(
        page("Accessibilité", acc, actif="accessibilite"), encoding="utf-8"
    )

    # --- page Urgences & délais (besoins immédiats d'abord) ---
    urgents = []
    for m in modules:
        for f in m.get("faits", []):
            if f.get("alerte_delai"):
                urgents.append((m, f))
    cartes_u = []
    for m, f in urgents:
        cartes_u.append(
            '<div class="urgent-card">'
            f'<h3>⏱ {esc(f.get("question"))}</h3>'
            f'<p><strong>À ne pas tarder :</strong> {esc(f.get("alerte_delai"))}</p>'
            f'<p class="lien"><a href="{esc(m["_slug"])}.html">Lire la réponse complète et les sources →</a></p>'
            "</div>"
        )
    urg = (
        '<a class="back" href="index.html">← Accueil</a>'
        '<h1 style="color:#c0392b">Urgences &amp; délais</h1>'
        "<p>Certaines situations n'attendent pas : un délai manqué peut coûter cher. "
        "Voici les cas où il faut <strong>agir vite</strong>. En cas de doute, contactez sans tarder "
        "un avocat (au besoin via l'aide juridique gratuite), un médiateur de dettes agréé ou un CPAS.</p>"
        f'<div class="disclaimer" role="note">ℹ️ {esc(AVERTISSEMENT_GLOBAL)}</div>'
        + ("".join(cartes_u) if cartes_u
           else "<p>Aucune alerte de délai enregistrée pour le moment.</p>")
    )
    (DIST / "urgences.html").write_text(
        page("Urgences & délais", urg, actif="urgences"), encoding="utf-8"
    )

    # --- page Textes de loi (crédibilité : la source légale officielle) ---
    textes = []
    tx = DATA / "_textes_legaux.json"
    if tx.exists():
        textes = json.loads(tx.read_text(encoding="utf-8")).get("textes", [])
    lignes_tx = []
    for t in textes:
        arts = t.get("articles_cles", [])
        arts_html = ("<br><span class='contact-meta'>" + esc(" · ".join(arts)) + "</span>") if arts else ""
        lignes_tx.append(
            '<div class="urgent-card" style="border-left-color:#0b3d6e">'
            f'<h3 style="color:#0b3d6e">{esc(t.get("nom",""))}</h3>'
            f'<div class="meta"><span class="badge">{esc(t.get("niveau",""))}</span></div>'
            f'<p class="lien"><a href="{esc(t.get("url"))}" target="_blank" rel="noopener">'
            "Lire le texte officiel (consolidé)"
            "<span class=\"visually-hidden\"> (s'ouvre dans un nouvel onglet)</span></a></p>"
            f"{arts_html}</div>"
        )
    txt = (
        '<a class="back" href="index.html">← Accueil</a>'
        '<h1 style="color:#0b3d6e">Textes de loi</h1>'
        "<p>La crédibilité, c'est pouvoir <strong>vérifier à la source</strong>. Voici les textes "
        "légaux officiels (versions consolidées) derrière nos réponses. Chaque réponse cite l'article "
        "applicable ; ici vous accédez au texte complet.</p>"
        f'<div class="disclaimer" role="note">ℹ️ Les versions officielles font foi. {esc(AVERTISSEMENT_GLOBAL)}</div>'
        + ("".join(lignes_tx) if lignes_tx else "<p>Registre en construction.</p>")
    )
    (DIST / "textes.html").write_text(
        page("Textes de loi", txt, actif="textes"), encoding="utf-8"
    )

    # --- page Lexique (langage clair / accessibilité cognitive) ---
    termes = []
    lx = DATA / "_lexique.json"
    if lx.exists():
        termes = json.loads(lx.read_text(encoding="utf-8")).get("termes", [])
    termes = sorted(termes, key=lambda t: t.get("terme", "").lower())
    lignes_lx = []
    for t in termes:
        dom = t.get("domaine", "")
        dom_html = f'<span class="badge">{esc(dom)}</span>' if dom else ""
        lignes_lx.append(
            '<article class="fait" data-q="' + esc(t.get("terme", "")).lower() + ' '
            + esc(t.get("definition", "")).lower() + '">'
            f'<h3>{esc(t.get("terme",""))}</h3>'
            f'<p>{esc(t.get("definition",""))}</p>'
            f'<div class="meta">{dom_html}</div></article>'
        )
    lex = (
        '<a class="back" href="index.html">← Accueil</a>'
        '<h1 style="color:#0b3d6e">Lexique en langage clair</h1>'
        "<p>Le droit utilise des mots compliqués. Ici, on les explique <strong>simplement</strong>. "
        "Cette page sert tout le monde — et particulièrement les personnes pour qui le jargon est un obstacle.</p>"
        '<div class="search"><label for="ql" class="visually-hidden">Rechercher un terme</label>'
        '<input id="ql" type="search" aria-label="Rechercher un terme" '
        'placeholder="Rechercher un terme (ex. préavis, saisie, prescription)…" '
        'oninput="var v=this.value.toLowerCase();document.querySelectorAll(\'.fait\').forEach('
        "function(a){a.style.display=a.dataset.q.indexOf(v)>=0?'':'none';});\"></div>"
        f'<p class="contact-meta">{len(termes)} termes expliqués</p>'
        + "".join(lignes_lx)
    )
    (DIST / "lexique.html").write_text(
        page("Lexique", lex, actif="lexique"), encoding="utf-8"
    )

    # --- page Nos spécialistes (un assistant guidé par domaine) ---
    specs = []
    sp = REPO / "data" / "governance" / "specialistes.json"
    if sp.exists():
        specs = json.loads(sp.read_text(encoding="utf-8")).get("specialistes", [])
    cartes_sp = []
    for s in specs:
        contacts = s.get("contacts_cles", [])
        cont_html = ""
        if contacts:
            items = []
            for c in contacts[:4]:
                num = f" — {esc(c.get('numero'))}" if c.get("numero") else ""
                items.append(f"<li>{esc(c.get('nom',''))}{num}</li>")
            cont_html = "<ul>" + "".join(items) + "</ul>"
        cartes_sp.append(
            '<div class="urgent-card" style="border-left-color:#0b3d6e">'
            f'<h3 style="color:#0b3d6e">{esc(s.get("titre",""))}</h3>'
            f'<p>{esc(s.get("mission",""))}</p>'
            f'<div class="meta"><span class="badge">{s.get("nb_reponses",0)} réponses sourcées</span></div>'
            f'{cont_html}'
            f'<p class="contact-meta">{esc(s.get("gouvernance",""))}</p></div>'
        )
    spg = (
        '<a class="back" href="index.html">← Accueil</a>'
        '<h1 style="color:#0b3d6e">Nos spécialistes</h1>'
        "<p>Pour chaque domaine, un <strong>spécialiste</strong> (assistant guidé) vous aide à "
        "comprendre et à <strong>faire valoir vos droits</strong>, à partir de sources officielles. "
        "Ce sont des assistants guidés, pas des avocats : en cas de doute, ils vous orientent vers un professionnel.</p>"
        + "".join(cartes_sp)
    )
    (DIST / "specialistes.html").write_text(
        page("Nos spécialistes", spg, actif="specialistes"), encoding="utf-8"
    )

    # --- page Nos sources fiables (l'endroit central des sources) ---
    tr = REPO / "data" / "governance" / "trusted_sources.json"
    wl = json.loads(tr.read_text(encoding="utf-8")) if tr.exists() else {}
    t1 = sorted(wl.get("tier1_officiel", []))
    t2 = sorted(wl.get("tier2_institutionnel", []))
    def doms(lst):
        return "".join(f'<li><a href="https://{esc(d)}" target="_blank" rel="noopener">{esc(d)}'
                       "<span class=\"visually-hidden\"> (s'ouvre dans un nouvel onglet)</span></a></li>"
                       for d in lst)
    srcpage = (
        '<a class="back" href="index.html">← Accueil</a>'
        '<h1 style="color:#0b3d6e">Nos sources fiables</h1>'
        "<p>La confiance, ça se vérifie. Tout notre contenu s'appuie sur des sources "
        "<strong>officielles</strong> (lois, administrations publiques). Voici les sources de référence du site.</p>"
        f'<h2 class="sec">Sources officielles (autorités publiques) — {len(t1)}</h2>'
        f"<ul>{doms(t1)}</ul>"
        f'<h2 class="sec">Sources institutionnelles (en appui) — {len(t2)}</h2>'
        f"<ul>{doms(t2)}</ul>"
        '<p class="contact-meta">Les textes de loi complets sont accessibles depuis la page '
        '<a href="textes.html">Textes de loi</a>. Le détail de notre méthode figure sur la page '
        '<a href="transparence.html">Transparence</a>.</p>'
    )
    (DIST / "sources.html").write_text(
        page("Nos sources", srcpage, actif="sources"), encoding="utf-8"
    )

    return {
        "modules": len(modules),
        "faits": total_faits,
        "sources_officielles": nb_off,
        "sources_complement": nb_sec,
        "urgences": len(urgents),
        "pages": len(modules) + 8,
    }


if __name__ == "__main__":
    stats = construire()
    print("═══ La Loi Avec Moi — site généré ═══")
    print(f"  Modules : {stats['modules']}")
    print(f"  Réponses (faits) : {stats['faits']}")
    print(f"  Sources officielles : {stats['sources_officielles']} | complément : {stats['sources_complement']}")
    print(f"  Pages HTML produites : {stats['pages']}")
    print(f"  → {DIST}")
    print("✓ Site prêt. Déployable tel quel (statique).")
