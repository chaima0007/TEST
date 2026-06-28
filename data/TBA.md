# 📊 Tableau de Bord d'Avancement — Caelum Partners

_Dernière mise à jour : 2026-06-28_

## 🚀 Avancement global de la flotte : **84%**
`█████████████████░░░` 84%

- **La Loi Avec Moi (citoyens)** — `████████░░░░░░` 60%
- **Caelum (entreprises B2B)** — `█████████████░` 95%
- **Infrastructure & Gouvernance (flotte d'agents)** — `█████████████░` 96%

## 🔔 Actions qui t'attendent (Chaima)
- **Activer la capture de leads** — Créer un webhook (Zapier "Catch Hook" ou Make) et coller son URL dans la variable d env LEADS_WEBHOOK_URL de l hébergement. Aucun mot de passe à me donner.
- **Fixer les prix des offres conformité** — Renseigner les montants (Essentiel / Sérénité / Sur-mesure) sur la page /offres-conformite.
- **Renseigner les vrais coûts** — Compléter data/cost_model.json avec les factures réelles (hébergement, domaine, etc.).
- **Déployer les 2 sites séparément** — Guide clé en main prêt: DEPLOIEMENT.md (Vercel, 2 projets séparés, variables d env, webhook leads). Build des 2 apps vérifié. Dis "go déploiement" et je te guide écran par écran.
- **Calibrer les fournisseurs d API** — Renseigner les vrais prix/qualité/latence dans data/governance/api_providers.json pour activer l arbitrage réel.

## La Loi Avec Moi (citoyens) — 60%
`████████████░░░░░░░░` 60%

> **Point de sortie :** 83 domaines / 270 réponses (dont couche UE), 100% lois + sources. Build + 1200 simulations OK (p95<111ms, 0% erreur).

| Tâche | Avancement | Statut |
|---|---|---|
| Base juridique sourcée (domaines + réponses) | `███████████░` 90% | en cours |
| Page « Base juridique » (rendu serveur) | `████████████` 100% | terminé |
| Modèles de documents prêts à l'emploi | `███████████░` 95% | en cours |
| Espace enfants & jeunes / mineurs | `███████████░` 90% | en cours |
| Versions multilingues (NL en premier) | `█░░░░░░░░░░░` 5% | à faire |
| Déploiement & hébergement | `░░░░░░░░░░░░` 0% | bloqué (décision Chaima) |
| Cartographie d'adresses officielles par ville | `░░░░░░░░░░░░` 0% | à faire |
| Pages SEO par domaine (acquisition) | `████████████` 100% | terminé |

- **Base juridique sourcée (domaines + réponses)** → prochaines étapes : Compléter les derniers domaines citoyens (recours administration, premier emploi jeunes, médiation de quartier)
- **Modèles de documents prêts à l'emploi** → prochaines étapes : (option) export PDF mis en page
- **Espace enfants & jeunes / mineurs** → prochaines étapes : Pictos illustrés / version lecture facile
- **Versions multilingues (NL en premier)** → prochaines étapes : Traduction NL des modules prioritaires
- **Déploiement & hébergement** → prochaines étapes : Hébergeur + domaine + NEXT_PUBLIC_SITE_URL
- **Cartographie d'adresses officielles par ville** → prochaines étapes : Trouver une source open-data officielle (jamais d'adresse inventée)

## Caelum (entreprises B2B) — 95%
`███████████████████░` 95%

> **Point de sortie :** Veille conformité 2026 (6 normes sourcées + chiffres), agent « Appels & Financements » et simulateur /appels-projets en ligne. Séparé de La Loi Avec Moi.

| Tâche | Avancement | Statut |
|---|---|---|
| Veille conformité 2026 (normes entreprises) | `██████████░░` 80% | en cours |
| Simulateur « Appels à projets » | `████████████` 100% | terminé |
| Agent « Appels & Financements » | `████████████` 100% | terminé |
| Page « Conformité 2026 » + simulateur « Suis-je concerné ? » | `████████████` 100% | terminé |
| Positionnement commercial & business plan | `████████████` 100% | terminé |
| Pages SEO programmatiques (acquisition) | `████████████` 100% | terminé |
| Capture de leads (simulateur) | `███████████░` 90% | en cours |
| Newsletter de veille (canal possédé) | `███████████░` 90% | en cours |

- **Veille conformité 2026 (normes entreprises)** → prochaines étapes : Ajouter UBO, AML, autres obligations sectorielles
- **Positionnement commercial & business plan** → prochaines étapes : Fixer les prix (décision Chaima)
- **Pages SEO programmatiques (acquisition)** → prochaines étapes : Pages par secteur (longue traîne) quand le trafic le justifiera
- **Capture de leads (simulateur)** → prochaines étapes : Brancher LEADS_WEBHOOK_URL (CRM/Zapier) — décision Chaima
- **Newsletter de veille (canal possédé)** → prochaines étapes : Brancher l envoi réel quand LEADS_WEBHOOK_URL / outil e-mail sera choisi

## Infrastructure & Gouvernance (flotte d'agents) — 96%
`███████████████████░` 96%

> **Point de sortie :** 43 protocoles. Agents incrémental + scalabilité/monitoring intégrés à l'orchestrateur, verdict global OK.

| Tâche | Avancement | Statut |
|---|---|---|
| Protocoles de gouvernance | `███████████░` 90% | en cours |
| Protocole incrémental (P-INCREMENTAL) | `████████████` 100% | terminé |
| Scalabilité & monitoring (P-SCALABILITE) | `███████████░` 95% | en cours |
| Charte d'autonomie (P-AUTONOMIE) | `████████████` 100% | terminé |
| Tableau de Bord d'Avancement (P-TBA) | `████████████` 100% | terminé |
| SEO technique (sitemap + robots) | `███████████░` 95% | en cours |
| Tests de charge & latence | `███████████░` 95% | en cours |

- **Protocoles de gouvernance** → prochaines étapes : Revue périodique
- **Scalabilité & monitoring (P-SCALABILITE)** → prochaines étapes : Renseigner les vrais coûts (décision Chaima)
- **SEO technique (sitemap + robots)** → prochaines étapes : Définir NEXT_PUBLIC_SITE_URL au déploiement (Caelum)
- **Tests de charge & latence** → prochaines étapes : Re-tester sur l hébergement réel après déploiement
