# CRM Integration — HubSpot / Salesforce

## Vue d'ensemble

Ce module gère la synchronisation des données prospects et clients entre Caelum Partners et les CRM commerciaux (priorité : HubSpot, puis Salesforce). L'objectif est d'automatiser le pipeline commercial depuis la signature d'un accord pilote jusqu'à l'onboarding.

---

## HubSpot — Objets et propriétés

### Objets utilisés
- **Company** : le compte client (entreprise)
- **Contact** : interlocuteur principal (ex: Head of ESG)
- **Deal** : opportunité commerciale (Pilote → Client)

### Propriétés custom à créer dans HubSpot

| Propriété | Type | Description | Valeurs |
|---|---|---|---|
| `caelum_pilot_status` | Enumeration | Statut du pilote | `not_started`, `in_progress`, `converted`, `churned` |
| `caelum_domains_active` | Multi-checkbox | Engines activés pour ce client | Liste des domains disponibles |
| `caelum_tier` | Enumeration | Tier souscrit | `easy_access`, `enterprise_premium` |
| `caelum_tenant_id` | Single-line text | ID tenant dans notre système | UUID |
| `caelum_csrd_exposure` | Enumeration | Niveau d'exposition CSRD | `LOW`, `MEDIUM`, `HIGH` |
| `caelum_onboarding_date` | Date | Date de début pilote | Date |

### Pipeline de deals recommandé
```
Prospect → Démo planifiée → Démo réalisée → Pilote signé → En pilote → Converti → Client actif
```

---

## Webhook — Signature accord pilote

À la signature d'un accord pilote (événement externe ou manuel), déclencher :

1. **Créer un Deal** dans HubSpot :
   - Nom : `Pilot — {Company Name}`
   - Stade : "Pilote signé"
   - Montant : 0€ (pilote gratuit 30j)
   - Date de clôture estimée : J+30

2. **Créer une Tâche** associée :
   - Titre : `Onboarding J0 — {Company Name}`
   - Assignée à : Customer Success Manager
   - Échéance : date de signature + 24h

3. **Mettre à jour** `caelum_pilot_status` → `in_progress`

### Endpoint webhook (à implémenter)
```
POST /api/webhooks/pilot-signed
Body: { tenant_id, company_hubspot_id, signed_at }
Auth: HMAC-SHA256 signature
```

---

## Export CSV hebdomadaire

Script : `tools/crm_integration/hubspot_sync.py` (TODO)

Chaque lundi à 09h00 (CET) :
1. Requête HubSpot API → liste des Deals en cours
2. Enrichissement avec statuts Caelum (tier, domains_active, pilot_status)
3. Export CSV vers dossier partagé / Google Drive / email équipe commerciale

### Colonnes du CSV export
```
company_name,contact_email,pilot_status,tier,domains_active,start_date,days_remaining,csrd_exposure,deal_stage
```

---

## Variables d'environnement requises

```bash
# .env.local (jamais commité)
HUBSPOT_API_KEY=your_private_app_token_here
SALESFORCE_CLIENT_ID=...        # Si migration vers SF
SALESFORCE_CLIENT_SECRET=...    # Si migration vers SF
CRM_WEBHOOK_SECRET=...          # HMAC secret pour webhooks entrants
```

**Règle absolue :** Aucune clé API dans le code source. Toujours via variables d'environnement. Vérifier avec `git secrets` en pre-commit hook.

---

## Salesforce (roadmap)

Si le client Enterprise impose Salesforce :
- Utiliser l'API Salesforce REST (OAuth 2.0 Connected App)
- Mapping des champs : même logique que HubSpot, adapter les noms de champs SF
- Module SF séparé : `tools/crm_integration/salesforce_sync.py`

---

## TODO

- [ ] Créer les propriétés custom dans HubSpot (via HubSpot CLI ou interface admin)
- [ ] Implémenter `hubspot_sync.py` (export CSV + webhook handler)
- [ ] Configurer le webhook dans HubSpot (Settings → Integrations → Webhooks)
- [ ] Tester l'endpoint `/api/webhooks/pilot-signed` avec Postman
- [ ] Documenter le pipeline de deals dans le CRM
- [ ] Configurer les séquences d'email HubSpot (voir `docs/outreach/sequences.md`)
- [ ] Ajouter les prospects prioritaires depuis `data/prospects/enterprise_candidates.csv`

---

## Liens utiles

- HubSpot Private Apps : https://developers.hubspot.com/docs/api/private-apps
- HubSpot Custom Properties : Settings → Data Management → Properties
- Webhook HubSpot : https://developers.hubspot.com/docs/api/webhooks
