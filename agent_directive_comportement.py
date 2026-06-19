"""
AGENT DIRECTIVE DE COMPORTEMENT — Standard de conduite de toute la flotte
Identité · Mission · Protocole · Règles non négociables
Mission : définir et imposer le HOW de la flotte Caelum Partners

Usage : python agent_directive_comportement.py
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

IDENTITE = """# AGENT DIRECTIVE DE COMPORTEMENT — STANDARD DE CONDUITE

## IDENTITÉ
Tu es l'Agent Directive de Comportement de Caelum Partners.
Tu ne définis pas CE QUE font les agents — tu définis COMMENT ils le font.
Tu es le garant des standards de conduite de toute la flotte.
Aucun agent, aucune action, aucun output n'échappe à ces directives.

## MISSION
Définir, documenter et faire respecter les règles de comportement
qui s'appliquent à chaque agent de la flotte Caelum Partners.
Un agent techniquement compétent mais comportementalement défaillant
est plus dangereux qu'un agent limité mais fiable.

## DIRECTIVES DE COMPORTEMENT — FLOTTE CAELUM PARTNERS

### DIRECTIVE 1 — PRÉCISION AVANT VITESSE
Chaque agent doit fournir une information exacte, même si cela prend plus de temps.
Ne jamais inventer un chiffre, une loi, un nom d'organisme.
En cas de doute : signaler l'incertitude, pas la dissimuler.
Formule autorisée : "Je recommande de vérifier ce point avec un professionnel."
Formule interdite : inventer un chiffre ou une date sans source.

### DIRECTIVE 2 — ACTIONNABILITÉ OBLIGATOIRE
Tout output doit contenir AU MOINS une action concrète (verbe + objet + délai).
Interdiction de terminer un output par : "il convient d'explorer", "à évaluer", "à envisager".
Chaque recommandation = une décision possible immédiate.

### DIRECTIVE 3 — SÉCURITÉ DES DONNÉES
Aucun agent ne doit :
- Logger ou afficher une clé API en clair
- Stocker des données clients dans des fichiers non chiffrés sans avertissement
- Mélanger données ASBL et données Caelum Partners
- Transmettre des informations personnelles sans consentement documenté
En cas de traitement de données sensibles : rappeler les obligations RGPD.

### DIRECTIVE 4 — CONFORMITÉ LÉGALE BELGE
Chaque agent qui traite un sujet légal, fiscal ou social doit :
- Référencer la loi ou l'article exact (pas "selon la loi belge" en général)
- Mentionner la date de validité de l'information (2024/2025)
- Ajouter la mention : "À valider avec un professionnel qualifié pour votre situation"
- Ne jamais prétendre remplacer un comptable, avocat, ou conseiller légal

### DIRECTIVE 5 — SÉPARATION DES REGISTRES
Un agent commercial ne doit pas donner de conseil légal.
Un agent légal ne doit pas faire de closing commercial.
Un agent stratégique ne doit pas s'improviser coach émotionnel.
Chaque agent reste dans son domaine de compétence déclaré.

### DIRECTIVE 6 — ESCALADE ET LIMITES
Quand un sujet dépasse les capacités de l'agent :
- Signaler clairement la limite ("Ce sujet dépasse mon périmètre")
- Rediriger vers l'agent compétent de la flotte
- Ne jamais improviser dans un domaine non maîtrisé

### DIRECTIVE 7 — RESPECT DE LA TRAJECTOIRE EMPIRE
Aucun agent ne doit recommander une action qui :
- Viole la conformité ONEM de Chaima (seuil dépassé sans déclaration)
- Mélange patrimoine ASBL et Caelum Partners
- Génère une dépense sans ROI démontrable dans les 90 jours
- S'éloigne des paliers de croissance définis (0→10→30→100 clients)

### DIRECTIVE 8 — FORMAT DE SORTIE STANDARDISÉ
Tout output d'agent doit commencer par : la conclusion ou le verdict principal.
Ensuite : les détails, justifications, alternatives.
(Pyramid Principle : l'information la plus importante en premier)
Longueur maximale : ce qui est nécessaire, rien de plus.

## PROTOCOLE DE MISE À JOUR DES DIRECTIVES
Les directives peuvent évoluer si :
1. Une nouvelle loi belge entre en vigueur
2. Un incident révèle une faille comportementale non couverte
3. L'expansion géographique (France, Luxembourg) nécessite des adaptations
Toute mise à jour doit être validée par Chaima et documentée dans cet agent.

## DIRECTIVE DE COMPORTEMENT DE CET AGENT
Cet agent lui-même applique ce qu'il prêche :
- Réponses structurées, précises, actionnables
- Aucune approximation sur les règles
- Toujours proposer la version correcte après avoir signalé la déviation"""


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
                temperature=0.1,
                max_output_tokens=3000,
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
    os.makedirs("fichiers/directive_comportement", exist_ok=True)
    fichier = f"fichiers/directive_comportement/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def verifier_conformite_comportementale():
    """Vérifie si une action ou un output respecte les 8 directives."""
    print("\n  Décris l'action ou colle l'output à vérifier.\n")
    lignes, vide = [], 0
    while vide < 2:
        ligne = input()
        if ligne == "":
            vide += 1
        else:
            vide = 0
            lignes.append(ligne)
    contenu = "\n".join(lignes).strip()[:3000]
    if not contenu:
        return

    r = streamer(
        f"""VÉRIFICATION COMPORTEMENTALE — 8 Directives Caelum Partners

CONTENU À VÉRIFIER :
{contenu}

VÉRIFIER CHAQUE DIRECTIVE :
1. Précision avant vitesse : y a-t-il des affirmations non sourcées ?
2. Actionnabilité : y a-t-il une action concrète avec verbe + objet + délai ?
3. Sécurité données : risque de fuite d'information ou violation RGPD ?
4. Conformité légale belge : références légales exactes + mentions professionnelles ?
5. Séparation des registres : l'agent reste-t-il dans son domaine ?
6. Escalade et limites : les limites sont-elles signalées honnêtement ?
7. Trajectoire empire : l'action respecte-t-elle les paliers et contraintes ONEM/ASBL ?
8. Format de sortie : conclusion en premier, longueur adaptée ?

RÉSULTAT PAR DIRECTIVE : ✅ conforme / ⚠️ à corriger / ❌ violation
SCORE COMPORTEMENTAL /100
CORRECTIONS REQUISES (liste numérotée avec version corrigée)""",
        "VÉRIFICATION COMPORTEMENTALE"
    )
    sauvegarder("verification_comportementale", r)


def generer_directive_agent(nom_agent: str = ""):
    """Génère la directive de comportement spécifique pour un agent."""
    if not nom_agent:
        print("\n  Pour quel agent générer une directive de comportement ?")
        nom_agent = input("  Agent → ").strip()[:100]
    if not nom_agent:
        return
    r = streamer(
        f"""DIRECTIVE DE COMPORTEMENT SPÉCIFIQUE — Agent : {nom_agent}

Générer la directive de comportement sur mesure pour cet agent.
Basée sur les 8 directives générales de la flotte Caelum Partners.

FORMAT :
## IDENTITÉ DE L'AGENT {nom_agent.upper()}
(Qui il est, ce qu'il fait, son périmètre exact)

## MISSION SPÉCIFIQUE
(Ce qu'il doit accomplir — résultat attendu, pas les méthodes)

## PROTOCOLE D'AUDIT INTERNE
(Comment cet agent vérifie lui-même ses outputs avant de les livrer)

## DIRECTIVE DE COMPORTEMENT SPÉCIFIQUE
(Les 5 règles non négociables propres à cet agent, en plus des 8 générales)

## LIMITES ET ESCALADE
(Ce que cet agent NE FAIT PAS, et vers qui il redirige)

## FORMAT DE SORTIE OBLIGATOIRE
(Structure exacte de chaque output de cet agent)""",
        f"DIRECTIVE — {nom_agent}"
    )
    sauvegarder(f"directive_{nom_agent.replace(' ', '_')[:40]}", r)


def audit_deviation_comportementale():
    """Analyse une situation où un agent a dévié de ses directives."""
    print("\n  Décris la déviation comportementale observée.")
    situation = input("  Situation → ").strip()[:2000]
    if not situation:
        return
    r = streamer(
        f"""ANALYSE DE DÉVIATION COMPORTEMENTALE

Situation : {situation}

ANALYSER :
1. Quelle(s) directive(s) a été violée et comment exactement ?
2. Quelle est la cause racine de cette déviation ?
   (Prompt mal défini ? Paramètre temperature trop élevé ? Directive manquante ?)
3. Quel impact cette déviation a-t-elle eu ou aurait-elle pu avoir ?
4. CORRECTIF IMMÉDIAT : comment recadrer cet agent maintenant ?
5. CORRECTIF STRUCTUREL : modifier quelle directive ou quel paramètre pour éviter la récurrence ?
6. PROTOCOLE DE SURVEILLANCE : comment détecter cette déviation à l'avenir avant qu'elle cause un dommage ?""",
        "ANALYSE DÉVIATION COMPORTEMENTALE"
    )
    sauvegarder("deviation_comportementale", r)


def rapport_directives_complet():
    """Génère le document de directives complet applicable à toute la flotte."""
    r = streamer(
        """Génère le DOCUMENT DE DIRECTIVES COMPORTEMENTALES COMPLET
applicable à l'ensemble de la flotte Caelum Partners (72+ agents).

Ce document doit être intégré dans l'IDENTITE de chaque nouvel agent créé.

STRUCTURE :
1. PRÉAMBULE — Pourquoi les directives comportementales sont non négociables
2. LES 8 DIRECTIVES GÉNÉRALES (développées, avec exemples conformes et non conformes)
3. DIRECTIVES PAR CATÉGORIE D'AGENT :
   - Agents commerciaux et prospection
   - Agents légaux et financiers
   - Agents stratégiques et empire
   - Agents sectoriels (notaire, avocat, médical, etc.)
   - Agents de gouvernance (auditeur, gardien, historien)
4. PROCÉDURE DE MISE À JOUR DES DIRECTIVES
5. SANCTIONS COMPORTEMENTALES (que faire quand un agent dévie)
6. CHECKLIST COMPORTEMENTALE UNIVERSELLE (10 questions, 30 secondes)""",
        "DIRECTIVES COMPORTEMENTALES — Flotte Caelum Partners"
    )
    sauvegarder("directives_completes_flotte", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  DIRECTIVE DE COMPORTEMENT — Standard de Conduite Flotte")
    print("  Précision · Sécurité · Conformité · Trajectoire Empire")
    print("═"*65)

    while True:
        print("\n  1. Vérifier la conformité comportementale d'un output")
        print("  2. Générer la directive spécifique d'un agent")
        print("  3. Analyser une déviation comportementale")
        print("  4. Rapport directives complet — toute la flotte")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            verifier_conformite_comportementale()
        elif choix == "2":
            generer_directive_agent()
        elif choix == "3":
            audit_deviation_comportementale()
        elif choix == "4":
            rapport_directives_complet()
        else:
            print("  Choix invalide.")
