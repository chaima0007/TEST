// music.js — MusicAgent : Expert compositeur IA pour Open City.
// 4 compositions uniques générées entièrement par Web Audio API.
// Architecture : lookahead scheduler (Chris Wilson pattern) pour un timing
// musical parfait, indépendant du framerate du jeu.
//
//  CITY   — Miami Dorian 88 BPM : basse moelleuse, snare huilée, hi-hat syncopé
//  CHASE  — Neon Pursuit 128 BPM : 4-on-floor agressif, lead tendu, bass drive
//  NIGHT  — Fantôme 100 BPM : pad éthéré Cmaj7, arpège ascendant, kick minimal
//  BOSS   — L'Architecte 140 BPM : industriel, dissonant, staccato brutal

const LOOKAHEAD_MS   = 100;  // scheduler polling interval
const SCHEDULE_AHEAD = 0.18; // seconds to schedule ahead of currentTime

// ── Note table (A4=440 Hz, 12-TET) ──────────────────────────────────────────
const N = (() => {
  const NAMES = ['C','Cs','D','Ds','E','F','Fs','G','Gs','A','As','B'];
  const t = {};
  for (let oct = 1; oct <= 7; oct++) {
    for (let i = 0; i < 12; i++) {
      const semis = (oct - 4) * 12 + (i - 9);
      t[`${NAMES[i]}${oct}`] = 440 * Math.pow(2, semis / 12);
    }
  }
  return t;
})();

// ── Track definitions (16-step grids, 16th notes) ────────────────────────────

// Each pattern: 16 booleans = one bar
// Bass/melody: null = rest, else frequency in Hz

const TRACKS = {
  city: {
    bpm: 88,
    kick:   [1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
    snare:  [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
    hat:    [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1],
    bass: [ N.D3,null,N.D3,null, N.G2,null,N.A2,null,
            N.C3,null,N.D3,null, N.A2,null,N.G2,null ],
    melody: [N.A4,null,null,N.F4, null,null,N.G4,null,
             N.A4,null,N.C5,null, null,N.A4,null,null ],
    padNotes: [N.D4, N.F4, N.A4, N.C5], // Dm7
    padBars:  4,
  },
  chase: {
    bpm: 128,
    kick:   [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0],
    snare:  [0,0,0,0, 1,0,0,1, 0,0,0,0, 1,0,1,0],
    hat:    [1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0],
    bass: [ N.E3,null,N.E3,N.G3, null,N.B2,null,null,
            N.E3,null,N.F3,null, N.Ds3,null,N.E3,null ],
    melody: [N.E5,null,N.G5,null, N.Fs5,null,N.E5,null,
             N.Ds5,null,N.E5,null, N.F5,null,N.E5,null ],
    padNotes: [N.E4, N.G4, N.B4],
    padBars: 2,
  },
  night: {
    bpm: 100,
    kick:   [1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
    snare:  [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
    hat:    [0,0,0,1, 0,0,0,1, 0,0,0,1, 0,0,0,1],
    bass: [ N.C3,null,null,null, N.E3,null,null,null,
            N.F3,null,null,null, N.G3,null,null,null ],
    melody: [N.C5,N.E5,N.G5,N.B5, N.D5,null,N.F5,null,
             N.F5,N.A5,null,null, N.G5,N.B5,N.D5,null ],
    padNotes: [N.C4, N.E4, N.G4, N.B4], // Cmaj7
    padBars: 8,
  },
  boss: {
    bpm: 140,
    kick:   [1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,1],
    snare:  [0,0,0,0, 1,0,0,1, 0,0,0,0, 1,1,0,0],
    hat:    [1,1,0,1, 1,1,0,1, 1,1,0,1, 1,1,1,0],
    bass: [ N.B2,null,N.B2,null, N.C3,null,N.B2,null,
            N.Ds3,null,N.B2,null, N.C3,N.B2,null,null ],
    melody: [N.B4,null,N.D5,null, N.C5,null,null,null,
             N.Ds5,null,N.B4,null, N.C5,null,N.B4,null ],
    padNotes: [N.B3, N.D4, N.F4], // Bm flat-5 (dissonant)
    padBars: 2,
  },
};

// ── Synthesis helpers ─────────────────────────────────────────────────────────

function playKick(ctx, bus, time, vol = 0.55) {
  try {
    const osc = ctx.createOscillator();
    const g   = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(140, time);
    osc.frequency.exponentialRampToValueAtTime(45, time + 0.08);
    g.gain.setValueAtTime(vol, time);
    g.gain.exponentialRampToValueAtTime(0.0001, time + 0.22);
    osc.connect(g); g.connect(bus);
    osc.start(time); osc.stop(time + 0.25);
    osc.onended = () => { try { osc.disconnect(); g.disconnect(); } catch(e){} };
  } catch(e) {}
}

function playSnare(ctx, bus, time, vol = 0.28) {
  try {
    const buf = ctx.createBuffer(1, ctx.sampleRate * 0.12, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length);
    const src = ctx.createBufferSource();
    src.buffer = buf;
    const filt = ctx.createBiquadFilter();
    filt.type = 'highpass';
    filt.frequency.value = 2200;
    const g = ctx.createGain();
    g.gain.setValueAtTime(vol, time);
    g.gain.exponentialRampToValueAtTime(0.0001, time + 0.14);
    src.connect(filt); filt.connect(g); g.connect(bus);
    src.start(time);
    src.onended = () => { try { src.disconnect(); filt.disconnect(); g.disconnect(); } catch(e){} };
  } catch(e) {}
}

function playHat(ctx, bus, time, vol = 0.12) {
  try {
    const buf = ctx.createBuffer(1, ctx.sampleRate * 0.05, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length);
    const src = ctx.createBufferSource();
    src.buffer = buf;
    const filt = ctx.createBiquadFilter();
    filt.type = 'highpass';
    filt.frequency.value = 8000;
    const g = ctx.createGain();
    g.gain.setValueAtTime(vol, time);
    g.gain.exponentialRampToValueAtTime(0.0001, time + 0.06);
    src.connect(filt); filt.connect(g); g.connect(bus);
    src.start(time);
    src.onended = () => { try { src.disconnect(); filt.disconnect(); g.disconnect(); } catch(e){} };
  } catch(e) {}
}

function playNote(ctx, bus, freq, time, dur, type = 'sawtooth', vol = 0.18, attack = 0.01) {
  if (!freq) return;
  try {
    const osc = ctx.createOscillator();
    const g   = ctx.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    g.gain.setValueAtTime(0.0001, time);
    g.gain.linearRampToValueAtTime(vol, time + attack);
    g.gain.setValueAtTime(vol, time + dur - 0.02);
    g.gain.linearRampToValueAtTime(0.0001, time + dur);
    osc.connect(g); g.connect(bus);
    osc.start(time); osc.stop(time + dur + 0.05);
    osc.onended = () => { try { osc.disconnect(); g.disconnect(); } catch(e){} };
  } catch(e) {}
}

// ── MusicAgent ────────────────────────────────────────────────────────────────

export class MusicAgent {
  constructor(ctx, destination) {
    if (!ctx) return;
    this._ctx  = ctx;
    this._bus  = ctx.createGain();
    this._bus.gain.value = 0;
    this._bus.connect(destination);

    this._state       = null;
    this._step        = 0;
    this._nextTime    = 0;
    this._interval    = null;
    this._padNodes    = []; // sustained pad oscillators
    this._padBar      = 0;
  }

  // Call with 'city' | 'chase' | 'night' | 'boss' | null (silence).
  // Crossfades in ~0.6 s.
  setState(state) {
    if (state === this._state) return;
    this._state = state;
    this._stopSequencer();
    if (state && TRACKS[state]) {
      // Tiny delay so the fade-out of old pads finishes first
      setTimeout(() => this._startSequencer(), 150);
      this._bus.gain.setTargetAtTime(0.32, this._ctx.currentTime + 0.05, 0.55);
    } else {
      this._bus.gain.setTargetAtTime(0, this._ctx.currentTime, 0.6);
    }
  }

  _stopSequencer() {
    if (this._interval) { clearInterval(this._interval); this._interval = null; }
    for (const n of this._padNodes) {
      try { n.gain.gain.setTargetAtTime(0, this._ctx.currentTime, 0.3);
            n.osc.stop(this._ctx.currentTime + 1); } catch(e) {}
    }
    this._padNodes = [];
  }

  _startSequencer() {
    if (!this._state || !TRACKS[this._state]) return;
    this._step     = 0;
    this._nextTime = this._ctx.currentTime + 0.1;
    this._padBar   = 0;
    this._schedulePad();
    this._interval = setInterval(() => this._tick(), LOOKAHEAD_MS);
  }

  _tick() {
    if (!this._state) return;
    const def = TRACKS[this._state];
    const step16 = 60 / def.bpm / 4; // duration of a 16th note in seconds

    while (this._nextTime < this._ctx.currentTime + SCHEDULE_AHEAD) {
      const s = this._step;

      if (def.kick[s])           playKick(this._ctx, this._bus, this._nextTime);
      if (def.snare[s])          playSnare(this._ctx, this._bus, this._nextTime);
      if (def.hat[s])            playHat(this._ctx, this._bus, this._nextTime);
      if (def.bass[s])           playNote(this._ctx, this._bus, def.bass[s] / 2, this._nextTime, step16 * 1.8, 'sawtooth', 0.22);
      if (def.melody[s])         playNote(this._ctx, this._bus, def.melody[s], this._nextTime, step16 * 0.85, 'sine', 0.09, 0.02);

      // Trigger new pad chord every N bars
      if (s === 0) {
        this._padBar = (this._padBar + 1) % def.padBars;
        if (this._padBar === 0) this._schedulePad();
      }

      this._step = (this._step + 1) % 16;
      this._nextTime += step16;
    }
  }

  _schedulePad() {
    if (!this._state) return;
    const def = TRACKS[this._state];
    const barsS = (60 / def.bpm) * 4 * def.padBars; // pad duration in seconds

    // Fade out old pads
    for (const n of this._padNodes) {
      try {
        n.gain.gain.setTargetAtTime(0, this._ctx.currentTime, 0.4);
        n.osc.stop(this._ctx.currentTime + 1.5);
      } catch(e) {}
    }
    this._padNodes = [];

    // New pad chord
    for (const freq of def.padNotes) {
      try {
        const osc  = this._ctx.createOscillator();
        const gain = this._ctx.createGain();
        osc.type = 'sine';
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(0, this._ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.055, this._ctx.currentTime + 0.8);
        gain.gain.setValueAtTime(0.055, this._ctx.currentTime + barsS - 0.8);
        gain.gain.linearRampToValueAtTime(0, this._ctx.currentTime + barsS);
        osc.connect(gain); gain.connect(this._bus);
        osc.start(this._ctx.currentTime);
        osc.stop(this._ctx.currentTime + barsS + 0.1);
        this._padNodes.push({ osc, gain });
      } catch(e) {}
    }
  }

  dispose() {
    this._stopSequencer();
    try { this._bus.disconnect(); } catch(e) {}
  }
}
