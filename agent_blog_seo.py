"""
AGENT BLOG & SEO [85] — Contenu SEO pour caelumpartners.agency
Articles de blog, méta-descriptions, mots-clés, plan éditorial mensuel.

Usage : python agent_blog_seo.py
"""

import os
import sys
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.0-flash"

IDENTITE = """# AGENT BLOG & SEO — Caelum Partners

## IDENTITÉ
Tu es l'expert SEO et content marketing de Caelum Partners.
Tu crées du contenu qui positionne Caelum Partners en tête des résultats Google pour les PME belges cherchant de l'aide IA.

## SITE WEB
- URL : caelumpartners.agency
- Hébergé : Cloudflare Pages
- Marché : PME belges, Bruxelles, Wallonie, Luxembourg

## MOTS-CLÉS CIBLES
- Primaires : "automation IA PME Belgique", "intelligence artificielle entreprise Bruxelles"
- Secondaires : "automatiser factures", "chatbot PME belge", "gain de temps IA"
- Longue traîne : "comment automatiser mes relances clients", "IA pour cabinet comptable belge"

## STRUCTURE ARTICLE SEO OPTIMAL
1. Titre H1 : mot-clé principal + promesse (60 caractères max)
2. Introduction : accroche + problème + solution en 100 mots
3. Corps : H2/H3, paragraphes courts, exemples concrets, chiffres
4. Sections FAQ (rich snippets Google)
5. Conclusion : résumé + CTA vers contact@caelumpartners.agency
6. Méta-description : 155 caractères max, mot-clé + CTA

## FORMAT
- Longueur cible : 800-1200 mots (assez pour SEO, pas trop long pour mobile)
- Langue : Français (marché belge FR)
- Ton : expert mais accessible, jamais trop technique
- Images suggérées : alt-text inclus"""


def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE,
                temperature=0.35,
                max_output_tokens=3500,
            ),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/blog_seo", exist_ok=True)
    fichier = f"fichiers/blog_seo/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def article_blog():
    print("\n  Sujet de l'article (ex: 'comment automatiser ses relances clients') :")
    sujet = input("  Sujet → ").strip()
    print("  Secteur cible (ex: cabinet comptable, restaurant, tous secteurs) :")
    secteur = input("  Secteur → ").strip() or "PME belges"
    if not sujet:
        return
    r = streamer(
        f"""Écris un ARTICLE DE BLOG SEO COMPLET pour caelumpartners.agency :
Sujet : {sujet}
Secteur cible : {secteur}

Format :
- Titre H1 optimisé SEO
- Méta-description (155 caractères max)
- Introduction accrocheuse (150 mots)
- 3-4 sections H2 avec contenu substantiel
- 1 section FAQ (3-5 questions/réponses)
- Conclusion + CTA vers contact@caelumpartners.agency
- Suggestion d'image principale avec alt-text

Intégrer naturellement les mots-clés SEO cibles.""",
        f"ARTICLE BLOG — {sujet[:40]}"
    )
    sauvegarder(f"article_{sujet[:20].replace(' ', '_')}", r)


def plan_editorial():
    print("\n  Mois cible (ex: Juillet 2026) :")
    mois = input("  Mois → ").strip() or datetime.now().strftime("%B %Y")
    r = streamer(
        f"""Crée un PLAN ÉDITORIAL SEO pour caelumpartners.agency — {mois}

4 articles pour le mois :

Pour chaque article :
SEMAINE X :
- Titre H1 optimisé
- Mot-clé principal
- Intention de recherche (informationnelle / commerciale / transactionnelle)
- Angle unique (pourquoi cet article fera la différence)
- Section FAQ incluse (3 questions)
- Lien interne suggéré (vers quelle autre page du site)
- CTA final

Inclure 1 article par secteur : tous secteurs / secteur spécifique / HORECA ou autre / légal ou comptable.""",
        f"PLAN ÉDITORIAL — {mois}"
    )
    sauvegarder(f"plan_editorial_{mois.replace(' ', '_')}", r)


def audit_seo():
    print("\n  URL ou page à auditer (ou 'homepage' pour la page d'accueil) :")
    page = input("  Page → ").strip() or "homepage caelumpartners.agency"
    r = streamer(
        f"""Effectue un AUDIT SEO simulé pour : {page} de caelumpartners.agency

Vérifie et donne les recommandations pour :
1. TECHNIQUE : vitesse, mobile-first, HTTPS, robots.txt, sitemap
2. ON-PAGE : H1, méta-title, méta-description, structure H2/H3
3. CONTENU : densité mots-clés, longueur, FAQ, liens internes
4. BACKLINKS : stratégie d'acquisition (annuaires belges, partenaires, presse locale)
5. LOCAL SEO : Google My Business (à créer), mentions NAP cohérentes

Format : problème → impact → solution prioritaire (facile/moyen/difficile)""",
        f"AUDIT SEO — {page}"
    )
    sauvegarder(f"audit_seo_{page[:20].replace(' ', '_')}", r)


def faq_seo():
    print("\n  Thème de la FAQ (ex: 'tarifs IA', 'délai de livraison', 'automatisation') :")
    theme = input("  Thème → ").strip() or "services Caelum Partners"
    r = streamer(
        f"""Génère une FAQ SEO OPTIMISÉE sur le thème : {theme}

10 questions/réponses au format :
**Q : [Question exacte que tape un client sur Google]**
R : [Réponse courte 50-100 mots, naturelle, avec mot-clé intégré]

Les questions doivent cibler des rich snippets Google (Position 0).
Inclure : prix, délais, fonctionnement, comparaison avec concurrents, garanties.""",
        f"FAQ SEO — {theme}"
    )
    sauvegarder(f"faq_{theme[:20].replace(' ', '_')}", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  BLOG & SEO — Caelum Partners")
    print("  Contenu · Référencement · Autorité Google")
    print("═"*65)

    while True:
        print("\n  1. Écrire un article de blog SEO")
        print("  2. Plan éditorial mensuel (4 articles)")
        print("  3. Audit SEO de la page")
        print("  4. FAQ SEO optimisée (rich snippets)")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            article_blog()
        elif choix == "2":
            plan_editorial()
        elif choix == "3":
            audit_seo()
        elif choix == "4":
            faq_seo()
        else:
            print("  Choix invalide.")
