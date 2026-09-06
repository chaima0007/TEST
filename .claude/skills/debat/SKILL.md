---
name: debat
description: Orchestre le Parcours 2 du Protocole Codex — décision engageante (dépendance, fonctionnalité, prix, opportunité, protocole). Lance avocat + contradicteur EN PARALLÈLE, puis simulateur, arbitre, vérificateur, et inscrit la ligne dans /codex/A-DECIDER.md. Chaima décide.
---

# /debat — Parcours 2 : une décision engageante

Entrée : la décision à examiner, formulée en une phrase décidable (une action précise, pas un
thème). Si l'argument reçu est un thème, reformule-le en action avant de commencer.

## Déroulé — aucune étape sautée, même pour une idée qui semble évidente

1. **avocat + contradicteur EN PARALLÈLE, dans un seul message** (deux appels d'agent dans le
   même bloc). Jamais l'un après l'autre : lancés séquentiellement, le second répond au
   premier, les positions convergent et le désaccord réel — la seule information utile du
   débat — disparaît. Chacun reçoit la décision et le contexte, pas la sortie de l'autre.
2. **simulateur-scenarios** : reçoit les deux plaidoiries, rend optimiste / réaliste /
   pessimiste. Jamais de pourcentage.
3. **arbitre-expert** : reçoit tout, rend UNE recommandation claire, dit ce que chaque camp a
   gagné ; l'objection la plus forte du contradicteur obtient gain de cause ou un garde-fou
   concret. Recommande, n'exécute jamais.
4. **verificateur-verite** : passe la recommandation au crible du §13 — source datée ou
   NON VÉRIFIÉ, CONFIRMÉ vs PLAUSIBLE, pas de pourcentage, vigilance sur les affirmations
   « sur nous ».
5. **Inscription dans `/codex/A-DECIDER.md`** (via cartographe ou directement) :
   `| Quoi | Projet | Type | En attente depuis [date du jour] | Résumé en 1 ligne |`
6. **Fin.** Chaima décide. La skill ne déclenche JAMAIS l'exécution de la décision — pas de
   merge, pas de dépense, pas d'envoi à un tiers (§10). La ligne ne sort d'A-DECIDER qu'avec
   un TRANCHÉ PAR CHAIMA daté.

## Règles transverses

- Chaque agent termine par le bloc de passation du §14 ; exige-le, il porte « NON VÉRIFIÉ »
  et « CE QUI CHANGERAIT MON AVIS ».
- Désaccord non départagé par les faits : le verdict le plus prudent gagne par défaut.
- Restitution finale à Chaima : la recommandation, l'objection la plus forte et son garde-fou,
  les trois scénarios en une ligne chacun, et la ligne A-DECIDER ajoutée. Court et décidable.
