"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

// Générateur de documents (espace Belgique francophone).
// Modèle économique honnête (freemium) :
//  - GRATUIT : aperçu en direct (filigrané) + copier le texte → l'usager peut toujours s'en sortir seul.
//  - PREMIUM : document personnalisé mis en forme, prêt à imprimer / enregistrer en PDF.
// On vend une PRESTATION DE MISE EN FORME, jamais du conseil juridique (réservé aux avocats).
// ⚠️ Le paiement réel n'est PAS branché ici : il nécessitera un prestataire (Stripe) et des clés
//    en variables d'environnement — ZÉRO credential dans le code.

type Field = {
  id: string;
  label: string;
  placeholder: string;
  type?: "text" | "textarea" | "date";
};

type Modele = {
  id: string;
  tag: string;
  title: string;
  desc: string;
  fields: Field[];
  build: (v: Record<string, string>) => string;
};

const F = {
  exp: { id: "expediteur", label: "Votre nom et prénom", placeholder: "Marie Dupont" },
  adr: { id: "adresse", label: "Votre adresse", placeholder: "Rue de la Loi 1, 1000 Bruxelles" },
  contact: { id: "contact", label: "Votre e-mail / téléphone", placeholder: "marie@exemple.be · 0470 00 00 00" },
  dest: { id: "destinataire", label: "Destinataire (nom)", placeholder: "Agence Immobilière X / Société Y" },
  destAdr: { id: "destAdresse", label: "Adresse du destinataire", placeholder: "Avenue Louise 100, 1050 Bruxelles" },
  lieu: { id: "lieu", label: "Fait à", placeholder: "Bruxelles" },
  date: { id: "date", label: "Date", placeholder: "", type: "date" as const },
};

function entete(v: Record<string, string>) {
  return `${v.expediteur || "[Votre nom]"}
${v.adresse || "[Votre adresse]"}
${v.contact || "[Votre e-mail / téléphone]"}

À l'attention de :
${v.destinataire || "[Destinataire]"}
${v.destAdresse || "[Adresse du destinataire]"}

${v.lieu || "[Lieu]"}, le ${v.date || "[date]"}

Envoi recommandé`;
}

function signature(v: Record<string, string>) {
  return `Je vous prie d'agréer mes salutations distinguées.

${v.expediteur || "[Votre nom]"}
(signature)`;
}

const MODELES: Modele[] = [
  {
    id: "mise-en-demeure",
    tag: "Réclamation",
    title: "Mise en demeure (paiement / obligation)",
    desc: "Pour exiger formellement un paiement, une réparation ou le respect d'un engagement, avec un délai.",
    fields: [
      F.exp, F.adr, F.contact, F.dest, F.destAdr,
      { id: "objet", label: "Ce que vous réclamez (en bref)", placeholder: "Remboursement de 350 € pour service non fourni", type: "textarea" },
      { id: "faits", label: "Les faits (ce qui s'est passé)", placeholder: "Le 3 mars, j'ai payé… Depuis, malgré mes relances…", type: "textarea" },
      { id: "delai", label: "Délai accordé", placeholder: "15 jours" },
      F.lieu, F.date,
    ],
    build: (v) => `${entete(v)}

Objet : Mise en demeure

Madame, Monsieur,

Par la présente, je vous mets en demeure concernant : ${v.objet || "[objet de la réclamation]"}.

Pour rappel des faits : ${v.faits || "[décrivez les faits, dates et montants]"}.

Je vous demande de régulariser la situation dans un délai de ${v.delai || "[délai]"} à compter de la réception de ce courrier. À défaut, je me réserve le droit d'entreprendre toute démarche utile pour faire valoir mes droits, y compris devant les instances compétentes.

${signature(v)}`,
  },
  {
    id: "garantie-locative",
    tag: "Logement",
    title: "Demande de restitution de la garantie locative",
    desc: "Pour récupérer votre garantie après la fin du bail, lorsque le propriétaire tarde à la libérer.",
    fields: [
      F.exp, F.adr, F.contact, F.dest, F.destAdr,
      { id: "bienAdresse", label: "Adresse du logement loué", placeholder: "Rue des Fleurs 12, 1030 Bruxelles" },
      { id: "finBail", label: "Date de fin du bail / état des lieux de sortie", placeholder: "30 avril 2026" },
      { id: "montant", label: "Montant de la garantie", placeholder: "1 500 €" },
      { id: "compte", label: "Votre IBAN pour le remboursement", placeholder: "BE00 0000 0000 0000" },
      F.lieu, F.date,
    ],
    build: (v) => `${entete(v)}

Objet : Demande de libération de la garantie locative

Madame, Monsieur,

Le bail relatif au logement situé ${v.bienAdresse || "[adresse du logement]"} a pris fin le ${v.finBail || "[date]"}, et l'état des lieux de sortie a été réalisé.

Je vous demande de bien vouloir libérer la garantie locative d'un montant de ${v.montant || "[montant]"}, conformément à la loi. Je vous prie de procéder au versement sur le compte suivant : ${v.compte || "[IBAN]"}.

Sans réponse de votre part dans un délai raisonnable, je me réserve le droit de saisir le juge de paix compétent.

${signature(v)}`,
  },
  {
    id: "retractation",
    tag: "Consommation",
    title: "Rétractation d'un achat à distance",
    desc: "Pour annuler un achat en ligne dans le délai légal de rétractation et obtenir le remboursement.",
    fields: [
      F.exp, F.adr, F.contact, F.dest, F.destAdr,
      { id: "produit", label: "Produit / service commandé", placeholder: "Aspirateur modèle X" },
      { id: "commande", label: "N° de commande", placeholder: "CMD-2026-12345" },
      { id: "dateCommande", label: "Date de commande / réception", placeholder: "10 juin 2026" },
      F.lieu, F.date,
    ],
    build: (v) => `${entete(v)}

Objet : Exercice du droit de rétractation

Madame, Monsieur,

Conformément à mon droit de rétractation, je vous notifie par la présente l'annulation de la commande suivante :

- Produit / service : ${v.produit || "[produit]"}
- N° de commande : ${v.commande || "[numéro]"}
- Date de commande / réception : ${v.dateCommande || "[date]"}

Je vous demande de me rembourser l'intégralité des sommes versées, y compris les frais de livraison standard, dans les meilleurs délais et au plus tard dans le délai légal. Je vous renverrai le produit selon vos instructions.

${signature(v)}`,
  },
  {
    id: "aide-juridique",
    tag: "Accès au droit",
    title: "Demande d'aide juridique (« pro deo »)",
    desc: "Pour solliciter un avocat dans le cadre de l'aide juridique, gratuite ou partiellement gratuite selon vos revenus.",
    fields: [
      F.exp, F.adr, F.contact,
      { id: "probleme", label: "Votre problème (en bref)", placeholder: "Litige avec mon propriétaire concernant…", type: "textarea" },
      F.lieu, F.date,
    ],
    build: (v) => `${v.expediteur || "[Votre nom]"}
${v.adresse || "[Votre adresse]"}
${v.contact || "[Votre e-mail / téléphone]"}

${v.lieu || "[Lieu]"}, le ${v.date || "[date]"}

Objet : Demande d'assistance juridique (aide juridique)

Madame, Monsieur,

Je souhaite être assisté·e par un avocat concernant la situation suivante : ${v.probleme || "[expliquez brièvement votre problème]"}.

Mes ressources étant limitées, je souhaite savoir si je peux bénéficier de l'aide juridique (« pro deo »), totalement ou partiellement gratuite. Je vous remercie de me préciser les documents à fournir et un rendez-vous possible.

Dans l'attente de votre réponse, je vous prie d'agréer mes salutations respectueuses.

${v.expediteur || "[Votre nom]"}
(signature)`,
  },
];

export default function GenerateurDocumentsPage() {
  const [selId, setSelId] = useState<string | null>(null);
  const [values, setValues] = useState<Record<string, string>>({});
  const [copied, setCopied] = useState(false);

  const modele = MODELES.find((m) => m.id === selId) ?? null;
  const texte = useMemo(() => (modele ? modele.build(values) : ""), [modele, values]);

  function pick(id: string) {
    setSelId(id);
    setValues({});
    setCopied(false);
  }

  function copy() {
    if (typeof navigator !== "undefined" && navigator.clipboard && modele) {
      navigator.clipboard.writeText(texte).then(() => {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      });
    }
  }

  function imprimer() {
    if (typeof window !== "undefined") window.print();
  }

  return (
    <main className="min-h-screen bg-white text-slate-900">
      {/* zone imprimable isolée (le reste est masqué à l'impression) */}
      <style>{`
        @media print {
          body * { visibility: hidden !important; }
          #zone-impression, #zone-impression * { visibility: visible !important; }
          #zone-impression { position: absolute; left: 0; top: 0; width: 100%; padding: 2.5cm; }
          #filigrane { display: none !important; }
        }
      `}</style>

      <header className="border-b border-slate-100 print:hidden">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi/modeles" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Modèles gratuits →</Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-16 px-6 print:hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Générateur de documents
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">
            Votre courrier officiel, prêt en 2 minutes
          </h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Choisissez un document, remplissez le formulaire, et obtenez une lettre complète et bien
            mise en forme — à imprimer ou enregistrer en PDF.
          </p>
        </div>
      </section>

      {/* Choix du document */}
      <section className="py-12 px-6 max-w-5xl mx-auto print:hidden">
        <h2 className="text-xl font-bold tracking-tight">1. Choisissez votre document</h2>
        <div className="mt-5 grid sm:grid-cols-2 gap-4">
          {MODELES.map((m) => (
            <button
              key={m.id}
              type="button"
              onClick={() => pick(m.id)}
              className={`text-left rounded-2xl border p-5 transition-all ${
                selId === m.id
                  ? "border-indigo-500 ring-2 ring-indigo-200 bg-indigo-50/50"
                  : "border-slate-200 hover:border-indigo-300 hover:shadow-md"
              }`}
            >
              <span className="text-xs font-bold uppercase tracking-wide text-indigo-600">{m.tag}</span>
              <h3 className="font-bold tracking-tight mt-1">{m.title}</h3>
              <p className="text-slate-600 text-sm mt-1.5 leading-relaxed">{m.desc}</p>
            </button>
          ))}
        </div>
      </section>

      {/* Formulaire + aperçu */}
      {modele && (
        <section className="pb-12 px-6 max-w-5xl mx-auto grid lg:grid-cols-2 gap-8">
          {/* Formulaire */}
          <div className="print:hidden">
            <h2 className="text-xl font-bold tracking-tight">2. Remplissez vos informations</h2>
            <div className="mt-5 space-y-4">
              {modele.fields.map((f) => (
                <div key={f.id}>
                  <label htmlFor={f.id} className="block text-sm font-semibold text-slate-700 mb-1.5">
                    {f.label}
                  </label>
                  {f.type === "textarea" ? (
                    <textarea
                      id={f.id}
                      rows={3}
                      placeholder={f.placeholder}
                      value={values[f.id] ?? ""}
                      onChange={(e) => setValues((s) => ({ ...s, [f.id]: e.target.value }))}
                      className="w-full rounded-xl border border-slate-300 px-3.5 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none resize-y"
                    />
                  ) : (
                    <input
                      id={f.id}
                      type={f.type === "date" ? "date" : "text"}
                      placeholder={f.placeholder}
                      value={values[f.id] ?? ""}
                      onChange={(e) => setValues((s) => ({ ...s, [f.id]: e.target.value }))}
                      className="w-full rounded-xl border border-slate-300 px-3.5 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none"
                    />
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Aperçu */}
          <div>
            <h2 className="text-xl font-bold tracking-tight print:hidden">3. Aperçu en direct</h2>
            <div className="mt-5 relative">
              <div
                id="zone-impression"
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
              >
                <pre className="whitespace-pre-wrap font-sans text-sm text-slate-800 leading-relaxed">
                  {texte}
                </pre>
              </div>
              {/* Filigrane (aperçu seulement, retiré à l'impression) */}
              <div
                id="filigrane"
                aria-hidden="true"
                className="pointer-events-none absolute inset-0 flex items-center justify-center overflow-hidden rounded-2xl"
              >
                <span className="text-slate-200/70 text-3xl font-black tracking-widest rotate-[-25deg] select-none">
                  APERÇU · LA LOI AVEC MOI
                </span>
              </div>
            </div>

            {/* Actions */}
            <div className="mt-5 flex flex-wrap gap-3 print:hidden">
              <button
                type="button"
                onClick={copy}
                className="inline-flex items-center gap-2 text-sm font-semibold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 rounded-xl px-4 py-2.5 transition-colors"
              >
                {copied ? "✓ Copié !" : "Copier le texte (gratuit)"}
              </button>
              <button
                type="button"
                onClick={imprimer}
                className="inline-flex items-center gap-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl px-4 py-2.5 transition-colors"
              >
                Imprimer / Enregistrer en PDF →
              </button>
            </div>
          </div>
        </section>
      )}

      {/* Offre Pro / B2B — transparente */}
      <section className="pb-20 px-6 max-w-5xl mx-auto print:hidden">
        <div className="rounded-2xl border border-indigo-200 bg-indigo-50 p-6">
          <h2 className="font-semibold text-indigo-900 text-lg">Pour les pros, communes & associations</h2>
          <p className="text-indigo-800/90 mt-2 text-sm leading-relaxed">
            Vous accompagnez du public (CPAS, commune, ONG, service RH, assurance protection juridique) ?
            Nous proposons une version <strong>sur mesure et multilingue (FR / NL)</strong> de ce générateur,
            intégrable à vos services. Documents personnalisés en masse, à votre charte.
          </p>
          <Link
            href="/contact"
            className="inline-flex items-center gap-1.5 mt-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 px-5 py-2.5 text-sm font-semibold text-white transition-colors"
          >
            Demander une démo →
          </Link>
        </div>

        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5 mt-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Ces documents sont des aides à la mise en forme, pas un conseil juridique personnalisé
            (réservé aux avocats). Pour une situation grave ou complexe, faites-vous accompagner —
            l&apos;aide juridique « pro deo » peut être gratuite selon vos revenus.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500 print:hidden">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
