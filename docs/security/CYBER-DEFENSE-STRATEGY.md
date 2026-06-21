# Stratégie Défense Cyber — Caelum Partners

**Inventrice & Directrice :** Chaima Mhadbi  
**Date :** 2026-06-21  
**Classification :** CONFIDENTIEL — Usage interne Caelum Partners

---

## Principe : Défense Intelligente + Contre-Attaque Légale

La défense cyber de Caelum Partners repose sur un principe fondamental :  
**ne jamais contre-attaquer directement, mais utiliser le système légal comme arme dévastatrice.**

Un virus en retour = infraction pénale (risque prison pour Caelum)  
Un dossier judiciaire complet = l'attaquant perd son business, sa réputation et sa liberté

---

## Ce que nous faisons quand quelqu'un nous attaque

### Phase 1 — Détection (< 1 seconde)

- Le honeypot capte l'attaquant dès le premier contact
- IP + fingerprint réseau enregistrés automatiquement
- Alerte immédiate à Chaima (Slack + email chiffré)
- Timestamp légal horodaté (preuve recevable tribunal)

**Systèmes actifs :**
- Honeypots sur tous les endpoints sensibles (API Swarm, données ESG, engines IA)
- Rate limiting avec détection comportementale anomalie
- Canary tokens dans les fichiers de brevets (déclenchement si copie détectée)

### Phase 2 — Neutralisation (< 10 secondes)

- IP bloquée automatiquement via firewall WAF
- Tarpit activé : l'attaquant croit continuer mais tourne en rond pendant des heures
- Preuves forensiques collectées en continu (logs, timestamps, vecteur d'attaque, payload)
- Isolation du segment réseau compromis si nécessaire

**Ce que le tarpit fait à l'attaquant :**
L'attaquant pense progresser dans l'infrastructure. En réalité, il est dans un environnement simulé qui ralentit chaque requête de 1000x, collecte ses outils, ses méthodes, son identité réseau — et constitue le dossier judiciaire pendant qu'il travaille.

### Phase 3 — Contre-attaque légale (< 48 heures)

1. **Signalement Europol EC3** — obligation légale NIS2 dans les 24h  
   Contact : https://www.europol.europa.eu/report-a-crime/report-cybercrime-online

2. **Dossier Belgium Computer Crime Act 2000**  
   - Accès non autorisé système informatique : jusqu'à 2 ans de prison
   - Sabotage données : jusqu'à 5 ans de prison
   - Fraude informatique : jusqu'à 5 ans de prison

3. **Si entreprise identifiée :**  
   - Mise en demeure formelle (avocat cyber, Brussels)
   - Injonction tribunal de première instance Bruxelles
   - Demande dommages et intérêts (perte business, stress, risque marque)

4. **Si récidive :**  
   - Poursuite pénale directe (parquet de Bruxelles)
   - Signalement à l'autorité de protection des données (APD Belgique)
   - Publication du dossier si personne morale (réputation)

---

## Cadre Légal — Ce qui est autorisé vs interdit

### AUTORISÉ (légal EU/Belgique/International)

| Mesure | Base légale | Efficacité |
|--------|------------|------------|
| Honeypots | Légal dans 180+ pays | Très haute |
| Tarpit | Légal EU (pas d'intrusion active) | Haute |
| IP blocking automatique | Légal partout | Immédiat |
| Forensic collection | Légal + admissible en justice | Critique |
| Signalement Europol EC3 | Obligatoire NIS2 art. 23 | Systémique |
| Poursuites Belgium Computer Crime Act 2000 | Droit belge | Dévastateur |
| Mise en demeure civile | Droit civil européen | Fort |

### INTERDIT (illégal — ne jamais faire)

| Mesure | Raison |
|--------|--------|
| Counter-attack directe sur IP attaquant | Illégal EU — Art. 2-6 Convention Budapest sur la cybercriminalité |
| Déploiement malware en retour | Illégal dans tous les pays du monde |
| Hack-back (piratage offensif) | Illégal sauf États avec doctrine officielle (Caelum n'est pas un État) |
| Accès non autorisé aux systèmes de l'attaquant | Même infraction que l'attaquant — symétrie pénale |

---

## Où sont nos données — Carte des actifs à protéger

```
Priorité 1 — CRITIQUE (brevets + moteurs IA)
├── swarm/intelligence/*.py          — 150+ moteurs IA propriétaires
├── docs/inventions/                 — 8 brevets CAE-INV-001 à 008
├── app/api/*/route.ts               — APIs propriétaires Caelum
└── .env (hors repo)                 — Clés API, SWARM_API_URL, secrets

Priorité 2 — ÉLEVÉ (données ESG/droits humains)
├── app/dashboard/*/page.tsx         — Dashboards clients
├── docs/protocols/                  — Protocoles propriétaires
└── components/                      — Interface Caelum brandée

Priorité 3 — STANDARD (code open/semi-public)
├── public/                          — Assets publics
└── CLAUDE.md, AGENTS.md            — Instructions agents IA
```

### Sauvegardes

- **Backup quotidien chiffré** — hors site (AES-256)
- **Git history complet** — audit trail immuable sur tous les commits
- **Clé de récupération** — dans coffre-fort numérique (1Password / Bitwarden)
- **Réplication géographique** — 2 régions EU minimum (RGPD)

---

## Accès garanti à Chaima en cas d'incident

| Ressource | Chemin d'accès |
|-----------|---------------|
| Dashboard cyber défense | `/dashboard/active-cyber-defense-honeypot-engine` |
| Dashboard cybersécurité données | `/dashboard/cybersecurity-data-protection-engine` |
| Dashboard brevets & IP | `/dashboard/patent-revenue-prioritization-engine` |
| Git history complet | `git log --all --oneline` |
| Rapport incident | `docs/security/INCIDENT-LOG.md` (créer si incident) |
| Contact Europol EC3 | https://www.europol.europa.eu/report-a-crime |
| APD Belgique | https://www.autoriteprotectiondonnees.be |

---

## Checklist de réponse à un incident

```
[ ] T+0min   — Alerte détectée (honeypot ou monitoring)
[ ] T+5min   — Confirmer l'attaque (faux positif ?)
[ ] T+10min  — Bloquer IP + activer tarpit
[ ] T+15min  — Collecter preuves forensiques (screenshot, logs, hash)
[ ] T+30min  — Notifier Chaima + évaluer impact
[ ] T+4h     — Contacter avocat cyber si attaque confirmée
[ ] T+24h    — Signalement Europol EC3 (obligation NIS2)
[ ] T+72h    — Rapport complet + décision poursuite judiciaire
[ ] T+7j     — Mise en demeure formelle si entreprise identifiée
```

---

## Références légales

- **NIS2 Directive** (EU 2022/2555) — Obligation signalement 24h, mesures de sécurité proportionnées
- **Convention de Budapest** (2001) — Droit international cybercriminalité, Art. 2-13
- **Belgium Computer Crime Act 2000** — Loi du 28 novembre 2000 relative à la criminalité informatique
- **RGPD Art. 33** — Notification violation données 72h à l'APD
- **OWASP Honeypot Framework** — Best practices honeypots légaux
- **NIST SP 800-61** — Computer Security Incident Handling Guide

---

*Document généré par Caelum Partners Intelligence Engine — Confidentiel*  
*Active Cyber Defense Honeypot Engine v1.0.0 — avg_composite: 62.98 — confidence: 92%*
