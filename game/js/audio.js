// audio.js — procedural sound effects via the Web Audio API only.
//
// No external audio assets are used (none exist in this offline-friendly
// project and we can't fetch any from a CDN). Everything here is synthesized
// at runtime with OscillatorNode/GainNode/BiquadFilterNode/etc.
//
// Usage (intended wiring from main.js, not done by this module):
//   const audio = new AudioSystem();
//   audio.setEngineIntensity(Math.abs(vehicle.getSpeedKmh()) / MAX_SPEED_KMH);
//   audio.setSirenActive(wanted.level > 0);
//   audio.playCollision(intensity);   // on hard impact
//   audio.playUiBlip();               // on mission complete / wanted level change
//   audio.dispose();                  // on teardown
//
// Autoplay policy: browsers block audio until a user gesture occurs. The
// AudioContext is created eagerly (it starts "suspended" in that case) and
// we listen once for the first keydown/pointerdown/touchstart on window to
// resume it. All public methods are written defensively so that calling
// them before the context is resumed (or if Web Audio is unavailable, or if
// resume() rejects) never throws.

const SMOOTH_TIME = 0.08; // seconds, used for setTargetAtTime ramps

export class AudioSystem {
  constructor() {
    this._ctx = null;
    this._master = null;
    this._disposed = false;

    this._engine = null;
    this._siren = null;
    this._sirenActive = false;
    this._drift = null;   // tire screech oscillator
    this._chase = null;   // chase/tension music layer

    // Bound listener refs so we can remove them on dispose().
    this._onFirstGesture = this._onFirstGesture.bind(this);
    this._gestureEvents = ['keydown', 'pointerdown', 'touchstart'];

    try {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) {
        // Web Audio not available in this environment at all.
        this._ctx = null;
        return;
      }
      this._ctx = new Ctx();

      this._master = this._ctx.createGain();
      this._master.gain.value = 0.8;
      this._master.connect(this._ctx.destination);

      this._buildEngine();
      this._buildSiren();
      this._buildDrift();
      this._buildChase();

      for (const evt of this._gestureEvents) {
        window.addEventListener(evt, this._onFirstGesture, { once: false, passive: true });
      }
    } catch (err) {
      // Never let audio setup break the game.
      this._ctx = null;
    }
  }

  _onFirstGesture() {
    if (!this._ctx) return;
    if (this._ctx.state === 'suspended') {
      this._ctx.resume().catch(() => {
        // Autoplay still blocked (or context closed) — ignore, we'll retry
        // on the next gesture event since we don't remove the listeners
        // until dispose() or a confirmed successful resume.
      });
    }
    if (this._ctx.state === 'running') {
      for (const evt of this._gestureEvents) {
        window.removeEventListener(evt, this._onFirstGesture);
      }
    }
  }

  // --- Engine drone ---------------------------------------------------

  _buildEngine() {
    const ctx = this._ctx;

    const osc = ctx.createOscillator();
    osc.type = 'sawtooth';
    osc.frequency.value = 40;

    // A second, lower oscillator one octave down adds body/grit.
    const subOsc = ctx.createOscillator();
    subOsc.type = 'square';
    subOsc.frequency.value = 20;

    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 400;
    filter.Q.value = 0.7;

    const gain = ctx.createGain();
    gain.gain.value = 0.0001; // effectively silent until intensity is set

    osc.connect(filter);
    subOsc.connect(filter);
    filter.connect(gain);
    gain.connect(this._master);

    try {
      osc.start();
      subOsc.start();
    } catch (err) {
      // Starting before a user gesture can throw in some browsers; the
      // oscillators are silent (gain ~0) anyway so this is harmless either
      // way, but guard against it just in case.
    }

    this._engine = { osc, subOsc, filter, gain, lastRatio: 0 };
  }

  // Called every frame with 0..1 (current speed / top speed). Cheap: only
  // adjusts existing node parameters, never allocates new nodes.
  setEngineIntensity(speedRatio) {
    if (!this._ctx || !this._engine) return;
    const ratio = clamp01(speedRatio);
    this._engine.lastRatio = ratio;

    const ctx = this._ctx;
    const now = ctx.currentTime;

    // Idle ~40Hz rumble rising to ~140Hz at top speed.
    const baseFreq = 40 + ratio * 100;
    const subFreq = baseFreq * 0.5;
    // Volume rises with speed but never fully silent at idle (engine still
    // "running"), and never deafening at top speed.
    const targetGain = 0.015 + ratio * 0.09;
    const targetFilterFreq = 300 + ratio * 2200;

    try {
      this._engine.osc.frequency.setTargetAtTime(baseFreq, now, SMOOTH_TIME);
      this._engine.subOsc.frequency.setTargetAtTime(subFreq, now, SMOOTH_TIME);
      this._engine.gain.gain.setTargetAtTime(targetGain, now, SMOOTH_TIME);
      this._engine.filter.frequency.setTargetAtTime(targetFilterFreq, now, SMOOTH_TIME);
    } catch (err) {
      // Defensive: ignore if context got closed concurrently.
    }
  }

  // --- Police siren -----------------------------------------------------

  _buildSiren() {
    const ctx = this._ctx;

    const osc = ctx.createOscillator();
    osc.type = 'sine';
    osc.frequency.value = 700;

    const gain = ctx.createGain();
    gain.gain.value = 0; // silent until activated

    osc.connect(gain);
    gain.connect(this._master);

    try {
      osc.start();
    } catch (err) {
      // see note in _buildEngine
    }

    this._siren = {
      osc,
      gain,
      lfoId: null, // interval id driving the two-tone wail
      phase: 0,
    };
  }

  // Toggles a classic two-tone wail on/off. Loops while active; stops
  // cleanly (ramped gain to 0, LFO cleared) when deactivated. Reuses the
  // same oscillator/gain rather than creating new nodes per call.
  setSirenActive(active) {
    if (!this._ctx || !this._siren) return;
    const want = !!active;
    if (want === this._sirenActive) return;
    this._sirenActive = want;

    const ctx = this._ctx;
    const now = ctx.currentTime;
    const siren = this._siren;

    if (want) {
      // Fade in, then drive frequency in a two-tone wail via a lightweight
      // interval that nudges the oscillator's target frequency. Using
      // setInterval here (instead of scheduling many future automation
      // events) keeps this simple and self-correcting if the tab is backgrounded.
      try {
        siren.gain.gain.setTargetAtTime(0.07, now, SMOOTH_TIME);
      } catch (err) {
        /* ignore */
      }

      if (siren.lfoId == null) {
        const TONE_HIGH = 880;
        const TONE_LOW = 660;
        const SWITCH_MS = 420; // duration of each tone, classic wail cadence
        siren.lfoId = setInterval(() => {
          if (!this._ctx) return;
          siren.phase = 1 - siren.phase;
          const freq = siren.phase ? TONE_HIGH : TONE_LOW;
          try {
            siren.osc.frequency.setTargetAtTime(freq, this._ctx.currentTime, 0.06);
          } catch (err) {
            /* ignore */
          }
        }, SWITCH_MS);
      }
    } else {
      try {
        siren.gain.gain.setTargetAtTime(0, now, SMOOTH_TIME);
      } catch (err) {
        /* ignore */
      }
      if (siren.lfoId != null) {
        clearInterval(siren.lfoId);
        siren.lfoId = null;
      }
    }
  }

  // --- Drift screech -------------------------------------------------------

  _buildDrift() {
    const ctx = this._ctx;
    // White noise through a band-pass filter = tire screech
    const bufLen = ctx.sampleRate * 2;
    const buf = ctx.createBuffer(1, bufLen, ctx.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < bufLen; i++) data[i] = Math.random() * 2 - 1;

    const src = ctx.createBufferSource();
    src.buffer = buf;
    src.loop = true;

    const filter = ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.value = 280;
    filter.Q.value = 3.5;

    const gain = ctx.createGain();
    gain.gain.value = 0;

    src.connect(filter);
    filter.connect(gain);
    gain.connect(this._master);
    try { src.start(); } catch (e) { /* silent */ }
    this._drift = { src, filter, gain };
  }

  setDriftActive(active) {
    if (!this._ctx || !this._drift) return;
    const now = this._ctx.currentTime;
    try {
      const target = active ? 0.18 : 0;
      this._drift.gain.gain.setTargetAtTime(target, now, 0.06);
      if (active) this._drift.filter.frequency.setTargetAtTime(280 + Math.random() * 80, now, 0.1);
    } catch (e) { /* ignore */ }
  }

  // --- Chase music (tension drone) ----------------------------------------

  _buildChase() {
    const ctx = this._ctx;
    const osc1 = ctx.createOscillator();
    osc1.type = 'sawtooth';
    osc1.frequency.value = 65;

    const osc2 = ctx.createOscillator();
    osc2.type = 'square';
    osc2.frequency.value = 98;

    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 180;
    filter.Q.value = 1.2;

    const gain = ctx.createGain();
    gain.gain.value = 0;

    osc1.connect(filter);
    osc2.connect(filter);
    filter.connect(gain);
    gain.connect(this._master);
    try { osc1.start(); osc2.start(); } catch (e) { /* silent */ }
    this._chase = { osc1, osc2, filter, gain };
  }

  // intensity 0-1 (wanted.level / 5)
  setChaseIntensity(intensity) {
    if (!this._ctx || !this._chase) return;
    const now = this._ctx.currentTime;
    try {
      const vol = clamp01(intensity) * 0.07;
      this._chase.gain.gain.setTargetAtTime(vol, now, 0.3);
      const f1 = 65 + intensity * 45;
      const f2 = 98 + intensity * 60;
      this._chase.osc1.frequency.setTargetAtTime(f1, now, 0.5);
      this._chase.osc2.frequency.setTargetAtTime(f2, now, 0.5);
      this._chase.filter.frequency.setTargetAtTime(180 + intensity * 400, now, 0.3);
    } catch (e) { /* ignore */ }
  }

  // --- One-shot SFX -------------------------------------------------------

  // Short noise/thump for car-vs-building collisions. intensity 0..1 scales
  // volume and brightness/length of the thump. Builds a short-lived buffer
  // source + envelope each call (one-shots are expected to allocate; this
  // is not called every frame like setEngineIntensity).
  playCollision(intensity) {
    if (!this._ctx) return;
    const ctx = this._ctx;
    const amt = clamp01(intensity);
    const now = ctx.currentTime;

    try {
      // Noise burst (white noise) for the "crunch".
      const duration = 0.18 + amt * 0.12;
      const sampleCount = Math.max(1, Math.floor(ctx.sampleRate * duration));
      const buffer = ctx.createBuffer(1, sampleCount, ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < sampleCount; i++) {
        // Exponential decay envelope baked into the noise itself.
        const t = i / sampleCount;
        const decay = Math.pow(1 - t, 3);
        data[i] = (Math.random() * 2 - 1) * decay;
      }

      const noiseSrc = ctx.createBufferSource();
      noiseSrc.buffer = buffer;

      const noiseFilter = ctx.createBiquadFilter();
      noiseFilter.type = 'lowpass';
      noiseFilter.frequency.value = 300 + amt * 1500;

      const noiseGain = ctx.createGain();
      noiseGain.gain.value = 0.25 + amt * 0.55;

      noiseSrc.connect(noiseFilter);
      noiseFilter.connect(noiseGain);
      noiseGain.connect(this._master);

      // Low-frequency "thump" body underneath the noise crunch.
      const thumpOsc = ctx.createOscillator();
      thumpOsc.type = 'sine';
      const startFreq = 90 + amt * 40;
      thumpOsc.frequency.setValueAtTime(startFreq, now);
      thumpOsc.frequency.exponentialRampToValueAtTime(Math.max(30, startFreq * 0.35), now + 0.16);

      const thumpGain = ctx.createGain();
      const thumpPeak = 0.3 + amt * 0.5;
      thumpGain.gain.setValueAtTime(thumpPeak, now);
      thumpGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.22);

      thumpOsc.connect(thumpGain);
      thumpGain.connect(this._master);

      noiseSrc.start(now);
      noiseSrc.stop(now + duration);
      thumpOsc.start(now);
      thumpOsc.stop(now + 0.24);

      // Let the browser GC these once they finish; no need to track refs.
      noiseSrc.onended = () => {
        try {
          noiseSrc.disconnect();
          noiseFilter.disconnect();
          noiseGain.disconnect();
        } catch (err) {
          /* ignore */
        }
      };
      thumpOsc.onended = () => {
        try {
          thumpOsc.disconnect();
          thumpGain.disconnect();
        } catch (err) {
          /* ignore */
        }
      };
    } catch (err) {
      // Never let a failed one-shot break gameplay.
    }
  }

  playNitro() {
    if (!this._ctx) return;
    const ctx = this._ctx;
    const now = ctx.currentTime;
    try {
      const osc = ctx.createOscillator();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(80, now);
      osc.frequency.exponentialRampToValueAtTime(400, now + 0.25);

      const filter = ctx.createBiquadFilter();
      filter.type = 'highpass';
      filter.frequency.value = 200;

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.linearRampToValueAtTime(0.22, now + 0.04);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.32);

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(this._master);
      osc.start(now);
      osc.stop(now + 0.35);
      osc.onended = () => { try { osc.disconnect(); filter.disconnect(); gain.disconnect(); } catch(e){} };
    } catch (e) { /* ignore */ }
  }

  // Short, subtle UI click/notification blip for mission complete /
  // wanted-level-change events.
  playUiBlip() {
    if (!this._ctx) return;
    const ctx = this._ctx;
    const now = ctx.currentTime;

    try {
      const osc = ctx.createOscillator();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(880, now);
      osc.frequency.exponentialRampToValueAtTime(1320, now + 0.08);

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.linearRampToValueAtTime(0.18, now + 0.012);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.14);

      osc.connect(gain);
      gain.connect(this._master);

      osc.start(now);
      osc.stop(now + 0.16);
      osc.onended = () => {
        try {
          osc.disconnect();
          gain.disconnect();
        } catch (err) {
          /* ignore */
        }
      };
    } catch (err) {
      // Never let a failed one-shot break gameplay.
    }
  }

  // --- Teardown -----------------------------------------------------------

  // Cleanly stops everything and closes the AudioContext. Safe to call
  // multiple times.
  dispose() {
    if (this._disposed) return;
    this._disposed = true;

    for (const evt of this._gestureEvents) {
      try {
        window.removeEventListener(evt, this._onFirstGesture);
      } catch (err) {
        /* ignore */
      }
    }

    if (this._siren && this._siren.lfoId != null) {
      clearInterval(this._siren.lfoId);
      this._siren.lfoId = null;
    }

    const stopNode = (node) => {
      if (!node) return;
      try {
        node.stop();
      } catch (err) {
        /* already stopped or never started */
      }
      try {
        node.disconnect();
      } catch (err) {
        /* ignore */
      }
    };

    if (this._engine) {
      stopNode(this._engine.osc);
      stopNode(this._engine.subOsc);
    }
    if (this._siren) {
      stopNode(this._siren.osc);
    }

    if (this._ctx) {
      try {
        const ctx = this._ctx;
        const closeResult = ctx.close();
        if (closeResult && typeof closeResult.catch === 'function') {
          closeResult.catch(() => {
            /* ignore — context may already be closed */
          });
        }
      } catch (err) {
        /* ignore */
      }
    }

    this._ctx = null;
    this._engine = null;
    this._siren = null;
    this._master = null;
  }
}

function clamp01(v) {
  if (typeof v !== 'number' || Number.isNaN(v)) return 0;
  return Math.max(0, Math.min(1, v));
}
