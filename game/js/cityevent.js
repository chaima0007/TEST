import * as THREE from 'three';

// CityEventAgent — Ronde 25 — VILLE VIVANTE
// Événements aléatoires qui surgissent dans la ville.
// Explosion de véhicule · Coupure électrique · Pluie de météorites · Fissure dimensionnelle

const EVENTS = [
  { id:'explosion', label:'💥 EXPLOSION',       cooldown:80,  prob:0.00035 },
  { id:'blackout',  label:'⚡ COUPURE ÉLEC.',   cooldown:110, prob:0.00020 },
  { id:'meteor',    label:'☄️ MÉTÉORITES',       cooldown:160, prob:0.00012, nightOnly:true },
  { id:'rift',      label:'🕳 FISSURE',          cooldown:190, prob:0.00010 },
];

const SUBTITLES = {
  explosion: 'Un véhicule vient d\'exploser à proximité',
  blackout:  'La ville plonge dans les ténèbres',
  meteor:    'Des corps célestes traversent le ciel',
  rift:      'Le tissu de la réalité se déchire',
};

export class CityEventAgent {
  constructor(scene) {
    this._scene      = scene;
    this._cooldowns  = {};
    this._active     = null;
    this._notifQueue = [];
    this._time       = 0;

    for (const ev of EVENTS) this._cooldowns[ev.id] = 30 + Math.random() * 40;

    this._buildBlackoutOverlay();
  }

  _buildBlackoutOverlay() {
    this._blackoutEl = document.createElement('div');
    this._blackoutEl.style.cssText = `
      position:fixed;inset:0;pointer-events:none;z-index:8990;
      background:rgba(0,0,0,0);transition:background 1.8s ease;
    `;
    document.body.appendChild(this._blackoutEl);
  }

  _pos(playerPos) {
    const a = Math.random() * Math.PI * 2;
    const d = 22 + Math.random() * 28;
    return { x: playerPos.x + Math.cos(a) * d, z: playerPos.z + Math.sin(a) * d };
  }

  // ── Explosion ────────────────────────────────────────────────────────────────

  _startExplosion(px, pz) {
    const a = this._active;
    a.duration = 9; a.timer = a.duration;

    // Boule de feu
    const fbMat = new THREE.MeshBasicMaterial({ color:0xff5500, transparent:true, opacity:0.9, blending:THREE.AdditiveBlending, depthWrite:false });
    const fb = new THREE.Mesh(new THREE.SphereGeometry(3.2, 8, 6), fbMat);
    fb.position.set(px, 3, pz);
    this._scene.add(fb); a.meshes.push(fb); a.fb = fb;

    // Anneau au sol
    const rMat = new THREE.MeshBasicMaterial({ color:0xff8800, transparent:true, opacity:0.7, blending:THREE.AdditiveBlending, depthWrite:false });
    const ring = new THREE.Mesh(new THREE.TorusGeometry(2, 0.6, 6, 24), rMat);
    ring.rotation.x = -Math.PI / 2;
    ring.position.set(px, 0.15, pz);
    this._scene.add(ring); a.meshes.push(ring); a.ring = ring;

    // Lumière
    const l = new THREE.PointLight(0xff4400, 35, 70);
    l.position.set(px, 5, pz);
    this._scene.add(l); a.lights.push(l); a.explLight = l;

    // Fumée (particules grises)
    const sPos = new Float32Array(120 * 3);
    for (let i = 0; i < 120; i++) {
      sPos[i*3]   = px + (Math.random() - 0.5) * 6;
      sPos[i*3+1] = Math.random() * 8;
      sPos[i*3+2] = pz + (Math.random() - 0.5) * 6;
    }
    const sGeo = new THREE.BufferGeometry();
    sGeo.setAttribute('position', new THREE.BufferAttribute(sPos, 3));
    const sMat = new THREE.PointsMaterial({ color:0x444444, size:1.2, transparent:true, opacity:0.55, depthWrite:false });
    const smoke = new THREE.Points(sGeo, sMat);
    this._scene.add(smoke); a.meshes.push(smoke);
    a.smokeAttr = sGeo.attributes.position; a.smokePos = sPos;
  }

  _tickExplosion(dt) {
    const a = this._active;
    const t = 1 - a.timer / a.duration; // 0→1

    if (a.fb) {
      // La boule de feu rétrécit et monte
      const s = Math.max(0, 1.5 - t * 1.8);
      a.fb.scale.setScalar(s);
      a.fb.position.y = 3 + t * 6;
      a.fb.material.opacity = Math.max(0, 0.9 - t * 1.1);
    }
    if (a.ring) {
      // L'anneau s'élargit
      const rs = 1 + t * 5;
      a.ring.scale.setScalar(rs);
      a.ring.material.opacity = Math.max(0, 0.7 - t * 0.8);
    }
    if (a.explLight) {
      a.explLight.intensity = Math.max(0, 35 * (1 - t * 1.1));
    }
    // Fumée monte
    if (a.smokePos && a.smokeAttr) {
      for (let i = 0; i < 120; i++) a.smokePos[i*3+1] += dt * (1.5 + Math.random() * 0.5);
      a.smokeAttr.needsUpdate = true;
    }
  }

  // ── Blackout ──────────────────────────────────────────────────────────────────

  _startBlackout(streetLamps) {
    const a = this._active;
    a.duration = 14; a.timer = a.duration;
    a.streetLamps = streetLamps;
    // Overlay sombre
    this._blackoutEl.style.background = 'rgba(0,0,0,0.72)';
  }

  _tickBlackout(dt) {
    // Les lampadaires restent éteints via update principal (voir isBlackout())
  }

  _endBlackout() {
    this._blackoutEl.style.background = 'rgba(0,0,0,0)';
  }

  // ── Météorites ────────────────────────────────────────────────────────────────

  _startMeteor(playerPos) {
    const a = this._active;
    a.duration = 14; a.timer = a.duration;
    a.meteors  = [];
    const N = 5 + Math.floor(Math.random() * 4);
    for (let i = 0; i < N; i++) {
      const mx = playerPos.x + (Math.random() - 0.5) * 100;
      const mz = playerPos.z + (Math.random() - 0.5) * 100;
      const mat = new THREE.MeshBasicMaterial({ color:0xff6622, blending:THREE.AdditiveBlending, depthWrite:false });
      const m   = new THREE.Mesh(new THREE.SphereGeometry(0.5 + Math.random() * 0.8, 6, 4), mat);
      m.position.set(mx, 80 + Math.random() * 40, mz);
      this._scene.add(m); a.meshes.push(m);

      // Traîne
      const trailMat = new THREE.MeshBasicMaterial({ color:0xff4400, transparent:true, opacity:0.55, blending:THREE.AdditiveBlending, depthWrite:false });
      const trail = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.5, 6, 4), trailMat);
      trail.position.set(mx, 80 + Math.random() * 40 + 3, mz);
      this._scene.add(trail); a.meshes.push(trail);

      const vy = -(35 + Math.random() * 20);
      a.meteors.push({ mesh:m, trail, vy, grounded:false });
    }
  }

  _tickMeteor(dt) {
    const a = this._active;
    for (const mt of a.meteors) {
      if (mt.grounded) continue;
      mt.mesh.position.y  += mt.vy * dt;
      mt.trail.position.y  = mt.mesh.position.y + 3;
      if (mt.mesh.position.y <= 0.5) {
        mt.grounded = true;
        // Impact flash
        const l = new THREE.PointLight(0xff6600, 20, 30);
        l.position.copy(mt.mesh.position);
        this._scene.add(l); a.lights.push(l);
        mt.impactLight = l;
        this._notifQueue.push('☄️ Impact détecté à ' + Math.round(Math.hypot(
          mt.mesh.position.x, mt.mesh.position.z)) + 'm');
      }
      if (mt.impactLight) mt.impactLight.intensity *= 0.88;
    }
  }

  // ── Fissure dimensionnelle ────────────────────────────────────────────────────

  _startRift(px, pz) {
    const a = this._active;
    a.duration = 22; a.timer = a.duration;

    // Tranchée noire au sol
    const mat = new THREE.MeshBasicMaterial({ color:0x000000 });
    const rift = new THREE.Mesh(new THREE.BoxGeometry(3, 0.4, 12), mat);
    rift.position.set(px, 0.1, pz);
    rift.rotation.y = Math.random() * Math.PI;
    this._scene.add(rift); a.meshes.push(rift); a.riftMesh = rift;

    // Lueur violette dans la fissure
    const l = new THREE.PointLight(0x8800ff, 12, 28);
    l.position.set(px, 0.5, pz);
    this._scene.add(l); a.lights.push(l); a.riftLight = l;

    // Particules qui s'échappent
    const pPos = new Float32Array(80 * 3);
    for (let i = 0; i < 80; i++) {
      pPos[i*3]   = px + (Math.random() - 0.5) * 3;
      pPos[i*3+1] = 0.5 + Math.random() * 0.5;
      pPos[i*3+2] = pz + (Math.random() - 0.5) * 12;
    }
    const pGeo = new THREE.BufferGeometry();
    pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
    const pMat = new THREE.PointsMaterial({ color:0x9900ff, size:0.2, transparent:true, opacity:0.75, blending:THREE.AdditiveBlending, depthWrite:false });
    const pts = new THREE.Points(pGeo, pMat);
    this._scene.add(pts); a.meshes.push(pts);
    a.riftPts = pGeo.attributes.position; a.riftPos = pPos;
  }

  _tickRift(dt) {
    const a = this._active;
    this._time += dt;
    if (a.riftLight) {
      a.riftLight.intensity = 12 + Math.sin(this._time * 4.5) * 5;
    }
    if (a.riftPos && a.riftPts) {
      for (let i = 0; i < 80; i++) {
        a.riftPos[i*3+1] += dt * (0.6 + Math.random() * 0.4);
        if (a.riftPos[i*3+1] > 5) {
          a.riftPos[i*3+1] = 0.5;
        }
      }
      a.riftPts.needsUpdate = true;
    }
  }

  // ── Cycle de vie ──────────────────────────────────────────────────────────────

  update(dt, playerPos, isNight, streetLamps) {
    for (const ev of EVENTS) {
      this._cooldowns[ev.id] = Math.max(0, (this._cooldowns[ev.id] || 0) - dt);
    }

    if (!this._active) {
      for (const ev of EVENTS) {
        if (this._cooldowns[ev.id] > 0) continue;
        if (ev.nightOnly && !isNight) continue;
        if (Math.random() < ev.prob) {
          const { x, z } = this._pos(playerPos);
          this._active = { id:ev.id, timer:0, duration:0, meshes:[], lights:[] };
          this._cooldowns[ev.id] = ev.cooldown;
          this._notifQueue.push(`${ev.label} — ${SUBTITLES[ev.id]}`);
          if (ev.id === 'explosion') this._startExplosion(x, z);
          if (ev.id === 'blackout')  this._startBlackout(streetLamps);
          if (ev.id === 'meteor')    this._startMeteor(playerPos);
          if (ev.id === 'rift')      this._startRift(x, z);
          break;
        }
      }
    }

    if (!this._active) return;

    this._active.timer -= dt;
    if (this._active.id === 'explosion') this._tickExplosion(dt);
    if (this._active.id === 'blackout')  this._tickBlackout(dt);
    if (this._active.id === 'meteor')    this._tickMeteor(dt);
    if (this._active.id === 'rift')      this._tickRift(dt);

    if (this._active.timer <= 0) {
      if (this._active.id === 'blackout') this._endBlackout();
      // Nettoyage géométrie
      for (const m of this._active.meshes) {
        this._scene.remove(m);
        if (m.geometry) m.geometry.dispose();
      }
      for (const l of this._active.lights) this._scene.remove(l);
      this._active = null;
    }
  }

  popNotif()       { return this._notifQueue.shift() || null; }
  isActive()       { return this._active !== null; }
  getActiveEvent() { return this._active?.id || '—'; }
  isBlackout()     { return this._active?.id === 'blackout'; }
  getCooldown(id)  { return this._cooldowns[id] ?? 0; }
}
