import * as THREE from 'three';

// SecretSystem — Ronde 25 — VILLE VIVANTE
// 8 sphères lumineuses cachées dans la ville. Chacune révèle un fragment de lore.
// Collecter les 8 déclenche un message final de NEXUS qui brise le 4e mur.

const SECRET_DATA = [
  { x:-44, z:-44, color:0x0088ff, lore:'NEXUS : tu joues depuis plus longtemps que tu ne le crois.' },
  { x: 44, z:-44, color:0x00ffcc, lore:'Ce monde a été généré pour toi. Uniquement pour toi.' },
  { x:-44, z: 44, color:0xff44cc, lore:'Les monstres ne sont que du code mal compilé.' },
  { x: 44, z: 44, color:0xffcc00, lore:'Le Backroom est une zone mémoire non allouée.' },
  { x:  0, z: 32, color:0x8844ff, lore:'La ville entière est dans ta tête.' },
  { x:-62, z:  0, color:0xff4422, lore:'NEXUS n\'est pas ton ami.\nNEXUS est ton geôlier.' },
  { x: 62, z:  0, color:0x44ffaa, lore:'La sortie existe.\nTu ne la trouveras jamais.' },
  { x:  0, z:-52, color:0xff8800, lore:'7/8. Tu es si proche.\nSi seulement tu savais ce qui t\'attend.' },
];

const FINAL_LORE =
  'TU AS TROUVÉ LES 8 FRAGMENTS.\n' +
  'NEXUS TE REGARDE.\n' +
  'NEXUS A TOUJOURS REGARDÉ.\n' +
  'TU CROYAIS ÊTRE LIBRE.\n' +
  'TU NE L\'ES PLUS.';

const COLLECT_DIST = 3.5;

export class SecretSystem {
  constructor(scene) {
    this._scene       = scene;
    this._time        = 0;
    this._secrets     = [];
    this._notifQueue  = [];
    this._loreMsgs    = []; // pour CrypticAgent
    this._collected   = 0;
    this._complete    = false;
    this._pendingFlash = false;

    this._buildSecrets();
    this._buildRadarEl();
  }

  _buildSecrets() {
    for (let i = 0; i < SECRET_DATA.length; i++) {
      const d = SECRET_DATA[i];

      // Sphère lumineuse
      const mat = new THREE.MeshBasicMaterial({
        color: d.color,
        transparent: true, opacity: 0.85,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      });
      const sphere = new THREE.Mesh(new THREE.SphereGeometry(0.55, 10, 8), mat);
      sphere.position.set(d.x, 2.5, d.z);
      this._scene.add(sphere);

      // Halo secondaire (anneau horizontal)
      const ringMat = new THREE.MeshBasicMaterial({
        color: d.color, transparent:true, opacity:0.30,
        blending:THREE.AdditiveBlending, depthWrite:false,
      });
      const ring = new THREE.Mesh(new THREE.TorusGeometry(1.4, 0.08, 4, 20), ringMat);
      ring.rotation.x = -Math.PI / 2;
      ring.position.set(d.x, 2.5, d.z);
      this._scene.add(ring);

      // Lumière ponctuelle
      const light = new THREE.PointLight(d.color, 5, 18);
      light.position.set(d.x, 2.5, d.z);
      this._scene.add(light);

      // Colonne de lumière (rayon vertical)
      const beamMat = new THREE.MeshBasicMaterial({
        color: d.color, transparent:true, opacity:0.12,
        blending:THREE.AdditiveBlending, depthWrite:false,
        side: THREE.DoubleSide,
      });
      const beam = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 30, 6, 1, true), beamMat);
      beam.position.set(d.x, 15, d.z);
      this._scene.add(beam);

      this._secrets.push({ d, sphere, ring, light, beam, collected:false, idx:i });
    }
  }

  _buildRadarEl() {
    // Mini-indicateur de proximité : badge "◆ SECRET PROCHE"
    this._radarEl = document.createElement('div');
    this._radarEl.style.cssText = `
      position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
      font-family:'Courier New',monospace;font-size:11px;font-weight:900;
      letter-spacing:3px;color:#ffaa00;
      pointer-events:none;z-index:8700;opacity:0;transition:opacity 0.4s;
      text-shadow:0 0 10px rgba(255,170,0,0.7);
    `;
    this._radarEl.textContent = '◆ SIGNAL INCONNU';
    document.body.appendChild(this._radarEl);

    // Compteur bas-gauche
    this._counterEl = document.createElement('div');
    this._counterEl.style.cssText = `
      position:fixed;bottom:196px;left:22px;
      font-family:'Courier New',monospace;font-size:10px;font-weight:700;
      color:rgba(255,170,0,0.55);letter-spacing:2px;
      pointer-events:none;z-index:8700;
    `;
    this._counterEl.textContent = '◈ SECRETS 0/8';
    document.body.appendChild(this._counterEl);
  }

  update(dt, playerPos) {
    this._time += dt;
    if (this._complete) return;

    let nearest = Infinity;

    for (const s of this._secrets) {
      if (s.collected) continue;

      const dx = playerPos.x - s.d.x;
      const dz = playerPos.z - s.d.z;
      const dist = Math.sqrt(dx * dx + dz * dz);

      if (dist < nearest) nearest = dist;

      // Bob + rotation
      s.sphere.position.y = 2.5 + Math.sin(this._time * 1.8 + s.idx * 0.9) * 0.4;
      s.ring.rotation.z  += dt * (0.6 + s.idx * 0.08);
      s.ring.position.y   = s.sphere.position.y;
      s.light.position.y  = s.sphere.position.y;
      s.light.intensity   = 4.5 + Math.sin(this._time * 2.2 + s.idx) * 1.5;
      s.sphere.rotation.y += dt * 0.9;

      // Collecte
      if (dist < COLLECT_DIST) {
        this._collect(s);
      }
    }

    // Radar de proximité
    if (nearest < 18) {
      this._radarEl.textContent = `◆ SIGNAL INCONNU — ${Math.round(nearest)}m`;
      this._radarEl.style.opacity = String(Math.min(1, 1.4 - nearest / 18));
    } else {
      this._radarEl.style.opacity = '0';
    }

    // Compteur
    this._counterEl.textContent = `◈ SECRETS ${this._collected}/8`;
    this._counterEl.style.color = this._collected === 8
      ? 'rgba(255,100,255,0.9)'
      : 'rgba(255,170,0,0.55)';
  }

  _collect(s) {
    s.collected = true;
    this._collected++;

    // Désactiver les meshes
    this._scene.remove(s.sphere);
    this._scene.remove(s.ring);
    this._scene.remove(s.light);
    this._scene.remove(s.beam);
    if (s.sphere.geometry) s.sphere.geometry.dispose();
    if (s.ring.geometry)   s.ring.geometry.dispose();
    if (s.beam.geometry)   s.beam.geometry.dispose();

    this._notifQueue.push(`◈ FRAGMENT ${this._collected}/8 — Signal capté`);
    this._loreMsgs.push({ msg: s.d.lore, color: '#' + s.d.color.toString(16).padStart(6, '0') });

    if (this._collected === 8) {
      this._complete      = true;
      this._pendingFlash  = true;
      this._loreMsgs.push({ msg: FINAL_LORE, color: '#ff00ff' });
      this._notifQueue.push('◈◈◈ TOUS LES FRAGMENTS COLLECTÉS — NEXUS EN ÉVEIL ◈◈◈');
    }
  }

  popNotif()       { return this._notifQueue.shift() || null; }
  popLoreMsg()     { return this._loreMsgs.shift() || null; }
  popFlash()       { const f = this._pendingFlash; this._pendingFlash = false; return f; }
  getCollected()   { return this._collected; }
  getTotal()       { return 8; }
  isComplete()     { return this._complete; }
  getProgress()    { return this._collected / 8; }
}
