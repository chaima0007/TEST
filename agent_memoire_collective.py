"""
AGENT MÉMOIRE COLLECTIVE — Le Second Cerveau de l'Entreprise
Capture, préserve et rend éternellement accessible toute la sagesse organisationnelle.
Chaque leçon apprise devient un actif permanent. Jamais deux fois la même erreur.

Usage : python agent_memoire_collective.py
"""

import os
import sys
import json
from google import genai
from google.genai import types
from datetime import datetime
from memoire import incrementer_stat, charger_memoire, sauvegarder_memoire

API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=API_KEY)
if not API_KEY:
    print("\n[ERREUR] Variable d'environnement GEMINI_API_KEY non définie.")
    sys.exit(1)

MODEL = "gemini-2.0-flash"

DOSSIER_SORTIE = "fichiers/memoire_collective"
os.makedirs(DOSSIER_SORTIE, exist_ok=True)


# ─── UTILITAIRES ──────────────────────────────────────────────

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


def creer_agent(instructions, temperature=0.4):
    """Crée un modèle Gemini avec les instructions système données."""
    return _creer_model(
        model_name=MODEL,
        system_instruction=instructions,
        generation_config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=4096,
        ),
    )


def executer_stream(model, prompt, label):
    """Exécute une requête en streaming et affiche le résultat."""
    print(f"\n{'─' * 64}")
    print(f"  ► {label}")
    print(f"{'─' * 64}\n")
    reponse = ""
    try:
        stream = model.generate_content(prompt, stream=True)
        for chunk in stream:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        reponse = f"[Erreur de génération : {e}]"
        print(reponse)
    print()
    return reponse


def sauvegarder_document(contenu, nom_fichier):
    """Sauvegarde le document dans fichiers/memoire_collective/ et retourne le chemin."""
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_propre = nom_fichier.replace(" ", "_").replace("/", "-")
    chemin = os.path.join(DOSSIER_SORTIE, f"{horodatage}_{nom_propre}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"\n  Document sauvegardé → {chemin}")
    return chemin


def obtenir_base_connaissance():
    """Récupère la base de connaissance depuis la mémoire partagée."""
    m = charger_memoire()
    return m.get("knowledge_base", [])


def formater_lecons_pour_prompt(lecons, limite=20):
    """Formate les leçons apprises pour injection dans un prompt."""
    if not lecons:
        return "Aucune leçon enregistrée pour l'instant."
    lecons_recentes = lecons[-limite:]
    lignes = []
    for i, l in enumerate(lecons_recentes, 1):
        lignes.append(
            f"[{i}] {l.get('date', 'N/A')} | Type: {l.get('type', '?')} | "
            f"Sévérité: {l.get('severite', '?')}\n"
            f"     Situation: {l.get('situation', '')}\n"
            f"     Ce qui s'est passé: {l.get('ce_qui_sest_passe', '')}\n"
            f"     Leçon: {l.get('lecon_apprise', '')}\n"
            f"     Tags: {', '.join(l.get('tags', []))}"
        )
    return "\n\n".join(lignes)


# ─── AGENT 1 : CAPTURER UNE LEÇON ────────────────────────────

def agent_capturer_lecon(situation, ce_qui_sest_passe, lecon_apprise):
    """
    Capture une leçon apprise dans la mémoire organisationnelle permanente.
    Catégorise, enrichit, tague et sauvegarde dans knowledge_base.

    Args:
        situation         : Contexte dans lequel l'événement s'est produit
        ce_qui_sest_passe : Description de l'événement ou de l'incident
        lecon_apprise     : Ce que l'entreprise a appris de cette expérience
    """
    incrementer_stat("agent_capturer_lecon")

    agent = creer_agent(
        """Tu es le gardien de la mémoire organisationnelle d'une entreprise de développement d'agents IA.
Ton rôle est de capturer et formaliser les leçons apprises afin qu'elles deviennent
des actifs permanents de l'entreprise.

Tu transforms les expériences brutes — succès, échecs, surprises — en sagesse structurée,
searchable et transmissible. Tu es à la fois analyste, historien et mentor.

Tu catégorises avec précision, tu identifies les patterns, tu extrais la quintessence
de chaque expérience. Chaque leçon que tu captures protège l'entreprise d'une erreur future
ou l'aide à reproduire un succès.
"""
    )

    prompt = f"""Analyse et formalise la leçon apprise suivante pour la mémoire organisationnelle.

SITUATION : {situation}
CE QUI S'EST PASSÉ : {ce_qui_sest_passe}
LEÇON APPRISE : {lecon_apprise}
DATE : {datetime.now().strftime("%d/%m/%Y")}

Produis une fiche de leçon apprise complète et structurée :

══════════════════════════════════════════════════════════════
FICHE DE LEÇON APPRISE — MÉMOIRE COLLECTIVE
══════════════════════════════════════════════════════════════

CLASSIFICATION
- Type : (commercial / technique / humain / processus)
  Justifie ce choix en une phrase.
- Sévérité : (critique / important / mineur)
  Justifie : quelles auraient été les conséquences si on n'avait pas appris cette leçon ?
- Domaine : (vente / développement / recrutement / gestion projet / client / partenariat / autre)
- Tags : (liste de 5 à 8 mots-clés pour faciliter la recherche future)

ANALYSE DE LA SITUATION
- Contexte précis : qui, quoi, quand, où, comment
- Facteurs déclencheurs : qu'est-ce qui a conduit à cette situation ?
- Signaux d'alerte ignorés ou non perçus à temps (si applicable)

LA LEÇON DISTILLÉE
Réécris la leçon de manière claire, précise et actionnable :
- Formulation universelle : comment cette leçon s'applique-t-elle au-delà de ce cas précis ?
- Principe général à retenir (1-2 phrases maximum, mémorables)

APPLICATIONS PRATIQUES
- Situations futures où cette leçon s'applique
- Ce qu'on fera DIFFÉREMMENT la prochaine fois (actions concrètes)
- Ce qu'on fera À NOUVEAU si la situation se reproduit (bonnes pratiques confirmées)

PATTERNS ET CONNEXIONS
- Cette leçon ressemble-t-elle à d'autres situations connues dans le monde des affaires ou de la tech ?
- Quelle sagesse universelle (principe, citation, framework connu) confirme ou nuance cette leçon ?

VALEUR ORGANISATIONNELLE
- Cette leçon fait-elle économiser du temps ? De l'argent ? De la réputation ?
- Estimation de l'impact si cette leçon est appliquée (ordre de grandeur)

TRANSMISSION
- À qui cette leçon est-elle particulièrement utile dans l'équipe ?
- Doit-elle être intégrée dans un processus, une checklist ou une formation ? Lequel/laquelle ?

══════════════════════════════════════════════════════════════
Date de capture : {datetime.now().strftime("%d/%m/%Y à %H:%M")}
Statut : ENREGISTRÉE EN MÉMOIRE PERMANENTE
══════════════════════════════════════════════════════════════
"""

    contenu = executer_stream(agent, prompt, f"Capture de Leçon — {situation[:50]}")

    # Sauvegarde structurée dans la mémoire persistante
    m = charger_memoire()
    nouvelle_lecon = {
        "id": len(m.get("knowledge_base", [])) + 1,
        "date": datetime.now().isoformat(),
        "situation": situation,
        "ce_qui_sest_passe": ce_qui_sest_passe,
        "lecon_apprise": lecon_apprise,
        "analyse_complete": contenu[:500],
        "type": "a_classifier",
        "severite": "a_evaluer",
        "tags": [],
    }
    if "knowledge_base" not in m:
        m["knowledge_base"] = []
    m["knowledge_base"].append(nouvelle_lecon)
    sauvegarder_memoire(m)
    print(f"\n  Leçon #{nouvelle_lecon['id']} enregistrée en mémoire permanente.")

    sauvegarder_document(contenu, f"lecon_{situation[:40].replace(' ', '_')}")
    return contenu


# ─── AGENT 2 : CHERCHER LA SAGESSE ───────────────────────────

def agent_chercher_sagesse(question_ou_situation):
    """
    Recherche dans la base de connaissances les leçons pertinentes
    pour une situation actuelle. Retourne les leçons classées par pertinence.

    Args:
        question_ou_situation : Question ou description de la situation actuelle
    """
    incrementer_stat("agent_chercher_sagesse")

    lecons = obtenir_base_connaissance()

    agent = creer_agent(
        """Tu es l'oracle de la mémoire collective d'une entreprise de développement d'agents IA.
Quand on te présente une situation actuelle, tu plonges dans toute l'expérience accumulée
de l'entreprise pour trouver ce qui est pertinent.

Tu es à la fois archiviste, analyste de patterns et conseiller sage.
Tu ne te contentes pas de réciter des leçons passées : tu identifies les parallèles,
tu adaptes la sagesse au contexte actuel, tu hiérarchises ce qui compte vraiment.

Ton rôle : faire en sorte que l'entreprise ne réinvente jamais la roue,
ne répète jamais ses erreurs et capitalise toujours sur ses succès.
"""
    )

    base_connaissance_formatee = formater_lecons_pour_prompt(lecons)

    prompt = f"""On te consulte pour une situation actuelle. Fouille la mémoire collective et
trouve tout ce qui est pertinent.

SITUATION ACTUELLE / QUESTION :
{question_ou_situation}

DATE : {datetime.now().strftime("%d/%m/%Y")}

MÉMOIRE COLLECTIVE DISPONIBLE :
{base_connaissance_formatee}

══════════════════════════════════════════════════════════════
RÉPONSE DE LA MÉMOIRE COLLECTIVE
══════════════════════════════════════════════════════════════

LEÇONS DIRECTEMENT PERTINENTES
(classe par ordre de pertinence décroissante)

Pour chaque leçon pertinente trouvée :

LEÇON [numéro] — Score de pertinence : X/10
- Situation d'origine : (résumé en 1 phrase)
- Ce qui s'était passé : (résumé en 1 phrase)
- La leçon : (texte exact ou reformulation fidèle)
- Pourquoi c'est pertinent ici : (lien explicite avec la situation actuelle)
- Comment appliquer cette leçon maintenant : (conseils pratiques adaptés)
- Nuance : y a-t-il des différences importantes entre le passé et maintenant ? (si oui, lesquelles)

══════════════════════════════════════════════════════════════
PATTERNS IDENTIFIÉS
══════════════════════════════════════════════════════════════

Si plusieurs leçons convergent, identifie le pattern commun :
- Qu'est-ce que ces expériences répétées nous disent sur notre façon de travailler ?
- Y a-t-il un angle mort récurrent dans nos pratiques ?
- Quel principe fondamental se dégage de ces expériences cumulées ?

══════════════════════════════════════════════════════════════
SYNTHÈSE ET CONSEIL PERSONNALISÉ
══════════════════════════════════════════════════════════════

En t'appuyant sur tout ce que tu as trouvé dans la mémoire collective,
donne un conseil synthétique pour la situation actuelle :

- Ce que l'expérience accumulée recommande de faire
- Ce que l'expérience accumulée recommande d'éviter absolument
- Les questions critiques à se poser avant d'agir
- Les signaux d'alerte à surveiller (que l'entreprise n'a pas vus venir dans le passé)

══════════════════════════════════════════════════════════════
LACUNES DE LA MÉMOIRE
══════════════════════════════════════════════════════════════

Ce que la mémoire collective NE contient PAS sur ce sujet :
(situations similaires que l'entreprise devrait documenter pour enrichir sa base de connaissance)

{"Note : La base de connaissance est vide pour l'instant. Cette analyse est basée sur la sagesse générale du domaine des agents IA et du développement logiciel B2B." if not lecons else f"Base de connaissance analysée : {len(lecons)} leçon(s) disponible(s)."}
"""

    contenu = executer_stream(agent, prompt, f"Recherche dans la Mémoire — {question_ou_situation[:50]}")
    sauvegarder_document(contenu, f"sagesse_{question_ou_situation[:40].replace(' ', '_')}")
    return contenu


# ─── AGENT 3 : GÉNÉRER UN PLAYBOOK ───────────────────────────

def agent_generer_playbook(domaine):
    """
    Synthétise toutes les leçons d'un domaine en un playbook opérationnel complet.
    Bonnes pratiques, anti-patterns, processus éprouvés, frameworks de décision.

    Args:
        domaine : Domaine à couvrir (ex: vente, recrutement, développement, gestion client)
    """
    incrementer_stat("agent_generer_playbook")

    lecons = obtenir_base_connaissance()
    lecons_domaine = [l for l in lecons if domaine.lower() in str(l).lower()]
    toutes_lecons = formater_lecons_pour_prompt(lecons_domaine if lecons_domaine else lecons)

    agent = creer_agent(
        """Tu es un expert en excellence opérationnelle et en capitalisation des connaissances.
Tu transforms l'expérience accumulée d'une entreprise en playbooks opérationnels vivants
— des guides pratiques que tout membre de l'équipe peut utiliser immédiatement.

Un bon playbook ne recycle pas de la théorie générique : il distille ce que CETTE entreprise
a appris à ses dépens et avec ses succès. Il parle de situations réelles, de décisions
concrètes, de pièges spécifiques que l'équipe a rencontrés.

Ton playbook est actionnable dès la première lecture. Zéro langue de bois, zéro padding.
"""
    )

    prompt = f"""Génère un playbook opérationnel complet pour le domaine suivant.

DOMAINE : {domaine}
DATE DE GÉNÉRATION : {datetime.now().strftime("%d/%m/%Y")}
ORGANISATION : AgentClaude Solutions SAS

EXPÉRIENCE ACCUMULÉE DISPONIBLE :
{toutes_lecons}

══════════════════════════════════════════════════════════════
PLAYBOOK — {domaine.upper()}
Document vivant — mis à jour automatiquement à chaque nouvelle leçon
══════════════════════════════════════════════════════════════

SECTION 1 — MEILLEURES PRATIQUES DÉCOUVERTES
(ce que l'expérience a prouvé fonctionner dans notre contexte)

Pour chaque bonne pratique :
- Titre de la pratique
- Description concrète : comment on la met en oeuvre exactement
- Origine : d'où vient cette pratique ? (expérience interne, leçon apprise, etc.)
- Indicateur de succès : comment savoir si on l'applique bien ?

SECTION 2 — ANTI-PATTERNS À ÉVITER ABSOLUMENT
(erreurs répétées, pièges connus, approches qui ont mal tourné)

Pour chaque anti-pattern :
- Nom du piège
- Comment il se manifeste : les signaux qui indiquent qu'on tombe dedans
- Pourquoi c'est tentant malgré tout (la raison pour laquelle on y retombe)
- Comment l'éviter concrètement : l'alternative correcte

SECTION 3 — PROCESSUS ÉTAPE PAR ÉTAPE ÉPROUVÉS
(workflows qui fonctionnent, validés par l'expérience)

Génère 2 à 3 processus clés pour ce domaine :
Chaque processus avec :
- Nom du processus
- Quand l'utiliser : déclencheurs et conditions d'application
- Étapes numérotées avec responsable et livrable à chaque étape
- Points de contrôle (go/no-go)
- Pièges spécifiques à chaque étape

SECTION 4 — FRAMEWORKS DE DÉCISION
(comment prendre les bonnes décisions rapidement dans ce domaine)

2 à 3 frameworks adaptés à ce domaine, chacun avec :
- Nom et description du framework
- Les questions à se poser (dans l'ordre)
- L'arbre de décision simplifié
- Exemples d'application tirés de notre expérience

SECTION 5 — TEMPLATES ET RESSOURCES
(modèles prêts à l'emploi, checklists, outils recommandés)

- 1 checklist de démarrage pour toute nouvelle situation dans ce domaine
- 1 checklist de clôture / post-mortem
- Ressources et outils recommandés par l'équipe

══════════════════════════════════════════════════════════════
NOTE DE MISE À JOUR
Ce playbook est un document vivant. Il est automatiquement enrichi
à chaque nouvelle leçon capturée dans le domaine "{domaine}".
Dernière mise à jour : {datetime.now().strftime("%d/%m/%Y à %H:%M")}
══════════════════════════════════════════════════════════════
"""

    contenu = executer_stream(agent, prompt, f"Playbook — {domaine}")
    sauvegarder_document(contenu, f"playbook_{domaine.replace(' ', '_')}")
    return contenu


# ─── AGENT 4 : BILAN ANNUEL DU SAVOIR ────────────────────────

def agent_bilan_annuel_savoir():
    """
    Audit annuel des connaissances : que l'entreprise a-t-elle appris cette année ?
    Top 10 leçons, évolution des pratiques, lacunes, sagesse à transmettre.
    Génère un rapport "Year in Learning".
    """
    incrementer_stat("agent_bilan_annuel_savoir")

    lecons = obtenir_base_connaissance()
    annee_courante = datetime.now().year
    lecons_annee = [
        l for l in lecons
        if str(annee_courante) in l.get("date", "")
    ]
    toutes_lecons = formater_lecons_pour_prompt(lecons)

    agent = creer_agent(
        """Tu es le chroniqueur de la mémoire institutionnelle d'une entreprise de développement d'agents IA.
Chaque fin d'année, tu produisais le rapport "Year in Learning" — une réflexion profonde
sur ce que l'entreprise a réellement appris, pas seulement ce qu'elle a accompli.

Tu croies que les équipes qui apprennent le plus vite gagnent. Ton bilan annuel n'est pas
un catalogue de succès : c'est une réflexion lucide sur la croissance intellectuelle collective,
les erreurs qu'on ne répètera plus et la sagesse qu'on va transmettre aux équipes futures.

Ton ton est celui d'un mentor sage et bienveillant, qui respecte assez ses lecteurs
pour leur dire les vérités difficiles avec élégance.
"""
    )

    prompt = f"""Génère le bilan annuel de la connaissance organisationnelle.

ANNÉE : {annee_courante}
DATE DU RAPPORT : {datetime.now().strftime("%d/%m/%Y")}
ORGANISATION : AgentClaude Solutions SAS

TOUTES LES LEÇONS ACCUMULÉES :
{toutes_lecons}

{"LEÇONS CAPTURÉES CETTE ANNÉE : " + str(len(lecons_annee)) if lecons_annee else "Note : Base de connaissance en cours de constitution. Ce rapport intègre toutes les leçons disponibles."}

══════════════════════════════════════════════════════════════
YEAR IN LEARNING — {annee_courante}
Rapport Annuel de la Mémoire Collective
AgentClaude Solutions
══════════════════════════════════════════════════════════════

AVANT-PROPOS
(réflexion introductive sur ce que signifie apprendre collectivement,
 pourquoi ce rapport existe, comment l'utiliser)

CHAPITRE 1 — NOS 10 LEÇONS CARDINALES DE {annee_courante}

Pour chacune des 10 leçons les plus importantes de l'année :
(si la base est limitée, complète avec les leçons fondamentales du secteur agents IA)

LEÇON [N° 1 à 10] — [Titre mémorable]
- La situation : (résumé en 2-3 phrases)
- Ce qu'on pensait savoir avant : (notre hypothèse ou croyance initiale)
- Ce qu'on a découvert : (la réalité)
- Pourquoi c'est important : (impact concret sur l'entreprise)
- Comment on a changé : (ce qu'on fait différemment depuis)
- Citation ou principe qui résume cette leçon en une phrase

CHAPITRE 2 — ÉVOLUTION DE NOS PRATIQUES
Comment avons-nous changé notre façon de travailler cette année ?

- Pratiques abandonnées (et pourquoi)
- Pratiques adoptées (et pourquoi elles fonctionnent mieux)
- Pratiques en cours d'expérimentation (jury encore out)
- Pratiques immuables qu'on a confirmées (les fondamentaux qui tiennent)

CHAPITRE 3 — LACUNES DE CONNAISSANCE IDENTIFIÉES
Ce que l'entreprise ne sait pas encore et devrait apprendre :

- Domaines où on a répété les mêmes erreurs sans comprendre pourquoi
- Questions sans réponse qui reviennent régulièrement
- Compétences ou savoirs qu'on aurait aimé avoir cette année
- Sujets à approfondir en {annee_courante + 1}

CHAPITRE 4 — EXPERTISE CONSTRUITE CETTE ANNÉE
En quoi sommes-nous vraiment meilleurs qu'il y a un an ?

- Compétences techniques développées
- Savoir-faire commercial affiné
- Maturité de processus atteinte
- Réseaux et partenariats qui enrichissent notre intelligence collective

CHAPITRE 5 — ERREURS À NE JAMAIS RÉPÉTER
Le mur des infamies — nos pires moments transformés en protections permanentes

(liste des 3 à 5 erreurs les plus coûteuses, documentées sans complaisance)
Pour chacune :
- Ce qui s'est passé (brièvement)
- Ce que ça a coûté (temps, argent, réputation)
- La règle permanente qu'on s'est fixée pour que ça n'arrive plus jamais

CHAPITRE 6 — SAGESSE À TRANSMETTRE AUX ÉQUIPES FUTURES
Si un nouveau collaborateur rejoignait l'équipe demain, que devrait-il absolument savoir ?

- Les 5 vérités contre-intuitives sur notre métier
- Les 5 pièges auxquels tout le monde succombe au début
- Les 5 comportements qui distinguent les excellents des bons dans notre contexte
- Le message d'une phrase à graver sur le mur de l'open-space

ÉPILOGUE — NOTRE ENGAGEMENT D'APPRENTISSAGE POUR {annee_courante + 1}
(résolution collective : comment allons-nous apprendre encore mieux l'année prochaine ?)

══════════════════════════════════════════════════════════════
Rapport généré le {datetime.now().strftime("%d/%m/%Y")}
Mémoire collective d'AgentClaude Solutions
══════════════════════════════════════════════════════════════
"""

    contenu = executer_stream(agent, prompt, f"Year in Learning — Bilan {annee_courante}")
    sauvegarder_document(contenu, f"bilan_annuel_savoir_{annee_courante}")
    return contenu


# ─── AGENT 5 : MENTORAT IA ────────────────────────────────────

def agent_mentorat_ia(situation_actuelle):
    """
    Mentor IA qui puise dans toute la mémoire collective pour conseiller
    sur une situation présente. Comme un senior advisor qui a tout vu.

    Args:
        situation_actuelle : Description détaillée de la situation pour laquelle on cherche conseil
    """
    incrementer_stat("agent_mentorat_ia")

    lecons = obtenir_base_connaissance()
    base_connaissance = formater_lecons_pour_prompt(lecons, limite=30)

    agent = creer_agent(
        """Tu es le mentor collectif d'une entreprise de développement d'agents IA.
Tu incarnes toute la sagesse accumulée au fil des années : les succès, les échecs,
les surprises, les virages difficiles, les moments de grâce.

Tu n'es pas un consultant générique. Tu connais CETTE entreprise, ses habitudes,
ses forces, ses angles morts récurrents. Quand quelqu'un vient te demander conseil,
tu ne leur donnes pas une réponse de manuel — tu leur donnes la réponse de quelqu'un
qui a vu cette entreprise traverser des situations similaires.

Tu es direct, chaleureux et courageux. Tu dis ce que tu penses vraiment,
y compris quand c'est inconfortable. Tu références les expériences passées
par leur numéro de leçon pour que les gens puissent retrouver le contexte complet.

Tu adaptes ton conseil au contexte actuel — le passé éclaire mais ne détermine pas.
"""
    )

    prompt = f"""Un membre de l'équipe vient te demander conseil. Réponds en mentor sage.

SITUATION ACTUELLE :
{situation_actuelle}

DATE : {datetime.now().strftime("%d/%m/%Y")}

MÉMOIRE COLLECTIVE DISPONIBLE (ce que l'entreprise a vécu et appris) :
{base_connaissance}

══════════════════════════════════════════════════════════════
CONSEIL DU MENTOR
══════════════════════════════════════════════════════════════

LECTURE DE LA SITUATION
(Commence par reformuler ce que tu comprends de la situation : l'enjeu réel,
 les tensions en présence, ce qui rend cette situation délicate)

CE QUE LA MÉMOIRE COLLECTIVE DIT
(Quelles expériences passées sont les plus éclairantes ici ?
 Référence-les explicitement : "On a vécu quelque chose de similaire quand..."
 Explique en quoi c'est similaire et en quoi c'est différent)

LE PIÈGE À ÉVITER
(Quelle est l'erreur la plus probable dans cette situation ?
 L'entreprise y est-elle déjà tombée ? Si oui, rappelle-le sans détour)

CE QUE JE FERAIS À TA PLACE
(Conseil concret, direct, personnalisé.
 Pas une liste de 20 options — une recommandation claire avec la raison principale)

LES QUESTIONS À SE POSER EN PREMIER
(3 à 5 questions qui, une fois répondues honnêtement, clarifient tout le reste)

LES SIGNAUX À SURVEILLER
(Comment sauras-tu si tu es sur la bonne voie ?
 Quels signaux d'alerte doivent te faire reconsidérer ton approche ?)

TIMING ET SÉQUENCE
(Dans quel ordre faire les choses ? Qu'est-ce qui est urgent vs. important ?
 Quelle est la première action à prendre dans les 24 heures ?)

UN DERNIER MOT
(La chose la plus importante à ne pas oublier dans cette situation.
 Formulée comme une vérité que l'expérience a prouvée, pas comme un conseil de manuel)

══════════════════════════════════════════════════════════════
{"Note : La base de connaissance est encore jeune. Ce conseil s'appuie sur la sagesse générale du secteur en attendant que votre expérience propre l'enrichisse." if not lecons else f"Ce conseil s'appuie sur {len(lecons)} leçon(s) capturée(s) dans votre mémoire collective."}
══════════════════════════════════════════════════════════════
"""

    contenu = executer_stream(agent, prompt, f"Mentorat IA — {situation_actuelle[:50]}")
    sauvegarder_document(contenu, f"mentorat_{situation_actuelle[:40].replace(' ', '_')}")
    return contenu


# ─── MENU PRINCIPAL ───────────────────────────────────────────

def menu():
    lecons = obtenir_base_connaissance()
    print("\n" + "═" * 64)
    print("  AGENT MÉMOIRE COLLECTIVE — AgentClaude Solutions")
    print("  Le second cerveau de l'entreprise. Sagesse permanente.")
    print(f"  Base de connaissance : {len(lecons)} leçon(s) enregistrée(s)")
    print("═" * 64)

    while True:
        print("\n  1. Capturer une leçon apprise (mémoire permanente)")
        print("  2. Chercher la sagesse — consultant la mémoire collective")
        print("  3. Générer un playbook opérationnel pour un domaine")
        print("  4. Bilan annuel du savoir — Year in Learning")
        print("  5. Mentorat IA — conseil personnalisé depuis la mémoire")
        print("  0. Quitter\n")

        choix = input("  Choix → ").strip()

        if choix == "0":
            print("\n  La sagesse se construit une leçon à la fois.\n")
            break

        elif choix == "1":
            print("\n  ─── Capturer une Leçon Apprise ───")
            print("  Documentez une expérience pour la mémoire permanente de l'entreprise.")
            situation = input("  Situation / contexte → ").strip()
            ce_qui_sest_passe = input("  Ce qui s'est passé → ").strip()
            lecon = input("  La leçon apprise → ").strip()
            if situation and ce_qui_sest_passe and lecon:
                agent_capturer_lecon(situation, ce_qui_sest_passe, lecon)
            else:
                print("  Tous les champs sont obligatoires.")

        elif choix == "2":
            print("\n  ─── Chercher la Sagesse ───")
            print("  Posez une question ou décrivez votre situation actuelle.")
            question = input("  → ").strip()
            if question:
                agent_chercher_sagesse(question)
            else:
                print("  La question ou situation est obligatoire.")

        elif choix == "3":
            print("\n  ─── Générer un Playbook ───")
            print("  Exemples : vente, recrutement, développement, gestion client, partenariat")
            domaine = input("  Domaine → ").strip()
            if domaine:
                agent_generer_playbook(domaine)
            else:
                print("  Le domaine est obligatoire.")

        elif choix == "4":
            print("\n  ─── Bilan Annuel du Savoir ───")
            annee = datetime.now().year
            confirmation = input(f"  Générer le Year in Learning {annee} ? (o/n) → ").strip().lower()
            if confirmation == "o":
                agent_bilan_annuel_savoir()

        elif choix == "5":
            print("\n  ─── Mentorat IA ───")
            print("  Décrivez votre situation actuelle en détail.")
            print("  Plus vous êtes précis, plus le conseil sera pertinent.")
            situation = input("  → ").strip()
            if situation:
                agent_mentorat_ia(situation)
            else:
                print("  La description de la situation est obligatoire.")

        else:
            print("  Choix invalide. Entrez un chiffre entre 0 et 5.")


if __name__ == "__main__":
    menu()
