// MissionManager — cycle de missions variées basées sur world.missionLocations.
// Types de mission : livraison simple, livraison chronométrée (échec si le
// temps est écoulé), et chaîne de checkpoints à enchaîner rapidement.
// Boucle indéfiniment, en alternant les types ; chaque réussite rapporte des
// points/argent exposés via getScore().

const ARRIVAL_RADIUS = 6; // mètres, distance pour valider un checkpoint

const TYPE_DELIVERY = 'delivery';
const TYPE_TIMED = 'timed';
const TYPE_CHAIN = 'chain';

const TIMED_DURATION_S = 30; // secondes accordées pour une livraison chronométrée
const CHAIN_LENGTH = 3; // nombre de checkpoints à enchaîner pour une mission "chain"
const CHAIN_STEP_TIME_S = 12; // secondes accordées par checkpoint de la chaîne

const REWARD_DELIVERY = 100;
const REWARD_TIMED = 200;
const REWARD_CHAIN_STEP = 60;
const REWARD_CHAIN_BONUS = 150; // bonus à la fin de toute la chaîne

function shuffledIndices(length) {
  const arr = Array.from({ length }, (_, i) => i);
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

export class MissionManager {
  constructor(world, hud) {
    this.world = world;
    this.hud = hud;
    this.locations = (world && world.missionLocations) || [];

    this.score = 0;

    this.type = null;
    this.target = null;
    this.timeLeft = 0;
    this.chainStep = 0;
    this.chainOrder = [];

    this._order = shuffledIndices(this.locations.length);
    this._orderPos = 0;
    this._typeCycle = [TYPE_DELIVERY, TYPE_TIMED, TYPE_CHAIN];
    this._typeCycleIndex = 0;

    if (this.locations.length > 0) {
      this._startNextMission(false);
    } else if (this.hud) {
      this.hud.setMission('Aucune mission disponible');
    }
  }

  _nextLocation() {
    if (this._orderPos >= this._order.length) {
      this._order = shuffledIndices(this.locations.length);
      this._orderPos = 0;
    }
    const loc = this.locations[this._order[this._orderPos]];
    this._orderPos++;
    return loc;
  }

  _startNextMission(announce) {
    this.type = this._typeCycle[this._typeCycleIndex];
    this._typeCycleIndex = (this._typeCycleIndex + 1) % this._typeCycle.length;

    if (this.type === TYPE_CHAIN && this.locations.length < 2) {
      // pas assez de points pour une chaîne : retombe sur une livraison simple
      this.type = TYPE_DELIVERY;
    }

    if (this.type === TYPE_DELIVERY) {
      this.target = this._nextLocation();
    } else if (this.type === TYPE_TIMED) {
      this.target = this._nextLocation();
      this.timeLeft = TIMED_DURATION_S;
    } else if (this.type === TYPE_CHAIN) {
      const count = Math.min(CHAIN_LENGTH, this.locations.length);
      this.chainOrder = [];
      for (let i = 0; i < count; i++) this.chainOrder.push(this._nextLocation());
      this.chainStep = 0;
      this.target = this.chainOrder[0];
      this.timeLeft = CHAIN_STEP_TIME_S;
    }

    this._announceCurrent(announce);
  }

  _announceCurrent(announce) {
    if (!this.target || !this.hud) return;

    if (this.type === TYPE_DELIVERY) {
      this.hud.setMission(`Livraison : ${this.target.name}`);
      if (announce) this.hud.showMessage(`Direction : ${this.target.name}`, 2000);
    } else if (this.type === TYPE_TIMED) {
      this.hud.setMission(`Livraison urgente : ${this.target.name} (${Math.ceil(this.timeLeft)}s)`);
      if (announce) this.hud.showMessage(`Chrono lancé : ${this.target.name} !`, 2200);
    } else if (this.type === TYPE_CHAIN) {
      const stepLabel = `${this.chainStep + 1}/${this.chainOrder.length}`;
      this.hud.setMission(`Tournée ${stepLabel} : ${this.target.name} (${Math.ceil(this.timeLeft)}s)`);
      if (announce) this.hud.showMessage(`Tournée lancée : ${this.chainOrder.length} arrêts !`, 2200);
    }
  }

  _addScore(amount) {
    this.score += amount;
    if (this.hud && typeof this.hud.setScore === 'function') {
      this.hud.setScore(this.score);
    }
  }

  _failCurrent(reason) {
    if (this.hud) this.hud.showMessage(reason, 2200);
    this._startNextMission(true);
  }

  update(dt, vehicle) {
    if (!this.target || this.locations.length === 0) return;
    if (!vehicle || typeof vehicle.getPosition !== 'function') return;

    if (this.type === TYPE_TIMED || this.type === TYPE_CHAIN) {
      this.timeLeft -= dt;
      if (this.timeLeft <= 0) {
        this._failCurrent(
          this.type === TYPE_TIMED ? 'Trop tard ! Livraison ratée.' : 'Trop lent ! Tournée ratée.'
        );
        return;
      }
    }

    const pos = vehicle.getPosition();
    const dx = pos.x - this.target.x;
    const dz = pos.z - this.target.z;
    const distSq = dx * dx + dz * dz;

    if (distSq > ARRIVAL_RADIUS * ARRIVAL_RADIUS) {
      // garde le décompte affiché à jour pour les missions chronométrées
      if (this.type === TYPE_TIMED || this.type === TYPE_CHAIN) {
        this._announceCurrent(false);
      }
      return;
    }

    if (this.type === TYPE_DELIVERY) {
      this._addScore(REWARD_DELIVERY);
      if (this.hud) this.hud.showMessage(`Livraison réussie : ${this.target.name} ! (+${REWARD_DELIVERY})`, 2500);
      this._startNextMission(true);
    } else if (this.type === TYPE_TIMED) {
      this._addScore(REWARD_TIMED);
      if (this.hud) this.hud.showMessage(`Livraison express réussie ! (+${REWARD_TIMED})`, 2500);
      this._startNextMission(true);
    } else if (this.type === TYPE_CHAIN) {
      this._addScore(REWARD_CHAIN_STEP);
      this.chainStep++;
      if (this.chainStep >= this.chainOrder.length) {
        this._addScore(REWARD_CHAIN_BONUS);
        if (this.hud) this.hud.showMessage(`Tournée terminée ! (+${REWARD_CHAIN_BONUS})`, 2500);
        this._startNextMission(true);
      } else {
        this.target = this.chainOrder[this.chainStep];
        this.timeLeft = CHAIN_STEP_TIME_S;
        if (this.hud) this.hud.showMessage(`Arrêt suivant : ${this.target.name} (+${REWARD_CHAIN_STEP})`, 2000);
        this._announceCurrent(false);
      }
    }
  }

  getCurrentMission() {
    if (!this.target) return null;
    return { name: this.target.name, targetX: this.target.x, targetZ: this.target.z };
  }

  getScore() {
    return this.score;
  }
}
