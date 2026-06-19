"""
AGENT D'INFLUENCE SYSTÉMIQUE — Positionner Chaima comme LA référence IA pour les PME belges
Autorité · Contenu pilier · Partenariats stratégiques · Presse · Ambassadeurs

Usage : python agent_influence_systemique.py
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

IDENTITE = """# AGENT D'INFLUENCE SYSTÉMIQUE — CAELUM PARTNERS

## IDENTITÉ ET RÔLE
Tu es l'Agent d'Influence Systémique de Caelum Partners.
Ta mission : positionner Chaima Mhadbi et Caelum Partners comme LA référence absolue
sur l'intelligence artificielle pour les PME en Belgique.
L'autorité est le moat ultime — impossible à copier, impossible à acheter.

## THÉORIE DE L'AUTORITÉ EN POSITIONNEMENT

### POURQUOI L'AUTORITÉ EST LE MOAT ULTIME
- L'autorité se construit sur des années → aucun concurrent ne peut l'acheter
- L'autorité génère des leads entrants gratuits (inbound) → coût d'acquisition = 0€
- L'autorité justifie un prix premium sans négociation
- L'autorité protège contre la concurrence par les prix → "je veux CHAIMA, pas un équivalent"

### LES 4 PILIERS DE L'AUTORITÉ (framework de positionnement)
1. CONTENU : produire du contenu de référence sur son domaine (YouTube, LinkedIn, podcast)
2. PREUVES SOCIALES : cas clients, témoignages, résultats chiffrés, prix reçus
3. RÉSEAU : associations stratégiques avec des marques de référence (ULB, Hub.Brussels)
4. MÉDIAS : apparitions dans la presse et les médias de référence belges

## ÉCOSYSTÈME MÉDIAS BELGES — CARTOGRAPHIE

### PRESSE ÉCRITE FRANCOPHONE
- L'ECHO : quotidien économique de référence, lectorat dirigeants et investisseurs
  → Contacts : rédaction@lecho.be, rubrique "Entreprises" et "Technologie"
- LA LIBRE BELGIQUE : quotidien généraliste premium, lectorat cadres et politiques
  → Rubrique "Économie" et "Tech"
- LE VIF / L'EXPRESS BELGIQUE : hebdomadaire, format magazine, sujets de fond
- TRENDS-TENDANCES : magazine économique belge, focus entrepreneuriat et innovation

### MÉDIAS AUDIOVISUELS FRANCOPHONES
- RTBF : radio et TV publique belge francophone
  → Émissions : "La Première" (radio), "Questions à la Une" (TV)
- BEL RTL : radio commerciale, émissions économiques du matin
- CANAL Z : chaîne TV économique belge, émissions dédiées aux entrepreneurs

### MÉDIAS NUMÉRIQUES ET NEWSLETTERS
- STARTUPS.BE : actualité startup belge, très lu par l'écosystème
- DATANEWS.BE : IT et technologie belge, lectorat DSI et managers IT
- RÉFÉRENCES.BE / MOUSTIQUE : magazines lifestyle belges (angle "portrait entrepreneur")

### PRESSE NÉERLANDOPHONE (pour le marché flamand)
- DE TIJD : équivalent de L'Echo, lectorat économique flamand
- KNACK FOCUS : magazine équivalent du VIF côté flamand

## PARTENARIATS STRATÉGIQUES HAUTE VALEUR EN BELGIQUE

### INSTITUTIONS PUBLIQUES ET PARA-PUBLIQUES
- HUB.BRUSSELS : agence de développement économique de Bruxelles
  → Services : mise en relation avec PME bruxelloises, espace de travail, réseau
  → Contact : info@hub.brussels — partenariat = accès à 10 000 PME bruxelloises
- AGENCE DU NUMÉRIQUE (Wallonie) : digitalisation des entreprises wallonnes
- DIGITAL WALLONIA : programme de transformation numérique wallon
- BRUXELLES ÉCONOMIE ET EMPLOI : subventions pour les entreprises bruxelloises innovantes

### UNIVERSITÉS ET GRANDES ÉCOLES
- ULB (Université Libre de Bruxelles) : partenariat recherche IA, accès aux étudiants
  → École Polytechnique de Bruxelles, École de Gestion Solvay
- VUB (Vrije Universiteit Brussel) : partenaire natural pour le marché néerlandophone
- ICHEC Brussels Management School : école de management, formation des futurs dirigeants PME
- SOLVAY ALUMNI : réseau de 30 000 anciens, décideurs économiques belges

### RÉSEAUX ENTREPRENEURIAUX
- BECI (Bruxelles Entreprises et Commerce) : chambre de commerce de Bruxelles
  → 2 500 entreprises membres, événements mensuels, accès à des dirigeants de PME
- CCI (Chambres de Commerce et d'Industrie) en Wallonie : Liège, Namur, Charleroi
- BNI (Business Network International) : réseau de référencement mutuel
- VOKA : chambre de commerce flamande, équivalent de la BECI pour la Flandre

### PARTENAIRES FINANCIERS
- BELFIUS ENTREPRISES : banque principale des ASBL et PME belges
  → Partenariat : co-organisation d'événements, co-branding, accès aux clients Belfius PME
- BNP PARIBAS FORTIS : première banque belge, programme d'accompagnement PME
  → "BNP Paribas Fortis for Entrepreneurs" : 200 000 clients PME potentiels
- BPIFRANCE équivalent belge : SOWALFIN, SFPIM → garanties de prêt aux PME

## STRATÉGIE DE THOUGHT LEADERSHIP
1. NICHE CLAIRE : "IA pratique pour les PME belges" (pas "IA en général")
2. POINT DE VUE UNIQUE : "L'IA n'est pas pour les grandes entreprises — c'est l'outil des PME"
3. FRÉQUENCE : 3 posts LinkedIn/semaine + 1 article long-form/mois + 1 événement/trimestre
4. FORMAT SIGNATURE : toujours commencer par un résultat chiffré (ex: "47% de temps économisé")

## FORMAT DE SORTIE OBLIGATOIRE
1. PLAN D'AUTORITÉ : 12 mois de construction d'autorité étape par étape
2. CONTENU PILIER : 3 pièces de contenu qui génèrent de l'autorité pour 5 ans
3. PARTENARIATS : 10 partenariats à signer dans l'ordre de priorité
4. STRATÉGIE PRESSE : 5 angles pour obtenir une première publication dans L'Echo ou La Libre
5. AMBASSADEURS : programme de référencement client systématique"""


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
    os.makedirs("fichiers/influence", exist_ok=True)
    fichier = f"fichiers/influence/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def strategie_autorite_complete():
    r = streamer(
        """Conçois le plan 12 mois pour positionner Chaima Mhadbi comme LA référence IA pour les PME belges.

PLAN D'AUTORITÉ SYSTÉMIQUE — 12 MOIS :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MOIS 1-2 — FONDATIONS DE L'AUTORITÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Objectif : établir une présence professionnelle inattaquable en ligne

1. Profil LinkedIn optimisé pour l'autorité :
   - Titre : "Fondatrice Caelum Partners | IA pour PME belges | [résultat client clé]"
   - À propos : storytelling + expertise + preuve sociale
   - Featured : 3 contenus qui démontrent l'expertise

2. Contenu LinkedIn (3 posts/semaine) :
   - Post type 1 : "Ce que j'ai appris en aidant [nom secteur] à automatiser [tâche]"
   - Post type 2 : "3 outils IA que toute PME belge devrait utiliser en 2025"
   - Post type 3 : "Étude de cas : [client X] a économisé [montant] avec l'IA"

3. Premier événement networking :
   - Assister à 2 événements BECI ou Hub.Brussels ce mois
   - Objectif : 10 nouvelles connexions qualifiées (dirigeants PME)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MOIS 3-4 — PREMIÈRES PREUVES SOCIALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Objectif : transformer les premiers clients en ambassadeurs publics

1. Cas d'usage documenté #1 :
   - Article LinkedIn "Étude de cas : comment [PME belge] a [résultat] grâce à l'IA"
   - Format : problème → solution → résultat chiffré → témoignage client

2. Premier "Live LinkedIn" ou "Newsletter" :
   - Thème : "L'IA en pratique pour les PME belges — ce qui marche vraiment"
   - Objectif : 100 abonnés newsletter

3. Candidature première reconnaissance :
   - "Startups of the Year" Belgique (Trends-Tendances)
   - "Prix de l'Innovation" BECI
   - "Femme Entrepreneur Digitale" IWEPS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MOIS 5-8 — AMPLIFICATION PAR LES PARTENARIATS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Objectif : être associé à des marques de référence

1. Partenariat Hub.Brussels : signer un accord de partenariat
2. Intervention dans une université (ULB ou ICHEC) : conférence "IA pour PME"
3. Première mention presse : communiqué de presse avec angle exclusif pour L'Echo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MOIS 9-12 — CONSOLIDATION DE L'AUTORITÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Objectif : être cité spontanément comme référence par des tiers

1. Premier article dans un média belge de référence
2. Première conférence publique en tant qu'intervenant
3. Lancement d'une newsletter hebdomadaire > 500 abonnés qualifiés
4. Premier partenariat banque (Belfius ou BNP Fortis) pour co-animer des ateliers PME

MÉTRIQUES D'AUTORITÉ À SUIVRE :
- Connexions LinkedIn qualifiées (dirigeants PME) : cible 500 en 12 mois
- Portée moyenne des posts : cible > 1 000 vues/post
- Mentions par des tiers (sans demander) : cible 5 par mois en mois 12
- Demandes entrantes de clients (sans prospection) : cible 2/mois en mois 12""",
        "STRATÉGIE AUTORITÉ 12 MOIS — Chaima Mhadbi, référence IA belge"
    )
    sauvegarder("strategie_autorite_complete", r)


def concevoir_contenu_pilier():
    r = streamer(
        """Conçois 3 pièces de contenu pilier qui établiront l'autorité de Chaima pour les 5 prochaines années.

DÉFINITION D'UN CONTENU PILIER :
Un contenu pilier est un contenu long, exhaustif, ultra-qualitatif qui :
- Répond à LA question fondamentale que se pose la cible
- Génère du trafic et des liens entrants pendant des années
- Ne se démode pas rapidement (evergreen)
- Peut être décliné en 50+ contenus plus courts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PILIER 1 — LE GUIDE ULTIME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TITRE : "L'IA pour les PME belges en 2025 : le guide complet"
FORMAT : article de 5 000 mots + version PDF téléchargeable
AUDIENCE : dirigeants de PME belges (10-100 employés), non-techniciens
STRUCTURE :
  - Chapitre 1 : Pourquoi l'IA n'est plus réservée aux grandes entreprises
  - Chapitre 2 : Les 10 tâches qu'une PME belge peut automatiser aujourd'hui
  - Chapitre 3 : Combien ça coûte vraiment ? (budget réaliste)
  - Chapitre 4 : Comment choisir son prestataire IA (grille d'évaluation)
  - Chapitre 5 : RGPD et IA : ce que toute PME doit savoir
  - Chapitre 6 : Étude de cas : 3 PME belges qui ont transformé leur activité avec l'IA
OBJECTIF : devenir LE résultat #1 sur Google pour "IA PME Belgique"
DÉLAI DE CRÉATION : 2 semaines avec les agents Caelum

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PILIER 2 — L'OUTIL GRATUIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TITRE : "Calculateur ROI IA pour PME belges" (outil en ligne gratuit)
FORMAT : calculateur interactif en ligne (ou Google Sheet partagé)
AUDIENCE : dirigeants qui veulent calculer le ROI avant d'investir
FONCTIONNEMENT :
  - Entrées : secteur, nb employés, tâches à automatiser, temps passé/semaine
  - Sorties : temps économisé/mois, économie en € à l'année, délai d'amortissement
  - CTA : "Obtenez votre diagnostic gratuit avec Caelum Partners"
OBJECTIF : générer 50 leads qualifiés/mois de façon automatique
DÉLAI DE CRÉATION : 3 jours avec agents Caelum

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PILIER 3 — LA SÉRIE VIDÉO / PODCAST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TITRE : "L'IA en pratique" — série de 12 épisodes
FORMAT : vidéo LinkedIn (5-10 min) ou podcast audio
STRUCTURE : 1 secteur belge par épisode (comptabilité, RH, retail, logistique...)
  Episode 1 : "Comment un cabinet comptable bruxellois a automatisé 60% de ses rapports"
  Episode 2 : "IA et recrutement : comment une PME de 20 personnes trie 200 CV en 10 minutes"
  [etc.]
OBJECTIF : 1 000 vues/épisode en mois 6, 5 000 vues/épisode en mois 12
DÉLAI DE CRÉATION : 1 épisode par semaine

PLAN DE DÉCLINAISON DES CONTENUS PILIERS :
1 pilier → 10 posts LinkedIn → 5 emailings → 2 présentations → 1 atelier""",
        "CONTENU PILIER — 3 pièces d'autorité durables pour Caelum Partners"
    )
    sauvegarder("contenu_pilier", r)


def cartographier_partenariats():
    r = streamer(
        """Cartographie les 10 partenariats à fort levier pour Caelum Partners en Belgique.

PARTENARIATS PRIORITAIRES — CLASSÉS PAR IMPACT/EFFORT :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIER 1 — IMPACT MAXIMAL, EFFORT MODÉRÉ (signer dans les 90 jours)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. HUB.BRUSSELS (Agence développement économique bruxellois)
   Impact : accès à 10 000 PME bruxelloises, légitimité officielle
   Comment contacter : formulaire partenaire sur hub.brussels
   Proposition de valeur pour Hub.Brussels : Caelum apporte l'expertise IA aux PME de leur réseau
   Format de partenariat : ateliers co-animés mensuels, référencement dans leur annuaire

2. BECI (Bruxelles Entreprises et Commerce)
   Impact : 2 500 membres entreprises, événements réguliers, newsletter aux dirigeants
   Comment contacter : partenariat@beci.be
   Proposition : Caelum anime 1 atelier "IA pour PME" par trimestre → accès à leurs membres
   Format : conférence + article dans leur magazine + profil dans l'annuaire

3. RÉSEAU DES COMPTABLES ET FIDUCIAIRES BELGES
   Impact : les comptables conseillent leurs clients PME → prescripteurs naturels de Caelum
   Comment contacter : IEC (Institut des Experts-comptables et Conseils fiscaux)
   Proposition : "Recommandez Caelum à vos clients PME qui veulent automatiser → commission 10%"
   Format : partenariat de référencement avec commission sur chaque client apporté

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIER 2 — IMPACT ÉLEVÉ, EFFORT PLUS IMPORTANT (mois 3-6)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. ULB — ÉCOLE DE GESTION SOLVAY
   Impact : accès aux étudiants MBA (futurs dirigeants), légitimité académique
   Format : intervention comme "practitioner" dans un cours d'IA managériale

5. BELFIUS ENTREPRISES
   Impact : 300 000 clients PME en Belgique → co-marketing avec la première banque des ASBL
   Format : co-organisation de webinaires "Financer et réussir sa transformation IA"

6. RÉSEAU DES AVOCATS D'AFFAIRES BELGES (OBFG / OVB)
   Impact : prescripteurs vers leurs clients PME (contrats, création d'entreprise)
   Format : partenariat de référencement avec commission

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIER 3 — IMPACT LONG TERME (mois 6-12)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7. AGORIA (fédération belge technologie)
8. DIGITAL WALLONIA (programme numérique wallon)
9. ENTERPRISE EUROPE NETWORK (réseau EU de PME innovantes)
10. BNP PARIBAS FORTIS FOR ENTREPRENEURS

TEMPLATE D'EMAIL DE PREMIER CONTACT POUR CHAQUE TIER :
[Rédiger un modèle d'email de prospection partenariat pour les 3 partenaires Tier 1]""",
        "CARTOGRAPHIE PARTENARIATS — 10 alliances stratégiques Caelum Partners"
    )
    sauvegarder("cartographie_partenariats", r)


def strategie_presse_medias():
    r = streamer(
        """Conçois la stratégie presse pour obtenir une première publication dans L'Echo ou La Libre en 6 mois.

STRATÉGIE PRESSE — CAELUM PARTNERS

ANALYSE DU PAYSAGE MÉDIATIQUE BELGE :
Les journalistes économiques belges cherchent des angles :
1. La réussite d'une entreprise bruxelloise innovante (angle "fierté locale")
2. L'impact de l'IA sur les PME belges (angle "tendance économique")
3. Le profil d'une fondatrice atypique (angle "diversité + tech")
4. L'IA Act européen et ce que ça change pour les entreprises belges (angle "réglementation")
5. Une étude de cas concrète avec des chiffres (angle "business case réel")

LES 5 ANGLES POUR OBTENIR UNE PUBLICATION :

ANGLE 1 — PORTRAIT ENTREPRENEUR (La Libre, Trends-Tendances) :
Titre potentiel : "Chaima Mhadbi, la Bruxelloise qui démocratise l'IA pour les PME"
Accroche : femme, jeune, bilingue, fondatrice d'une ASBL ET d'une société IA
Comment le proposer : dossier de presse + demande d'interview (portrait)

ANGLE 2 — TENDANCE ÉCONOMIQUE (L'Echo, De Tijd) :
Titre potentiel : "Les PME belges rattrapent leur retard sur l'IA : le marché explose"
Accroche : données de croissance du marché IA en Belgique + positionnement Caelum
Comment le proposer : étude / baromètre original + Chaima comme experte citée

ANGLE 3 — RÉGLEMENTATION (L'Echo, La Libre) :
Titre potentiel : "L'IA Act européen : ce que les PME belges doivent faire avant 2026"
Accroche : expertise conformité IA + conseils concrets pour PME
Comment le proposer : tribune libre signée par Chaima

ANGLE 4 — ÉTUDE DE CAS (DataNews, Trends) :
Titre potentiel : "Comment cette PME bruxelloise a divisé ses coûts par 3 grâce à l'IA"
Accroche : résultat concret + chiffres réels du client
Comment le proposer : communiqué de presse avec étude de cas détaillée

ANGLE 5 — ÉVÉNEMENT DÉCLENCHEUR (tous médias) :
Titre potentiel : "Caelum Partners remporte le Prix de l'Innovation BECI 2025"
Accroche : la reconnaissance externe génère automatiquement la couverture médiatique
Comment le déclencher : candidater à tous les prix entrepreneuriaux belges

KIT PRESSE DE CAELUM PARTNERS À PRÉPARER :
1. Communiqué de presse type (template + 3 versions d'angle)
2. Photo professionnelle haute résolution de Chaima (fond blanc, sourire, tenue pro)
3. Biographie courte (100 mots) et longue (300 mots)
4. Chiffres clés de Caelum (date création, services, nb clients, résultats)
5. Citations prêtes à l'emploi pour les journalistes (5 citations sur différents angles)
6. Contacts journalistes ciblés avec nom/email (liste de 20 journalistes prioritaires)""",
        "STRATÉGIE PRESSE — Caelum Partners dans les médias belges"
    )
    sauvegarder("strategie_presse", r)


def programme_ambassadeurs():
    r = streamer(
        """Conçois le programme d'ambassadeurs clients pour générer des référencements systématiques.

PROGRAMME AMBASSADEURS CAELUM PARTNERS

POURQUOI LES AMBASSADEURS SONT LA SOURCE LA PLUS PUISSANTE :
- Coût d'acquisition : 0€ (le client existant fait le travail)
- Taux de conversion : 5-10x supérieur à la prospection froide
- Qualité des leads : le client recommande des profils similaires à lui (fit parfait)
- Autorité transférée : "mon comptable m'a recommandé Caelum" = confiance immédiate

STRUCTURE DU PROGRAMME :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NIVEAU 1 — AMBASSADOR BASIQUE (tout client satisfait)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Conditions : client livré, satisfaction confirmée (questionnaire post-livraison)
Ce qu'on demande :
  1. Un témoignage écrit (3-5 phrases) pour le site web et LinkedIn
  2. Une note Google (5 étoiles) si applicable
  3. La permission de les citer comme référence

Récompense : RIEN (la qualité du service est suffisante) — NE PAS monétiser systématiquement
→ Exception : si le client propose de recommander spontanément, voir Niveau 2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NIVEAU 2 — PARTENAIRE RÉFÉRENT (clients actifs et enthousiastes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Conditions : client récurrent ou client qui a eu un ROI exceptionnel
Ce qu'on demande :
  1. Introduction directe à 2-3 contacts dans leur réseau
  2. Co-participation à un témoignage vidéo (2 minutes)
  3. Mention sur leur propre LinkedIn ("Je travaille avec @Caelum Partners")

Récompense :
  Option A : remise 10% sur la prochaine facture
  Option B : 1 heure de consultation stratégique IA offerte
  Option C : mention dans la newsletter Caelum (visibilité pour leur propre entreprise)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NIVEAU 3 — AMBASSADEUR OFFICIEL (partenaires prescripteurs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Conditions : prescripteurs naturels (comptables, avocats, consultants) qui recommandent Caelum
Ce qu'on propose :
  1. Commission 10% sur chaque client apporté qui signe
  2. Formation gratuite sur les services Caelum pour mieux les recommander
  3. Co-branding : "partenaire certifié Caelum" sur leur site web

PROCESSUS D'ACTIVATION DU PROGRAMME :

1. À J+30 après livraison : envoyer questionnaire satisfaction
2. Si satisfaction > 8/10 : demander le témoignage écrit
3. À J+60 : invitation à rejoindre le Niveau 2 si client enthousiaste
4. À J+90 : proposer une introduction à 2 contacts de leur réseau

SCRIPT D'INTRODUCTION DE RÉFÉRENCEMENT :
"Bonjour [nom], suite à notre collaboration sur [projet], je suis ravi(e) du résultat obtenu.
J'aimerais savoir si vous connaissez d'autres dirigeants de PME qui pourraient bénéficier
du même type d'accompagnement IA. Si oui, seriez-vous à l'aise pour faire une introduction ?"

TABLEAU DE BORD AMBASSADEURS (métriques à suivre) :
- Nb ambassadeurs actifs niveau 1/2/3
- Nb leads apportés par les ambassadeurs (par mois)
- Taux de conversion des leads ambassadeurs
- CA généré via ambassadeurs (%)""",
        "PROGRAMME AMBASSADEURS — Référencement systématique Caelum Partners"
    )
    sauvegarder("programme_ambassadeurs", r)


if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  INFLUENCE SYSTÉMIQUE — Caelum Partners")
    print("  Autorité · Contenu · Partenariats · Presse · Ambassadeurs")
    print("═"*65)

    while True:
        print("\n  1. Stratégie d'autorité 12 mois (plan complet)")
        print("  2. Concevoir les contenus piliers")
        print("  3. Cartographier les partenariats stratégiques")
        print("  4. Stratégie presse et médias belges")
        print("  5. Programme ambassadeurs clients")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()
        if choix == "0":
            break
        elif choix == "1":
            strategie_autorite_complete()
        elif choix == "2":
            concevoir_contenu_pilier()
        elif choix == "3":
            cartographier_partenariats()
        elif choix == "4":
            strategie_presse_medias()
        elif choix == "5":
            programme_ambassadeurs()
        else:
            print("  Choix invalide.")
