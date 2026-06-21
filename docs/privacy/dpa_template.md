# Data Processing Agreement (DPA) — Template

> **NOTE LEGALE :** Ce modèle doit être validé par un conseil juridique avant signature. Il est fourni à titre indicatif uniquement.

---

## Parties

**Sous-traitant :** Caelum Partners (ci-après « le Prestataire »)
**Responsable du traitement :** [Nom du client] (ci-après « le Client »)

---

## 1. Objet et Finalités du Traitement

Le Prestataire traite des données pour le compte du Client aux fins exclusives suivantes :

- Analyse des risques relatifs aux droits humains (Due Diligence sur les Droits Humains, DDH)
- Production de rapports ESG / DDH sur des pays, régions et organisations
- Mise à disposition de tableaux de bord analytiques

Les données traitées portent exclusivement sur des **entités collectives** (pays, régions, organisations). Aucune donnée de personnes physiques identifiables n'est collectée ou traitée dans le cadre des engines d'analyse.

---

## 2. Durée du Traitement

Le traitement est effectué pendant la durée du contrat pilote ou d'abonnement conclu entre les parties. À l'expiration du contrat, le Prestataire supprime ou anonymise toutes les données du Client dans un délai de 30 jours.

---

## 3. Nature des Données Traitées

- Données analytiques agrégées sur des États, territoires et organisations
- Métadonnées de sessions dashboard (anonymisées — voir section 5)
- Aucune donnée PII au sens du RGPD (Règlement (UE) 2016/679)

---

## 4. Transferts Hors Union Européenne

Si des données sont transférées vers des pays tiers (hors UE/EEE) :

- Le transfert doit être encadré par des **Clauses Contractuelles Types (CCT)** adoptées par la Commission européenne.
- Le Prestataire informe le Client de tout sous-traitant ultérieur situé hors UE.
- Le Client donne son accord préalable à tout transfert hors UE.

---

## 5. Mesures Techniques et Organisationnelles

Le Prestataire s'engage à mettre en œuvre les mesures suivantes :

**Chiffrement :**
- Données en transit : TLS 1.2 minimum
- Données au repos : chiffrement AES-256 (si stockage persistant)

**Contrôle d'accès :**
- Accès aux dashboards : authentification requise (couche auth à implémenter — voir `PII_guidelines.md`)
- Accès aux secrets : variables d'environnement uniquement, jamais dans le code source
- Principe du moindre privilège pour tous les accès systèmes

**Audit et traçabilité :**
- Logs d'accès conservés 30 jours maximum
- Anonymisation des logs (IP et user-agents masqués)

**Gestion des incidents :**
- Processus de réponse aux incidents documenté (voir `infra/security/README.md`)
- Notification au Client en cas de violation dans les 24 heures

---

## 6. Droits des Personnes Concernées

Dans la mesure où des données de personnes physiques seraient incidentellement traitées, le Prestataire s'engage à :

- Répondre aux demandes d'exercice des droits (accès, rectification, effacement, portabilité, opposition) dans un délai de 30 jours.
- Notifier le Client de toute demande reçue directement, sans y donner suite sans instruction du Client.

---

## 7. Violation de Données

En cas de violation de données à caractère personnel :

- Le Prestataire notifie le Client **dans les 72 heures** suivant la prise de connaissance de l'incident.
- La notification comprend : nature de la violation, catégories et volume de données affectées, mesures prises.
- Le Client procède à la notification à la **CNIL** (ou autorité compétente) si la violation présente un risque pour les droits et libertés des personnes.

---

## 8. Sous-traitance Ultérieure

Le Prestataire peut faire appel aux sous-traitants ultérieurs suivants :

- Hébergeur cloud (Vercel / AWS — à préciser)
- Base de connaissances vectorielle (Weaviate Cloud — voir `infra/terraform/vector.tf`)

Tout nouveau sous-traitant ultérieur doit être communiqué au Client avec un délai de préavis de 30 jours.

---

## 9. Signatures

| | Prestataire | Client |
|---|---|---|
| **Société** | Caelum Partners | [Nom du Client] |
| **Représentant** | [Nom] | [Nom] |
| **Date** | ___/___/______ | ___/___/______ |
| **Signature** | | |
