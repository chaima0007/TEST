# SOLEA — Être payé en 3 clics

> SOLEA touche sa commission (FeetFinder 25 % + 5 % récurrent) dès qu'un visiteur clique vers un créateur via un lien `?ref=CODE` et s'inscrit. Tout est conçu pour que ce clic arrive vite, sans friction, sans dark pattern.

## Le parcours en 3 clics

**Clic 0 — Age-gate (non compté)** : mémorisé en `localStorage` → ne réapparaît plus.

**Chemin EXPRESS (par défaut)**
1. **Clic 1** : carte créateur sur l'accueil → c'est un lien affilié (`?ref=SOLEA_CODE`), ouvre la page du créateur chez le partenaire (nouvel onglet).
2. **Clic 2** : bouton « S'inscrire pour voir » chez le partenaire.
3. **Clic 3** : paiement → **SOLEA encaisse**.

**Chemin EXPLORATEUR**
1. **Clic 1** : une catégorie / un chip → redirection immédiate vers une recherche partenaire pré-filtrée.
2. **Clic 2** : un créateur chez le partenaire.
3. **Clic 3** : paiement.

## Convention d'URL de tracking (unique)
```
https://feetfinder.com/{slug}?ref=SOLEA_CODE&utm_source=solea&utm_medium=affiliate&utm_campaign={emplacement}
recherche : https://feetfinder.com/search?ref=SOLEA_CODE&tags={tags}
```
- `ref=SOLEA_CODE` = **le seul paramètre qui paie** (remplace par ton vrai code).
- `utm_campaign` : `card_home`, `cat_home`, `explorer_chip`, `selbar` → savoir ce qui convertit.

## Config centrale (déjà câblée dans index.html & category.html)
```js
const AFF = {
  base:"https://feetfinder.com", ref:"SOLEA_CODE",
  link(slug,c){return `${this.base}/${slug}?ref=${this.ref}&utm_source=solea&utm_medium=affiliate&utm_campaign=${c}`},
  search(tags,c){return `${this.base}/search?ref=${this.ref}&tags=${encodeURIComponent(tags)}&utm_source=solea&utm_medium=affiliate&utm_campaign=${c}`}
};
```
➡️ **La seule chose critique : remplacer `ref:"SOLEA_CODE"` par ton vrai code FeetFinder** dans `index.html` et `category.html`.

## 5 règles UX anti-friction
1. L'age-gate ne coûte qu'une fois (mémorisé).
2. Zéro `alert`, zéro pop-up bloquant, zéro écran SOLEA intermédiaire.
3. Toute la carte est cliquable (pas juste le bouton) — cibles ≥ 44 px sur mobile.
4. Toujours un chemin « 1 clic = je pars » ; composer une sélection reste un bonus, jamais un péage.
5. Nouvel onglet + `rel="noopener nofollow sponsored"` (transparent, conforme).
