export type CertStatus = "certifié" | "en cours" | "non certifié";

export interface Certification {
  code: string;
  label: string;
  issuer: string;
  scope: string;
  status: CertStatus;
  year?: number;
}

export interface EntityCertProfile {
  entityPrefix: string;
  certs: Certification[];
}

const CERT_TEMPLATES: Omit<Certification, "status" | "year">[] = [
  {
    code: "ISO-26000",
    label: "ISO 26000",
    issuer: "ISO",
    scope: "Responsabilité sociétale des organisations",
  },
  {
    code: "SA8000",
    label: "SA8000",
    issuer: "Social Accountability International",
    scope: "Conditions de travail & droits des travailleurs",
  },
  {
    code: "FAIR-TRADE",
    label: "Fair Trade Certified",
    issuer: "Fairtrade International",
    scope: "Commerce équitable & protection des producteurs",
  },
  {
    code: "CSDDD",
    label: "CSDDD 2024/1760",
    issuer: "Union Européenne",
    scope: "Devoir de vigilance chaîne de valeur",
  },
  {
    code: "ILO-C182",
    label: "Convention OIT C182",
    issuer: "Organisation Internationale du Travail",
    scope: "Pires formes de travail des enfants",
  },
];

function deriveStatus(score: number, index: number): CertStatus {
  const thresholds = [
    [70, 100],
    [55, 70],
    [40, 55],
    [60, 100],
    [50, 100],
  ];
  const [low] = thresholds[index] ?? [60, 100];
  if (score >= low + 20) return "certifié";
  if (score >= low) return "en cours";
  return "non certifié";
}

function deriveYear(score: number): number | undefined {
  if (score >= 80) return 2023;
  if (score >= 65) return 2024;
  return undefined;
}

export function buildCertProfile(entityId: string, compositeScore: number): EntityCertProfile {
  return {
    entityPrefix: entityId,
    certs: CERT_TEMPLATES.map((tmpl, i) => ({
      ...tmpl,
      status: deriveStatus(compositeScore, i),
      year: deriveStatus(compositeScore, i) === "certifié" ? deriveYear(compositeScore) : undefined,
    })),
  };
}

export const STATUS_COLOR: Record<CertStatus, string> = {
  "certifié": "#16a34a",
  "en cours": "#d97706",
  "non certifié": "#dc2626",
};

export const STATUS_ICON: Record<CertStatus, string> = {
  "certifié": "✓",
  "en cours": "⏳",
  "non certifié": "✗",
};
