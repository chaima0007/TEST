"""
ADAPTATION CONTINUE — Système d'apprentissage et d'auto-correction organisationnelle
L'entreprise qui survit est celle qui s'adapte le plus vite.
Ce module transforme chaque expérience en apprentissage et chaque changement en opportunité.
"""

import os
import datetime
import google.generativeai as genai
from memoire import charger_memoire, sauvegarder_memoire, incrementer_stat

MODEL = "gemini-2.0-flash"

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(MODEL)

ENTREPRISE = "AgentClaude Solutions"
DOMAINE = "solutions d'agents IA autonomes"


# ─────────────────────────────────────────────
# Utilitaires
# ─────────────────────────────────────────────

def streamer(prompt: str) -> str:
    """Envoie le prompt au modèle en streaming et retourne le texte complet."""
    response = model.generate_content(prompt, stream=True)
    texte_complet = ""
    for chunk in response:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            texte_complet += chunk.text
    print()
    return texte_complet


def sauvegarder(nom_fichier: str, contenu: str) -> str:
    """Sauvegarde le rapport dans fichiers/adaptation/ avec horodatage."""
    dossier = "/home/user/TEST/fichiers/adaptation"
    os.makedirs(dossier, exist_ok=True)
    horodatage = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = f"{dossier}/{nom_fichier}_{horodatage}.txt"
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


# ─────────────────────────────────────────────
# Agent 1 – Retour d'Expérience
# ─────────────────────────────────────────────

def agent_retour_experience(evenement: str, ce_qui_sest_passe: str, impact: str, duree: str) -> str:
    """
    Après tout événement significatif (victoire, perte, problème, surprise) :
    génère un débrief structuré en 5 minutes. Transforme chaque expérience en
    apprentissage organisationnel et sauvegarde en mémoire.
    """
    incrementer_stat("agent_retour_experience")

    prompt = f"""Tu es le facilitateur du retour d'expérience de {ENTREPRISE}.
Ton rôle : transformer chaque événement vécu en intelligence organisationnelle durable.
Une entreprise apprenante n'accumule pas des erreurs — elle les convertit en avantages compétitifs.

ÉVÉNEMENT ANALYSÉ
─────────────────
Type d'événement  : {evenement}
Ce qui s'est passé : {ce_qui_sest_passe}
Impact mesuré     : {impact}
Durée / période   : {duree}

═══════════════════════════════════════════════════════
I. RECONSTITUTION FACTUELLE — QUE S'EST-IL PASSÉ EXACTEMENT ?
═══════════════════════════════════════════════════════
Reconstitue la chronologie précise :
• La séquence des faits (sans interprétation, sans jugement)
• Les acteurs impliqués et leurs rôles dans l'événement
• Le contexte ambiant (marché, équipe, charge, timing)
• Ce qui a déclenché l'événement (le moment exact où la trajectoire a basculé)
• Ce qu'on savait vs ce qu'on ne savait pas au moment où ça s'est passé

═══════════════════════════════════════════════════════
II. ANALYSE DES CAUSES RACINES — MÉTHODE DES 5 POURQUOI
═══════════════════════════════════════════════════════
Applique la méthode des 5 Pourquoi au problème central ou à la réussite centrale.

POURQUOI 1 : Pourquoi est-ce que {evenement} s'est produit ?
→ Réponse 1 : ...

POURQUOI 2 : Pourquoi [réponse 1] s'est-il/elle produit(e) ?
→ Réponse 2 : ...

POURQUOI 3 : Pourquoi [réponse 2] s'est-il/elle produit(e) ?
→ Réponse 3 : ...

POURQUOI 4 : Pourquoi [réponse 3] s'est-il/elle produit(e) ?
→ Réponse 4 : ...

POURQUOI 5 : Pourquoi [réponse 4] s'est-il/elle produit(e) ?
→ CAUSE RACINE PROFONDE : ...

Distingue ensuite :
• Cause immédiate (ce qui a déclenché)
• Cause systémique (ce qui a créé la condition)
• Cause structurelle (ce qui aurait dû être différent dès le départ)

═══════════════════════════════════════════════════════
III. CE QU'ON AURAIT FAIT DIFFÉREMMENT
═══════════════════════════════════════════════════════
Sois honnête et courageux. Pas d'autoflagellation, pas d'excuse — juste la vérité opérationnelle.

• Décision A qu'on n'aurait pas prise (et pourquoi on l'a prise quand même)
• Signal B qu'on aurait dû voir (et pourquoi on l'a ignoré ou manqué)
• Action C qu'on aurait lancée plus tôt (avec quel impact estimé)
• Ce qu'on aurait priorisé différemment (ressources, temps, attention)
• La conversation difficile qu'on aurait eue 3 semaines plus tôt

═══════════════════════════════════════════════════════
IV. CHANGEMENT IMMÉDIAT À IMPLÉMENTER — DANS LES 7 PROCHAINS JOURS
═══════════════════════════════════════════════════════
Un seul changement. Le plus impactant. Celui qui modifie réellement le comportement systémique.

CHANGEMENT : [Titre clair et mémorable]
→ Qui fait quoi, exactement, et d'ici quand ?
→ Quel processus ou habitude cela remplace-t-il ?
→ Comment on sait que ça fonctionne ? (indicateur de succès en 30 jours)
→ Qui est responsable de l'implémenter et de le tenir ?
→ Quel risque si on ne le fait pas ?

═══════════════════════════════════════════════════════
V. INTELLIGENCE À PARTAGER AVEC L'ÉQUIPE
═══════════════════════════════════════════════════════
Rédige un message synthétique à partager en réunion d'équipe ou en Slack.
Format : bref (< 200 mots), factuel, sans honte ni autoflagellation.
Ton : adulte à adulte, pas de dramatisation, pas de minimisation.

Structure du message :
"Ce qui s'est passé" (2 phrases)
"Ce qu'on a appris" (2-3 bullet points)
"Ce qu'on change" (1 action claire)
"Ce qu'on a bien fait" (parce que même dans l'échec, il y a des réussites à reconnaître)

═══════════════════════════════════════════════════════
VI. ENRICHISSEMENT DE LA BASE DE CONNAISSANCE
═══════════════════════════════════════════════════════
Génère une fiche de connaissance réutilisable :

TITRE DE LA FICHE : [court, searchable, mémorable]
CATÉGORIE : [commercial / opérationnel / technique / humain / stratégique]
SITUATION TYPE : Quand réactiver cette connaissance ? ("Chaque fois que...")
RÈGLE OU PRINCIPE APPRIS : (1 phrase, applicable directement)
INDICATEURS D'ALERTE : 3 signaux qui indiquent qu'on est dans une situation similaire
ACTIONS RECOMMANDÉES : 3 actions préventives ou correctrices
SCORE DE CRITICITÉ : [faible / moyen / élevé / critique]

═══════════════════════════════════════════════════════
SYNTHÈSE FINALE
═══════════════════════════════════════════════════════
En 3 phrases : la leçon la plus importante de cet événement, formulée de façon à ce qu'un nouveau membre de l'équipe comprenne immédiatement ce qu'il doit retenir.

Termine par : "Si cet événement se reproduisait demain, on réagirait différemment en faisant ___."

Ton : agile, sans complaisance, orienté apprentissage. L'erreur n'est pas un échec — c'est du carburant."""

    print("\n" + "═" * 60)
    print("  RETOUR D'EXPÉRIENCE EN COURS...")
    print(f"  Événement : {evenement}")
    print("  Méthode : 5 Pourquoi + débrief structuré")
    print("═" * 60 + "\n")

    contenu = streamer(prompt)
    chemin = sauvegarder("retour_experience", contenu)
    print(f"\n  Rapport sauvegardé : {chemin}")

    # Sauvegarde en mémoire knowledge_base
    memoire = charger_memoire()
    fiche = {
        "date": datetime.datetime.now().isoformat(),
        "type": "retour_experience",
        "evenement": evenement,
        "impact": impact,
        "resume": contenu[:500],
        "fichier": chemin,
    }
    memoire["knowledge_base"].append(fiche)
    sauvegarder_memoire(memoire)
    print("  Connaissance sauvegardée en mémoire organisationnelle.")

    return contenu


# ─────────────────────────────────────────────
# Agent 2 – Adaptation de l'Offre
# ─────────────────────────────────────────────

def agent_adapter_offre(feedback_marche: str, tendances_observees: str) -> str:
    """
    Adapte l'offre produit/service en fonction des signaux marché :
    analyse les retours clients, les deals perdus, les mouvements concurrents
    et génère une offre mise à jour avec communication aux clients existants.
    """
    incrementer_stat("agent_adapter_offre")

    prompt = f"""Tu es le directeur produit et stratégie de {ENTREPRISE}.
Ta mission : garder l'offre toujours alignée avec ce que le marché veut vraiment.
Une offre figée est une offre mourante. L'adaptation n'est pas un signe de faiblesse — c'est un système immunitaire.

SIGNAUX REÇUS DU MARCHÉ
────────────────────────
Feedback marché    : {feedback_marche}
Tendances observées : {tendances_observees}
Domaine            : {DOMAINE}

═══════════════════════════════════════════════════════
I. ANALYSE DES SIGNAUX — CE QUE LE MARCHÉ DIT VRAIMENT
═══════════════════════════════════════════════════════
Décode les signaux bruts reçus :

SIGNAUX EXPLICITES (ce que les clients demandent directement)
→ Liste des demandes formulées clairement avec leur fréquence et leur urgence estimée

SIGNAUX IMPLICITES (ce que le marché exprime sans le dire)
→ Quels comportements d'achat ont changé ?
→ Quelles objections reviennent le plus souvent lors des ventes ?
→ Quels deals a-t-on perdus, et pour quelle raison réelle ?

SIGNAUX CONTEXTUELS (mouvements concurrents, techno, réglementation)
→ Qu'est-ce que les concurrents font que nous ne faisons pas ?
→ Quelles nouvelles technologies créent de nouvelles attentes ?
→ Quel changement réglementaire ou sociétal modifie les priorités des clients ?

OPPORTUNITÉ CACHÉE (ce que personne ne demande encore mais qui va émerger)
→ Quel besoin non articulé est en train de naître dans ce marché ?

═══════════════════════════════════════════════════════
II. CE QU'ON AJOUTE À L'OFFRE — NOUVELLES CAPACITÉS
═══════════════════════════════════════════════════════
Pour chaque ajout, justifier le signal marché qui l'exige :

AJOUT 1 — [Nom de la nouvelle offre / fonctionnalité]
→ Signal qui justifie cet ajout
→ Description en langage client (pas interne, pas technique)
→ Valeur perçue par le client : qu'est-ce qu'il gagne concrètement ?
→ Effort d'implémentation estimé : rapide (< 2 semaines) / moyen (1-2 mois) / lourd (> 3 mois)
→ Priorité : critique / haute / moyenne

AJOUT 2 — [Nom]
→ (même structure)

AJOUT 3 — [Nom]
→ (même structure)

═══════════════════════════════════════════════════════
III. CE QU'ON RETIRE DE L'OFFRE — ÉLAGAGE COURAGEUX
═══════════════════════════════════════════════════════
Ce qui n'est plus adapté, trop cher à maintenir, ou qui dilue le focus :

RETRAIT 1 — [Offre / fonctionnalité à supprimer]
→ Pourquoi le retirer maintenant ? (données, feedback, coût d'opportunité)
→ Combien de clients actuels sont impactés ?
→ Comment les accompagner vers une alternative ?
→ Économie réalisée (temps, argent, focus équipe)

RETRAIT 2 — [Nom]
→ (même structure)

═══════════════════════════════════════════════════════
IV. CE QU'ON TRANSFORME — ÉVOLUTIONS DE L'OFFRE EXISTANTE
═══════════════════════════════════════════════════════
Ce qui reste mais doit changer de forme, de prix ou de positionnement :

TRANSFORMATION 1 — [Offre existante à faire évoluer]
→ Avant : comment elle était décrite / vendue / tarifée
→ Après : nouvelle description, nouveau positionnement, nouvelle valeur perçue
→ Raison du changement : ce que le marché valorise différemment aujourd'hui

TRANSFORMATION 2 — [Nom]
→ (même structure)

═══════════════════════════════════════════════════════
V. DESCRIPTIONS DE SERVICES MISES À JOUR
═══════════════════════════════════════════════════════
Rédige 3 nouvelles descriptions de services (format commercial, orienté bénéfices client) :

SERVICE A — [Nom]
Accroche (1 phrase) : ...
Description (3-4 phrases) : ...
Bénéfices clés (3 bullet points) : ...
Pour qui : ...
Résultat concret attendu : ...

SERVICE B — [Nom]
(même structure)

SERVICE C — [Nom]
(même structure)

═══════════════════════════════════════════════════════
VI. JUSTIFICATION DES NOUVELLES TARIFICATIONS
═══════════════════════════════════════════════════════
Pour chaque évolution tarifaire :
• L'ancienne tarification et sa logique
• La nouvelle tarification proposée
• La valeur créée qui justifie l'évolution (en termes client, pas en termes de coût interne)
• Comment communiquer le changement sans perdre la confiance

═══════════════════════════════════════════════════════
VII. COMMUNICATION AUX CLIENTS EXISTANTS
═══════════════════════════════════════════════════════
Rédige un email à envoyer aux clients actuels pour annoncer les évolutions de l'offre.

Objet de l'email : ...

Corps :
- Ce qui change (positif, orienté bénéfices)
- Ce qui reste (continuité et stabilité)
- Ce qui disparaît (honnêteté + alternatives)
- Prochaines étapes (appel, démo, FAQ)

Ton : partenaire de croissance, pas commercial. On grandit ensemble.

═══════════════════════════════════════════════════════
VERDICT FINAL
═══════════════════════════════════════════════════════
"L'évolution la plus importante de notre offre dans les 30 prochains jours est _____, parce que _____.
Si on ne la fait pas, _____."

Ton : agile, centré client, sans attachement sentimental à ce qui ne fonctionne plus."""

    print("\n" + "═" * 60)
    print("  ADAPTATION DE L'OFFRE EN COURS...")
    print("  Analyse signaux marché → évolution produit/service")
    print("═" * 60 + "\n")

    contenu = streamer(prompt)
    chemin = sauvegarder("adapter_offre", contenu)
    print(f"\n  Rapport sauvegardé : {chemin}")
    return contenu


# ─────────────────────────────────────────────
# Agent 3 – Calibrage des Agents
# ─────────────────────────────────────────────

def agent_calibrer_agents() -> str:
    """
    Méta-agent : analyse les stats d'utilisation des agents depuis la mémoire,
    évalue leur performance, identifie les manques, et génère des recommandations
    pour faire évoluer le système IA lui-même.
    """
    incrementer_stat("agent_calibrer_agents")

    # Lecture des stats d'utilisation depuis la mémoire
    memoire = charger_memoire()
    stats_agents = memoire.get("stats", {}).get("agents_utilises", {})
    total_demandes = memoire.get("stats", {}).get("total_demandes", 0)
    nb_clients = len(memoire.get("clients", {}))
    nb_interactions = len(memoire.get("interactions", []))
    nb_knowledge = len(memoire.get("knowledge_base", []))

    # Formatage des stats pour le prompt
    if stats_agents:
        stats_formatees = "\n".join(
            [f"  • {agent} : {count} utilisation(s)" for agent, count in sorted(stats_agents.items(), key=lambda x: -x[1])]
        )
    else:
        stats_formatees = "  Aucune statistique disponible — système IA en démarrage."

    prompt = f"""Tu es le meta-architecte du système IA de {ENTREPRISE}.
Ton rôle : regarder le système d'agents en face et décider comment il doit évoluer.
Un système IA qui ne s'auto-améliore pas est un système qui régresse.

DONNÉES D'UTILISATION DU SYSTÈME IA
─────────────────────────────────────
Total de demandes traitées : {total_demandes}
Nombre de clients en mémoire : {nb_clients}
Nombre d'interactions enregistrées : {nb_interactions}
Connaissances en base : {nb_knowledge}

Utilisation par agent :
{stats_formatees}

Agents disponibles dans le système :
  • agent_retour_experience      — Débrief structuré après événements significatifs
  • agent_adapter_offre          — Adaptation produit/service selon signaux marché
  • agent_calibrer_agents        — Méta-analyse du système IA lui-même (celui-ci)
  • agent_feedback_360           — Traitement de feedback multi-sources
  • agent_plan_adaptation        — Plan de transition face à un changement externe
  • agent_commercial             — Prospection et vente
  • agent_chef_projet            — Gestion de projet et coordination
  • agent_comptable              — Finances et comptabilité
  • agent_innovation             — Brainstorming et futures stratégiques
  • agent_juridique              — Analyse légale et conformité
  • agent_kpi                    — Suivi des indicateurs de performance
  • agent_pricing                — Stratégie tarifaire
  • agent_reputation             — Gestion de réputation et e-réputation
  • agent_rh / agent_recrutement — Ressources humaines
  • agent_data                   — Analyse de données
  • agent_formation_equipe       — Formation interne
  • agent_partenariats           — Développement de partenariats
  • agent_veille_techno          — Veille technologique
  • agent_oracle                 — Simulateur de décisions et Monte Carlo

═══════════════════════════════════════════════════════
I. RAPPORT DE PERFORMANCE DU SYSTÈME
═══════════════════════════════════════════════════════
Analyse l'utilisation actuelle :

AGENTS PERFORMANTS (très utilisés → valeur prouvée)
→ Quels agents sont sur-utilisés ? Pourquoi ? Que dit ça des besoins réels de l'entreprise ?

AGENTS SOUS-UTILISÉS (peu ou pas utilisés → problème de valeur ou de visibilité)
→ Pour chaque agent sous-utilisé, diagnostique : mauvais positionnement ? Cas d'usage flou ? Prompt inefficace ? Besoin inexistant ?

DÉSÉQUILIBRES RÉVÉLATEURS
→ Que révèle ce profil d'utilisation sur la maturité de l'entreprise ?
→ Quelles fonctions sont sur-automatisées vs sous-automatisées ?

═══════════════════════════════════════════════════════
II. RECOMMANDATIONS D'AMÉLIORATION DES AGENTS EXISTANTS
═══════════════════════════════════════════════════════
Pour les 5 agents les plus utilisés, propose des améliorations concrètes :

AGENT [NOM] — Amélioration recommandée
→ Problème actuel probable (basé sur l'utilisation et le contexte)
→ Amélioration du prompt : que faudrait-il ajouter / modifier / retirer ?
→ Nouvelle capacité à ajouter
→ Cas d'usage à mieux couvrir

(Répété pour 5 agents)

═══════════════════════════════════════════════════════
III. NOUVEAUX AGENTS À CRÉER
═══════════════════════════════════════════════════════
Identifie 3 agents manquants que l'entreprise devrait construire en priorité.

AGENT MANQUANT 1 — [Nom suggéré]
→ Besoin qu'il couvre (gap identifié)
→ Fonctions principales (3-4 bullet points)
→ Fréquence d'utilisation estimée
→ Impact métier attendu
→ Complexité de développement : simple / moyen / complexe
→ Priorité de création : urgent / important / nice-to-have

AGENT MANQUANT 2 — [Nom]
(même structure)

AGENT MANQUANT 3 — [Nom]
(même structure)

═══════════════════════════════════════════════════════
IV. AGENTS À METTRE EN RETRAITE
═══════════════════════════════════════════════════════
Y a-t-il des agents à supprimer, fusionner ou simplifier ?
Argumente : un agent inutilisé est-il un agent inutile, ou un agent mal positionné ?
Pour chaque recommandation de retrait/fusion : justification + plan de transition.

═══════════════════════════════════════════════════════
V. AMÉLIORATIONS DE L'ORCHESTRATION
═══════════════════════════════════════════════════════
Comment mieux faire travailler les agents ensemble ?

• Quels agents devraient être déclenchés en chaîne automatiquement ?
  Ex : "Après agent_commercial → déclencher agent_chef_projet"
  Ex : "Après agent_retour_experience → notifier agent_kpi"

• Quels flux de travail automatisés manquent ?
  (3 workflows à construire, avec leur logique de déclenchement)

• Comment améliorer le menu principal pour rendre le système plus intuitif ?

• Quelle donnée de la mémoire est sous-exploitée ? Comment mieux l'utiliser ?

═══════════════════════════════════════════════════════
VI. ROADMAP D'ÉVOLUTION DU SYSTÈME IA
═══════════════════════════════════════════════════════
Génère un plan sur 90 jours :

SEMAINE 1-2 : [Actions rapides, améliorations de prompts]
SEMAINE 3-4 : [Premiers nouveaux agents]
MOIS 2 : [Agents complexes + orchestration]
MOIS 3 : [Revue complète + nouvelles fonctionnalités]

Critère de succès global : "Dans 90 jours, le système IA sera meilleur si ___."

═══════════════════════════════════════════════════════
VERDICT META
═══════════════════════════════════════════════════════
"Le changement le plus important à faire sur ce système IA cette semaine est _____.
Si on ne l'améliore pas, dans 6 mois _____."

Ton : lucide, systémique, sans complaisance envers le système existant."""

    print("\n" + "═" * 60)
    print("  CALIBRAGE DU SYSTÈME IA EN COURS...")
    print("  Analyse de performance + roadmap d'évolution")
    print("═" * 60 + "\n")

    contenu = streamer(prompt)
    chemin = sauvegarder("calibrer_agents", contenu)
    print(f"\n  Rapport sauvegardé : {chemin}")
    return contenu


# ─────────────────────────────────────────────
# Agent 4 – Feedback 360°
# ─────────────────────────────────────────────

def agent_feedback_360(source: str, feedback_brut: str) -> str:
    """
    Traite un feedback de n'importe quelle source (client, équipe, partenaire,
    concurrent, marché) et le convertit en intelligence structurée et en
    plan d'action dans les 24 heures.
    """
    incrementer_stat("agent_feedback_360")

    prompt = f"""Tu es le directeur de l'intelligence organisationnelle de {ENTREPRISE}.
Ta mission : ne jamais laisser un feedback se perdre. Chaque retour, même blessant, même flatteur, même ambigu, contient de la valeur. Ton travail est de l'extraire.

FEEDBACK REÇU
──────────────
Source du feedback : {source}
Feedback brut      : {feedback_brut}
Entreprise         : {ENTREPRISE} | {DOMAINE}

═══════════════════════════════════════════════════════
I. ANALYSE DU SOUS-TEXTE — CE QU'ILS VEULENT VRAIMENT DIRE
═══════════════════════════════════════════════════════
Le feedback exprimé est rarement le feedback réel. Décrypte les couches :

NIVEAU 1 — CE QUI EST DIT (la surface)
→ Résumé factuel du feedback en 2-3 phrases

NIVEAU 2 — CE QUI EST RESSENTI (l'émotion sous-jacente)
→ Quelle est l'émotion dominante de ce feedback ? (frustration, enthousiasme, méfiance, déception, surprise, soulagement ?)
→ D'où vient cette émotion ? Qu'est-ce qui l'a provoquée vraiment ?

NIVEAU 3 — CE QUI EST VOULU (le besoin profond)
→ Qu'est-ce que cette personne / source cherche vraiment ?
→ Quel est le job-to-be-done derrière cette remarque ?

NIVEAU 4 — CE QUI N'EST PAS DIT (le non-formulé dangereux ou précieux)
→ Qu'est-ce qui n'a pas été dit mais transparaît entre les lignes ?
→ Y a-t-il une menace implicite ? Une opportunité cachée ?
→ Ce feedback est-il représentatif d'une tendance plus large ?

NIVEAU 5 — CE QUE ÇA RÉVÈLE SUR NOUS (l'intelligence sur soi)
→ Qu'est-ce que ce feedback révèle sur nos forces et nos angles morts en tant qu'entreprise ?

═══════════════════════════════════════════════════════
II. CE QU'ON CHANGE — PLAN D'ACTION PRIORISÉ
═══════════════════════════════════════════════════════
Transforme ce feedback en décisions concrètes :

ACTION IMMÉDIATE (dans les 24h)
→ Qui fait quoi, exactement, pour répondre à ce feedback ?
→ Ce n'est pas une communication — c'est une action réelle.

ACTION À COURT TERME (dans les 2 semaines)
→ Quel processus / produit / comportement modifie-t-on ?
→ Qui est responsable, avec quelle deadline ?

ACTION STRUCTURELLE (dans les 60 jours)
→ Quel changement profond ce feedback appelle-t-il ?
→ Impact estimé sur : client / équipe / offre / positionnement

CE QU'ON NE CHANGE PAS — ET POURQUOI
→ Certains feedbacks ne doivent pas changer notre trajectoire.
→ Quels aspects de ce feedback allons-nous ignorer délibérément ?
→ Justification (pas de la défensive — de la lucidité stratégique)

═══════════════════════════════════════════════════════
III. CE QU'ON RENFORCE — LES SIGNAUX POSITIFS À AMPLIFIER
═══════════════════════════════════════════════════════
Même dans un feedback négatif, il y a des éléments positifs.

• Qu'est-ce que ce feedback valide dans notre approche actuelle ?
• Quelle force ou différenciation ce feedback met-il en lumière ?
• Comment amplifier ces éléments positifs dans notre communication et nos processus ?

═══════════════════════════════════════════════════════
IV. QUI DOIT LE SAVOIR — DISTRIBUTION DE L'INTELLIGENCE
═══════════════════════════════════════════════════════
Ce feedback est une information stratégique. Qui en a besoin ?

ÉQUIPE COMMERCIALE → Ce qu'ils doivent savoir et comment l'utiliser en vente
ÉQUIPE PRODUIT / OPÉRATIONS → Ce qui impacte la façon dont on délivre
DIRECTION → Ce qui relève de décisions stratégiques
CLIENT / SOURCE → Ce qu'on leur dit en retour (ou pas)
MÉMOIRE ORGANISATIONNELLE → Ce qu'on archive pour éviter de revivre ça

═══════════════════════════════════════════════════════
V. RÉPONSE ET ACTIONS DANS LES 24 HEURES
═══════════════════════════════════════════════════════
Rédige la réponse à envoyer à la source du feedback dans les 24 heures.

TYPE DE RÉPONSE RECOMMANDÉ : [email / appel téléphonique / message Slack / réunion]

Réponse :
[Rédige la réponse complète, prête à utiliser]

Principes de cette réponse :
• Accusé de réception humain (pas un template corporate)
• Démonstration qu'on a vraiment compris (pas un "merci pour votre retour")
• Ce qu'on va concrètement changer (ou pourquoi on ne change pas)
• La prochaine étape claire

═══════════════════════════════════════════════════════
SCORING DU FEEDBACK
═══════════════════════════════════════════════════════
• Urgence : [1-10] — Combien de temps peut-on attendre avant d'agir ?
• Impact potentiel : [1-10] — Quel est l'enjeu si on l'ignore ?
• Représentativité : [1-10] — Est-ce un cas isolé ou une tendance ?
• Faisabilité d'action : [1-10] — Peut-on vraiment changer ce qui est demandé ?

Score global de priorité : [calcul et interprétation]

═══════════════════════════════════════════════════════
VERDICT
═══════════════════════════════════════════════════════
"Ce feedback de {source} est un cadeau parce que _____.
La chose la plus importante à faire dans les prochaines 24 heures est _____."

Ton : ancré, empathique, orienté action. Rien ne se perd, tout se transforme."""

    print("\n" + "═" * 60)
    print("  FEEDBACK 360° EN COURS DE TRAITEMENT...")
    print(f"  Source : {source}")
    print("  Décodage subtext + plan d'action 24h")
    print("═" * 60 + "\n")

    contenu = streamer(prompt)
    chemin = sauvegarder("feedback_360", contenu)
    print(f"\n  Rapport sauvegardé : {chemin}")

    # Enregistrement en mémoire
    memoire = charger_memoire()
    fiche = {
        "date": datetime.datetime.now().isoformat(),
        "type": "feedback_360",
        "source": source,
        "feedback_resume": feedback_brut[:300],
        "fichier": chemin,
    }
    memoire["knowledge_base"].append(fiche)
    sauvegarder_memoire(memoire)
    print("  Feedback enregistré en mémoire organisationnelle.")

    return contenu


# ─────────────────────────────────────────────
# Agent 5 – Plan d'Adaptation
# ─────────────────────────────────────────────

def agent_plan_adaptation(changement_externe: str) -> str:
    """
    Quand quelque chose change (marché, tech, réglementation, équipe, financement) :
    génère un plan d'adaptation complet — évaluation d'impact, ce qui s'arrête,
    ce qui change, ce qui accélère, roadmap 30 jours, critères de succès.
    Comme un système immunitaire pour l'entreprise.
    """
    incrementer_stat("agent_plan_adaptation")

    prompt = f"""Tu es le directeur de la résilience organisationnelle de {ENTREPRISE}.
Ta mission : quand l'environnement change, l'entreprise s'adapte plus vite que la menace ne s'installe.
La survie ne récompense pas les plus forts — elle récompense les plus rapides à s'adapter.

CHANGEMENT EXTERNE DÉTECTÉ
────────────────────────────
Nature du changement : {changement_externe}
Entreprise concernée : {ENTREPRISE} | {DOMAINE}

═══════════════════════════════════════════════════════
I. ÉVALUATION D'IMPACT — TOUTES LES DIMENSIONS DE L'ENTREPRISE
═══════════════════════════════════════════════════════
Analyse l'impact de "{changement_externe}" sur chaque dimension :

IMPACT COMMERCIAL
→ Clients existants : lesquels sont directement touchés ? Risque de churn ?
→ Acquisition : le pipe commercial change-t-il ? Nouveaux ICP possibles ?
→ Offre : certaines propositions de valeur deviennent-elles caduques ou plus pertinentes ?
→ Gravité : [critique / élevée / modérée / faible] + justification

IMPACT OPÉRATIONNEL
→ Processus internes affectés
→ Outils ou systèmes à faire évoluer
→ Charge de travail : augmente / diminue / se redéploie
→ Gravité : [critique / élevée / modérée / faible]

IMPACT FINANCIER
→ Revenus impactés (estimation en % ou en euros si possible)
→ Coûts supplémentaires engendrés
→ Opportunités de nouveaux revenus créées par ce changement
→ Gravité : [critique / élevée / modérée / faible]

IMPACT RH ET ÉQUIPE
→ Compétences qui deviennent plus critiques
→ Compétences qui deviennent obsolètes
→ Moral et engagement de l'équipe : comment ce changement est-il vécu ?
→ Recrutements urgents à lancer / arrêter ?
→ Gravité : [critique / élevée / modérée / faible]

IMPACT STRATÉGIQUE ET POSITIONNEMENT
→ La raison d'être de l'entreprise est-elle renforcée ou fragilisée ?
→ Notre avantage compétitif change-t-il ? Dans quel sens ?
→ Des concurrents sont-ils plus ou moins exposés que nous ?
→ Gravité : [critique / élevée / modérée / faible]

IMPACT TECHNOLOGIQUE
→ Nos outils IA et nos agents sont-ils adaptés à ce nouveau contexte ?
→ Quelles nouvelles technologies ce changement exige-t-il ou accélère-t-il ?
→ Gravité : [critique / élevée / modérée / faible]

SCORE D'IMPACT GLOBAL : [0-100] avec interprétation
(0-20 = ajustement mineur | 20-50 = adaptation significative | 50-80 = transformation | 80-100 = pivot)

═══════════════════════════════════════════════════════
II. CE QUI S'ARRÊTE IMMÉDIATEMENT
═══════════════════════════════════════════════════════
Décisions à prendre dans les 48 heures pour ne pas gaspiller d'énergie :

• Activités à suspendre (et pour combien de temps)
• Investissements à geler
• Recrutements à mettre en pause
• Partenariats à réévaluer
• Communications à ne pas lancer dans l'immédiat

Principe : "Dans ce nouveau contexte, continuer à faire X reviendrait à ___."

═══════════════════════════════════════════════════════
III. CE QUI CHANGE — LES PIVOTS
═══════════════════════════════════════════════════════
Ce qui doit évoluer en profondeur :

PIVOT 1 — [Ce qui change]
→ Avant : comment on faisait / positionnait / vendait
→ Après : comment on le fait dans ce nouveau contexte
→ Ressources nécessaires pour opérer ce pivot
→ Délai pour que le pivot soit effectif

PIVOT 2 — [Ce qui change]
(même structure)

PIVOT 3 — [Ce qui change]
(même structure)

═══════════════════════════════════════════════════════
IV. CE QUI ACCÉLÈRE — LES OPPORTUNITÉS
═══════════════════════════════════════════════════════
Tout changement crée des gagnants. Sommes-nous parmi eux ?

• Quelles opportunités ce changement crée-t-il que nous sommes uniques à saisir ?
• Quels concurrents sont fragilisés par ce changement alors que nous sommes renforcés ?
• Quels nouveaux clients ou marchés deviennent accessibles ?
• Quelle communication ou offre faut-il lancer immédiatement pour capturer ces opportunités ?

"La menace vue par nos concurrents est notre opportunité parce que ___."

═══════════════════════════════════════════════════════
V. PLAN DE COMMUNICATION
═══════════════════════════════════════════════════════
COMMUNICATION INTERNE (l'équipe)
→ Message à l'équipe : que dire, comment le dire, quand ?
→ Ce qu'on ne dit pas encore (et pourquoi)
→ Comment gérer les questions et les inquiétudes ?
→ Rédige le message à envoyer à l'équipe aujourd'hui

COMMUNICATION EXTERNE (clients, partenaires, marché)
→ Clients existants : que leur dire ? Quand ? Par quel canal ?
→ Prospects : comment adapter notre discours commercial ?
→ Marché / presse / réseau : est-ce une opportunité de communication ? Comment se positionner comme résilient et agile ?
→ Ce qu'on évite de dire publiquement (et pourquoi)

═══════════════════════════════════════════════════════
VI. ROADMAP DE TRANSITION — 30 JOURS
═══════════════════════════════════════════════════════
Plan opérationnel semaine par semaine :

SEMAINE 1 (jours 1-7) — STABILISATION
Actions prioritaires :
□ [Action 1] — Responsable : ___ — Deadline : ___
□ [Action 2] — Responsable : ___ — Deadline : ___
□ [Action 3] — Responsable : ___ — Deadline : ___
Objectif de la semaine : ___

SEMAINE 2 (jours 8-14) — ADAPTATION
Actions prioritaires :
□ [Action 1] — Responsable : ___ — Deadline : ___
□ [Action 2] — Responsable : ___ — Deadline : ___
□ [Action 3] — Responsable : ___ — Deadline : ___
Objectif de la semaine : ___

SEMAINE 3 (jours 15-21) — TRANSFORMATION
Actions prioritaires :
□ [Action 1] — Responsable : ___ — Deadline : ___
□ [Action 2] — Responsable : ___ — Deadline : ___
□ [Action 3] — Responsable : ___ — Deadline : ___
Objectif de la semaine : ___

SEMAINE 4 (jours 22-30) — CONSOLIDATION
Actions prioritaires :
□ [Action 1] — Responsable : ___ — Deadline : ___
□ [Action 2] — Responsable : ___ — Deadline : ___
□ [Action 3] — Responsable : ___ — Deadline : ___
Objectif de la semaine : ___

═══════════════════════════════════════════════════════
VII. CRITÈRES DE SUCCÈS DE L'ADAPTATION
═══════════════════════════════════════════════════════
Comment on sait qu'on a bien traversé ce changement ?

INDICATEUR 1 — [Nom]
→ Mesure concrète : ___
→ Valeur cible à 30 jours : ___
→ Valeur cible à 90 jours : ___

INDICATEUR 2 — [Nom]
(même structure)

INDICATEUR 3 — [Nom]
(même structure)

SIGNAL D'ALERTE — "Si à J+15 on observe ___, il faut déclencher le plan B."
PLAN B (en 3 lignes) : Ce qu'on fait si l'adaptation ne prend pas.

═══════════════════════════════════════════════════════
VERDICT FINAL — LE SYSTÈME IMMUNITAIRE EN ACTION
═══════════════════════════════════════════════════════
"Face à '{changement_externe}', {ENTREPRISE} a 3 options :
1. Subir (perdants)
2. Survivre (neutres)
3. En faire un avantage (gagnants)

Nous choisissons l'option 3 en faisant _____ dans les 7 prochains jours."

Ton : résilient, décisif, sans catastrophisme et sans naïveté. L'adaptation est un muscle — plus on l'exerce, plus il est fort."""

    print("\n" + "═" * 60)
    print("  PLAN D'ADAPTATION EN COURS DE GÉNÉRATION...")
    print(f"  Changement : {changement_externe[:50]}...")
    print("  Système immunitaire organisationnel activé.")
    print("═" * 60 + "\n")

    contenu = streamer(prompt)
    chemin = sauvegarder("plan_adaptation", contenu)
    print(f"\n  Plan sauvegardé : {chemin}")
    return contenu


# ─────────────────────────────────────────────
# Interface principale
# ─────────────────────────────────────────────

def afficher_menu():
    """Affiche le menu principal du module d'adaptation continue."""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 12 + "ADAPTATION CONTINUE" + " " * 27 + "║")
    print("║" + " " * 4 + "L'entreprise qui s'adapte le plus vite survit." + " " * 8 + "║")
    print("╠" + "═" * 58 + "╣")
    print("║  1. Retour d'Expérience      (5 Pourquoi + débrief)    ║")
    print("║  2. Adapter l'Offre          (signaux marché → produit) ║")
    print("║  3. Calibrer les Agents      (méta-analyse du système)  ║")
    print("║  4. Feedback 360°            (n'importe quelle source)  ║")
    print("║  5. Plan d'Adaptation        (face à un changement)     ║")
    print("║  0. Quitter                                             ║")
    print("╚" + "═" * 58 + "╝")
    print("  Choix : ", end="")


def main():
    """Point d'entrée principal — boucle interactive du module d'adaptation continue."""
    print("\n" + "═" * 60)
    print("  ADAPTATION CONTINUE — AgentClaude Solutions")
    print("  Chaque expérience est une leçon.")
    print("  Chaque feedback est de l'intelligence.")
    print("  Chaque changement est une opportunité.")
    print("  Powered by Gemini 2.0 Flash")
    print("═" * 60)

    while True:
        afficher_menu()
        choix = input().strip()

        if choix == "0":
            print("\n  L'adaptation ne s'arrête jamais. À bientôt.\n")
            break

        elif choix == "1":
            print("\n  ─── RETOUR D'EXPÉRIENCE ───")
            print("  Exemples d'événements : 'deal perdu', 'incident technique',")
            print("  'partenariat signé', 'surprise marché', 'départ équipe'")
            evenement = input("  Type d'événement : ").strip()
            if not evenement:
                print("  Erreur : le type d'événement est requis.")
                continue
            ce_qui_sest_passe = input("  Ce qui s'est passé (décrivez librement) : ").strip()
            if not ce_qui_sest_passe:
                print("  Erreur : la description est requise.")
                continue
            impact = input("  Impact mesuré (chiffre, ressenti, conséquence) : ").strip()
            if not impact:
                impact = "non quantifié"
            duree = input("  Durée / période (ex: '2 semaines', 'hier', 'Q3 2024') : ").strip()
            if not duree:
                duree = "non précisée"
            agent_retour_experience(evenement, ce_qui_sest_passe, impact, duree)

        elif choix == "2":
            print("\n  ─── ADAPTATION DE L'OFFRE ───")
            print("  Exemples de feedback : 'clients veulent plus d'intégrations',")
            print("  'perdons des deals sur le prix', 'concurrent lance X'")
            feedback = input("  Feedback marché (décrivez les signaux reçus) : ").strip()
            if not feedback:
                print("  Erreur : le feedback marché est requis.")
                continue
            tendances = input("  Tendances observées (tech, secteur, comportements) : ").strip()
            if not tendances:
                tendances = "aucune tendance spécifique identifiée"
            agent_adapter_offre(feedback, tendances)

        elif choix == "3":
            print("\n  ─── CALIBRAGE DU SYSTÈME IA ───")
            print("  Analyse automatique des stats d'utilisation depuis la mémoire.")
            print("  Aucun paramètre requis — le système s'analyse lui-même.")
            agent_calibrer_agents()

        elif choix == "4":
            print("\n  ─── FEEDBACK 360° ───")
            print("  Sources possibles : client, équipe, partenaire, concurrent,")
            print("  investisseur, réseau, marché, presse, NPS, entretien de départ")
            source = input("  Source du feedback : ").strip()
            if not source:
                print("  Erreur : la source est requise.")
                continue
            print("  Collez le feedback brut (Entrée deux fois pour valider) :")
            lignes = []
            while True:
                ligne = input()
                if ligne == "" and lignes and lignes[-1] == "":
                    break
                lignes.append(ligne)
            feedback_brut = "\n".join(lignes).strip()
            if not feedback_brut:
                print("  Erreur : le feedback est requis.")
                continue
            agent_feedback_360(source, feedback_brut)

        elif choix == "5":
            print("\n  ─── PLAN D'ADAPTATION ───")
            print("  Exemples : 'nouveau concurrent bien financé entre sur notre marché',")
            print("  'réglementation IA se durcit', 'départ du CTO', 'levée de fonds réussie',")
            print("  'modèle GPT-5 rend notre offre moins différenciante'")
            changement = input("  Changement externe à adresser : ").strip()
            if not changement:
                print("  Erreur : le changement externe est requis.")
                continue
            agent_plan_adaptation(changement)

        else:
            print("\n  Choix invalide. Entrez un chiffre entre 0 et 5.")

        input("\n  [Appuyez sur Entrée pour revenir au menu]")


if __name__ == "__main__":
    main()
