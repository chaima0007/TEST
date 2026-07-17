# Nous 🤍

Une petite app **mobile-first** et **locale** pour les couples et futurs couples :
comprendre les limites de l'autre et mieux communiquer, en s'adaptant à
l'humeur, au rythme du corps (cycle) et aux sensibilités de chacun.

> Projet personnel, prototype de démonstration. **Toutes les données pré-remplies
> sont fictives.**

## Ce que fait le MVP

- **Aujourd'hui** — check-in humeur / énergie, « code couleur » d'ambiance,
  signaux *« J'ai besoin de… »* (un seul tap), phase du cycle du jour et
  rituel suggéré.
- **Repères** — carte des limites & consentement (Oui / Peut-être / Non) et
  liste des allergies & sensibilités. Pour *comprendre les limites de l'autre*.
- **Rituels** — guides de dialogue fondés sur des approches reconnues
  (Communication NonViolente de Rosenberg, méthode Gottman, consentement FRIES)
  + un **traducteur** qui transforme un ressenti brut en message en « je ».
- **Réglages** — cycle (activable), prénoms, sources, confidentialité, reset.

## Local-first & vie privée

Aucun serveur, aucun compte : tout est stocké **dans le navigateur**
(`localStorage`). Pour une app aussi intime, la donnée ne quitte jamais
l'appareil.

## Sources

Le contenu s'appuie sur des cadres établis, sans invention : CNV (M. Rosenberg,
modèle OSBD), méthode Gottman (démarrage en douceur, pause, bilan de couple),
modèle de consentement FRIES (Planned Parenthood), et une description générale
des phases du cycle menstruel (information de bien-être, non médicale).

## Démarrer

```bash
npm install
npm run dev
```

Puis ouvrir [http://localhost:3000](http://localhost:3000).

## Stack

Next.js 16 (App Router) · React 19 · TypeScript · Tailwind CSS v4.
Voir `AGENTS.md` : ce projet utilise des versions dont les conventions diffèrent.
