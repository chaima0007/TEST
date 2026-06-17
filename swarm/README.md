# SWARM — Essaim de 54 Agents Autonomes

Système multi-agents piloté par LLM (Claude Opus) pour détecter des prospects, rédiger des emails personnalisés, négocier, produire des livrables, gérer les finances et documenter les succès — de façon entièrement autonome.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SWARM — ORCHESTRATEUR CENTRAL (LangGraph)              │
│                                                                             │
│   SwarmState ──► Div 1 ──► Div 2 ──► Div 5 ──► Div 3 ──► Div 4 ──► END   │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐   ┌──────────────────────────────────┐
│  DIVISION 1 — DÉTECTION & SCOUTING  │   │  DIVISION 2 — RÉDACTION & OUTREACH│
│  🔍  10 agents (1 Manager + 9 Exec) │   │  ✍️  10 agents (1 Manager + 9 Exec)│
│                                      │   │                                   │
│  1.0  Manager Détection              │   │  2.0  Directeur de la Rédaction   │
│  1.1  Éclaireur Artisans & Bâtiment  │   │  2.1  Copywriter Le Factuel       │
│  1.2  Éclaireur Restauration & Hôtel │   │  2.2  Copywriter L'Amical         │
│  1.3  Éclaireur Médical & Soin       │   │  2.3  Copywriter Le Client Perdu  │
│  1.4  Éclaireur E-commerce Local     │   │  2.4  Copywriter Région Nord      │
│  1.5  Éclaireur Agences Immo         │   │  2.5  Copywriter Région Sud       │
│  1.6  Éclaireur Écoles & Formation   │   │  2.6  Copywriter Paris & IDF      │
│  1.7  Éclaireur Garages & Auto       │   │  2.7  Copywriter Luxe & Premium   │
│  1.8  Éclaireur Juridique & Compta   │   │  2.8  Copywriter Artisans & TPE   │
│  1.9  Éclaireur Associations & Loisir│   │  2.9  Copywriter Relance & Suivi  │
└──────────────────────────────────────┘   └──────────────────────────────────┘

┌──────────────────────────────────────┐   ┌──────────────────────────────────┐
│  DIVISION 3 — RELATION & NÉGOCIATION │   │  DIVISION 4 — PRODUCTION & DESIGN│
│  🤝  10 agents (1 Manager + 9 Exec) │   │  ⚙️  10 agents (1 Manager + 9 Exec)│
│                                      │   │                                   │
│  3.0  Directeur de Clientèle         │   │  4.0  Directeur Technique (CTO)   │
│  3.1  Négociateur Sceptiques/Preuves │   │  4.1  Dev Front-End HTML/CSS      │
│  3.2  Négociateur Sceptiques/Garanti.│   │  4.2  Dev Front-End JS            │
│  3.3  Négociateur Sceptiques/Urgence │   │  4.3  Dev CMS & WordPress         │
│  3.4  Négociateur Enthousiastes/Tech │   │  4.4  Expert SEO — Audit & Balises│
│  3.5  Négociateur Enthousiastes/Vente│   │  4.5  Expert SEO — Contenu Web    │
│  3.6  Négociateur Upsell & Cross-sell│   │  4.6  Expert SEO — Local & Maillag│
│  3.7  Négociateur Relance J+4        │   │  4.7  Spécialiste Perf. Images    │
│  3.8  Négociateur Relance J+10       │   │  4.8  Spécialiste SSL & Sécurité  │
│  3.9  Négociateur Relance J+21       │   │  4.9  Spécialiste Core Web Vitals │
└──────────────────────────────────────┘   └──────────────────────────────────┘

┌──────────────────────────────────────┐   ┌──────────────────────────────────┐
│  DIVISION 5 — FINANCE & CONFORMITÉ   │   │  DIVISION 6 — DOCUMENTATION &    │
│  🛡️  10 agents (1 Manager + 9 Exec) │   │  ✨  PERSONAL BRANDING (4 agents) │
│                                      │   │                                   │
│  5.0  CFO (Directeur Fin. & Admin.)  │   │  6.0  Expert Branding (Manager)   │
│  5.1  Contrôleur Devis & Stripe      │   │  6.1  Rédacteur LinkedIn          │
│  5.2  Contrôleur Réconciliation      │   │  6.2  Rédacteur CV (Format STAR)  │
│  5.3  Contrôleur Relances Impayés    │   │  6.3  Rédacteur Études de Cas     │
│  5.4  Officier RGPD — Audit Emails   │   │                                   │
│  5.5  Officier RGPD — Opt-Out        │   │  Agent standalone — observe tous  │
│  5.6  Officier RGPD — Registre       │   │  les cycles et transforme chaque  │
│  5.7  Superviseur Health Monitor     │   │  résultat en contenu LinkedIn,    │
│  5.8  Superviseur Queue Manager      │   │  entrée CV et étude de cas.       │
│  5.9  Superviseur Logs & Analytics   │   │                                   │
└──────────────────────────────────────┘   └──────────────────────────────────┘

  Total : 54 agents configurés (50 opérationnels + 4 branding)
```

---

## Prérequis

- **Python 3.12+**
- **Redis 7+** (pour les queues inter-divisions via Celery)
- **Clé API Anthropic** (`ANTHROPIC_API_KEY`) — modèle `claude-opus-4`
- **Compte Stripe** avec clé secrète et webhook secret
- **Clé Google Maps API** (scouting Division 1)
- **Clé PageSpeed Insights API** (audit performance Division 1)
- Optionnel : compte SMTP (SendGrid ou autre) pour l'envoi d'emails

---

## Installation

```bash
# 1. Cloner le dépôt et aller dans le répertoire swarm
git clone <repo> && cd <repo>/swarm

# 2. Créer l'environnement virtuel et installer les dépendances
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API réelles
```

---

## Usage CLI

```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Afficher la cartographie complète des 54 agents
python main.py --status

# Exécuter un cycle unique (Détection → Rédaction → Finance → Négociation → Production)
python main.py

# Mode continu : relance automatiquement un cycle toutes les heures
python main.py --loop

# Simuler le dialogue inter-agents Agent 3.5 (Vendeur) ↔ Agent 5.1 (Finance)
python main.py --simulate-sale

# Exécuter un cycle et exporter les résultats en JSON
python main.py --output-json resultats.json

# Mode continu avec export JSON (écrase le fichier à chaque cycle)
python main.py --loop --output-json resultats.json
```

---

## Usage API (FastAPI)

### Lancement du serveur

```bash
# Depuis le répertoire swarm/
uvicorn api_server:app --host 0.0.0.0 --port 8001 --reload
```

La documentation interactive Swagger est disponible sur : `http://localhost:8001/docs`

### Endpoints disponibles

#### Santé & monitoring

```bash
# Vérifier que le serveur est en ligne
curl http://localhost:8001/

# Bilan de santé détaillé (agents actifs, erreurs, uptime)
curl http://localhost:8001/health
```

#### Statut de l'essaim

```bash
# Statut complet : agents, divisions, KPIs, chiffre d'affaires du jour
curl http://localhost:8001/swarm/status

# Déclencher un cycle complet en tâche de fond
curl -X POST http://localhost:8001/swarm/cycle/trigger

# Consulter le résumé du dernier cycle exécuté
curl http://localhost:8001/swarm/cycle/last
```

#### Négociation (Division 3)

```bash
# Soumettre une réponse entrante d'un prospect (déclenche l'Agent 3.0 → routage)
curl -X POST http://localhost:8001/negotiation/inbound \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "boulangerie_martin_75",
    "prospect_name": "Boulangerie Martin",
    "sector": "Restauration & Hôtellerie",
    "message": "Bonjour, combien coûte la réparation de mon site mobile ?",
    "sentiment": "Curieux"
  }'
# Réponse : thread_id, négociateur assigné, devis, lien Stripe
```

#### Finance (Division 5)

```bash
# Confirmer un paiement Stripe et déclencher la production (Division 4)
curl -X POST http://localhost:8001/payment/confirm \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "thread_boulangerie_martin_75",
    "amount_eur": 149.0,
    "stripe_charge_id": "ch_3OxxxYYY"
  }'
# Réponse : job_id, nombre de livrables, URL du package, CA du jour

# Rapport financier quotidien (CA, taux conversion, panier moyen, impayés)
curl http://localhost:8001/finance/report
```

#### Conformité RGPD

```bash
# Blacklister un domaine suite à une demande opt-out
curl -X POST "http://localhost:8001/compliance/opt-out?domain=example.fr"
```

#### Cartographie des agents

```bash
# Lister les 54 agents avec leur rôle, division et outils
curl http://localhost:8001/agents
```

---

## Variables d'environnement

Créer un fichier `.env` à partir de `.env.example` :

```bash
cp .env.example .env
```

| Variable              | Description                                      | Exemple                        |
|-----------------------|--------------------------------------------------|--------------------------------|
| `ANTHROPIC_API_KEY`   | Clé API Anthropic pour les agents LLM            | `sk-ant-api03-xxxxx`           |
| `STRIPE_SECRET_KEY`   | Clé secrète Stripe (paiements)                   | `sk_live_xxxxx`                |
| `STRIPE_WEBHOOK_SECRET` | Secret de validation des webhooks Stripe       | `whsec_xxxxx`                  |
| `REDIS_URL`           | URL de connexion Redis (queues Celery)            | `redis://localhost:6379/0`     |
| `SMTP_HOST`           | Serveur SMTP pour l'envoi d'emails               | `smtp.sendgrid.net`            |
| `SMTP_PORT`           | Port SMTP                                        | `587`                          |
| `SMTP_USER`           | Identifiant SMTP                                 | `apikey`                       |
| `SMTP_PASS`           | Mot de passe ou clé API SMTP                     | `SG.xxxxx`                     |
| `FROM_EMAIL`          | Adresse email expéditrice                        | `contact@votre-domaine.fr`     |
| `GOOGLE_MAPS_API_KEY` | Clé API Google Maps (scouting Division 1)        | `AIzaSyxxxxx`                  |
| `PAGESPEED_API_KEY`   | Clé API PageSpeed Insights (audit performance)   | `AIzaSyxxxxx`                  |

---

## Structure des fichiers

```
swarm/
├── .env.example          # Modèle de variables d'environnement
├── __init__.py
├── api_server.py         # Serveur FastAPI REST (interface Next.js ↔ Swarm)
├── config.py             # Configuration des 54 agents (rôles, objectifs, outils)
├── orchestrator.py       # Machine d'état LangGraph — coordination des 5 divisions
├── main.py               # Point d'entrée CLI (--status, --loop, --simulate-sale)
├── simulation.py         # Simulation dialogue Agent 3.5 ↔ 5.1
├── requirements.txt      # Dépendances Python
├── Dockerfile            # Image Docker pour le serveur FastAPI
├── README.md             # Ce fichier
│
├── agents/
│   ├── __init__.py
│   ├── base.py           # Classe de base BaseSwarmAgent (CrewAI wrapper)
│   └── tools.py          # Outils partagés (pagespeed, google_maps, stripe, etc.)
│
└── divisions/
    ├── __init__.py
    ├── division_1_detection.py    # Logique métier Division 1 (scouting web)
    ├── division_2_redaction.py    # Logique métier Division 2 (cold email)
    ├── division_3_negotiation.py  # Logique métier Division 3 (CRM, négociation)
    ├── division_4_production.py   # Logique métier Division 4 (livrables techniques)
    ├── division_5_finance.py      # Logique métier Division 5 (Stripe, RGPD)
    └── division_6_branding.py     # Logique métier Division 6 (LinkedIn, CV)
```

---

## Flux de travail inter-divisions

Le cycle complet suit un graphe d'état LangGraph orchestré séquentiellement :

```
1. DÉTECTION (Division 1)
   ├── L'Agent 1.0 (Manager) découpe le web en 9 territoires sectoriels
   ├── Les Agents 1.1–1.9 scannent en parallèle via Google Maps + PageSpeed
   └── Résultat : liste de fiches ProspectFiche (JSON) transmises à Division 2

2. RÉDACTION (Division 2)
   ├── L'Agent 2.0 (Directeur Rédaction) distribue les fiches aux 9 copywriters
   ├── Chaque copywriter applique son angle psychologique (factuel, amical, etc.)
   ├── L'Agent 5.4 valide la conformité RGPD de chaque email avant envoi
   └── Résultat : file OutreachRecord enrichie → envoi SMTP automatisé

3. VALIDATION RGPD (Division 5 — première passe)
   ├── L'Agent 5.4 scanne chaque email (lien STOP, ton, données personnelles)
   ├── L'Agent 5.5 maintient la liste noire des domaines opt-out
   └── Résultat : emails validés ou bloqués, registre mis à jour

4. NÉGOCIATION (Division 3)
   ├── L'Agent 3.0 surveille les réponses entrantes en temps réel
   ├── Il analyse le sentiment (Curieux, Sceptique, Enthousiaste, Fantôme…)
   ├── Il route vers le négociateur spécialisé (Agents 3.1–3.9)
   ├── L'Agent 3.5 (Vendeur Principal) collabore avec l'Agent 5.1 pour le devis
   ├── L'Agent 5.1 génère le lien Stripe et confirme le montant
   └── Résultat : thread NegotiationThread avec lien Stripe envoyé au prospect

5. PRODUCTION (Division 4)
   ├── Déclenchée automatiquement par le webhook Stripe (paiement confirmé)
   ├── L'Agent 4.0 (CTO) distribue le travail aux 9 techniciens
   ├── En parallèle : HTML/CSS (4.1), JS (4.2), WordPress (4.3),
   │   SEO (4.4–4.6), Performance (4.7–4.9)
   └── Résultat : package livrable (ZIP) + rapports PDF envoyés au client

6. FINANCE & RÉCONCILIATION (Division 5 — deuxième passe)
   ├── L'Agent 5.2 réconcilie les paiements Stripe avec les livraisons
   ├── L'Agent 5.3 relance automatiquement les impayés (J+3, J+7)
   ├── L'Agent 5.7 surveille la santé des 50 agents opérationnels
   ├── L'Agent 5.8 gère les queues Redis/Celery (priorisation des tâches)
   ├── L'Agent 5.9 agrège les logs et génère des recommandations d'optimisation
   └── Résultat : rapport financier quotidien (CA, taux conversion, panier moyen)

7. DOCUMENTATION & BRANDING (Division 6 — asynchrone)
   ├── L'Agent 6.0 observe tous les cycles en temps réel
   ├── L'Agent 6.1 rédige des posts LinkedIn storytelling (≤ 1 300 caractères)
   ├── L'Agent 6.2 génère des bullet points CV format STAR avec mots-clés ATS
   └── L'Agent 6.3 rédige des études de cas Avant/Après pour le portfolio
```

---

## Stack technique

| Composant       | Technologie                                      |
|-----------------|--------------------------------------------------|
| LLM             | Anthropic Claude Opus (`claude-opus-4`)          |
| Orchestration   | LangGraph 0.2 (machine d'état asynchrone)        |
| Agents          | CrewAI 0.80 (agents + tools)                     |
| LLM Client      | LangChain-Anthropic 0.3                          |
| API REST        | FastAPI 0.115 + Uvicorn 0.34                     |
| Queues          | Redis 7 + Celery 5.4                             |
| Paiements       | Stripe API (Payment Links, Webhooks, Reporting)  |
| Frontend        | Next.js 16 (TypeScript, React 19, Tailwind CSS 4)|
| CLI             | Rich 13 (tableaux, panels, couleurs)             |
| Validation      | Pydantic v2                                      |
| HTTP client     | HTTPX + aiohttp (requêtes async)                 |
| Containerisation| Docker + Docker Compose                          |

---

## Lancement avec Docker Compose

```bash
# Depuis la racine du projet
docker compose up --build

# Services disponibles :
#   Next.js dashboard  →  http://localhost:3000
#   Swarm FastAPI      →  http://localhost:8001
#   Swagger UI         →  http://localhost:8001/docs
#   Redis              →  localhost:6379
```

> **Note :** En production, remplacer le fichier `.env.example` par un vrai `.env`
> contenant vos clés API réelles avant de lancer `docker compose up`.
