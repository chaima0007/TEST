"""
╔══════════════════════════════════════════════════════════════════════╗
║              L'ORACLE — INTELLIGENCE PROPHÉTIQUE                    ║
║         Lit tous les signaux. Prédit l'avenir. Agit avant.          ║
╚══════════════════════════════════════════════════════════════════════╝

Système de prédiction et détection de signaux faibles pour l'entreprise.
Analyse l'intégralité des données mémorisées et projette les trajectoires.

Usage : python agent_oracle.py
"""

import os
import sys
import json
from datetime import datetime, timedelta
from google import genai
from google.genai import types

from memoire import charger_memoire, incrementer_stat

# ─── Configuration ────────────────────────────────────────────
API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] Variable GEMINI_API_KEY non définie. Exécutez : export GEMINI_API_KEY=votre_cle")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

ENTREPRISE = "AgentClaude Solutions"
ORACLE_DIR = os.path.join("fichiers", "oracle")
os.makedirs(ORACLE_DIR, exist_ok=True)

LARGEUR = 72


# ═══════════════════════════════════════════════════════════════
# UTILITAIRES
# ═══════════════════════════════════════════════════════════════

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


def _sep(car="═", n=LARGEUR):
    return car * n


def _titre(texte, car="═"):
    return f"\n{_sep(car)}\n  {texte}\n{_sep(car)}"


def _jours_depuis(date_str: str) -> int:
    """Calcule le nombre de jours depuis une date ISO."""
    try:
        date = datetime.fromisoformat(date_str)
        return (datetime.now() - date).days
    except Exception:
        return 0


def _statut_facture(facture: dict) -> str:
    if facture.get("payee"):
        return "PAYEE"
    date_echeance_str = facture.get("date_echeance")
    if date_echeance_str:
        try:
            date_echeance = datetime.fromisoformat(date_echeance_str)
            if datetime.now() > date_echeance:
                return "EN RETARD"
        except Exception:
            pass
    return "EN ATTENTE"


def _streamer(prompt: str, temperature: float = 0.7) -> str:
    """Appelle Gemini en streaming et retourne le texte complet."""
    modele = _creer_model(
        model_name=MODEL,
        generation_config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=8192,
        ),
    )
    print()
    texte = ""
    for chunk in modele.generate_content(prompt, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
            texte += chunk.text
    print("\n")
    return texte


def _sauvegarder(nom_fichier: str, contenu: str) -> str:
    """Sauvegarde un rapport dans fichiers/oracle/ et retourne le chemin."""
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = os.path.join(ORACLE_DIR, f"{nom_fichier}_{horodatage}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


def _serialiser_memoire(memoire: dict) -> str:
    """Convertit la mémoire en texte structuré pour le prompt."""
    lignes = []
    now = datetime.now()

    # ── Clients ──
    clients = memoire.get("clients", {})
    lignes.append(f"=== CLIENTS ({len(clients)}) ===")
    for nom, c in clients.items():
        interactions_client = c.get("interactions", [])
        dernier_contact = None
        if interactions_client:
            try:
                dernier_contact = max(
                    (i.get("date", "") for i in interactions_client if i.get("date")),
                    default=None
                )
            except Exception:
                pass
        jours_silence = _jours_depuis(dernier_contact) if dernier_contact else 999
        lignes.append(
            f"  Client: {nom} | Secteur: {c.get('secteur','?')} | "
            f"Statut: {c.get('statut','?')} | "
            f"Interactions: {len(interactions_client)} | "
            f"Silence depuis: {jours_silence}j | "
            f"Besoin: {c.get('besoin_principal','?')}"
        )
        if interactions_client:
            # Dates des 3 dernières interactions
            dates = sorted(
                [i.get("date", "") for i in interactions_client if i.get("date")],
                reverse=True
            )[:3]
            lignes.append(f"    Dernières interactions: {', '.join(dates)}")

    # ── Factures ──
    factures = memoire.get("factures", [])
    lignes.append(f"\n=== FACTURES ({len(factures)}) ===")
    for f in factures:
        statut = _statut_facture(f)
        client_nom = f.get("client", {}).get("nom", f.get("client_nom", "?"))
        if isinstance(f.get("client"), str):
            client_nom = f["client"]
        jours_retard = 0
        if statut == "EN RETARD":
            jours_retard = _jours_depuis(f.get("date_echeance", ""))
        lignes.append(
            f"  Facture: {f.get('numero','?')} | Client: {client_nom} | "
            f"Montant: {f.get('total_ttc', f.get('montant_ttc', 0)):.0f}€ TTC | "
            f"Statut: {statut} | "
            f"Retard: {jours_retard}j | "
            f"Émise: {f.get('date_emission', f.get('date_creation','?'))[:10] if f.get('date_emission') or f.get('date_creation') else '?'}"
        )

    # ── Tickets ──
    tickets = memoire.get("tickets", [])
    lignes.append(f"\n=== TICKETS SUPPORT ({len(tickets)}) ===")
    for t in tickets:
        lignes.append(
            f"  Ticket: {t.get('ref','?')} | Client: {t.get('client','?')} | "
            f"Urgence: {t.get('urgence','?')} | "
            f"Résolu: {'Oui' if t.get('resolu') else 'Non'} | "
            f"Sujet: {str(t.get('question', t.get('sujet','?')))[:80]}"
        )

    # ── Projets ──
    projets = memoire.get("projets", {})
    lignes.append(f"\n=== PROJETS ({len(projets)}) ===")
    for nom_p, p in projets.items():
        derniere_maj = p.get("derniere_mise_a_jour", p.get("date_mise_a_jour", ""))
        jours_maj = _jours_depuis(derniere_maj) if derniere_maj else 999
        lignes.append(
            f"  Projet: {nom_p} | Client: {p.get('client','?')} | "
            f"Statut: {p.get('statut','?')} | "
            f"Avancement: {p.get('avancement', p.get('progression', 0))}% | "
            f"Dernière MAJ: {jours_maj}j | "
            f"Budget: {p.get('budget', 0)}€"
        )

    # ── Interactions globales (30 dernières) ──
    interactions = memoire.get("interactions", [])
    lignes.append(f"\n=== INTERACTIONS GLOBALES ({len(interactions)} total, 30 dernières) ===")
    interactions_triees = sorted(
        interactions,
        key=lambda x: x.get("date", ""),
        reverse=True
    )[:30]
    for i in interactions_triees:
        lignes.append(
            f"  [{i.get('date','?')[:10]}] {i.get('client','?')} | "
            f"{i.get('action','?')} | {str(i.get('resultat',''))[:60]}"
        )

    # ── Stats agents ──
    stats = memoire.get("stats", {})
    agents_utilises = stats.get("agents_utilises", {})
    lignes.append(f"\n=== UTILISATION AGENTS (total: {stats.get('total_demandes', 0)} requêtes) ===")
    for agent, nb in sorted(agents_utilises.items(), key=lambda x: x[1], reverse=True):
        lignes.append(f"  {agent}: {nb} utilisations")

    return "\n".join(lignes)


# ═══════════════════════════════════════════════════════════════
# AGENT 1 — ORACLE BRIEFING HEBDOMADAIRE
# ═══════════════════════════════════════════════════════════════

def agent_oracle_semaine():
    """
    Lit TOUTES les données et prédit ce qui va se passer cette semaine :
    quel client va contacter, quelle facture sera en retard, quel projet
    va avoir un problème, quel prospect va convertir.
    """
    print(_titre("🔮  ORACLE — BRIEFING HEBDOMADAIRE  🔮"))
    print(f"\n  Consultation des étoiles de données en cours...")
    print(f"  Date de la vision : {datetime.now().strftime('%A %d %B %Y à %H:%M')}\n")

    memoire = charger_memoire()
    donnees = _serialiser_memoire(memoire)
    incrementer_stat("oracle_semaine")

    prompt = f"""Tu es L'ORACLE, un système d'intelligence prophétique pour {ENTREPRISE}.
Tu as accès à l'intégralité des données de l'entreprise et tu dois prédire ce qui va se passer cette semaine.

DONNÉES COMPLÈTES DE L'ENTREPRISE :
{donnees}

Date actuelle : {datetime.now().strftime('%d/%m/%Y')}

Génère un ORACLE WEEKLY BRIEFING en français, avec un ton mystique mais rigoureusement fondé sur les données.

Structure ton rapport ainsi :

╔══════════════════════════════════════════════════════════════╗
║              ✦ ORACLE WEEKLY BRIEFING ✦                      ║
║         Les Étoiles de Données ont Parlé                     ║
╚══════════════════════════════════════════════════════════════╝

🌟 VISION I — LES CLIENTS QUI VONT SE MANIFESTER
Pour chaque client susceptible de contacter l'entreprise cette semaine :
- Probabilité en % (basée sur fréquence d'interaction passée)
- Raison de la prédiction (patterns de contact, délai depuis dernier contact)
- Action préemptive recommandée (contacter avant eux, préparer tel dossier)

⚡ VISION II — LES FACTURES QUI VONT SOUFFRIR
Pour chaque facture à risque de retard :
- Probabilité de retard en % (historique de paiement du client)
- Jour probable du dépassement
- Action préemptive (relance préventive, appel, négociation)

🌑 VISION III — LES PROJETS QUI CHANCELLENT
Pour chaque projet montrant des signes de turbulence :
- Probabilité de problème en % (fréquence des mises à jour, avancement)
- Nature probable du problème
- Intervention recommandée

💫 VISION IV — LES PROSPECTS QUI VONT BASCULER
Pour chaque prospect proche de la conversion :
- Score d'engagement estimé
- Élément déclencheur probable
- Action pour accélérer la conversion

⭐ ORACLE SUMMARY
Un paragraphe conclusif résumant la semaine à venir, les 3 actions les plus urgentes,
et un conseil mystique mais actionnable.

Note : Si certaines données sont vides ou insuffisantes, indique-le poétiquement
et génère des prédictions basées sur ce qui est disponible.
Le ton doit être celui d'un oracle data-driven : précis, chiffré, mais envoûtant."""

    texte = _streamer(prompt, temperature=0.7)

    chemin = _sauvegarder("oracle_hebdo", texte)
    print(f"  ✦ Vision sauvegardée → {chemin}\n")
    return texte


# ═══════════════════════════════════════════════════════════════
# AGENT 2 — DÉTECTEUR DE SIGNAUX FAIBLES
# ═══════════════════════════════════════════════════════════════

def agent_detecter_signaux_faibles():
    """
    Détecte les signaux faibles annonciateurs de changements :
    churn client, stress de trésorerie, patterns de croissance, etc.
    Comme un sismographe pour le business.
    """
    print(_titre("⚡  DÉTECTEUR DE SIGNAUX FAIBLES  ⚡"))
    print(f"\n  Calibration du sismographe business...")
    print(f"  Analyse des micro-tremblements en cours...\n")

    memoire = charger_memoire()
    donnees = _serialiser_memoire(memoire)
    incrementer_stat("oracle_signaux_faibles")

    prompt = f"""Tu es le SISMOGRAPHE DE L'ORACLE pour {ENTREPRISE}.
Ta mission : détecter les signaux faibles qui annoncent un changement avant qu'il soit visible.
Ces signaux sont souvent imperceptibles seuls, mais révélateurs ensemble.

DONNÉES COMPLÈTES DE L'ENTREPRISE :
{donnees}

Date actuelle : {datetime.now().strftime('%d/%m/%Y')}

Analyse ces données et identifie tous les signaux faibles détectables.
Pour chaque signal trouvé, présente-le dans ce format exact :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ SIGNAL : [Nom court et percutant du signal]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Intensité   : [⚡] à [⚡⚡⚡⚡⚡] (1 à 5 éclairs)
  Catégorie   : [CHURN / TRÉSORERIE / CROISSANCE / OPÉRATIONNEL / MARCHÉ]
  Observation : [Ce que les données montrent concrètement — avec chiffres]
  Signification: [Ce que cela pourrait annoncer]
  Confiance   : [X%] — [justification de ce niveau de confiance]
  Monitoring  : [Action de surveillance recommandée — spécifique et mesurable]

Catégories à analyser :

🔴 SIGNAUX DE CHURN (clients qui vont partir)
- Baisse de fréquence des interactions avec un client actif
- Client qui ne répond plus aux communications
- Tickets de support en augmentation pour un client
- Projet qui stagne sans nouvelles

🟡 SIGNAUX DE TRÉSORERIE (stress financier)
- Délais de paiement qui s'allongent
- Factures en retard qui s'accumulent
- Concentrations sur peu de gros clients
- Mois sans nouvelles factures

🟢 SIGNAUX DE CROISSANCE (opportunités qui émergent)
- Agents spécifiques de plus en plus sollicités
- Client qui multiplie les demandes
- Pattern d'interaction qui évolue

🔵 SIGNAUX OPÉRATIONNELS
- Agents sous-utilisés
- Types de tickets récurrents
- Projets qui ne se terminent jamais

Termine par :
╔══════════════════════════════════════════════════════════════╗
║ LECTURE GLOBALE DU SISMOGRAPHE                               ║
╚══════════════════════════════════════════════════════════════╝
Un paragraphe sur l'état vibratoire de l'entreprise et les 3 signaux
les plus urgents à surveiller cette semaine."""

    texte = _streamer(prompt, temperature=0.6)

    chemin = _sauvegarder("signaux_faibles", texte)
    print(f"  ⚡ Sismogramme sauvegardé → {chemin}\n")
    return texte


# ═══════════════════════════════════════════════════════════════
# AGENT 3 — PRÉDICTION D'OPPORTUNITÉS CACHÉES
# ═══════════════════════════════════════════════════════════════

def agent_prediction_opportunite():
    """
    Scanne tous les patterns de données pour identifier les opportunités
    cachées : client sous-exploité, service non vendu, fenêtre de timing,
    cross-sell basé sur profils similaires.
    Classe par valeur potentielle et facilité de capture.
    """
    print(_titre("💎  ORACLE DES OPPORTUNITÉS CACHÉES  💎"))
    print(f"\n  Fouille des veines d'or dans les données...")
    print(f"  Cartographie des richesses inexploitées...\n")

    memoire = charger_memoire()
    donnees = _serialiser_memoire(memoire)
    incrementer_stat("oracle_opportunites")

    prompt = f"""Tu es le PROSPECTEUR DE L'ORACLE pour {ENTREPRISE}.
Ta mission : identifier les opportunités cachées que les données révèlent mais que personne n'a encore exploitées.
Ces opportunités sont là, dans les patterns, les silences, les comparaisons.

DONNÉES COMPLÈTES DE L'ENTREPRISE :
{donnees}

Date actuelle : {datetime.now().strftime('%d/%m/%Y')}

Identifie et présente TOUTES les opportunités détectables.
Range-les par ordre décroissant de priorité (valeur potentielle × facilité).

Pour chaque opportunité :

╔══════════════════════════════════════════════════════════════╗
║ OPPORTUNITÉ #[N] — [Titre accrocheur]                        ║
╚══════════════════════════════════════════════════════════════╝
  Type           : [UPSELL / CROSS-SELL / RÉACTIVATION / TIMING / NOUVEAU SERVICE]
  Client(s)      : [qui est concerné]
  Valeur potentielle : [estimation en € ou fourchette]
  Facilité       : [FACILE / MODÉRÉE / DIFFICILE] — [pourquoi]
  Signal déclencheur: [ce que les données montrent précisément]
  Fenêtre d'action  : [maintenant / ce mois / ce trimestre]
  Script d'approche : [comment aborder le sujet — 2-3 phrases concrètes]
  ──────────────────────────────────────────────────────────────

Types d'opportunités à rechercher :

1. CLIENTS SOUS-SERVIS
   - Client actif avec peu de services utilisés vs ses besoins identifiés
   - Client dont les interactions révèlent des besoins non adressés
   - Client qui utilise un service basique alors qu'il pourrait aller plus loin

2. SERVICES NON VENDUS AUX BONS CLIENTS
   - Un service populaire chez certains clients mais absent pour d'autres de même profil
   - Pattern : "les clients du secteur X achètent toujours Y et Z ensemble"

3. FENÊTRES DE TIMING
   - Fin d'année fiscale = budget à dépenser
   - Nouveaux projets imminents = besoin de support
   - Période de croissance détectable = besoin de scalabilité

4. RÉACTIVATION DE DORMANTS
   - Prospects qui ont montré de l'intérêt mais n'ont pas converti
   - Anciens clients inactifs

5. EFFETS RÉSEAU ET RECOMMANDATIONS
   - Clients satisfaits dans des secteurs où l'entreprise cherche à grandir

Termine par un CLASSEMENT FINAL des 5 meilleures opportunités avec
une note composite (valeur × facilité × urgence) et le ROI estimé du temps investi."""

    texte = _streamer(prompt, temperature=0.65)

    chemin = _sauvegarder("opportunites_cachees", texte)
    print(f"  💎 Carte des opportunités sauvegardée → {chemin}\n")
    return texte


# ═══════════════════════════════════════════════════════════════
# AGENT 4 — CHRONOLOGIE FUTURE (NARRATIVE 12 MOIS)
# ═══════════════════════════════════════════════════════════════

def agent_chronologie_future(evenements_planifies: str = ""):
    """
    Génère un récit narratif des 12 prochains mois basé sur la trajectoire actuelle.
    Mois par mois. Points d'inflexion. Moments de vérité. Style documentaire.
    """
    print(_titre("📖  CHRONOLOGIE DU FUTUR — LES 12 PROCHAINS MOIS  📖"))
    print(f"\n  Déroulement des fils du temps...")
    print(f"  Projection de la trajectoire en cours...\n")

    memoire = charger_memoire()
    donnees = _serialiser_memoire(memoire)
    incrementer_stat("oracle_chronologie")

    mois_actuel = datetime.now().month
    annee_actuelle = datetime.now().year
    noms_mois = [
        "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"
    ]
    calendrier = []
    for i in range(12):
        m = (mois_actuel + i - 1) % 12
        a = annee_actuelle + (mois_actuel + i - 1) // 12
        calendrier.append(f"{noms_mois[m].capitalize()} {a}")

    evenements_section = ""
    if evenements_planifies.strip():
        evenements_section = f"\nÉVÉNEMENTS DÉJÀ PLANIFIÉS / CONNUS :\n{evenements_planifies}\n"

    prompt = f"""Tu es le NARRATEUR DE L'ORACLE pour {ENTREPRISE}.
Ta mission : raconter l'histoire des 12 prochains mois de cette entreprise,
comme un documentaire sur le futur, fondé sur les trajectoires actuelles des données.

DONNÉES COMPLÈTES DE L'ENTREPRISE :
{donnees}
{evenements_section}
Date actuelle : {datetime.now().strftime('%d/%m/%Y')}
Les 12 prochains mois : {' → '.join(calendrier)}

Génère une CHRONOLOGIE NARRATIVE en français, mois par mois, avec :

╔══════════════════════════════════════════════════════════════════════╗
║      📖 CHRONIQUE DU FUTUR — {annee_actuelle}-{annee_actuelle+1}                          ║
║         Basée sur les Trajectoires Actuelles                        ║
╚══════════════════════════════════════════════════════════════════════╝

Pour chaque mois ({' | '.join(calendrier)}) :

▶ [Mois Année]
  Situation probable : [2-3 phrases sur l'état de l'entreprise ce mois]
  Événements attendus : [ce qui va probablement arriver]
  Indicateur clé : [une métrique à surveiller ce mois]
  Risque du mois : [la chose la plus susceptible de mal tourner]
  Opportunité du mois : [la chose la plus susceptible de bien marcher]

Marque les POINTS D'INFLEXION avec :
⚡ MOMENT DE VÉRITÉ — [description de ce qui se joue]

Et les DÉCISIONS CRITIQUES avec :
🔴 DÉCISION CRITIQUE — [quelle décision doit être prise et pourquoi]

Après les 12 mois, une section :

╔══════════════════════════════════════════════════════════════╗
║ LES 3 DÉCISIONS QUI DÉFINIRONT L'ANNÉE                       ║
╚══════════════════════════════════════════════════════════════╝
Pour chaque décision critique identifiée :
  - La décision (formulée clairement)
  - Quand elle doit être prise
  - Option A et ses conséquences
  - Option B et ses conséquences
  - Ce que les données suggèrent

Termine par :
╔══════════════════════════════════════════════════════════════╗
║ ÉPILOGUE — DEUX FUTURS POSSIBLES                             ║
╚══════════════════════════════════════════════════════════════╝
Futur A (si les bonnes décisions sont prises) : portrait en 5 lignes
Futur B (si rien ne change) : portrait en 5 lignes

Ton : celui d'un documentariste qui a vu l'avenir dans les données.
Poétique mais rigoureusement ancré dans les chiffres et patterns observés."""

    texte = _streamer(prompt, temperature=0.75)

    chemin = _sauvegarder("chronologie_future", texte)
    print(f"  📖 Chronique du futur sauvegardée → {chemin}\n")
    return texte


# ═══════════════════════════════════════════════════════════════
# AGENT 5 — ALERTE NOIRE (DÉTECTEUR DE CYGNES NOIRS)
# ═══════════════════════════════════════════════════════════════

def agent_alerte_noire(seuil_criticite: int = 5):
    """
    Détecte les cygnes noirs : risques existentiels pour l'entreprise.
    Même à 1% de probabilité. Force la pensée inconfortable.
    Seuil de criticité : score d'impact minimum (1-10) à inclure.
    """
    print(_titre("🖤  ALERTE NOIRE — DÉTECTEUR DE CYGNES NOIRS  🖤"))
    print(f"\n  Plongée dans les zones d'ombre des données...")
    print(f"  Cartographie des risques existentiels (seuil: {seuil_criticite}/10)...\n")
    print("  ⚠  Ce rapport force une pensée inconfortable. C'est son but.")
    print("  ⚠  Certains scénarios ont moins de 1% de probabilité. Ils sont là quand même.\n")

    memoire = charger_memoire()
    donnees = _serialiser_memoire(memoire)
    incrementer_stat("oracle_alerte_noire")

    prompt = f"""Tu es le GARDIEN DES OMBRES pour {ENTREPRISE}.
Ta mission : identifier ce qui pourrait tuer cette entreprise.
Ne te censure pas. Sois impitoyablement honnête.
Le but n'est pas de faire peur — c'est de survivre en sachant ce qu'on risque.

DONNÉES COMPLÈTES DE L'ENTREPRISE :
{donnees}

Date actuelle : {datetime.now().strftime('%d/%m/%Y')}
Seuil de criticité minimum à inclure : {seuil_criticite}/10

N'inclus que les risques avec un impact ≥ {seuil_criticite}/10.
Même si la probabilité est 0.5%, inclus-le si l'impact potentiel est suffisant.

Pour chaque risque existentiel identifié :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🖤 CYGNE NOIR : [Nom du risque — court, percutant, mémorable]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Probabilité    : [X%] sur 12 mois — [justification honnête]
  Impact         : [N/10] — [ce qui se passerait concrètement]
  Vitesse        : [LENTE (mois) / RAPIDE (semaines) / SOUDAINE (jours)]
  Scénario       : [Décris comment ce risque se matérialise — 3-4 étapes]
  Signaux d'alerte : [3-5 indicateurs concrets à surveiller MAINTENANT]
  Plan de survie : [Que faire si ce scénario se déclenche — actions précises]
  Préparation    : [Ce qu'on peut faire aujourd'hui pour réduire ce risque]

Risques OBLIGATOIRES à évaluer (adapte au contexte de l'entreprise) :

🔴 RISQUES CLIENTS
- Départ du client le plus important (concentration du CA)
- Faillite d'un client débiteur
- Client mécontent qui fait une campagne négative

🔴 RISQUES TECHNOLOGIQUES & FOURNISSEURS
- L'API Anthropic/Google Gemini change drastiquement ses tarifs
- EU AI Act interdit certaines pratiques actuelles
- Panne critique du système en pleine mission client

🔴 RISQUES HUMAINS
- Départ d'une personne clé / fondateur
- Burn-out de l'équipe core
- Fraude interne

🔴 RISQUES FINANCIERS
- Trésorerie à zéro (compte les jours de runway)
- Perte simultanée de plusieurs gros clients
- Factures impayées qui s'accumulent

🔴 RISQUES MARCHÉ
- Concurrent majeur qui copie et dumpe les prix
- Changement réglementaire qui invalide le modèle
- Disruption technologique (un modèle IA gratuit fait tout ça)

🔴 RISQUES RÉPUTATIONNELS
- Incident de données / fuite d'informations clients
- Erreur grave d'un agent IA avec conséquences juridiques

Après tous les risques :

╔══════════════════════════════════════════════════════════════╗
║ TABLEAU DE BORD DES RISQUES EXISTENTIELS                     ║
╚══════════════════════════════════════════════════════════════╝
Un tableau récapitulatif : Risque | Probabilité | Impact | Urgence de préparation

╔══════════════════════════════════════════════════════════════╗
║ LE SCÉNARIO DU PIRE — WHAT IF EVERYTHING GOES WRONG         ║
╚══════════════════════════════════════════════════════════════╝
Et si 3 risques se matérialisaient en même temps : lesquels seraient les plus
probables de se combiner ? Raconte ce scénario catastrophe et comment y survivre.

╔══════════════════════════════════════════════════════════════╗
║ LES 5 ACTIONS DE RÉSILIENCE PRIORITAIRES                     ║
╚══════════════════════════════════════════════════════════════╝
Ce que l'entreprise devrait faire dans les 30 prochains jours pour
se blinder contre les risques les plus probables.

Ton : lucide, direct, sans complaisance. Ceci est un outil de survie."""

    texte = _streamer(prompt, temperature=0.6)

    chemin = _sauvegarder("alerte_noire", texte)
    print(f"  🖤 Rapport des risques existentiels sauvegardé → {chemin}\n")
    return texte


# ═══════════════════════════════════════════════════════════════
# MENU
# ═══════════════════════════════════════════════════════════════

def afficher_menu():
    print(_titre("✦  L'ORACLE — INTELLIGENCE PROPHÉTIQUE  ✦", "═"))
    print(f"  Entreprise : {ENTREPRISE}")
    print(f"  Date       : {datetime.now().strftime('%A %d %B %Y à %H:%M')}")
    print(f"  Répertoire : {ORACLE_DIR}/")
    print()
    print(f"  {'─' * (LARGEUR - 4)}")
    print(f"  1 │ 🔮  BRIEFING HEBDOMADAIRE DE L'ORACLE")
    print(f"    │    Prédictions semaine : contacts, retards, projets, conversions")
    print()
    print(f"  2 │ ⚡  DÉTECTEUR DE SIGNAUX FAIBLES")
    print(f"    │    Sismographe business : churn, trésorerie, croissance, ops")
    print()
    print(f"  3 │ 💎  PRÉDICTION D'OPPORTUNITÉS CACHÉES")
    print(f"    │    Upsell, cross-sell, timing, clients dormants à réactiver")
    print()
    print(f"  4 │ 📖  CHRONOLOGIE DU FUTUR — 12 MOIS")
    print(f"    │    Récit narratif mois par mois, points d'inflexion, décisions clés")
    print()
    print(f"  5 │ 🖤  ALERTE NOIRE — DÉTECTEUR DE CYGNES NOIRS")
    print(f"    │    Risques existentiels, scénarios catastrophe, plans de survie")
    print()
    print(f"  0 │    Quitter l'Oracle")
    print(f"  {'─' * (LARGEUR - 4)}")


def menu():
    while True:
        afficher_menu()
        choix = input("\n  Votre choix → ").strip()

        if choix == "0":
            print()
            print("  ✦ L'Oracle referme ses yeux de données.")
            print("  ✦ Les visions s'estompent... mais les signaux demeurent.")
            print()
            break

        elif choix == "1":
            agent_oracle_semaine()

        elif choix == "2":
            agent_detecter_signaux_faibles()

        elif choix == "3":
            agent_prediction_opportunite()

        elif choix == "4":
            print()
            print("  Événements déjà planifiés (optionnel)")
            print("  Décrivez vos événements connus, projets prévus, jalons importants.")
            print("  Laissez vide pour une projection pure des trajectoires actuelles.")
            print()
            lignes = []
            print("  Entrez les événements (ligne vide pour terminer) :")
            while True:
                ligne = input("  > ").strip()
                if not ligne:
                    break
                lignes.append(ligne)
            evenements = "\n".join(lignes)
            agent_chronologie_future(evenements)

        elif choix == "5":
            print()
            print("  Seuil de criticité (impact minimum sur 10 à inclure)")
            print("  Recommandé : 5 (équilibre). Entrez 3 pour voir plus de risques.")
            print("  Entrez 7 pour ne voir que les risques graves.")
            seuil_str = input("  Seuil [défaut: 5] → ").strip()
            if not seuil_str:
                seuil = 5
            else:
                try:
                    seuil = int(seuil_str)
                    seuil = max(1, min(10, seuil))
                except ValueError:
                    print("  Valeur invalide — seuil par défaut : 5")
                    seuil = 5
            agent_alerte_noire(seuil)

        else:
            print("\n  ✦ L'Oracle ne reconnaît pas ce signe. Choisissez entre 0 et 5.\n")


if __name__ == "__main__":
    menu()
