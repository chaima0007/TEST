# Audit & stratégie de consolidation — Domaines & DNS

> Revue : 2026-06-29. Audit : `python3 scripts/domains_audit.py` → **CRITIQUE (fragmentation)**.
> ⚠️ Je n'ai pas accès à tes comptes registrars : complète `data/governance/domains_inventory.json`
> avec les données réelles ; ce document fixe la **stratégie** et le **runbook**.

---

## 1. Constat : pourquoi l'état actuel est fragile
3 registrars (**OVH, Register, Porkbun**) → fragmentation = **points de défaillance multiples** :
- Plusieurs comptes / 2FA / cartes de paiement → **risque d'expiration** d'un domaine oublié (= site mort, e-mails morts).
- Pas de **vue unique** ni de politique de sécurité homogène (lock, DNSSEC).
- DNS dispersé → un changement = plusieurs interfaces, risque d'erreur et de **downtime**.
- Risque de **détournement** (hijacking) accru si un compte est mal protégé.

## 2. Principe directeur : séparer + centraliser
**Découpler le registrar du DNS, et centraliser chacun.**
- **DNS = 1 seul fournisseur pour TOUTES les zones → Cloudflare DNS** (gratuit, rapide, DNSSEC, anycast). Indépendant du registrar.
- **Registrar = 1 seul** qui gère **.be ET .com/.eu/gTLD → OVH ou Gandi** (UE).
  - ⚠️ Contrainte vérifiée : **Cloudflare Registrar ne vend pas le .be**. Pour un registrar unique couvrant ton `.be`, c'est **OVH ou Gandi** (pas Cloudflare).
  - Compromis coût pur : `.com` est moins cher chez Cloudflare/Porkbun (à prix coûtant) → si on tolère 2 registrars, on garde `.com` chez Cloudflare et `.be` chez OVH/Gandi. **Mais tu veux la centralisation** → recommandation : **tout chez OVH ou Gandi** (quelques € de plus sur le .com, mais 1 seule console = robustesse).

## 3. Architecture cible (2 fournisseurs, rôles clairs)
```
Registrar unique (OVH ou Gandi, UE)  →  possède tous les domaines (.be, .com…)
        │  (délègue les nameservers)
        ▼
DNS unique (Cloudflare)              →  gère toutes les zones, DNSSEC, vitesse
        │
        ▼
Hébergement (Cloudflare Pages / UE-natif)  →  cf. ETUDE_VEILLE_CONCURRENTIELLE_INFRA.md
```
Plus de fragmentation : **1 registrar, 1 DNS, 1 compte propriétaire dédié** (pas de comptes personnels éparpillés).

## 4. Socle de sécurité (éliminer les points de défaillance) — par domaine
- ✅ **Transfer lock** activé · ✅ **2FA** sur le compte registrar **et** DNS · ✅ **Auto-renew** ON + carte valide
- ✅ **DNSSEC** activé · ✅ **WHOIS privacy** · ✅ **EPP/auth code** stocké dans un coffre
- ✅ **Monitoring d'expiration** (alerte 60/30/7 jours) · ✅ **compte propriétaire** au nom de l'entité, pas perso

## 5. Runbook de migration (sans downtime)
**Étape 0 — Inventaire** : compléter `domains_inventory.json` (domaine, registrar, DNS, expiration, statuts sécurité).
**Étape 1 — Centraliser le DNS d'abord (réversible, sans transfert)** :
  1. Créer la zone dans Cloudflare, **importer tous les enregistrements** (A, AAAA, MX, TXT/SPF/DKIM/DMARC, CNAME).
  2. **Vérifier** la zone (comparer enregistrements), baisser les TTL avant bascule.
  3. Changer les **nameservers** chez chaque registrar vers Cloudflare. Tester (mail + web) avant de continuer.
**Étape 2 — Consolider le registrar** (domaine par domaine) :
  1. **Déverrouiller** + récupérer le **code EPP/auth** chez le registrar source.
  2. Vérifier l'éligibilité (pas de transfert < 60 jours après création/transfert précédent ; `.be` : procédure DNS Belgium).
  3. **Initier le transfert** vers OVH/Gandi, confirmer l'e-mail, payer (souvent +1 an inclus).
  4. Après transfert : **re-locker**, **auto-renew ON**, **DNSSEC** (re-publier la clé), **2FA**.
**Étape 3 — Vérification & doc** : audit final, mettre à jour l'inventaire, activer le monitoring.

> Le DNS est centralisé **avant** les transferts : ainsi, même pendant les transferts de registrar, la résolution DNS reste stable (zéro interruption).

## 6. Ordre de priorité (risque d'abord)
1. **Le plus urgent** : domaine le plus proche de l'expiration / sans auto-renew → sécuriser auto-renew + lock **aujourd'hui**.
2. Centraliser le **DNS** (gain de résilience immédiat, réversible).
3. Transférer les registrars vers **un seul** (OVH/Gandi).
4. Appliquer le **socle de sécurité** partout + monitoring.

## 7. Suivi
- Source de vérité : `data/governance/domains_inventory.json`.
- Audit récurrent : `python3 scripts/domains_audit.py` (signale fragmentation + manques) — verdict **CRITIQUE** tant que > 1 registrar.

> Décision recommandée (à valider) : **Registrar unique = OVH ou Gandi** (UE, gère .be) · **DNS unique = Cloudflare**.
> Si priorité coût absolue : 2 registrars (.be OVH/Gandi, .com Cloudflare) mais DNS toujours centralisé Cloudflare.
