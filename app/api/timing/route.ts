import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Scoring logic mirroring Python ContactTimingOptimizer ─────────────────────

const ARTISAN_PROFILE: Record<number, number> = {
  6: 15, 7: 40, 8: 65, 9: 75, 10: 70, 11: 60,
  12: 30, 13: 20, 14: 50, 15: 60, 16: 55, 17: 45, 18: 25, 19: 15,
};

const MEDICAL_PROFILE: Record<number, number> = {
  7: 20, 8: 55, 9: 80, 10: 75, 11: 65,
  12: 25, 13: 15, 14: 60, 15: 70, 16: 65, 17: 40, 18: 20, 19: 10,
};

const RESTAURANT_PROFILE: Record<number, number> = {
  8: 30, 9: 50, 10: 65, 11: 45,
  12: 10, 13: 5, 14: 40, 15: 60, 16: 70, 17: 65, 18: 20, 19: 10,
};

const PME_PROFILE: Record<number, number> = {
  7: 20, 8: 55, 9: 85, 10: 90, 11: 80,
  12: 35, 13: 30, 14: 75, 15: 80, 16: 70, 17: 55, 18: 25, 19: 10,
};

const SECTOR_PROFILES: Record<string, Record<number, number>> = {
  artisan: ARTISAN_PROFILE, plombier: ARTISAN_PROFILE, électricien: ARTISAN_PROFILE,
  restaurant: RESTAURANT_PROFILE, hôtel: RESTAURANT_PROFILE, coiffeur: RESTAURANT_PROFILE,
  médecin: MEDICAL_PROFILE, dentiste: MEDICAL_PROFILE, médical: MEDICAL_PROFILE,
  comptable: PME_PROFILE, avocat: PME_PROFILE, notaire: PME_PROFILE,
  immobilier: PME_PROFILE, PME: PME_PROFILE,
};

const DAY_MULTIPLIERS: Record<number, number> = {
  0: 0.90, 1: 1.00, 2: 0.85, 3: 0.95, 4: 0.70, 5: 0.15, 6: 0.05,
};

const DAY_NAMES = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"];

const KNOWN_SECTORS = [
  "artisan", "restaurant", "médecin", "comptable", "avocat",
  "PME", "immobilier", "hôtel", "dentiste", "notaire",
];

function getProfile(sector: string): Record<number, number> {
  const s = sector.toLowerCase();
  for (const [key, profile] of Object.entries(SECTOR_PROFILES)) {
    if (s.includes(key)) return profile;
  }
  return PME_PROFILE;
}

function scoreSlot(sector: string, day: number, hour: number): number {
  const profile = getProfile(sector);
  const base = profile[hour] ?? 0;
  const dayMult = DAY_MULTIPLIERS[day] ?? 0.5;
  return Math.round(base * dayMult * 10) / 10;
}

function bestWindow(sector: string) {
  let bestScore = -1, bestDay = 1, bestHour = 10;
  for (let d = 0; d < 5; d++) {
    for (let h = 6; h < 20; h++) {
      const score = scoreSlot(sector, d, h);
      if (score > bestScore) { bestScore = score; bestDay = d; bestHour = h; }
    }
  }
  const confidence = bestScore >= 70 ? "high" : bestScore >= 40 ? "medium" : "low";
  return {
    sector, day_of_week: bestDay, day_name: DAY_NAMES[bestDay],
    hour_start: bestHour, hour_end: bestHour + 1,
    score: bestScore, confidence,
    rationale: rationale(sector, bestDay, bestHour, bestScore),
  };
}

function topWindows(sector: string, n: number) {
  const slots: [number, number, number][] = [];
  for (let d = 0; d < 5; d++) {
    for (let h = 6; h < 20; h++) {
      const s = scoreSlot(sector, d, h);
      if (s > 0) slots.push([s, d, h]);
    }
  }
  slots.sort((a, b) => b[0] - a[0]);
  return slots.slice(0, n).map(([score, day, hour]) => ({
    sector, day_of_week: day, day_name: DAY_NAMES[day],
    hour_start: hour, hour_end: hour + 1, score,
    confidence: score >= 70 ? "high" : score >= 40 ? "medium" : "low",
    rationale: rationale(sector, day, hour, score),
  }));
}

function weeklySchedule(sector: string) {
  return Object.fromEntries(
    DAY_NAMES.map((name, d) => [
      name,
      Object.fromEntries(
        Array.from({ length: 14 }, (_, i) => i + 6).map((h) => [h, scoreSlot(sector, d, h)])
      ),
    ])
  );
}

function rationale(sector: string, day: number, hour: number, score: number): string {
  const dayName = DAY_NAMES[day];
  const hourStr = `${hour}h–${hour + 1}h`;
  const s = sector.toLowerCase();
  if (["artisan", "plombier", "électricien"].some((k) => s.includes(k))) {
    if (hour >= 7 && hour <= 9) return `${dayName} ${hourStr} — avant démarrage chantier, taux d'ouverture +40%`;
    if (hour >= 14 && hour <= 16) return `${dayName} ${hourStr} — pause chantier après-midi`;
  }
  if (["restaurant", "hôtel", "coiffeur"].some((k) => s.includes(k))) {
    if (hour >= 14 && hour <= 17) return `${dayName} ${hourStr} — créneau entre services, disponibilité maximale`;
  }
  if (["médecin", "dentiste", "médical"].some((k) => s.includes(k))) {
    if (hour === 9 || hour === 15) return `${dayName} ${hourStr} — entre consultations, pic de réponse`;
  }
  if (hour === 10) return `${dayName} ${hourStr} — pic d'engagement matinal B2B`;
  if (hour === 15) return `${dayName} ${hourStr} — relance post-déjeuner, focus décisionnel`;
  return `${dayName} ${hourStr} — score d'engagement : ${score}/100`;
}

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const sector = searchParams.get("sector") ?? "all";

  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/timing/summary`, { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch { /* fall through */ }
  }

  if (sector !== "all") {
    return NextResponse.json({
      best: bestWindow(sector),
      top: topWindows(sector, 5),
      schedule: weeklySchedule(sector),
    });
  }

  return NextResponse.json({
    sectors: KNOWN_SECTORS.map((s) => ({
      ...bestWindow(s),
      top_windows: topWindows(s, 3),
    })),
    known_sectors: KNOWN_SECTORS,
  });
}
