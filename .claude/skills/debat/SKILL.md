---
name: debat
description: Orchestre le PARCOURS 2 du PROTOCOLE CODEX (décision engageante — dépendance, fonctionnalité, prix, opportunité, protocole). Lance Avocat + Contradicteur EN PARALLÈLE, puis Simulateur → Arbitre-Expert → Vérificateur de Vérité, dépose en /codex/A-DECIDER.md pour que Chaima tranche. À utiliser dès qu'une décision engage argent, code poussé, lancement, prix, ou une modif du protocole.
---

# Skill : debat — orchestration du Parcours 2 (§8)

Déclenche-la pour **toute décision engageante**. Ne saute aucune étape, surtout si l'idée « paraît évidente ».

## Séquence obligatoire

1. **Avocat + Contradicteur EN PARALLÈLE — un seul message, deux `Agent` en même temps.**
   > Lancés l'un après l'autre, le second répond au premier : les positions convergent et le désaccord réel — la seule info utile du débat — disparaît. C'est une faute contre le protocole.
   - `Agent(subagent_type: avocat, …)` et `Agent(subagent_type: contradicteur, …)` dans le même tour.

2. **simulateur-scenarios** — optimiste / réaliste / pessimiste. **Jamais de pourcentage.**

3. **arbitre-expert** — UNE recommandation qui dit ce que **chaque camp a gagné**. Toute objection écartée doit être reprise par un **garde-fou explicite**, sinon la décision n'est pas arbitrée, seulement gagnée. L'arbitre **recommande, n'exécute pas**.

4. **verificateur-verite** — passe sur toute la sortie : source datée ou « NON VÉRIFIÉ ». Vigilance max sur les affirmations sur nous.

5. **Dépôt en `/codex/A-DECIDER.md`** (§6) via cartographe → **Chaima tranche** (§10). Statut posé par un agent : au plus **PROPOSÉ** (§13). Rien n'est engagé sans **TRANCHÉ PAR CHAIMA le [date]**.

## Règles dures
- Faits non départageants → **le verdict le plus prudent gagne par défaut** (§14).
- Aucun chiffre inventé, aucune source fabriquée (§10).
- Chaque agent termine par le **bloc de passation §14**.
