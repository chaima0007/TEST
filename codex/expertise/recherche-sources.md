# EXPERTISE — RECHERCHE DE SOURCES

**Maturité : DÉBUTANT (1 fiche)** · Transverse (§4) · Dernière mise à jour : 2026-09-16

---

## EXP-SRC-001 — Un résumé d'index n'est pas une source primaire

- **ID :** EXP-SRC-001
- **Domaine :** recherche de sources / vérification (§13)
- **Principe appris :**
  Un moteur de recherche renvoie deux choses très différentes qu'il présente identiquement :
  **des URLs** (fiables : l'adresse existe) et **un résumé du contenu** rédigé par un modèle à
  partir de l'index, pas de la page. Le second est un **relais** : il a le ton d'une source
  officielle et la fiabilité d'un blog. Trois conséquences pratiques :
  1. **Quand la page primaire est inatteignable, le relais sert à savoir quelle URL ouvrir — jamais à conclure.** Il se note `RELAYÉ (non consulté)`, distinct de `VÉRIFIÉ` comme de `NON VÉRIFIÉ`.
  2. **Un chiffre ne passe jamais par un relais.** Tarif, taux, seuil, délai, montant d'amende : si la page n'a pas été ouverte, c'est `NON VÉRIFIÉ`, littéralement, à la place du chiffre. Un résumé automatique est exactement le mécanisme qui produit un chiffre plausible et faux.
  3. **L'échec d'accès est lui-même un livrable.** Dire « bloqué » sans nommer les domaines refusés oblige le suivant à refaire le travail ; les nommer transforme un échec en liste d'actions pour un humain qui, lui, n'est pas filtré.
- **Contrainte d'environnement constatée (2026-09-16) :** dans cette session, **aucune page n'a pu
  être ouverte** — 403 CONNECT sur les 14 domaines testés, sans exception : `*.belgium.be`,
  `*.fgov.be` (dont Justel), `inasti.be`, `smartbe.be`, `eur-lex.europa.eu`, `peppol.org`,
  `stripe.com`, `mollie.com`, `paypal.com`, `ing.be`, `kbc.be`. **`WebSearch` fonctionne ;
  `WebFetch` et `curl` sont bloqués identiquement** — donc tout ce qu'un agent rapporte ici vient
  de l'index, y compris ce qui est présenté comme une citation.
  **Conséquence de contrôle :** dans une session où `WebFetch` est bloqué, un dossier qui affiche
  « sources consultées le [date] » et des chiffres à la décimale près décrit une consultation qui
  **n'a pas pu avoir lieu** — c'est un point à vérifier avant de s'appuyer sur ses chiffres.
  *Constat d'une session, pas une règle permanente : à revérifier avant de s'y fier.*
- **Sources liées :** journal du proxy (`$HTTPS_PROXY/__agentproxy/status`, champ
  `recentRelayFailures`, 2026-09-16) · `/root/.ccr/README.md`, section « 403 / 407 from the proxy » :
  ne pas contourner, rapporter l'hôte bloqué.
- **Projets où appliqué :** TEST/Caelum — `codex/atlas/deliberations/DOSSIER-02-ENCAISSEMENT.md`.
- **Fiabilité :** ÉLEVÉE sur le principe (il découle du §13) · **CONFIRMÉE** sur la contrainte
  d'environnement (reproduite sur 8 domaines, 2 outils).
- **Date de dernière confirmation :** 2026-09-16
