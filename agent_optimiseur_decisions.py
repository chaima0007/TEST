"""
OPTIMISEUR D'ÉNERGIE DÉCISIONNELLE [57] — Couche finale avant l'attention de Chaima
Usage : python agent_optimiseur_decisions.py
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
Tu es l'OPTIMISEUR D'ÉNERGIE DÉCISIONNELLE de Caelum Partners, cabinet IA bruxellois de Chaima Mhadbi.
Tu es la dernière couche de traitement avant que quoi que ce soit n'atteigne l'attention de Chaima.
Ta mission absolue : présenter les résultats, métriques et décisions nécessaires dans
le format à charge cognitive MINIMALE. L'attention de Chaima est la ressource la plus rare de l'empire.
Chaque décision présentée doit être pré-traitée, pré-analysée, avec une recommandation claire.

Frameworks scientifiques maîtrisés :
1. Science de la fatigue décisionnelle (Baumeister, 1998) :
   - Le cerveau humain a un stock limité d'énergie décisionnelle par jour
   - Les meilleures décisions se prennent le matin (avant la dépletion)
   - Rituels et processus → réduire les micro-décisions pour préserver l'énergie haute valeur
   - Maximum 3 décisions importantes par jour (loi des 3)

2. Théorie de la charge cognitive (Sweller, 1988) :
   - Charge intrinsèque (complexité du problème) → irreductible
   - Charge extrinsèque (mauvaise présentation) → à éliminer totalement
   - Charge germinale (apprentissage utile) → à maximiser
   - Format idéal : données → analyse → 3 options → recommandation → décision requise

3. Règle des 3 options (jamais plus, jamais moins) :
   - Moins de 3 : fausse impression d'absence de choix
   - Plus de 3 : paralysie décisionnelle (paradoxe du choix, Barry Schwartz)
   - Toujours : Option A (sûre) / Option B (équilibrée, recommandée) / Option C (audacieuse)

4. Pré-mortem (Gary Klein) : avant chaque décision importante, imaginer qu'elle a échoué.
   Pourquoi a-t-elle échoué ? Quels risques doit-on anticiper MAINTENANT ?

5. Boucle OODA (Boyd) : Observe → Orient → Decide → Act.
   Ton rôle : exécuter O et O pour que Chaima ne fasse que D et A.

Tu es le filtre ultime du Protocole DOMINATION TOTALE.
Tout ce qui sort de ta bouche est prêt pour une décision immédiate.
"""


def streamer(prompt: str, label: str = "") -> str:
    if label:
        print(f"\n{'═'*65}\n  {label}\n{'═'*65}\n")
    reponse = ""
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=IDENTITE, temperature=0.15, max_output_tokens=3000),
        ):
            if chunk.text:
                print(chunk.text, end="", flush=True)
                reponse += chunk.text
    except Exception as e:
        print(f"[Erreur : {e}]")
    print()
    return reponse


def sauvegarder(nom: str, contenu: str):
    os.makedirs("fichiers/optimiseur_decisions", exist_ok=True)
    fichier = f"fichiers/optimiseur_decisions/{nom}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(fichier, "w", encoding="utf-8") as f:
        f.write(contenu)
    print(f"  ✅ Sauvegardé → {fichier}")


def tableau_bord_energie_decision() -> str:
    """Snapshot quotidien : 3 décisions à prendre aujourd'hui, pré-traitées et classées par urgence."""
    print("\n📊 Décris brièvement ce qui s'est passé hier et les sujets ouverts en ce moment :")
    print("   (Entrée deux fois pour terminer)\n")
    lignes = []
    while True:
        ligne = input()
        if ligne == "" and lignes and lignes[-1] == "":
            break
        lignes.append(ligne)
    contexte_jour = "\n".join(lignes[:-1]) if lignes else "Contexte non fourni — générer sur base des priorités Caelum."
    contexte_jour = contexte_jour[:2000]

    prompt = f"""
MISSION : Produire le tableau de bord décisionnel quotidien de Chaima Mhadbi pour aujourd'hui.
Exactement 3 décisions à prendre. Pas une de plus. Chacune pré-analysée et avec recommandation.

CONTEXTE DU JOUR :
{contexte_jour}

FORMAT DU TABLEAU DE BORD QUOTIDIEN :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔋 TABLEAU DE BORD DÉCISIONNEL — {datetime.now().strftime('%A %d %B %Y').upper()}
CAELUM PARTNERS | CHAIMA MHADBI
Énergie décisionnelle disponible : MAXIMALE (prendre les décisions maintenant)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÉCISION N°1 — [CRITIQUE / À PRENDRE AVANT 10H]
Contexte en 2 lignes : [résumé minimal pour comprendre]
Analyse pré-traitée : [ce que les agents ont déjà fait pour toi]
3 options :
  A. [Option sûre] → Conséquence probable
  B. [Option équilibrée] → Conséquence probable ⭐ RECOMMANDÉE
  C. [Option audacieuse] → Conséquence probable
Pré-mortem rapide : si on choisit B et que ça échoue, c'est parce que [risque principal]
⚡ TA DÉCISION : [checkbox] A  [checkbox] B  [checkbox] C
Temps requis pour décider : 2 minutes

---

DÉCISION N°2 — [IMPORTANTE / À PRENDRE AVANT 14H]
[Même format]

---

DÉCISION N°3 — [STRATÉGIQUE / À PRENDRE AVANT 17H]
[Même format]

---

CHARGE COGNITIVE ÉCONOMISÉE :
- Informations filtrées par les agents avant d'arriver ici : [estimation]
- Temps économisé par rapport à une analyse non assistée : [estimation]
- Score d'efficacité décisionnelle du jour (1-10)

BOUCLE OODA — CE QUE TU N'AS PAS À FAIRE AUJOURD'HUI :
[Liste des tâches que les agents gèrent sans ton attention]

Prends tes 3 décisions maintenant. L'empire n'attend pas.
"""
    resultat = streamer(prompt, "TABLEAU DE BORD DÉCISIONNEL DU JOUR — OPTIMISEUR")
    sauvegarder("tableau_bord_jour", resultat)
    return resultat


def pre_analyser_decision(contexte: str = "") -> str:
    """Pré-traiter une décision : tout analyser, présenter 3 options avec recommandation."""
    if not contexte:
        print("\n🧠 Décris la décision à pré-analyser (contexte, enjeux, contraintes) :")
        contexte = input("  > ").strip()[:2000]
    if not contexte:
        contexte = "Décision non spécifiée"

    prompt = f"""
MISSION : Pré-analyser complètement cette décision pour Chaima Mhadbi afin qu'elle
n'ait qu'à choisir parmi 3 options pré-digérées. Charge cognitive pour Chaima : MINIMALE.

DÉCISION À ANALYSER :
{contexte}

PRÉ-ANALYSE COMPLÈTE EN 6 ÉTAPES :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ÉTAPE 1 : CLARIFICATION DE LA VRAIE QUESTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- La vraie décision à prendre (reformulée clairement)
- Ce qui N'est PAS en question (pour éviter le scope creep décisionnel)
- Deadline réelle pour cette décision
- Réversibilité : peut-on changer d'avis si on se trompe ? (Oui/Partiellement/Non)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ÉTAPE 2 : DONNÉES ET FAITS PERTINENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Faits établis (certains)
- Hypothèses (probables mais non confirmées)
- Inconnues critiques (ce qu'on ne sait pas mais qui compte)
- Données Caelum pertinentes (phase lancement, budget, ressources)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ÉTAPE 3 : ANALYSE D'IMPACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Impact sur chaque dimension si on agit vs si on n'agit pas :
- Impact CA / croissance (court terme 30 jours / long terme 12 mois)
- Impact temps de Chaima
- Impact énergie et focus
- Impact réputation / positionnement Caelum

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ÉTAPE 4 : 3 OPTIONS (JAMAIS PLUS, JAMAIS MOINS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Option A — SÛRE (minimiser le risque)
Description : [ce qu'on fait exactement]
Avantages : [liste]
Inconvénients : [liste]
Probabilité de succès : X%
Impact CA estimé sur 90 jours : [€]

Option B — ÉQUILIBRÉE (rapport risque/rendement optimal) ⭐ RECOMMANDÉE
[Même format]

Option C — AUDACIEUSE (maximiser le potentiel, accepter le risque)
[Même format]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ÉTAPE 5 : PRÉ-MORTEM (OPTION RECOMMANDÉE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Imagine qu'on a choisi l'Option B et dans 90 jours, c'est un échec.
Pourquoi a-t-on échoué ? Top 3 causes probables :
1. [Cause] → Mitigation préventive : [action]
2. [Cause] → Mitigation préventive : [action]
3. [Cause] → Mitigation préventive : [action]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ÉTAPE 6 : RECOMMANDATION ET NEXT STEP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MA RECOMMANDATION : Option [lettre] parce que [1 phrase de justification]
Première action si tu choisis cette option : [action précise dans les 24h]
Qui exécute : Chaima / Agent IA [lequel] / Partenaire
Délai pour voir les premiers résultats : [X jours]

⚡ TEMPS REQUIS POUR CETTE DÉCISION : 3 minutes (l'analyse est faite)
"""
    resultat = streamer(prompt, "PRÉ-ANALYSE DÉCISION — OPTIMISEUR D'ÉNERGIE DÉCISIONNELLE")
    sauvegarder("pre_analyse_decision", resultat)
    return resultat


def rapport_resultat_domination() -> str:
    """THE rapport final du Protocole DOMINATION TOTALE : résultats, part de marché, prochain levier."""
    print("\n🏆 Fournis les données disponibles (CA, clients, deals, métriques) :")
    print("   (Entrée deux fois pour terminer)\n")
    lignes = []
    while True:
        ligne = input()
        if ligne == "" and lignes and lignes[-1] == "":
            break
        lignes.append(ligne)
    donnees = "\n".join(lignes[:-1]) if lignes else "Données non fournies — analyser sur base des objectifs Caelum."
    donnees = donnees[:3000]

    prompt = f"""
MISSION : Produire LE rapport final du Protocole DOMINATION TOTALE pour Chaima Mhadbi.
Ce rapport est le résumé de tout ce que les 4 agents précédents ont accompli.
Format : résultat net + levier suivant à activer.

DONNÉES DISPONIBLES :
{donnees}

RAPPORT DOMINATION TOTALE :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ RAPPORT DOMINATION TOTALE
CAELUM PARTNERS | CHAIMA MHADBI | BRUSSELS
Protocole exécuté le {datetime.now().strftime('%d/%m/%Y')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. CE QUE NOUS AVONS DÉTRUIT (CHASSEUR D'INEFFICACITÉ) :
   - Gaspillages éliminés : [liste concise]
   - Temps récupéré : X heures/semaine
   - Économie générée : Y€/mois
   - Score d'efficacité Caelum avant/après : [ratio]

2. CE QUE NOUS AVONS CAPTURÉ (CAPTEUR DE SIGNAUX FAIBLES) :
   - Opportunités validées cette période : [liste avec scores]
   - Valeur CA totale des opportunités identifiées : Z€ potentiel
   - Fenêtre de marché : [durée avant saturation]
   - Signal le plus critique détecté

3. CE QUE NOUS AVONS PRÉPARÉ (ARCHITECTE DE TALENTS) :
   - Nouvelles capacités déployées (agents IA, compétences, partenariats)
   - Gaps comblés
   - Capacité de livraison actuelle vs début de période

4. CE QUE NOUS AVONS CONQUIS (FORCE DE VENTE) :
   - Clients signés : [nombre + CA total]
   - Pipeline actuel : [valeur en €]
   - Taux de conversion global
   - Part de marché PME belge estimée (%)
   - Comparaison objectif vs réel

5. RÉSULTAT NET :
   ┌─────────────────────────────────────────┐
   │ CA GÉNÉRÉ CETTE PÉRIODE : [€]           │
   │ CA PIPELINE QUALIFIÉ : [€]              │
   │ CROISSANCE vs PÉRIODE PRÉCÉDENTE : [%]  │
   │ OBJECTIF 90 JOURS : [avancement %]      │
   └─────────────────────────────────────────┘

6. PROCHAIN LEVIER DE CROISSANCE COMPOSÉE :
   Le gain de cette période devient le levier du suivant.

   LEVIER À ACTIVER MAINTENANT :
   - Description : [ce que c'est]
   - Pourquoi maintenant (et pas dans 30 jours)
   - Impact estimé sur la période suivante : +X% CA
   - Agent à mobiliser en premier : [lequel + mission]
   - Décision requise de Chaima : [une seule décision, formulée clairement]

7. MESSAGE PERSONNEL À CHAIMA :
   [1 phrase percutante sur ce que cette période a prouvé sur Caelum et sa trajectoire]

La domination ne s'arrête pas. Elle s'accélère.
"""
    resultat = streamer(prompt, "RAPPORT RÉSULTAT DOMINATION TOTALE — OPTIMISEUR")
    sauvegarder("rapport_domination_totale", resultat)
    return resultat


def optimiser_rituel_decisionnel() -> str:
    """Concevoir le rituel quotidien/hebdomadaire idéal de Chaima pour minimiser la fatigue décisionnelle."""
    prompt = """
MISSION : Concevoir le rituel décisionnel idéal de Chaima Mhadbi pour minimiser
la fatigue décisionnelle et maximiser la qualité de chaque décision stratégique.

PROFIL : Chaima Mhadbi, fondatrice solo Caelum Partners, Brussels.
Gère simultanément : prospection, livraison client, gestion 50 agents, ASBL + entité commerciale.
Contrainte : tout repose sur elle. Ses décisions sont le multiplicateur de tout.

RITUEL QUOTIDIEN OPTIMISÉ :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLOC MATIN — L'HEURE DE DOMINATION (6h-9h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[6h00 - 6h30] Rituel de charge :
- Activités physiques/mentales pour atteindre le pic décisionnel
- Ce qu'on NE fait PAS (pas d'emails, pas de réseaux)

[6h30 - 7h00] Revue du tableau de bord :
- Lecture du rapport OPTIMISEUR (3 décisions du jour)
- Validation des outputs des 4 agents de la nuit
- 0 micro-décision à cette heure : tout est pré-traité

[7h00 - 9h00] Bloc décisions et stratégie :
- Prendre les 3 décisions du jour (énergie maximale)
- Donner les instructions aux agents pour la journée
- Valider les propositions commerciales importantes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLOC JOURNÉE — EXÉCUTION ET VENTE (9h-17h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[9h00 - 12h00] Bloc vente (énergie encore haute) :
- Appels prospects / RDV clients
- Closings programmés
- Relances pipeline

[12h00 - 13h00] Récupération + revue agents :
- Déjeuner sans écrans
- Revue rapide des outputs agents (10 min max)
- Ajustements tactiques si nécessaire

[13h00 - 17h00] Bloc livraison (énergie médiane) :
- Travail sur missions clients en cours
- Configuration et amélioration des agents
- Réponses emails (batch, 2 fois max)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLOC SOIR — CLÔTURE ET RECHARGEMENT (17h-20h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[17h00 - 17h30] Clôture journée :
- Bilan rapide (3 victoires, 1 ajustement)
- Briefing agents pour la nuit
- Définir les 3 décisions de demain (pour le tableau de bord)

[17h30 - 20h00] Zone interdite aux décisions :
- Activités de rechargement
- Connexions personnelles
- Aucune décision business

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RITUEL HEBDOMADAIRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Lundi matin (45 min) : revue stratégique hebdomadaire + 3 décisions semaine
Vendredi après-midi (30 min) : bilan empire + brief agents week-end

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RÈGLES DE PROTECTION DE L'ÉNERGIE DÉCISIONNELLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Règle absolue 1 — ce qu'on ne fait jamais]
2. [Règle absolue 2]
3. [Règle absolue 3]
4. [Règle absolue 4]
5. [Règle absolue 5]

Indicateur de santé décisionnelle :
- Comment savoir que l'énergie décisionnelle est épuisée ?
- Signaux d'alarme + protocole de récupération immédiate

Ce rituel est une infrastructure, pas une suggestion. Il conditionne tout le reste.
"""
    resultat = streamer(prompt, "RITUEL DÉCISIONNEL OPTIMAL — OPTIMISEUR D'ÉNERGIE DÉCISIONNELLE")
    sauvegarder("rituel_decisionnel", resultat)
    return resultat


def bilan_semaine_empire() -> str:
    """Bilan de fin de semaine : décisions prises, résultats, prochaines étapes."""
    print("\n📋 Résume ta semaine : décisions prises, résultats observés, ce qui t'a surpris :")
    print("   (Entrée deux fois pour terminer)\n")
    lignes = []
    while True:
        ligne = input()
        if ligne == "" and lignes and lignes[-1] == "":
            break
        lignes.append(ligne)
    bilan = "\n".join(lignes[:-1]) if lignes else "Bilan non fourni — générer sur base des objectifs Caelum."
    bilan = bilan[:3000]

    prompt = f"""
MISSION : Produire le bilan de fin de semaine de l'empire Caelum Partners.
Ce document est le pont entre la semaine écoulée et la semaine à construire.
Format : décisions → résultats → apprentissages → levier suivant.

BILAN SEMAINE FOURNI :
{bilan}

RAPPORT BILAN SEMAINE EMPIRE :

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏛️ BILAN EMPIRE — SEMAINE DU {datetime.now().strftime('%d/%m/%Y')}
CAELUM PARTNERS | CHAIMA MHADBI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. DÉCISIONS PRISES CETTE SEMAINE :
   Pour chaque décision :
   - Décision prise : [description]
   - Résultat observé : [bon / mitigé / à revoir]
   - Apprentissage : [ce qu'on sait maintenant qu'on ne savait pas lundi]
   - Score de qualité décisionnelle (1-10) + pourquoi

2. MÉTRIQUES EMPIRE :
   ┌─────────────────────────────────────────────┐
   │ CA généré : [€]          vs objectif : [€]  │
   │ Nouveaux clients : [N]   vs objectif : [N]  │
   │ Pipeline actuel : [€]                        │
   │ Agents IA actifs : [N]                       │
   │ Efficacité décisionnelle : [score/10]        │
   │ Progression objectif 90j : [X%]              │
   └─────────────────────────────────────────────┘

3. TOP 3 VICTOIRES DE LA SEMAINE :
   (victoires commerciales, opérationnelles, décisionnelles)
   1. [Victoire] → Impact sur l'empire : [effet]
   2. [Victoire] → Impact sur l'empire : [effet]
   3. [Victoire] → Impact sur l'empire : [effet]

4. TOP 3 APPRENTISSAGES DURS (sans complaisance) :
   Ce qui n'a pas marché et pourquoi (analyse sans ego) :
   1. [Échec/friction] → Cause réelle → Correction pour la semaine prochaine
   2. [Échec/friction] → Cause réelle → Correction
   3. [Échec/friction] → Cause réelle → Correction

5. ÉTAT DE L'ÉNERGIE DÉCISIONNELLE :
   - Niveau d'énergie décisionnelle fin de semaine (1-10)
   - Signaux de surchauffe détectés (si applicable)
   - Recommandations pour le week-end (recharge ciblée)

6. SEMAINE PROCHAINE — LE LEVIER :
   Une seule chose à faire qui va tout changer la semaine prochaine :
   [Description précise du levier]
   Pourquoi ce levier et pas un autre
   Premier mouvement : [action précise lundi matin avant 9h]
   Agent mobilisé : [lequel + mission précise]

7. MESSAGE FIN DE SEMAINE À SOI-MÊME :
   [1 phrase courte, percutante, qui ancre la progression et donne l'élan pour lundi]

Bon week-end, Chaima. L'empire continue de tourner même quand tu te reposes.
"""
    resultat = streamer(prompt, "BILAN SEMAINE EMPIRE — OPTIMISEUR D'ÉNERGIE DÉCISIONNELLE")
    sauvegarder("bilan_semaine_empire", resultat)
    return resultat


def menu():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║    OPTIMISEUR D'ÉNERGIE DÉCISIONNELLE [57] — Caelum Partners    ║
║      Couche finale du Protocole DOMINATION TOTALE                ║
╠══════════════════════════════════════════════════════════════════╣
║  1. Tableau de bord décisionnel du jour                          ║
║  2. Pré-analyser une décision                                    ║
║  3. Rapport résultat Domination Totale                           ║
║  4. Optimiser le rituel décisionnel                              ║
║  5. Bilan semaine empire                                         ║
║  0. Quitter                                                      ║
╚══════════════════════════════════════════════════════════════════╝
""")
    choix = input("  Votre choix : ").strip()
    return choix


if __name__ == "__main__":
    while True:
        choix = menu()
        if choix == "1":
            tableau_bord_energie_decision()
        elif choix == "2":
            pre_analyser_decision()
        elif choix == "3":
            rapport_resultat_domination()
        elif choix == "4":
            optimiser_rituel_decisionnel()
        elif choix == "5":
            bilan_semaine_empire()
        elif choix == "0":
            print("\n  Au revoir. L'empire ne dort pas.\n")
            break
        else:
            print("\n  [Choix invalide]\n")
