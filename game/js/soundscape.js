// SoundscapeAgent — Ronde 24 — IMMERSION TOTALE
// Sons procéduraux ambiants pour chaque contexte onirique/horreur.
// Backroom : bourdonnement fluorescent 60 Hz + vacillement.
// Monstre   : grondement LFO grave modulé par type.
// DreamZone : tonalités cristallines avec delay feedback.
// Peur      : battements cardiaques synthétiques (BPM 55→130).

export class SoundscapeAgent {
  constructor(audioCtx) {
    this._ctx = audioCtx;
    if (!this._ctx) return;

    this._master = this._ctx.createGain();
    this._master.gain.value = 0.60;
    this._master.connect(this._ctx.destination);

    this._buildBackroom();
    this._buildMonster();
    this._buildDream();

    this._heartTimer   = 0;
    this._heartBPM     = 60;
    this._heartGain    = this._ctx.createGain();
    this._heartGain.gain.value = 0;
    this._heartGain.connect(this._master);

    this._t = 0;
  }

  _buildBackroom() {
    const ctx = this._ctx;

    const osc1 = ctx.createOscillator();
    osc1.type = 'sawtooth';
    osc1.frequency.value = 60;

    const osc2 = ctx.createOscillator();
    osc2.type = 'sine';
    osc2.frequency.value = 180;

    // Bruit blanc tamisé (texture néon crépitant)
    const bufLen = ctx.sampleRate * 2;
    const buf = ctx.createBuffer(1, bufLen, ctx.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < bufLen; i++) data[i] = (Math.random() * 2 - 1) * 0.10;
    const noise = ctx.createBufferSource();
    noise.buffer = buf;
    noise.loop = true;

    const noiseFilt = ctx.createBiquadFilter();
    noiseFilt.type = 'bandpass';
    noiseFilt.frequency.value = 3800;
    noiseFilt.Q.value = 1.2;

    const comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -20;
    comp.ratio.value = 5;

    this._backroomGain = ctx.createGain();
    this._backroomGain.gain.value = 0;

    osc1.connect(this._backroomGain);
    osc2.connect(this._backroomGain);
    noise.connect(noiseFilt);
    noiseFilt.connect(this._backroomGain);
    this._backroomGain.connect(comp);
    comp.connect(this._master);

    osc1.start(); osc2.start(); noise.start();
    this._backroomOsc = osc1;
  }

  _buildMonster() {
    const ctx = this._ctx;

    const osc = ctx.createOscillator();
    osc.type = 'sawtooth';
    osc.frequency.value = 55;

    const lfo = ctx.createOscillator();
    lfo.type = 'sine';
    lfo.frequency.value = 0.8;
    const lfoGain = ctx.createGain();
    lfoGain.gain.value = 18;
    lfo.connect(lfoGain);
    lfoGain.connect(osc.frequency);

    this._monsterFilter = ctx.createBiquadFilter();
    this._monsterFilter.type = 'lowpass';
    this._monsterFilter.frequency.value = 280;
    this._monsterFilter.Q.value = 2.5;

    this._monsterGain = ctx.createGain();
    this._monsterGain.gain.value = 0;

    osc.connect(this._monsterFilter);
    this._monsterFilter.connect(this._monsterGain);
    this._monsterGain.connect(this._master);

    osc.start(); lfo.start();
    this._monsterOsc = osc;
    this._monsterLFO = lfo;
  }

  _buildDream() {
    const ctx = this._ctx;

    // Delay feedback pour reverb artisanal
    const delay = ctx.createDelay(1.0);
    delay.delayTime.value = 0.28;
    const feedGain = ctx.createGain();
    feedGain.gain.value = 0.42;
    delay.connect(feedGain);
    feedGain.connect(delay);

    const wet = ctx.createGain();
    wet.gain.value = 0.55;
    delay.connect(wet);

    this._dreamGain = ctx.createGain();
    this._dreamGain.gain.value = 0;

    // 3 sinusoïdes harmoniques cristallines (528 Hz base)
    this._dreamOscs = [528, 792, 1056].map(f => {
      const o = ctx.createOscillator();
      o.type = 'sine';
      o.frequency.value = f;
      const g = ctx.createGain();
      g.gain.value = 0.16;
      o.connect(g);
      g.connect(delay);
      g.connect(this._dreamGain);
      o.start();
      return { osc: o, baseFreq: f };
    });

    wet.connect(this._dreamGain);
    this._dreamGain.connect(this._master);
  }

  _triggerHeartbeat() {
    if (!this._ctx) return;
    const ctx = this._ctx;
    const now = ctx.currentTime;

    // Kick synthétique — descente rapide 180 → 28 Hz
    const osc = ctx.createOscillator();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(175, now);
    osc.frequency.exponentialRampToValueAtTime(28, now + 0.20);

    const env = ctx.createGain();
    env.gain.setValueAtTime(0, now);
    env.gain.linearRampToValueAtTime(0.9, now + 0.012);
    env.gain.exponentialRampToValueAtTime(0.001, now + 0.26);

    osc.connect(env);
    env.connect(this._heartGain);
    osc.start(now);
    osc.stop(now + 0.28);

    // Second thump (écho cardiaque)
    const osc2 = ctx.createOscillator();
    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(110, now + 0.09);
    osc2.frequency.exponentialRampToValueAtTime(22, now + 0.28);

    const env2 = ctx.createGain();
    env2.gain.setValueAtTime(0, now + 0.09);
    env2.gain.linearRampToValueAtTime(0.38, now + 0.10);
    env2.gain.exponentialRampToValueAtTime(0.001, now + 0.32);

    osc2.connect(env2);
    env2.connect(this._heartGain);
    osc2.start(now + 0.09);
    osc2.stop(now + 0.34);
  }

  update(dt, backroomActive, fearLevel, monsterType, dreamActive) {
    if (!this._ctx) return;
    // Resume contexte si suspendu (gestion autoplay browsers)
    if (this._ctx.state === 'suspended') this._ctx.resume();

    this._t += dt;
    const now = this._ctx.currentTime;

    // ── Bourdonnement Backroom ──────────────────────────
    const backTarget = backroomActive ? 0.50 : 0;
    this._backroomGain.gain.setTargetAtTime(backTarget, now, 0.6);

    // Vacillement aléatoire du néon
    if (backroomActive && Math.random() < 0.006) {
      const cur = backTarget;
      this._backroomGain.gain.setValueAtTime(cur * 0.15, now);
      this._backroomGain.gain.linearRampToValueAtTime(cur, now + 0.03 + Math.random() * 0.07);
    }

    // ── Battements cardiaques ───────────────────────────
    const heartTarget = (backroomActive || fearLevel > 0.18) ? Math.min(1, fearLevel + 0.28) : 0;
    this._heartGain.gain.setTargetAtTime(heartTarget, now, 0.5);

    if (heartTarget > 0.05) {
      this._heartBPM = 55 + fearLevel * 80;
      const interval = 60 / this._heartBPM;
      this._heartTimer += dt;
      if (this._heartTimer >= interval) {
        this._heartTimer -= interval;
        this._triggerHeartbeat();
      }
    }

    // ── Grondement monstre ──────────────────────────────
    const monTarget = (monsterType && monsterType !== '—') ? fearLevel * 0.65 : 0;
    this._monsterGain.gain.setTargetAtTime(monTarget, now, 0.7);

    if (monsterType === 'BÊTE') {
      this._monsterFilter.frequency.value = 160 + Math.sin(this._t * 1.1) * 55;
      this._monsterOsc.frequency.value    = 36  + Math.sin(this._t * 0.38) * 10;
      this._monsterLFO.frequency.value    = 0.55;
    } else if (monsterType === 'CYCLOPE') {
      this._monsterFilter.frequency.value = 820 + Math.sin(this._t * 2.4) * 180;
      this._monsterOsc.frequency.value    = 85  + Math.sin(this._t * 0.28) * 18;
      this._monsterLFO.frequency.value    = 1.6;
    } else {
      // Ombre — chuchotement médium
      this._monsterFilter.frequency.value = 240 + Math.sin(this._t * 0.75) * 70;
      this._monsterOsc.frequency.value    = 52  + Math.sin(this._t * 0.48) * 12;
      this._monsterLFO.frequency.value    = 0.9;
    }

    // ── Tonalités zone magique ──────────────────────────
    const dreamTarget = dreamActive ? 0.40 : 0;
    this._dreamGain.gain.setTargetAtTime(dreamTarget, now, 1.0);

    if (dreamActive) {
      for (const { osc, baseFreq } of this._dreamOscs) {
        osc.frequency.setValueAtTime(baseFreq + Math.sin(this._t * 0.28) * 3, now);
      }
    }
  }

  isReady() { return !!this._ctx; }
}
