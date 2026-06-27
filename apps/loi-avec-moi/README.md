# La Loi Avec Moi — site public

> Projet **séparé** et autonome. Ne se mélange pas avec `competeiq` (CRM à la racine du repo).
> Règle d'or respectée : *rien n'est mélangé*.

## Principe

Le site est **généré à partir d'une source de vérité unique** : les fichiers
JSON vérifiés et certifiés dans `data/belgium/*.json`. Conséquence directe :
le site ne peut **jamais** afficher une information qui n'est pas déjà sourcée
et datée dans la base. Pas de contenu écrit « à la main » dans les pages.

## Construire le site

```bash
python3 apps/loi-avec-moi/build_site.py
```

Sortie : `apps/loi-avec-moi/dist/` (HTML statique, aucune dépendance).

## Ce qui est garanti à chaque build

- Chaque réponse cite **au moins une source officielle** + une **date de vérification**.
- Chaque page contient l'**avertissement** légal.
- Une page **Transparence** liste les engagements et les limites, honnêtement.

## Déploiement

Site 100 % statique → hébergeable partout (Vercel, Netlify, GitHub Pages,
Cloudflare Pages). Aucun secret, aucune base de données à l'exécution.
Pour Vercel : pointer le « output directory » sur `apps/loi-avec-moi/dist`.

## Ce qui N'EST PAS encore là (volontairement, à décider avec Chaima)

- Paiement (Stripe) → nécessite les clés de Chaima, via variables d'environnement (jamais dans le code).
- Nom de domaine + hébergement → au nom de Chaima.
- Versions néerlandaises (NL) du contenu.
