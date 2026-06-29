#!/usr/bin/env python3
"""
deploy_controller.py — Contrôleur de mise en place (P-MISE-EN-PLACE).

Donne un GO / NO-GO clair pour mettre les sites en ligne. Il distingue :
  • ce qui est PRÊT automatiquement (contenu viable, sources, templates d'env, sécurité) ;
  • ce qui dépend d'une DÉCISION HUMAINE de Chaima (domaines, identité légale, webhook, prix, coûts).

Il NE déploie pas (aucune action irréversible) : il contrôle l'état et écrit un rapport.

Usage : python3 scripts/deploy_controller.py
"""
import json
import os
import re
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_MD = os.path.join(BASE, "data", "governance", "mise_en_place_report.md")


def existe(*parts):
    return os.path.exists(os.path.join(BASE, *parts))


def lire(*parts):
    try:
        with open(os.path.join(BASE, *parts), encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def main():
    auto = []   # (ok, libellé)
    humain = []  # (fait, libellé)

    # 1) Contenu viable (rapport du content_controller)
    try:
        cc = json.load(open(os.path.join(BASE, "data", "governance", "content_control_report.json"), encoding="utf-8"))
        ok = cc.get("global_ok", False)
        details = " · ".join(f"{r['projet']} {r['viabilite_pct']}%" for r in cc.get("rapports", []))
        auto.append((ok, f"Contenu viable ({details})"))
    except Exception:
        auto.append((False, "Contenu viable — lancer d'abord content_controller.py"))

    # 2) Templates d'environnement
    auto.append((existe("env.example"), "Modèle d'env Caelum (env.example)"))
    auto.append((existe("laloiavecmoi", "env.example"), "Modèle d'env La Loi Avec Moi (laloiavecmoi/env.example)"))

    # 3) Guides
    auto.append((existe("DEPLOIEMENT.md"), "Guide de déploiement (DEPLOIEMENT.md)"))
    auto.append((existe("GO_NO_GO.md"), "Rapport GO/NO-GO"))

    # 4) Sécurité : pas de mot de passe en dur dans la route de login
    login = lire("app", "api", "auth", "login", "route.ts")
    pas_de_secret = ('?? "demo' not in login) and ("demo123" not in login)
    auto.append((pas_de_secret, "Sécurité : aucun mot de passe démo en dur"))

    # 5) Pages SEO générées (au moins quelques modules)
    n_modules = len([f for f in glob.glob(os.path.join(BASE, "laloiavecmoi", "data", "belgium", "*.json"))
                     if not os.path.basename(f).startswith("_")])
    auto.append((n_modules >= 100, f"Base juridique étoffée ({n_modules} modules)"))

    # --- Décisions humaines ---
    # Identité légale (La Loi Avec Moi)
    ident = lire("laloiavecmoi", "data", "identite.ts")
    ident_ok = "[à compléter]" not in ident and bool(ident)
    humain.append((ident_ok, "Identité légale de l'éditeur complétée (laloiavecmoi/data/identite.ts)"))
    # Les autres décisions ne peuvent pas être déduites du code sans risque d'invention :
    humain.append((False, "Hébergement + noms de domaine choisis"))
    humain.append((False, "Webhook leads (LEADS_WEBHOOK_URL) branché chez l'hébergeur"))
    humain.append((False, "Prix des offres Caelum fixés"))
    humain.append((False, "Coûts réels renseignés (data/cost_model.json)"))

    auto_ok = all(ok for ok, _ in auto)
    humain_ok = all(ok for ok, _ in humain)

    # Rapport
    L = ["# 🚀 Contrôleur de mise en place (GO / NO-GO)", ""]
    L.append("## ✅ Prêt automatiquement (technique / contenu / sécurité)")
    for ok, lib in auto:
        L.append(f"- {'✅' if ok else '⛔'} {lib}")
    L.append("")
    L.append("## ⏳ Décisions de Chaima (ne peuvent pas être inventées)")
    for ok, lib in humain:
        L.append(f"- {'✅' if ok else '⏳'} {lib}")
    L.append("")
    L.append("---")
    if auto_ok and humain_ok:
        verdict = "🟢 GO — tout est prêt, déploiement possible."
    elif auto_ok:
        verdict = "🟡 GO TECHNIQUE — prêt côté système ; en attente des décisions de Chaima."
    else:
        verdict = "🔴 NO-GO — corriger d'abord les points techniques ⛔ ci-dessus."
    L.append(f"**Verdict : {verdict}**")
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(L) + "\n")

    print("═══ CONTRÔLEUR DE MISE EN PLACE ═══")
    print(f"  Prêt auto : {sum(ok for ok,_ in auto)}/{len(auto)}  ·  Décisions Chaima : {sum(ok for ok,_ in humain)}/{len(humain)}")
    print(f"  {verdict}")
    print(f"  → rapport : data/governance/mise_en_place_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
