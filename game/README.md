# Open City — prototype de jeu

Prototype open-world (voiture + ville + missions + police), inspiré de GTA,
en Three.js pur (modules ES, sans étape de build).

## Jouer en local (PC)

```bash
cd game
python3 -m http.server 8000
```

Puis ouvrir http://localhost:8000 dans le navigateur.

## Jouer sur téléphone Android (avec Python/Termux)

1. Installer [Termux](https://termux.com/) puis `pkg install python`.
2. Copier ou cloner ce dossier `game/` sur le téléphone.
3. Dans Termux :
   ```bash
   cd game
   python -m http.server 8000
   ```
4. Ouvrir un navigateur sur le même téléphone et aller sur
   http://localhost:8000

Pas besoin de réseau Wi-Fi partagé : le serveur et le navigateur tournent sur
le même appareil. Les contrôles tactiles (volant/accélérateur/frein à
l'écran) s'affichent automatiquement sur mobile.

## Commandes (clavier, sur PC)

- Flèches / ZQSD : direction et accélération
- Espace : frein à main
- P ou Échap : pause

## Tests automatisés

```bash
cd game
npm install   # aucune dépendance réelle, prépare juste le shim de test
npm test
```

Suite `node --test` qui vérifie la génération du monde, la physique du
véhicule, le système de police/recherché et les missions, indépendamment du
rendu 3D.
