// dialogue.js — Expert Dialogue IA (drôle · sérieux · triste)
// Génère du dialogue procédural pour les piétons selon :
//   • Humeur de la personnalité (TOURISTE→drôle, PRESSÉ→sérieux, NERVEUX→triste…)
//   • Contexte du jeu (police, crash, pluie, nuit, boss)
//   • Proximité du joueur (déclenchement dans un rayon de 7 m)
// Affichage via bulles CSS positionnées en espace écran (projection 3D→2D).
// Zéro texture externe — pur DOM + projection Three.js.

import * as THREE from 'three';

// ── Banque de répliques ───────────────────────────────────────────────────────

export const LINES = {
  drole: [
    'Il fait chaud ou c\'est moi qui cours ?',
    'Mon GPS dit "destination atteinte"… depuis 3 rues.',
    'J\'ai vu des trucs. Des trucs.',
    'Les pigeons ici sont plus stressés que moi.',
    'Mon bus est en retard. C\'est sa passion.',
    'J\'aurais dû prendre la voiture.',
    'Quelqu\'un a vu mes clés ?',
    'Cette ville me doit une explication.',
    'J\'adore marcher. Disait personne jamais.',
    'Encore du café. Toujours du café.',
    'Pourquoi courir ? Tout finit pareil.',
    'La route est longue et mes jambes sont courtes.',
    'Je suis perdu. Mais c\'est bon pour l\'aventure.',
    'Mon téléphone est à 2 %. C\'est ma vie.',
    'Je cherche le bonheur. Il est où le parking ?',
  ],
  serieux: [
    'Cette ville ne dort jamais.',
    'Quelqu\'un surveille tout ici.',
    'La nuit tombe. Rentrez.',
    'Faites attention à qui vous parlez.',
    'Ce n\'est pas un endroit pour les honnêtes gens.',
    'Les rues ont des yeux.',
    'Ne traînez pas seul le soir.',
    'J\'ai vu des choses que je ne peux pas raconter.',
    'Chacun ses secrets dans cette ville.',
    'Méfiez-vous du silence.',
    'Rien n\'arrive sans raison ici.',
    'Les ombres bougent plus vite que les gens.',
    'Cette ville mange les imprudents.',
    'Gardez la tête baissée.',
    'Certains font des choix. D\'autres les subissent.',
  ],
  triste: [
    'Je me souviens quand ce quartier était beau...',
    'Encore une nuit dans cette ville sans mémoire.',
    'J\'ai perdu quelque chose ici. Je ne sais plus quoi.',
    'Les rues changent. Les gens restent les mêmes.',
    'Mon chien est parti hier.',
    'Certains jours, la ville pèse trop lourd.',
    'Je cherche quelque chose que je n\'ai peut-être jamais eu.',
    'Le temps passe différemment ici.',
    'On finit tous par se perdre.',
    'Je rentre. Mais où est chez moi ?',
    'J\'ai raté quelque chose. Quelque chose d\'important.',
    'Les lumières clignotent. Comme mes espoirs.',
    'Il y a longtemps, je souriais en marchant ici.',
    'Cette pluie… elle ressemble à ma vie.',
    'Personne ne me cherche. Personne.',
  ],
  // Contextuelles — déclenchées par des événements précis
  police: [
    'La police encore… restez calme.',
    'Sirènes. Rien d\'étonnant.',
    'Bougez pas, ça va passer.',
    'C\'est la chasse !',
    'Qui a fait ça encore ?',
    'Dieu merci, ce n\'est pas pour moi.',
  ],
  crash: [
    'Vous avez vu ça ?!',
    'Incroyable !',
    'Appelez le 15 !',
    'C\'est pas possible ce bruit…',
    'Ça va vraiment pas du tout !',
    'Le monde est fou.',
  ],
  pluie: [
    'Encore cette pluie...',
    'J\'ai oublié mon parapluie. Comme d\'hab.',
    'La ville pleure. Ou c\'est moi.',
    'Belle journée pour se noyer.',
    'Cette pluie nettoie rien du tout.',
  ],
  nuit: [
    'La nuit, tout est différent ici.',
    'Ces lumières… jamais éteintes.',
    'Encore debout à cette heure ?',
    'La nuit cache beaucoup de choses.',
    'Je marche mieux quand le soleil dort.',
  ],
  boss: [
    'Cette voiture noire… elle revient.',
    'Quelqu\'un de puissant est en ville.',
    'Je sens que ça va chauffer.',
    'Cette nuit va être longue.',
    'Fuyez. Fuyez maintenant.',
  ],
};

// Humeur par défaut selon la personnalité trafic
const MOOD_MAP = {
  TOURISTE: 'drole',
  PRESSÉ:   'serieux',
  JOGGEUR:  'drole',
  NERVEUX:  'triste',
  COSTAUD:  'serieux',
};

function rand(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

// ── Styles des bulles ─────────────────────────────────────────────────────────

const BUBBLE_CSS = `
#dlg-overlay { position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:200;overflow:hidden; }
.dlg-bubble {
  position:absolute;
  transform:translate(-50%,-110%);
  background:rgba(8,10,20,0.82);
  border:1px solid rgba(255,255,255,0.18);
  border-radius:10px;
  padding:5px 10px;
  font-size:11.5px;
  font-weight:600;
  line-height:1.35;
  white-space:nowrap;
  max-width:220px;
  white-space:normal;
  pointer-events:none;
  transition:opacity 0.25s;
  font-family:'Segoe UI',Arial,sans-serif;
}
.dlg-bubble::after {
  content:'';
  position:absolute;
  bottom:-7px;left:50%;transform:translateX(-50%);
  border:7px solid transparent;
  border-top-color:rgba(8,10,20,0.82);
  border-bottom:none;
}
.dlg-drole   { color:#ffe87a; border-color:rgba(255,230,80,0.30); }
.dlg-serieux { color:#c9dfff; border-color:rgba(100,160,255,0.25); }
.dlg-triste  { color:#b8c8d8; border-color:rgba(120,160,200,0.20); }
.dlg-ctx     { color:#ff9944; border-color:rgba(255,150,50,0.30); }
`;

function injectStyles() {
  if (typeof document === 'undefined') return;
  if (document.getElementById('dlg-styles')) return;
  const s = document.createElement('style');
  s.id = 'dlg-styles';
  s.textContent = BUBBLE_CSS;
  document.head.appendChild(s);
}

// ── DialogueAgent ─────────────────────────────────────────────────────────────

export class DialogueAgent {
  constructor() {
    this._active  = new Map(); // mesh → { text, mood, timer, ttl, el }
    this._cooldowns = new WeakMap(); // ped → secondes avant prochain dialogue
    this._v3 = new THREE.Vector3();
    this._overlay = null;

    if (typeof document !== 'undefined') {
      injectStyles();
      this._overlay = document.createElement('div');
      this._overlay.id = 'dlg-overlay';
      document.body.appendChild(this._overlay);
    }
  }

  // Assigne une réplique à un piéton.
  // mood     : 'drole' | 'serieux' | 'triste' (null → déduit depuis personnalité)
  // context  : chaîne optionnelle parmi les clés contextuelles ('police', 'crash'…)
  // Retourne le texte sélectionné (pour les tests sans DOM).
  trigger(ped, mood = null, context = null) {
    if (!ped || !ped.mesh) return null;
    // Pas de doublon pour le même piéton
    if (this._active.has(ped.mesh)) return null;

    let pool;
    if (context && LINES[context]) {
      pool = LINES[context];
      mood = 'ctx';
    } else {
      const m = mood || MOOD_MAP[ped.personality?.name] || 'drole';
      mood = m;
      pool = LINES[m] || LINES.drole;
    }

    const text = rand(pool);
    const ttl  = 3.5 + text.length * 0.025; // durée proportionnelle à la longueur

    const entry = { text, mood, timer: ttl, ttl, el: null };
    this._active.set(ped.mesh, entry);
    this._cooldowns.set(ped, 12 + Math.random() * 8); // 12-20 s avant prochain

    if (this._overlay) {
      const el = document.createElement('div');
      el.className = `dlg-bubble dlg-${mood}`;
      el.textContent = text;
      this._overlay.appendChild(el);
      entry.el = el;
    }

    return text;
  }

  // gameCtx : { wantedLevel, weatherId, isNight, architectActive, recentCrash }
  update(dt, pedestrians, playerPos, camera, renderer, gameCtx = {}) {
    const { wantedLevel = 0, weatherId = 'sunny', isNight = false,
            architectActive = false, recentCrash = false } = gameCtx;

    // ── Vieillissement des cooldowns ──────────────────────────────────
    for (const ped of pedestrians) {
      if (!ped.active) continue;
      const cd = this._cooldowns.get(ped) || 0;
      if (cd > 0) this._cooldowns.set(ped, cd - dt);
    }

    // ── Déclenchement contextuel : événements globaux ─────────────────
    const activePeds = pedestrians.filter(p => p.active && p.mesh);
    if (recentCrash && Math.random() < 0.04) {
      const nearby = activePeds.filter(p =>
        playerPos && Math.hypot(p.mesh.position.x - playerPos.x, p.mesh.position.z - playerPos.z) < 14
      );
      if (nearby.length) this.trigger(rand(nearby), null, 'crash');
    }
    if (wantedLevel >= 2 && Math.random() < 0.008) {
      const target = rand(activePeds);
      if (target) this.trigger(target, null, 'police');
    }
    if (architectActive && Math.random() < 0.005) {
      const target = rand(activePeds);
      if (target) this.trigger(target, null, 'boss');
    }

    // ── Déclenchement de proximité joueur ─────────────────────────────
    if (playerPos) {
      for (const ped of activePeds) {
        if (this._cooldowns.get(ped) > 0) continue;
        if (this._active.has(ped.mesh)) continue;
        const dist = Math.hypot(ped.mesh.position.x - playerPos.x, ped.mesh.position.z - playerPos.z);
        if (dist < 7 && Math.random() < 0.003) {
          // Choix du contexte selon conditions
          let ctx = null;
          if (isNight && Math.random() < 0.4) ctx = 'nuit';
          else if (weatherId === 'rain' && Math.random() < 0.4) ctx = 'pluie';
          this.trigger(ped, null, ctx);
        }
      }
    }

    // ── Vieillissement et projection des bulles actives ───────────────
    const canvasW = renderer?.domElement?.clientWidth  || (typeof window !== 'undefined' ? window.innerWidth  : 800);
    const canvasH = renderer?.domElement?.clientHeight || (typeof window !== 'undefined' ? window.innerHeight : 600);

    for (const [mesh, entry] of this._active) {
      entry.timer -= dt;
      if (entry.timer <= 0) {
        if (entry.el) { entry.el.remove(); }
        this._active.delete(mesh);
        continue;
      }

      // Projection 3D → 2D
      if (entry.el && camera) {
        this._v3.set(mesh.position.x, mesh.position.y + 2.3, mesh.position.z);
        this._v3.project(camera);
        const screenX = (this._v3.x + 1) * canvasW / 2;
        const screenY = (-this._v3.y + 1) * canvasH / 2;
        const inView  = this._v3.z < 1 && screenX > -50 && screenX < canvasW + 50 && screenY > -50 && screenY < canvasH + 100;

        entry.el.style.left    = `${screenX}px`;
        entry.el.style.top     = `${screenY}px`;
        entry.el.style.opacity = inView ? Math.min(1, entry.timer / 0.4, (entry.ttl - entry.timer + 0.3) / 0.3) : '0';
      }
    }
  }

  // Nombre de bulles actives (pour tests et HUD)
  getActiveCount() { return this._active.size; }

  // Retourne les entrées actives sans DOM (pour tests)
  getActiveEntries() {
    return [...this._active.values()].map(e => ({ text: e.text, mood: e.mood, timer: e.timer }));
  }

  dispose() {
    if (this._overlay) this._overlay.remove();
    this._active.clear();
  }
}
