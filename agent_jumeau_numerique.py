"""
╔══════════════════════════════════════════════════════════════════╗
║          JUMEAU NUMÉRIQUE — Digital Twin de l'Entreprise         ║
║   Simulez l'impact de vos décisions AVANT de les prendre.        ║
║   Univers parallèle. Risque zéro. Intelligence maximale.         ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import datetime
from pathlib import Path

from google import genai
from google.genai import types

from memoire import charger_memoire, incrementer_stat

# ── Configuration ─────────────────────────────────────────────────────────────
MODEL = "gemini-2.0-flash"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

ENTREPRISE = "AgentClaude Solutions"
DOMAINE = "solutions d'agents IA autonomes"

DOSSIER_SORTIE = Path("fichiers/simulation")
DOSSIER_SORTIE.mkdir(parents=True, exist_ok=True)


# ── Utilitaires ───────────────────────────────────────────────────────────────

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


def streamer(prompt: str) -> str:
    """Appel Gemini en streaming — retourne le texte complet."""
    model = _creer_model(MODEL)
    print()
    texte_complet = ""
    try:
        reponse = model.generate_content(
            prompt,
            stream=True,
            generation_config=types.GenerateContentConfig(temperature=0.8),
        )
        for chunk in reponse:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                texte_complet += chunk.text
    except Exception as e:
        print(f"\n  Erreur API Gemini : {e}")
    print()
    return texte_complet


def sauvegarder(nom_fichier: str, contenu: str) -> Path:
    """Sauvegarde la simulation dans fichiers/simulation/ avec horodatage."""
    horodatage = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = DOSSIER_SORTIE / f"{nom_fichier}_{horodatage}.txt"
    chemin.write_text(contenu, encoding="utf-8")
    return chemin


def extraire_contexte_memoire() -> str:
    """Extrait les données clés de la mémoire pour enrichir les simulations."""
    m = charger_memoire()
    clients = m.get("clients", {})
    stats = m.get("stats", {})

    nb_clients = len(clients)
    nb_actifs = sum(1 for c in clients.values() if c.get("statut") == "actif")
    secteurs = list({c.get("secteur", "N/A") for c in clients.values()})[:5]
    total_demandes = stats.get("total_demandes", 0)

    segments = {"champions": 0, "grands_comptes": 0, "pme": 0}
    for c in clients.values():
        secteur = c.get("secteur", "").lower()
        interactions = len(c.get("interactions", []))
        if interactions >= 10:
            segments["champions"] += 1
        elif "grand" in secteur or "enterprise" in secteur or interactions >= 5:
            segments["grands_comptes"] += 1
        else:
            segments["pme"] += 1

    return f"""
Données mémoire entreprise :
- Clients totaux : {nb_clients} ({nb_actifs} actifs)
- Segments : Champions={segments['champions']}, Grands Comptes={segments['grands_comptes']}, PME={segments['pme']}
- Secteurs représentés : {', '.join(secteurs) if secteurs else 'Non renseigné'}
- Total interactions trackées : {total_demandes}
"""


def bandeau(titre: str, sous_titre: str = ""):
    largeur = 68
    print("\n" + "▓" * largeur)
    print(f"  ◈  {titre}")
    if sous_titre:
        print(f"     {sous_titre}")
    print("▓" * largeur)


# ── Agent 1 — Simulateur de Décision ─────────────────────────────────────────

def agent_simuler_decision(decision: str, contexte: str) -> str:
    """
    Simule l'impact d'une décision business sur 6 dimensions et 3 timelines.
    Recommande GO / NO-GO / ADJUST avec probabilités.
    """
    incrementer_stat("agent_jumeau_decision")
    contexte_memoire = extraire_contexte_memoire()

    prompt = f"""Tu es le Jumeau Numérique de {ENTREPRISE}, une IA de simulation d'entreprise de niveau qualitatif exceptionnel.
Tu simules avec précision les conséquences d'une décision business AVANT qu'elle ne soit prise dans le monde réel.

Entreprise : {ENTREPRISE} ({DOMAINE})
{contexte_memoire}

DÉCISION À SIMULER : {decision}
CONTEXTE FOURNI : {contexte}

Génère une simulation complète et futuriste de l'impact de cette décision.

══════════════════════════════════════════════════════════════════
◈  SIMULATION MULTIDIMENSIONNELLE — {decision[:60]}
══════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIMENSION 1 — IMPACT FINANCIER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Impact sur les revenus :
- Variation du chiffre d'affaires estimée (€ et %)
- Nouveaux flux de revenus potentiels créés
- Flux de revenus mis en danger

Impact sur les coûts :
- Investissement initial requis (CAPEX)
- Variation des coûts opérationnels mensuels (OPEX)
- Coûts cachés et risques financiers non-évidents

Métriques financières clés :
- ROI estimé (horizon 12 mois)
- Point mort / break-even
- Impact sur la trésorerie (burn rate)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIMENSION 2 — IMPACT CLIENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Risque de churn (par segment) :
- Champions : risque de départ (%) + raisons
- Grands Comptes : risque de départ (%) + raisons
- PME : risque de départ (%) + raisons

Potentiel d'acquisition :
- Nouveaux profils clients attirés par cette décision
- Marchés / segments nouvellement accessibles
- Estimation du nombre de nouveaux clients potentiels (6 mois)

NPS et satisfaction :
- Impact estimé sur le NPS (variation de points)
- Segments qui applaudiront vs. segments qui résisteront

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIMENSION 3 — IMPACT ÉQUIPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Moral et engagement :
- Réactions probables de l'équipe (enthousiasme / résistance)
- Risques de départs clés liés à cette décision
- Comment annoncer et embarquer l'équipe

Charge de travail :
- Surcharge temporaire anticipée (qui, combien de temps ?)
- Processus fortement impactés
- Ressources humaines à mobiliser ou recruter

Compétences requises :
- Skills manquants dans l'équipe actuelle pour exécuter cette décision
- Formation nécessaire
- Profils à recruter d'urgence si décision GO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIMENSION 4 — IMPACT CONCURRENTIEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Réactions probables des concurrents :
- Concurrent A (leader) : réaction probable + délai de réponse
- Concurrent B (challenger) : réaction probable + délai de réponse
- Concurrent C (entrants) : opportunisme possible

Avantage compétitif créé ou détruit :
- En quoi cette décision renforce ou fragilise le positionnement
- Nouvelles barrières à l'entrée générées
- Nouvelles vulnérabilités exposées

Signal envoyé au marché :
- Comment le marché interprétera cette décision
- Effet sur la réputation et le brand positioning

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIMENSION 5 — IMPACT OPÉRATIONNEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Processus fortement impactés :
- Processus qui disparaissent ou sont transformés
- Nouveaux processus à créer from scratch
- Risques d'interruption de service pendant la transition

Systèmes et outils :
- Systèmes IT / outils à modifier ou remplacer
- Intégrations à refaire ou créer
- Risques techniques et dette technique générée

Risques opérationnels :
- Top 3 risques d'exécution avec probabilité et impact
- Plan de contingence pour chaque risque

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIMENSION 6 — ALIGNEMENT STRATÉGIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mission et vision :
- Dans quelle mesure cette décision sert ou trahit la mission de l'entreprise
- Cohérence avec les valeurs affichées
- Risque de dissonance identitaire (qui sommes-nous vraiment ?)

Positionnement à long terme :
- Cette décision ouvre-t-elle ou ferme-t-elle des options futures ?
- Décisions irrévocables vs. décisions réversibles
- Impact sur la valorisation et l'attractivité pour les investisseurs

══════════════════════════════════════════════════════════════════
◈  PROJECTION TEMPORELLE — 3 TIMELINES
══════════════════════════════════════════════════════════════════

Pour chaque timeline, décris 3 scénarios : OPTIMISTE / RÉALISTE / PESSIMISTE

J+30 (Premier mois) :
OPTIMISTE (probabilité X%) : [ce qui se passe dans le meilleur cas]
RÉALISTE (probabilité X%) : [ce qui se passe probablement]
PESSIMISTE (probabilité X%) : [ce qui se passe si ça déraille]
Indicateurs à surveiller impérativement à J+30 :

J+90 (Trimestre) :
OPTIMISTE (probabilité X%) : [momentum et résultats]
RÉALISTE (probabilité X%) : [état de situation]
PESSIMISTE (probabilité X%) : [spirale négative potentielle]
Critères de go/continue/pivot à J+90 :

J+365 (Un an) :
OPTIMISTE (probabilité X%) : [transformation réussie]
RÉALISTE (probabilité X%) : [bilan net de la décision]
PESSIMISTE (probabilité X%) : [dommages résiduels]
Leçons à retenir quelle que soit l'issue :

══════════════════════════════════════════════════════════════════
◈  VERDICT DU JUMEAU NUMÉRIQUE
══════════════════════════════════════════════════════════════════

RECOMMANDATION FINALE : [GO ✅ / NO-GO ❌ / ADJUST ⚡]

Score de confiance dans la simulation : X/100

Si GO : les 5 conditions non-négociables pour réussir
Si NO-GO : les 3 alternatives à explorer à la place
Si ADJUST : les modifications précises qui transformeraient un NO-GO en GO

Décision miroir : qu'est-ce que le NON-faire de cette décision coûterait à l'entreprise ?
(Car l'inaction est aussi une décision avec ses propres conséquences.)

Premier geste à faire dans les 48 heures :
[3 actions concrètes, assignées à un rôle, avec deadline]

Tout en français. Sois précis, chiffré, audacieux dans les projections. C'est une simulation — ose les hypothèses."""

    bandeau(
        "JUMEAU NUMÉRIQUE — SIMULATEUR DE DÉCISION",
        f"Décision : {decision[:55]}"
    )

    resultat = streamer(prompt)
    chemin = sauvegarder("simulation_decision", resultat)
    print(f"\n  [Simulation sauvegardée : {chemin}]")
    return resultat


# ── Agent 2 — Test de Prix Virtuel ────────────────────────────────────────────

def agent_test_prix_virtuel(nouveau_prix: str, service: str) -> str:
    """
    Simule un changement de prix : élasticité, impact par segment,
    churn estimé, impact CA, analyse break-even.
    """
    incrementer_stat("agent_jumeau_prix")
    contexte_memoire = extraire_contexte_memoire()
    m = charger_memoire()
    clients = m.get("clients", {})

    # Extraction d'un contexte pricing enrichi depuis la mémoire
    segments_detail = []
    for nom, data in clients.items():
        interactions = len(data.get("interactions", []))
        if interactions >= 10:
            tier = "Champion"
        elif interactions >= 5:
            tier = "Grand Compte"
        else:
            tier = "PME"
        segments_detail.append(f"  - {nom} ({data.get('secteur','?')}) — Tier: {tier}, Interactions: {interactions}")

    detail_clients = "\n".join(segments_detail[:15]) if segments_detail else "  Aucun client en mémoire (simulation sur données théoriques)"

    prompt = f"""Tu es le Jumeau Numérique de {ENTREPRISE}, module de simulation tarifaire.
Tu simules en temps réel les conséquences d'un changement de prix sur l'ensemble de la base clients.

Entreprise : {ENTREPRISE} ({DOMAINE})
{contexte_memoire}

SERVICE CONCERNÉ : {service}
NOUVEAU PRIX ENVISAGÉ : {nouveau_prix}

Base clients connue :
{detail_clients}

══════════════════════════════════════════════════════════════════
◈  SIMULATION PRIX VIRTUEL — {service} → {nouveau_prix}
══════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. MODÈLE D'ÉLASTICITÉ-PRIX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Élasticité de la demande pour des solutions IA B2B :
- Coefficient d'élasticité estimé par segment (Champions / Grands Comptes / PME)
  (rappel : élasticité = % variation demande / % variation prix)
- Seuil psychologique de prix à ne pas franchir par segment
- Effet d'ancrage : comment le marché perçoit ce nouveau prix vs. l'actuel
- Analyse willingness-to-pay : quel % de la valeur créée le client est prêt à payer ?

Courbe demande-prix pour {service} :
- Prix actuel → demande actuelle (baseline)
- Nouveau prix {nouveau_prix} → demande projetée
- Prix optimal théorique (maximisation du revenu total)
- Zone de danger (prix qui déclenchent une vague de churn)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
II. IMPACT SEGMENTÉ PAR TYPE DE CLIENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SEGMENT CHAMPIONS (clients historiques, fort engagement) :
  Réaction probable : [description détaillée]
  Probabilité de churn : X% — Raisonnement : [pourquoi]
  Probabilité de renégociation : X%
  Impact CA sur ce segment : +/- X€ estimé
  Message à leur tenir si augmentation : [script recommandé]

SEGMENT GRANDS COMPTES (ETI, contrats pluriannuels) :
  Réaction probable : [description détaillée]
  Probabilité de churn : X% — Raisonnement : [pourquoi]
  Probabilité de renégociation : X%
  Impact CA sur ce segment : +/- X€ estimé
  Levier de rétention recommandé : [action concrète]

SEGMENT PME (clients sensibles au prix, faible switching cost) :
  Réaction probable : [description détaillée]
  Probabilité de churn : X% — Raisonnement : [pourquoi]
  Probabilité de migration vers offre inférieure : X%
  Impact CA sur ce segment : +/- X€ estimé
  Stratégie pour limiter la casse : [action concrète]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
III. IMPACT SUR L'ACQUISITION DE NOUVEAUX CLIENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Le nouveau prix {nouveau_prix} positionne {ENTREPRISE} comment sur le marché ?
- Positionnement relatif vs. concurrents (moins cher / premium / aligné)
- Nouveaux prospects attirés par ce positionnement tarifaire
- Prospects perdus à cause de ce positionnement
- Impact sur le cycle de vente (durée, complexité des négociations)
- Impact sur le CAC (coût d'acquisition client)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IV. ANALYSE REVENUS AVANT / APRÈS + BREAK-EVEN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hypothèses de base (sur la base des données mémoire) :

Scénario AVANT le changement de prix :
  Revenus mensuels estimés sur {service} : X€
  Nombre de clients actifs sur ce service : X
  Revenu moyen par client : X€/mois

Scénario APRÈS le changement à {nouveau_prix} :
  Churn attendu : X clients perdus
  Revenus perdus sur les clients churned : -X€/mois
  Revenus gagnés sur les clients restants : +X€/mois
  Nouveaux clients attirés (6 mois) : +X clients
  Revenus des nouveaux clients : +X€/mois
  IMPACT NET MENSUEL : +/- X€
  IMPACT ANNUALISÉ : +/- X€

Analyse break-even du changement de prix :
  Si churn > X% : la décision est perdante
  Si churn < X% : la décision est gagnante
  Point mort exact : [calcul]
  Délai pour récupérer l'ARR perdu via nouveaux clients : X mois

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V. STRATÉGIE D'IMPLÉMENTATION RECOMMANDÉE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option A — Changement brutal (J+0) :
  Avantages / Inconvénients / Risques / Probabilité de succès : X%

Option B — Transition progressive (grandfathering) :
  Clients existants : maintien du prix actuel pendant X mois, puis hausse
  Nouveaux clients : nouveau prix immédiatement
  Avantages / Inconvénients / Risques / Probabilité de succès : X%

Option C — Restructuration de l'offre (bundling) :
  Intégrer de la valeur ajoutée pour justifier le nouveau prix
  Avantages / Inconvénients / Risques / Probabilité de succès : X%

RECOMMANDATION FINALE : [Option + justification]
Date idéale pour implémenter ce changement : [mois + raisonnement]
Message aux clients : [draft de communication en 3 phrases]

Tout en français. Précis, chiffré, actionnable. Ose simuler les cas extrêmes."""

    bandeau(
        "JUMEAU NUMÉRIQUE — TEST DE PRIX VIRTUEL",
        f"Service : {service}  |  Nouveau prix : {nouveau_prix}"
    )

    resultat = streamer(prompt)
    chemin = sauvegarder(f"simulation_prix_{service.lower().replace(' ', '_')}", resultat)
    print(f"\n  [Simulation sauvegardée : {chemin}]")
    return resultat


# ── Agent 3 — Simulateur de Recrutement ──────────────────────────────────────

def agent_simuler_recrutement(poste: str, budget_annuel: str) -> str:
    """
    Simule l'impact complet d'un recrutement : capacité, ROI, risques,
    break-even, coût d'un mauvais recrutement, alternatives.
    """
    incrementer_stat("agent_jumeau_recrutement")
    contexte_memoire = extraire_contexte_memoire()

    prompt = f"""Tu es le Jumeau Numérique de {ENTREPRISE}, module de simulation RH et organisationnelle.
Tu modélises avec précision l'impact d'un recrutement AVANT qu'il ne soit lancé.

Entreprise : {ENTREPRISE} ({DOMAINE})
{contexte_memoire}

POSTE À RECRUTER : {poste}
BUDGET ANNUEL (SALAIRE CHARGÉ) : {budget_annuel}

══════════════════════════════════════════════════════════════════
◈  SIMULATION RECRUTEMENT — {poste}
══════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. IMPACT SUR LA CAPACITÉ ET LA VÉLOCITÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Capacité actuelle sans ce recrutement :
- Goulots d'étranglement identifiables lié à l'absence de ce profil
- Tâches non faites / mal faites aujourd'hui par manque de ce profil
- Opportunités manquées chaque mois faute de cette ressource

Impact du recrutement sur la vélocité :
- Délai d'onboarding et montée en compétences (J+30 / J+60 / J+90)
- Gain de capacité opérationnelle estimé en % (mois 1 / mois 3 / mois 6)
- Multiplicateur d'équipe : comment ce profil démultiplie les autres
- Nouvelles capacités débloquées qui n'existaient pas avant

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
II. POTENTIEL DE REVENUS DÉBLOQUÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Revenus directement générés ou débloqués par ce recrutement :
- Revenus additionnels projetés à 6 mois : X€ (hypothèses explicites)
- Revenus additionnels projetés à 12 mois : X€
- Revenus indirects (rétention clients, qualité, NPS) : X€ estimé

Cas d'usage concrets :
- 3 exemples de deals / projets / livrables que ce profil permet de faire
  et qui sont impossibles ou dégradés sans lui

Contribution au chiffre d'affaires :
  Si profil commercial : X€ de pipeline généré / deals closés
  Si profil technique : X projets supplémentaires / X% d'amélioration produit
  Si profil support/ops : X% de rétention client / X heures libérées pour le rev

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
III. RISQUE D'UN MAUVAIS RECRUTEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Coût d'un mauvais recrutement (référence : 1,5x le salaire annuel chargé) :
  Budget annuel déclaré : {budget_annuel}
  Coût d'un bad hire estimé : {budget_annuel} × 1,5 = [calcul]

Décomposition du coût d'un mauvais recrutement :
  - Salaire versé avant détection du problème (mois X à Y) : X€
  - Coût managérial (temps perdu en supervision / correction) : X€
  - Coût du re-recrutement (process, agence, temps RH) : X€
  - Coût d'opportunité (projets ralentis, clients insatisfaits) : X€
  - Coût de séparation (préavis, éventuellement rupture conventionnelle) : X€
  - Impact moral sur l'équipe (valeur difficile à chiffrer mais réelle) : +++

Probabilité d'un mauvais recrutement pour ce profil : X%
  (basé sur la difficulté à trouver ce profil sur le marché + criticité du poste)

Signaux d'alerte à surveiller pendant la période d'essai :
  [5 red flags concrets spécifiques à ce poste]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IV. TIMELINE DE BREAK-EVEN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Analyse du retour sur investissement de ce recrutement :

Coût total du recrutement sur 12 mois :
  - Salaire chargé mensuel : [budget_annuel / 12]€/mois
  - Coût du process de recrutement (annonce, entretiens, tests) : X€
  - Équipement et setup : X€
  - Formation et onboarding : X€
  - COÛT TOTAL ANNÉE 1 : X€

Revenus / économies générés par le recrutement :
  Mois 1-2 (ramping) : X€ contribué
  Mois 3-6 (montée en puissance) : X€ contribué
  Mois 7-12 (pleine productivité) : X€ contribué
  TOTAL ANNÉE 1 : X€

BREAK-EVEN : Mois X (quand la contribution dépasse le coût total)
ROI à 12 mois : X%
ROI à 24 mois : X%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V. SCÉNARIOS ALTERNATIFS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Alternative A — FREELANCE / PORTAGE SALARIAL :
  Coût mensuel estimé pour ce profil en freelance : X€
  Avantages : flexibilité, pas de charges, résultats immédiats
  Inconvénients : moins d'engagement, turnover, pas de culture
  Quand choisir cette option : [critères précis]
  Économie vs. CDI sur 12 mois : +/- X€

Alternative B — PARTENARIAT / SOUS-TRAITANCE :
  Trouver un partenaire qui couvre ce besoin
  Coût estimé : X€/projet ou X€/mois
  Avantages : réseau, crédibilité, pas de management
  Inconvénients : marge partagée, dépendance, contrôle limité
  Quand choisir cette option : [critères précis]

Alternative C — AUTOMATISATION / IA :
  Dans quelle mesure une solution IA pourrait couvrir ce besoin ?
  Coût d'une solution d'automatisation : X€
  % du poste automatisable dès aujourd'hui : X%
  Timeline pour atteindre X% d'automatisation : X mois
  Quand choisir cette option : [critères précis]

Alternative D — MONTÉE EN COMPÉTENCES INTERNE :
  Qui dans l'équipe pourrait évoluer vers ce rôle ?
  Délai de montée en compétences : X mois
  Coût de formation : X€
  Risque : distraction de leur poste actuel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VI. RECOMMANDATION FINALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉCISION RECOMMANDÉE : [CDI MAINTENANT / CDI DANS X MOIS / FREELANCE / AUTOMATISER / NE PAS RECRUTER]

Score de confiance : X/100

Justification en 3 arguments chiffrés :
1. [argument financier]
2. [argument stratégique]
3. [argument de timing]

Si GO — Profil idéal du candidat :
  - Expérience indispensable (non-négociable)
  - Compétences techniques clés
  - Soft skills critiques pour ce contexte
  - Red flags à détecter en entretien

Si GO — Les 3 premières missions à confier dès J+1 :
[actions concrètes qui valident le recrutement rapidement]

Tout en français. Précis, chiffré. Ce sont des vies professionnelles et de l'argent réel."""

    bandeau(
        "JUMEAU NUMÉRIQUE — SIMULATION RECRUTEMENT",
        f"Poste : {poste}  |  Budget : {budget_annuel}"
    )

    resultat = streamer(prompt)
    chemin = sauvegarder(f"simulation_recrutement_{poste.lower().replace(' ', '_')}", resultat)
    print(f"\n  [Simulation sauvegardée : {chemin}]")
    return resultat


# ── Agent 4 — War Game Concurrentiel ─────────────────────────────────────────

def agent_war_game(scenario_concurrent: str) -> str:
    """
    Simule un mouvement concurrent et 3 stratégies de réponse.
    Identifie la réponse gagnante et les 5 premières actions dans les 48h.
    """
    incrementer_stat("agent_jumeau_wargame")
    contexte_memoire = extraire_contexte_memoire()

    prompt = f"""Tu es le Jumeau Numérique de {ENTREPRISE}, module de guerre stratégique et simulation concurrentielle.
Tu organises un war game complet pour préparer {ENTREPRISE} à une attaque concurrentielle avant qu'elle ne se produise.

Entreprise : {ENTREPRISE} ({DOMAINE})
{contexte_memoire}

SCÉNARIO CONCURRENT : {scenario_concurrent}

══════════════════════════════════════════════════════════════════
◈  WAR GAME CONCURRENTIEL — SIMULATION 6 MOIS
══════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. ANALYSE DU MOUVEMENT CONCURRENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Décryptage du mouvement : {scenario_concurrent}
- Motivation probable de ce mouvement (pourquoi maintenant ?)
- Ressources mobilisées par le concurrent pour exécuter ce mouvement
- Clients de {ENTREPRISE} les plus exposés à ce mouvement
- Timing : phase d'annonce (J0) / phase d'exécution (J+30-90) / impact plein (J+6 mois)
- Crédibilité du mouvement : probabilité qu'ils exécutent vraiment (X%)

Impact immédiat non-simulé (si aucune réponse de {ENTREPRISE}) :
- Perte de revenus estimée à 6 mois : X€
- Clients à risque immédiat : [profils]
- Deals en cours menacés : [types de deals]
- Réputation sur le marché : [impact]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
II. STRATÉGIE DE RÉPONSE A — CONTRE-ATTAQUE FRONTALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Description : Répliquer directement le mouvement concurrent, voire le surpasser

Actions concrètes (timeline J0 → J+180) :
  J0-J+7 : [actions immédiates]
  J+7-J+30 : [mobilisation ressources]
  J+30-J+90 : [exécution]
  J+90-J+180 : [consolidation]

Ressources requises :
  Budget estimé : X€
  Équipe mobilisée : [rôles]
  Délai d'exécution : X semaines

Résultats projetés à 6 mois :
  Part de marché défendue : X%
  Revenus protégés : X€
  Nouveaux revenus générés : X€
  Bilan net : +/- X€

Risques de cette stratégie :
  1. [risque majeur]
  2. [risque secondaire]
  3. [piège à éviter]

Score de succès : X/100
Signal de victoire : [comment savoir que cette stratégie fonctionne ?]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
III. STRATÉGIE DE RÉPONSE B — DIFFÉRENCIATION RADICALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Description : Ne pas jouer leur jeu — aller là où ils ne peuvent pas nous suivre

Principe : pendant qu'ils font X, nous allons faire Y qui démontre notre supériorité sur d'autres axes

Actions concrètes (timeline J0 → J+180) :
  J0-J+7 : [repositionnement messaging]
  J+7-J+30 : [renforcement des avantages distinctifs]
  J+30-J+90 : [nouvelles offres / fonctionnalités / marchés]
  J+90-J+180 : [leadership consolidé sur nouveaux axes]

Ressources requises :
  Budget estimé : X€
  Équipe mobilisée : [rôles]
  Délai d'exécution : X semaines

Résultats projetés à 6 mois :
  Nouveaux clients attirés par le repositionnement : X
  Revenus protégés (clients fidèles à notre différenciation) : X€
  Nouveaux revenus : X€
  Bilan net : +/- X€

Risques de cette stratégie :
  1. [risque majeur]
  2. [risque secondaire]
  3. [piège à éviter]

Score de succès : X/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IV. STRATÉGIE DE RÉPONSE C — REPLI STRATÉGIQUE ET FOCALISATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Description : Accepter de perdre un segment / terrain pour dominer encore plus fort ailleurs

Principe : "Tout tenter de défendre, c'est tout perdre" — choisir ses batailles

Actions concrètes (timeline J0 → J+180) :
  J0-J+7 : [audit des positions à défendre vs. à abandonner]
  J+7-J+30 : [concentration des ressources sur le cœur]
  J+30-J+90 : [domination verticale sur le segment prioritaire]
  J+90-J+180 : [expansion depuis une position de force]

Ressources libérées par l'abandon de certains segments : X€/mois
Ressources redirigées vers le cœur : X€

Résultats projetés à 6 mois :
  Revenus perdus (abandon segments) : -X€
  Revenus gagnés (domination cœur) : +X€
  Bilan net : +/- X€

Risques de cette stratégie :
  1. [risque de perception : "ils battent en retraite"]
  2. [risque de perte de clients dans les segments abandonnés]
  3. [risque que la focalisation ne suffise pas]

Score de succès : X/100

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V. VERDICT DU WAR GAME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STRATÉGIE GAGNANTE : [A / B / C / Hybride A+B]

Pourquoi cette stratégie bat les autres dans ce scénario :
  Argument 1 : [argument financier]
  Argument 2 : [argument temporel]
  Argument 3 : [argument de ressources]

Tableau comparatif des 3 stratégies :
  Stratégie A → Score X/100 — Bilan net 6 mois : +/- X€
  Stratégie B → Score X/100 — Bilan net 6 mois : +/- X€
  Stratégie C → Score X/100 — Bilan net 6 mois : +/- X€

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VI. LES 5 ACTIONS À LANCER DANS LES 48 HEURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ ACTION 1 (Aujourd'hui, avant 18h) :
  Quoi : [action précise]
  Qui : [rôle responsable]
  Pourquoi c'est urgent : [impact si non fait]

⚡ ACTION 2 (Demain matin) :
  Quoi : [action précise]
  Qui : [rôle responsable]
  Résultat attendu : [outcome mesurable]

⚡ ACTION 3 (Dans les 24h) :
  Quoi : [action précise]
  Qui : [rôle responsable]
  Résultat attendu : [outcome mesurable]

⚡ ACTION 4 (Dans les 48h) :
  Quoi : [action précise]
  Qui : [rôle responsable]
  Résultat attendu : [outcome mesurable]

⚡ ACTION 5 (Avant la fin de la semaine) :
  Quoi : [action précise]
  Qui : [rôle responsable]
  Résultat attendu : [outcome mesurable]

Signaux d'alarme à surveiller (indicateurs que la situation se dégrade) :
  Signal 1 : [déclencheur]
  Signal 2 : [déclencheur]
  Signal 3 : [déclencheur]

Plan de contingence si dégradation : [action d'urgence]

Tout en français. Simulation de guerre stratégique de haut niveau. Sois impitoyable dans l'analyse."""

    bandeau(
        "JUMEAU NUMÉRIQUE — WAR GAME CONCURRENTIEL",
        f"Scénario : {scenario_concurrent[:55]}"
    )

    resultat = streamer(prompt)
    chemin = sauvegarder("war_game_concurrent", resultat)
    print(f"\n  [Simulation sauvegardée : {chemin}]")
    return resultat


# ── Agent 5 — Simulateur de Pivot ─────────────────────────────────────────────

def agent_simuler_pivot(nouveau_marche: str, nouveau_modele: str) -> str:
    """
    Simule un pivot stratégique (marché / modèle) :
    courbe J, rétention clients actuels, besoins en cash,
    point of no return, score de probabilité de succès.
    """
    incrementer_stat("agent_jumeau_pivot")
    contexte_memoire = extraire_contexte_memoire()

    prompt = f"""Tu es le Jumeau Numérique de {ENTREPRISE}, module de simulation de pivot stratégique.
Tu modélises avec une précision chirurgicale ce qui se passe quand une entreprise change de cap.

Entreprise : {ENTREPRISE} ({DOMAINE})
{contexte_memoire}

NOUVEAU MARCHÉ CIBLE : {nouveau_marche}
NOUVEAU MODÈLE D'AFFAIRES : {nouveau_modele}

══════════════════════════════════════════════════════════════════
◈  SIMULATION PIVOT STRATÉGIQUE
══════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I. DIAGNOSTIC DU PIVOT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type de pivot selon la taxonomie Lean Startup :
  [Zoom-in / Zoom-out / Customer segment / Customer need /
   Platform / Business architecture / Value capture / Channel /
   Technology] — lequel correspond le mieux ?

Distance du pivot (1 = ajustement, 10 = révolution totale) : X/10
  Justification : [pourquoi ce score]

Actifs transférables (ce qui reste valable après le pivot) :
  - Technologie : [ce qui est réutilisable]
  - Clients : [segments qui suivront probablement]
  - Équipe : [compétences qui restent pertinentes]
  - Réputation : [capital marque transférable]
  - Données : [assets données réutilisables]

Actifs obsolètes (ce qui devient inutile ou négatif) :
  - [liste des choses à abandonner]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
II. COURBE J — MODÉLISATION DE LA TRANSITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

La courbe J représente la chute initiale des revenus avant la remontée.

Phase 1 — La descente (Mois 1 à X) :
  Revenus perdus sur l'activité actuelle (décélération) :
    Mois 1 : -X% vs. baseline
    Mois 2 : -X%
    Mois 3 : -X%
    [jusqu'au creux]
  Raisons de la descente : [distraction managériale, clients perdus, focus splitting]
  Creux minimal estimé : -X% du revenu actuel au mois X

Phase 2 — Le fond du creux (Mois X à X) :
  Durée estimée : X semaines / mois
  Ce qui se passe au fond : [restructuration, focus total sur le nouveau modèle]
  Signal que le creux est passé : [indicateur]
  Trésorerie consommée pendant cette phase : X€

Phase 3 — La remontée (Mois X à X) :
  Premiers revenus du nouveau modèle / marché :
    Mois X : X€ (premiers contrats pilotes)
    Mois X+3 : X€ (accélération)
    Mois X+6 : X€ (croisement avec baseline)
  Revenu au niveau de baseline : atteint au mois X
  Revenu au-delà de baseline : atteint au mois X

Visualisation de la courbe J (en valeurs relatives) :
  Mois 0   : ████████████████████ 100% (baseline)
  Mois 3   : ████████████████ 80% (déclin)
  Mois 6   : ████████████ 60% (creux)
  Mois 9   : ██████████████ 70% (amorce remontée)
  Mois 12  : ████████████████████ 100% (retour baseline)
  Mois 18  : ████████████████████████████ 140% (dépassement)
  [Adapter les chiffres au contexte du pivot]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
III. RÉTENTION DE LA BASE CLIENTS ACTUELLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Segments clients actuels et leur comportement probable face au pivot :

Champions (clients les plus engagés) :
  Probabilité de rester : X%
  Raison principale de rester : [pourquoi ils restent]
  Raison principale de partir : [pourquoi certains partent]
  Stratégie de rétention : [action concrète]

Grands Comptes :
  Probabilité de rester : X%
  Risque contractuel (clauses de résiliation ?) : [analyse]
  Stratégie de rétention : [action concrète]

PME :
  Probabilité de rester : X%
  Sensibilité au changement : [élevée / moyenne / faible]
  Stratégie de rétention : [action concrète]

ARR à risque lors du pivot : X€ (X% de l'ARR total)
ARR probable conservé après pivot : X€

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IV. COURBE D'ACQUISITION SUR LE NOUVEAU MARCHÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Marché cible : {nouveau_marche}
Modèle cible : {nouveau_modele}

Hypothèses d'acquisition sur le nouveau marché :
  CAC initial (sans réputation sur ce marché) : X€
  CAC stabilisé (après 6 mois de présence) : X€
  Cycle de vente moyen sur ce marché : X semaines
  ARPU moyen attendu sur ce marché : X€/mois

Courbe d'acquisition projetée :
  Mois 1-3 (Exploration) : X nouveaux clients — X€ ARR additionnel
  Mois 4-6 (Premiers succès) : X nouveaux clients — X€ ARR additionnel
  Mois 7-9 (Accélération) : X nouveaux clients — X€ ARR additionnel
  Mois 10-12 (Scaling) : X nouveaux clients — X€ ARR additionnel
  ARR total nouveau marché à 12 mois : X€

Facteurs d'accélération de l'acquisition :
  [Quels assets de l'ancien marché peuvent accélérer l'acquisition sur le nouveau ?]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V. BESOINS EN CASH PENDANT LA TRANSITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Modélisation des flux de trésorerie pendant le pivot :

Dépenses additionnelles liées au pivot :
  - Développement produit pour le nouveau marché : X€
  - Marketing et go-to-market nouveau marché : X€
  - Recrutements nécessaires (nouveaux profils) : X€/mois
  - Restructuration / séparations éventuelles : X€
  - Conseil externe (juridique, marché) : X€
  - CAPEX pivot total estimé : X€

Cash burn net pendant la phase de descente (creux J) :
  Burn mensuel supplémentaire vs. aujourd'hui : +X€/mois
  Durée de la phase de transition : X mois
  Cash additionnel requis pour passer le creux : X€

Scénario de trésorerie :
  Cash disponible aujourd'hui (hypothèse) : X€
  Cash requis pour financer le pivot : X€
  Gap de financement : X€ (si positif → levée nécessaire)
  Sources de financement du pivot : [fonds propres / dette / levée / subventions]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VI. POINT OF NO RETURN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Le "point of no return" est le moment où revenir en arrière coûterait plus cher que d'aller de l'avant.

Pour ce pivot, le point of no return est atteint quand :
  1. [condition 1 — ex: X% des clients actuels ont churné]
  2. [condition 2 — ex: X€ ont été investis dans le nouveau marché]
  3. [condition 3 — ex: l'équipe a été restructurée pour le nouveau profil]
  4. [condition 4 — ex: X mois se sont écoulés depuis l'annonce]

Délai estimé avant d'atteindre le point of no return : X semaines

Coût de l'abandon après le point of no return : X€

Fenêtre de réversibilité totale (avant le point of no return) :
  Durée : X semaines depuis la décision de pivot
  Coût de l'abandon dans cette fenêtre : X€ (raisonnable)
  Recommandation : si doutes, décider dans les X semaines

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VII. SCORE DE PROBABILITÉ DE SUCCÈS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCORE DE SUCCÈS DU PIVOT : X / 100

Décomposition du score :
  Adéquation du nouveau marché avec les assets existants (0-25) : X/25
  Viabilité financière de la transition (0-25) : X/25
  Capacité de l'équipe à exécuter ce pivot (0-25) : X/25
  Timing marché (0-25) : X/25

Interprétation :
  80-100 : Pivot hautement recommandé, forte probabilité de succès
  60-79  : Pivot viable avec les bonnes conditions en place
  40-59  : Pivot risqué — conditions à créer avant de lancer
  0-39   : Pivot non recommandé dans ces conditions — revoir la stratégie

Les 3 conditions sine qua non pour que ce pivot réussisse :
  1. [condition non-négociable]
  2. [condition non-négociable]
  3. [condition non-négociable]

Killer assumption (l'hypothèse dont tout dépend) :
  Si [hypothèse X] est vraie → le pivot réussit.
  Comment valider cette hypothèse en moins de 30 jours et moins de 5 000€ : [méthode]

VERDICT FINAL : [PIVOTER MAINTENANT / PRÉPARER ENCORE X MOIS / NE PAS PIVOTER]

Tout en français. Simulation stratégique de niveau executive. Ose les projections chiffrées même incertaines."""

    bandeau(
        "JUMEAU NUMÉRIQUE — SIMULATION DE PIVOT",
        f"Vers : {nouveau_marche}  |  Modèle : {nouveau_modele}"
    )

    resultat = streamer(prompt)
    chemin = sauvegarder("simulation_pivot", resultat)
    print(f"\n  [Simulation sauvegardée : {chemin}]")
    return resultat


# ── Menu Principal ─────────────────────────────────────────────────────────────

def afficher_menu():
    print("\n")
    print("  ╔══════════════════════════════════════════════════════════════╗")
    print("  ║        ◈  JUMEAU NUMÉRIQUE — Digital Twin Business  ◈        ║")
    print("  ║   Simulez l'impact de vos décisions AVANT de les prendre.   ║")
    print("  ║         Univers parallèle. Risque zéro. Futur clair.        ║")
    print("  ╚══════════════════════════════════════════════════════════════╝")
    print()
    print("  [1]  Simuler une Décision       — Impact 6D + Timelines J+30/90/365")
    print("  [2]  Tester un Prix Virtuel     — Élasticité, segments, break-even")
    print("  [3]  Simuler un Recrutement     — ROI, bad hire, alternatives, break-even")
    print("  [4]  War Game Concurrent        — 3 stratégies de réponse, 5 actions 48h")
    print("  [5]  Simuler un Pivot           — Courbe J, cash, point of no return")
    print()
    print("  [0]  Quitter le jumeau numérique")
    print()
    print("  ▓" * 34)


def main():
    while True:
        afficher_menu()
        choix = input("\n  Entrez votre choix : ").strip()

        if choix == "0":
            print("\n  Au revoir. Le jumeau numérique reste en veille.")
            print("  Vos décisions sont entre de bonnes mains.\n")
            break

        elif choix == "1":
            print("\n  ── SIMULATEUR DE DÉCISION ──")
            print("  Exemples : 'lancer un nouveau produit', 'augmenter les prix de 20%',")
            print("             'recruter une équipe commerciale', 'ouvrir un bureau à Berlin'")
            decision = input("\n  Décision à simuler : ").strip()
            if not decision:
                print("  Erreur : la décision est requise.")
                continue
            contexte = input("  Contexte additionnel (optionnel, appuyez sur Entrée pour passer) : ").strip()
            if not contexte:
                contexte = "Aucun contexte additionnel fourni."
            agent_simuler_decision(decision, contexte)

        elif choix == "2":
            print("\n  ── TEST DE PRIX VIRTUEL ──")
            print("  Exemples de services : 'Agent IA sur mesure', 'Abonnement mensuel SaaS',")
            print("                         'Formation agents IA', 'Audit automatisation'")
            service = input("\n  Service concerné : ").strip()
            if not service:
                print("  Erreur : le service est requis.")
                continue
            nouveau_prix = input("  Nouveau prix envisagé (ex: 2 500€/mois, 15 000€/projet) : ").strip()
            if not nouveau_prix:
                print("  Erreur : le nouveau prix est requis.")
                continue
            agent_test_prix_virtuel(nouveau_prix, service)

        elif choix == "3":
            print("\n  ── SIMULATEUR DE RECRUTEMENT ──")
            print("  Exemples : 'Sales Engineer IA', 'Développeur Python senior',")
            print("             'Customer Success Manager', 'Head of Marketing', 'CTO'")
            poste = input("\n  Poste à recruter : ").strip()
            if not poste:
                print("  Erreur : le poste est requis.")
                continue
            budget_annuel = input("  Budget annuel chargé (ex: 70 000€, 90K€, 120 000€) : ").strip()
            if not budget_annuel:
                print("  Erreur : le budget annuel est requis.")
                continue
            agent_simuler_recrutement(poste, budget_annuel)

        elif choix == "4":
            print("\n  ── WAR GAME CONCURRENTIEL ──")
            print("  Exemples de scénarios :")
            print("    - 'Un concurrent lance une offre gratuite pour les PME'")
            print("    - 'Notre principal concurrent lève 20M€'")
            print("    - 'Google intègre des agents IA natifs dans Workspace'")
            print("    - 'Un concurrent débauche notre meilleur commercial'")
            scenario = input("\n  Scénario concurrent : ").strip()
            if not scenario:
                print("  Erreur : le scénario est requis.")
                continue
            agent_war_game(scenario)

        elif choix == "5":
            print("\n  ── SIMULATEUR DE PIVOT ──")
            print("  Exemples de nouveaux marchés : 'secteur santé', 'PME industrielles',")
            print("                                 'marchés anglophones', 'RH et recrutement'")
            print("  Exemples de nouveaux modèles : 'usage-based pricing', 'marketplace d\\'agents',")
            print("                                 'franchise IA', 'SaaS vertical spécialisé'")
            nouveau_marche = input("\n  Nouveau marché cible : ").strip()
            if not nouveau_marche:
                print("  Erreur : le nouveau marché est requis.")
                continue
            nouveau_modele = input("  Nouveau modèle d'affaires : ").strip()
            if not nouveau_modele:
                print("  Erreur : le nouveau modèle est requis.")
                continue
            agent_simuler_pivot(nouveau_marche, nouveau_modele)

        else:
            print("\n  Choix invalide. Entrez un chiffre entre 0 et 5.")
            continue

        input("\n  [Appuyez sur Entrée pour revenir au menu du jumeau numérique]")


if __name__ == "__main__":
    main()
