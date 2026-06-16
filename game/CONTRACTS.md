# Open City — interfaces entre modules

Prototype de jeu open-world (voiture + ville + missions), inspiré de GTA, en
Three.js pur (ES modules, pas de build step). Chaque fichier ci-dessous est
développé indépendamment ; ces interfaces sont le contrat à respecter pour
que tout s'assemble sans conflit dans `main.js`.

## `world.js`
```js
export function createWorld(scene) {
  // Ajoute sol, routes, bâtiments, lampadaires, etc. à la scène.
  // Retourne :
  return {
    colliders: [ { x, z, halfWidth, halfDepth } /* AABB au sol, axes XZ */ ],
    spawnPoint: { x, z, rotationY },
    missionLocations: [ { name: string, x, z } ], // au moins 3 points nommés
  };
}
```

## `vehicle.js`
```js
export class Vehicle {
  constructor(scene, spawnPoint) {} // crée le mesh (boîte/voiture basse-poly), this.mesh, position initiale = spawnPoint
  update(dt, input, colliders) {}   // applique accélération/direction/friction, résout collisions AABB simples, met à jour this.mesh
  getPosition() {}                  // { x, z }
  getSpeedKmh() {}                  // nombre, pour le HUD
  getHeading() {}                   // radians, direction actuelle
}
```

## `camera.js`
```js
export function createFollowCamera(renderer) {}      // retourne THREE.PerspectiveCamera configurée
export function updateFollowCamera(camera, vehicle, dt) {} // caméra 3e personne, suit fluide derrière la voiture
```

## `missions.js`
```js
export class MissionManager {
  constructor(world, hud) {}            // utilise world.missionLocations
  update(dt, vehicle) {}                // détecte arrivée sur checkpoint, passe à la mission suivante, appelle hud.setMission / hud.showMessage
  getCurrentMission() {}                // { name, targetX, targetZ } | null si terminé
}
```

## `police.js`
```js
export class WantedSystem {
  constructor(scene, world) {}
  update(dt, vehicle, hud) {}  // augmente le niveau si vitesse excessive / collisions répétées,
                                // fait apparaître 1-3 voitures de police qui poursuivent le joueur (IA simple : se dirigent vers vehicle.getPosition()),
                                // appelle hud.setWanted(level 0-5)
}
```

## `hud.js`
```js
export class HUD {
  constructor(rootEl) {}        // construit l'overlay DOM dans #hud-root (vitesse, mission, étoiles wanted)
  setSpeed(kmh) {}
  setMission(text) {}
  setWanted(level) {}           // 0 à 5 étoiles
  showMessage(text, durationMs) {} // toast temporaire (ex: "Mission terminée !")
}
```

## Boucle principale (`main.js`, déjà écrit)
```js
import * as THREE from 'three';
import { createWorld } from './world.js';
import { Vehicle } from './vehicle.js';
import { createFollowCamera, updateFollowCamera } from './camera.js';
import { InputManager } from './input.js';
import { MissionManager } from './missions.js';
import { WantedSystem } from './police.js';
import { HUD } from './hud.js';

// scene, renderer, world = createWorld(scene), vehicle = new Vehicle(...),
// camera = createFollowCamera(renderer), input = new InputManager(),
// hud = new HUD(...), missions = new MissionManager(world, hud),
// wanted = new WantedSystem(scene, world)
// boucle: vehicle.update(dt, input, world.colliders); updateFollowCamera(...);
//         missions.update(dt, vehicle); wanted.update(dt, vehicle, hud);
//         hud.setSpeed(vehicle.getSpeedKmh()); renderer.render(scene, camera);
```

Unités : 1 unité Three.js ≈ 1 mètre. Sol sur le plan XZ, Y = hauteur.
Aucune dépendance externe autre que `three` (déjà en importmap dans `index.html`).
