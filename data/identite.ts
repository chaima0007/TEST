// Identité légale de l'éditeur — Caelum (projet ENTREPRISES, séparé de La Loi Avec Moi).
// ⚠️ À COMPLÉTER PAR CHAIMA avant la mise en ligne (obligation légale des mentions légales).
// Les pages légales lisent ce fichier : il suffit de modifier ICI, une seule fois.
// Tant qu'un champ vaut "[à compléter]", les pages affichent un avertissement (rien d'inventé).

export const IDENTITE_CAELUM = {
  denomination: "[à compléter]",        // ex. "Chaima Mhadbi" ou la société Caelum
  forme_juridique: "[à compléter]",     // ex. "personne physique", "SRL"
  adresse: "[à compléter]",             // siège
  bce: "[à compléter]",                 // n° d'entreprise (BCE)
  tva: "[à compléter]",                 // n° de TVA
  email: "chaima.caelumpartners@gmail.com", // e-mail PROPRE à Caelum (jamais celui de La Loi Avec Moi)
  responsable_publication: "[à compléter]",
  hebergeur: "Vercel Inc., 340 S Lemon Ave #4133, Walnut, CA 91789, USA — vercel.com",
};

export function identiteCaelumIncomplete(): boolean {
  return Object.values(IDENTITE_CAELUM).some((v) => v.includes("[à compléter]"));
}
