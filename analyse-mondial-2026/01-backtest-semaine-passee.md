# Backtest — Coupe du Monde 2026 : la méthode aurait-elle prédit les matchs déjà joués ?

*Analyse multi-agents du 5 juillet 2026. 14 agents (1 inventaire, 12 prédictions aveugles, 1 auditeur). Données brutes : `donnees/backtest-semaine-passee.json`*

## Question posée
Si on avait fait tourner le modèle AVANT chaque match de la semaine passée (16es et huitièmes déjà joués), aurait-on prédit le bon résultat ? Exemple demandé : **Maroc – Canada**.

## Réponse pour Maroc – Canada : OUI pour le vainqueur, NON pour l'ampleur
- Données d'avant-match : Maroc 6e FIFA, invaincu, défense quasi imprenable ; Canada 30e FIFA, attaque gonflée par le 6-0 contre le Qatar, Alphonso Davies hors du onze
- Cotes d'avant-match : Maroc ~69 % de qualification implicite
- **Prédiction aveugle du modèle : victoire Maroc (53,8 % sur 90 min), score 1-0**
- Résultat réel : **Maroc 3-0** → vainqueur correct, score faux (un 3-0 n'avait que ~5,6 % de probabilité)

## Score global du backtest (12 matchs)
| Mesure | Résultat |
|---|---|
| Vainqueur/qualifié correct | **10/12 (83 %)** — 9/12 (75 %) si on juge strictement sur 90 minutes |
| Score exact correct | **2/12 (17 %)** (Canada 1-0 Afrique du Sud, Colombie 1-0 Ghana) |
| Erreurs | Pays-Bas–Maroc et Allemagne–Paraguay — deux nuls 1-1 perdus aux tirs au but |

Détail : aucune prédiction n'a désigné une équipe qui a PERDU son match en 90 minutes. Les deux seules erreurs sont des loteries de tirs au but.

## Les vraies surprises de la semaine
1. **Allemagne éliminée par le Paraguay** (~16 % implicite) — l'upset majeur, mais un événement à 16 % arrive 1 fois sur 6
2. **Pays-Bas–Maroc** — en réalité un quasi 50/50 que le marché sous-cotait (biais de notoriété : le Maroc était classé DEVANT les Pays-Bas au classement FIFA)
3. L'ampleur du Maroc 3-0 Canada (~5,6 % de probabilité)

## Verdict d'honnêteté de l'auditeur (important)
- Les 12 prédictions coïncidaient toutes avec le favori des bookmakers : le backtest valide surtout la stratégie « suivre les cotes dé-margées » ; le modèle n'a jamais divergé du marché, donc **aucun edge propriétaire n'est encore démontré**
- Le 83 % est un plafond obtenu sur des affiches déséquilibrées (espérance ~8/12) : sur les quarts et au-delà, entre équipes proches, la fiabilité réaliste retombe à **55-65 % sur le vainqueur** et **10-15 % sur le score exact**
- Biais rétrospectif identifié et cantonné : les « leçons » des agents sur-ajustent aux résultats connus ; les probabilités elles-mêmes collaient aux cotes d'avant-match, sans gonflement suspect

## Leçons intégrées pour les prédictions à venir
1. Ancrer la probabilité vainqueur sur les cotes dé-margées ; le Poisson sert à distribuer les scores, pas à contredire le marché
2. Dégonfler les stats obtenues contre des adversaires faibles (les 6 buts du Canada vs Qatar ont faussé tous les modèles naïfs)
3. Modéliser explicitement le chemin « nul + tirs au but » : c'est par là que passent les upsets (Maroc, Paraguay)
4. Contre un bloc bas ayant déjà résisté à des grands, décoter agressivement le lambda du favori
5. Quand classement FIFA et cotes divergent, le marché sous-cote peut-être l'outsider (cas Maroc)
6. Toujours donner 3 probabilités séparées : victoire 90 min, qualification, score modal
