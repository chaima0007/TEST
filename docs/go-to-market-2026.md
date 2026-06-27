# CaelumSwarm™ — Plan Go-To-Market 2026

> Positionnement : **Plateforme de conformité et d'audit pour systèmes d'IA** —
> preuve réglementaire automatisée (AI Act + CSDDD 2024/1760 + RGPD) pour
> institutions, hôpitaux et grandes entreprises de l'UE.
>
> Basé à Schaerbeek (Bruxelles) — proximité directe avec l'écosystème décisionnel européen.

---

## 1. Le constat stratégique

| Piste envisagée | Verdict | Raison |
|-----------------|---------|--------|
| Conseil archi multi-agents | Démarrage seulement | Vend du temps, pas scalable |
| Vente de licences modules infra (persistance/observabilité) | ❌ Abandonner | Concurrence open-source gratuite mature (Redis, OTel, Sentry) |
| **Audit & conformité IA (SaaS)** | ✅ **Cœur du business** | Marché captif réglementaire, actifs déjà alignés |

**Pourquoi maintenant :** l'AI Act entre en application par phases 2025→2027. Toute entreprise
UE utilisant de l'IA « à haut risque » (santé, RH, scoring, biométrie) DOIT prouver sa
conformité. Ce n'est pas optionnel — c'est une obligation légale assortie d'amendes
(jusqu'à 7% du CA mondial).

**Notre avantage :** 200+ engines droits humains + sceau de protocole (traçabilité des
décisions) + build guard + observabilité = exactement la matière première d'un service
d'audit de conformité.

---

## 2. Cibles (par ordre de priorité)

### Segment A — Institutions publiques & santé (cœur)
- Hôpitaux et réseaux de soins UE (IA diagnostique = haut risque AI Act)
- Administrations régionales/européennes (Bruxelles = terrain immédiat)
- **Douleur** : obligation de conformité + zéro outillage interne + responsabilité juridique
- **Tier** : Enterprise (990€/mo) → On-premise

### Segment B — Grandes entreprises soumises CSDDD
- Sociétés >1000 employés / >450M€ CA (seuil CSDDD)
- Devoir de vigilance sur chaîne de valeur (droits humains + environnement)
- **Douleur** : reporting CSDDD obligatoire, nos engines couvrent déjà 200+ domaines
- **Tier** : Enterprise → White-Label (4900€/mo) pour les cabinets de conseil revendeurs

### Segment C — PME tech & scale-ups (volume / freemium)
- Startups IA cherchant à se mettre en conformité avant levée de fonds
- **Tier** : Free → Pro (99€/mo), acquisition via contenu + GitHub

---

## 3. Pricing (déjà implémenté dans license_manager_agent.py)

| Tier | Prix | Cible | Levier |
|------|------|-------|--------|
| Free | 0€ | PME découverte | Acquisition, 3 engines |
| Pro | 99€/mo (990€/an) | PME/scale-up | Conversion freemium ~8% |
| Enterprise | 990€/mo (9 900€/an) | Hôpitaux, institutions | SSO, audit RGPD, on-premise |
| White-Label | 4 900€/mo (49 000€/an) | Cabinets revendeurs | Marque blanche, revente |

**Projection mix réaliste an 1** (cf. `--revenue`) :
500 Free + 80 Pro + 12 Enterprise + 2 White-Label = **~29 600€/mo → 355 200€ ARR**

---

## 4. Feuille de route 2026 (trimestrielle)

### T1 2026 — Fondations & crédibilité
- [ ] Finaliser le SaaS MVP (auth, licences signées, 50 engines exposés)
- [ ] Mapping AI Act ↔ engines (quel engine couvre quelle exigence légale)
- [ ] **Partenaire juriste** (conformité = pas qu'un problème de code — voir risques)
- [ ] 3 entretiens découverte avec hôpitaux/institutions bruxelloises

### T2 2026 — Premiers clients payants
- [ ] 5 pilotes Enterprise (gratuit/réduit contre étude de cas)
- [ ] Première étude de cas publiable + certification visée (ISO 27001 en cours)
- [ ] Lancement Pro freemium (ProductHunt, LinkedIn, GitHub)
- [ ] Objectif : 5 000€ MRR

### T3 2026 — Traction
- [ ] Convertir 2 pilotes en Enterprise payants
- [ ] Premier partenaire White-Label (cabinet de conseil)
- [ ] Boucle de referral activée
- [ ] Objectif : 15 000€ MRR

### T4 2026 — Échelle
- [ ] 12+ Enterprise, 80+ Pro
- [ ] Dossier de levée de fonds (si voie VC) OU rentabilité bootstrap
- [ ] Objectif : ~30 000€ MRR (≈355K€ ARR)

---

## 5. Avantages techniques défendables (à NE PAS vendre séparément)

Ces briques restent **internes** — elles crédibilisent notre propre rigueur :
- `decision_seal.py` — sceau de protocole (traçabilité décisionnelle auditable)
- `build_guard.py` — anti-récurrence d'erreurs (qualité industrielle)
- `observability.py` — logs/tracing/métriques (transparence opérationnelle)
- `resilience_engine.py` — stabilité sous charge (retry/circuit-breaker)
- `dependency_scanner.py` — sécurité supply-chain (conformité by design)

---

## 6. Risques & honnêteté (red team)

| Risque | Réalité | Mitigation |
|--------|---------|------------|
| **Conformité ≠ code seul** | Vendre à un hôpital exige certifications, assurance responsabilité, juriste | Partenaire juridique dès T1 |
| **Crédibilité d'un acteur nouveau** | Institutions achètent à des acteurs établis | Pilotes + études de cas + certification |
| **Données des engines** | Scores actuels = synthétiques/démo, pas sources primaires auditées | Sourcer données réelles (ONU, OHCHR, Eurostat) avant vente |
| **AI Act mouvant** | Les exigences précises évoluent encore | Veille réglementaire continue, mapping versionné |
| **Capacité de livraison** | Solo/petite équipe vs promesses entreprise | Cadrer le scope des pilotes, ne pas survendre |

> ⚠️ **Le point le plus important** : la techno est une condition nécessaire mais pas
> suffisante. Le succès dépend autant du juridique, des certifications et de la confiance
> que du code. Ce plan est réaliste **si** ces éléments non-techniques sont traités en parallèle.

---

*Document vivant — à réviser chaque trimestre. Généré dans le cadre du protocole CaelumSwarm™.*
