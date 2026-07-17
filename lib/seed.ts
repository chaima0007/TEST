import type { AppState } from "./types";

export const STATE_VERSION = 1;

// Données de DÉMO 100 % fictives. Servent à rendre l'app immédiatement
// démontrable, même en solo. « Moi » est modifiable ; « Alex » illustre
// ce que verrait l'autre partenaire une fois qu'il rejoint.
export function seedState(todayIso: string): AppState {
  return {
    version: STATE_VERSION,
    people: {
      moi: { id: "moi", name: "Toi", emoji: "🫀" },
      partenaire: { id: "partenaire", name: "Alex", emoji: "🌙" },
    },
    checkins: {
      partenaire: {
        date: todayIso,
        mood: 3,
        energy: 2,
        availability: "orange",
        note: "Journée dense au boulot, un peu à plat ce soir.",
      },
    },
    needs: [],
    limits: [
      { id: "l1", person: "partenaire", area: "tendresse", item: "Câlins en public", level: "peut-etre", note: "OK si discret." },
      { id: "l2", person: "partenaire", area: "com", item: "Régler un conflit à chaud", level: "non", note: "J'ai besoin d'une pause d'abord." },
      { id: "l3", person: "partenaire", area: "temps", item: "Soirée seul·e / semaine", level: "oui", note: "Le mardi, pour décompresser." },
      { id: "l4", person: "partenaire", area: "social", item: "Publier des photos de nous", level: "peut-etre", note: "Me demander avant." },
      { id: "l5", person: "moi", area: "com", item: "Messages toute la journée", level: "oui" },
      { id: "l6", person: "moi", area: "sujets", item: "Parler d'argent", level: "peut-etre", note: "Plutôt au calme, pas le soir." },
    ],
    sensitivities: [
      { id: "s1", person: "partenaire", kind: "allergie", label: "Arachides", severity: "fort", note: "Éviter totalement — vérifier les étiquettes." },
      { id: "s2", person: "partenaire", kind: "intolerance", label: "Lactose", severity: "moyen" },
      { id: "s3", person: "partenaire", kind: "sensorielle", label: "Bruit fort / foule", severity: "moyen", note: "Se fatigue vite en soirée bruyante." },
      { id: "s4", person: "partenaire", kind: "sujet", label: "Blagues sur le poids", severity: "fort", note: "Sujet à ne pas toucher, même pour rire." },
      { id: "s5", person: "moi", kind: "intolerance", label: "Gluten", severity: "leger" },
    ],
    cycle: {
      enabled: true,
      person: "partenaire",
      lastPeriodStart: shiftDate(todayIso, -3),
      cycleLength: 28,
      periodLength: 5,
    },
  };
}

function shiftDate(iso: string, days: number): string {
  const [y, m, d] = iso.split("-").map(Number);
  const dt = new Date(y, (m || 1) - 1, d || 1);
  dt.setDate(dt.getDate() + days);
  const mm = String(dt.getMonth() + 1).padStart(2, "0");
  const dd = String(dt.getDate()).padStart(2, "0");
  return `${dt.getFullYear()}-${mm}-${dd}`;
}
