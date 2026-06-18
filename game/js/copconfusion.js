// copconfusion.js — Agent Confusion Policière
// Quand le wanted ≥ 2, une voiture de police se trompe de cible et poursuit
// une voiture civile innocente pendant quelques secondes, avec un message HUD
// hilarant. La voiture confuse clignote en orange dans main.js.
// Aucune dépendance Three.js.

const CONFUSION_CHANCE  = 0.0018; // par frame à 60fps ≈ toutes les ~9 min
const CONFUSION_DURATION = 9;     // secondes de confusion
const MSG_DURATION       = 4.0;   // durée d'affichage du message

const MESSAGES = [
  'Agent 08 : cible confondue avec un livreur de pizza !',
  'Dispatch : on perd la Peugeot… c\'était une poussette.',
  'GPS en panne — poursuivons ce foodtruck suspect.',
  'Rapport : la "Ferrari" était un vélo avec des LEDs.',
  'Unité 3 prend en chasse… un pigeon avec une casquette.',
  'Erreur système : j\'ai visé le boulanger. Désolé.',
  'HQ, le suspect vient de muter en camionnette blanche.',
  'Alerte : suspect porté disparu. Était devant nous.',
];

export class CopConfusionAgent {
  constructor() {
    this._confused    = false;
    this._timer       = 0;
    this._fakeTarget  = null;  // { x, z } de la voiture civile confondue
    this._confusedCar = null;  // mesh du policier confus
    this._pendingMsg  = null;  // message à afficher (consommé une fois)
    this._msgTimer    = 0;
    this._confusionCount = 0;
  }

  update(dt, wantedLevel, policeCars, trafficCars) {
    this._pendingMsg = null;

    if (this._msgTimer > 0) this._msgTimer -= dt;

    if (this._confused) {
      this._timer -= dt;

      // Met à jour la position du faux objectif si la voiture civile bouge
      if (this._fakeTarget && this._confusedCarRef?.mesh) {
        this._fakeTarget.x = this._confusedCarRef.mesh.position.x;
        this._fakeTarget.z = this._confusedCarRef.mesh.position.z;
      }

      if (this._timer <= 0) {
        this._confused      = false;
        this._fakeTarget    = null;
        this._confusedCar   = null;
        this._confusedCarRef = null;
        this._pendingMsg    = 'Agent 08 : cible retrouvée. Reprise en chasse !';
        this._msgTimer      = MSG_DURATION;
      }
    } else if (
      wantedLevel >= 2 &&
      policeCars.length > 0 &&
      trafficCars.length > 0 &&
      Math.random() < CONFUSION_CHANCE
    ) {
      // Choisit une voiture civile proche au hasard
      const civilian = trafficCars.filter(c => c.active && c.mesh);
      if (civilian.length === 0) return;

      const target  = civilian[Math.floor(Math.random() * civilian.length)];
      const copMesh = policeCars[Math.floor(Math.random() * policeCars.length)]?.mesh;

      if (target && copMesh) {
        this._confused       = true;
        this._timer          = CONFUSION_DURATION;
        this._fakeTarget     = { x: target.mesh.position.x, z: target.mesh.position.z };
        this._confusedCar    = copMesh;
        this._confusedCarRef = target;
        this._pendingMsg     = MESSAGES[Math.floor(Math.random() * MESSAGES.length)];
        this._msgTimer       = MSG_DURATION;
        this._confusionCount++;
      }
    }
  }

  isConfused()         { return this._confused; }
  getFakeTarget()      { return this._fakeTarget; }
  getConfusedCar()     { return this._confusedCar; }  // mesh du policier confus
  popMessage()         { const m = this._pendingMsg; this._pendingMsg = null; return m; }
  hasPendingMessage()  { return this._pendingMsg !== null; }
  getMsgTimer()        { return this._msgTimer; }
  getTimeLeft()        { return Math.max(0, this._timer); }
  getConfusionCount()  { return this._confusionCount; }
}
