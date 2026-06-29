# SOLEA — Hub de découverte (amateurs de pieds)

> **Le modèle malin** : tu ne crées pas de contenu et tu n'héberges rien.
> Tu construis **la destination** où les amateurs de pieds atterrissent, et tu monétises le **trafic**.
> Simple, original, semi-passif, aucun anonymat à gérer.

---

## 📦 Ce qu'il y a dans ce dossier

- `index.html` — le site complet, **autonome** (rien à installer). Ouvre-le dans un navigateur pour le voir.
  - Age-gate 18+ obligatoire ✅
  - Catégories par style ✅
  - Grille de créateurs avec **boutons affiliés** ✅
  - Capture d'emails (newsletter) ✅
  - Emplacements publicitaires ✅
  - Pied de page légal (CGU, confidentialité, DMCA, 18+) ✅

## 💰 Comment ça rapporte (3 leviers)

### 1. Affiliation (le principal — récurrent)
Les plateformes paient une commission quand un visiteur s'inscrit via ton lien :
- **FeetFinder** — programme d'affiliation (commission sur les inscriptions).
- **OnlyFans / Fansly** — liens de parrainage créateurs.
- Régies d'affiliation adultes (ex. réseaux CPA) qui regroupent plein d'offres.

👉 **Où mettre tes liens** : dans `index.html`, bloc `const creators = [...]`, remplace chaque
`url:"#"` par TON lien affilié. C'est la seule chose vraiment importante à faire.

### 2. Publicité display
Les deux blocs `Emplacement publicitaire` se remplacent par le script d'une **régie pub adulte**
(réseaux spécialisés qui paient au CPM / clic). Tu colles leur script, c'est tout.

### 3. La newsletter (ton actif n°1 sur le long terme)
Chaque email capturé = un client que tu peux re-toucher gratuitement. Branche le formulaire à
**Brevo**, **Mailchimp** ou **Formspree** (gratuit au début). Voir « À connecter » plus bas.

## 🚀 Mettre en ligne gratuitement (5 min)

Choisis-en un, tous gratuits :
- **Cloudflare Pages** : crée un projet, glisse le dossier `feet-hub`. (J'ai un accès Cloudflare ici, je peux t'aider à le déployer.)
- **Netlify** : va sur app.netlify.com → "Add new site" → "Deploy manually" → glisse le dossier.
- **Vercel** : `vercel` en ligne de commande, ou import du repo.

Ensuite, achète un nom de domaine court (~10 €/an, ex. `solea.fr` ou `.co`) et branche-le.

## 🔧 À connecter (checklist)

| Élément | Où | Comment |
|---|---|---|
| Liens affiliés | `index.html` → `const creators` | Remplace `url:"#"` par tes liens |
| Pub | `index.html` → `.ad-slot` | Colle le script de la régie |
| Newsletter | `index.html` → `<form>` | Mets l'`action` vers Brevo/Mailchimp/Formspree |
| Pages légales | liens du footer | Rédige CGU / confidentialité / DMCA (modèles gratuits en ligne) |
| Vrais visuels | `.thumb` des cartes | Remplace l'initiale par une vignette **non explicite** fournie par le créateur |

## ⚖️ Légal — à respecter (important)

- **18+** : l'age-gate est en place. Ne le retire jamais.
- **N'héberge aucun contenu explicite** sur ton site : tu **liens** seulement vers les
  plateformes officielles. C'est ce qui te garde simple et en règle.
- Affiche des **pages légales** (CGU, confidentialité, DMCA, mentions légales).
- Déclare tes revenus (auto-entrepreneur en France).
- Respecte le règlement des programmes d'affiliation (liens en `rel="sponsored nofollow"` — déjà fait).

## 📈 Comment amener du trafic (le vrai travail)

Le site est l'outil ; le trafic, c'est le nerf de la guerre :
1. **SEO** : des pages-guides (« où regarder du contenu pieds en 2026 », « X créateurs à suivre »)
   → tu te positionnes sur Google sur une niche peu concurrentielle.
2. **Reddit / X** : partage tes guides et sélections (entonnoir gratuit vers le site).
3. **Newsletter** : recapture et fidélise.

> 80 % du succès = trafic + bons liens affiliés. Le site est déjà prêt. À toi de l'alimenter.

---

### Prochaines étapes que je peux faire pour toi
- Le **déployer en ligne** (Cloudflare Pages) pour que tu aies une vraie URL.
- Coder les **pages-guides SEO** (le moteur à trafic).
- Te rédiger les **pages légales** (CGU, confidentialité, DMCA).
- Brancher la **newsletter** (Brevo/Formspree).
