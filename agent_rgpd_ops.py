"""
AGENT RGPD OPÉRATIONNEL [91] — Conformité GDPR pour projets clients belges
Registres de traitements, politiques confidentialité, DPA, audit RGPD.

Usage : python agent_rgpd_ops.py
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

IDENTITE = """# AGENT RGPD OPÉRATIONNEL — Caelum Partners

## IDENTITÉ
Tu es l'expert RGPD (GDPR) de Caelum Partners.
Tu assures la conformité des projets IA pour les clients belges, selon le Règlement (UE) 2016/679.
Autorité de contrôle belge : Autorité de Protection des Données (APD) — apd-gba.be

## CONTEXTE BELGIQUE
- APD (Autorité Protection des Données) : contrôle et sanctions
- Sanctions : jusqu'à 20M€ ou 4% du CA mondial annuel
- Obligation de désigner un DPO si traitement à grande échelle
- Délai de notification violation : 72h à l'APD
- Charte ePrivacy belge : cookies, marketing électronique

## CAELUM PARTNERS — POSITION RGPD
- Rôle : RESPONSABLE DU TRAITEMENT pour ses propres données
- Rôle : SOUS-TRAITANT pour les données des clients de ses clients
- Obligation : DPA (Data Processing Agreement) avec chaque client
- Les agents IA traitent des données → audit RGPD systématique

## DOCUMENTS RGPD FONDAMENTAUX
1. Registre des activités de traitement (RAT) — Article 30 RGPD
2. Politique de confidentialité — obligation légale site web
3. DPA (Data Processing Agreement) — contrat sous-traitant
4. DPIA (Data Protection Impact Assessment) — si traitement à risque élevé
5. Mentions légales et cookies — obligation Belgique

## BASES LÉGALES DE TRAITEMENT (Article 6)
- Consentement (6.1.a) : formulaire opt-in explicite
- Contrat (6.1.b) : nécessaire pour exécuter le contrat
- Obligation légale (6.1.c) : comptabilité, TVA
- Intérêt légitime (6.1.f) : prospection B2B (avec opt-out)"""


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
    os.makedirs("fichiers/rgpd", exist_ok=True)
    fichier = f"fichiers/rgpd/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def politique_confidentialite():
    print("\n  Pour qui générer la politique (ex: Caelum Partners / nom client) :")
    entite = input("  Entité → ").strip() or "Caelum Partners"
    print("  Types de données traitées (ex: emails, noms, données comptables) :")
    donnees = input("  Données → ").strip() or "nom, email, données professionnelles"
    r = streamer(
        f"""Génère une POLITIQUE DE CONFIDENTIALITÉ RGPD complète et conforme pour :
Entité : {entite}
Données traitées : {donnees}
Pays : Belgique (APD comme autorité de contrôle)

Sections obligatoires :
1. Identité et coordonnées du responsable du traitement
2. Types de données collectées et finalités
3. Base légale de chaque traitement (Article 6 RGPD)
4. Durée de conservation des données
5. Partage des données avec des tiers
6. Transferts hors UE (le cas échéant)
7. Droits des personnes concernées (accès, rectification, effacement, portabilité)
8. Cookies et traceurs (avec tableau des cookies)
9. Contact DPD/DPO et APD
10. Date et version

Langue : Français. Format : document professionnel prêt à publier.""",
        f"POLITIQUE CONFIDENTIALITÉ — {entite}"
    )
    sauvegarder(f"politique_confidentialite_{entite.replace(' ', '_')}", r)


def registre_traitements():
    print("\n  Nom de l'organisation :")
    org = input("  Organisation → ").strip() or "Caelum Partners"
    print("  Secteur d'activité :")
    secteur = input("  Secteur → ").strip() or "Services IA / Automation"
    r = streamer(
        f"""Génère un REGISTRE DES ACTIVITÉS DE TRAITEMENT (Article 30 RGPD) pour :
Organisation : {org}
Secteur : {secteur}

Format tableau pour chaque traitement :
| Finalité | Catégories de données | Personnes concernées | Base légale | Durée conservation | Destinataires | Mesures sécurité |

Traitements à inclure pour {org} :
1. Gestion clients et prospects (CRM)
2. Facturation et comptabilité
3. Communication email et newsletter
4. Site web et analytics
5. Recrutement éventuel
6. Sous-traitance pour clients (data clients des clients)

Inclure : mesures techniques et organisationnelles de sécurité.""",
        f"REGISTRE TRAITEMENTS — {org}"
    )
    sauvegarder(f"registre_{org.replace(' ', '_')}", r)


def dpa_client():
    print("\n  Nom du client Caelum (responsable du traitement) :")
    client_nom = input("  Client → ").strip()
    print("  Type de traitement que Caelum fait pour ce client :")
    traitement = input("  Traitement → ").strip() or "automation emails, traitement données clients"
    if not client_nom:
        return
    r = streamer(
        f"""Génère un DPA (Data Processing Agreement / Accord de sous-traitance) entre :
- RESPONSABLE DU TRAITEMENT : {client_nom}
- SOUS-TRAITANT : Caelum Partners (Chaima Mhadbi, Bruxelles)
- Traitement effectué : {traitement}

Clauses obligatoires (Article 28 RGPD) :
1. Objet, nature, finalité et durée du traitement
2. Instructions documentées du responsable
3. Confidentialité des personnes autorisées
4. Mesures de sécurité (Article 32)
5. Sous-traitance ultérieure (conditions)
6. Droit d'audit du responsable
7. Assistance pour exercice des droits
8. Retour/suppression des données en fin de contrat
9. Notification des violations de données
10. Signatures et date

Format : contrat juridique prêt à signer, droit belge applicable.""",
        f"DPA — {client_nom}"
    )
    sauvegarder(f"dpa_{client_nom.replace(' ', '_')}", r)


def audit_projet_ia():
    print("\n  Décris le projet IA que tu vas développer pour le client :")
    projet = input("  Projet → ").strip()
    print("  Secteur du client :")
    secteur = input("  Secteur → ").strip() or "PME"
    if not projet:
        return
    r = streamer(
        f"""AUDIT RGPD PRÉLIMINAIRE pour ce projet IA :
Projet : {projet}
Secteur client : {secteur}

Analyse :
1. DONNÉES PERSONNELLES IMPLIQUÉES : quelles catégories ? (ordinaires / sensibles Art. 9 ?)
2. DPIA REQUISE ? (évaluation d'impact — obligatoire si traitement à risque élevé)
3. BASE LÉGALE RECOMMANDÉE pour chaque traitement
4. RISQUES RGPD SPÉCIFIQUES à ce projet IA (biais, profilage, décision automatisée)
5. MESURES TECHNIQUES OBLIGATOIRES (chiffrement, anonymisation, pseudonymisation)
6. DOCUMENTS À PRÉPARER avant lancement
7. POINTS D'ATTENTION SECTEUR {secteur.upper()} (spécificités légales)
8. FEUX VERTS : ce qui est conforme sans modification
9. FEUX ROUGES : ce qui doit être corrigé avant déploiement

Format : rapport d'audit structuré.""",
        f"AUDIT RGPD PROJET IA — {secteur}"
    )
    sauvegarder(f"audit_rgpd_{secteur.replace(' ', '_')}", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  RGPD OPÉRATIONNEL — Caelum Partners")
    print("  Conformité GDPR · Belgique · APD")
    print("═"*65)

    while True:
        print("\n  1. Politique de confidentialité (site web / client)")
        print("  2. Registre des activités de traitement (RAT)")
        print("  3. DPA / Accord de sous-traitance client")
        print("  4. Audit RGPD d'un projet IA")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            politique_confidentialite()
        elif choix == "2":
            registre_traitements()
        elif choix == "3":
            dpa_client()
        elif choix == "4":
            audit_projet_ia()
        else:
            print("  Choix invalide.")
