# Site Moonbow SAS

Site vitrine + démonstration du futur portail de supervision, pour le
projet étudiant de modernisation IT de Moonbow SAS.

- `public/` : site statique (vitrine, page de connexion, tableau de bord démo).
- `backend/` : serveur Node.js (Express) qui sert le site et expose une API
  (formulaire de contact, connexion, métriques d'infrastructure simulées),
  avec une base SQLite locale (`backend/moonbow.db`, créée automatiquement).

## Lancer en local

```bash
cd backend
npm install
npm start
```

Puis ouvrir http://localhost:4000

Identifiants de démonstration pour le portail (`/login.html`) :
- Identifiant : `admin`
- Mot de passe : `moonbow2026`

## Déploiement

Pas encore déployé en ligne (pas de nom de domaine / hébergement choisi).
Le code est prêt pour être déployé sur n'importe quel hébergeur Node.js
(ex: Render, Railway, Fly.io) : il suffit de définir `PORT` et
`SESSION_SECRET` en variables d'environnement.
