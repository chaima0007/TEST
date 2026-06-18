import * as THREE from 'three';

// DreamZoneAgent — Ronde 23 — ONIRIQUE / MAGIQUE
// Des endroits que tu ne trouveras pas dans un jeu normal.
// Tourne à droite au bon moment — et tu tombes sur un autre monde.
// Inspiré de: Yume Nikki, Spirited Away, Disco Elysium, Monument Valley.

const ZONES = [
  {
    id:    'ames',
    name:  'Jardin des Âmes',
    desc:  'Des âmes bleues s\'élèvent — ce lieu ressemble à quelque chose d\'oublié',
    x: -68, z: -68,
    color: 0x0044ff, glowColor: 0x0088ff,
    radius: 18,
    bonus: 400,
    build: buildAmes,
  },
  {
    id:    'cristal',
    name:  'Cathédrale de Cristal',
    desc:  'Une forêt de flèches translucides. La lumière y est vivante.',
    x: 68, z: -68,
    color: 0x00ffee, glowColor: 0x00eecc,
    radius: 20,
    bonus: 350,
    build: buildCristal,
  },
  {
    id:    'aiguilles',
    name:  'Forêt des Aiguilles',
    desc:  'Mille fines colonnes magenta qui chuchotent quand on passe',
    x: -68, z: 68,
    color: 0xff00cc, glowColor: 0xaa0088,
    radius: 22,
    bonus: 380,
    build: buildAiguilles,
  },
  {
    id:    'source',
    name:  'Source de Lumière',
    desc:  'Une fontaine de lumière pure. Votre véhicule sera réparé.',
    x: 68, z: 68,
    color: 0xffee00, glowColor: 0xffaa00,
    radius: 16,
    bonus: 300,
    heals: true,
    build: buildSource,
  },
  {
    id:    'vortex',
    name:  'Vortex Cosmique',
    desc:  'Le centre de la ville cache une anomalie — le tissu du réel s\'effondre ici',
    x: 0, z: 0,
    color: 0x8800ff, glowColor: 0x4400cc,
    radius: 24,
    bonus: 600,
    teleports: true,
    build: buildVortex,
  },
  {
    id:    'miroir',
    name:  'Lac des Reflets',
    desc:  'Une ville entière à l\'envers. Laquelle est réelle ?',
    x: 0, z: -85,
    color: 0x88ccff, glowColor: 0x4488ff,
    radius: 19,
    bonus: 450,
    build: buildMiroir,
  },
];

// ── Builders ──────────────────────────────────────────────────────────────────

function makeParticles(scene, N, cx, cz, spread, height, color) {
  const pos = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    pos[i*3]   = cx + (Math.random() - 0.5) * spread;
    pos[i*3+1] = Math.random() * height;
    pos[i*3+2] = cz + (Math.random() - 0.5) * spread;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const mat = new THREE.PointsMaterial({ color, size: 0.35, sizeAttenuation: true, transparent: true, opacity: 0.9, depthWrite: false, blending: THREE.AdditiveBlending });
  const pts = new THREE.Points(geo, mat);
  scene.add(pts);
  return { pts, pos, posAttr: geo.attributes.position, N };
}

function buildAmes(scene, z) {
  const meshes = [], particles = [];
  const cx = z.x, cz = z.z;

  // Cristaux pointus bleus (ConeGeometry tournés)
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2;
    const r = 6 + Math.random() * 6;
    const h = 4 + Math.random() * 8;
    const mat = new THREE.MeshStandardMaterial({ color: 0x002288, metalness: 0.6, roughness: 0.1, emissive: 0x001144 });
    const m = new THREE.Mesh(new THREE.ConeGeometry(0.4 + Math.random() * 0.6, h, 5), mat);
    m.position.set(cx + Math.cos(a) * r, h / 2, cz + Math.sin(a) * r);
    m.rotation.y = a;
    scene.add(m); meshes.push(m);
  }

  // Lumière centrale bleue
  const l = new THREE.PointLight(0x0044ff, 6, 35);
  l.position.set(cx, 3, cz); scene.add(l); meshes.push(l);

  // Âmes (particules montantes)
  particles.push(makeParticles(scene, 280, cx, cz, 28, 14, 0x2266ff));
  particles.push(makeParticles(scene, 100, cx, cz, 12, 10, 0xaaccff));

  return { meshes, particles };
}

function buildCristal(scene, z) {
  const meshes = [], particles = [];
  const cx = z.x, cz = z.z;

  // Forêt de flèches translucides
  for (let i = 0; i < 20; i++) {
    const a = Math.random() * Math.PI * 2;
    const r = Math.random() * 14;
    const h = 3 + Math.random() * 12;
    const mat = new THREE.MeshStandardMaterial({
      color: 0x00ffee, metalness: 0.8, roughness: 0.05,
      transparent: true, opacity: 0.5 + Math.random() * 0.4,
      emissive: 0x004433, emissiveIntensity: 0.8,
    });
    const m = new THREE.Mesh(new THREE.ConeGeometry(0.3, h, 4), mat);
    m.position.set(cx + Math.cos(a) * r, h / 2, cz + Math.sin(a) * r);
    m.rotation.y = Math.random() * Math.PI;
    m.rotation.z = (Math.random() - 0.5) * 0.3;
    scene.add(m); meshes.push(m);
  }

  // Arche centrale
  const archMat = new THREE.MeshStandardMaterial({ color: 0x00ccee, metalness: 0.9, roughness: 0.0, transparent: true, opacity: 0.4 });
  const arch = new THREE.Mesh(new THREE.TorusGeometry(8, 0.5, 6, 24), archMat);
  arch.position.set(cx, 6, cz);
  arch.rotation.x = Math.PI / 2;
  scene.add(arch); meshes.push(arch);

  const l = new THREE.PointLight(0x00ffee, 7, 40);
  l.position.set(cx, 4, cz); scene.add(l); meshes.push(l);

  particles.push(makeParticles(scene, 200, cx, cz, 30, 16, 0x00eeff));

  return { meshes, particles };
}

function buildAiguilles(scene, z) {
  const meshes = [], particles = [];
  const cx = z.x, cz = z.z;

  // Forêt de fines colonnes magenta
  for (let i = 0; i < 35; i++) {
    const a = Math.random() * Math.PI * 2;
    const r = Math.random() * 16;
    const h = 6 + Math.random() * 16;
    const mat = new THREE.MeshStandardMaterial({
      color: 0xff00cc, metalness: 0.3, roughness: 0.6,
      emissive: 0x550033, emissiveIntensity: 0.4,
    });
    const m = new THREE.Mesh(new THREE.CylinderGeometry(0.08 + Math.random() * 0.15, 0.25, h, 5), mat);
    m.position.set(cx + Math.cos(a) * r, h / 2, cz + Math.sin(a) * r);
    m.rotation.z = (Math.random() - 0.5) * 0.12;
    scene.add(m); meshes.push(m);
  }

  const l = new THREE.PointLight(0xff00cc, 5, 38);
  l.position.set(cx, 5, cz); scene.add(l); meshes.push(l);

  particles.push(makeParticles(scene, 160, cx, cz, 26, 20, 0xff44cc));

  return { meshes, particles };
}

function buildSource(scene, z) {
  const meshes = [], particles = [];
  const cx = z.x, cz = z.z;

  // Fontaine centrale
  const baseMat = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.8, roughness: 0.1 });
  const base = new THREE.Mesh(new THREE.CylinderGeometry(2.5, 3.5, 1.0, 12), baseMat);
  base.position.set(cx, 0.5, cz); scene.add(base); meshes.push(base);

  const col = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.6, 2.5, 8), baseMat);
  col.position.set(cx, 1.8, cz); scene.add(col); meshes.push(col);

  const bowl = new THREE.Mesh(new THREE.SphereGeometry(2, 16, 8, 0, Math.PI*2, 0, Math.PI/2), baseMat);
  bowl.position.set(cx, 3, cz); scene.add(bowl); meshes.push(bowl);

  // Rayons dorés en étoile
  for (let i = 0; i < 8; i++) {
    const a = (i / 8) * Math.PI * 2;
    const mat = new THREE.MeshBasicMaterial({ color: 0xffee00, transparent: true, opacity: 0.6, blending: THREE.AdditiveBlending, depthWrite: false });
    const ray = new THREE.Mesh(new THREE.PlaneGeometry(0.3, 10), mat);
    ray.position.set(cx + Math.cos(a) * 5, 5, cz + Math.sin(a) * 5);
    ray.rotation.y = a;
    scene.add(ray); meshes.push(ray);
  }

  const l = new THREE.PointLight(0xffee00, 8, 35);
  l.position.set(cx, 4, cz); scene.add(l); meshes.push(l);

  particles.push(makeParticles(scene, 300, cx, cz, 20, 12, 0xffcc00));
  particles.push(makeParticles(scene, 100, cx, cz, 8, 18, 0xffffff));

  return { meshes, particles };
}

function buildVortex(scene, z) {
  const meshes = [], particles = [];
  const cx = z.x, cz = z.z;

  // Anneaux toroïdaux concentriques tournants
  for (let i = 0; i < 7; i++) {
    const r = 4 + i * 3.5;
    const mat = new THREE.MeshBasicMaterial({
      color: new THREE.Color().setHSL(i / 7, 1, 0.6),
      transparent: true, opacity: 0.35, blending: THREE.AdditiveBlending, depthWrite: false,
    });
    const torus = new THREE.Mesh(new THREE.TorusGeometry(r, 0.22, 5, 40), mat);
    torus.position.set(cx, 1 + i * 0.8, cz);
    torus.rotation.x = Math.PI / 2 + (i % 2 === 0 ? 0 : 0.4);
    torus.rotation.z = i * 0.25;
    torus.userData.rotSpeed = (i % 2 === 0 ? 1 : -1) * (0.3 + i * 0.08);
    scene.add(torus); meshes.push(torus);
  }

  // Pilier central noir avec fissures violettes
  const coreMat = new THREE.MeshStandardMaterial({ color: 0x000000, emissive: 0x220044 });
  const core = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 16, 8), coreMat);
  core.position.set(cx, 8, cz); scene.add(core); meshes.push(core);

  const l = new THREE.PointLight(0x8800ff, 10, 50);
  l.position.set(cx, 6, cz); scene.add(l); meshes.push(l);

  particles.push(makeParticles(scene, 400, cx, cz, 35, 20, 0x8844ff));
  particles.push(makeParticles(scene, 150, cx, cz, 10, 30, 0xcc00ff));

  return { meshes, particles };
}

function buildMiroir(scene, z) {
  const meshes = [], particles = [];
  const cx = z.x, cz = z.z;

  // Surface miroir (plane réfléchissant)
  const mirMat = new THREE.MeshStandardMaterial({
    color: 0x001122, metalness: 0.98, roughness: 0.01,
    transparent: true, opacity: 0.8,
  });
  const mirror = new THREE.Mesh(new THREE.CircleGeometry(14, 32), mirMat);
  mirror.rotation.x = -Math.PI / 2;
  mirror.position.set(cx, 0.04, cz); scene.add(mirror); meshes.push(mirror);

  // Statues renversées (bâtiments à l'envers)
  for (let i = 0; i < 6; i++) {
    const a = (i / 6) * Math.PI * 2;
    const r = 8;
    const h = 5 + Math.random() * 8;
    const mat = new THREE.MeshStandardMaterial({ color: 0x112244, metalness: 0.5, roughness: 0.4, emissive: 0x001122 });
    const bld = new THREE.Mesh(new THREE.BoxGeometry(2, h, 2), mat);
    bld.position.set(cx + Math.cos(a) * r, 0.04 - h / 2, cz + Math.sin(a) * r);
    scene.add(bld); meshes.push(bld);
  }

  // Cadres de fenêtre dans l'eau
  const l = new THREE.PointLight(0x4488ff, 6, 38);
  l.position.set(cx, 2, cz); scene.add(l); meshes.push(l);

  particles.push(makeParticles(scene, 180, cx, cz, 22, 4, 0x88aaff));

  return { meshes, particles };
}

// ── Agent principal ────────────────────────────────────────────────────────────

export class DreamZoneAgent {
  constructor(scene) {
    this._scene    = scene;
    this._time     = 0;
    this._zones    = [];
    this._notifQueue = [];
    this._pendingBonus = 0;
    this._pendingHeal  = false;
    this._pendingTeleport = false;
    this._currentZone  = null;

    for (const def of ZONES) {
      const built = def.build(scene, def);
      this._zones.push({
        def,
        meshes:    built.meshes,
        particles: built.particles,
        visited:   false,
        cooldown:  0,
      });
    }
  }

  update(dt, playerPos, vehicleDamage) {
    this._time += dt;
    this._currentZone = null;

    for (const zone of this._zones) {
      const { def } = zone;
      const dx = playerPos.x - def.x;
      const dz = playerPos.z - def.z;
      const dist = Math.sqrt(dx * dx + dz * dz);

      if (dist < def.radius) this._currentZone = def;

      // Zone entry bonus
      if (zone.cooldown > 0) {
        zone.cooldown -= dt;
      } else if (dist < def.radius * 0.7) {
        zone.cooldown = 60; // re-enter cooldown
        if (!zone.visited) zone.visited = true;

        this._notifQueue.push(`✦ ${def.name} — ${def.desc}`);
        this._pendingBonus += def.bonus;
        if (def.heals) this._pendingHeal = true;
        if (def.teleports) this._pendingTeleport = true;
      }

      // Animate particles
      for (const { pts, pos, posAttr, N } of zone.particles) {
        for (let i = 0; i < N; i++) {
          pos[i * 3 + 1] += dt * (0.8 + Math.sin(this._time + i) * 0.4);
          // Reset quand trop haut
          if (pos[i * 3 + 1] > 20) {
            pos[i * 3]     = def.x + (Math.random() - 0.5) * def.radius * 1.8;
            pos[i * 3 + 1] = 0;
            pos[i * 3 + 2] = def.z + (Math.random() - 0.5) * def.radius * 1.8;
          }
        }
        posAttr.needsUpdate = true;
      }

      // Animate toroïdes du vortex
      if (def.id === 'vortex') {
        for (const m of zone.meshes) {
          if (m.userData?.rotSpeed) {
            m.rotation.z += m.userData.rotSpeed * dt;
          }
        }
      }

      // Animate arche du cristal
      if (def.id === 'cristal') {
        for (const m of zone.meshes) {
          if (m.geometry?.type === 'TorusGeometry') {
            m.rotation.z += dt * 0.22;
          }
        }
      }

      // Pulse lumière selon zone
      for (const m of zone.meshes) {
        if (m.isLight) {
          const pulse = 0.8 + Math.sin(this._time * 1.5 + def.x * 0.1) * 0.25;
          m.intensity = (def === ZONES.find(z => z.id === 'vortex') ? 10 : 6) * pulse;
        }
      }
    }
  }

  popNotif()           { return this._notifQueue.shift() || null; }
  popBonus()           { const b = this._pendingBonus;    this._pendingBonus = 0;    return b; }
  popHeal()            { const h = this._pendingHeal;     this._pendingHeal = false; return h; }
  popTeleport()        { const t = this._pendingTeleport; this._pendingTeleport = false; return t; }
  getVisitedCount()    { return this._zones.filter(z => z.visited).length; }
  getTotalCount()      { return this._zones.length; }
  isInZone()           { return this._currentZone !== null; }
  getCurrentColor()    { return this._currentZone?.color ?? null; }
  getCurrentZoneName() { return this._currentZone?.name ?? null; }
}
