# SOLEA — Guide : trouver le contenu & le mettre en ligne

> Rappel : **SOLEA n'héberge AUCUN contenu.** « Mettre le contenu » = ajouter des **fiches de
> créateurs** qui pointent (via TON lien d'affiliation) vers leurs profils sur la plateforme.
> Tu ne stockes ni photo ni vidéo : tu **références** et tu **renvoies**.

---

## PARTIE 1 — OÙ TROUVER LE CONTENU (les créateurs à référencer)

### Étape 1 — T'inscrire au programme d'affiliation (obligatoire d'abord)
Sans code d'affiliation, tu peux référencer des créateurs mais **tu ne gagnes rien**.
1. Va sur **FeetFinder** → cherche « Affiliate / Referral program » (en bas de page ou dans l'aide).
2. Inscris-toi → tu reçois un **code** (ex. `MONCODE`) et/ou un lien de parrainage.
3. Note aussi le **format de lien créateur** : généralement `feetfinder.com/<pseudo>?ref=MONCODE`.

### Étape 2 — Trouver des créateurs à lister (légalement)
Tu listes **uniquement** des créateurs qui se promeuvent déjà publiquement (donc consentants
à être trouvés) :
- **Sur la plateforme partenaire** : parcours les profils publics/populaires de la niche.
- **Reddit** : `r/FeetFinderPromo`, `r/VerifiedFeet`, `r/feetpics` — des créatrices **postent
  elles-mêmes** leur profil pour être trouvées. C'est la meilleure source.
- **X (Twitter)** : hashtags `#footfetish #feetpics #FeetFinder` → profils publics.

> ⚠️ **Règles d'or** (déjà dans `GUIDE_CONTENU` et la recherche d'audience) :
> - Seulement des créateurs **majeurs et consentants** qui se promeuvent publiquement.
> - **Jamais** de célébrités, de personnes réelles non consentantes, ni de contenu volé.
> - Idéalement, **demande l'accord** (DM) pour les référencer → certains te donneront même
>   une vignette promo et relaieront ton lien (effet réseau).

### Étape 3 — Pour chaque créateur, récupère 3 infos
1. **Le pseudo / slug** (ex. `lina`) → pour construire le lien.
2. **Son style** (ex. « Bas & collants ») → pour le ranger dans une catégorie.
3. **(optionnel) une vignette promo** qu'il/elle te fournit avec accord.

---

## PARTIE 2 — OÙ COLLER LE CONTENU DANS LE SITE (fichier + ligne)

### A) Les cartes « Créateurs à découvrir » de l'accueil → `index.html`
Cherche le bloc `creators:` (il y en a **deux** : la version FR et la version EN, dans `I18N`).
Chaque créateur est une ligne : `["Nom","Style","Tag","slug"]`.

**Pour ajouter/modifier un créateur**, édite ces lignes :
```js
creators:[
  ["Lina","Luxe & bijoux","Populaire","lina"],     // ← remplace par un vrai pseudo
  ["Aurélie","Épuré & marbre","Nouveau","aurelie"],
  // ... ajoute autant de lignes que tu veux
],
```
- `slug` = le pseudo utilisé dans le lien `feetfinder.com/<slug>?ref=...`.
- Le `Tag` est facultatif (`""`, `"Nouveau"`, `"Populaire"`, `"VIP"`, `"Tendance"`).
- Mets à jour **les deux** listes (`fr` et `en`) pour rester bilingue.

### B) Le code d'affiliation (à mettre UNE fois par fichier)
Dans `index.html`, `category.html`, `creators.html`, `diapason.html`, `collections.html`,
cherche `ref:"SOLEA_CODE"` et remplace **`SOLEA_CODE` par ton vrai code**. C'est ce qui te paie.
> Astuce : un simple « rechercher-remplacer » de `SOLEA_CODE` → `MONCODE` dans le dossier `feet-hub/`.

### C) Les « Collections » hebdo → `collections.html`
Cherche le tableau `const COLLECTIONS = [ ... ]`. Pour publier une nouvelle collection, **copie un
objet en haut de la liste** et change les champs :
```js
{num:15, titre_fr:"Soie & Or", titre_en:"Silk & Gold", date:"2026-07-03",
 intro_fr:"…", intro_en:"…", tags:["Soie / draps","Bagues d'orteil","Luxe / glamour"]},
```
Les `tags` doivent correspondre aux catégories de l'Explorateur (sinon la recherche ne filtre rien).

### D) Les catégories / l'Explorateur → déjà rempli
Les **centaines de catégories** sont déjà dans `explorer.html` et `category.html`
(familles : état, mise en scène, soin, tenue, angle, etc.). Tu n'as rien à ajouter,
sauf si tu veux une nouvelle catégorie : ajoute son libellé dans la bonne famille.

---

## PARTIE 3 — CHECKLIST « mettre le contenu aujourd'hui »
1. [ ] S'inscrire au programme d'affiliation → récupérer **MONCODE**.
2. [ ] Remplacer `SOLEA_CODE` → `MONCODE` dans les 5 fichiers HTML.
3. [ ] Trouver 8–15 créateurs (Reddit `r/FeetFinderPromo`, plateforme, X) → noter pseudo + style.
4. [ ] Les ajouter dans `creators:` (FR **et** EN) de `index.html`.
5. [ ] (option) Créer la **Collection №15** de la semaine dans `collections.html`.
6. [ ] Ouvrir `index.html` dans un navigateur → vérifier que « Voir le profil » ouvre le bon lien.
7. [ ] (quand tu veux) Déployer (voir `LANCEMENT.md`).

> Tu m'envoies la liste (pseudo + style + ton code) → **je remplis tout le code pour toi** et je commite.
