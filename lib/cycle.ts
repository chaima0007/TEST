import type { CycleSettings } from "./types";

// Calcul de phase du cycle — information de bien-être, PAS un avis médical
// ni une méthode de contraception. Les repères sont volontairement généraux.

export type CyclePhase = "menstruelle" | "folliculaire" | "ovulatoire" | "luteale";

export interface CycleInfo {
  dayOfCycle: number;
  phase: CyclePhase;
  label: string;
  emoji: string;
  summary: string;
  energy: string;
  // Comment le/la partenaire peut s'adapter en douceur.
  tips: string[];
}

const PHASE_CONTENT: Record<CyclePhase, Omit<CycleInfo, "dayOfCycle" | "phase">> = {
  menstruelle: {
    label: "Phase menstruelle",
    emoji: "🌑",
    summary: "Les règles. Énergie souvent basse, besoin de repos et de douceur.",
    energy: "Énergie basse",
    tips: [
      "Proposer du repos, une bouillotte, un plat réconfortant sans qu'on le demande.",
      "Alléger la charge mentale : prendre une tâche en plus, sans en faire un sujet.",
      "Éviter les décisions lourdes ou les débats à chaud si l'envie n'y est pas.",
    ],
  },
  folliculaire: {
    label: "Phase folliculaire",
    emoji: "🌒",
    summary: "Après les règles. L'énergie remonte, l'humeur s'ouvre.",
    energy: "Énergie qui remonte",
    tips: [
      "Bon moment pour lancer des projets, planifier une sortie, se motiver ensemble.",
      "L'envie d'échanger et d'essayer des choses est souvent plus grande.",
    ],
  },
  ovulatoire: {
    label: "Phase ovulatoire",
    emoji: "🌕",
    summary: "Milieu de cycle. Énergie et sociabilité souvent au plus haut.",
    energy: "Énergie haute",
    tips: [
      "Moment souvent propice à la connexion et à la proximité — rester à l'écoute du oui de l'autre.",
      "Idéal pour un vrai temps à deux, une conversation de fond, une soirée qui compte.",
    ],
  },
  luteale: {
    label: "Phase lutéale",
    emoji: "🌘",
    summary: "Avant les règles. Sensibilité parfois accrue (SPM possible), besoin de calme.",
    energy: "Énergie qui redescend",
    tips: [
      "Plus de patience et de réassurance : ne pas prendre l'irritabilité personnellement.",
      "Privilégier le calme, réduire la pression sociale, offrir des petites attentions.",
      "Vérifier avant de supposer : « De quoi tu aurais besoin, là ? »",
    ],
  },
};

function parseDate(iso: string): Date {
  const [y, m, d] = iso.split("-").map(Number);
  return new Date(y, (m || 1) - 1, d || 1);
}

const DAY_MS = 24 * 60 * 60 * 1000;

export function computeCycle(settings: CycleSettings, todayIso: string): CycleInfo | null {
  if (!settings.enabled || !settings.lastPeriodStart) return null;
  const len = Math.max(20, Math.min(45, settings.cycleLength || 28));
  const periodLen = Math.max(2, Math.min(10, settings.periodLength || 5));

  const start = parseDate(settings.lastPeriodStart).getTime();
  const today = parseDate(todayIso).getTime();
  const diffDays = Math.floor((today - start) / DAY_MS);
  if (diffDays < 0) return null;

  const dayOfCycle = ((diffDays % len) + len) % len + 1; // 1..len
  const ovulation = len - 14; // approximation classique

  let phase: CyclePhase;
  if (dayOfCycle <= periodLen) phase = "menstruelle";
  else if (dayOfCycle < ovulation - 1) phase = "folliculaire";
  else if (dayOfCycle <= ovulation + 1) phase = "ovulatoire";
  else phase = "luteale";

  return { dayOfCycle, phase, ...PHASE_CONTENT[phase] };
}
