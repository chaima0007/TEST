---
name: debat
description: Lance le parcours 2 du §8 du PROTOCOLE CODEX (pipeline de décision) sur un sujet — Avocat et Contradicteur plaident indépendamment et EN PARALLÈLE, Simulateur stress-teste les deux, Arbitre-Expert synthétise en intégrant les deux plaidoiries, la fiche part dans /codex/A-DECIDER.md. À utiliser avant toute décision engageante : nouvelle dépendance, nouvelle fonctionnalité, changement de prix, opportunité, changement de protocole.
---

# Parcours 2 du §8 — pipeline de décision

Aucune étape n'est sautée, **même pour une idée évidente**. Une idée évidente qui survit au
débat est une idée solide ; une idée évidente qui n'y survit pas vient d'être évitée.

## Étape 0 — Cadrer

Écris la proposition en **une phrase décidable** : une action précise, pas un thème.
❌ "les tests" → ✅ "ajouter un lanceur de tests et couvrir le parcours d'authentification
avant la prochaine fonctionnalité facturable".
Si la proposition n'est pas décidable, le débat produira du bruit. Cadre d'abord.

## Étape 1 — Plaidoiries indépendantes (EN PARALLÈLE, obligatoire)

Lance `avocat` et `contradicteur` **dans un seul message, en deux appels simultanés**.

C'est la règle la plus importante de tout le pipeline. Lancés l'un après l'autre, le second
répond au premier : les deux positions convergent et le désaccord réel disparaît. Lancés
ensemble, chacun explore son propre terrain, et **c'est l'écart entre les deux qui porte
l'information**.

Donne à chacun exactement le même énoncé et le même contexte. Ne transmets à aucun des deux
la sortie de l'autre.

## Étape 2 — Simulation

Lance `simulateur-scenarios` avec **les deux plaidoiries intégrales**. Il produit les trois
trajectoires, le signal d'alerte précoce à 30 jours, le coût du demi-tour et un niveau de
confiance FAIBLE / MODÉRÉE / ÉLEVÉE — jamais de pourcentage.

## Étape 3 — Arbitrage intégrant les deux camps

Lance `arbitre-expert` avec les trois documents. Son livrable doit contenir, dans l'ordre :

1. **La recommandation unique** : FAIRE / NE PAS FAIRE / FAIRE MAIS RÉDUIT / ATTENDRE
   (avec l'événement précis attendu).
2. **Ce que l'Avocat a gagné** — le ou les points qu'il emporte et qui sont **conservés dans
   la décision finale**.
3. **Ce que le Contradicteur a gagné** — ses objections retenues, et **le garde-fou concret
   qui les traite** dans la décision finale.
4. **Le désaccord irréductible** : l'hypothèse implicite sur laquelle les deux divergent
   vraiment, et comment on saura qui avait raison.
5. **Le plus petit premier pas** réversible.
6. **La condition de révision** : quel fait, observé quand, rouvre la décision.

Un arbitrage qui se contente de donner raison à un camp et d'ignorer l'autre est à refaire :
si le Contradicteur a été écarté sans qu'aucun garde-fou ne reprenne son objection, la
décision n'est pas arbitrée, elle est simplement gagnée.

**Règle du désaccord (§2)** : quand les faits ne départagent pas, le verdict le plus prudent
l'emporte par défaut. S'en écarter exige une justification explicite.

## Étape 4 — Vérité, puis dépôt

Passe la synthèse à `verificateur-verite`. Tout "NON VÉRIFIÉ" ou "FAUX" est signalé dans la
fiche — il n'est pas gommé.

Ajoute la ligne dans `/codex/A-DECIDER.md` (§6) : `Quoi / Projet / Type / En attente depuis
/ Résumé en 1 ligne`, la fiche complète en dessous. Si la décision constitue un jalon,
ajoute-la à `/codex/EVOLUTION.md` (§6.5).

## Ce que le pipeline ne fait jamais (§10)

Il ne décide pas. Il **prépare** la décision de Chaima : rien n'est exécuté, mergé, dépensé,
lancé ni envoyé. Le seul statut qu'un agent peut poser est **PROPOSÉ**.
