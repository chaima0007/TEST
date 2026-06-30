# SOLEA — Déploiement (3 options gratuites)

> Le site est **statique** : il se déploie partout, gratuitement, et **encaisse un trafic énorme**
> via CDN sans rien à gérer côté serveur.

## ⚠️ Important : ce dépôt contient AUSSI une app Next.js (CompeteIQ)
SOLEA est dans le dossier **`feet-hub/`**. Il faut dire à la plateforme de **servir ce dossier
en statique**, sans builder Next.js. Les réglages ci-dessous le font.

## Option A — Netlify (le plus simple)
- **Drag & drop** : app.netlify.com/drop → glisse le dossier `feet-hub`. Fini.
- **Depuis Git** : un fichier `netlify.toml` est déjà à la racine (`publish = "feet-hub"`,
  pas de build). Connecte le dépôt, choisis la branche, déploie.

## Option B — Cloudflare Pages
1. dash.cloudflare.com → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
2. Dépôt `chaima0007/TEST`, branche `claude/foot-site-business-plan-ch0jt0`
3. **Framework preset : None**
4. **Build command : (laisser vide)**
5. **Build output directory : `feet-hub`**
6. Save and Deploy → URL en `*.pages.dev`

## Option C — Vercel
1. vercel.com → Add New → Project → importe le dépôt
2. **Framework Preset : Other**
3. **Root Directory : `feet-hub`**
4. Build command : vide · Output : vide (statique)
5. Deploy

## Après le déploiement
- Remplace `https://TON-DOMAINE.com` dans `robots.txt` et `sitemap.xml`.
- Branche ton domaine perso (tableau de bord de la plateforme).
- Soumets le `sitemap.xml` à Google Search Console (référencement).

## Vérifs rapides
- [ ] La page d'accueil s'affiche (age-gate → site).
- [ ] L'intro cinématique joue puis disparaît.
- [ ] Les liens « Voir le profil » / catégories pointent vers le partenaire avec **ton** code.
- [ ] FR/EN fonctionne. Mobile OK.
