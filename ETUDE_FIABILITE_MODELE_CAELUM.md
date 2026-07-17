# Étude approfondie — Marché, fiabilité technique des agents & solidité du modèle économique (Caelum)

> Étude fiable et sourcée. Revue : 2026-06-29. **Honnêteté radicale assumée** : les estimations de marché
> varient selon les cabinets (périmètres différents) — on donne des **fourchettes**, pas un chiffre unique ;
> nos « agents » et « simulations » sont décrits tels qu'ils sont réellement (LLM + protocoles déterministes
> + supervision humaine), sans survente.

---

## 0. Résumé exécutif (le verdict)

- **Marché** : porteur et tiré par la loi. RegTech Europe estimé entre **~3,5 et ~14 Md$ en 2024-2025** selon le périmètre, avec une croissance **~15–20 %/an** sur la plupart des sources. En Belgique, l'e-facturation B2B obligatoire depuis le **01/01/2026** touche **~1,2 million d'entreprises** assujetties à la TVA. La demande est **créée par la réglementation**, pas à inventer.
- **Fiabilité technique des agents** : nos agents reposent sur des LLM (probabilistes) **encadrés** par des protocoles déterministes (audits de sources, références légales, sceaux) et une **supervision humaine**. C'est précisément l'architecture que la littérature 2025-2026 recommande pour fiabiliser l'IA agentique. Limite réelle et assumée : un LLM peut halluciner ; notre garde-fou = **sourçage officiel tier1 + contrôle humain avant livraison**.
- **Modèle économique** : modèle SaaS récurrent + services, à **forte marge brute** (cible 75–85 %, cohérente avec les benchmarks). La solidité dépend de 3 leviers : récurrence (NRR), efficacité d'acquisition (CAC payback) et le **canal fiduciaires** (effet de levier). Le risque n°1 n'est pas le marché mais l'**exécution commerciale**.

**Verdict** : modèle **solide et défendable**, sur un marché en croissance structurelle, à condition de tenir les unit economics et de transformer le canal fiduciaires en moteur. La fiabilité technique est **maîtrisable** car on ne confie jamais la décision finale à un LLM seul.

---

## 1. VOLET 1 — Étude de marché

### 1.1 Taille & croissance (RegTech Europe) — fourchette honnête
Les cabinets divergent (périmètres « finance only » vs « compliance large ») :

| Source | Valeur (année) | Projection | CAGR |
|---|---|---|---|
| Research & Markets | 3,55 Md$ (2024) | 13,10 Md$ (2031) | **20,2 %** |
| Research & Markets (autre rapport) | 4,59 Md$ (2024) | 9,38 Md$ (2029) | 15,3 % |
| OMR Global | 2,19 Md$ (2025) | 9,06 Md$ (2035) | 15,3 % |
| MarkNtel | 14,32 Md$ (2025) | 19,27 Md$ (2032) | 4,3 % |
| Fortune Business Insights (Europe) | 5,87 Md$ (2025) | — | ~20 % (monde) |

**Lecture** : quel que soit le chiffre, la tendance est **haussière et durable**. Moteurs convergents (toutes sources) : complexité réglementaire croissante, supervision « continue » des régulateurs, bascule cloud/SaaS, et surtout **gouvernance ESG/CSRD = segment applicatif le plus dynamique (~23,5 % CAGR)**. Les **PME** sont le segment qui croît le plus vite (~25 % CAGR) — cœur de cible de Caelum.

### 1.2 Le marché belge (notre terrain)
- **~1,2 million d'entreprises** assujetties TVA concernées par l'e-facturation B2B obligatoire depuis le 01/01/2026 (SPF Économie).
- Adoption fulgurante : **25 millions** de factures Peppol en janvier 2026 (vs 900 000 en février 2025) ; **~1 million** d'entreprises inscrites Peppol ; **>95 %** prêtes selon la FEB (fin de tolérance le 31/03/2026).
- Gain reconnu : **jusqu'à ~9 €/facture** économisés (FEB).
- **Asymétrie régionale** = opportunité : Flandre ~68 % des Peppol-ID, Wallonie ~22 %, Bruxelles ~9 % → fort potentiel de rattrapage en Wallonie/Bruxelles (terrain de Caelum).
- Déficit d'information = opportunité conseil : **54 %** des entrepreneurs ignoraient la déductibilité fiscale à 120 % liée (enquête Lucy).

### 1.3 Demande au-delà de l'e-facture
L'e-facture est le **produit d'appel**. La vraie demande récurrente vient de l'**empilement** : RGPD, NIS2, DORA, CSRD, CBAM, transparence salariale, UBO… chacun avec échéance et sanction. C'est ce qui justifie un **abonnement** (veille + mise à jour) plutôt qu'une prestation one-shot.

### 1.4 Concurrence & différenciation
Le marché est **fragmenté et mono-sujet** (un outil e-facture OU RGPD OU cyber). Différenciation Caelum :
1. **Agrégation** multi-normes en un point.
2. **Traçabilité** (sources officielles tier1).
3. **Conformité finançable** (obligation ↔ aide publique) — rare.
4. **Canal fiduciaires** marque blanche (levier).

### 1.5 Fenêtre de tir
2026-2027 = pic d'échéances (e-facture passée, CSRD/transparence/PPWR/CBAM à venir). La fenêtre est **maintenant**.

---

## 2. VOLET 2 — Fiabilité technique des agents

### 2.1 Ce que sont réellement nos « agents » (sans survente)
Trois couches :
1. **LLM (probabiliste)** — pour la recherche, la rédaction, l'analyse. Puissant mais faillible (hallucination).
2. **Protocoles déterministes (code)** — audits de références légales, contrôle de confiance des sources (tier1), sceaux de décision, détection de doublons, capteurs (sources mortes, fraîcheur juridique), plateforme autonome. **Reproductibles, non probabilistes.**
3. **Supervision humaine (HITL)** — rien n'est livré sans validation humaine.

> ⚠️ Honnêteté : nos « simulations » (plateforme autonome, Monte Carlo) sont des **modèles locaux**, pas des appels réseau réels ; les volumes affichés sont **recomptés** depuis le dépôt, jamais inventés.

### 2.2 Ce que dit la littérature 2025-2026 (et où on se situe)
- **L'accuracy seule ne suffit pas.** Le framework **CLEAR** (arXiv 2511.14136) impose 5 axes : Coût, Latence, Efficacité, Assurance, Fiabilité. Constat clé : la performance d'un agent peut chuter de **60 % (1 run) à 25 % (cohérence sur 8 runs)**, et il existe un **écart labo→production de ~37 %**.
- **La fiabilité est multi-dimensionnelle** (« Science of AI agent reliability ») : *consistance, robustesse, prédictibilité, sûreté*.
- **HITL indispensable** pour les décisions à enjeu (AWS) ; **77 % des dirigeants** citent la **confiance** (pas l'adoption) comme premier frein à l'IA (Accenture, via Kore.ai).
- **Évaluation = code + modèle + humain** (Dynatrace).

**Notre positionnement** : on adresse le risque exactement comme recommandé — on ne laisse **jamais** un LLM décider seul ; la couche déterministe + l'humain bornent la sévérité des erreurs (axe « safety/assurance »).

### 2.3 Forces de fiabilité (réelles, dans le dépôt)
- **Groundedness** : chaque réponse renvoie à une **source officielle tier1** (audit `source_trust_protocol` : 0 source hors tier1) et à une **loi concrète** (`loi_reference_audit` : 100 %).
- **Garde-fous** : anti-doublon sémantique, sceaux de décision, garde de branche, capteurs (sources mortes, fraîcheur), plateforme autonome (autonomie système 100 %).
- **Sûreté applicative** : limites de payload, fallback 502, zéro secret dans le code.
- **Traçabilité & dates** de vérification sur chaque fiche.

### 2.4 Limites assumées & plan de fiabilisation
| Limite réelle | Mitigation en place | À renforcer |
|---|---|---|
| Hallucination LLM | Sourçage tier1 + contrôle humain | Jeu de tests « golden » + LLM-as-judge |
| Consistance (variance entre runs) | Protocoles déterministes pour les décisions | Mesure pass@k sur les tâches critiques |
| Écart labo→prod | Audits pré-commit (hook) | Indicateurs de prod (latence, taux d'erreur réels) |
| Sources qui changent | Capteur de santé des sources + veille | Exécution planifiée en réseau ouvert |

**Conclusion volet 2** : la fiabilité n'est pas « parfaite » (aucun système agentique ne l'est) mais elle est **architecturalement maîtrisée** : la décision finale reste humaine et chaque sortie est ancrée sur une source vérifiable. C'est le bon design pour un domaine à enjeu juridique.

---

## 3. VOLET 3 — Solidité du modèle économique

### 3.1 Structure de revenus
Produit d'appel (e-facture) → **abonnement récurrent** (veille + conformité, le cœur) → **services/projets** (marge) → **canal fiduciaires** (marque blanche, levier). Modèle **hybride** (récurrent + services), réputé le plus robuste pour la rétention.

### 3.2 Unit economics : cibles vs benchmarks 2025-2026
| Indicateur | Benchmark B2B SaaS | Cible Caelum | Commentaire |
|---|---|---|---|
| Marge brute totale | médiane **77 %** (abo 81–85 %) | **75–85 %** | Atteignable (SaaS + conseil outillé) |
| NRR (rétention nette) | médiane **101 %** (top 110–120 %) | viser **>105 %** | Upsell multi-normes = expansion naturelle |
| GRR (rétention brute) | **88–90 %** | viser **>90 %** | Obligation légale = faible churn structurel |
| CAC payback | médiane B2B **8,6 mois** (early-stage ~4,8) | **< 9 mois** | Le canal fiduciaires le réduit fortement |
| New CAC ratio | **2,0 $** S&M / 1 $ ARR | < 1,5 visé | SEO déjà construit = CAC marginal faible |
| LTV:CAC | cible **≥ 3** | **≥ 3** | Récurrence + faible churn aident |
| Rule of 40 | médiane **35–40** (top >50) | viser **>40** | Croissance + efficacité |

### 3.3 Atouts structurels de solidité
1. **Churn naturellement bas** : la conformité est une **obligation continue**, pas un confort → rétention élevée (GRR/NRR).
2. **Expansion intégrée** : chaque nouvelle norme = upsell (NRR > 100 % par construction).
3. **CAC marginal faible** : 577+ pages SEO déjà publiées + pépites virales (compte à rebours, badge) = acquisition organique.
4. **Effet de levier fiduciaires** : 1 cabinet = des dizaines de PME (widget marque blanche).
5. **Marge** : produit logiciel + conseil outillé → marge brute élevée.

### 3.4 Projections (rappel, source : `revenue_simulation_grands_comptes.py`)
ARR médian (Monte Carlo n=100 000) — **projections sous hypothèses, pas des garanties** :
- **Prudent** : 0,29 M€ (An1) → 1,42 (An2) → **3,30 M€** (An3)
- **Base** : 0,58 → 2,83 → **6,88 M€**
- **Ambitieux** : 1,17 → 5,10 → **12,35 M€**
> Le 1ᵉʳ million est franchi **dès l'An 2 même en scénario prudent**.

### 3.5 Risques & robustesse
| Risque | Gravité | Mitigation |
|---|---|---|
| **Exécution commerciale** (le vrai risque) | Élevée | Dates butoirs (roadmap), canal fiduciaires, pépites organiques |
| Dépendance fondatrice (solo) | Élevée | Automatisation supervisée, protocoles documentés, partenaires |
| Banalisation e-facture (commodité) | Moyenne | Pivot vers l'abonnement multi-normes (valeur récurrente) |
| Exigence labels (SOC 2/ISO) grands comptes | Moyenne | Trust Center honnête + roadmap certifications |
| Concurrence d'éditeurs établis | Moyenne | Différenciation « finançable + sourcé + local » |
| Décisions humaines en attente (prix/identité/webhook) | Bloquante court terme | Roadmap datée, prix déjà préparé |

---

## 4. Conclusion & conditions de réussite

**Le modèle est solide** : marché tiré par la loi, churn structurellement bas, marge élevée, différenciation réelle, et une fiabilité technique **architecturalement encadrée** (jamais de LLM décideur seul). Ce n'est pas un pari sur la demande (elle existe, créée par la réglementation) mais sur l'**exécution**.

**3 conditions de réussite :**
1. **Tenir les unit economics** (CAC payback < 9 mois, NRR > 105 %, marge > 77 %).
2. **Activer le canal fiduciaires** (le levier de scalabilité) — widget marque blanche en place.
3. **Décisions fondatrice** (prix → identité → webhook) pour passer en mode acquisition (roadmap datée).

> Sources principales : Research & Markets, MarkNtel, OMR Global, Fortune Business Insights (RegTech) ; SPF Économie, FEB/VBO, Statbel, enquête Lucy (Belgique) ; arXiv 2511.14136 (CLEAR), « Science of AI agent reliability », AWS, Dynatrace, Kore.ai (fiabilité IA) ; Benchmarkit/Baker Tilly, SaaSCan, Maxio, PepperEffect (benchmarks SaaS 2025-2026).
