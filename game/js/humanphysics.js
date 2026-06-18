// humanphysics.js — Expert Physique Humaine IA
// Couche de dynamiques corporelles réalistes par-dessus CharacterAnimator.
// Applique : inclinaison du corps (lean spring), respiration, trébuchement,
// chute/relèvement, et regard actif vers une cible (head tracking).
// Appelé APRÈS CharacterAnimator.update() pour compléter ses valeurs.

const LEAN_SPRING   = 9;     // raideur du ressort de rappel (rad/s²)
const LEAN_DAMP     = 0.82;  // amortissement par frame
const MAX_LEAN_FWD  = 0.18;  // rad max inclinaison avant (~10°)
const MAX_LEAN_SIDE = 0.20;  // rad max inclinaison latérale (~11°)
const HEAD_SPEED    = 3.5;   // rad/s de rotation de la tête vers la cible
const BREATH_RATE   = 0.30;  // Hz de base de la respiration
const BREATH_AMP    = 0.007; // amplitude breathing (mètres)

function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

export class HumanPhysicsAgent {
  constructor() {
    // État physique individuel stocké par référence de mesh (WeakMap → pas de fuite mémoire)
    this._states = new WeakMap();
  }

  _state(mesh) {
    if (!this._states.has(mesh)) {
      this._states.set(mesh, {
        leanX: 0, leanZ: 0,       // inclinaison actuelle (rad)
        leanVelX: 0, leanVelZ: 0, // vitesse du ressort
        stumbleTimer: 0,           // durée restante du trébuchement (s)
        fallTimer: 0,              // durée restante de la chute (s)
        breathPhase: Math.random() * Math.PI * 2,
        headYaw: 0,                // rotation courante de la tête (rad)
        inFall: false,
      });
    }
    return this._states.get(mesh);
  }

  // mesh     : root Group de buildDetailedCharacter()
  // speed    : vitesse de déplacement m/s
  // angVel   : vitesse angulaire rad/s (positif = gauche, négatif = droite)
  // dt       : delta temps secondes
  // opts     : { stumble:bool, fall:bool, headTarget:{x,z}|null }
  update(mesh, speed, angVel, dt, opts = {}) {
    const b = mesh.userData.bones;
    if (!b) return;
    const s = this._state(mesh);

    // ── Respiration ───────────────────────────────────────────────────
    s.breathPhase += dt * (BREATH_RATE + speed * 0.06) * Math.PI * 2;
    const breathOff = Math.sin(s.breathPhase) * BREATH_AMP;
    // Ajoute au headGroup.position.y déjà fixé par CharacterAnimator
    b.headGroup.position.y += breathOff;

    // ── Déclenchement trébuchement / chute ───────────────────────────
    if (opts.stumble && s.stumbleTimer <= 0 && s.fallTimer <= 0) {
      s.stumbleTimer = 0.55;
    }
    if (opts.fall && s.fallTimer <= 0 && s.stumbleTimer <= 0) {
      s.fallTimer = 1.9;
      s.inFall = true;
    }

    // ── Séquence chute + relèvement (prioritaire sur tout le reste) ──
    if (s.fallTimer > 0) {
      s.fallTimer -= dt;
      const progress = 1 - s.fallTimer / 1.9;
      if (progress < 0.3) {
        // Bascule : tombe vers l'avant
        const t = progress / 0.3;
        mesh.rotation.x = t * 1.35;
        mesh.position.y = -t * 0.55;
        b.uArmL.rotation.x = t * 1.1;
        b.uArmR.rotation.x = t * 1.1;
      } else if (progress < 0.65) {
        // À terre : reste couché
        mesh.rotation.x = 1.35;
        mesh.position.y = -0.55;
        b.uArmL.rotation.x = 1.1;
        b.uArmR.rotation.x = 1.1;
      } else {
        // Relèvement
        const t = 1 - (progress - 0.65) / 0.35;
        mesh.rotation.x = t * 1.35;
        mesh.position.y = -t * 0.55;
        b.uArmL.rotation.x = t * 0.9;
        b.uArmR.rotation.x = t * 0.9;
      }
      if (s.fallTimer <= 0) { s.inFall = false; mesh.position.y = 0; }
      return; // bloque lean et head tracking pendant la chute
    }
    mesh.position.y = 0;

    // ── Trébuchement ─────────────────────────────────────────────────
    if (s.stumbleTimer > 0) {
      s.stumbleTimer -= dt;
      const t = 1 - s.stumbleTimer / 0.55;
      const stumbleLean = Math.sin(t * Math.PI) * 0.42;
      mesh.rotation.x = s.leanX + stumbleLean;
      b.uArmL.rotation.x += Math.sin(t * Math.PI * 2) * 0.75;
      b.uArmR.rotation.x -= Math.sin(t * Math.PI * 2) * 0.75;
      // Pas de lean/tracking pendant trébuchement
      return;
    }

    // ── Inclinaison corporelle (lean spring) ─────────────────────────
    // Lean avant = proportionnel à la vitesse, lean latéral = virage
    const targetX = clamp(speed * 0.022, 0, MAX_LEAN_FWD);
    const targetZ = clamp(-angVel * 0.15, -MAX_LEAN_SIDE, MAX_LEAN_SIDE);

    s.leanVelX += (targetX - s.leanX) * LEAN_SPRING * dt;
    s.leanVelZ += (targetZ - s.leanZ) * LEAN_SPRING * dt;
    s.leanVelX *= LEAN_DAMP;
    s.leanVelZ *= LEAN_DAMP;
    s.leanX += s.leanVelX * dt;
    s.leanZ += s.leanVelZ * dt;

    mesh.rotation.x = s.leanX;
    mesh.rotation.z = s.leanZ;

    // ── Head tracking vers cible ──────────────────────────────────────
    if (opts.headTarget) {
      const dx = opts.headTarget.x - mesh.position.x;
      const dz = opts.headTarget.z - mesh.position.z;
      const worldAngle = Math.atan2(dx, dz);
      // Angle relatif à la rotation du personnage
      const rel = worldAngle - mesh.rotation.y;
      const wrapped = Math.atan2(Math.sin(rel), Math.cos(rel));
      const target  = clamp(wrapped, -0.85, 0.85);
      s.headYaw += (target - s.headYaw) * HEAD_SPEED * dt;
    } else {
      // Retour position neutre avec amortissement
      s.headYaw *= Math.pow(0.05, dt);
    }
    b.headGroup.rotation.y = s.headYaw;
  }

  // Déclenche un trébuchement sur un mesh donné (appel externe depuis traffic.js)
  stumble(mesh) {
    const s = this._state(mesh);
    if (s.stumbleTimer <= 0 && s.fallTimer <= 0) s.stumbleTimer = 0.55;
  }

  // Déclenche une chute sur un mesh (appel externe)
  fall(mesh) {
    const s = this._state(mesh);
    if (s.fallTimer <= 0) s.fallTimer = 1.9;
  }

  isDown(mesh) {
    const s = this._states.get(mesh);
    return s ? s.inFall || s.stumbleTimer > 0 : false;
  }
}
