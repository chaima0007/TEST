// district.js — Quartiers de la ville avec ambiances et personnalités distinctes
// Partition simple en 5 zones basée sur la position X/Z du joueur.
// Aucune dépendance Three.js : le fog est passé en paramètre (optionnel).

const _D = {
  centre: {
    id: 'centre', name: 'Centre-Ville',
    desc: 'Coeur commercial, toujours en mouvement',
    fogColor: 0x87ceeb,
    personalityBias: ['TOURISTE', 'PRESSÉ'],
  },
  nord: {
    id: 'nord', name: 'Quartier Nord',
    desc: 'Zone industrielle — méfiez-vous',
    fogColor: 0x6a8090,
    personalityBias: ['COSTAUD', 'NERVEUX'],
  },
  sud: {
    id: 'sud', name: 'Bord de Mer',
    desc: 'Air de vacances, touristes partout',
    fogColor: 0xa0d8ff,
    personalityBias: ['TOURISTE', 'JOGGEUR'],
  },
  ouest: {
    id: 'ouest', name: 'Quartier Ouest',
    desc: 'Zone résidentielle, calme relatif',
    fogColor: 0x88b8a0,
    personalityBias: ['JOGGEUR', 'TOURISTE'],
  },
  est: {
    id: 'est', name: 'Quartier Est',
    desc: 'Néons et vie nocturne',
    fogColor: 0x9080b8,
    personalityBias: ['NERVEUX', 'COSTAUD'],
  },
};

export class DistrictSystem {
  constructor() {
    this._current = _D.centre;
    this._prevId  = null;
  }

  // Retourne le quartier pour une position donnée (pure function).
  // Frontières calquées sur les routes de la grille (roadXs/Zs à ±57).
  getDistrict(x, z) {
    if (z < -57) return _D.nord;
    if (z >  57) return _D.sud;
    if (x < -57) return _D.ouest;
    if (x >  57) return _D.est;
    return _D.centre;
  }

  getCurrent() { return this._current; }

  // Détecte un changement de quartier. Retourne le nouveau quartier ou null.
  // fog : THREE.Fog optionnel — met à jour sa couleur si fourni.
  update(x, z, fog) {
    const d = this.getDistrict(x, z);
    this._current = d;
    if (d.id === this._prevId) return null;
    this._prevId = d.id;
    if (fog) fog.color.setHex(d.fogColor);
    return d;
  }
}
