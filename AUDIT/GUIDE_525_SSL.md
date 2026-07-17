# Guide — Corriger l'erreur SSL 525 sur caelumpartners.agency
> Projet : site web Caelum · Domaine : `caelumpartners.agency`
> Rédigé : 2026-07-13 · Réversible à chaque étape.

## Ce qu'est vraiment l'erreur 525 (en clair)
« 525 » = la poignée de main SSL **entre Cloudflare et le serveur d'origine échoue**.
- Toi ✅  →  Cloudflare ✅  →  Serveur d'origine ❌
- Ton mode SSL Cloudflare « Full » est **bon**, on n'y touche pas.
- Le blocage : l'origine ne présente pas encore de **certificat HTTPS valide** à Cloudflare.

⚠️ Ça se corrige dans des **tableaux de bord** (Cloudflare + hébergeur), pas dans le code.
Aucune étape ci-dessous n'est définitive : tout est réversible.

---

## ÉTAPE 0 — D'abord : où le site est-il vraiment hébergé ?
Un 525 se répare différemment selon l'origine. Regarde dans cet ordre :
- **GitHub Pages** → repo `chaima0007/keywordmoneymaker` → onglet **Settings → Pages**.
  S'il y a un « Custom domain » et un déploiement Pages → c'est **le cas A** (le plus courant).
- **Cloudflare Worker/Pages** → dashboard Cloudflare → **Workers & Pages** → projet
  `autumn-credit-409b` → onglet **Custom Domains** → c'est **le cas B**.

Dis-moi lequel tu vois, et on suit la bonne colonne.

---

## CAS A — Le site est sur GitHub Pages

1. **GitHub → repo `keywordmoneymaker` → Settings → Pages**
   - Champ **Custom domain** : mets `caelumpartners.agency` → **Save**.
   - (GitHub ajoute un fichier `CNAME` dans le repo, c'est normal.)

2. **Laisser GitHub fabriquer son certificat** (l'étape clé du 525)
   - Va dans **Cloudflare → DNS**.
   - Sur l'enregistrement de `caelumpartners.agency`, clique le **nuage orange** pour le
     passer en **nuage gris = « DNS only »** (temporairement).
   - Pourquoi : tant que Cloudflare masque l'origine, GitHub ne peut pas vérifier le domaine
     ni générer son certificat Let's Encrypt. En « DNS only », GitHub voit le domaine et
     provisionne le certificat.

3. **Attendre le certificat**
   - Retourne sur **GitHub → Settings → Pages**.
   - Attends le message vert **« Your site is published at https://… »** et que la case
     **« Enforce HTTPS »** devienne **cliquable** (quelques minutes, parfois jusqu'à 24 h).
   - Coche **« Enforce HTTPS »**.

4. **Rallumer la protection Cloudflare**
   - **Cloudflare → DNS** : repasse le nuage **gris → orange** (proxy réactivé).
   - **Cloudflare → SSL/TLS** : garde le mode sur **« Full »** (ou « Full (strict) »
     maintenant qu'un vrai certificat existe).

5. **Vérifier** → va sur `https://caelumpartners.agency`
   - ✅ Page qui s'affiche, cadenas fermé, **plus de 525**. Terminé.

---

## CAS B — Le site est sur un Worker / Cloudflare Pages

1. **Cloudflare → Workers & Pages → ton projet (`autumn-credit-409b`)**
2. Onglet **Custom Domains → Add Custom Domain** → `caelumpartners.agency`.
   - Cloudflare rattache le domaine et **génère automatiquement un certificat valide**.
3. Attends que le statut passe à **« Active »**.
4. **Vérifier** → `https://caelumpartners.agency` → ✅ 200 + cadenas, plus de 525.

---

## Si ça bloque encore
- 525 qui persiste après le cas A → le certificat n'est pas encore prêt : attends, puis
  recoche « Enforce HTTPS ». Ne remets PAS le proxy orange avant que le certificat existe.
- Erreur **526** = « Full (strict) » avec un certificat non valide → repasse en « Full ».
- Toujours coincée → note l'écran exact (capture) et on regarde ensemble.

## Règle de sécurité
On ne clique jamais au hasard. Une étape = un écran = une vérification.
Tout est réversible : le nuage se rebascule, la case se décoche, rien n'est cassé.
