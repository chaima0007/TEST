# Mise en ligne — guide clé en main (2 sites séparés)

> Objectif : passer La Loi Avec Moi et Caelum **en ligne**, séparément. C'est le levier n°1 (P-CROISSANCE).
> Les deux apps **se buildent déjà** (vérifié). Aucun mot de passe à me donner : tu colles les valeurs côté hébergeur.

## A. Ce qu'il faut (ressources)
- Un compte d'hébergement **Vercel** (recommandé pour Next.js, offre gratuite pour démarrer) — ou Netlify/OVH/Cloudflare.
- Un **nom de domaine** par site (ex. `laloiavecmoi.be` et `caelum…`). Tu peux déployer d'abord SANS domaine (URL `*.vercel.app`).
- (Pour les leads) un **webhook** gratuit : Zapier « Catch Hook » ou Make.

## B. Déployer La Loi Avec Moi (citoyens) — dossier `laloiavecmoi/`
1. Sur Vercel : « New Project » → importe le dépôt → **Root Directory = `laloiavecmoi`**.
2. Framework détecté : Next.js. Build par défaut (`next build`). **Déploie.**
3. (Option) Variable d'environnement :
   - `NEXT_PUBLIC_SITE_URL` = l'URL finale (ex. `https://laloiavecmoi.be`) — pour le sitemap/robots.
4. (Option) Branche le **domaine** dans Vercel → Domains.

## C. Déployer Caelum (entreprises) — dossier racine `app/` (projet racine)
1. Sur Vercel : « New Project » → même dépôt → **Root Directory = racine (`.`)**.
2. Variables d'environnement à renseigner :
   - `NEXT_PUBLIC_SITE_URL` = l'URL Caelum.
   - `LEADS_WEBHOOK_URL` = l'URL de ton webhook (voir D) — **active la capture de leads**.
   - `DATABASE_URL` = si tu utilises la base (Prisma/login) ; sinon laisse les pages publiques fonctionner.
3. **Déploie**, puis branche le domaine.

> Important : **deux projets Vercel distincts** (un par Root Directory) = vraie séparation, conforme à ta règle.

## D. Activer la capture de leads (webhook) — 2 minutes
1. Crée un Zap « **Catch Hook** » (Zapier) ou un scénario « Webhook » (Make). Copie l'URL fournie.
2. Colle-la dans la variable `LEADS_WEBHOOK_URL` (étape C2) → re-déploie.
3. Côté Zapier/Make, envoie le lead où tu veux : Google Sheet, e-mail, CRM.
   → Les formulaires (simulateur `/conformite-2026`, newsletter `/veille`) enverront alors `email + profil + normes + source`.
   **Aucun mot de passe ne passe par le code : seulement l'URL du webhook, côté hébergeur.**

## E. Après la mise en ligne (rapide)
- Soumets les **sitemaps** à Google Search Console : `…/sitemap.xml` (les ~150 pages SEO seront indexées).
- Re-lance le **test de charge** sur l'URL réelle : `python3 scripts/load_simulation.py --base https://TON-URL`.

## F. Récapitulatif des variables d'environnement
| Variable | Où | Rôle |
|---|---|---|
| `NEXT_PUBLIC_SITE_URL` | les 2 apps | URL de base (sitemap/robots) |
| `LEADS_WEBHOOK_URL` | Caelum | destination des leads (webhook) |
| `DATABASE_URL` | Caelum (si base) | base de données (Prisma) |

> Tout le reste est déjà prêt : build vérifié, pages SEO générées, sécurité (zéro credential en dur), séparation des projets. Dis « go déploiement » quand tu veux : je te guide écran par écran.
