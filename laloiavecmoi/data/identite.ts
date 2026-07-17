// Identité légale de l'éditeur — La Loi Avec Moi.
// ⚠️ À COMPLÉTER PAR CHAIMA avant la mise en ligne (obligation légale des mentions légales).
// Remplacez chaque "[à compléter]" par les vraies données. Les pages légales lisent ce fichier :
// il suffit donc de modifier ICI, une seule fois.
//
// Tant qu'un champ vaut "[à compléter]", la page affiche un avertissement (rien n'est inventé).

export const IDENTITE_EDITEUR = {
  denomination: "[à compléter]",      // ex. "Chaima Mhadbi" ou la dénomination de la société
  forme_juridique: "[à compléter]",   // ex. "personne physique", "SRL", "ASBL"…
  adresse: "[à compléter]",           // adresse du siège
  bce: "[à compléter]",               // n° d'entreprise (BCE), ex. "0123.456.789"
  tva: "[à compléter]",               // n° de TVA si assujetti, sinon "non assujetti"
  email: "contact@laloiavecmoi.be",   // e-mail propre à La Loi Avec Moi (séparé de Caelum)
  hebergeur: "[à compléter]",         // nom + coordonnées de l'hébergeur (ex. Vercel Inc.)
};

export function identiteIncomplete(): boolean {
  return Object.values(IDENTITE_EDITEUR).some((v) => v.includes("[à compléter]"));
}
