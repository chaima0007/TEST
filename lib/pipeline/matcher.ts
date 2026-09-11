// ─── Étape 3 — Matching (logique pure, sans DB) ──────────────────────────────
//
// Calcule un score de compatibilité [0..1] entre une offre qualifiée et un
// profil freelance. Fonction pure → entièrement testable (cf. __tests__).

export interface MatchCandidateJob {
  skills: string[];
  budget: number | null;
  location: string | null;
}

export interface MatchCandidateProfile {
  skills: string[]; // déjà canonisées (mêmes libellés que l'analyzer)
  minBudget: number;
  locations: string[]; // ex: ["remote", "Paris"]
}

export interface MatchResult {
  confidence: number;
  /** Détail pondéré, utile pour expliquer la décision dans l'UI. */
  breakdown: { skills: number; budget: number; location: number };
}

const norm = (s: string) => s.trim().toLowerCase();

/**
 * Score = 60% recouvrement de compétences + 25% adéquation budget + 15% lieu.
 * Le recouvrement de compétences est exigé : sans aucune compétence commune,
 * la confiance est forcée à 0 (pas de faux positif).
 */
export function scoreMatch(
  job: MatchCandidateJob,
  profile: MatchCandidateProfile,
): MatchResult {
  const jobSkills = new Set(job.skills.map(norm));
  const profSkills = new Set(profile.skills.map(norm));

  const overlap = [...jobSkills].filter((s) => profSkills.has(s)).length;
  const skillScore = jobSkills.size === 0 ? 0 : overlap / jobSkills.size;

  // Budget : 1 si l'offre atteint/dépasse le minimum du freelance, dégradé sinon.
  let budgetScore = 0.5; // budget inconnu → neutre
  if (job.budget !== null) {
    if (profile.minBudget <= 0) budgetScore = 1;
    else budgetScore = Math.max(0, Math.min(1, job.budget / profile.minBudget));
  }

  const locs = new Set(profile.locations.map(norm));
  let locationScore = 0.5; // lieu inconnu → neutre
  if (job.location) {
    locationScore = locs.has(norm(job.location)) || locs.has("remote") ? 1 : 0;
  }

  const confidence =
    overlap === 0
      ? 0
      : 0.6 * skillScore + 0.25 * budgetScore + 0.15 * locationScore;

  return {
    confidence: Math.round(confidence * 100) / 100,
    breakdown: {
      skills: Math.round(skillScore * 100) / 100,
      budget: Math.round(budgetScore * 100) / 100,
      location: Math.round(locationScore * 100) / 100,
    },
  };
}

/** Génère l'explication "pourquoi ça matche" affichée à l'utilisateur. */
export function buildSnippet(
  jobTitle: string,
  result: MatchResult,
  commonSkills: string[],
): string {
  const pct = Math.round(result.confidence * 100);
  const skills = commonSkills.length ? commonSkills.join(", ") : "profil compatible";
  return `Compatibilité ${pct}% sur « ${jobTitle} » — compétences en commun : ${skills}.`;
}
