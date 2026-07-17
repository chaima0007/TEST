// Inventaires de sentiments et de besoins issus de la Communication NonViolente
// (Rosenberg / CNVC). Listes volontairement courtes et courantes.

export const FEELINGS: string[] = [
  "triste",
  "seul·e",
  "blessé·e",
  "frustré·e",
  "inquiet·ète",
  "fatigué·e",
  "agacé·e",
  "déçu·e",
  "tendu·e",
  "débordé·e",
  "vulnérable",
  "en insécurité",
];

export const NEEDS: string[] = [
  "d'attention",
  "de repos",
  "d'être écouté·e",
  "de sécurité",
  "de tendresse",
  "de reconnaissance",
  "d'espace",
  "de soutien",
  "de clarté",
  "de me sentir prioritaire",
  "de partager",
  "de calme",
];

// Assemble un message en « je » selon le modèle OSBD.
export function assembleNvc(opts: {
  observation?: string;
  feeling?: string;
  need?: string;
  request?: string;
}): string {
  const { observation, feeling, need, request } = opts;
  const parts: string[] = [];
  if (observation?.trim()) {
    parts.push(`Quand ${observation.trim()}`);
  }
  if (feeling) {
    parts.push(`${parts.length ? ", " : ""}je me sens ${feeling}`);
  }
  if (need) {
    parts.push(` parce que j'ai besoin ${need}`);
  }
  let msg = parts.join("").trim();
  if (msg) msg += ".";
  if (request?.trim()) {
    msg += ` Est-ce que tu serais d'accord pour ${request.trim()} ?`;
  }
  return msg.trim();
}
