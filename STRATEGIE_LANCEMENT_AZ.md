# Stratégie de lancement A → Z (Caelum Partners)

> 🛑 **Règle posée par Chaima : on ne lance RIEN tant que ce plan n'est pas complet et validé.**
> Document de SYNTHÈSE — il consolide les docs existants (liens en §9), ne les répète pas.
> Aucun chiffre inventé ; les montants restent à fixer par Chaima.

## 1. Vision
Deux produits, **un seul moteur** d'intelligence vérifiée :
- 🏛️ **La Loi Avec Moi** (citoyens) — info juridique fiable, sourcée, gratuite → audience + autorité.
- 🏢 **Caelum** (entreprises) — conformité réglementaire en abonnement → revenu récurrent.

## 2. Ce qui est PRÊT ✅
- Contenu : **84 domaines / 272 réponses** (100 % loi réelle + source officielle), couche UE.
- Caelum : entonnoir complet (9 normes, SEO normes+secteurs, simulateur, capture leads, newsletter, offres).
- Technique : 2 apps séparées, **builds vérifiés**, **1200 simulations** (p95 < 111 ms, 0 % erreur), 51 protocoles verts.
- Confiance : pages Transparence/sources, vérification croisée, anti-désync.

## 3. Ce qui MANQUE (le cœur de ton constat) — avec responsable
**🔵 À toi (décisions / comptes — personne d'autre ne peut) :**
| Ressource | Pourquoi | Statut |
|---|---|---|
| Hébergeur + 2 domaines | mettre en ligne | ⛔ |
| Outil e-mail/CRM + webhook (`LEADS_WEBHOOK_URL`) | collecter & nourrir les leads | ⛔ |
| Prix des offres Caelum | facturer | ⛔ |
| Paiement (Stripe) | encaisser en ligne | ⛔ (si vente directe) |
| Coûts réels (`cost_model.json`) | piloter la marge | ⛔ |
| Analytics + Search Console | mesurer & indexer | ⛔ |
| Page/persona LinkedIn (founder-led) | canal d'acquisition n°1 | ⛔ |

**🟢 Moi (flotte — je peux le faire sans toi) :**
| Ressource | Statut |
|---|---|
| Pages légales **La Loi Avec Moi** (mentions, confidentialité/RGPD, accessibilité) | à créer |
| Identité visuelle simple (logo/couleurs cohérents) | à préparer |
| Versions **NL** des modules prioritaires | à faire |
| Kit de lancement (posts LinkedIn, e-mails, FAQ) | à produire |
| Intégration du code analytics (une fois l'outil choisi) | prêt à brancher |

## 4. Stratégie marketing A → Z (unifiée)
*(détail Caelum dans CAELUM_STRATEGIE_MARKETING.md — ici, la vue d'ensemble des 2 projets)*

**A. Attirer (acquisition)**
- SEO : La Loi Avec Moi (≈150 pages) capte le grand public ; Caelum (normes × secteurs) capte l'intention B2B.
- Founder-led LinkedIn (toi) : 2 posts/semaine sur les changements de loi.
- Presse/data : « Baromètre conformité PME » → couverture gratuite.

**B. Convertir**
- Citoyen : aimant = réponses gratuites + modèles → e-mail (newsletter).
- Entreprise : simulateur « Suis-je concerné ? » → e-mail + devis → abonnement.

**C. Fidéliser & étendre**
- Newsletter de veille (produit + canal).
- Renouvellements au rythme du calendrier réglementaire.
- B2B2B : fiduciaires (1 cabinet = ~300 PME).

**D. Garde-fou** : honnêteté = stratégie (dire qui n'est pas concerné, citer les sources).

## 5. Plan de lancement par phases
**Phase 0 — Préparation (avant tout lancement)**
- Moi : pages légales La Loi Avec Moi, identité visuelle, NL prioritaire, kit de contenu.
- Toi : hébergeur+domaines, outil e-mail/CRM, prix, analytics, LinkedIn.

**Phase 1 — Soft launch (silencieux)**
- Déployer les 2 sites (guide `DEPLOIEMENT.md`), brancher leads + analytics, soumettre sitemaps.
- Tester en réel (charge, formulaires) sur quelques utilisateurs.

**Phase 2 — Lancement public & croissance**
- Campagne LinkedIn + presse data ; 1er fiduciaire pilote ; produit d'appel e-facture.
- Suivi MRR, itérations selon les données.

## 6. Budget (posture, sans montant inventé)
Bootstrap + **subventions** (chèques entreprises) pour financer le développement. Coûts maîtrisés par le rendu statique (hébergement faible). Montants réels à compléter dans `cost_model.json`.

## 7. KPIs à suivre dès le jour 1
Trafic organique → leads · taux de capture des simulateurs · ouverture newsletter · leads → devis → clients · **MRR** · CAC vs LTV · % leads via fiduciaires.

## 8. Critères GO / NO-GO (checklist de lancement)
- [ ] 2 sites déployés sur leur domaine
- [ ] Capture de leads active (webhook testé)
- [ ] Pages légales en place (les 2 sites)
- [ ] Analytics + Search Console branchés
- [ ] Prix des offres fixés
- [ ] Kit de contenu prêt (5 posts + 3 e-mails)
- [ ] Test de charge OK sur l'URL réelle
→ **Lancement seulement quand toutes les cases sont cochées.**

## 9. Documents détaillés (consolidés ici)
- Marketing : `CAELUM_STRATEGIE_MARKETING.md` · Logique d'entreprise : `CAELUM_LOGIQUE_ENTREPRISE.md`
- Viabilité : `CAELUM_EVALUATION_VIABILITE_FLOTTE.md` · Revenus : `PLAN_REVENUS.md` · Trafic : `STRATEGIE_TRAFIC.md`
- Niches : `NICHES_OR.md` · Déploiement : `DEPLOIEMENT.md` · Business plan : `BUSINESS_PLAN_GLOBAL.md`

---
**En résumé :** le produit et la technique sont prêts ; il manque surtout des **ressources de lancement** (hébergement, e-mail/CRM, prix, analytics, pages légales, NL, kit de contenu). Ce plan dit qui fait quoi. **Aucun lancement avant que la checklist §8 soit complète.**
