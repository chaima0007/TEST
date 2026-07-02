# Module Prospection — CompeteIQ

Pipeline d'agents autonomes qui détecte, via Google Places, des entreprises
locales **sans site internet** et leur propose par email la création d'un site
(séquence de 4 emails, envoi SMTP, quota quotidien, **dry-run par défaut**).

## Vue d'ensemble du pipeline

L'Orchestrateur (`lib/outreach/agents/orchestrator.ts`) pilote cinq agents
experts, chacun responsable d'une étape, et persiste tout en base (Prisma) :

```
                        ┌──────────────────────┐
                        │    ORCHESTRATEUR     │
                        │  runPipeline(...)    │
                        └──────────┬───────────┘
           ┌───────────┬──────────┼──────────┬────────────┐
           ▼           ▼          ▼          ▼            ▼
      ┌─────────┐ ┌───────────┐ ┌────────────┐ ┌───────────┐ ┌─────────┐
      │  SCOUT  │ │ QUALIFIER │ │ COPYWRITER │ │ SEQUENCER │ │ MAILER  │
      │ Google  │ │  Scoring  │ │ Rédaction  │ │ Planning  │ │  SMTP   │
      │ Places  │ │ prospects │ │ 4 emails   │ │ J0/J+4/   │ │ (ou     │
      │ sans    │ │ (score ≥  │ │ personna-  │ │ J+10/J+18 │ │ dry-run)│
      │ site    │ │ min)      │ │ lisés      │ │           │ │         │
      └────┬────┘ └─────┬─────┘ └─────┬──────┘ └─────┬─────┘ └────┬────┘
           │            │             │              │            │
           └────────────┴─────────────┼──────────────┴────────────┘
                                      ▼
                        ┌──────────────────────┐
                        │   BASE DE DONNÉES    │
                        │ Prospects · Messages │
                        │ AgentRuns (rapports) │
                        └──────────────────────┘
```

- **Scout** : interroge Google Places (Places API New) par catégorie × ville et
  ne retient que les entreprises **sans site web déclaré**.
- **Qualifier** : attribue un score (avis, note, téléphone, complétude…) ; seuls
  les prospects ≥ `OUTREACH_MIN_SCORE` (défaut 30) passent en `qualified`.
- **Copywriter** : rédige les 4 emails personnalisés (nom, ville, métier, offre).
- **Sequencer** : planifie les envois selon la séquence J0 / J+4 / J+10 / J+18
  et arrête la séquence dès réponse ou désinscription.
- **Mailer** : envoie via SMTP (nodemailer) dans la limite du quota quotidien —
  ou simule sans rien envoyer en dry-run.

## Mise en route

1. **Google Places** : dans Google Cloud Console, activer **"Places API (New)"**
   sur votre projet, créer une clé d'API et la mettre dans
   `GOOGLE_PLACES_API_KEY`.
2. **Configuration** : copier `.env.example` vers `.env` et remplir l'identité
   de l'agence (`AGENCY_*`) et le SMTP (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`,
   `SMTP_PASS`, `SMTP_FROM`).
3. **Base de données** :
   ```bash
   npx prisma db push
   ```
4. **Dashboard** : lancer `npm run dev` puis ouvrir
   [`/dashboard/outreach`](http://localhost:3000/dashboard/outreach) — suivi des
   prospects, ajout manuel d'emails, marquage "Répondu", liste d'appels.
5. **CLI** :
   ```bash
   # Découvrir + qualifier + préparer les brouillons (jamais d'envoi)
   npm run outreach:discover -- "plombier,restaurant" "Lyon,Villeurbanne"

   # Traiter la file (envois/relances dus) en dry-run — rien ne part
   npm run outreach:run

   # Idem mais en envoi réel (--live)
   npm run outreach:send
   ```
6. **Cron recommandé** — envoi chaque jour ouvré à 9 h :
   ```cron
   0 9 * * 1-5 cd /app && npm run outreach:send
   ```

## Fonctionnement

### Séquence de 4 emails

| Étape | Jour  | Objectif                                                    |
|-------|-------|-------------------------------------------------------------|
| 1     | J0    | Premier contact : constat (pas de site) + offre concrète     |
| 2     | J+4   | Relance courte et polie                                      |
| 3     | J+10  | Apport de valeur (bénéfices concrets d'un site, exemples)    |
| 4     | J+18  | Clôture : dernière proposition, porte laissée ouverte        |

La séquence s'arrête immédiatement si le prospect répond (`replied`), se
désinscrit (`optout`) ou est marqué gagné/perdu.

### Garde-fous

- **Dry-run par défaut** : `OUTREACH_DRY_RUN=true` — aucun email ne part tant
  que vous n'avez pas explicitement activé le mode live (`--live` ou
  `OUTREACH_DRY_RUN=false`).
- **Quota quotidien** : `OUTREACH_DAILY_LIMIT` (défaut 50 emails/jour).
- **Scoring de qualification** : seuls les prospects dont le score atteint
  `OUTREACH_MIN_SCORE` (défaut 30) sont contactés — on privilégie la
  pertinence au volume.

### Statuts d'un prospect

`new` → `qualified` → `contacted` → `followup` → puis `replied`, `won`,
`lost` ou `optout` (désinscription — plus jamais contacté).

## Conformité

La prospection B2B par email est **admise en France** sur la base légale de
l'**intérêt légitime** (doctrine CNIL), à condition de respecter les règles
suivantes — le module les intègre, mais leur respect final vous incombe :

- **Pertinence professionnelle** : le message doit être en rapport avec la
  profession du destinataire. Ici : proposer un site web à une entreprise qui
  n'en a pas — ciblez des catégories pour lesquelles c'est réellement utile.
- **Identification de l'expéditeur (LCEN)** : nom de l'agence, email, téléphone
  et SIRET (`AGENCY_*`) figurent dans chaque email. Renseignez-les tous.
- **Source des données** : chaque email mentionne l'origine des coordonnées
  (fiche établissement publique Google).
- **Droit d'opposition simple** : chaque email contient un **lien de
  désinscription** (`GET /api/outreach/unsubscribe?token=...`) et le header
  **`List-Unsubscribe`**. La désinscription passe le prospect en `optout` et
  bloque tout envoi futur.
- **Droit de suppression** : honorez sans délai toute demande d'effacement des
  données (dashboard ou base).
- **Registre des traitements** : tenez à jour votre registre RGPD (art. 30) en
  y décrivant ce traitement de prospection (finalité, données collectées —
  nom, adresse, téléphone, email —, durée de conservation, base légale).

> **AVERTISSEMENT — allégations marketing.** Les valeurs configurées et
> annoncées dans les emails (notamment `AGENCY_YEARS_EXPERIENCE`, le prix
> `AGENCY_STARTING_PRICE`, le délai `AGENCY_DELIVERY_DAYS`) doivent être
> **EXACTES et vérifiables**. Annoncer par exemple des années d'expérience
> fictives constitue une pratique commerciale trompeuse, sanctionnée par les
> **articles L121-2 et suivants du Code de la consommation** (jusqu'à 2 ans
> d'emprisonnement et 300 000 € d'amende, majorables). Ne configurez que des
> faits vrais.

Enfin, restez mesuré : le quota quotidien (`OUTREACH_DAILY_LIMIT`) limite le
volume — gardez-le bas et visez la pertinence plutôt que la masse.

## Limites connues

- **Pas d'emails via Google Places** : l'API ne fournit jamais d'adresse
  email. Beaucoup de prospects n'ont donc qu'un téléphone → ils alimentent la
  **liste d'appels** du dashboard. Un email peut être ajouté à la main
  (dashboard) ou via `POST /api/outreach/prospects` ; la séquence email démarre
  alors normalement.
- **Détection de réponses manuelle** : le module n'analyse pas la boîte de
  réception. Quand un prospect répond, cliquez sur le bouton **"Répondu"** du
  dashboard pour stopper sa séquence.
