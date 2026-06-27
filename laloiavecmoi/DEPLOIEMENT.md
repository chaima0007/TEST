# 🚀 Mettre « La Loi Avec Moi » en ligne — guide ultra-simple

> À faire quand tu es reposée. **5 minutes, 6 étapes.** Rien d'autre à préparer :
> le site est déjà construit et testé (build ✓). Aucun risque pour ton code.

## Les étapes (sur vercel.com)

1. **Va sur la liste de tes projets** : en haut à gauche, clique sur **« Projets de chaima… »**.
2. En haut à **droite**, clique le bouton noir **« Add New… » → « Project »**.
3. **Importe le dépôt** : `chaima0007/TEST`.
4. ⭐ **LE point clé** — déplie **« Root Directory »** → **Edit** → choisis le dossier **`laloiavecmoi`**.
5. Déplie **« Git » → Production Branch** → mets : `claude/swarm-50-agent-architecture-3l6cno`
6. Clique **« Deploy »** 🎉

→ Au bout de ~2 min : une adresse type `laloiavecmoi-xxx.vercel.app` qui affiche
**uniquement** ton site juridique (page d'accueil « La Loi Avec Moi », **zéro Caelum**).

## Après (optionnel)
- **Nom de domaine** : Project → Settings → **Domains** → ajoute `laloiavecmoi.be`.
- **Mettre à jour l'e-mail de contact** : fichier `app/contact/page.tsx` (placeholder `contact@laloiavecmoi.be`).

## En cas de souci
- Si le bouton « Add New » est introuvable : tu es sans doute *à l'intérieur* d'un projet.
  Reviens à la **liste des projets** (clic sur le nom de l'équipe en haut à gauche).
- Le confirmateur de suppression Vercel demande de taper `delete my project`
  **sans les guillemets**.

## Note technique
Le code de ce site vit pour l'instant dans le dépôt `chaima0007/TEST`, dans le dossier
`laloiavecmoi/`. Le **site déployé** est 100% indépendant (Root Directory = `laloiavecmoi`).
Plus tard, on pourra déplacer ce dossier dans son propre dépôt si tu le souhaites.
