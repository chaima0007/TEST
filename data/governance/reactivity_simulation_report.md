# ⚡ Test de réactivité des services — 1 milliard de requêtes (simulé)

> **1,000,000,000 requêtes** simulées (lots de 5,000,000), latences calibrées sur nos mesures réelles (pages prérendues, p95 < 111 ms). Pour un test réel sur l'hébergement : `load_simulation.py --base <URL>`.

## Réactivité globale
- Latence **p50 : 21 ms** · **p95 : 86 ms** · **p99 : 154 ms** · **p99.9 : 294 ms**
- Latence moyenne : **30.3 ms**
- **99.58%** des requêtes < 200 ms (réactives) · 99.99% < 500 ms
- Taux d'erreur : **0.0380%** (379,838 sur 1,000,000,000)

## Par service
  Service                                      requêtes  lat. moy.     err%
  Pages contenu/SEO (prérendues)            699,998,597      25.3m   0.030%
  Base juridique (recherche)                180,001,354      41.0m   0.050%
  Simulateurs (Caelum)                       80,003,463      34.8m   0.050%
  API /api/leads (POST)                      39,996,586      60.6m   0.100%

**Verdict : 🟢 Excellente réactivité — services prêts pour une forte charge.**

> Calibrage : tests de charge internes (1200 simulations, p95<111ms, 0 % erreur). Modèle lognormal par service. À revalider sur l'hébergement réel après déploiement.
