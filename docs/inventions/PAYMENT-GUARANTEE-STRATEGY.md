# Stratégie de Garantie de Paiement — Caelum Partners SPRL

**Inventrice :** Chaima Mhadbi  
**Objectif :** Être payée quoi qu'il arrive — rendre le non-paiement impossible

---

## Principe Fondamental : Paiement = Accès. Pas de Paiement = Pas d'Accès.

La stratégie repose sur **7 couches indépendantes**. Si une couche échoue, la suivante prend le relais.

```
┌─────────────────────────────────────────────────────────┐
│  COUCHE 1 : API KEY / SMART CONTRACT (TECHNIQUE)        │
│  → Clé désactivée si paiement échoue. INSTANTANÉ.       │
├─────────────────────────────────────────────────────────┤
│  COUCHE 2 : PRÉPAIEMENT OBLIGATOIRE                     │
│  → Client paie AVANT d'avoir accès. Toujours.           │
├─────────────────────────────────────────────────────────┤
│  COUCHE 3 : STRIPE/SEPA AUTO-DÉBIT                      │
│  → Débit automatique mensuel. Retry 3 fois si échec.    │
├─────────────────────────────────────────────────────────┤
│  COUCHE 4 : LETTRE DE CRÉDIT (grands comptes)           │
│  → Banque du client garantit le paiement à notre place. │
├─────────────────────────────────────────────────────────┤
│  COUCHE 5 : ASSURANCE CRÉDIT COMMERCIAL                 │
│  → Euler Hermes / Coface couvre 85-95% si impayé.       │
├─────────────────────────────────────────────────────────┤
│  COUCHE 6 : PÉNALITÉS CONTRACTUELLES                    │
│  → 1%/semaine de retard + résiliation immédiate.         │
├─────────────────────────────────────────────────────────┤
│  COUCHE 7 : RECOUVREMENT JUDICIAIRE                     │
│  → Injonction belge (€200, 15j) / UE / WIPO arbitrage.  │
└─────────────────────────────────────────────────────────┘
```

## Modèle SaaS — Le Plus Sûr

Le modèle SaaS est **la meilleure protection contre le non-paiement** car :
- Pas de paiement = pas de clé API = technologie inutilisable
- Le client ne peut pas copier et continuer à utiliser sans payer
- Abonnement mensuel = revenu prévisible + protection continue

### Configuration Stripe (à mettre en place quand Caelum lance)
```
1. Stripe Dashboard → Products → Créer tier Startup/Enterprise/Gov
2. Stripe Billing → Activer auto-retry (3 fois en 7 jours)
3. Stripe Webhook → payment.failed → désactiver API key automatiquement
4. Stripe Dunning → emails automatiques J+1, J+3, J+7 après échec
5. Stripe Connect → paiements Belgique → compte ING/BNP Paribas Fortis
```

### Smart Contract (optionnel, pour clients crypto/international)
```
Polygon Network (frais <€0.01 par transaction)
ERC-20 USDC payments → auto-renew → accès automatique
Zéro intervention manuelle requise
```

## Grille Tarifaire avec Garanties

| Tier | Prix/mois | Paiement | Garantie |
|------|-----------|----------|----------|
| Trial (14j) | €0 | Carte requise dès J1 | Charge auto J+15 |
| Startup | €1,500 | SEPA auto-débit prépayé | Pénalités 1%/sem |
| PME ESG | €5,000 | Virement trimestriel prépayé | LC ou assurance crédit |
| Enterprise | €15,000 | Trimestriel prépayé | LC bancaire obligatoire |
| Gouvernement | €40,000 | Bon de commande + semestriel | Garantie souveraine |

## Recours en Cas d'Impayé

### 1. Belgique — Le Plus Rapide (15 jours, €200)
```
→ e-DÉPÔT : edepot.be
→ Formulaire injonction de payer en ligne
→ Pas d'avocat requis
→ Décision en 15 jours ouvrés
→ Titre exécutoire → huissier → saisie compte
```

### 2. Europe — Injonction Européenne (27 pays)
```
→ Règlement CE 1896/2006
→ Formulaire A en ligne (pas d'avocat <€2000)
→ Exécutoire dans 27 pays UE sans procédure supplémentaire
→ Utilisable si client a des filiales dans plusieurs pays UE
```

### 3. International — WIPO Arbitrage
```
→ wipo.int/amc (Genève)
→ Sentence arbitrale exécutoire dans 170 pays
→ Convention de New York sur la reconnaissance des sentences arbitrales
→ Parfait pour clients USA, Asie, Moyen-Orient
→ Délai : 6-18 mois (vs 3-7 ans tribunaux ordinaires)
```

## Assurance Crédit — À Souscrire Dès Premier Contrat >€10k

| Assureur | Couverture | Contact |
|---------|-----------|---------|
| Euler Hermes (Allianz) | 85-95% créances | eulerhermes.com/be |
| Coface | 80-90% créances | coface.be |
| Atradius | 85-95% créances | atradius.be |

**Coût typique :** 0.2-0.8% du CA couvert/an  
**Ce que ça couvre :** insolvabilité + défaut de paiement prolongé  
**Quand souscrire :** dès le premier contrat Enterprise (€15k+/mois)

## Diversification — Règle des 10%

Aucun client ne peut représenter plus de 10% du CA total.

**Pourquoi :** Si 1 client (10% CA) ne paie pas → perte de 10% → supportable.  
Si 1 client (50% CA) ne paie pas → perte de 50% → catastrophique.

**Objectif :** 50+ clients actifs dans des secteurs variés.  
**Timeline :** 5 clients la première année → 20 à 3 ans → 50+ à 5 ans.

## Résumé — Être Payée Quoi Qu'il Arrive

| Scénario | Protection Active |
|----------|------------------|
| Client oublie de payer | Stripe auto-retry + email automatique |
| Client refuse de payer | Coupure accès API immédiate + pénalités |
| Client fait faillite | Assurance crédit Euler Hermes (85-95%) |
| Client à l'étranger | WIPO arbitrage + Convention New York |
| Grand compte récalcitrant | Lettre de crédit bancaire irrévocable |
| Startup sans cash | Prépaiement obligatoire (jamais de crédit) |
| Tout le reste | Injonction belge €200 → saisie 15 jours |

**Résultat : Caelum ne peut PAS ne pas être payée si ces 7 couches sont en place.**
