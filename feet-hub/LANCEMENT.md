# SOLEA — Checklist de lancement (mise en place)

> Suis ces étapes dans l'ordre. À la fin, ton site est **en ligne et capable de rapporter**.

## ✅ Étape 1 — Mettre ton code d'affiliation (CRITIQUE)
Sans ça, tous les clics partent **sans te rémunérer**.
1. Inscris-toi au **programme d'affiliation FeetFinder** (et/ou un autre partenaire).
2. Récupère ton **code de parrainage** (ex. `MONCODE`).
3. Dans le dossier `feet-hub/`, fais un **rechercher-remplacer** de `SOLEA_CODE` → `MONCODE`
   dans ces 6 fichiers : `index.html`, `category.html`, `creators.html`, `diapason.html`,
   `collections.html` (et vérifie `guides/FUNNEL_3CLICS.md`).
4. Vérifie que `AFF.base` pointe bien vers la bonne plateforme.

## ✅ Étape 2 — Mettre en ligne (gratuit, ~5 min)
**Option A — Netlify (le plus simple)**
- Va sur **app.netlify.com/drop** → glisse le dossier `feet-hub`. URL live immédiate.
- (Ou « Import from Git » : un `netlify.toml` est déjà prêt à la racine du dépôt.)

**Option B — Cloudflare Pages (depuis Git)**
- dash.cloudflare.com → Workers & Pages → Create → Pages → Connect to Git
- Repo `chaima0007/TEST`, branche `claude/foot-site-business-plan-ch0jt0`
- Framework preset : **None** · Build command : *(vide)* · **Output directory : `feet-hub`**

## ✅ Étape 3 — Brancher un domaine (~10 €/an)
- Achète un domaine court. Branche-le à Netlify/Cloudflare (instructions dans leur tableau de bord).
- Remplace `https://TON-DOMAINE.com` dans `robots.txt` et `sitemap.xml`.

## ✅ Étape 4 — Pages légales (avant de pousser du trafic)
- Transforme `LEGAL_MODELES.md` en pages `cgu.html`, `confidentialite.html`, `dmca.html`,
  `mentions-legales.html` (relecture juridique recommandée).
- Branche la bannière cookies.

## ✅ Étape 5 — Mesure (pour savoir ce qui marche)
- Ajoute un outil d'analytics **sans cookies** (Plausible ou Matomo) ou Google Analytics.
- Surveille : visiteurs, sources de trafic, clics affiliés (via les `utm_campaign` déjà en place).

## ✅ Étape 6 — Newsletter
- Crée un compte **Brevo** (gratuit) → remplace l'action des formulaires (`index.html`,
  `category.html`, `aide.html`) par ton endpoint Brevo/Formspree.

## ✅ Étape 7 — Premier trafic
- Suis `STRATEGIE_MARKETING.md` + `guides/RECHERCHE_AUDIENCE.md` :
  SEO (pages-guides), Reddit (règles anti-ban), X, Pinterest. 1 action/jour.

---
### Récap des fichiers utiles
| Fichier | Quand |
|---|---|
| `LANCEMENT.md` (ce fichier) | maintenant |
| `DEPLOIEMENT.md` | étape 2 |
| `LEGAL_MODELES.md` | étape 4 |
| `STRATEGIE_MARKETING.md`, `guides/` | étape 7 |
| `BUSINESS_PLAN_VIABILITE.md`, `ETUDE_MARCHE.md` | pour piloter |
