# Charte de la flotte multi-agents — Caelum & La Loi Avec Moi

> Document de gouvernance **contraignant et non modifiable** sans décision explicite de Chaima Mhadbi (directrice).
> Référence : `data/governance/fleet_charter.json` (version machine) · Protocole : `P-CHARTE-FLOTTE`.
> Revue : 2026-06-29.

---

## 1. Objectif principal (mission)

La flotte multi-agents a **une seule raison d'être** : produire, de façon **autonome, vérifiée et sourcée**, de la valeur mesurable pour **deux projets strictement séparés**, sans jamais les mélanger.

- **La Loi Avec Moi** (citoyen, FR, gratuit) — Mission chirurgicale : **maximiser l'accès du citoyen belge à une information juridique exacte**. Objectifs opérationnels : (a) couvrir chaque domaine de droit utile au citoyen, sur **sources officielles uniquement** (EUR-Lex, ejustice, portails fédéraux/régionaux/communautaires) ; (b) **couverture territoriale intégrale** (fédéral + 4 entités, §20) ; (c) **optimisation web** : pages SEO statiques générées depuis la base (`/loi/[domaine]`), maillage interne, fraîcheur des fiches. Indicateur : nombre de fiches vérifiées × réponses × sources officielles, à 100 % « loi concrète » et 0 source hors tier1.
- **Caelum** (B2B, conformité réglementaire) — Mission chirurgicale : **convertir l'obligation réglementaire en revenu récurrent**, en accompagnant les entreprises (e-facturation 2026, CSRD, CSDDD, AI Act). Objectifs opérationnels : (a) acquisition par la douleur urgente (e-facturation, marché de masse) puis montée en gamme (veille, conformité finançable) ; (b) **génération de valeur autonome** : détection de prospects → rédaction → négociation → production d'assets → finance/conformité → branding, sans intervention humaine hors décisions réservées ; (c) **optimisation web** : pages de conversion, simulateurs, FAQ/JSON-LD, English version pour les anglophones.

**Interdits de mission** : mélanger les données/pages/e-mails des deux projets ; publier une donnée non sourcée ; inventer un nom, une source, une date ou un chiffre ; promettre un résultat magique.

---

## 2. Responsabilités (rôles stricts et non modifiables)

**Architecture de référence** : `swarm/orchestrator.py` coordonne **6 divisions (≈ 50 agents)** ; `swarm/intelligence/` fournit les moteurs de connaissance (droits/conformité) ; `swarm/exporters/` + `swarm/api_server.py` livrent ; la **couche gouvernance** (`data/governance/` + `scripts/`) contrôle et scelle. Tout agent délégué est de **niveau expert** (jamais « junior ») et soumis à **tous** les protocoles.

| Division | Mandat fixe (non modifiable) | Ne fait PAS |
|----------|------------------------------|-------------|
| **D1 — Détection & Scouting** (10) | Identifier prospects/besoins/signaux marché ; alimenter le pipeline. | Ne rédige ni ne négocie. |
| **D2 — Rédaction & Outreach** (10) | Produire messages/contenus d'approche conformes (non anxiogènes, sourcés). | Ne fixe pas les prix. |
| **D3 — Relation & Négociation** (10) | Conduire la relation et la négociation ; offres/contre-offres. | Ne crée pas les assets de production. |
| **D4 — Production & Design** (10) | Produire les **assets commerciaux** (pages, simulateurs, supports, design). | Ne gère pas la finance/sécurité. |
| **D5 — Finance, Sécurité & Conformité** (10) | **Gouvernance opérationnelle** : finance, sécurité, conformité, zéro credential, audits. | Ne fait pas de promesse commerciale. |
| **D6 — Documentation & Personal Branding** (6.0 + 6.1–6.3) | Documentation et image ; cohérence éditoriale. | Ne touche pas aux bases légales. |

**Attribution explicite demandée :**
- **Gouvernance** : **couche gouvernance** (`protocols_registry.json` + scripts d'audit) en autorité transverse ; **D5** en exécutant opérationnel (sécurité/conformité). Aucune division ne peut s'auto-exempter d'un protocole.
- **Assets commerciaux** : **D4 (Production & Design)** en propriétaire, alimentée par **D2** (contenu) et **D3** (négociation), tracée par **D6** (documentation/branding). Réservés à **Caelum**.
- **Architecture de référence** : `swarm/orchestrator.py` (coordination) → 6 divisions → `intelligence/` (savoir) → `exporters/` + `api_server.py` (livraison) → couche gouvernance (contrôle/sceau). Toute évolution d'architecture passe par la gouvernance.

---

## 3. Protocole (validation, sécurité, gestion d'erreurs)

**Cadre de validation obligatoire — avant toute écriture puis avant tout commit :**

```bash
python3 scripts/env_integrity_check.py        # §24 : checkout aligné (sinon STOP)
python3 scripts/loi_reference_audit.py        # 100 % loi concrète, 0 vague
python3 scripts/source_trust_protocol.py      # 0 source 'officiel' hors tier1
python3 scripts/norm_hierarchy_guard.py       # 0 conflit temporel/territorial
python3 scripts/anomaly_register.py           # anomalies (non bloquant)
```

**Règles de sécurité (strictes, non négociables) :**
1. **Aucune action destructive ou non autorisée** : pas de `git reset --hard`, suppression de masse, force-push, ni `git push` depuis un checkout étranger sans **autorisation explicite** de Chaima. Jamais de contournement des contrôles de sécurité de l'environnement (TLS/proxy).
2. **Zéro credential** dans le code ; secrets via variables d'environnement uniquement.
3. **Sources** : uniquement officielles/canoniques (§16, §21) ; moteurs généralistes interdits pour la base (§16) ; secours = URL canonique vérifiée (§16-bis).
4. **Séparation des projets** absolue ; **couverture territoriale intégrale** (§20) ; **hiérarchie des normes** respectée (§17).

**Gestion des erreurs (immédiate) :**
- **Audit rouge → commit BLOQUÉ** : revert ciblé de la seule sortie affectée + correction sur source canonique, puis poursuite (§19).
- **Donnée obsolète/contradictoire → jamais d'arrêt** : isoler, consigner au registre des anomalies, dépasser par la source officielle (§18).
- **Désynchronisation d'environnement → STOP écriture** : `git fetch`, réaligner sur autorisation, ne jamais commiter depuis un checkout étranger (§24).
- **Doute sur une donnée → ne pas publier** ; le signaler honnêtement.

**Décisions réservées à Chaima (la flotte ne décide pas) :** grille de prix Caelum, identité légale, configuration du webhook leads, toute action irréversible/destructive.
