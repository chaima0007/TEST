# Remise en ligne du site — Guide (suspension Netlify crédits)

## Ce qui s'est passé
Netlify : **300 crédits de build/mois épuisés** (cycle 21 juin → 20 juillet) →
projets suspendus. Cause : chaque `git push` reconstruisait tout le site, même
les commits ne touchant que les moteurs Python (`swarm/`).

## Correctif déjà en place (anti-gaspillage)
- `netlify.toml` → `ignore = "bash scripts/netlify-ignore-build.sh"`
  Le build est **annulé** si aucun fichier déployé n'a changé (moteurs, scripts,
  docs, data → 0 crédit).
- `.github/workflows/ci.yml` → `paths-ignore` (swarm, scripts, data, docs, md).
- Résultat : **les waves de moteurs ne consomment plus aucun crédit**.

## Option A — Attendre le reset (RECOMMANDÉ, 0 €)
Le **21 juillet**, les crédits Netlify se réinitialisent. Le site redevient
automatiquement en ligne. Grâce au correctif, les crédits ne seront plus gaspillés.
→ Rien à faire.

## Option B — Vercel en secours (gratuit, site en ligne tout de suite)
Le projet a déjà `vercel.json`. Étapes (nécessite ton compte) :
1. vercel.com → **Add New → Project** → importer le repo GitHub
2. Framework : **Next.js** (auto-détecté)
3. Root Directory : **.** (racine) pour le site Caelum,
   ou `laloiavecmoi` pour le site « La loi avec moi » séparé
4. Variables d'environnement : recopier celles de Netlify (SWARM_API_URL, DB…)
5. **Deploy**
→ Site en ligne en ~5 min, indépendant de Netlify.

## Option C — Réduire le coût des builds (durable)
L'app est lourde (milliers d'icônes sidebar, centaines de dashboards). Pistes :
- `scripts/scalability_guardian.py` surveille déjà les seuils OOM sidebar.
- Lazy-load des dashboards, split des barrels d'icônes, suppression du superflu.
→ Chaque build coûte moins → marge de crédits retrouvée.

## Important
Les **moteurs Python** (`swarm/`) n'ont PAS besoin d'être déployés sur Netlify :
c'est le **front Next.js** qui est buildé. La flotte de moteurs peut grandir
sans aucun coût de build.
