---
name: debat
description: Orchestre le PARCOURS 2 du CODEX (une décision engageante — dépendance, fonctionnalité, prix, opportunité, protocole). À invoquer AVANT toute recommandation sur une décision qui engage. Lance POUR et CONTRE en parallèle, puis simulateur → arbitre → vérificateur → A-DECIDER, et laisse Chaima décider.
---

# Skill : debat (parcours 2 du CODEX)

Une décision engageante se présente. Ce skill garantit qu'on ne « gagne » pas un débat, qu'on l'arbitre — le désaccord réel est la seule information utile.

## Séquence obligatoire (aucune étape sautée, surtout pour une idée « évidente »)
1. **POUR + CONTRE en parallèle, dans un seul message.** `avocat` (POUR, sourcé) ET `contradicteur` (CONTRE, permanent) EN MÊME TEMPS. Les lancer l'un après l'autre détruit le désaccord.
2. **simulateur-scenarios** — optimiste / réaliste / pessimiste. Jamais de pourcentage.
3. **arbitre-expert** — UNE recommandation ; dit ce que CHAQUE camp a gagné ; recommande, n'exécute jamais.
4. **verificateur-verite** — source datée, sinon « NON VÉRIFIÉ ».
5. **Consigner dans /codex/A-DECIDER.md** puis **Chaima décide** (§10).

## Règle de désaccord (§14)
Quand deux agents se contredisent et que les faits ne départagent pas : **le verdict le plus prudent gagne par défaut.**

## Sortie — bloc de passation (§14)
    DE : arbitre-expert            POUR : CHAIMA
    OBJET : [une phrase décidable]
    VERDICT : [mot du §13]
    PARCE QUE : [fait porteur — fichier:ligne ou source datée]
    NON VÉRIFIÉ : [ce qui n'a pas pu être établi, ou « rien »]
    CE QUI CHANGERAIT MON AVIS : [le fait précis]

## NOTE D'INSTALLATION (2026-09-11)
Les agents référencés (`avocat`, `contradicteur`, `simulateur-scenarios`, `arbitre-expert`, `verificateur-verite`) font partie des 21 rôles CODEX **pas encore créés** dans ce dépôt (décision transverse parquée, voir /codex/A-DECIDER.md). En attendant, appliquer la séquence manuellement, en une passe, sans sauter le CONTRE — au besoin via des sous-agents.
