# Prédictions des matchs — Coupe du Monde 2026

*Escouade de 36 agents (14 collecte, 7 simulation Monte Carlo, 7 intégrité, 7 audit, 1 méta-auditeur), 5 juillet 2026. Chaque simulation = 10 000 matchs simulés en Python (modèle de Poisson + prolongation + tirs au but), code réellement exécuté et vérifié. Données brutes : `donnees/predictions-matchs.json`*

## Tableau des prédictions consolidées

| Match | Vainqueur prédit | Qualification | Victoire 90 min | Score le plus probable | Suspicion trucage |
|---|---|---|---|---|---|
| **Brésil – Norvège** | **Brésil** | **72,7 %** | 59,1 % | **2-1** (10,1 %) | 12/100 (faible) |
| Mexique – Angleterre | Angleterre (à très faible conviction) | ~52 % | 30,9 % (Ang) / 42,1 % (Mex) | 1-1 à 90 min, Ang 2-1 si vainqueur | 10/100 |
| Portugal – Espagne | **Espagne** | ~61 % | 46,6 % | Portugal 0-1 Espagne (12,2 %) | 10/100 |
| USA – Belgique | USA | ~53 % | 40,2 % | 1-1 à 90 min, USA 2-1 si vainqueur | 10/100 |
| **Argentine – Égypte** | **Argentine** | **78,3 %** (le plus sûr) | 64,8 % | 2-0 / 1-0 | 10/100 |
| Suisse – Colombie | Colombie (match le plus serré) | ~53-55 % | 38,4 % | 1-1 à 90 min, Sui 0-1 Col si vainqueur | 8/100 |
| **France – Maroc** (quart) | **France** | ~69 % | 53,9 % | 1-0 (12,4 %) | 12/100 |

Notes du méta-auditeur :
- **MEX-ANG est la seule contradiction frontale du lot** : la simulation donne le Mexique (56,8 %), les bookmakers et Opta donnent l'Angleterre ; l'auditeur s'est ancré sur les marchés. Traiter ce match comme un vrai 50/50 (l'altitude de l'Azteca est peut-être comptée 4 fois).
- Les simulations sont systématiquement plus prudentes que les marchés pour les favoris (biais conservateur connu et documenté).

## Verdict sur l'hypothèse de trucage

**AUCUNE PREUVE DE TRUCAGE.** Les 7 indices de suspicion sont tous faibles (8-12/100). Cotes homogènes entre bookmakers sur les 7 affiches, aucun mouvement de ligne anormal, aucune alerte IBIA/Sportradar/FIFA sur un match précis. Le seul signal réel du tournoi est un scandale de spot-fixing sur cartons jaunes visant 2 joueurs non nommés (sans lien établi avec les 14 sélections analysées) — un risque de micro-manipulation périphérique (un carton acheté), pas de résultats truqués. Les gros flux d'argent pro-USA/pro-Mexique sont de l'argent patriotique du public, l'inverse d'un profil de fix.

## Classement des favoris pour le titre (déduit des probabilités)

1. **France** (déjà en quart, ~69 % de passer en demi)
2. **Argentine** (championne en titre, qualification la plus probable : 78 %)
3. **Espagne** (0 but encaissé en 4 matchs, montée en puissance)
4. **Brésil** (défense d'élite mais absences créatives)
5. Angleterre — 6. Mexique — 7. USA — 8. Colombie — 9. Belgique — 10. Suisse — 11. Maroc — 12. Norvège — 13. Égypte

## Angles morts identifiés (ce qui n'a PAS été couvert)

1. Météo/canicule de juillet et pelouses hybrides — non modélisées (seule l'altitude de l'Azteca l'a été)
2. Arbitres désignés et leur historique — non analysés
3. Suspensions futures (joueurs sous menace de cartons) — non suivies
4. Distances de voyage/récupération — non quantifiées systématiquement
5. Pas de simulation du tableau complet (probabilités de titre = déduction qualitative)
6. Compositions officielles (annoncées ~1h avant le match) — pas de procédure de mise à jour
7. Marchés dérivés (cartons/corners), là où opère le vrai spot-fixing — non surveillés
8. Limites du Poisson indépendant (pas de corrélation de scores, nul sous-estimé)

## Incohérences détectées par le méta-auditeur (transparence totale)

- Meilleur buteur contradictoire entre dossiers (Messi 7, Mbappé 7, Oyarzabal 4 dit « co-meilleur ») — non résolu
- Volume de paris du tournoi : 3 chiffres divergents selon les agents (7,3 / 50 / 60 Md$)
- Uniformité suspecte des verdicts d'audit (7/7 « valide avec réserves ») — possible ancrage sur un gabarit
