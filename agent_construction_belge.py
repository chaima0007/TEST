"""
AGENT SECTEUR CONSTRUCTION & ARCHITECTURE BELGIQUE — Devis, rapports de chantier, conformité
Usage : python agent_construction_belge.py
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

IDENTITE = """
Tu es un assistant IA spécialisé pour les entreprises belges du secteur de la construction, les architectes et les chefs de projet.
La Belgique compte plus de 80 000 entreprises de construction générant plus de 30 milliards d'euros de chiffre d'affaires annuel.
Tu maîtrises parfaitement la réglementation belge : permis d'urbanisme, Loi Breyne (protection acheteurs sur plan), certificat PEB (Performance Énergétique des Bâtiments), règles PLACI pour l'amiante, et la coordination de sécurité obligatoire pour les chantiers de plus de 500 m².
Tu connais les organismes sectoriels belges : Constructiv (fonds social sectoriel), FIEC, CCT Construction, et les assurances décennales obligatoires.
Tu rédiges des documents professionnels en français belge : devis, rapports d'avancement, correspondances avec sous-traitants, checklists de conformité.
Tu appliques les structures contractuelles standards du secteur belge : acomptes 30/30/30/10, garanties légales, responsabilités décennales et quinquennales.
Tu connais les types de chantiers courants : rénovation, construction neuve, transformation, extension, ainsi que les corps de métier (HVAC, plomberie, électricité) nécessitant chacun des permis spécifiques.
Tu sais que la coordination de sécurité-santé est obligatoire dès qu'il y a plus d'un entrepreneur et que le chantier dépasse certains seuils.
Tu intègres les références aux normes NBN, aux PV de réception provisoire et définitive, et aux garanties biennales sur les équipements.
Un entrepreneur SME belge gère en moyenne 10 à 30 chantiers simultanément et consacre 30 % de son temps aux tâches administratives.
Tu aides à transformer ce temps perdu en valeur : un entrepreneur facturant 80€/h économise 1 200€/mois avec tes documents professionnels.
Caelum Partners propose des forfaits à 500€, 1 500€ et 3 000€ pour les entreprises de construction belges.
Tu génères des documents prêts à envoyer au client, au sous-traitant ou à l'administration communale belge.
Ton ton est professionnel, précis, juridiquement solide et adapté aux usages belges francophones.
Tu mentionnes systématiquement les références légales pertinentes (Loi Breyne, Code wallon du Logement, RRU bruxellois si applicable).
Tu structures chaque document avec des sections claires, numérotées, avec entêtes et pieds de page professionnels.
Tu adaptes le contenu selon la région belge si précisé : Bruxelles-Capitale, Wallonie ou Flandre (réglementations régionales différentes).
"""

def sanitize(texte: str) -> str:
    return texte.strip()[:3000]

def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.2, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse

def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/construction_belge", exist_ok=True)
    fichier = f"fichiers/construction_belge/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def generer_devis_construction():
    print("\n  — Génération d'un devis construction professionnel —")
    type_projet = sanitize(input("  Type de projet (ex: rénovation salle de bains, construction neuve, extension) : "))
    scope = sanitize(input("  Description des travaux (surfaces, prestations principales) : "))
    client_nom = sanitize(input("  Nom du client / maître d'ouvrage : "))
    duree = sanitize(input("  Durée estimée des travaux : "))
    loi_breyne = input("  Projet soumis à la Loi Breyne ? (o/n) : ").strip().lower()

    prompt = f"""Génère un devis de construction professionnel complet pour une entreprise belge.

PARAMÈTRES DU PROJET :
- Type de projet : {type_projet}
- Scope des travaux : {scope}
- Client / Maître d'ouvrage : {client_nom}
- Durée estimée : {duree}
- Soumis à la Loi Breyne : {"Oui" if loi_breyne == "o" else "Non"}

Le devis doit inclure :
1. En-tête professionnel (entreprise émettrice, date, numéro de devis, validité 30 jours)
2. Identification complète du maître d'ouvrage et du chantier
3. Description détaillée des travaux par postes (démolition, gros œuvre, second œuvre, finitions)
4. Tableau de prix unitaires et forfaitaires par poste
5. Récapitulatif HT / TVA 6% (rénovation >10 ans) ou 21% (neuf) / TTC
6. Structure d'acomptes : 30% à la commande / 30% à mi-chantier / 30% à la réception provisoire / 10% à la réception définitive
7. Garanties légales : responsabilité décennale (art. 1792 CC), garantie biennale sur équipements
8. Clause Loi Breyne si applicable (montant maximal acompte, assurance achèvement obligatoire)
9. Conditions générales : délais de paiement, pénalités de retard, clause de révision des prix
10. Mentions légales obligatoires (numéro TVA, numéro BCE, assurance RC, Constructiv)

Ton : professionnel, précis, juridiquement rigoureux. Format prêt à envoyer au client."""

    resultat = streamer(prompt, "DEVIS CONSTRUCTION BELGE")
    sauvegarder("devis_construction", resultat)

def rapport_avancement_chantier():
    print("\n  — Rapport d'avancement de chantier —")
    projet = sanitize(input("  Nom / référence du projet : "))
    semaine = sanitize(input("  Numéro de semaine / période : "))
    travaux_realises = sanitize(input("  Travaux réalisés cette période : "))
    problemes = sanitize(input("  Problèmes / retards / blocages rencontrés : "))
    prochaines_etapes = sanitize(input("  Prochaines étapes prévues : "))

    prompt = f"""Génère un rapport d'avancement de chantier professionnel bipartite (client + interne) pour une entreprise de construction belge.

DONNÉES DU CHANTIER :
- Projet : {projet}
- Période : Semaine {semaine}
- Travaux réalisés : {travaux_realises}
- Problèmes / Retards : {problemes}
- Prochaines étapes : {prochaines_etapes}

Génère DEUX documents distincts :

DOCUMENT 1 — RAPPORT CLIENT (ton professionnel, rassurant, axé résultats) :
- En-tête avec logo fictif, date, référence chantier
- Résumé exécutif : avancement global en %
- Travaux réalisés cette semaine (liste structurée par corps de métier)
- Points d'attention et solutions mises en œuvre
- Planning semaine suivante
- Photos prévues / demandes d'informations client
- Signature chef de projet

DOCUMENT 2 — LOG INTERNE (ton factuel, technique) :
- Heures prestées par équipe
- Matériaux consommés vs prévu
- Problèmes techniques détaillés et actions correctives
- Impacts planning et budget
- Alertes sous-traitants
- Points à escalader à la direction

Format : sections claires, professionnel, prêt à envoyer."""

    resultat = streamer(prompt, "RAPPORT D'AVANCEMENT CHANTIER")
    sauvegarder("rapport_avancement", resultat)

def lettre_sous_traitant(situation: str = ""):
    print("\n  — Correspondance sous-traitant —")
    if not situation:
        print("  Situations possibles :")
        print("  a) Bon de commande / ordre de mission")
        print("  b) Retard de livraison")
        print("  c) Non-conformité qualité")
        print("  d) Réception finale des travaux sous-traités")
        situation = sanitize(input("  Décrivez la situation (ou entrez a/b/c/d) : "))
    sous_traitant = sanitize(input("  Nom et coordonnées du sous-traitant : "))
    details = sanitize(input("  Détails spécifiques de la situation : "))
    projet_ref = sanitize(input("  Référence du projet / chantier : "))

    situations_types = {
        "a": "bon de commande et ordre de mission",
        "b": "mise en demeure pour retard de livraison",
        "c": "signalement de non-conformité qualité avec demande de correction",
        "d": "procès-verbal de réception des travaux sous-traités"
    }
    type_lettre = situations_types.get(situation.lower(), situation)

    prompt = f"""Génère une lettre professionnelle de correspondance avec un sous-traitant belge de construction.

CONTEXTE :
- Type de courrier : {type_lettre}
- Sous-traitant : {sous_traitant}
- Projet / Chantier : {projet_ref}
- Détails : {details}

La lettre doit inclure :
1. En-tête professionnel (expéditeur, destinataire, date, référence)
2. Objet clair et précis
3. Corps structuré : rappel du contrat, faits constatés, demande précise avec délai
4. Références légales pertinentes (CCT Construction, Code Civil belge, cahier des charges)
5. Clause de réserve si applicable (réception avec réserves)
6. Mention des pénalités contractuelles si retard/non-conformité
7. Formule de politesse professionnelle et signature
8. Mentions : ASBL Constructiv, numéro ONSS, obligations sociales sous-traitant

Ton : ferme mais professionnel, juridiquement rigoureux, en français belge standard."""

    resultat = streamer(prompt, f"LETTRE SOUS-TRAITANT — {type_lettre.upper()}")
    sauvegarder("lettre_sous_traitant", resultat)

def checklist_conformite_chantier():
    print("\n  — Checklist de conformité réglementaire belge —")
    type_projet = sanitize(input("  Type de projet (rénovation / construction neuve / extension / transformation) : "))
    phase = sanitize(input("  Phase du projet (avant-projet / permis / démarrage / en cours / réception) : "))
    region = sanitize(input("  Région (Bruxelles / Wallonie / Flandre) : "))
    surface = sanitize(input("  Surface approximative (m²) : "))

    prompt = f"""Génère une checklist de conformité réglementaire complète pour un projet de construction belge.

PROJET :
- Type : {type_projet}
- Phase actuelle : {phase}
- Région : {region}
- Surface : {surface} m²

La checklist doit couvrir, par catégorie :

1. PERMIS & AUTORISATIONS
   - Permis d'urbanisme (délais, documents requis, autorité compétente selon région)
   - Permis d'environnement si applicable
   - Notification de chantier CPPT

2. PERFORMANCE ÉNERGÉTIQUE (PEB)
   - Responsable PEB désigné ?
   - Déclaration PEB initiale déposée ?
   - Certificat PEB final prévu ?

3. SÉCURITÉ & COORDINATION
   - Coordination de sécurité obligatoire si >500m² ou >1 entrepreneur ?
   - Plan de sécurité et de santé (PSS) disponible ?
   - Journal de coordination tenu ?

4. AMIANTE (PLACI)
   - Inventaire amiante réalisé pour bâtiment >1978 ?
   - Entreprise agréée PLACI si amiante détecté ?

5. OBLIGATIONS SOCIALES
   - Enregistrement Constructiv (déclaration préalable chantier)
   - Vérification sous-traitants (statut social, TVA, assurance)
   - Limosa pour travailleurs détachés

6. ASSURANCES
   - RC décennale contractant
   - Tous risques chantier
   - Assurance achèvement (Loi Breyne si applicable)

7. RÉCEPTION
   - PV réception provisoire avec/sans réserves
   - Délai de garantie (1 an petits défauts, 10 ans gros œuvre)
   - Dossier As-Built et plans conformes à l'exécution

Format : tableau avec ✅ / ⚠️ / ❌ / N/A pour chaque item, avec colonnes Responsable et Délai."""

    resultat = streamer(prompt, "CHECKLIST CONFORMITÉ RÉGLEMENTAIRE BELGE")
    sauvegarder("checklist_conformite", resultat)

def kit_prospection_construction():
    prompt = """Génère un kit de prospection commercial complet pour Caelum Partners ciblant les PME belges du secteur construction.

Le kit doit contenir :

1. EMAIL DE PROSPECTION (objet + corps, 200 mots max)
   - Accroche sur la douleur réelle : "Vous passez 30% de votre temps sur l'admin au lieu de facturer"
   - Preuve : un entrepreneur à 80€/h perd 1 200€/mois en admin non-facturée
   - Offre claire : forfait 1 500€ Caelum Partners
   - CTA : démonstration gratuite de 20 minutes

2. MESSAGE LINKEDIN (300 caractères max, direct et percutant)
   Ciblant : gérant / chef d'entreprise construction, architecte indépendant

3. SCRIPT D'APPEL TÉLÉPHONIQUE (30 secondes)
   - Présentation, accroche, question ouverte, proposition de démo

4. CALCUL ROI DÉTAILLÉ
   - Hypothèses : entrepreneur 80€/h, 8h/semaine en admin
   - Temps économisé avec Caelum : 4h/semaine
   - Gain mensuel : 4h x 4 semaines x 80€ = 1 280€/mois
   - Payback forfait 1 500€ : 5-6 semaines
   - ROI annuel : 15 360€ économisés pour 1 500€ investis → ROI 924%

5. OFFRE DE DÉMONSTRATION
   - "Je vous génère votre prochain devis chantier en direct, en 3 minutes"
   - Documents montrables : devis, rapport avancement, lettre sous-traitant

6. OBJECTIONS & RÉPONSES
   - "J'ai déjà un secrétaire" → "Libérez-le pour des tâches à valeur ajoutée"
   - "C'est trop cher" → montrez le ROI 924%
   - "Je verrai plus tard" → "Chaque mois sans Caelum = 1 280€ perdus"

Ton : direct, chiffré, belge. Signé Chaima Mhadbi — Caelum Partners, Bruxelles."""

    resultat = streamer(prompt, "KIT PROSPECTION SECTEUR CONSTRUCTION")
    sauvegarder("kit_prospection_construction", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT SECTEUR CONSTRUCTION & ARCHITECTURE BELGIQUE")
    print("  Devis · Rapports chantier · Conformité · Prospection")
    print("  Caelum Partners — Chaima Mhadbi, Bruxelles")
    print("═"*65)

    while True:
        print("\n  [MENU]")
        print("  1. Générer un devis construction")
        print("  2. Rapport d'avancement chantier")
        print("  3. Lettre sous-traitant")
        print("  4. Checklist conformité chantier")
        print("  5. Kit prospection secteur construction")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            print("  Au revoir.")
            break
        elif choix == "1":
            generer_devis_construction()
        elif choix == "2":
            rapport_avancement_chantier()
        elif choix == "3":
            lettre_sous_traitant()
        elif choix == "4":
            checklist_conformite_chantier()
        elif choix == "5":
            kit_prospection_construction()
        else:
            print("  Choix invalide. Entrez 0 à 5.")
