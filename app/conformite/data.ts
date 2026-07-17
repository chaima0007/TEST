import fs from "node:fs";
import path from "node:path";

// Source : data/caelum/conformite_entreprises.json (base vérifiée, séparée de La Loi Avec Moi).
// Utilitaire serveur partagé par le hub /conformite et les pages SEO /conformite/[norme].

export type Source = { type?: string; url?: string; intitule?: string };
export type Norme = {
  id: string;
  norme: string;
  changement: string;
  concernes: string;
  sanction: string;
  echeance: string;
  reference_legale: string;
  solution_caelum?: string;
  sources?: Source[];
};

// Slugs lisibles et stables pour le SEO.
const SLUGS: Record<string, string> = {
  "EFACT-2026": "e-facturation",
  "NIS2-BE": "nis2",
  "CSRD-OMNIBUS": "csrd",
  "CSDDD-OMNIBUS": "csddd",
  RGPD: "rgpd",
  "LANCEURS-ALERTE": "lanceurs-alerte",
  "AI-ACT": "ai-act",
  EAA: "accessibilite-numerique",
  UBO: "registre-ubo",
  "DORA-2025": "dora-resilience-numerique",
  "PAYEQUITY-2026": "transparence-salariale",
  "DAC7-2024": "dac7-plateformes-numeriques",
  "PPWR-2026": "emballages-ppwr",
  "DELAIS-PAIEMENT": "delais-paiement-b2b",
  "CBAM-2026": "cbam-carbone",
  "EUDR": "eudr-deforestation",
  "AML-LBC": "anti-blanchiment",
};

export function loadNormes(): Norme[] {
  try {
    const p = path.join(process.cwd(), "data", "caelum", "conformite_entreprises.json");
    const d = JSON.parse(fs.readFileSync(p, "utf-8"));
    return Array.isArray(d.normes) ? d.normes : [];
  } catch {
    return [];
  }
}

export function slugFor(n: Norme): string {
  return SLUGS[n.id] ?? n.id.toLowerCase();
}

export function normeBySlug(slug: string): Norme | undefined {
  return loadNormes().find((n) => slugFor(n) === slug);
}
