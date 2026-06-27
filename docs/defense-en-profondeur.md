# Défense en profondeur — Pourquoi tu peux être rassuré

> Tu ne fais pas confiance à UN agent. Tu fais confiance à un **système où
> plusieurs gardiens indépendants vérifient tout, à des moments différents.**
> Pour qu'une erreur passe, elle devrait tromper TOUTES les couches à la fois —
> c'est quasi impossible. C'est la méthode des banques et de l'aéronautique.

## Les couches de protection (de la plus tôt à la plus tard)

| # | Quand | Gardien | Ce qu'il bloque |
|---|-------|---------|-----------------|
| 1 | **Avant chaque commit** | hook `pre-commit` | Erreurs de code + incohérences de marque |
| 2 | **Avant chaque envoi (push)** | hook `pre-push` | Collision entre sessions (écrasement) |
| 3 | **Sur GitHub, à chaque changement** | CI `quality-guards` | Build + cohérence + sécurité dépendances |
| 4 | **Avant toute publication (manuel)** | `preflight.py` | Les 4 gardiens d'un coup |
| 5 | **Sur chaque décision importante** | `decision_seal.py` | Décision non validée |
| 6 | **Mémoire des erreurs passées** | `build_guard` + `errors.json` | Toute erreur déjà vue ne se reproduit plus |

## Ce que ça veut dire concrètement

- Une faute de code ? → arrêtée à la couche 1, 3 ou 4.
- Une ancienne marque oubliée ? → arrêtée à la couche 1 ou 3.
- Un écrasement de travail entre sessions ? → arrêté à la couche 2.
- Une faille de sécurité dans une dépendance ? → arrêtée à la couche 3 ou 4.
- Une décision risquée ? → bloquée à la couche 5 si non validée.

## Les gardiens tournent SANS Claude

Les couches 1, 2, 3 sont **automatiques** : elles s'exécutent toutes seules
(au commit, au push, sur GitHub) — même quand aucune session Claude n'est ouverte.
Le contrôle qualité ne s'arrête jamais.

## Comment forcer (si vraiment nécessaire)

Les gardiens peuvent être contournés volontairement (`git commit --no-verify`,
`git push --no-verify`) — mais **uniquement en connaissance de cause**. Par défaut,
rien ne passe sans validation.

---

*Tu peux dormir tranquille : il faudrait une série d'échecs simultanés et indépendants
pour qu'une erreur atteigne la production. C'est ça, la défense en profondeur.*
