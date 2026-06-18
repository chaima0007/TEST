import * as THREE from 'three';

// MonsterAgent — Ronde 23 — ONIRIQUE / HORREUR
// Trois créatures surgissent la nuit dans la ville.
// L'Ombre : silhouette impossible qui suit.
// La Bête : quadrupède monstrueux qui charge.
// Le Cyclope : œil géant flottant qui observe.

const SPAWN_DIST   = 85;
const COOLDOWN_DEF = 140; // secondes entre apparitions
const SCARE_DIST   = 9;   // distance de capture
const FLEE_DIST    = 120; // distance max avant despawn

function buildShadow() {
  const mat  = new THREE.MeshStandardMaterial({ color: 0x000000, roughness: 1, emissive: 0x0c0005 });
  const eyeM = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const g = new THREE.Group();
  const add = (geo, m, x, y, z, rx=0, ry=0, rz=0) => {
    const mesh = new THREE.Mesh(geo, m);
    mesh.position.set(x, y, z);
    mesh.rotation.set(rx, ry, rz);
    g.add(mesh);
  };

  add(new THREE.BoxGeometry(1.0, 2.8, 0.5), mat,   0, 2.0,  0);            // torse
  add(new THREE.SphereGeometry(0.52, 8, 6), mat,   0, 3.85, 0);            // tête (trop petite)
  add(new THREE.CylinderGeometry(0.14, 0.08, 5.2, 6), mat, -1.55, 3.1, 0, 0, 0,  0.28); // bras G (trop long)
  add(new THREE.CylinderGeometry(0.14, 0.08, 5.2, 6), mat,  1.55, 3.1, 0, 0, 0, -0.28); // bras D
  add(new THREE.CylinderGeometry(0.2, 0.14, 3.2, 6), mat, -0.35,  0, 0);  // jambe G
  add(new THREE.CylinderGeometry(0.2, 0.14, 3.2, 6), mat,  0.35,  0, 0);  // jambe D
  add(new THREE.SphereGeometry(0.06, 4, 3), eyeM, -0.16, 3.90, 0.50);     // oeil G
  add(new THREE.SphereGeometry(0.06, 4, 3), eyeM,  0.16, 3.90, 0.50);     // oeil D
  const aura = new THREE.PointLight(0x1a0022, 2.5, 22);
  aura.position.y = 2.5;
  g.add(aura);

  return { group: g, type: 'OMBRE', speed: 3.2, height: 0, floats: false };
}

function buildBeast() {
  const mat  = new THREE.MeshStandardMaterial({ color: 0x060606, roughness: 0.95, emissive: 0x060000 });
  const eyeM = new THREE.MeshBasicMaterial({ color: 0xff2200 });
  const g = new THREE.Group();
  const add = (geo, m, x, y, z, rx=0, ry=0, rz=0) => {
    const mesh = new THREE.Mesh(geo, m);
    mesh.position.set(x, y, z);
    mesh.rotation.set(rx, ry, rz);
    g.add(mesh);
  };

  // Corps allongé
  add(new THREE.BoxGeometry(5.5, 3.0, 10.5), mat, 0, 5.0, 0);
  // Cou
  add(new THREE.CylinderGeometry(1.1, 1.5, 3.2, 8), mat, 0, 7.0, 4.0, -0.3);
  // Tête
  add(new THREE.BoxGeometry(2.8, 2.4, 4.0), mat, 0, 8.5, 5.8);
  // Mâchoire inférieure
  add(new THREE.BoxGeometry(2.2, 0.8, 3.2), mat, 0, 7.4, 6.2);
  // 4 pattes
  for (const [x, z] of [[-2.4, 3.5], [2.4, 3.5], [-2.4, -3.5], [2.4, -3.5]]) {
    add(new THREE.CylinderGeometry(0.58, 0.38, 6.0, 7), mat, x, 2.0, z);
    add(new THREE.BoxGeometry(1.4, 0.5, 2.0), mat, x, -1.0, z + 0.5); // patte
  }
  // Épines dorsales
  for (let i = 0; i < 5; i++) {
    add(new THREE.ConeGeometry(0.28, 2.2, 5), mat, 0, 7.0 + i * 0.1, 2.5 - i * 1.8);
  }
  // Yeux rouges
  for (const x of [-0.85, 0.85]) {
    add(new THREE.SphereGeometry(0.32, 8, 6), eyeM, x, 9.0, 7.5);
    const l = new THREE.PointLight(0xff2200, 5, 20);
    l.position.set(x, 9.0, 7.5);
    g.add(l);
  }
  // Aura sombre
  const aura = new THREE.PointLight(0x1a0000, 3, 30);
  aura.position.y = 5;
  g.add(aura);

  return { group: g, type: 'BÊTE', speed: 5.5, height: 0, floats: false };
}

function buildCyclope() {
  const scleraMat = new THREE.MeshStandardMaterial({ color: 0xf0e8d0, roughness: 0.35 });
  const irisMat   = new THREE.MeshBasicMaterial({ color: 0x1a006a, side: THREE.DoubleSide });
  const pupilMat  = new THREE.MeshBasicMaterial({ color: 0x000000, side: THREE.DoubleSide });
  const veinMat   = new THREE.MeshBasicMaterial({ color: 0xcc2200, side: THREE.DoubleSide });
  const stalkMat  = new THREE.MeshStandardMaterial({ color: 0x100c04, roughness: 0.92 });
  const g = new THREE.Group();
  const add = (geo, m, x, y, z, rx=0, ry=0, rz=0) => {
    const mesh = new THREE.Mesh(geo, m);
    mesh.position.set(x, y, z);
    mesh.rotation.set(rx, ry, rz);
    g.add(mesh);
  };

  // Globe oculaire
  add(new THREE.SphereGeometry(4.5, 18, 14), scleraMat, 0, 14, 0);
  // Iris
  add(new THREE.CircleGeometry(2.6, 24), irisMat, 0, 14, 4.48);
  // Pupille verticale (ellipse aplatie)
  const pupilGeo = new THREE.EllipseCurve ? (() => {
    const g2 = new THREE.CircleGeometry(1.1, 16); g2.scale(0.6, 1, 1); return g2;
  })() : new THREE.CircleGeometry(1.1, 16);
  add(pupilGeo, pupilMat, 0, 14, 4.50);
  // Veines (ring subtils)
  for (let i = 0; i < 4; i++) {
    const r = new THREE.Mesh(
      new THREE.TorusGeometry(2.5 + i * 0.5, 0.04, 4, 20),
      veinMat
    );
    r.position.set(0, 14, 0);
    r.rotation.set(Math.random(), Math.random(), Math.random());
    g.add(r);
  }
  // Tige (pedoncule)
  add(new THREE.CylinderGeometry(0.3, 1.0, 12, 8), stalkMat, 0, 6, 0);
  // Lumière bleue
  const l = new THREE.PointLight(0x1100ff, 7, 40);
  l.position.set(0, 14, 0);
  g.add(l);
  const aura = new THREE.PointLight(0x0a0040, 3, 60);
  aura.position.y = 14;
  g.add(aura);

  return { group: g, type: 'CYCLOPE', speed: 0, height: 0, floats: true };
}

const BUILDERS = [buildShadow, buildBeast, buildCyclope];

export class MonsterAgent {
  constructor(scene) {
    this._scene    = scene;
    this._active   = false;
    this._cooldown = 60; // premier spawn après 60s
    this._monster  = null;
    this._type     = '';
    this._fearLevel = 0;
    this._dist      = 999;
    this._time      = 0;
    this._spawnIdx  = 0;
    this._scaredCount = 0;
    this._notifQueue  = [];
    this._buildFearOverlay();
  }

  _buildFearOverlay() {
    this._fearEl = document.createElement('div');
    this._fearEl.style.cssText = `
      position:fixed;inset:0;pointer-events:none;z-index:8600;
      background:rgba(60,0,0,0);
      box-shadow:inset 0 0 0px rgba(200,0,0,0);
      transition:background .15s, box-shadow .15s;
    `;
    document.body.appendChild(this._fearEl);

    this._fearLabel = document.createElement('div');
    this._fearLabel.style.cssText = `
      position:fixed;bottom:220px;left:50%;transform:translateX(-50%);
      font-family:'Courier New',monospace;font-size:12px;font-weight:900;
      letter-spacing:3px;pointer-events:none;z-index:8601;
      opacity:0;transition:opacity .3s;color:#ff1100;text-align:center;
      text-shadow:0 0 14px rgba(255,0,0,0.7);
    `;
    document.body.appendChild(this._fearLabel);
  }

  _spawn(playerPos) {
    const builder  = BUILDERS[this._spawnIdx % BUILDERS.length];
    this._spawnIdx++;
    const data     = builder();
    this._monster  = data;
    this._active   = true;
    this._time     = 0;
    this._fearLevel = 0;

    const angle = Math.random() * Math.PI * 2;
    data.group.position.set(
      playerPos.x + Math.cos(angle) * SPAWN_DIST,
      data.height,
      playerPos.z + Math.sin(angle) * SPAWN_DIST
    );
    this._scene.add(data.group);

    const labels = {
      OMBRE:  '⚠ QUELQUE CHOSE APPROCHE DANS L\'OMBRE',
      BÊTE:   '⚠ LA TERRE TREMBLE — UNE BÊTE S\'ÉVEILLE',
      CYCLOPE:'⚠ UN ŒIL VOUS OBSERVE DEPUIS LE CIEL',
    };
    this._notifQueue.push(labels[data.type] || '⚠ VOUS N\'ÊTES PAS SEUL');
  }

  _despawn(reason) {
    if (this._monster) {
      this._scene.remove(this._monster.group);
      this._monster.group.traverse(child => {
        if (child.geometry) child.geometry.dispose();
      });
      this._monster = null;
    }
    this._active    = false;
    this._fearLevel = 0;
    this._cooldown  = reason === 'scared' ? 80 : COOLDOWN_DEF;
  }

  update(dt, playerPos, isNight, wantedLevel, vehicle) {
    this._time += dt;

    if (this._cooldown > 0) { this._cooldown -= dt; }

    if (!this._active) {
      if (isNight && wantedLevel === 0 && this._cooldown <= 0) {
        this._spawn(playerPos);
      }
      this._fearLevel = Math.max(0, this._fearLevel - dt * 1.5);
      this._updateFearUI();
      return;
    }

    const m   = this._monster;
    const mx  = m.group.position.x, mz = m.group.position.z;
    const dx  = playerPos.x - mx, dz = playerPos.z - mz;
    this._dist = Math.sqrt(dx * dx + dz * dz);

    // Mouvement vers le joueur (pas Le Cyclope)
    if (!m.floats && this._dist > 1) {
      const spd  = m.speed * (1 + Math.max(0, (30 - this._dist) / 30) * 0.8);
      m.group.position.x += (dx / this._dist) * spd * dt;
      m.group.position.z += (dz / this._dist) * spd * dt;
      m.group.rotation.y  = Math.atan2(dx, dz);
    }

    // Animation (balancement)
    if (m.type === 'OMBRE') {
      m.group.position.y = Math.sin(this._time * 1.8) * 0.15;
    }
    if (m.type === 'CYCLOPE') {
      m.group.position.y = Math.sin(this._time * 0.7) * 2;
      m.group.rotation.y += dt * 0.18;
      // Suit le joueur avec les yeux (rotation vers le joueur)
      m.group.position.x = playerPos.x + Math.sin(this._time * 0.2) * 40;
      m.group.position.z = playerPos.z + Math.cos(this._time * 0.2) * 40;
    }
    if (m.type === 'BÊTE') {
      m.group.position.y = Math.abs(Math.sin(this._time * m.speed * 0.4)) * 0.4;
    }

    // Niveau de peur
    const maxFearDist = m.type === 'CYCLOPE' ? 60 : 45;
    const targetFear  = Math.pow(Math.max(0, 1 - this._dist / maxFearDist), 2.0);
    this._fearLevel  += (targetFear - this._fearLevel) * dt * 2.2;

    // Despawn si trop loin (joueur fuit vite)
    if (this._dist > FLEE_DIST) {
      this._notifQueue.push('La créature perd votre trace.');
      this._despawn('fled');
      return;
    }

    // Capture / frayeur
    if (this._dist < SCARE_DIST) {
      this._scaredCount++;
      this._notifQueue.push('⚠ RENCONTRE — Fuyez plus vite !');
      this._despawn('scared');
      return;
    }

    // Wanted level rompt le sortilège
    if (wantedLevel >= 3) {
      this._notifQueue.push('La créature recule face au chaos.');
      this._despawn('police');
      return;
    }

    this._updateFearUI();
  }

  _updateFearUI() {
    const f = this._fearLevel;
    const alpha = f * 0.45;
    const glow  = Math.round(f * 80);
    this._fearEl.style.background   = `rgba(60,0,0,${alpha.toFixed(2)})`;
    this._fearEl.style.boxShadow    = `inset 0 0 ${glow}px rgba(200,0,0,${(f * 0.5).toFixed(2)})`;
    if (f > 0.25) {
      this._fearLabel.style.opacity = '1';
      const labels = {
        OMBRE:  `L'OMBRE EST À ${Math.round(this._dist)}m`,
        BÊTE:   `LA BÊTE EST À ${Math.round(this._dist)}m`,
        CYCLOPE:`LE CYCLOPE VOUS OBSERVE`,
      };
      this._fearLabel.textContent = this._monster
        ? (labels[this._monster.type] || `DANGER — ${Math.round(this._dist)}m`)
        : '';
    } else {
      this._fearLabel.style.opacity = '0';
    }
  }

  popNotif()       { return this._notifQueue.shift() || null; }
  isActive()       { return this._active; }
  getFearLevel()   { return this._fearLevel; }
  getMonsterType() { return this._monster?.type || '—'; }
  getDistance()    { return this._dist; }
  getScareCount()  { return this._scaredCount; }
  getCooldown()    { return this._cooldown; }
}
