import * as THREE from 'three';

// TrendRadarAgent — Ronde 21
// Agent espion qui surveille les tendances tech des jeux AAA 2024-2026
// et orchestre l'adoption dans NEXUS CITY.

const INTEL_DB = [
  { id: 'sky_gradient',    game: 'Horizon Forbidden West', pub: 'Guerrilla Games',    tech: 'Physical Sky Gradient',             year: 2022, agent: 'AtmosphereAgent', status: 'ACTIF' },
  { id: 'god_rays',        game: 'Red Dead Redemption 2',  pub: 'Rockstar Games',     tech: 'Volumetric God Rays',               year: 2018, agent: 'AtmosphereAgent', status: 'ACTIF' },
  { id: 'dynamic_stars',   game: 'Starfield',              pub: 'Bethesda',           tech: 'Dynamic Star Field + Moon',         year: 2023, agent: 'AtmosphereAgent', status: 'ACTIF' },
  { id: 'neon_bloom',      game: 'Cyberpunk 2077 2.1',     pub: 'CD Projekt RED',     tech: 'HDR Neon Halos + Bloom Ground',     year: 2024, agent: 'AtmosphereAgent', status: 'ACTIF' },
  { id: 'fog_sync',        game: 'GTA VI',                 pub: 'Rockstar Games',     tech: 'Dynamic Fog Color / Atmosphere',    year: 2025, agent: 'AtmosphereAgent', status: 'ACTIF' },
  { id: 'rain_particles',  game: 'Cyberpunk 2077',         pub: 'CD Projekt RED',     tech: 'Volumetric Rain Particles',         year: 2020, agent: 'WeatherFXAgent',  status: 'ACTIF' },
  { id: 'wet_roads',       game: 'GTA VI',                 pub: 'Rockstar Games',     tech: 'PBR Wet Road Reflections (Flaques)',year: 2025, agent: 'WeatherFXAgent',  status: 'ACTIF' },
  { id: 'lightning',       game: 'Red Dead Redemption 2',  pub: 'Rockstar Games',     tech: 'Dynamic Lightning Flash',           year: 2018, agent: 'WeatherFXAgent',  status: 'ACTIF' },
  { id: 'car_envmap',      game: 'Forza Horizon 5',        pub: 'Playground Games',   tech: 'Real-time Car Environment Map',     year: 2021, agent: 'CarShaderAgent',  status: 'ACTIF' },
  { id: 'car_dirt',        game: 'Gran Turismo 7',         pub: 'Polyphony Digital',  tech: 'Progressive Car Dirt Accumulation', year: 2022, agent: 'CarShaderAgent',  status: 'ACTIF' },
  { id: 'clearcoat',       game: 'Need for Speed Unbound', pub: 'Criterion Games',    tech: 'Multi-layer Clearcoat Paint Shimmer',year:2022, agent: 'CarShaderAgent',  status: 'ACTIF' },
  { id: 'pbr_body',        game: 'Forza Motorsport 2023',  pub: 'Turn 10',            tech: 'PBR Metalness/Roughness Car Body',   year: 2023, agent: 'CarShaderAgent',  status: 'ACTIF' },
  { id: 'procedural_city', game: 'Cities Skylines 2',      pub: 'Paradox Interactive',tech: 'Procedural Density City',           year: 2023, agent: 'NEXUS World',     status: 'ACTIF' },
  { id: 'ai_npc',          game: 'GTA VI',                 pub: 'Rockstar Games',     tech: 'Autonomous NPC Behaviors',          year: 2025, agent: 'FlashMob+Dialogue',status:'ACTIF' },
  { id: 'predictive_ai',   game: 'Alien Isolation',        pub: 'Creative Assembly',  tech: '2nd-order Predictive AI',           year: 2014, agent: 'PredictivePolice',status: 'ACTIF' },
  { id: 'emotion_engine',  game: 'Heavy Rain',             pub: 'Quantic Dream',      tech: 'Dynamic Emotion Engine',            year: 2010, agent: 'EmotionEngine',   status: 'ACTIF' },
  { id: 'bpm_sync',        game: 'Rez Infinite',           pub: 'Enhance Games',      tech: 'BPM-synced Ambient System',         year: 2016, agent: 'CityPulseAgent',  status: 'ACTIF' },
  { id: 'surreal_districts',game:'Cyberpunk 2077',         pub: 'CD Projekt RED',     tech: 'Distinct Thematic Districts',       year: 2020, agent: 'DistrictSystem',  status: 'ACTIF' },
];

// Messages d'alerte RADAR affichés périodiquement
const RADAR_ALERTS = [
  g => `[RADAR] ${g.game} — "${g.tech}" confirmé ACTIF`,
  g => `[RADAR] Technique "${g.tech}" — niveau compétition ${g.year}`,
  g => `[RADAR] Agent ${g.agent} intègre tech de ${g.pub}`,
  g => `[INTEL] ${g.game} → ${g.tech} — NEXUS CITY à niveau AAA`,
];

export class TrendRadarAgent {
  constructor() {
    this._db           = INTEL_DB;
    this._scanTimer    = 0;
    this._scanInterval = 38;
    this._lastScan     = null;
    this._notifQueue   = [];
    this._alertIdx     = 0;
  }

  scan() {
    this._lastScan = {
      total:    this._db.length,
      active:   this._db.filter(i => i.status === 'ACTIF').length,
      items:    this._db,
      scannedAt: Date.now(),
    };
    return this._lastScan;
  }

  update(dt) {
    this._scanTimer += dt;
    if (this._scanTimer >= this._scanInterval) {
      this._scanTimer = 0;
      this.scan();
      const item = this._db[Math.floor(Math.random() * this._db.length)];
      const tpl  = RADAR_ALERTS[this._alertIdx % RADAR_ALERTS.length];
      this._alertIdx++;
      this._notifQueue.push(tpl(item));
    }
  }

  popNotif() {
    return this._notifQueue.shift() || null;
  }

  getReport()       { return this._lastScan || this.scan(); }
  getActiveCount()  { return this._db.filter(i => i.status === 'ACTIF').length; }
  getTotalCount()   { return this._db.length; }
  getCooldown()     { return Math.max(0, this._scanInterval - this._scanTimer); }

  getStatusLine() {
    const r = this.getReport();
    return `${r.active}/${r.total} techs AAA intégrées | Prochain scan ${Math.round(this.getCooldown())}s`;
  }
}
