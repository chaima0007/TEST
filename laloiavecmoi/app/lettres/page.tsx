"use client";

import Link from "next/link";
import { useState } from "react";

// Générateur de lettre type sourcée — La Loi Avec Moi (outil citoyen gratuit).
// L'utilisateur remplit quelques champs → une lettre pré-rédigée, avec la base légale citée.
// Honnête : modèle indicatif, pas un conseil juridique ; chaque modèle renvoie à sa fiche sourcée.

type Champ = { key: string; label: string; placeholder?: string; aire?: boolean };
type Modele = {
  id: string;
  titre: string;
  intro: string;
  champs: Champ[];
  base_legale: string;
  fiche?: string;
  corps: (v: Record<string, string>) => string;
};

const exp = (v: Record<string, string>) =>
  `${v.nom || "[Votre nom]"}\n${v.adresse || "[Votre adresse]"}\n\n`;
const dest = (v: Record<string, string>) =>
  `À : ${v.destinataire || "[Nom du destinataire]"}\n${v.adresse_dest || "[Adresse du destinataire]"}\n\nLe ${v.date || "[date]"}\n\n`;

const MODELES: Modele[] = [
  {
    id: "garantie",
    titre: "Demande de restitution de la garantie locative",
    intro: "Pour réclamer votre garantie locative après la fin du bail.",
    base_legale: "Code civil — bail de résidence principale (libération de la garantie locative en fin de bail)",
    fiche: "bail_wallonie",
    champs: [
      { key: "nom", label: "Votre nom" },
      { key: "adresse", label: "Votre adresse" },
      { key: "destinataire", label: "Nom du bailleur" },
      { key: "adresse_dest", label: "Adresse du bailleur" },
      { key: "date", label: "Date" },
      { key: "adresse_bien", label: "Adresse du logement loué" },
      { key: "fin_bail", label: "Date de fin du bail" },
      { key: "iban", label: "Votre IBAN (pour le remboursement)" },
    ],
    corps: (v) =>
      exp(v) + dest(v) +
      `Objet : Restitution de la garantie locative\n\nMadame, Monsieur,\n\n` +
      `J'étais locataire du logement situé ${v.adresse_bien || "[adresse du bien]"}, dont le bail a pris fin le ${v.fin_bail || "[date]"}. ` +
      `Le logement a été rendu en bon état et les lieux ont été quittés.\n\n` +
      `Par la présente, je vous demande de libérer et de me restituer la garantie locative dans les meilleurs délais, ` +
      `sur le compte ${v.iban || "[votre IBAN]"}.\n\n` +
      `À défaut de réponse de votre part, je me réserve le droit de saisir la justice de paix compétente.\n\n` +
      `Je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées.\n\n${v.nom || "[Votre nom]"}`,
  },
  {
    id: "retractation",
    titre: "Rétractation d'un achat en ligne (14 jours)",
    intro: "Pour annuler un achat à distance dans le délai légal de 14 jours.",
    base_legale: "Code de droit économique — droit de rétractation (14 jours pour les achats à distance)",
    fiche: "consommation",
    champs: [
      { key: "nom", label: "Votre nom" },
      { key: "adresse", label: "Votre adresse" },
      { key: "destinataire", label: "Nom du vendeur" },
      { key: "adresse_dest", label: "Adresse / e-mail du vendeur" },
      { key: "date", label: "Date" },
      { key: "commande", label: "N° de commande" },
      { key: "produit", label: "Produit concerné" },
      { key: "date_reception", label: "Date de réception" },
    ],
    corps: (v) =>
      exp(v) + dest(v) +
      `Objet : Exercice du droit de rétractation\n\nMadame, Monsieur,\n\n` +
      `Je vous notifie par la présente ma rétractation du contrat portant sur la commande ${v.commande || "[n°]"} ` +
      `(${v.produit || "[produit]"}), reçue le ${v.date_reception || "[date]"}.\n\n` +
      `Conformément au droit de rétractation de 14 jours pour les achats à distance, je vous demande le remboursement ` +
      `de la totalité des sommes versées, dans un délai maximum de 14 jours.\n\n` +
      `Je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées.\n\n${v.nom || "[Votre nom]"}`,
  },
  {
    id: "prodeo",
    titre: "Demande d'aide juridique (pro deo)",
    intro: "Pour solliciter l'assistance d'un avocat pris en charge (aide juridique de 2e ligne).",
    base_legale: "Code judiciaire — aide juridique (deuxième ligne / pro deo)",
    fiche: "aide_juridique",
    champs: [
      { key: "nom", label: "Votre nom" },
      { key: "adresse", label: "Votre adresse" },
      { key: "destinataire", label: "Bureau d'Aide Juridique (BAJ)" },
      { key: "adresse_dest", label: "Adresse du BAJ" },
      { key: "date", label: "Date" },
      { key: "probleme", label: "Nature du problème juridique", aire: true },
    ],
    corps: (v) =>
      exp(v) + dest(v) +
      `Objet : Demande d'aide juridique de deuxième ligne (pro deo)\n\nMadame, Monsieur,\n\n` +
      `Je sollicite le bénéfice de l'aide juridique de deuxième ligne pour la situation suivante :\n` +
      `${v.probleme || "[décrivez votre problème]"}.\n\n` +
      `Mes revenus sont limités ; je joins les documents justificatifs de ma situation (composition de ménage, revenus). ` +
      `Je vous remercie de m'indiquer si je remplis les conditions et la marche à suivre pour la désignation d'un avocat.\n\n` +
      `Je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées.\n\n${v.nom || "[Votre nom]"}`,
  },
  {
    id: "preavis",
    titre: "Résiliation de bail par le locataire (préavis)",
    intro: "Pour donner congé de votre logement en respectant le préavis.",
    base_legale: "Code civil — bail de résidence principale (congé et délai de préavis du locataire)",
    fiche: "bail_wallonie",
    champs: [
      { key: "nom", label: "Votre nom" },
      { key: "adresse", label: "Votre adresse" },
      { key: "destinataire", label: "Nom du bailleur" },
      { key: "adresse_dest", label: "Adresse du bailleur" },
      { key: "date", label: "Date" },
      { key: "adresse_bien", label: "Adresse du logement loué" },
    ],
    corps: (v) =>
      exp(v) + dest(v) +
      `Objet : Congé de bail (résiliation par le locataire)\n\nMadame, Monsieur,\n\n` +
      `Je vous donne par la présente congé du logement situé ${v.adresse_bien || "[adresse]"}, ` +
      `en respectant le délai de préavis légal applicable à mon bail.\n\n` +
      `Le préavis prend cours le premier jour du mois qui suit l'envoi de ce courrier. Je vous propose de convenir ensemble ` +
      `d'une date d'état des lieux de sortie.\n\n` +
      `Je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées.\n\n${v.nom || "[Votre nom]"}`,
  },
];

export default function LettresPage() {
  const [sel, setSel] = useState(MODELES[0].id);
  const [v, setV] = useState<Record<string, string>>({});
  const modele = MODELES.find((m) => m.id === sel)!;
  const texte = modele.corps(v);

  function maj(k: string, val: string) {
    setV((prev) => ({ ...prev, [k]: val }));
  }
  function choisir(id: string) {
    setSel(id);
    setV({});
  }
  function copier() {
    navigator.clipboard?.writeText(texte);
  }
  function imprimer() {
    const w = window.open("", "_blank");
    if (!w) return;
    w.document.write(`<pre style="font-family:Georgia,serif;white-space:pre-wrap;padding:40px;line-height:1.6">${texte.replace(/</g, "&lt;")}</pre>`);
    w.document.close();
    w.print();
  }

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="font-bold text-lg tracking-tight">La Loi Avec Moi</Link>
          <Link href="/base-juridique" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Toutes mes réponses →</Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-blue-950 to-slate-900 text-white py-14 px-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold">Générateur de lettres</h1>
          <p className="mt-3 text-blue-100 max-w-2xl">
            Une lettre claire, pré-rédigée et gratuite — avec la base légale citée. Remplissez, copiez, envoyez.
          </p>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-6 py-10 grid lg:grid-cols-2 gap-8">
        {/* Choix + formulaire */}
        <div>
          <label className="block text-sm font-semibold text-slate-800 mb-2">Quelle lettre ?</label>
          <div className="flex flex-wrap gap-2">
            {MODELES.map((m) => (
              <button
                key={m.id}
                type="button"
                onClick={() => choisir(m.id)}
                className={"px-3 py-2 rounded-full border text-sm font-medium transition-colors " +
                  (sel === m.id ? "bg-blue-700 border-blue-700 text-white" : "bg-white border-slate-300 text-slate-700 hover:border-blue-400")}
              >
                {m.titre}
              </button>
            ))}
          </div>
          <p className="text-sm text-slate-500 mt-3">{modele.intro}</p>

          <div className="mt-5 space-y-3">
            {modele.champs.map((c) => (
              <div key={c.key}>
                <label className="block text-xs font-semibold text-slate-600 mb-1">{c.label}</label>
                {c.aire ? (
                  <textarea
                    rows={3}
                    value={v[c.key] || ""}
                    onChange={(e) => maj(c.key, e.target.value)}
                    className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
                  />
                ) : (
                  <input
                    type="text"
                    value={v[c.key] || ""}
                    onChange={(e) => maj(c.key, e.target.value)}
                    className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
                  />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Aperçu */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-sm font-semibold text-slate-800">Votre lettre</label>
            <div className="flex gap-2">
              <button type="button" onClick={copier} className="text-sm font-semibold text-blue-700 hover:text-blue-900">Copier</button>
              <button type="button" onClick={imprimer} className="text-sm font-semibold text-blue-700 hover:text-blue-900">Imprimer / PDF</button>
            </div>
          </div>
          <pre className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm text-slate-800 whitespace-pre-wrap font-serif leading-relaxed min-h-[300px]">{texte}</pre>
          <p className="mt-3 text-xs text-slate-500">⚖️ Base légale : {modele.base_legale}.</p>
          {modele.fiche && (
            <Link href={`/loi/${modele.fiche}`} className="text-sm font-semibold text-blue-700 hover:text-blue-900 mt-1 inline-block">
              Lire la fiche sourcée →
            </Link>
          )}
          <p className="mt-4 text-xs text-slate-400 border-t border-slate-100 pt-3">
            Modèle indicatif, à adapter à votre situation. Ne remplace pas un conseil juridique personnalisé.
            Pour un litige, voyez l&apos;aide juridique ou un professionnel.
          </p>
        </div>
      </div>
    </main>
  );
}
