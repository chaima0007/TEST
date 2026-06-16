// MissionManager — cycle de checkpoints séquentiels basés sur world.missionLocations.
// Boucle indéfiniment : arrivée sur la cible -> message de succès -> cible suivante.

const ARRIVAL_RADIUS = 6; // mètres, distance pour valider un checkpoint

export class MissionManager {
  constructor(world, hud) {
    this.world = world;
    this.hud = hud;
    this.locations = (world && world.missionLocations) || [];
    this.currentIndex = this.locations.length > 0 ? 0 : -1;

    if (this.currentIndex >= 0) {
      this._announceCurrent(false);
    } else if (this.hud) {
      this.hud.setMission('Aucune mission disponible');
    }
  }

  _announceCurrent(isAdvance) {
    const loc = this.locations[this.currentIndex];
    if (!loc || !this.hud) return;
    this.hud.setMission(`Livraison : ${loc.name}`);
    if (isAdvance) {
      this.hud.showMessage(`Direction : ${loc.name}`, 2000);
    }
  }

  update(dt, vehicle) {
    if (this.currentIndex < 0 || this.locations.length === 0) return;
    if (!vehicle || typeof vehicle.getPosition !== 'function') return;

    const target = this.locations[this.currentIndex];
    const pos = vehicle.getPosition();
    const dx = pos.x - target.x;
    const dz = pos.z - target.z;
    const distSq = dx * dx + dz * dz;

    if (distSq <= ARRIVAL_RADIUS * ARRIVAL_RADIUS) {
      if (this.hud) {
        this.hud.showMessage(`Livraison réussie : ${target.name} !`, 2500);
      }
      this.currentIndex = (this.currentIndex + 1) % this.locations.length;
      this._announceCurrent(true);
    }
  }

  getCurrentMission() {
    if (this.currentIndex < 0 || this.locations.length === 0) return null;
    const loc = this.locations[this.currentIndex];
    return { name: loc.name, targetX: loc.x, targetZ: loc.z };
  }
}
