# 📊 Tableau de Bord d'Avancement — Caelum Partners

_Dernière mise à jour : 2026-06-28_

## 🚀 Avancement global de la flotte : **88%**
`██████████████████░░` 88%

- **La Loi Avec Moi (citoyens)** — `██████████░░░░` 71%
- **Caelum (entreprises B2B)** — `██████████████` 97%
- **Infrastructure & Gouvernance (flotte d'agents)** — `█████████████░` 96%

## 🔔 Actions qui t'attendent (Chaima)
- **Activer la capture de leads** — Créer un webhook (Zapier "Catch Hook" ou Make) et coller son URL dans la variable d env LEADS_WEBHOOK_URL de l hébergement. Aucun mot de passe à me donner. _(en attente depuis 1 j)_
- **Fixer les prix des offres conformité** — Renseigner les montants (Essentiel / Sérénité / Sur-mesure) sur la page /offres-conformite. _(en attente depuis 1 j)_
- **Renseigner les vrais coûts** — Compléter data/cost_model.json avec les factures réelles (hébergement, domaine, etc.). _(en attente depuis 1 j)_
- **Déployer les 2 sites séparément** — EN ATTENTE : valider d abord la stratégie A→Z (STRATEGIE_LANCEMENT_AZ.md) + cocher la checklist GO/NO-GO. Pas de lancement avant. _(en attente depuis 1 j)_
- **Calibrer les fournisseurs d API** — Renseigner les vrais prix/qualité/latence dans data/governance/api_providers.json pour activer l arbitrage réel. _(en attente depuis 1 j)_

## La Loi Avec Moi (citoyens) — 71%
`██████████████░░░░░░` 71%

> **Point de sortie :** 117 modules / 371 réponses (couverture citoyenne très large), 100% lois + sources. Build OK (193 pages), audits verts.

| Tâche | Avancement | Statut |
|---|---|---|
| Base juridique sourcée (domaines + réponses) | `███████████░` 92% | en cours |
| Page « Base juridique » (rendu serveur) | `████████████` 100% | terminé |
| Modèles de documents prêts à l'emploi | `███████████░` 95% | en cours |
| Espace enfants & jeunes / mineurs | `███████████░` 90% | en cours |
| Versions multilingues (NL en premier) | `█████████░░░` 75% | en cours |
| Déploiement & hébergement | `░░░░░░░░░░░░` 0% | bloqué (décision Chaima) |
| Cartographie d'adresses officielles par ville | `░░░░░░░░░░░░` 0% | à faire |
| Pages SEO par domaine (acquisition) | `████████████` 100% | terminé |
| Pages légales (mentions, confidentialité, accessibilité) | `███████████░` 90% | en cours |

- **Base juridique sourcée (domaines + réponses)** → prochaines étapes : Continuer les domaines citoyens manquants (sécurité sociale détaillée, baux commerciaux, etc.)
- **Modèles de documents prêts à l'emploi** → prochaines étapes : (option) export PDF mis en page
- **Espace enfants & jeunes / mineurs** → prochaines étapes : Pictos illustrés / version lecture facile
- **Versions multilingues (NL en premier)** → prochaines étapes : Poursuivre la traduction NL (familie approfondie) selon le trafic
- **Déploiement & hébergement** → prochaines étapes : Hébergeur + domaine + NEXT_PUBLIC_SITE_URL
- **Cartographie d'adresses officielles par ville** → prochaines étapes : Trouver une source open-data officielle (jamais d'adresse inventée)
- **Pages légales (mentions, confidentialité, accessibilité)** → prochaines étapes : Compléter l identité légale de l éditeur (BCE/TVA/adresse)

## Caelum (entreprises B2B) — 97%
`███████████████████░` 97%

> **Point de sortie :** Veille conformité 2026 (6 normes sourcées + chiffres), agent « Appels & Financements » et simulateur /appels-projets en ligne. Séparé de La Loi Avec Moi.

| Tâche | Avancement | Statut |
|---|---|---|
| Veille conformité 2026 (normes entreprises) | `███████████░` 95% | en cours |
| Simulateur « Appels à projets » | `████████████` 100% | terminé |
| Agent « Appels & Financements » | `████████████` 100% | terminé |
| Page « Conformité 2026 » + simulateur « Suis-je concerné ? » | `████████████` 100% | terminé |
| Positionnement commercial & business plan | `████████████` 100% | terminé |
| Pages SEO programmatiques (acquisition) | `████████████` 100% | terminé |
| Capture de leads (simulateur) | `███████████░` 90% | en cours |
| Newsletter de veille (canal possédé) | `███████████░` 90% | en cours |
| Kit de contenu de lancement (posts + e-mails + FAQ) | `████████████` 100% | terminé |

- **Veille conformité 2026 (normes entreprises)** → prochaines étapes : Veille continue: ajouter les futures obligations dès publication officielle
- **Positionnement commercial & business plan** → prochaines étapes : Fixer les prix (décision Chaima)
- **Pages SEO programmatiques (acquisition)** → prochaines étapes : Pages par secteur (longue traîne) quand le trafic le justifiera
- **Capture de leads (simulateur)** → prochaines étapes : Brancher LEADS_WEBHOOK_URL (CRM/Zapier) — décision Chaima
- **Newsletter de veille (canal possédé)** → prochaines étapes : Brancher l envoi réel quand LEADS_WEBHOOK_URL / outil e-mail sera choisi
- **Kit de contenu de lancement (posts + e-mails + FAQ)** → prochaines étapes : Remplacer les [lien] par les URLs réelles après mise en ligne

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
