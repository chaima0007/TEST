/**
 * CaelumSwarm™ — Intellectual Property Protection Layer
 * © 2024-2026 Caelum Partners SPRL — All rights reserved
 * Proprietary & confidential — unauthorized reproduction prohibited
 */

export const IP_NOTICE = {
  owner: "Caelum Partners SPRL",
  product: "CaelumSwarm™",
  year: "2024-2026",
  registration: "BE 0XXX.XXX.XXX",
  jurisdiction: "Bruxelles, Belgique — Droit belge & Règlement EU 2024/1760",
  contact: "legal@caelumpartners.eu",
} as const;

export const COPYRIGHT_HEADER = `© ${IP_NOTICE.year} ${IP_NOTICE.owner} — CaelumSwarm™ est une marque déposée. Tous droits réservés. Toute reproduction, diffusion ou exploitation sans autorisation écrite est interdite.`;

export const WATERMARK_TEXT = `CaelumSwarm™ © ${IP_NOTICE.year} ${IP_NOTICE.owner} — CONFIDENTIEL`;

export interface SealedPayload<T> {
  data: T;
  meta: {
    source: string;
    owner: string;
    copyright: string;
    generatedAt: string;
    confidentiality: "CONFIDENTIEL" | "USAGE INTERNE" | "PUBLIC";
    redistributionAllowed: boolean;
    watermark: string;
  };
}

export function wrapWithIPProtection<T>(
  data: T,
  source: string,
  confidentiality: SealedPayload<T>["meta"]["confidentiality"] = "CONFIDENTIEL"
): SealedPayload<T> {
  return {
    data,
    meta: {
      source,
      owner: IP_NOTICE.owner,
      copyright: COPYRIGHT_HEADER,
      generatedAt: new Date().toISOString(),
      confidentiality,
      redistributionAllowed: false,
      watermark: WATERMARK_TEXT,
    },
  };
}

export const SHARING_DISCLAIMER = `
Ce document est la propriété exclusive de ${IP_NOTICE.owner}.
Il contient des informations confidentielles et propriétaires de CaelumSwarm™.

INTERDICTIONS :
• Reproduction ou copie sans autorisation écrite
• Diffusion à des tiers non autorisés
• Utilisation à des fins commerciales sans licence
• Décompilation ou ingénierie inverse de la méthodologie

En cas de violation : contact immédiat à ${IP_NOTICE.contact}
Droit applicable : droit belge — Tribunal de commerce de Bruxelles
`.trim();

export const EXPORT_NOTICE = (format: string, recipient: string) =>
  `[EXPORT ${format.toUpperCase()}] Généré par CaelumSwarm™ — © ${IP_NOTICE.year} ${IP_NOTICE.owner} — Destinataire : ${recipient} — Usage strictement limité au destinataire désigné — ${new Date().toISOString()}`;
