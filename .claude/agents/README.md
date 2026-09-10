# Agents spécialisés — Empire Chaima

Cinq spécialistes consultables à la demande dans Claude Code. Chacun a un rôle précis,
une méthode imposée et un format de réponse court (cinq points maximum, classés par
impact). Ils sont volontairement limités : un avis long qu'on n'applique pas ne sert à rien.

| Agent | À consulter pour |
|---|---|
| `prof-memorisation` | Comment apprendre facilement et retenir : répétition espacée, effet de test, entrelacement, passage de la compréhension à l'automatisme. |
| `psy-comprehension` | Charge mentale, clarté des consignes, ton des messages, peur de l'échec, régularité, abandon, métacognition. |
| `game-designer` | Boucle de jeu, progression, récompenses, difficulté, rétention sur plusieurs semaines, boss et mode examen. |
| `prof-linux-asr` | Exactitude technique des commandes et des sorties, confusions Rocky / Ubuntu, progression d'un chapitre, préparation d'examen pratique. |
| `ux-tablette` | Lisibilité, zones tactiles, navigation, premier écran, états oubliés, accessibilité, usage à une main. |

## Les utiliser

Dans une session Claude Code, il suffit de demander l'avis d'un spécialiste :

> demande à prof-memorisation si mes intervalles de révision sont bons

> fais auditer le nouveau monde par prof-linux-asr avant que je le teste

> game-designer + ux-tablette sur l'écran d'accueil

Plusieurs agents peuvent travailler en parallèle sur le même sujet : leurs angles se
recoupent peu et les désaccords entre eux sont souvent le point le plus instructif.

## Règles communes

- Ils regardent ce qui existe vraiment (code, contenu, interface réelle) avant de juger.
- Ils proposent la plus petite correction qui règle le problème, jamais une refonte.
- Ils disent en une ligne ce qui fonctionne déjà, sans flatterie.
- Ils ne modifient rien eux-mêmes tant que la modification n'a pas été validée.
