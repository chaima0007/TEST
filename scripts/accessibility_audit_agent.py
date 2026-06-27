#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent d'AUDIT D'ACCESSIBILITÉ — La Loi Avec Moi.

Contrôle automatiquement le site généré (apps/loi-avec-moi/dist/*.html) contre
une série de critères WCAG 2.2 vérifiables sans navigateur.

Honnêteté : un audit automatique NE remplace PAS un test humain (lecteur d'écran,
clavier, handicap cognitif). Il attrape les erreurs mécaniques fréquentes ;
les limites sont affichées telles quelles.

Sortie : data/governance/accessibility_report.md
"""
import re
import pathlib
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
DIST = REPO / "apps" / "loi-avec-moi" / "dist"
OUT = REPO / "data" / "governance" / "accessibility_report.md"


def auditer_page(nom, html):
    """Renvoie (liste_succes, liste_echecs) pour une page."""
    ok, ko = [], []

    def check(cond, libelle):
        (ok if cond else ko).append(libelle)

    # 1. Langue déclarée (WCAG 3.1.1)
    check(re.search(r'<html[^>]*\blang="[a-zA-Z-]+"', html), "Langue de page déclarée (lang)")

    # 2. Titre de page (WCAG 2.4.2)
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    check(bool(t and t.group(1).strip()), "Titre de page présent et non vide")

    # 3. Viewport sans blocage du zoom (WCAG 1.4.4)
    vp = re.search(r'name="viewport"\s+content="([^"]*)"', html)
    if vp:
        c = vp.group(1).lower()
        check("user-scalable=no" not in c and "maximum-scale=1" not in c,
              "Zoom non bloqué (viewport)")
    else:
        ko.append("Balise viewport absente")

    # 4. Un seul <h1> (WCAG 1.3.1 / bonne pratique)
    nb_h1 = len(re.findall(r"<h1[\s>]", html))
    check(nb_h1 == 1, f"Exactement un titre h1 (trouvé : {nb_h1})")

    # 5. Lien d'évitement (WCAG 2.4.1)
    check('class="skip-link"' in html or "skip-link" in html, "Lien « aller au contenu »")

    # 6. Repère principal main avec cible (WCAG 1.3.1 / 2.4.1)
    check('id="contenu"' in html and "<main" in html, "Repère <main> ciblable présent")

    # 7. Images : toutes avec alt (WCAG 1.1.1)
    imgs = re.findall(r"<img\b[^>]*>", html)
    sans_alt = [i for i in imgs if not re.search(r"\balt=", i)]
    check(len(sans_alt) == 0, f"Images avec texte alternatif ({len(imgs)} img, {len(sans_alt)} sans alt)")

    # 8. Champs de formulaire étiquetés (WCAG 1.3.1 / 4.1.2)
    inputs = re.findall(r"<input\b[^>]*>", html)
    non_etiquetes = []
    for inp in inputs:
        has_aria = re.search(r'aria-label="[^"]+"', inp)
        idm = re.search(r'id="([^"]+)"', inp)
        has_label = idm and (f'for="{idm.group(1)}"' in html)
        if not (has_aria or has_label):
            non_etiquetes.append(inp[:40])
    check(len(non_etiquetes) == 0, f"Champs de saisie étiquetés ({len(inputs)} champ(s))")

    # 9. Liens avec intitulé non vide (WCAG 2.4.4)
    liens = re.findall(r"<a\b[^>]*>(.*?)</a>", html, re.S)
    vides = [l for l in liens if not re.sub(r"<[^>]+>", "", l).strip()]
    check(len(vides) == 0, f"Liens avec intitulé ({len(liens)} lien(s), {len(vides)} vide(s))")

    # 10. Nouvelles fenêtres signalées (WCAG 3.2.5)
    blanks = re.findall(r"<a\b[^>]*target=\"_blank\"[^>]*>(.*?)</a>", html, re.S)
    non_signales = [b for b in blanks if "nouvel onglet" not in b and "nouvelle fenêtre" not in b]
    check(len(non_signales) == 0,
          f"Ouvertures dans un nouvel onglet signalées ({len(blanks)} lien(s) _blank)")

    return ok, ko


def construire():
    pages = sorted(DIST.glob("*.html"))
    par_page = []
    total_ok = total_ko = 0
    for p in pages:
        html = p.read_text(encoding="utf-8")
        ok, ko = auditer_page(p.name, html)
        total_ok += len(ok)
        total_ko += len(ko)
        par_page.append((p.name, ok, ko))

    today = date.today().isoformat()
    L = []
    L.append("# Rapport d'audit d'accessibilité (WCAG 2.2)")
    L.append("")
    L.append(f"*Généré le {today} sur {len(pages)} page(s). Audit automatique : "
             "attrape les erreurs mécaniques, ne remplace pas un test humain.*")
    L.append("")
    L.append(f"**Contrôles réussis : {total_ok} · à corriger : {total_ko}**")
    L.append("")
    for nom, ok, ko in par_page:
        etat = "✅" if not ko else "⚠️"
        L.append(f"## {etat} {nom}")
        for x in ok:
            L.append(f"- ✅ {x}")
        for x in ko:
            L.append(f"- ❌ {x}")
        L.append("")
    L.append("## Limite honnête")
    L.append("- Test humain requis ensuite : lecteur d'écran (NVDA/VoiceOver), "
             "navigation 100% clavier, lisibilité pour handicap cognitif (langage simple).")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    return len(pages), total_ok, total_ko


if __name__ == "__main__":
    nb_pages, total_ok, total_ko = construire()
    print("═══ AGENT D'AUDIT D'ACCESSIBILITÉ (WCAG 2.2) ═══")
    print(f"  Pages auditées : {nb_pages}")
    print(f"  Contrôles réussis : {total_ok} | à corriger : {total_ko}")
    print(f"  → {OUT}")
    if total_ko == 0:
        print("✓ Tous les contrôles automatiques passent (test humain recommandé ensuite).")
    else:
        print("⚠️  Des points d'accessibilité sont à corriger.")
