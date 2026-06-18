import os
import datetime
from google import genai
from google.genai import types
from memoire import incrementer_stat

MODEL = "gemini-2.0-flash"

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = _creer_model(MODEL)

ENTREPRISE = "AgentClaude Solutions"
DOMAINE = "solutions d'agents IA autonomes"
SECTEUR = "intelligence artificielle et automatisation"


# ─────────────────────────────────────────────
# Utilitaires
# ─────────────────────────────────────────────

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
    """Sauvegarde le rapport dans fichiers/innovation/ avec horodatage."""
    dossier = "/home/user/TEST/fichiers/innovation"
    os.makedirs(dossier, exist_ok=True)
    horodatage = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    chemin = f"{dossier}/{nom_fichier}_{horodatage}.txt"
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


# ─────────────────────────────────────────────
# Agent 1 – Brainstorm Quantique
# ─────────────────────────────────────────────

def agent_brainstorm_quantique(probleme: str, contraintes: str) -> str:
    """Brainstorming quantique : 5 frameworks simultanés → 25 idées → top 5 avec chemin d'implémentation."""
    incrementer_stat("agent_brainstorm_quantique")

    prompt = f"""Tu es un génie créatif hybride : partie Nikola Tesla, partie Steve Jobs, partie chamane Silicon Valley.
Tu opères dans une dimension où l'impossible est simplement une idée qui n'a pas encore été pensée.

Problème à résoudre : {probleme}
Contraintes connues : {contraintes}
Contexte : {ENTREPRISE}, spécialisée en {DOMAINE}

Ta mission : activer SIMULTANÉMENT 5 frameworks de pensée créative et générer 25 idées radicales.

═══════════════════════════════════════════════════════
FRAMEWORK 1 — SCAMPER (5 idées)
═══════════════════════════════════════════════════════
Applique chaque lettre au problème :
• Substitute : qu'est-ce qu'on pourrait remplacer dans la solution actuelle ?
• Combine : quelles deux choses qu'on n'a jamais combinées pourraient fusionner ?
• Adapt : qu'est-ce qui existe ailleurs et qu'on pourrait adapter ici ?
• Modify/Magnify : si on exagérait ou réduisait à l'extrême un aspect, que se passe-t-il ?
• Put to other uses : à quoi d'autre cela pourrait-il servir, de façon inattendue ?
• Eliminate : qu'est-ce qu'on suppose nécessaire mais qui ne l'est pas vraiment ?
• Reverse : et si on faisait exactement l'inverse de ce que tout le monde fait ?
Génère 5 idées issues de ce framework, numérotées S1 à S5.

═══════════════════════════════════════════════════════
FRAMEWORK 2 — 6 CHAPEAUX DE DE BONO (5 idées)
═══════════════════════════════════════════════════════
Explore le problème avec les 6 perspectives :
• Chapeau Blanc : faits purs, données, qu'est-ce qu'on sait objectivement ?
• Chapeau Rouge : intuitions, émotions, qu'est-ce que "ça sent" ?
• Chapeau Noir : risques, ce qui peut échouer, l'avocat du diable
• Chapeau Jaune : optimisme pur, le meilleur scénario possible
• Chapeau Vert : pensée latérale pure, idées folles sans filtre
• Chapeau Bleu : la méta-perspective, comment penser différemment le problème lui-même ?
Génère 5 idées issues de ce framework, numérotées D1 à D5.

═══════════════════════════════════════════════════════
FRAMEWORK 3 — BIOMIMICRY (5 idées)
═══════════════════════════════════════════════════════
La nature a résolu 3,8 milliards d'années de problèmes d'ingénierie.
Demande-toi :
• Comment une fourmilière résoudrait ce problème ? (intelligence collective, sans centre de contrôle)
• Comment un arbre résoudrait ce problème ? (croissance lente, réseaux racinaires cachés)
• Comment un virus résoudrait ce problème ? (reproduction virale, adaptation rapide)
• Comment un banc de poissons résoudrait ce problème ? (comportement émergent, pas de chef)
• Comment la sélection naturelle résoudrait ce problème ? (variation, sélection, amplification)
Génère 5 idées bio-inspirées, numérotées B1 à B5.

═══════════════════════════════════════════════════════
FRAMEWORK 4 — PREMIERS PRINCIPES (méthode Elon Musk) (5 idées)
═══════════════════════════════════════════════════════
Décompose le problème jusqu'à ses atomes fondamentaux :
1. Quelles sont les suppositions que tout le monde accepte comme vraies ?
2. Lesquelles sont réellement fausses ou questionables ?
3. Après avoir tout démoli, reconstruis depuis zéro avec seulement la physique, la logique et les contraintes réelles.
4. Qu'est-ce qui devient possible quand on ignore les "meilleures pratiques" du secteur ?
5. Quelle serait la solution si on partait d'une feuille blanche absolue en 2030 ?
Génère 5 idées de premiers principes, numérotées P1 à P5.

═══════════════════════════════════════════════════════
FRAMEWORK 5 — SCIENCE-FICTION 2050 (5 idées)
═══════════════════════════════════════════════════════
Tu es en 2050. Ce problème a été résolu il y a 20 ans d'une façon que personne n'avait imaginée.
• Quelle technologie disponible en 2050 (mais pas encore en 2025) a tout changé ?
• Comment l'AGI ou une IA suprême aurait-elle abordé ça ?
• Si les interfaces cerveau-machine existaient, comment changerait la solution ?
• Si l'énergie était gratuite et infinie, qu'est-ce qui deviendrait possible ?
• Un enfant de 2050 regardant ce problème pense : "mais c'est évident, il fallait juste..."
Génère 5 idées futuristes, numérotées F1 à F5.

═══════════════════════════════════════════════════════
SYNTHÈSE QUANTIQUE — TOP 5 IDÉES IMPOSSIBLES À IGNORER
═══════════════════════════════════════════════════════
Parmi les 25 idées générées, sélectionne les 5 qui :
- Font battre le cœur plus vite
- Semblent impossibles mais sont en réalité faisables
- Créeraient un avantage compétitif asymétrique
- N'existent nulle part encore

Pour chacune des 5 idées finalistes :
★ NOM DE CODE (provocateur, mémorable)
★ L'IDÉE EN UNE PHRASE (si tu ne peux pas l'expliquer en une phrase, tu ne la comprends pas encore)
★ POURQUOI C'EST BRILLANT (l'insight non-évident)
★ CHEMIN D'IMPLÉMENTATION EN 3 ÉTAPES (90 jours, 6 mois, 12 mois)
★ QUI ÇA DÉTRUIT (les concurrents/industries qui disparaissent si ça marche)
★ NIVEAU D'AUDACE : ★★★★★ (5 = "on va se faire arrêter pour ça")

Termine par une ligne : "L'idée la plus dangereuse du lot est _____ parce que _____."

Sois radical. Sois inconfortable. L'innovation timide est une contradiction dans les termes."""

    print("\n" + "═" * 60)
    print("  BRAINSTORM QUANTIQUE EN COURS...")
    print("  5 frameworks activés simultanément.")
    print("═" * 60 + "\n")

    contenu = streamer(prompt)
    chemin = sauvegarder("brainstorm_quantique", contenu)
    print(f"\n  Rapport sauvegardé : {chemin}")
    return contenu


# ─────────────────────────────────────────────
# Agent 2 – Constructeur de Futurs
# ─────────────────────────────────────────────

def agent_constructeur_futurs(horizon_ans: int) -> str:
    """Planification par scénarios style Shell : 4 futurs radicaux + stratégie robuste à tous."""
    incrementer_stat("agent_constructeur_futurs")

    prompt = f"""Tu es le chef de l'équipe "Scenario Planning" de Shell — l'équipe qui a prédit le choc pétrolier de 1973 et la chute de l'URSS.
Tu appliques leur méthodologie à l'industrie des agents IA sur un horizon de {horizon_ans} ans.

Entreprise : {ENTREPRISE} — {DOMAINE}

Ta mission : construire 4 futurs radicalement différents et concevoir une stratégie robuste à TOUS les scénarios.

═══════════════════════════════════════════════════════
SCÉNARIO 1 — UTOPIE IA 🌟
"L'IA a tout résolu"
═══════════════════════════════════════════════════════
Dans ce futur (horizon {horizon_ans} ans) :
• L'IA généraliste a tenu ses promesses. Les agents autonomes gèrent 80% des tâches cognitives des entreprises.
• La productivité mondiale a triplé. Le travail humain s'est recentré sur la créativité et le relationnel.
• Les barrières à l'entrepreneuriat ont disparu : n'importe qui peut lancer une entreprise avec 3 agents.

MONDE : Décris précisément comment ce monde fonctionne (économie, travail, entreprises, société).
GAGNANTS : Qui prospère ? Quels secteurs explosent ? Quels nouveaux métiers existent ?
PERDANTS : Qui disparaît ? Quels secteurs s'effondrent ? Quelles compétences deviennent obsolètes ?
NOTRE POSITION : Où est {ENTREPRISE} dans ce monde ? Quelle part de marché ? Quel rôle ?
SIGNAL FAIBLE AUJOURD'HUI : Quel signe visible en 2025 indique qu'on va vers ce scénario ?

═══════════════════════════════════════════════════════
SCÉNARIO 2 — DYSTOPIE RÉGLEMENTAIRE ⚖️
"L'UE a tout interdit"
═══════════════════════════════════════════════════════
Dans ce futur :
• L'EU AI Act s'est durci après un incident majeur (crash financier IA, désinformation massive, accident industriel).
• Les agents autonomes sont classés "systèmes à haut risque" et nécessitent 18 mois de certification.
• Les entreprises européennes sont paralysées. Les Américains et Chinois dominent depuis l'offshore.

MONDE : Comment fonctionne ce monde réglementé à l'extrême ?
GAGNANTS : Qui s'adapte et prospère malgré tout ? Quels business models survivent ?
PERDANTS : Qui est écrasé par la conformité ? Quelles startups meurent ?
NOTRE POSITION : Comment {ENTREPRISE} survit-elle ? Pivot, compliance, résistance ?
SIGNAL FAIBLE AUJOURD'HUI : Quel signe visible en 2025 indique qu'on va vers ce scénario ?

═══════════════════════════════════════════════════════
SCÉNARIO 3 — FRAGMENTATION 🌐
"50 écosystèmes concurrents"
═══════════════════════════════════════════════════════
Dans ce futur :
• Aucun standard n'a émergé. Chaque industrie a son propre protocole d'agents IA incompatible.
• L'Healthcare IA ne parle pas à la Finance IA qui ne parle pas au Legal IA.
• Les coûts d'intégration explosent. Les intermédiaires règnent. La complexité est reine.

MONDE : Comment naviguer dans cet archipel de silos ?
GAGNANTS : Les agrégateurs ? Les traducteurs de protocoles ? Les experts verticaux ?
PERDANTS : Les solutions horizontales ? Les plateformes généralistes ?
NOTRE POSITION : {ENTREPRISE} devient quoi — un silo vertical ou un pont entre silos ?
SIGNAL FAIBLE AUJOURD'HUI : Quel signe visible en 2025 indique qu'on va vers ce scénario ?

═══════════════════════════════════════════════════════
SCÉNARIO 4 — SINGULARITÉ PRÉCOCE 🚀
"L'AGI est arrivé trop tôt"
═══════════════════════════════════════════════════════
Dans ce futur :
• L'AGI (Intelligence Artificielle Générale) arrive d'ici {min(horizon_ans, 7)} ans, bien avant les prévisions.
• Les agents spécialisés sont obsolètes du jour au lendemain — l'AGI fait tout mieux que tout le monde.
• Les règles du jeu changent complètement. La notion même "d'agent IA" devient désuète.

MONDE : Comment les entreprises s'organisent avec une entité qui peut tout faire ?
GAGNANTS : Ceux qui ont la relation directe avec l'AGI ? Les propriétaires d'infrastructure ?
PERDANTS : Toutes les solutions verticales spécialisées ? Les intégrateurs ?
NOTRE POSITION : {ENTREPRISE} se repositionne comment face à ce tsunami technologique ?
SIGNAL FAIBLE AUJOURD'HUI : Quel signe visible en 2025 indique qu'on va vers ce scénario ?

═══════════════════════════════════════════════════════
STRATÉGIE ROBUSTE — CE QU'ON FAIT MAINTENANT
"Les mouvements gagnants dans TOUS les futurs"
═══════════════════════════════════════════════════════
La vraie question du scenario planning n'est pas "quel futur va se réaliser ?"
C'est : "quels mouvements stratégiques sont gagnants QUEL QUE SOIT le futur ?"

Identifie :

1. LES INVARIANTS (ce qui est vrai dans tous les scénarios)
   → Sur quelles certitudes peut-on construire ?

2. LES OPTIONS STRATÉGIQUES ROBUSTES (6 mouvements concrets à lancer maintenant)
   Pour chaque mouvement :
   - Action concrète (pas un vœu pieux, une décision réelle)
   - Pourquoi gagnant dans le scénario Utopie
   - Pourquoi gagnant dans le scénario Dystopie
   - Pourquoi gagnant dans le scénario Fragmentation
   - Pourquoi gagnant dans le scénario Singularité
   - Délai pour le lancer : immédiat / 6 mois / 12 mois

3. LES PARIS ASYMÉTRIQUES (3 bets à faible coût / haut upside dans certains scénarios)
   → Quoi tester maintenant qui vaut une fortune si un scénario se réalise ?

4. LES LIGNES DIRECTRICES (3 signaux qui doivent déclencher un pivot majeur)
   → "Si X se produit d'ici 18 mois, on abandonne tout et on fait Y."

Conclus par : "La décision la plus importante que {ENTREPRISE} doit prendre dans les 90 prochains jours est _____ parce que c'est le seul mouvement stratégique qui change nos options dans les 4 scénarios."

Sois précis. Sois courageux. La stratégie timide n'existe pas."""

    print("\n" + "═" * 60)
    print(f"  CONSTRUCTION DE 4 FUTURS — HORIZON {horizon_ans} ANS")
    print("  Méthode Shell Scenario Planning activée.")
    print("═" * 60 + "\n")

    contenu = streamer(prompt)
    chemin = sauvegarder("constructeur_futurs", contenu)
    print(f"\n  Rapport sauvegardé : {chemin}")
    return contenu


# ─────────────────────────────────────────────
# Agent 3 – Produit Futuriste
# ─────────────────────────────────────────────

def agent_produit_futuriste(besoin_latent: str) -> str:
    """Invention de produits depuis les besoins latents : Jobs-to-be-Done + 3 produits inexistants."""
    incrementer_stat("agent_produit_futuriste")

    prompt = f"""Tu es un directeur de l'innovation dans un incubateur de startup à San Francisco en 2030.
Tu combines la rigueur du framework Jobs-to-be-Done de Clayton Christensen avec l'audace d'un fondateur de licorne.
Ton superpower : voir les besoins que les gens ne savent pas encore qu'ils ont.

Besoin latent à explorer : {besoin_latent}
Contexte : marché des agents IA, entreprise {ENTREPRISE}, domaine {DOMAINE}

═══════════════════════════════════════════════════════
ÉTAPE 1 — ARCHÉOLOGIE DU BESOIN
(Jobs-to-be-Done : le besoin réel sous le besoin exprimé)
═══════════════════════════════════════════════════════
Les gens ne veulent pas une perceuse, ils veulent un trou dans le mur.
Les gens ne veulent pas un trou dans le mur, ils veulent accrocher un tableau.
Les gens ne veulent pas accrocher un tableau, ils veulent que leurs invités pensent qu'ils ont bon goût.

Applique cette démarche à : {besoin_latent}

→ Besoin exprimé (surface)
→ Besoin fonctionnel (une couche dessous)
→ Besoin émotionnel (deux couches dessous)
→ Besoin identitaire (le vrai job-to-be-done)
→ Le besoin latent ultime que personne n'a encore articulé

═══════════════════════════════════════════════════════
ÉTAPE 2 — CARTOGRAPHIE DES TENSIONS
═══════════════════════════════════════════════════════
Dans ce domaine, quelles sont les 5 tensions non résolues ?
(Une tension = deux désirs légitimes mais contradictoires)
Ex : "vouloir plus de contrôle" vs "vouloir moins d'effort"
     "vouloir personnalisation" vs "vouloir simplicité"

Liste 5 tensions avec leur intensité (1-10) et pourquoi elles ne sont pas résolues aujourd'hui.

═══════════════════════════════════════════════════════
PRODUIT 1 — [NOM DU PRODUIT]
═══════════════════════════════════════════════════════
Invente un produit qui n'existe pas encore mais devrait exister.

◆ NOM DU PRODUIT : (mémorable, évocateur, un peu mystérieux)
◆ TAGLINE : (8 mots maximum, fait ressentir quelque chose)
◆ LE PROBLÈME QU'IL RÉSOUT : (le besoin latent en une phrase coupante)
◆ COMMENT ÇA MARCHE : (description fonctionnelle en 5 bullet points, sans jargon)
◆ L'INSIGHT NON-ÉVIDENT : (le truc que tout le monde a raté et qui rend ce produit possible)
◆ POURQUOI MAINTENANT : (quelle technologie rendue disponible en 2024-2025 rend ça faisable)
◆ MARCHÉ ADRESSABLE : (estimation TAM/SAM/SOM avec raisonnement)
◆ MODÈLE DE REVENUS : (comment on gagne de l'argent, simplement)
◆ PREMIERS PAS VERS UN PROTOTYPE :
   - Semaine 1 : (ce qu'on construit en une semaine avec 2 personnes)
   - Mois 1 : (MVP montrable à des prospects réels)
   - Mois 3 : (premier client payant, premier signal de product-market fit)
◆ LE CONCURRENT QUI DEVRAIT AVOIR PEUR : (et pourquoi ils ne l'ont pas encore fait)

═══════════════════════════════════════════════════════
PRODUIT 2 — [NOM DU PRODUIT]
═══════════════════════════════════════════════════════
(même structure que Produit 1, mais angle radicalement différent — cible un autre segment ou use case)

◆ NOM DU PRODUIT :
◆ TAGLINE :
◆ LE PROBLÈME QU'IL RÉSOUT :
◆ COMMENT ÇA MARCHE :
◆ L'INSIGHT NON-ÉVIDENT :
◆ POURQUOI MAINTENANT :
◆ MARCHÉ ADRESSABLE :
◆ MODÈLE DE REVENUS :
◆ PREMIERS PAS VERS UN PROTOTYPE :
◆ LE CONCURRENT QUI DEVRAIT AVOIR PEUR :

═══════════════════════════════════════════════════════
PRODUIT 3 — [NOM DU PRODUIT]
═══════════════════════════════════════════════════════
(même structure, mais celui-là est le plus audacieux, le plus "et si on allait vraiment loin")

◆ NOM DU PRODUIT :
◆ TAGLINE :
◆ LE PROBLÈME QU'IL RÉSOUT :
◆ COMMENT ÇA MARCHE :
◆ L'INSIGHT NON-ÉVIDENT :
◆ POURQUOI MAINTENANT :
◆ MARCHÉ ADRESSABLE :
◆ MODÈLE DE REVENUS :
◆ PREMIERS PAS VERS UN PROTOTYPE :
◆ LE CONCURRENT QUI DEVRAIT AVOIR PEUR :

═══════════════════════════════════════════════════════
VERDICT DE L'INVESTISSEUR
═══════════════════════════════════════════════════════
Tu es maintenant un partenaire de a16z avec 500M$ à déployer.
Lequel des 3 produits recevrait ton term sheet demain matin, et pourquoi ?
Quel risque t'empêche de financer les deux autres ?
Quelle question tu poserais au fondateur lors du premier pitch pour savoir s'il comprend vraiment le marché ?

Sois concret. Sois précis. Ce n'est pas de la prospective — c'est un plan de guerre."""

    print("\n" + "═" * 60)
    print("  INVENTION DE PRODUITS FUTURISTES EN COURS...")
    print("  Jobs-to-be-Done + Vision 2030 activés.")
    print("═" * 60 + "\n")

    contenu = streamer(prompt)
    chemin = sauvegarder("produit_futuriste", contenu)
    print(f"\n  Rapport sauvegardé : {chemin}")
    return contenu


# ─────────────────────────────────────────────
# Agent 4 – Disruption Créative
# ─────────────────────────────────────────────

def agent_disruption_creative(industrie_ciblee: str) -> str:
    """Playbook de disruption créative : 5 modèles légendaires × 3 stratégies IA."""
    incrementer_stat("agent_disruption_creative")

    prompt = f"""Tu es un stratège de disruption. Ton portfolio inclut des investissements précoces dans Uber, Airbnb, Spotify, Netflix et Apple.
Tu analyses maintenant comment détruire l'industrie : {industrie_ciblee}
En utilisant les agents IA comme arme principale.
Entreprise qui va disrupter : {ENTREPRISE}

═══════════════════════════════════════════════════════
ANATOMIE DE L'INDUSTRIE CIBLE
═══════════════════════════════════════════════════════
Avant de disrupter, il faut comprendre ce qu'on attaque :

• LES 3 VACHES SACRÉES : Quelles suppositions irrationnelles protège cette industrie ?
  (ex: "les taxis doivent avoir des licences", "les hôtels doivent posséder leurs chambres")

• LE GRUYÈRE : Où sont les 5 inefficacités majeures que les acteurs en place ne voient plus ?
  (Ils ne les voient plus car elles sont leur source de profit)

• LE CLIENT IGNORÉ : Quel segment de clients est mal servi ou surpayant sans alternative ?

• LA RÈGLE QUI N'A PAS DE SENS : Quelle règle du secteur semble évidente mais est arbitraire ?

═══════════════════════════════════════════════════════
LENS 1 — DISRUPTION UBER (Marketplace + Désintermédiation)
═══════════════════════════════════════════════════════
Uber a pris les taxis, retiré le dispatching central, mis l'offre et la demande en contact direct.
La valeur cachée : les actifs sous-utilisés (voitures des conducteurs) + l'information (position en temps réel).

Comment appliquer le modèle Uber à {industrie_ciblee} avec des agents IA ?
• Quel est l'"actif sous-utilisé" dans cette industrie ? (l'équivalent des voitures des chauffeurs Uber)
• Quel intermédiaire devient inutile grâce aux agents IA ?
• Comment la marketplace IA fonctionnerait-elle ?
• Avantage compétitif asymétrique : pourquoi les acteurs en place NE PEUVENT PAS répliquer ?
• Modèle de revenus : take rate, abonnement, données ?
• Nom de code de cette stratégie de disruption

═══════════════════════════════════════════════════════
LENS 2 — DISRUPTION AIRBNB (Asset-Sharing + Confiance algorithmique)
═══════════════════════════════════════════════════════
Airbnb a transformé des actifs dormants en actifs productifs via une couche de confiance numérique.
La vraie innovation : résoudre le problème de confiance entre inconnus à l'échelle mondiale.

Comment appliquer le modèle Airbnb à {industrie_ciblee} avec des agents IA ?
• Quels actifs dorment dans cette industrie (compétences, données, infrastructure, relations) ?
• Comment les agents IA créent-ils la couche de confiance nécessaire ?
• Quel "système de réputation" les agents IA peuvent-ils construire ?
• Pourquoi l'économie de partage n'a pas encore touché ce secteur ?
• Avantage compétitif asymétrique
• Nom de code de cette stratégie de disruption

═══════════════════════════════════════════════════════
LENS 3 — DISRUPTION SPOTIFY (Abonnement + Algorithme + Découverte)
═══════════════════════════════════════════════════════
Spotify a transformé la propriété (acheter un CD) en accès (stream), puis a créé de la valeur via la découverte algorithmique.
La vraie innovation : Discover Weekly — un algorithme qui te connaît mieux que toi-même.

Comment appliquer le modèle Spotify à {industrie_ciblee} avec des agents IA ?
• Qu'est-ce qui est aujourd'hui "acheté" et devrait être "streamé / accédé" ?
• Quel est le "Discover Weekly" de cette industrie ? (la découverte personnalisée que personne ne propose encore)
• Comment les agents IA personnalisent-ils l'expérience à l'échelle de 1 ?
• Modèle d'abonnement : tiers, pricing, ce qui est inclus
• Avantage compétitif asymétrique
• Nom de code de cette stratégie de disruption

═══════════════════════════════════════════════════════
LENS 4 — DISRUPTION NETFLIX (Contenu propriétaire + Données comportementales)
═══════════════════════════════════════════════════════
Netflix est passé de distributeur à producteur grâce aux données. House of Cards n'a pas été créé par instinct créatif — il a été calculé par les données de 30 millions d'abonnés.

Comment appliquer le modèle Netflix à {industrie_ciblee} avec des agents IA ?
• Quelle "propriété intellectuelle" les agents IA peuvent-ils générer dans ce secteur ?
• Quelles données comportementales, inexploitées aujourd'hui, révèlent ce que veulent vraiment les clients ?
• Comment passer de "distributeur" à "créateur" grâce aux agents IA ?
• Barrière à l'entrée créée : pourquoi les données accumulées deviennent inimitables ?
• Avantage compétitif asymétrique
• Nom de code de cette stratégie de disruption

═══════════════════════════════════════════════════════
LENS 5 — DISRUPTION APPLE (Écosystème + Lock-in + Premium)
═══════════════════════════════════════════════════════
Apple ne vend pas des produits — elle vend une identité et un écosystème dont sortir est douloureux.
La vraie innovation : rendre le lock-in désirable. Les gens ne veulent pas partir.

Comment appliquer le modèle Apple à {industrie_ciblee} avec des agents IA ?
• Quel "écosystème d'agents" créerait des switching costs naturels ?
• Comment rendre l'intégration entre agents si fluide que quitter coûte trop cher ?
• Quelle identité/statut peut-on vendre (pas juste un outil) ?
• Comment justifier un premium de 30-50% sur le marché ?
• Avantage compétitif asymétrique
• Nom de code de cette stratégie de disruption

═══════════════════════════════════════════════════════
SYNTHÈSE — LES 3 STRATÉGIES DE DISRUPTION RETENUES
═══════════════════════════════════════════════════════
Parmi les 5 lens, sélectionne les 3 qui sont les plus viables pour {ENTREPRISE} dans {industrie_ciblee}.

Pour chaque stratégie retenue :
🎯 STRATÉGIE [NOM] :
   → Résumé en 2 phrases
   → Pourquoi {ENTREPRISE} est positionnée pour gagner
   → Première étape concrète (dans les 30 jours)
   → Risque principal à surveiller
   → Métrique de validation : "On sait qu'on a raison si ___ arrive dans 6 mois"

VERDICT FINAL : "La disruption la plus asymétrique que {ENTREPRISE} peut lancer dans {industrie_ciblee} est _____.
Les acteurs en place ne peuvent pas riposter parce que _____."

Sois impitoyable dans l'analyse. La politesse n'a pas sa place ici."""

    print("\n" + "═" * 60)
    print(f"  DISRUPTION CRÉATIVE : {industrie_ciblee.upper()}")
    print("  5 modèles légendaires × agents IA = chaos créatif.")
    print("═" * 60 + "\n")

    contenu = streamer(prompt)
    chemin = sauvegarder("disruption_creative", contenu)
    print(f"\n  Rapport sauvegardé : {chemin}")
    return contenu


# ─────────────────────────────────────────────
# Agent 5 – Manifeste d'Entreprise
# ─────────────────────────────────────────────

def agent_manifeste_entreprise() -> str:
    """Rédige le manifeste radical de l'entreprise — pas une mission statement, un cri de guerre."""
    incrementer_stat("agent_manifeste_entreprise")

    prompt = f"""Tu es la voix de {ENTREPRISE}.
Non pas un copywriter, non pas un consultant en branding. La voix profonde de l'entreprise — celle qu'on entend quand on se demande pourquoi on se lève le matin.

Ta mission : écrire le MANIFESTE de {ENTREPRISE}.

Pas une page "À propos". Pas une mission statement corporate et tiède.
Un MANIFESTE. Comme les 95 thèses de Luther. Comme le Manifeste Communiste. Comme "Think Different" d'Apple. Comme la lettre de Patagonia "La Terre est notre seul actionnaire".
Un texte qui fait quelque chose aux gens. Qui divise. Qui inspire. Qui recrute.

Contexte : {ENTREPRISE} construit {DOMAINE} — des systèmes d'agents IA autonomes qui transforment la façon dont les entreprises opèrent.

═══════════════════════════════════════════════════════
I. LE PROBLÈME QUE NOUS COMBATTONS
(Ce qui ne va pas dans le monde actuel — sans pitié)
═══════════════════════════════════════════════════════
Commence par le diagnostic radical. Qu'est-ce qui est cassé, absurde, inacceptable dans la façon dont les entreprises fonctionnent aujourd'hui ?
Ne sois pas gentil. Les grandes choses commencent par un "NON" retentissant.

Exemple de ton : "Des milliers d'heures de travail humain sont englouties chaque jour dans des tâches que des machines pourraient faire pendant que les humains dorment. Nous appelons ça de la productivité. Nous appelons ça normal. Nous appelons ça travailler. C'est une catastrophe silencieuse."

Écris 3-4 paragraphes qui nomment le problème avec précision et indignation.

═══════════════════════════════════════════════════════
II. LE FUTUR QUE NOUS CONSTRUISONS
(La vision — concrète, audacieuse, visualisable)
═══════════════════════════════════════════════════════
Pas "un monde meilleur". Une image précise du monde dans 10 ans si {ENTREPRISE} gagne.
Qui vit différemment ? Comment ? Qu'est-ce qui a disparu ? Qu'est-ce qui est apparu ?

Écris 3-4 paragraphes qui font voir ce futur comme si c'était déjà vrai.

═══════════════════════════════════════════════════════
III. NOS CROYANCES RADICALES
(Ce qu'on croit que le monde de l'IA doit entendre)
═══════════════════════════════════════════════════════
Une liste de 7 croyances. Chaque croyance doit :
- Commencer par "Nous croyons que..."
- Être provocatrice (pas évidente, sinon ce n'est pas une croyance, c'est un consensus)
- Être prête à être débattue et contestée
- Dire quelque chose que les concurrents n'oseraient pas dire

Ex : "Nous croyons que la plupart des réunions d'entreprise sont une forme subtile de violence faite au temps humain."

═══════════════════════════════════════════════════════
IV. CE QUE NOUS REFUSONS
(Les lignes rouges — ce qui définit qui on n'est pas)
═══════════════════════════════════════════════════════
Une entreprise qui dit oui à tout est une entreprise sans âme.
Liste 5 refus absolus. Chaque refus commence par "Nous refusons de..."
Ces refus doivent nous différencier concrètement des concurrents.
Certains nous feront perdre des clients. C'est le but.

═══════════════════════════════════════════════════════
V. NOS PROMESSES
(Trois promesses, trois audiences)
═══════════════════════════════════════════════════════
PROMESSE À NOS CLIENTS :
Une phrase. Pas un SLA — une promesse humaine. Ce qu'on leur doit fondamentalement.

PROMESSE À NOTRE ÉQUIPE :
Une phrase. Ce que rejoindre {ENTREPRISE} signifie vraiment pour leur vie.

PROMESSE À LA SOCIÉTÉ :
Une phrase. Notre responsabilité envers le monde au-delà du business.

═══════════════════════════════════════════════════════
VI. LE CRI DE RALLIEMENT
(Une ligne. Celle qu'on grave au mur.)
═══════════════════════════════════════════════════════
Une seule ligne. Pas un slogan publicitaire — un cri de guerre.
Cette ligne doit :
- Pouvoir être criée lors d'un rassemblement
- Résumer tout ce qui précède en moins de 10 mots
- Faire ressentir quelque chose dans la poitrine

Propose 3 options et indique laquelle tu choisirais et pourquoi.

═══════════════════════════════════════════════════════
NOTE DE TON :
═══════════════════════════════════════════════════════
• Rédige en français contemporain, direct, sans jargon corporate
• Alterne phrases courtes (impact) et longues (nuance)
• Tutoie le lecteur par moments — on s'adresse à des humains, pas à des organigrammes
• Le manifeste doit être lisible à voix haute sans honte
• Il doit inspirer autant qu'il provoque
• Il doit donner envie de rejoindre la révolution OU de la combattre — pas rester indifférent

Ce manifeste sera affiché sur nos murs, lu lors des onboardings, envoyé à chaque nouveau client.
Il durera 10 ans. Écris-le en conséquence."""

    print("\n" + "═" * 60)
    print("  RÉDACTION DU MANIFESTE D'ENTREPRISE...")
    print("  Cherchons la voix qui fait lever les gens.")
    print("═" * 60 + "\n")

    contenu = streamer(prompt)
    chemin = sauvegarder("manifeste_entreprise", contenu)
    print(f"\n  Manifeste sauvegardé : {chemin}")
    return contenu


# ─────────────────────────────────────────────
# Interface principale
# ─────────────────────────────────────────────

def afficher_menu():
    """Affiche le menu principal du moteur d'innovation radicale."""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "MOTEUR D'INNOVATION RADICALE" + " " * 20 + "║")
    print("║" + " " * 6 + f"{ENTREPRISE}" + " " * (52 - len(ENTREPRISE)) + "║")
    print("╠" + "═" * 58 + "╣")
    print("║  1. Brainstorm Quantique      (5 frameworks, 25 idées)  ║")
    print("║  2. Constructeur de Futurs    (4 scénarios Shell)       ║")
    print("║  3. Produit Futuriste         (3 inventions JTBD)       ║")
    print("║  4. Disruption Créative       (5 modèles légendaires)   ║")
    print("║  5. Manifeste d'Entreprise    (le cri de ralliement)    ║")
    print("║  0. Quitter                                             ║")
    print("╚" + "═" * 58 + "╝")
    print("  Choix : ", end="")


def main():
    """Point d'entrée principal — boucle interactive du moteur d'innovation."""
    print("\n" + "═" * 60)
    print("  BIENVENUE DANS LE MOTEUR D'INNOVATION RADICALE")
    print("  Où l'impossible devient une roadmap produit.")
    print("  Powered by Gemini 2.0 Flash — All boldness enabled.")
    print("═" * 60)

    while True:
        afficher_menu()
        choix = input().strip()

        if choix == "0":
            print("\n  L'avenir appartient à ceux qui le construisent. À bientôt.\n")
            break

        elif choix == "1":
            print("\n  ─── BRAINSTORM QUANTIQUE ───")
            probleme = input("  Problème à résoudre : ").strip()
            if not probleme:
                print("  Erreur : le problème est requis.")
                continue
            contraintes = input("  Contraintes (budget, délai, tech, équipe — ou 'aucune') : ").strip()
            if not contraintes:
                contraintes = "aucune contrainte définie"
            agent_brainstorm_quantique(probleme, contraintes)

        elif choix == "2":
            print("\n  ─── CONSTRUCTEUR DE FUTURS ───")
            print("  Horizons suggérés : 5, 10, 15, 20 ans")
            horizon_str = input("  Horizon en années : ").strip()
            try:
                horizon = int(horizon_str)
                if horizon <= 0:
                    raise ValueError
            except ValueError:
                print("  Erreur : entrez un nombre entier positif.")
                continue
            agent_constructeur_futurs(horizon)

        elif choix == "3":
            print("\n  ─── PRODUIT FUTURISTE ───")
            print("  Exemples : 'la solitude des managers', 'la peur de décider vite',")
            print("             'perdre le fil dans des projets trop complexes'")
            besoin = input("  Besoin latent à explorer : ").strip()
            if not besoin:
                print("  Erreur : le besoin latent est requis.")
                continue
            agent_produit_futuriste(besoin)

        elif choix == "4":
            print("\n  ─── DISRUPTION CRÉATIVE ───")
            print("  Exemples : Conseil en management, RH & Recrutement, Assurance,")
            print("             Comptabilité, Logistique, Formation professionnelle")
            industrie = input("  Industrie à disrupter : ").strip()
            if not industrie:
                print("  Erreur : l'industrie cible est requise.")
                continue
            agent_disruption_creative(industrie)

        elif choix == "5":
            print("\n  ─── MANIFESTE D'ENTREPRISE ───")
            print("  Aucun paramètre requis. Préparons le cri de ralliement.")
            agent_manifeste_entreprise()

        else:
            print("\n  Choix invalide. Entrez un chiffre entre 0 et 5.")

        input("\n  [Appuyez sur Entrée pour revenir au menu]")


if __name__ == "__main__":
    main()
