// Configuration centrale du module Prospection.
// Toute l'identité de l'agence est pilotée par variables d'environnement :
// les valeurs annoncées aux prospects (années d'expérience, réalisations…)
// doivent rester exactes et vérifiables (art. L121-2 Code de la consommation).

function int(value: string | undefined, fallback: number): number {
  const n = Number(value);
  return Number.isFinite(n) && n > 0 ? Math.floor(n) : fallback;
}

export const agency = {
  name: process.env.AGENCY_NAME ?? "CompeteIQ Studio",
  senderName: process.env.AGENCY_SENDER_NAME ?? "L'équipe CompeteIQ Studio",
  yearsExperience: int(process.env.AGENCY_YEARS_EXPERIENCE, 10),
  email: process.env.AGENCY_EMAIL ?? "contact@competeiq.io",
  phone: process.env.AGENCY_PHONE ?? "",
  website: process.env.AGENCY_WEBSITE ?? "competeiq.io",
  city: process.env.AGENCY_CITY ?? "Paris",
  siret: process.env.AGENCY_SIRET ?? "",
  // Offre mise en avant dans les emails
  offer: {
    startingPrice: int(process.env.AGENCY_STARTING_PRICE, 490),
    deliveryDays: int(process.env.AGENCY_DELIVERY_DAYS, 15),
  },
};

export const outreach = {
  // Sécurité : par défaut on n'envoie RIEN réellement (dry-run).
  // Passer OUTREACH_DRY_RUN=false explicitement pour activer l'envoi SMTP.
  dryRun: process.env.OUTREACH_DRY_RUN !== "false",
  dailySendLimit: int(process.env.OUTREACH_DAILY_LIMIT, 50),
  // Jours d'attente avant chaque étape de la séquence (étape 1 = J0)
  stepDelaysDays: [0, 4, 10, 18] as const,
  minScoreToContact: int(process.env.OUTREACH_MIN_SCORE, 30),
  publicBaseUrl: process.env.PUBLIC_BASE_URL ?? "http://localhost:3000",
  googlePlacesApiKey: process.env.GOOGLE_PLACES_API_KEY ?? "",
  smtp: {
    host: process.env.SMTP_HOST ?? "",
    port: int(process.env.SMTP_PORT, 587),
    user: process.env.SMTP_USER ?? "",
    pass: process.env.SMTP_PASS ?? "",
    from:
      process.env.SMTP_FROM ??
      `${process.env.AGENCY_NAME ?? "CompeteIQ Studio"} <${process.env.AGENCY_EMAIL ?? "contact@competeiq.io"}>`,
  },
};

export type AgencyConfig = typeof agency;
export type OutreachConfig = typeof outreach;
