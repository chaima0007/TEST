import * as THREE from 'three';

// BackroomAgent — Ronde 23 — ONIRIQUE / HORREUR
// Tu tournes à droite la nuit — et la ville disparaît.
// Inspiré des Backrooms, SCP Foundation, Twin Peaks, Silent Hill.
// Couloirs jaunes infinis, lumières vacillantes, L'Entité qui approche.

const WALL_MAT  = () => new THREE.MeshStandardMaterial({ color: 0xd0be6a, roughness: 0.92, emissive: 0x0a0900, emissiveIntensity: 0.08 });
const FLOOR_MAT = () => new THREE.MeshStandardMaterial({ color: 0x7a8a35, roughness: 0.98 });
const CEIL_MAT  = () => new THREE.MeshStandardMaterial({ color: 0xbcad52, roughness: 0.90 });
const LIGHT_MAT = () => new THREE.MeshStandardMaterial({ color: 0xfff8d8, emissive: 0xfff8d8, emissiveIntensity: 2.8 });

const ENTITY_SPEED   = 3.4;  // m/s
const ROOM_HEIGHT    = 3.6;
const TIMER_MAX      = 58;   // seconds before forced exit
const ESCAPE_SPEED   = 55;   // km/h min to escape
const ESCAPE_HOLD    = 5.5;  // seconds at escape speed needed
const TRIGGER_CHANCE = 0.00055; // per frame at 60fps ≈ once per ~30s of eligible driving
const CATCH_DIST     = 5.5;

function buildEntity(scene) {
  const mat  = new THREE.MeshStandardMaterial({ color: 0x000000, roughness: 1, emissive: 0x0a0004 });
  const eyeM = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const g = new THREE.Group();

  const add = (geo, m, x, y, z, rx = 0, ry = 0, rz = 0) => {
    const mesh = new THREE.Mesh(geo, m);
    mesh.position.set(x, y, z);
    mesh.rotation.set(rx, ry, rz);
    g.add(mesh);
    return mesh;
  };

  add(new THREE.BoxGeometry(1.1, 2.5, 0.55), mat,    0, 1.8,  0);            // torso
  add(new THREE.SphereGeometry(0.58, 8, 6), mat,     0, 3.55, 0);            // tête
  add(new THREE.CylinderGeometry(0.16, 0.11, 3.8, 6), mat, -1.4, 2.8, 0, 0, 0,  0.22);  // bras G
  add(new THREE.CylinderGeometry(0.16, 0.11, 3.8, 6), mat,  1.4, 2.8, 0, 0, 0, -0.22);  // bras D
  add(new THREE.CylinderGeometry(0.22, 0.16, 2.8, 6), mat, -0.37, -0.05, 0);             // jambe G
  add(new THREE.CylinderGeometry(0.22, 0.16, 2.8, 6), mat,  0.37, -0.05, 0);             // jambe D
  add(new THREE.SphereGeometry(0.07, 4, 3), eyeM,  -0.18, 3.62, 0.56);      // oeil G
  add(new THREE.SphereGeometry(0.07, 4, 3), eyeM,   0.18, 3.62, 0.56);      // oeil D

  const aura = new THREE.PointLight(0x2a0012, 2.2, 20);
  aura.position.y = 2.5;
  g.add(aura);

  g.visible = false;
  scene.add(g);
  return g;
}

function buildGeometry(scene, cx, cz) {
  const meshes = [];
  const H = ROOM_HEIGHT;
  const R = 90; // half-extent

  const add = (geo, mat, x, y, z, rx = 0, ry = 0, rz = 0) => {
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x, y, z);
    m.rotation.set(rx, ry, rz);
    scene.add(m);
    meshes.push(m);
    return m;
  };

  // Sol + plafond (gigantesques pour cacher les bords)
  add(new THREE.PlaneGeometry(R * 2, R * 2), FLOOR_MAT(), cx, 0.01, cz, -Math.PI / 2);
  add(new THREE.PlaneGeometry(R * 2, R * 2), CEIL_MAT(), cx, H, cz, Math.PI / 2);

  // Murs extérieurs
  add(new THREE.BoxGeometry(R * 2, H, 0.14), WALL_MAT(), cx, H / 2, cz - R);
  add(new THREE.BoxGeometry(R * 2, H, 0.14), WALL_MAT(), cx, H / 2, cz + R);
  add(new THREE.BoxGeometry(0.14, H, R * 2), WALL_MAT(), cx - R, H / 2, cz);
  add(new THREE.BoxGeometry(0.14, H, R * 2), WALL_MAT(), cx + R, H / 2, cz);

  // Cloisons internes (couloirs répétitifs)
  for (let i = -4; i <= 4; i++) {
    if (i === 0) continue;
    const zw = cz + i * 11;
    const xw = cx + i * 11;
    // Paroi horizontale avec une ouverture au centre (gap de 6 unités)
    add(new THREE.BoxGeometry(R * 2 - 8, H, 0.10), WALL_MAT(), cx, H / 2, zw);
    add(new THREE.BoxGeometry(0.10, H, R * 2 - 8), WALL_MAT(), xw, H / 2, cz);
  }

  // Néons fluorescents au plafond (vacillants via emissiveIntensity animée)
  const lightMeshes = [];
  for (let zi = -3; zi <= 3; zi++) {
    for (let xi = -3; xi <= 3; xi++) {
      const m = add(
        new THREE.BoxGeometry(0.18, 0.06, 2.8), LIGHT_MAT(),
        cx + xi * 11, H - 0.03, cz + zi * 11
      );
      lightMeshes.push(m);
    }
  }

  return { meshes, lightMeshes };
}

export class BackroomAgent {
  constructor(scene) {
    this._scene      = scene;
    this._active     = false;
    this._cooldown   = 45; // pas de backroom dans les 45 premières secondes
    this._timer      = 0;
    this._escapeHold = 0;
    this._entity     = buildEntity(scene);
    this._geometry   = null;
    this._exitPos    = { x: 0, z: 0 };
    this._notifQueue = [];
    this._fearLevel  = 0;
    this._flickerT   = 0;
    this._caughtTimer = 0;
    this._entityDist  = 999;
    this._buildOverlay();
    this._buildFogStore();
  }

  _buildOverlay() {
    this._overlay = document.createElement('div');
    this._overlay.style.cssText = `
      position:fixed;inset:0;pointer-events:none;z-index:8800;
      border:0px solid rgba(255,50,10,0);
      box-shadow:inset 0 0 0px rgba(255,0,0,0);
      background:rgba(200,180,80,0);
      transition:all .3s;
    `;
    document.body.appendChild(this._overlay);

    this._label = document.createElement('div');
    this._label.style.cssText = `
      position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
      font-family:'Courier New',monospace;font-size:14px;font-weight:900;
      color:#cc8800;letter-spacing:3px;text-align:center;
      pointer-events:none;z-index:8801;opacity:0;transition:opacity .5s;
      text-shadow:0 0 12px rgba(255,180,0,0.6);
    `;
    document.body.appendChild(this._label);
  }

  _buildFogStore() {
    // Brouillard spécifique au backroom (jaune dense)
    this._backroomFog = new THREE.FogExp2(0xc8b06a, 0.030);
  }

  _enter(playerPos, vehicle) {
    this._active     = true;
    this._timer      = 0;
    this._escapeHold = 0;
    this._fearLevel  = 0;
    this._exitPos    = { x: playerPos.x, z: playerPos.z };

    // Génère la géométrie autour du joueur
    this._geometry = buildGeometry(this._scene, playerPos.x, playerPos.z);

    // Place l'entité loin du joueur
    const angle = Math.random() * Math.PI * 2;
    this._entity.position.set(playerPos.x + Math.cos(angle) * 55, 0, playerPos.z + Math.sin(angle) * 55);
    this._entity.visible = true;

    // UI overlay
    this._overlay.style.border     = '10px solid rgba(255,80,10,0.45)';
    this._overlay.style.boxShadow  = 'inset 0 0 80px rgba(255,30,0,0.22)';
    this._overlay.style.background = 'rgba(200,180,60,0.06)';
    this._label.style.opacity      = '1';

    this._notifQueue.push('⚠ BACKROOM — Vous avez quitté la ville. Fuyez !');
  }

  _exit(reason) {
    this._active     = false;
    this._cooldown   = reason === 'caught' ? 25 : 90;
    this._timer      = 0;
    this._entity.visible = false;
    this._fearLevel  = 0;

    if (this._geometry) {
      for (const m of this._geometry.meshes) {
        this._scene.remove(m);
        m.geometry.dispose();
      }
      this._geometry = null;
    }

    // Restore overlay
    this._overlay.style.border     = '0px solid rgba(255,50,10,0)';
    this._overlay.style.boxShadow  = 'inset 0 0 0px rgba(255,0,0,0)';
    this._overlay.style.background = 'rgba(200,180,80,0)';
    this._label.style.opacity      = '0';

    if (reason === 'escape') this._notifQueue.push('✓ ÉCHAPPÉ — Bienvenue de retour dans la réalité.');
    if (reason === 'caught') this._notifQueue.push('L\'ENTITÉ VOUS A TOUCHÉ. Fuyez.');
  }

  update(dt, playerPos, vehicle, isNight, wantedLevel) {
    this._flickerT += dt;

    // Cooldown before re-entry / first trigger
    if (this._cooldown > 0) { this._cooldown -= dt; }

    if (!this._active) {
      // Trigger check
      if (isNight && wantedLevel === 0 && this._cooldown <= 0 && Math.random() < TRIGGER_CHANCE) {
        this._enter(playerPos, vehicle);
      }
      return;
    }

    this._timer += dt;

    // Flicker les néons
    if (this._geometry) {
      for (const m of this._geometry.lightMeshes) {
        const flicker = 0.6 + Math.abs(Math.sin(this._flickerT * (3 + Math.random() * 4))) * 2.2;
        m.material.emissiveIntensity = flicker;
      }
    }

    // Mouvement de l'entité
    const ex = this._entity.position.x, ez = this._entity.position.z;
    const dx = playerPos.x - ex, dz = playerPos.z - ez;
    this._entityDist = Math.sqrt(dx * dx + dz * dz);
    if (this._entityDist > 0.5) {
      const speed = ENTITY_SPEED * (1 + Math.max(0, (20 - this._entityDist) / 20) * 1.5);
      this._entity.position.x += (dx / this._entityDist) * speed * dt;
      this._entity.position.z += (dz / this._entityDist) * speed * dt;
      this._entity.rotation.y = Math.atan2(dx, dz);
    }

    // Peur (distance → fear)
    const targetFear = Math.pow(Math.max(0, 1 - this._entityDist / 40), 1.8);
    this._fearLevel += (targetFear - this._fearLevel) * dt * 2;

    // Capture
    if (this._entityDist < CATCH_DIST) {
      this._caughtTimer += dt;
      if (this._caughtTimer > 0.8) {
        vehicle.mesh.position.set(this._exitPos.x, 0, this._exitPos.z);
        this._exit('caught');
        this._caughtTimer = 0;
        return;
      }
    } else {
      this._caughtTimer = 0;
    }

    // Escape: vitesse élevée maintenue
    const spd = Math.abs(vehicle.getSpeedKmh ? vehicle.getSpeedKmh() : 0);
    if (spd >= ESCAPE_SPEED) {
      this._escapeHold += dt;
      if (this._escapeHold >= ESCAPE_HOLD) this._exit('escape');
    } else {
      this._escapeHold = Math.max(0, this._escapeHold - dt * 0.5);
    }

    // Timeout forcé
    if (this._timer >= TIMER_MAX) {
      vehicle.mesh.position.set(this._exitPos.x, 0, this._exitPos.z);
      this._exit('timeout');
      this._notifQueue.push('Vous avez survécu. Cette fois.');
    }

    // Label UI
    const remaining = Math.max(0, TIMER_MAX - this._timer);
    const escPct    = Math.round((this._escapeHold / ESCAPE_HOLD) * 100);
    this._label.innerHTML = `
      ⚠ BACKROOM<br>
      <span style="font-size:11px;color:#aaaa00;">Fuyez à ${ESCAPE_SPEED}+ km/h — ${escPct}% fuite</span><br>
      <span style="font-size:11px;color:#884400;">${Math.round(remaining)}s restant · Dist. entité : ${Math.round(this._entityDist)}m</span>
    `;
  }

  // Appelé après atmosphere.update() pour écraser le fog/bg
  applySceneOverride(scene) {
    if (!this._active) return;
    scene.fog   = this._backroomFog;
    scene.background.setHex(0xc8b06a);
  }

  popNotif()      { return this._notifQueue.shift() || null; }
  isActive()      { return this._active; }
  getFearLevel()  { return this._fearLevel; }
  getEntityDist() { return this._entityDist; }
  getTimer()      { return this._timer; }
  getEscapePct()  { return Math.min(1, this._escapeHold / ESCAPE_HOLD); }
}
