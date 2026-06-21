# PII Guidelines — Caelum Partners

## Définition et Périmètre

**Règle fondamentale :** Les engines Caelum n'analysent **aucune donnée PII** (Personally Identifiable Information) de personnes physiques.

Les entités analysées sont exclusivement :
- Des **pays** et **territoires**
- Des **régions** géographiques
- Des **organisations** (entreprises, institutions, ONG)

Les engines ne doivent jamais contenir de noms de personnes physiques, coordonnées, identifiants personnels ou données biométriques.

---

## Logs et Traces

**Anonymisation obligatoire :**
- Les adresses IP doivent être **tronquées ou hachées** avant tout stockage de log.
- Les User-Agents doivent être **agrégés par catégorie** (browser family), jamais stockés bruts.
- Les session IDs ne doivent pas être corrélables à une identité sans clé de déchiffrement séparée.

**Durée de rétention :** 30 jours maximum pour tous les logs applicatifs.

**Implémentation recommandée :**
```typescript
// Anonymiser l'IP avant log
const ip = req.headers.get("x-forwarded-for")?.split(",")[0]?.trim();
const hashedIp = crypto.createHash("sha256").update(ip + process.env.LOG_SALT).digest("hex").slice(0, 16);
logger.info({ ip: hashedIp, path: req.nextUrl.pathname });
```

---

## Contrôle d'Accès aux Dashboards

- **TODO :** Implémenter une couche d'authentification pour les dashboards pilotes.
- En attendant : accès restreint par configuration réseau ou token partagé.
- Les accès aux endpoints `/api/*` doivent être tracés (sans IP brute).
- Authentification recommandée : NextAuth.js avec provider OAuth2 (Google Workspace ou GitHub).

---

## Rétention des Données

| Type de donnée | Durée de rétention | Lieu de stockage |
|---|---|---|
| Logs applicatifs | 30 jours | Hébergeur cloud |
| Scores analytiques (engines) | Durée du contrat | Base vectorielle / CDN |
| Sessions dashboard | Session uniquement (stateless) | Mémoire client |
| Métadonnées d'audit | 12 mois | Logs sécurisés |

---

## Checklist Pré-Commit

Avant tout commit dans ce repo, vérifier l'absence de :

- [ ] Noms propres de personnes physiques dans le code ou les données
- [ ] Adresses email (hors variables d'env et documentation officielle)
- [ ] Numéros de téléphone, SIRET, numéros d'identification personnels
- [ ] Adresses IP fixes ou plages d'adresses internes
- [ ] Clés API, tokens ou mots de passe en clair
- [ ] Données issues de scraping contenant des PII
- [ ] Fichiers `.env`, `.env.local`, `.env.production` commités

**Commande de vérification rapide :**
```bash
# Chercher des patterns suspects avant commit
git diff --cached | grep -iE "(api_key|secret|password|token|@gmail|@hotmail|[0-9]{10,})"
```

---

## Signalement

Toute suspicion de fuite PII doit être signalée immédiatement à : retrouvetonsmile@gmail.com

Voir aussi la procédure complète dans `infra/security/README.md` (section Incident Response).
