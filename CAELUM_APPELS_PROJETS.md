# Caelum — Répondre aux appels à projets (mon avis)

> Projet **ENTREPRISES (B2B)**. Séparé de La Loi Avec Moi.
> Données sourcées dans `data/caelum/appels_projets.json`.

## 1. D'abord, « appel à projet » = 3 choses différentes

1. **Subventions / financements** (chèques-entreprises Wallonie, VLAIO, Innoviris, Horizon Europe, Digital Europe…) → pour **financer** un projet.
2. **Marchés publics** (e-Procurement, TED) → pour **gagner du chiffre d'affaires** récurrent et crédible.
3. **Service vendable** → aider **tes clients** à faire les deux.

La plupart des gens ne voient que la 1. Le vrai levier est de traiter les 3 avec **un seul moteur**.

## 2. Ma reco (simulation, comme le veut le protocole)

| Option | Revenu rapide | Crédibilité/preuve | Coût | Scalable | Score |
|---|---|---|---|---|---|
| A. Caelum répond pour **se financer** (dogfooding) | moyen | **élevée** | faible | moyen | 7.5 |
| B. Caelum **vend** le service aux clients direct | élevé | faible (pas de preuve) | moyen | élevé | 7.0 |
| **C. Hybride : construire l'agent → l'utiliser sur soi → le vendre** | élevé | **très élevée** | moyen | **élevé** | **9.0** |

**Gagnant : C.** On construit la capacité une fois, on l'éprouve sur Caelum (décrocher un chèque/subvention = **preuve vivante**), puis on la vend : *« on a financé notre propre conformité avec l'argent public — on fait pareil pour vous. »*

## 3. Le « cheat code » que tu n'aurais pas pensé

> **La conformité (ton produit) est désormais un CRITÈRE de sélection des marchés publics.**
> Le RGPD s'applique à **tous** les marchés publics, et la cybersécurité est de plus en plus exigée.
> Donc : **être conforme grâce à Caelum = devenir éligible et mieux noté sur les appels d'offres.**

Tu ne vends plus « de la conformité ». Tu vends **« la clé qui ouvre les marchés publics »**.

## 4. Les autres idées à fort levier

1. **Le combo qui tue : conformité + subvention pour la payer.** *« On vous met aux normes ET on trouve la subvention publique qui finance la mise en conformité. »* No-brainer pour le client.
2. **Bibliothèque de réponses réutilisables.** 80 % d'un dossier est du copier-coller intelligent (références, RGPD, cyber, ESG, CV équipe). L'agent capitalise chaque réponse → chaque dossier suivant est plus rapide.
3. **Go/No-Go automatique AVANT d'écrire.** Le temps se perd sur des appels ingagnables. Un score d'éligibilité × probabilité × montant × effort filtre dès le départ.
4. **Allotissement.** Les gros marchés sont découpés en **lots** pour ouvrir aux PME → viser les lots, pas le marché entier.
5. **Consortiums (UE).** Horizon/Digital Europe exigent souvent des partenaires → un service de **mise en relation** est vendable.
6. **Un seul moteur de veille.** Le même système qui détecte « une norme a changé » détecte « un appel s'est ouvert ». Tu construis l'infra une fois.
7. **Le calendrier = moteur de campagnes.** Chaque date d'ouverture d'appel = une vague marketing programmée.
8. **Honnêteté = crédibilité.** Certains dispositifs ferment en cours d'année (ex. budget épuisé). La veille évite de **promettre du vent** — et c'est précisément ce qui te démarque.

## 5. Risques à connaître (vérifiés, 2026)

- **Innoviris (Bruxelles)** : budget limité, des dispositifs n'acceptent plus de nouvelles demandes en 2026 → vérifier avant de promettre.
- **VLAIO (Flandre)** : réforme 2026, volet conseil recentré sur la cybersécurité.
- **Seuils marchés publics UE revus à la baisse** → plus de marchés publiés sur TED (= plus d'opportunités).

## 6. Ce que je propose de construire (côté Caelum)

1. **Agent « Appels & Financements »** dans le swarm : Veille → Go/No-Go → Rédaction assistée → Suivi.
2. **Simulateur « Quelle aide pour mon projet ? »** : 4 questions (région, taille, secteur, besoin) → liste d'aides + marchés pertinents.
3. **Bibliothèque de réponses** (briques réutilisables) alimentée à chaque dossier.

Dis « go » et je code l'agent + le simulateur (sans toucher à La Loi Avec Moi).
