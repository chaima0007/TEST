---
name: debat
description: Orchestre le Parcours 2 du PROTOCOLE CODEX — toute décision engageante (dépendance, fonctionnalité, prix, opportunité, protocole). Lance avocat + contradicteur EN PARALLÈLE, puis simulateur, arbitre, vérificateur, et consigne dans A-DECIDER.md pour décision de Chaima.
---

> Généré dérivé du PROTOCOLE CODEX §8.
> Mise à jour 2026-09-11 : les agents appelés ci-dessous (`avocat`, `contradicteur`, `simulateur-scenarios`,
> `arbitre-expert`, `verificateur-verite`, `cartographe`) existent dans `.claude/agents/` au **set canonique**
> de l'Empire — lançables directement comme sous-agents (`/codex/agents-correspondance.md`).

# Skill : débat (Parcours 2)

Déclenche cette procédure pour **toute décision engageante** : ajouter une dépendance,
lancer une fonctionnalité, fixer un prix, retenir une opportunité, modifier le protocole.
**Aucune étape sautée — surtout pour une idée qui semble évidente.**

## Étapes (dans l'ordre)

1. **Avocat + Contradicteur EN PARALLÈLE, dans UN SEUL message.**
   Impératif : les lancer ensemble. Lancés l'un après l'autre, le second répond au premier,
   les positions convergent et le désaccord réel — la seule information utile — disparaît (§8).
2. **simulateur-scenarios** : optimiste / réaliste / pessimiste. Jamais de pourcentage (FAIBLE/MODÉRÉE/ÉLEVÉE).
3. **arbitre-expert** : UNE recommandation. Doit dire **ce que chaque camp a gagné** ; toute
   objection écartée est reprise par un garde-fou explicite (sinon la décision n'est pas
   arbitrée, seulement gagnée).
4. **verificateur-verite** : chaque affirmation = source datée ou « NON VÉRIFIÉ » (§13).
5. **cartographe** : inscrire la décision dans `/codex/A-DECIDER.md` (§6).
6. **CHAIMA décide.** Un agent recommande ; il n'exécute jamais (§10).

## Règles invariantes
- Le contradicteur est **permanent, non désactivable**.
- En cas d'égalité factuelle entre deux agents, **le verdict le plus prudent gagne par défaut** (§14).
- Chaque agent finit par le **bloc de passation §14** (DE/POUR/OBJET/VERDICT/PARCE QUE/NON VÉRIFIÉ/CE QUI CHANGERAIT MON AVIS).
- Rien ne s'engage (merge, argent, envoi, signature, « LANCÉ ») sans Chaima (§10).
