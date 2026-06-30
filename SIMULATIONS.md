# 3 simulations — niches mal servies, MVP < 2h, budget mini

> Cadrage honnête : une niche « zéro concurrent » n'existe presque jamais.
> Quand personne n'y est, c'est en général qu'il n'y a pas d'argent. On vise
> donc des **niches mal servies** : demande réelle + outils existants vieillots,
> moches ou hors de prix. Tous les chiffres ci-dessous sont **prudents** et
> servent à décider, pas à rêver.

Hypothèses budget : hébergement Vercel **gratuit** (apps 100% client), seul coût
fixe = nom de domaine **~12 €/an**. Paiement via **Stripe / Lemon Squeezy**
(pas d'abonnement, commission ~5% au prélèvement). Aucun stock, aucune logistique.

---

## Niche A — « Motif Studio » : photo → patron de broderie / perles ⭐ RETENUE

**Le problème** : les passionnés de point de croix, Hama/Perler beads, diamond
painting et pixel-art veulent transformer une photo en *patron* (grille +
symboles + légende des fils/couleurs à acheter). Les outils existants sont
souvent des reliques (ères Flash), moches, en anglais, ou facturent un
abonnement absurde pour un usage ponctuel.

**Pourquoi ça paie** : deux populations qui sortent déjà la carte bleue —
1. les **hobbyistes** qui veulent un PDF imprimable propre tout de suite ;
2. les **vendeurs Etsy** qui revendent des patrons (5–20 €/patron) et ont
   besoin de les générer en série.

**Modèle** : freemium. Gratuit = aperçu + petite grille + export PNG filigrané.
Payant = **4,99 € à l'unité** (PDF imprimable, grande grille, légende complète)
ou **6 €/mois** illimité pour les vendeurs.

**Simulation prudente (mois 3, après un peu de SEO + posts Pinterest)**

| Trafic / mois | Taux conv. | Ventes unité (4,99 €) | Abos (6 €) | Revenu brut | Net (~-5%) |
|---|---|---|---|---|---|
| 1 500 visites | 1,5 % | ~18 × 4,99 | 4 abos | ~114 € | ~108 € |
| 5 000 visites | 2,0 % | ~80 × 4,99 | 12 abos | ~471 € | ~447 € |
| 15 000 visites | 2,5 % | ~280 × 4,99 | 35 abos | ~1 607 € | ~1 527 € |

Coûts mensuels : ~1 € (domaine amorti). **Marge quasi totale.**
**Court terme** : ventes à l'unité dès le 1er visiteur convaincu.
**Long terme** : SEO « générateur patron point de croix / perles » + base de
vendeurs Etsy abonnés (revenu récurrent).

**Faisabilité < 2h** : ★★★★★ — tout se fait dans le navigateur (Canvas),
aucun back-end, aucun coût variable. C'est celle que je construis.

---

## Niche B — « StickerSheet » : planches d'autocollants imprimables à la demande

**Le problème** : micro-boutiques Etsy/Instagram et orthophonistes/instits
veulent générer des *planches d'autocollants* (A4, marges de découpe, motifs
répétés, tailles calibrées pour les machines Cricut/Silhouette). Les outils
généralistes (Canva) ne calibrent pas les marges de découpe → galère.

**Pourquoi ça paie** : gain de temps direct pour des gens qui vendent déjà.
**Modèle** : 3,99 €/planche exportée en PDF calibré, ou 8 €/mois.

**Simulation prudente (mois 3)**

| Trafic / mois | Conv. | Revenu brut | Net |
|---|---|---|---|
| 1 000 | 1,5 % | ~60 € | ~57 € |
| 4 000 | 2,0 % | ~320 € | ~304 € |
| 10 000 | 2,5 % | ~800 € | ~760 € |

**Faisabilité < 2h** : ★★★★ — Canvas + génération PDF. Un cran plus complexe
que A à cause du calibrage d'impression (mm réels).

---

## Niche C — « Pochette d'album » : générateur de visuels « vinyle/cassette » rétro

**Le problème** : musiciens indés et créateurs de playlists veulent une pochette
stylée (vinyle, cassette, polaroid) à partir d'une image, sans Photoshop.
**Pourquoi ça paie** : sortie de single = besoin ponctuel, achat impulsif.
**Modèle** : 2,99 € l'export HD sans filigrane.

**Simulation prudente (mois 3)**

| Trafic / mois | Conv. | Revenu brut | Net |
|---|---|---|---|
| 2 000 | 2 % | ~120 € | ~114 € |
| 8 000 | 3 % | ~717 € | ~681 € |

**Faisabilité < 2h** : ★★★★ — Canvas + filtres. Marché plus volatil (tendances).

---

## Décision

**On construit A (Motif Studio).** Meilleur rapport
*demande prouvée × faisabilité immédiate × marge × récurrence possible*, et
100 % côté client donc **0 € de coût serveur**. Le code de l'aperçu et de la
génération de grille est livré dans ce repo (`/studio`).

### Ce qui te restera à faire (minimal)
1. Acheter un domaine (~12 €) et brancher Vercel (gratuit) — 15 min.
2. Coller une clé Stripe/Lemon Squeezy pour activer le bouton « PDF 4,99 € ».
3. 3 épingles Pinterest + 1 post dans 2 groupes FB de point de croix / Hama.

Tout le reste (l'outil) est automatisé.
