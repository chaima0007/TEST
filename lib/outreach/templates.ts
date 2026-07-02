// Séquence d'emails de prospection (4 étapes) — texte brut, français, vouvoiement.
// Toutes les valeurs chiffrées proviennent de la config : rien d'invérifiable.

import type { EmailDraft } from "./types";
import { agency, outreach } from "./config";

export const STEP_LABELS: Record<1 | 2 | 3 | 4, string> = {
  1: "Premier contact",
  2: "Relance",
  3: "Apport de valeur",
  4: "Dernier message",
};

interface ProspectInfo {
  name: string;
  category: string;
  city: string;
  optOutToken: string;
}

// Personnalisation métier : accroche (étape 1), bénéfice reformulé (étape 2),
// sujet des photos conseillées (étape 3).
interface CategoryProfile {
  keywords: string[];
  hook: string;
  benefit: string;
  photoSubject: string;
}

const CATEGORY_PROFILES: CategoryProfile[] = [
  {
    keywords: ["plombier", "électricien", "electricien", "chauffagiste", "artisan"],
    hook: "Sans site, les appels d'urgence et les demandes de devis partent vers les confrères visibles en ligne.",
    benefit:
      "un site simple qui rassure et transforme les recherches Google en appels et en demandes de devis",
    photoSubject: "vos réalisations et chantiers",
  },
  {
    keywords: ["restaurant", "pizzeria", "traiteur"],
    hook: "Sans site, impossible pour eux de consulter votre menu ou de réserver une table depuis leur téléphone.",
    benefit:
      "un site avec votre menu à jour et la réservation en ligne, consultable depuis n'importe quel téléphone",
    photoSubject: "vos plats et de votre salle",
  },
  {
    keywords: ["coiffeur", "institut", "barbier"],
    hook: "Sans site, pas de prise de rendez-vous en ligne : les clients réservent chez ceux qui la proposent.",
    benefit:
      "un site avec la prise de rendez-vous en ligne, pour remplir votre agenda même en dehors des heures d'ouverture",
    photoSubject: "votre salon et de vos réalisations",
  },
  {
    keywords: ["garage", "auto"],
    hook: "Sans site, les demandes de devis filent vers les garages visibles en ligne.",
    benefit:
      "un site qui vous apporte des demandes de devis directement, sans effort de votre part",
    photoSubject: "votre atelier",
  },
  {
    keywords: ["boulangerie", "commerce"],
    hook: "Sans site, vos clients ne trouvent ni vos horaires ni la possibilité de commander en click & collect.",
    benefit:
      "un site qui affiche vos horaires et vous permet de proposer le click & collect",
    photoSubject: "vos produits et de votre boutique",
  },
];

const DEFAULT_PROFILE: CategoryProfile = {
  keywords: [],
  hook: "Sans site, ces clients potentiels choisissent tout simplement un établissement plus visible.",
  benefit:
    "un site sobre et professionnel qui vous rend visible auprès des clients qui vous cherchent déjà",
  photoSubject: "votre activité au quotidien",
};

function profileFor(category: string): CategoryProfile {
  const c = category.toLowerCase();
  return (
    CATEGORY_PROFILES.find((p) => p.keywords.some((k) => c.includes(k))) ??
    DEFAULT_PROFILE
  );
}

function signature(): string {
  const lines = [agency.senderName, agency.name];
  if (agency.phone) lines.push(agency.phone);
  lines.push(agency.email, agency.website);
  return lines.join("\n");
}

// Pied de page légal obligatoire (opposition en un clic + mentions).
function legalFooter(optOutToken: string): string {
  return `—\nVous recevez cet email car votre établissement figure dans les annuaires professionnels publics et ne dispose pas de site internet référencé. Vous pouvez vous opposer à tout futur message en un clic : ${outreach.publicBaseUrl}/api/outreach/unsubscribe?token=${optOutToken}\n${agency.name}${agency.siret ? " — SIRET " + agency.siret : ""} — ${agency.city}`;
}

function assemble(paragraphs: string[], optOutToken: string): string {
  return [...paragraphs, signature(), legalFooter(optOutToken)].join("\n\n");
}

export function buildEmail(step: 1 | 2 | 3 | 4, prospect: ProspectInfo): EmailDraft {
  const { name, city, optOutToken } = prospect;
  const profile = profileFor(prospect.category);
  const { startingPrice, deliveryDays } = agency.offer;

  switch (step) {
    case 1:
      return {
        step,
        subject: `Un site internet pour ${name} ?`,
        body: assemble(
          [
            "Bonjour,",
            `Nous avons remarqué que ${name}, à ${city}, ne dispose pas encore de site internet. Or aujourd'hui, la majorité de vos clients cherchent d'abord sur Google avant de pousser une porte. ${profile.hook}`,
            `Nous sommes ${agency.name}, avec plus de ${agency.yearsExperience} ans d'expérience dans la création de sites pour les artisans et commerçants. Notre offre est simple : un site professionnel à partir de ${startingPrice} €, livré en ${deliveryDays} jours, pensé pour votre métier.`,
            "Est-ce que 15 minutes au téléphone vous conviendraient pour en parler ? Une simple réponse à cet email suffit aussi, nous nous adaptons à vos disponibilités.",
            "Bonne journée,",
          ],
          optOutToken
        ),
      };

    case 2:
      return {
        step,
        subject: `Notre proposition pour ${name}`,
        body: assemble(
          [
            "Bonjour,",
            `Nous nous permettons de revenir vers vous suite à notre message de la semaine dernière, au sujet d'un site internet pour ${name}. ${profile.hook}`,
            `En deux mots, nous vous proposons ${profile.benefit}. À partir de ${startingPrice} €, livré en ${deliveryDays} jours.`,
            `Si le moment est mal choisi, dites-le-nous simplement. Sinon, un court appel de 15 minutes suffit pour voir ensemble ce qui conviendrait à votre établissement à ${city}.`,
            "Bonne journée,",
          ],
          optOutToken
        ),
      };

    case 3:
      return {
        step,
        subject: `3 conseils gratuits pour ${name}`,
        body: assemble(
          [
            "Bonjour,",
            `Site internet ou non, voici trois actions gratuites qui aident déjà un établissement comme le vôtre à gagner des clients à ${city} :`,
            `1. Complétez votre fiche Google (horaires, téléphone, adresse) : c'est souvent la première chose que voient les gens qui vous cherchent.\n2. Demandez un avis Google à vos clients satisfaits : quelques avis récents font une vraie différence face aux établissements voisins.\n3. Ajoutez des photos récentes de ${profile.photoSubject} : une fiche vivante inspire confiance.`,
            `Et si vous souhaitez aller plus loin, notre offre reste valable : un site professionnel à partir de ${startingPrice} €, livré en ${deliveryDays} jours. Une simple réponse à cet email et nous en parlons.`,
            "Bonne journée,",
          ],
          optOutToken
        ),
      };

    case 4:
      return {
        step,
        subject: `Dernier message pour ${name}`,
        body: assemble(
          [
            "Bonjour,",
            "Sans réponse de votre part, nous n'insisterons pas davantage : nous clôturons votre dossier et vous ne recevrez plus de message de notre part.",
            `Sachez simplement que la porte reste ouverte. Si un jour vous souhaitez créer un site internet pour ${name}, écrivez-nous : un site professionnel à partir de ${startingPrice} €, livré en ${deliveryDays} jours, et nous serons ravis de vous aider.`,
            `Nous vous souhaitons une excellente continuation à ${city}.`,
            "Bien à vous,",
          ],
          optOutToken
        ),
      };
  }
}
