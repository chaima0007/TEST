"""
AGENT SEO & RÉFÉRENCEMENT WEB
Optimise ta présence en ligne, génère du contenu Google-friendly,
analyse ta concurrence SEO et positionne ton entreprise sur le web.

Usage : python agent_seo.py
"""

import os
import sys
import json
from datetime import datetime
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] set GEMINI_API_KEY=ta_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

ENTREPRISE = {
    "nom": "AgentClaude Solutions",
    "secteur": "Intelligence Artificielle — Agents autonomes",
    "services": ["Agents IA sur mesure", "Migration code legacy", "Audit sécurité IA", "Formation agents Claude"],
    "cible": "PME, startups tech, DSI grandes entreprises",
    "zone": "Europe francophone",
    "url": "agentclaude.com",
}


def _creer_model(model_name=None, system_instruction="", generation_config=None, **kwargs):
    """Compatibilité: retourne un proxy GenerativeModel pour google.genai."""
    class _ModelProxy:
        def __init__(self, mn, si, cfg):
            self.model_name = mn or MODEL
            self.system_instruction = si
            self.config = cfg or types.GenerateContentConfig(temperature=0.3, max_output_tokens=2000)
            if isinstance(self.config, types.GenerateContentConfig):
                self.config = types.GenerateContentConfig(
                    system_instruction=si,
                    temperature=self.config.temperature if hasattr(self.config, 'temperature') else 0.3,
                    max_output_tokens=self.config.max_output_tokens if hasattr(self.config, 'max_output_tokens') else 2000,
                )
        def generate_content(self, prompt, stream=False):
            if stream:
                return client.models.generate_content_stream(
                    model=self.model_name, contents=prompt, config=self.config)
            return client.models.generate_content(
                model=self.model_name, contents=prompt, config=self.config)
    config = generation_config
    if config and not isinstance(config, types.GenerateContentConfig):
        config = types.GenerateContentConfig(
            temperature=getattr(config, 'temperature', 0.3),
            max_output_tokens=getattr(config, 'max_output_tokens', 2000),
        )
    return _ModelProxy(model_name, system_instruction, config)


def stream(instructions, prompt, label):
    print(f"\n{'─'*60}\n  ► {label}\n{'─'*60}\n")
    model = _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(temperature=0.5, max_output_tokens=2048),
    )
    reponse = ""
    try:
        for chunk in model.generate_content(prompt, stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        reponse = f"[Erreur : {e}]"
        print(reponse)
    print()
    return reponse


def sauvegarder(nom, contenu):
    os.makedirs("seo_output", exist_ok=True)
    fichier = f"seo_output/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")
    return fichier


# ─────────────────────────────────────────────────────────────
# AGENT 1 : RECHERCHE DE MOTS-CLÉS
# ─────────────────────────────────────────────────────────────

def agent_mots_cles(sujet=""):
    sujet = sujet or f"{ENTREPRISE['secteur']} {ENTREPRISE['zone']}"
    resultat = stream(
        """Tu es un expert SEO spécialisé en IA et tech B2B.
Génère une liste de mots-clés structurée :

## MOTS-CLÉS PRINCIPAUX (volume fort)
## MOTS-CLÉS LONGUE TRAÎNE (intention d'achat)
## MOTS-CLÉS INFORMATIONNELS (blog, contenu)
## MOTS-CLÉS CONCURRENTIELS (vs concurrents)
## QUESTIONS FRÉQUENTES (pour featured snippets)

Pour chaque mot-clé : volume estimé, difficulté (facile/moyen/difficile), intention (info/commercial/transactionnel)""",
        f"Entreprise : {ENTREPRISE['nom']}\nSecteur : {ENTREPRISE['secteur']}\nServices : {', '.join(ENTREPRISE['services'])}\nCible : {ENTREPRISE['cible']}\nSujet : {sujet}",
        "Recherche de Mots-Clés SEO"
    )
    sauvegarder("mots_cles", resultat)
    return resultat


# ─────────────────────────────────────────────────────────────
# AGENT 2 : GÉNÉRATEUR D'ARTICLES DE BLOG SEO
# ─────────────────────────────────────────────────────────────

def agent_article_blog(sujet, mot_cle_principal):
    resultat = stream(
        """Tu es un rédacteur SEO expert en IA et technologie B2B.
Écris un article de blog optimisé SEO :
- Titre H1 avec le mot-clé principal (60 caractères max)
- Meta description (155 caractères max, avec CTA)
- Introduction avec le mot-clé dans les 100 premiers mots
- Structure H2/H3 logique (minimum 5 sections)
- 800-1200 mots, ton expert mais accessible
- Inclure des statistiques et chiffres crédibles
- CTA final vers les services
- Balises schema.org suggérées
- Maillage interne suggéré (3 articles liés)""",
        f"Sujet : {sujet}\nMot-clé principal : {mot_cle_principal}\nEntreprise : {ENTREPRISE['nom']}\nServices : {', '.join(ENTREPRISE['services'])}",
        f"Article Blog SEO — {sujet}"
    )
    sauvegarder(f"article_{sujet[:30].replace(' ','_')}", resultat)
    return resultat


# ─────────────────────────────────────────────────────────────
# AGENT 3 : OPTIMISATION PAGE WEB
# ─────────────────────────────────────────────────────────────

def agent_optimiser_page(type_page, contenu_actuel=""):
    resultat = stream(
        """Tu es un expert en on-page SEO et conversion.
Génère le contenu SEO complet pour la page :
- Title tag (60 chars max)
- Meta description (155 chars max)
- H1 optimisé
- Structure complète H2/H3
- Texte optimisé (inclure mots-clés naturellement)
- Schema.org JSON-LD approprié
- Open Graph tags (pour partage social)
- Recommandations Core Web Vitals
- Liens internes suggérés""",
        f"Type de page : {type_page}\nEntreprise : {ENTREPRISE['nom']}\nURL : {ENTREPRISE['url']}\nServices : {', '.join(ENTREPRISE['services'])}\nContenu actuel : {contenu_actuel[:500] if contenu_actuel else 'Nouveau contenu à créer'}",
        f"Optimisation Page — {type_page}"
    )
    sauvegarder(f"page_{type_page.replace(' ','_')}", resultat)
    return resultat


# ─────────────────────────────────────────────────────────────
# AGENT 4 : STRATÉGIE GOOGLE MY BUSINESS & LOCAL SEO
# ─────────────────────────────────────────────────────────────

def agent_google_business():
    resultat = stream(
        """Tu es un expert en référencement local et Google My Business.
Génère une stratégie complète :
## Fiche Google My Business
- Description optimisée (750 chars)
- Catégories recommandées
- Services à lister
- Posts GMB hebdomadaires (4 exemples)
- Questions/Réponses à préparer (5 FAQ)
## Avis clients
- Template email demande d'avis
- Réponses types aux avis positifs/négatifs
## Citations locales
- Annuaires où s'inscrire (top 10)
## Signaux locaux
- Mentions NAP cohérentes recommandées""",
        f"Entreprise : {ENTREPRISE['nom']}\nSecteur : {ENTREPRISE['secteur']}\nZone : {ENTREPRISE['zone']}\nServices : {', '.join(ENTREPRISE['services'])}",
        "Stratégie Google My Business & SEO Local"
    )
    sauvegarder("google_my_business", resultat)
    return resultat


# ─────────────────────────────────────────────────────────────
# AGENT 5 : AUDIT SEO COMPLET
# ─────────────────────────────────────────────────────────────

def agent_audit_seo(url=""):
    url = url or ENTREPRISE["url"]
    resultat = stream(
        """Tu es un auditeur SEO senior.
Produis un audit SEO complet structuré :

## SCORE GLOBAL /100
## TECHNIQUE (Core Web Vitals, mobile, HTTPS, sitemap, robots.txt)
## CONTENU (qualité, mots-clés, structure, fraîcheur)
## AUTORITÉ (backlinks, domaine, citations)
## EXPÉRIENCE UTILISATEUR (navigation, CTA, conversion)
## TOP 10 ACTIONS PRIORITAIRES (classées par impact/effort)
## ROADMAP 3 MOIS (actions semaine par semaine)

Sois précis et actionnable.""",
        f"URL à auditer : {url}\nEntreprise : {ENTREPRISE['nom']}\nSecteur : {ENTREPRISE['secteur']}\nConcurrents principaux : agents-ia.com, automatisation-ia.fr",
        f"Audit SEO Complet — {url}"
    )
    sauvegarder("audit_seo", resultat)
    return resultat


# ─────────────────────────────────────────────────────────────
# AGENT 6 : PLAN DE CONTENU 3 MOIS
# ─────────────────────────────────────────────────────────────

def agent_plan_contenu():
    resultat = stream(
        """Tu es un stratège content marketing spécialisé en SaaS/IA B2B.
Génère un plan de contenu sur 3 mois :

Pour chaque semaine :
- 1 article de blog (titre + mot-clé + angle)
- 2 posts LinkedIn (sujet + format : carousel/texte/vidéo)
- 1 email newsletter (sujet + objectif)

Inclure aussi :
## PILIERS DE CONTENU (5 thèmes récurrents)
## FORMATS PRIORITAIRES par canal
## KPIs à suivre (trafic, leads, engagement)
## Outils recommandés (gratuits en priorité)""",
        f"Entreprise : {ENTREPRISE['nom']}\nCible : {ENTREPRISE['cible']}\nServices : {', '.join(ENTREPRISE['services'])}\nObjectif : générer des leads qualifiés en Europe francophone",
        "Plan de Contenu 3 Mois"
    )
    sauvegarder("plan_contenu_3mois", resultat)
    return resultat


# ─────────────────────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  AGENT SEO & RÉFÉRENCEMENT — AgentClaude Solutions")
    print("═"*60)

    while True:
        print("\n  1. Recherche de mots-clés")
        print("  2. Générer un article de blog SEO")
        print("  3. Optimiser une page web")
        print("  4. Stratégie Google My Business")
        print("  5. Audit SEO complet")
        print("  6. Plan de contenu 3 mois")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            break
        elif choix == "1":
            sujet = input("  Sujet spécifique (Entrée pour général) → ").strip()
            agent_mots_cles(sujet)
        elif choix == "2":
            sujet = input("  Sujet de l'article → ").strip()
            mot_cle = input("  Mot-clé principal → ").strip()
            agent_article_blog(sujet, mot_cle)
        elif choix == "3":
            page = input("  Type de page (accueil/service/contact/blog) → ").strip()
            agent_optimiser_page(page)
        elif choix == "4":
            agent_google_business()
        elif choix == "5":
            url = input("  URL à auditer (Entrée pour défaut) → ").strip()
            agent_audit_seo(url)
        elif choix == "6":
            agent_plan_contenu()
        else:
            print("  Choix invalide.")
