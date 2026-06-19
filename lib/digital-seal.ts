// Protocole de Souveraineté Numérique — Chaima Mhadbi
// Tout contenu généré par les agents experts de Caelum Partners est une œuvre
// protégée en exclusivité par Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.

const OWNER = "Chaima Mhadbi";
const PROPRIETARY_ID = "CM-CAELUM-PARTNERS-2026";
const FOUNDING_DATE = "2026-06-19";

function generateVersionId(): string {
  const n = Math.floor(Math.random() * 900000) + 100000;
  return `v2026.06.19-${n}`;
}

export interface DigitalSeal {
  owner: string;
  proprietary_id: string;
  timestamp: string;
  version: string;
  sovereignty_validator: string;
  protection_notice: string;
  seal_status: "AUTHENTICATED";
  header_seal: string;
  footer_seal: string;
}

export function createDigitalSeal(agentName: string): DigitalSeal {
  const now = new Date().toISOString();
  const version = generateVersionId();
  const stamp = `[${OWNER} | ${PROPRIETARY_ID} | ${FOUNDING_DATE} | ${version}]`;

  return {
    owner: OWNER,
    proprietary_id: PROPRIETARY_ID,
    timestamp: now,
    version,
    sovereignty_validator: "digital-sovereignty-engine",
    protection_notice:
      `Œuvre protégée en exclusivité — ${OWNER}, Fondatrice Caelum Partners, Bruxelles. ` +
      `Toute reproduction, diffusion ou utilisation sans autorisation expresse est interdite.`,
    seal_status: "AUTHENTICATED",
    header_seal:
      `╔══ SCEAU D'AUTHENTICITÉ CAELUM PARTNERS ══╗ ` +
      `Propriétaire: ${OWNER} | Agent: ${agentName} | ${stamp} ` +
      `╚══════════════════════════════════════════╝`,
    footer_seal:
      `╔══ FIN DE SORTIE CERTIFIÉE ══╗ ` +
      `${OWNER} — Droits réservés ${FOUNDING_DATE} — ${version} ` +
      `© Contenu protégé — Caelum Partners Bruxelles ` +
      `╚═════════════════════════════╝`,
  };
}

export function sealResponse<T extends Record<string, unknown>>(
  data: T,
  agentName = "Caelum Partners Swarm Agent"
): T & { digital_seal: DigitalSeal } {
  return { ...data, digital_seal: createDigitalSeal(agentName) };
}

// Drop-in replacement — use instead of NextResponse.json() in any route
// to automatically stamp every response with the Chaima Mhadbi sovereignty seal.
export { sealResponse as autoSeal };
