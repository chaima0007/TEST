# Note de Divulgation d'Invention — CAE-INV-2025-003

**CONFIDENTIEL — PROPRIÉTÉ EXCLUSIVE CAELUM PARTNERS SPRL**

---

| Champ | Valeur |
|-------|--------|
| **Référence interne** | CAE-INV-2025-003 |
| **Nom commercial** | ComplianceIQ™ |
| **Date de divulgation** | 21 juin 2025 |
| **Inventrice** | Chaima Mhadbi |
| **Titulaire** | Caelum Partners SPRL, Bruxelles, Belgique |

---

## Titre

**Algorithme de scoring composite pondéré multicritères pour la détection et classification automatisée des violations des droits fondamentaux dans les chaînes d'approvisionnement mondiales en conformité avec la directive européenne CSDDD 2024**

---

## Problème Résolu

La directive EU CSDDD 2024 oblige les entreprises (500+ salariés) à identifier les violations droits humains dans leurs chaînes d'approvisionnement. Aucun outil existant ne propose un algorithme standardisé, reproductible et auditables pour convertir des données hétérogènes en score de risque CSDDD-compatible.

---

## Description

**Formule brevetable :**
```
CS = (S1 × 0.30) + (S2 × 0.25) + (S3 × 0.25) + (S4 × 0.20)
IDX = round(CS / 100 × 10, 2)
```

**Innovation spécifique :**
- Pondération empirique calibrée sur corrélation documentée entre sous-dimensions et violations réelles
- 4 sous-dimensions adaptatives par domaine thématique (travail forcé, violence genre, apatridie, etc.)
- Seuils de classification normalisés : critique (CS ≥ 60), élevé (40–59.9), modéré (20–39.9), faible (<20)
- Distribution contrainte 4/2/1/1 garantissant la comparabilité inter-entreprises et inter-vagues d'analyse
- Indice dérivé /10 pour reporting exécutif

**Application CSDDD directe :**
- Chaque entité auditée produit un score ≡ niveau de diligence requise
- Critique → action corrective immédiate requise (article 10 CSDDD)
- Élevé → plan d'action sous 12 mois
- Modéré → surveillance continue
- Faible → conformité acquise

---

## Revendications Préliminaires

1. Algorithme de calcul d'un score de risque droits humains basé sur une formule pondérée à quatre composantes.
2. Application de l'algorithme selon la revendication 1 à la vérification de conformité CSDDD.
3. Procédé de classification automatique en quatre niveaux de risque à partir du score calculé.
4. Distribution contrainte garantissant la représentativité statistique dans un portefeuille d'entités analysées.

---

*Document rédigé le 21 juin 2025 — Caelum Partners SPRL*
