# DOSSIER-02 — ENCAISSEMENT & FACTURE (Belgique)

**ID :** ATLAS-DOSSIER-02 · **Le :** 2026-09-16 · **Par :** `scout` (ATLAS) · **Statut :** PROPOSÉ
**Objet :** 2e volet du blocage n°1 du premier euro (`A-DECIDER.md`, 2026-09-11) — être payée ~500 € par un client professionnel, et facturer conformément. **Options, aucune recommandation** (§10).

## AVERTISSEMENT DE SOURCE — à lire avant toute ligne

**Aucune page officielle n'a pu être ouverte depuis cette session** (403 CONNECT sur les domaines
belges officiels et sur les prestataires de paiement — détail au bloc §14). Tout ce qui suit vient
d'un **résumé d'index** de page officielle, pas de la page : **relais de rang 3 portant du rang 1**,
utile pour savoir **quelle URL ouvrir**, jamais pour conclure. Étiquette : **RELAYÉ (non consulté)**.
Rien ici n'est **VÉRIFIÉ** (§13). **Index consulté le 2026-09-16** ; date des documents eux-mêmes :
**NON VÉRIFIÉ** (page non ouverte).

---

# PARTIE A — La facture conforme

## A1. Mentions obligatoires
Base légale couramment invoquée : AR n° 1 du 29.12.1992, art. 5 → **NON VÉRIFIÉ** (texte non ouvert).

**RELAYÉ (SPF Finances)** — 9 mentions : (1) date d'émission · (2) numéro séquentiel unique ·
(3) nom + adresse du fournisseur · (4) idem du client · (5) numéro de TVA des **deux** ·
(6) description et quantité du service · (7) date de l'opération si ≠ date d'émission ·
(8) base imposable par taux · (9) taux et montant de TVA dû.
**Exhaustivité de cette liste : NON VÉRIFIÉ.**

URL à ouvrir : `finances.belgium.be/fr/entreprises/tva/comptabilite-facturation/comptabilite-facturation`

## A2. Délais

| Quoi | Réponse | Statut |
|---|---|---|
| Émission | au plus tard le **15e jour du mois suivant** la prestation (exceptions selon l'opération) | RELAYÉ (SPF Fin. + SPF Éco.) |
| Conservation | **NON VÉRIFIÉ** — durée non établie, aucun chiffre écrit de mémoire | NON VÉRIFIÉ |
| Paiement | pas de délai légal minimum ; sans clause, le montant est **dû immédiatement** → à fixer dans PACTE | RELAYÉ (SPF Éco.) |

## A3. Si Chaima n'est pas assujettie à la TVA (franchise)

| Point | Réponse | Statut |
|---|---|---|
| Seuil de la franchise | chiffre d'affaires annuel ≤ **25 000 €** | RELAYÉ (SPF Fin.) |
| Facture | sans TVA portée en compte | RELAYÉ |
| **Libellé exact de la mention de franchise** | **NON VÉRIFIÉ** — une formule type existe très probablement ; son libellé n'a pas pu être établi. **Ne pas l'inventer : une mention fausse est pire qu'une mention absente.** | **NON VÉRIFIÉ** |
| Franchise = dispense d'e-facturation ? | **NON** — voir B0 | RELAYÉ |

URL à ouvrir : `finances.belgium.be/fr/entreprises/tva/assujettissement-tva/regime-franchise-taxe`

---

# PARTIE B — Les moyens d'être payée

## B0. E-FACTURATION PEPPOL — **le point potentiellement bloquant**

| Point | Ce que dit la source relayée | Statut |
|---|---|---|
| Obligation | depuis le **01.01.2026**, toute entreprise belge assujettie à la TVA doit **émettre et recevoir** des factures **structurées** (XML/UBL, EN 16931, Peppol BIS) en **B2B** | RELAYÉ (efacture / SPF Fin.) |
| Franchise (≤ 25 000 €) | **également concernée** — présenté comme récemment clarifié | RELAYÉ |
| Exceptions | B2C ; assujetti non établi en Belgique ; opérations exonérées **art. 44** CTVA | RELAYÉ |
| Tolérance | générale (1er trimestre 2026) **terminée** ; ciblée autofacturation jusqu'au **30.06.2026** — **échue** | RELAYÉ |
| **Conséquence** | un **PDF par e-mail** à un client pro belge assujetti **ne suffirait pas** — or l'ICP (consultant/coach indépendant) est exactement ce cas | **PLAUSIBLE** (déduit) |
| Émettre | exige un logiciel raccordé au réseau Peppol | RELAYÉ |
| **Hermes** | outil **gratuit** de l'administration fédérale : **reçoit** les factures Peppol et les renvoie en PDF par e-mail. **Réception seule — ne règle pas l'émission.** | RELAYÉ |
| Coût logiciel · Amendes | **NON VÉRIFIÉ** — aucun tarif ni montant d'amende lu à la source | NON VÉRIFIÉ |

URLs à ouvrir, sur `efacture.belgium.be/fr/` : `article/pour-qui-la-facturation-electronique-deviendra-t-elle-obligatoire` ·
`article/quel-logiciel-puis-je-utiliser-pour-la-facturation-electronique` · `news/fin-de-la-periode-de-tolerance-pour-le-facturation`

## B1-B4. Les canaux d'encaissement

| Moyen | Coût réel | Délai de mise en place | Exigé pour s'inscrire | Risque |
|---|---|---|---|---|
| **Virement SEPA** (IBAN sur la facture) | **NON VÉRIFIÉ** (dépend du contrat bancaire) | immédiat si un compte existe | rien de plus | le client paie quand il veut : écrire le délai au devis (A2) |
| **Compte pro** | **NON VÉRIFIÉ** | **NON VÉRIFIÉ** | **NON VÉRIFIÉ** | **Obligatoire ou non pour une personne physique indépendante : NON VÉRIFIÉ** (page SPF Économie non ouverte) |
| **Paiement en ligne** (Stripe · Mollie · PayPal) | **NON VÉRIFIÉ — aucun tarif lu chez les prestataires (accès refusé)** | **NON VÉRIFIÉ** | **NON VÉRIFIÉ** | commission sur 500 € ; ne dispense **pas** de B0 |
| **E-facturation** | voir B0 | voir B0 | n° BCE + raccordement Peppol | **bloquant** |

---

## À établir, depuis un poste non filtré
Chaque **NON VÉRIFIÉ** ci-dessus, dans l'ordre : B0 (Peppol) → A3 (mention de franchise) → A1
(conservation, exhaustivité) → compte pro (`economie.fgov.be` → Créer une entreprise → « L'ouverture
d'un compte bancaire ») → tarifs (`stripe.com/en-BE/pricing`, `mollie.com/be/pricing`,
`paypal.com/be/webapps/mpp/merchant-fees`).

> **Ce dossier n'est pas un conseil juridique ou comptable. Confirmation par un comptable avant première facture.**

---

    DE : scout (ATLAS)              POUR : CHAIMA
    OBJET : Ouvrir les 6 URLs listées « Ce qui reste à établir » depuis un poste non filtré, en commençant par l'obligation Peppol (B0), avant d'envoyer le moindre devis PACTE.
    VERDICT : NON VÉRIFIÉ
    PARCE QUE : aucune source primaire n'a pu être consultée — la sortie réseau de cette session refuse (403 CONNECT) efacture.belgium.be, finances.belgium.be, economie.fgov.be, ejustice.just.fgov.be et les prestataires de paiement (journal du proxy, 2026-09-16). Tout ci-dessus est un relais d'index, jamais une page lue.
    NON VÉRIFIÉ : exhaustivité des mentions · durée de conservation · libellé de la mention de franchise · obligation de compte pro · tous les tarifs · montants d'amende · date de publication de chaque page.
    CE QUI CHANGERAIT MON AVIS : l'ouverture effective d'une seule de ces pages, en priorité le champ d'application Peppol. S'il ne couvrait pas un indépendant en franchise facturant un autre indépendant, B0 cesserait d'être bloquant et le virement SEPA suffirait.
