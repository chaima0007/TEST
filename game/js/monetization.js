// MonetizationAgent — Achievements, daily challenges, social share, progression.
// Zero-backend: all state lives in localStorage.

const STORAGE = {
  ACHIEVEMENTS: 'moonbow_achievements',
  DAILY:        'moonbow_daily',
  UNLOCKS:      'moonbow_unlocks',
  PLAY_COUNT:   'moonbow_plays',
};

const ACHIEVEMENTS = [
  { id: 'first_drift',     label: 'PREMIER DRIFT',       reward: 50  },
  { id: 'speed_150',       label: 'VITESSE FOLLE',        reward: 100 },
  { id: 'drift_500',       label: 'ROI DU DRIFT',         reward: 200 },
  { id: 'wanted_3',        label: 'RECHERCHE NATIONALE',  reward: 150 },
  { id: 'wanted_5',        label: 'ENNEMI PUBLIC N°1',    reward: 500 },
  { id: 'score_1000',      label: 'PREMIERS PAS',         reward: 100 },
  { id: 'score_5000',      label: 'AMATEUR SÉRIEUX',      reward: 250 },
  { id: 'score_10000',     label: 'EXPERT URBAIN',        reward: 500 },
  { id: 'score_50000',     label: 'LÉGENDE DES RUES',     reward: 2000},
  { id: 'nitro_3',         label: 'ACCÉLÉRATION PURE',    reward: 100 },
  { id: 'detective_lose',  label: 'INTROUVABLE',          reward: 300 },
  { id: 'fantome_win',     label: 'FANTÔME VAINCU',       reward: 400 },
];

const DAILY_POOL = [
  { id: 'drift_daily',  label: 'ROI DU BITUME',  desc: 'Scorer 1 000 pts de drift',     target: 1000, type: 'drift'   },
  { id: 'speed_daily',  label: 'FULL GAZ',        desc: 'Tenir 130+ km/h pendant 5 s',   target: 5,    type: 'speed'   },
  { id: 'score_daily',  label: 'GROS SCORE',      desc: 'Atteindre $8 000 aujourd\'hui', target: 8000, type: 'score'   },
  { id: 'wanted_daily', label: 'FUGITIF',         desc: 'Survivre 30 s niveau 4+',       target: 30,   type: 'wanted'  },
];

const COLOR_UNLOCKS = [
  { score: 0,     color: 0x2255cc, name: 'Bleu Standard' },
  { score: 2000,  color: 0xff2244, name: 'Rouge Turbo'   },
  { score: 5000,  color: 0x00ff88, name: 'Vert Néon'     },
  { score: 10000, color: 0xffd700, name: 'Or Champion'   },
  { score: 25000, color: 0xff00ff, name: 'Rose Fantôme'  },
  { score: 50000, color: 0x00eeff, name: 'Cyan Nitro'    },
];

function dayKey() {
  const d = new Date();
  return `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;
}

export class MonetizationAgent {
  constructor(hud) {
    this._hud = hud;

    this._done   = JSON.parse(localStorage.getItem(STORAGE.ACHIEVEMENTS) || '{}');
    this._unlocks = JSON.parse(localStorage.getItem(STORAGE.UNLOCKS) || '{"maxScore":0}');
    this._plays  = parseInt(localStorage.getItem(STORAGE.PLAY_COUNT) || '0', 10) + 1;
    localStorage.setItem(STORAGE.PLAY_COUNT, String(this._plays));

    this._daily = this._loadDaily();

    // Per-session trackers
    this._driftPeak   = 0;
    this._nitroCount  = 0;
    this._detectEsc   = 0;
    this._highSpeedT  = 0;
    this._wantedHighT = 0;
    this._bonusPool   = 0;

    if (this._plays % 8 === 0) setTimeout(() => this._sharePrompt(), 4000);
  }

  _loadDaily() {
    const saved = JSON.parse(localStorage.getItem(STORAGE.DAILY) || '{}');
    if (saved.key === dayKey()) return saved;
    const c = DAILY_POOL[Math.floor(Math.random() * DAILY_POOL.length)];
    const d = { key: dayKey(), ...c, progress: 0, completed: false };
    localStorage.setItem(STORAGE.DAILY, JSON.stringify(d));
    return d;
  }

  _saveDaily() { localStorage.setItem(STORAGE.DAILY, JSON.stringify(this._daily)); }

  _unlock(id) {
    if (this._done[id]) return;
    this._done[id] = true;
    localStorage.setItem(STORAGE.ACHIEVEMENTS, JSON.stringify(this._done));
    const a = ACHIEVEMENTS.find(x => x.id === id);
    if (!a) return;
    this._bonusPool += a.reward;
    this._hud.showAchievement(a.label, a.reward);
  }

  // Returns bonus score to add this frame. Call once per frame.
  update(dt, vehicle, wantedLevel, driftSystem, nitroFired, detectiveEscaped, fantomeWon, totalScore) {
    const bonus = this._bonusPool;
    this._bonusPool = 0;

    const spd = vehicle ? Math.abs(vehicle.getSpeedKmh()) : 0;

    // Achievements
    if (driftSystem && driftSystem.isDrifting()) {
      this._unlock('first_drift');
      const ds = driftSystem.getSessionScore();
      if (ds > this._driftPeak) this._driftPeak = ds;
      if (this._driftPeak >= 500) this._unlock('drift_500');
    }
    if (spd >= 150) this._unlock('speed_150');
    if (wantedLevel >= 3) this._unlock('wanted_3');
    if (wantedLevel >= 5) this._unlock('wanted_5');
    if (totalScore >= 1000)  this._unlock('score_1000');
    if (totalScore >= 5000)  this._unlock('score_5000');
    if (totalScore >= 10000) this._unlock('score_10000');
    if (totalScore >= 50000) this._unlock('score_50000');

    if (nitroFired) {
      this._nitroCount++;
      if (this._nitroCount >= 3) this._unlock('nitro_3');
    }
    if (detectiveEscaped) {
      this._detectEsc++;
      if (this._detectEsc >= 3) this._unlock('detective_lose');
    }
    if (fantomeWon) this._unlock('fantome_win');

    // Daily challenge
    const d = this._daily;
    if (!d.completed) {
      let prog = d.progress;
      if (d.type === 'drift') prog = Math.max(prog, this._driftPeak);
      if (d.type === 'score') prog = Math.max(prog, totalScore);
      if (d.type === 'speed') {
        if (spd >= 130) this._highSpeedT += dt; else this._highSpeedT = 0;
        prog = Math.max(prog, this._highSpeedT);
      }
      if (d.type === 'wanted') {
        if (wantedLevel >= 4) this._wantedHighT += dt;
        prog = Math.max(prog, this._wantedHighT);
      }
      if (prog !== d.progress) { d.progress = prog; this._saveDaily(); }
      if (d.progress >= d.target) {
        d.completed = true;
        this._saveDaily();
        this._bonusPool += 1500;
        this._hud.showMessage('DÉFI QUOTIDIEN ACCOMPLI ! +$1 500 !', 4000);
      }
    }

    // Color unlock progression
    if (totalScore > (this._unlocks.maxScore || 0)) {
      const prev = this._unlocks.maxScore || 0;
      this._unlocks.maxScore = totalScore;
      for (const u of COLOR_UNLOCKS) {
        if (u.score > 0 && prev < u.score && totalScore >= u.score) {
          this._hud.showMessage(`COULEUR DÉBLOQUÉE : ${u.name} !`, 3500);
          this._unlocks['c_' + u.score] = true;
        }
      }
      localStorage.setItem(STORAGE.UNLOCKS, JSON.stringify(this._unlocks));
    }

    return bonus;
  }

  getDailyStatus() {
    const d = this._daily;
    if (d.completed) return { label: d.label, text: 'ACCOMPLI ✓', pct: 1 };
    const pct = Math.min(1, d.progress / d.target);
    return { label: d.label, text: d.desc, pct };
  }

  getAchievementCount() {
    return Object.keys(this._done).length;
  }

  _sharePrompt() {
    const score = localStorage.getItem('moonbow_highscore') || '0';
    const text = `J\'ai scoré $${score} sur Open City ! Peux-tu faire mieux ? 🚗💨`;
    this._hud.showSharePrompt(text, () => {
      if (navigator.share) {
        navigator.share({ title: 'Open City', text, url: window.location.href }).catch(() => {});
      } else {
        const enc = encodeURIComponent(`${text} ${window.location.href}`);
        window.open(`https://twitter.com/intent/tweet?text=${enc}`, '_blank');
      }
    });
  }
}
