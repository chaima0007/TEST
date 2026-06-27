# Rapport de résilience — simulation des incidents

*Généré le 2026-06-27. On rejoue chaque problème connu et on vérifie que la défense tient.*

**Incidents enregistrés : 3 · testés automatiquement : 3 · défenses tenues : 3/3**

## INC-001 — Démarrage figé du conteneur (checkout obsolète)  ✅ défense OK
- **Symptôme :** Au démarrage, le dépôt local est au vieux commit 1699dd9 ; les fichiers récents (data/belgium, scripts, apps) sont absents. Il faut resynchroniser à la main.
- **Cause racine :** Le conteneur d'exécution distant boote sur un instantané épinglé au commit 1699dd9 et ne tire pas automatiquement la dernière version. Le remote, lui, a toujours tout le travail.
- **Solution :** Auto-synchronisation au démarrage : le hook SessionStart exécute scripts/setup-hooks.sh qui fait git fetch + git merge --ff-only sur la branche de travail (fast-forward uniquement, jamais destructif, ignoré si modifications non commitées).
- **Protocole :** P-RESILIENCE : auto-sync au boot + commit/push fréquents (le remote est le filet).
- **Limite honnête :** La cause profonde (instantané épinglé) relève de l'infrastructure managée. Parade fiable côté utilisateur : recréer/rafraîchir l'environnement cloud pour que sa base = dernier commit.
- **Simulation :** Auto-sync présent, ff-only, fetch avec reprises, non bloquant — défense OK.

## INC-002 — Date de vérification figée (faux « date dans le futur »)  ✅ défense OK
- **Symptôme :** Le vérificateur juridique bloquait tout fait daté du jour réel, en disant « date_verification dans le futur ».
- **Cause racine :** La fonction _today() du vérificateur renvoyait une date codée en dur (2026-06-26), inférieure à la date réelle (2026-06-27).
- **Solution :** Utiliser l'horloge réelle (date.today()) + une tolérance de 2 jours absorbant tout décalage de fuseau/horloge.
- **Protocole :** P-SOURCES : la date de vérification suit l'horloge réelle, jamais une constante.
- **Limite honnête :** Aucune ; entièrement sous contrôle.
- **Simulation :** _today()=2026-06-27 (horloge réelle) ; un fait daté du jour passe — défense OK.

## INC-003 — Domaine officiel hors liste blanche  ✅ défense OK
- **Symptôme :** À chaque nouvelle niche, un domaine officiel réel (emploi.belgique.be, mobilit.belgium.be…) était signalé « officiel hors tier1 » et bloquait.
- **Cause racine :** La liste blanche ne contenait pas toutes les bases officielles ; chaque sous-domaine devait être ajouté un par un.
- **Solution :** Ajouter les bases officielles larges (belgique.be, fgov.be…). La correspondance étant par suffixe, tous leurs sous-domaines sont désormais couverts automatiquement.
- **Protocole :** P-CONFIANCE-SOURCES : whitelist par bases officielles (suffixe), pas sous-domaine par sous-domaine.
- **Limite honnête :** Les domaines en .brussels restent ajoutés au cas par cas (extension ouverte au public).
- **Simulation :** Tous les domaines officiels testés sont reconnus tier1 (par suffixe) — défense OK.

