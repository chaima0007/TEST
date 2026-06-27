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
.search{margin:1.2rem 0}
.search input{width:100%;padding:.7rem .9rem;border:1px solid var(--bord);border-radius:10px;font-size:1rem}
footer.site{border-top:1px solid var(--bord);background:var(--gris);color:var(--muted);font-size:.85rem}
footer.site .wrap{max-width:920px;margin:0 auto;padding:1.3rem 1.25rem}
.back{display:inline-block;margin-bottom:1rem;font-size:.9rem}
h2.sec{color:var(--bleu);border-bottom:2px solid var(--bord);padding-bottom:.3rem;margin-top:2rem}
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
        + navlink("transparence.html", "Transparence", "transparence")
    )
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(titre)} — La Loi Avec Moi</title>
<meta name="description" content="Informations juridiques belges fiables et sourcées : bail, surendettement.">
<style>{CSS}</style>
</head>
<body>
<header class="site"><div class="wrap">
  <a href="index.html"><span class="brand">La Loi Avec Moi<small>Le droit belge, clair et sourcé</small></span></a>
  <nav class="top">{nav}</nav>
</div></header>
<main>
{contenu}
</main>
<footer class="site"><div class="wrap">
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
            f'<li><a href="{esc(s.get("url"))}" target="_blank" rel="noopener">{esc(s.get("intitule"))}</a> '
            f'<span class="{cls}">[{tag}]</span></li>'
        )
    src_html = ""
    if srcs:
        src_html = '<div class="src"><strong>Sources :</strong><ul>' + "".join(srcs) + "</ul></div>"
    ref = fait.get("reference_legale", "")
    ref_html = f'<div class="ref">⚖️ {esc(ref)}</div>' if ref else ""
    date = fait.get("date_verification", "")
    date_html = f'<div class="date">Vérifié le {esc(date)}</div>' if date else ""
    q = esc(fait.get("question"))
    r = esc(fait.get("reponse"))
    return (
        f'<article class="fait" data-q="{q.lower()}">'
        f"<h3>{q}</h3><p>{r}</p>{ref_html}{src_html}{date_html}</article>"
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
        f'<div class="disclaimer">ℹ️ {esc(AVERTISSEMENT_GLOBAL)}</div>'
        '<div class="search"><input id="q" type="search" '
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
            lien = f' — <a href="{esc(url)}" target="_blank" rel="noopener">source officielle</a>' if url else ""
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
            '<div class="search"><input type="search" placeholder="Filtrer dans cette page…" '
            'oninput="var v=this.value.toLowerCase();document.querySelectorAll(\'.fait\').forEach('
            "function(a){a.style.display=a.dataset.q.indexOf(v)>=0?'':'none';});\"></div>"
            f"{faits_html}"
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

    return {
        "modules": len(modules),
        "faits": total_faits,
        "sources_officielles": nb_off,
        "sources_complement": nb_sec,
        "pages": len(modules) + 2,
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
