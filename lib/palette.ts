// Palette de fils type DMC (sous-ensemble curé pour le MVP).
// code = référence DMC, name = nom courant, hex = couleur approchée.
// Les symboles sont attribués dynamiquement aux couleurs réellement utilisées.

export interface Thread {
  code: string;
  name: string;
  hex: string;
}

export const DMC_PALETTE: Thread[] = [
  { code: "B5200", name: "Blanc neige", hex: "#ffffff" },
  { code: "White", name: "Blanc", hex: "#fcfbf7" },
  { code: "3865", name: "Blanc cassé", hex: "#f6efe2" },
  { code: "712", name: "Crème", hex: "#f4ecd8" },
  { code: "739", name: "Beige clair", hex: "#eeddbd" },
  { code: "738", name: "Beige", hex: "#e3c598" },
  { code: "437", name: "Tan", hex: "#d2a874" },
  { code: "435", name: "Marron clair", hex: "#a76f43" },
  { code: "433", name: "Marron", hex: "#7a4a23" },
  { code: "898", name: "Marron foncé", hex: "#4d2c14" },
  { code: "938", name: "Brun café", hex: "#36210f" },
  { code: "310", name: "Noir", hex: "#000000" },
  { code: "413", name: "Gris anthracite", hex: "#565656" },
  { code: "318", name: "Gris", hex: "#9a9a9a" },
  { code: "762", name: "Gris perle", hex: "#d4d6d8" },
  { code: "666", name: "Rouge vif", hex: "#e21f26" },
  { code: "321", name: "Rouge", hex: "#c5202e" },
  { code: "815", name: "Rouge foncé", hex: "#8a1c2b" },
  { code: "351", name: "Corail", hex: "#e8897a" },
  { code: "353", name: "Pêche", hex: "#fdc5ac" },
  { code: "972", name: "Orange", hex: "#f6a300" },
  { code: "742", name: "Orange clair", hex: "#fdb94e" },
  { code: "744", name: "Jaune", hex: "#f7d97a" },
  { code: "307", name: "Jaune vif", hex: "#fbe54a" },
  { code: "907", name: "Vert pomme", hex: "#8bbf3c" },
  { code: "702", name: "Vert", hex: "#3aa84b" },
  { code: "699", name: "Vert sapin", hex: "#1f7a36" },
  { code: "890", name: "Vert foncé", hex: "#16472a" },
  { code: "964", name: "Vert d'eau", hex: "#9fd9cd" },
  { code: "3766", name: "Turquoise", hex: "#4fa7c0" },
  { code: "996", name: "Cyan", hex: "#1ec0e6" },
  { code: "996b", name: "Bleu ciel", hex: "#73c2e8" },
  { code: "799", name: "Bleu", hex: "#5a8fcf" },
  { code: "797", name: "Bleu roi", hex: "#26528f" },
  { code: "823", name: "Bleu nuit", hex: "#1a2a52" },
  { code: "208", name: "Violet", hex: "#8a5aab" },
  { code: "550", name: "Violet foncé", hex: "#5a1f6e" },
  { code: "3608", name: "Rose", hex: "#e89ac8" },
  { code: "603", name: "Rose vif", hex: "#f25fa0" },
  { code: "326", name: "Framboise", hex: "#b0344f" },
];

export const SYMBOLS =
  "■●▲◆★✚✖◼◻▣▤▥▦▧▨▩◐◑◒◓∎ΦΨΩ□△▽◇☆✦✧✩◈⬟⬢⬡✿❀❄✜⊕⊗⊞⊠";

export function hexToRgb(hex: string): [number, number, number] {
  const h = hex.replace("#", "");
  return [
    parseInt(h.slice(0, 2), 16),
    parseInt(h.slice(2, 4), 16),
    parseInt(h.slice(4, 6), 16),
  ];
}

const RGB_CACHE: [number, number, number][] = DMC_PALETTE.map((t) =>
  hexToRgb(t.hex),
);

// Distance perceptuelle pondérée (approx. luminance) — meilleur rendu que
// l'euclidien brut sur les tons chair / verts.
export function nearestThreadIndex(r: number, g: number, b: number): number {
  let best = 0;
  let bestD = Infinity;
  for (let i = 0; i < RGB_CACHE.length; i++) {
    const [pr, pg, pb] = RGB_CACHE[i];
    const dr = r - pr;
    const dg = g - pg;
    const db = b - pb;
    const d = 0.3 * dr * dr + 0.59 * dg * dg + 0.11 * db * db;
    if (d < bestD) {
      bestD = d;
      best = i;
    }
  }
  return best;
}
