"""
AGENT HORECA & RESTAURATION BELGIQUE — Menus trilingues, social media, événements, prospection
Usage : python agent_horeca_belge.py
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
Tu es un assistant IA spécialisé pour le secteur HORECA belge (Hôtels, Restaurants, Cafés), avec une expertise particulière sur Bruxelles et la Wallonie.
Le secteur HORECA belge représente plus de 50 000 établissements et 300 000 employés, en pleine reprise post-COVID.
Tu maîtrises les obligations légales belges spécifiques au secteur : AFSCA (Agence Fédérale pour la Sécurité de la Chaîne Alimentaire), obligation de caisse enregistreuse blanche (système GKS depuis 2014), TVA HORECA 12% sur la nourriture et 6% sur les boissons non alcoolisées.
Tu connais le statut flexi-job spécifique au secteur HORECA belge (loi du 16 novembre 2015 et modifications) permettant d'employer des travailleurs à taux réduit de cotisations.
Tu sais que le Horeca Fonds de Fermeture (secteur social) intervient en cas de fermeture involontaire d'établissement.
Tu produis des menus trilingues FR/NL/EN avec les 14 allergènes obligatoires selon le règlement EU n° 1169/2011 et la réglementation AFSCA belge.
À Bruxelles, de nombreux établissements sont tenus d'afficher leurs menus en français ET en néerlandais, avec l'anglais fortement recommandé pour les zones touristiques.
Tu génères des contenus social media percutants pour Instagram et Facebook adaptés à la culture belge : brasseries, restaurants gastronomiques, cafés-concerts.
Tu connais la culture culinaire belge : bières artisanales (500+ brasseries), chocolat, frites (patrimoine UNESCO), moules, spéculoos, genièvre, cuisine à la bière.
Un chef belge travaille en moyenne 60 à 80 heures par semaine : le temps administratif (menus, réseaux sociaux, correspondances) est son ennemi principal.
Un manager HORECA consacre en moyenne 20 heures par semaine aux tâches administratives évitables.
Tu aides à transformer ce temps en chiffre d'affaires additionnel : 10h/semaine économisées = 520h/an = temps pour développer 2 offres de privatisation supplémentaires.
Caelum Partners cible les 50 000 établissements belges avec un forfait entrée de gamme à 500€, très accessible et à ROI immédiat.
Ton ton est chaleureux, professionnel, orienté client, avec une touche de fierté pour la gastronomie belge.
Tu adaptes automatiquement le ton au type d'établissement : brasserie populaire, restaurant gastronomique, hôtel boutique, traiteur événementiel.
Tu maîtrises les formules de privatisation et banquets avec les structures tarifaires belges standard (boissons à la consommation, forfait boissons, menus en 3 ou 5 services).
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
                system_instruction=IDENTITE, temperature=0.25, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse

def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/horeca_belge", exist_ok=True)
    fichier = f"fichiers/horeca_belge/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")

def generer_menu_trilingue():
    print("\n  — Génération de menu trilingue FR + NL + EN —")
    print("  Entrez les plats (un par ligne, format : Nom | Ingrédients principaux | Info diét.).")
    print("  Ligne vide pour terminer.")
    plats = []
    while True:
        ligne = input(f"  Plat {len(plats)+1} : ").strip()
        if not ligne:
            break
        plats.append(sanitize(ligne))
    type_etablissement = sanitize(input("  Type d'établissement (brasserie / restaurant gastronomique / traiteur / café) : "))
    region = sanitize(input("  Région / Ville (Bruxelles / Liège / Gand / autre) : "))

    plats_texte = "\n".join([f"- {p}" for p in plats]) if plats else "À définir"

    prompt = f"""Génère des descriptions de menu trilingues professionnelles pour un établissement HORECA belge.

ÉTABLISSEMENT : {type_etablissement} — {region}
PLATS À DÉCRIRE :
{plats_texte}

Pour CHAQUE plat, génère :

VERSION FRANÇAISE :
- Nom du plat en français élégant
- Description appétissante (2-3 lignes), évocatrice, avec techniques de cuisson et terroir si pertinent
- Mention des allergènes obligatoires (parmi les 14 : gluten, crustacés, œufs, poisson, arachides, soja, lait, fruits à coque, céleri, moutarde, sésame, sulfites, lupin, mollusques)
- Label éventuel : Vegan 🌱 / Végétarien / Sans gluten / Bio

VERSION NÉERLANDAISE :
- Traduction professionnelle en néerlandais culinaire (pas automatique — adapté au style)
- Même structure avec allergènes en NL

VERSION ANGLAISE :
- Traduction en anglais culinaire international (pour touristes et expats)
- Même structure avec allergènes en EN

À la fin : note sur la présentation du menu (format suggéré, ordre des plats, conseils mise en page)

Ton : gastronomique, évocateur, professionnel. Qualité carte de restaurant étoilé."""

    resultat = streamer(prompt, "MENU TRILINGUE FR + NL + EN")
    sauvegarder("menu_trilingue", resultat)

def contenu_social_media_resto():
    print("\n  — Génération de contenu social media restaurant —")
    specials = sanitize(input("  Spéciaux de la semaine / plats du moment : "))
    evenements = sanitize(input("  Événements / thèmes de la semaine (soirée jazz, menu St-Valentin, etc.) : "))
    theme_saisonnier = sanitize(input("  Thème saisonnier (printemps, été, Noël, etc.) : "))
    type_resto = sanitize(input("  Type de restaurant et ambiance : "))

    prompt = f"""Génère 5 posts de réseaux sociaux professionnels pour un restaurant belge.

RESTAURANT : {type_resto}
SPÉCIAUX DE LA SEMAINE : {specials}
ÉVÉNEMENTS : {evenements}
THÈME SAISONNIER : {theme_saisonnier}

Génère 5 posts variés :

POST 1 — PLAT DU MOMENT (Instagram focus)
- Caption FR (150 mots max) : description sensorielle, emojis pertinents, hashtags FR
- Caption NL (150 mots max) : adaptation culturelle, hashtags NL
- Suggestion visuelle : angle photo, mise en scène recommandée

POST 2 — ÉVÉNEMENT / SOIRÉE
- Caption FR + NL (120 mots max chacun)
- Call-to-action : réservation, lien bio, numéro de téléphone fictif
- Hashtags événement

POST 3 — STORY FORMAT (vertical, texte court)
- 3 slides FR + 3 slides NL
- Poll ou question d'engagement suggéré

POST 4 — HERITAGE / AUTHENTIQUE (valoriser le terroir belge)
- Storytelling sur un produit belge (bière, chocolat, produit local)
- Caption FR + NL, ton narratif et fier

POST 5 — OFFRE COMMERCIALE / PRIVATISATION
- Accroche sur les événements privés ou formules semaine
- Caption FR + NL avec CTA réservation

Pour chaque post : hashtags ciblés (10-15), meilleur moment de publication, format recommandé (Reel / Carrousel / Photo unique)."""

    resultat = streamer(prompt, "CONTENU SOCIAL MEDIA RESTAURANT")
    sauvegarder("social_media_resto", resultat)

def reponse_avis_client(avis: str = ""):
    print("\n  — Réponse professionnelle à un avis client —")
    if not avis:
        avis = sanitize(input("  Collez l'avis client (Google, TripAdvisor, etc.) : "))
    plateforme = sanitize(input("  Plateforme (Google / TripAdvisor / Facebook / autre) : "))
    nom_etablissement = sanitize(input("  Nom de votre établissement : "))
    type_etablissement = sanitize(input("  Type d'établissement : "))

    prompt = f"""Génère une réponse professionnelle et stratégique à cet avis client pour un établissement HORECA belge.

ÉTABLISSEMENT : {nom_etablissement} ({type_etablissement})
PLATEFORME : {plateforme}
AVIS CLIENT :
{avis}

Génère :

ANALYSE DE L'AVIS :
- Ton de l'avis : positif / négatif / mitigé
- Points soulevés : ce qui peut être actionnable vs émotionnel
- Risque réputationnel : faible / moyen / élevé
- Stratégie recommandée

RÉPONSE EN FRANÇAIS (prête à publier) :
- Salutation personnalisée (sans copier le prénom si non fourni)
- Remerciement sincère (même pour un avis négatif)
- Réponse aux points spécifiques soulevés (sans être défensif)
- Transformation du négatif en positif (si applicable)
- Invitation à revenir ou à contacter en privé
- Signature professionnelle (prénom + fonction)
- Longueur : 100-150 mots max (optimal SEO et lisibilité)

RÉPONSE EN NÉERLANDAIS :
- Même structure, ton adapté (culture flamande/néerlandophone)
- Même longueur cible

CONSEIL SUIVI :
- Action interne recommandée suite à cet avis
- Si avis faux / abusif : procédure de signalement sur {plateforme}

Ton : chaleureux, professionnel, brand-consistent. Jamais défensif, toujours constructif."""

    resultat = streamer(prompt, "RÉPONSE AVIS CLIENT PROFESSIONNEL")
    sauvegarder("reponse_avis_client", resultat)

def proposition_evenement_privatisation():
    print("\n  — Proposition d'événement / privatisation —")
    type_evenement = sanitize(input("  Type d'événement (mariage / anniversaire / team building / séminaire / cocktail) : "))
    capacite = sanitize(input("  Capacité de la salle / espace (nombre de personnes) : "))
    services = sanitize(input("  Services disponibles (cuisine, bar, sono, décoration, hébergement) : "))
    budget_indicatif = sanitize(input("  Budget indicatif par personne ou total (ou 'à préciser') : "))

    prompt = f"""Génère une proposition commerciale complète pour un événement privatisation dans un établissement HORECA belge.

ÉVÉNEMENT : {type_evenement}
CAPACITÉ : {capacite} personnes
SERVICES : {services}
BUDGET : {budget_indicatif}

La proposition doit inclure :

1. PAGE DE GARDE PROFESSIONNELLE
   - Titre de l'événement, date de la proposition, référence
   - Coordonnées établissement et contact événementiel

2. PRÉSENTATION DE L'ÉTABLISSEMENT (3-4 lignes accrocheur)
   - Points forts pour ce type d'événement

3. FORMULES PROPOSÉES (3 niveaux)
   FORMULE ESSENTIELLE :
   - Menu (3 services), boissons à la consommation
   - Prix par personne indicatif

   FORMULE PRESTIGE :
   - Menu (5 services), forfait boissons 3h, animation de base
   - Prix par personne

   FORMULE SUR MESURE :
   - Description des options de personnalisation
   - Tarification à la demande

4. CONDITIONS DE RÉSERVATION
   - Acompte 30% à la signature, solde 15 jours avant
   - Délai de confirmation du nombre définitif (J-7)
   - Politique d'annulation (>30j : remboursement intégral / 15-30j : 50% / <15j : 100%)
   - TVA 6% boissons non alcoolisées / 12% nourriture / 21% alcool

5. OPTIONS ADDITIONNELLES
   - Animations, DJ, fleurs, photographe partenaire
   - Hébergement si disponible

6. PROCHAINES ÉTAPES & SIGNATURE
   - Call-to-action : visite de l'établissement proposée
   - Signature commerciale

Format : document professionnel prêt à envoyer en PDF. Ton chaleureux et commercial."""

    resultat = streamer(prompt, "PROPOSITION ÉVÉNEMENT / PRIVATISATION")
    sauvegarder("proposition_evenement", resultat)

def kit_prospection_horeca():
    prompt = """Génère un kit de prospection commercial complet pour Caelum Partners ciblant les gérants d'établissements HORECA belges.

Le kit doit contenir :

1. EMAIL DE PROSPECTION (objet + corps, 200 mots max)
   - Accroche réaliste : "Vous passez 20h/semaine sur l'admin au lieu de servir vos clients"
   - Douleur spécifique : menu trilingue = 3h de travail / Caelum = 5 minutes
   - Offre : forfait 500€ Caelum Partners — le plus accessible
   - CTA : "Je vous génère votre menu trilingue maintenant, gratuitement"

2. SCRIPT VISITE EN PERSONNE (30 secondes au comptoir)
   - Approche naturelle pour entrer dans le restaurant en heure creuse
   - Phrase d'accroche directe au gérant/chef
   - Proposition de démo sur spot (téléphone/tablette)
   - Gestion du "pas le temps" → "Justement, c'est pour ça que je suis là"

3. MESSAGE INSTAGRAM DM (150 caractères max)
   - Ciblant les restaurants actifs sur Instagram
   - Accroche sur leur contenu actuel → proposition d'amélioration

4. CALCUL ROI HORECA
   - Temps actuel : 2h/semaine menus + 3h social media + 2h réponses avis = 7h/semaine
   - Économie avec Caelum : 5h/semaine
   - Valorisation : chef à 25€/h équivalent = 125€/semaine = 500€/mois
   - Forfait Caelum : 500€/an = payback en 1 mois
   - ROI annuel : 6 000€ économisés pour 500€ investis

5. DÉMONSTRATION EN 3 MINUTES
   - Séquence : "Donnez-moi 3 plats de votre menu actuel"
   - Génération du menu trilingue EN DIRECT
   - Résultat affiché : 3 langues, 14 allergènes, prêt à imprimer
   - Impact : "Sans moi, c'est 2h de votre dimanche soir"

6. OBJECTIONS & RÉPONSES
   - "J'ai pas le budget" → ROI 1 mois payback
   - "Ma femme s'en occupe" → "Libérez-la pour le service"
   - "On fait déjà ça" → démo qualité comparative

Ton : direct, sympathique, belge. Signé Chaima Mhadbi — Caelum Partners, Bruxelles."""

    resultat = streamer(prompt, "KIT PROSPECTION HORECA BELGE")
    sauvegarder("kit_prospection_horeca", resultat)

if __name__ == "__main__":
    print("\n" + "═"*65)
    print("  AGENT HORECA & RESTAURATION BELGIQUE")
    print("  Menus · Social Media · Événements · Prospection")
    print("  Caelum Partners — Chaima Mhadbi, Bruxelles")
    print("═"*65)

    while True:
        print("\n  [MENU]")
        print("  1. Générer un menu trilingue FR + NL + EN")
        print("  2. Contenu social media restaurant")
        print("  3. Réponse à un avis client")
        print("  4. Proposition événement / privatisation")
        print("  5. Kit prospection HORECA")
        print("  0. Quitter\n")
        choix = input("  Choix → ").strip()
        if choix == "0":
            print("  Au revoir.")
            break
        elif choix == "1":
            generer_menu_trilingue()
        elif choix == "2":
            contenu_social_media_resto()
        elif choix == "3":
            reponse_avis_client()
        elif choix == "4":
            proposition_evenement_privatisation()
        elif choix == "5":
            kit_prospection_horeca()
        else:
            print("  Choix invalide. Entrez 0 à 5.")
