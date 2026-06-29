import Link from "next/link";

// Page « Fiduciaires & comptables » — Caelum (ENTREPRISES, séparé de La Loi Avec Moi).
// Programme partenaire marque blanche pour cabinets (cible : experts-comptables ITAA).
// Honnêteté : on présente un PROGRAMME à mettre en place ensemble, pas un portail SaaS
// multi-clients déjà existant. Aucun montant inventé ("sur devis", "à définir ensemble").

export const metadata = {
  title: "Programme partenaire fiduciaires & comptables — Caelum",
  description:
    "Offrez à vos clients une conformité réglementaire suivie (e-facturation, RGPD, NIS2…) en marque blanche, sans surcharger votre cabinet.",
};

const benefices = [
  {
    titre: "Un service de plus, sans recruter",
    texte:
      "La conformité réglementaire devient une offre de votre cabinet, prise en charge par Caelum. Vous gardez la relation client, nous faisons le travail de fond.",
  },
  {
    titre: "Marque blanche ou co-branding",
    texte:
      "Diagnostic, checklist « suis-je en règle ? » et attestation peuvent porter vos couleurs. À définir ensemble selon votre image.",
  },
  {
    titre: "Vos clients restent en règle",
    texte:
      "Veille réglementaire, échéances à jour (CSRD, transparence salariale, PPWR…) : vos clients ne ratent plus une obligation, et c'est vous qui le leur apportez.",
  },
  {
    titre: "Conformité (partiellement) finançable",
    texte:
      "Pour certains volets (cybersécurité, numérique), des aides publiques régionales existent. Un argument concret à présenter à vos clients.",
  },
];

const etapes = [
  "On cadre ensemble le périmètre (vos clients types, vos secteurs, votre image).",
  "On met en place le dispositif : diagnostic, suivi des échéances, documents tenus à jour.",
  "Vous présentez l'offre à vos clients ; nous assurons l'exécution et le support.",
];

export default function FiduciairesPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link
            href="/contact"
            className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors"
          >
            Devenir partenaire
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Fiduciaires & experts-comptables
          </span>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
            La conformité de vos clients,
            <span className="block bg-gradient-to-r from-indigo-300 to-sky-300 bg-clip-text text-transparent">
              portée par votre cabinet
            </span>
          </h1>
          <p className="text-lg text-slate-300 mt-6 leading-relaxed">
            Vos clients vous posent déjà des questions sur l&apos;e-facturation, le RGPD, NIS2… Faites-en une offre de
            votre cabinet, en marque blanche, sans surcharge pour vos équipes. Caelum exécute, vous gardez la relation.
          </p>
          <Link
            href="/contact"
            className="inline-block mt-7 bg-white/10 border border-white/20 hover:bg-white/20 text-white font-semibold px-6 py-3 rounded-xl transition-colors"
          >
            Discuter d&apos;un partenariat
          </Link>
        </div>
      </section>

      <section className="py-16 px-6 max-w-6xl mx-auto">
        <h2 className="text-2xl font-bold text-center">Pourquoi un cabinet s&apos;associe à Caelum</h2>
        <div className="mt-10 grid md:grid-cols-2 gap-6">
          {benefices.map((b) => (
            <div key={b.titre} className="rounded-2xl border border-slate-200 p-6">
              <h3 className="font-bold text-lg">{b.titre}</h3>
              <p className="mt-2 text-sm text-slate-600 leading-relaxed">{b.texte}</p>
            </div>
          ))}
        </div>

        <div className="mt-12 rounded-2xl bg-slate-50 border border-slate-200 p-7">
          <h2 className="text-xl font-bold">Comment ça marche</h2>
          <ol className="mt-5 space-y-4">
            {etapes.map((e, i) => (
              <li key={i} className="flex items-start gap-3">
                <span className="flex-shrink-0 w-7 h-7 rounded-full bg-indigo-600 text-white text-sm font-bold flex items-center justify-center">
                  {i + 1}
                </span>
                <span className="text-sm text-slate-700 leading-relaxed pt-0.5">{e}</span>
              </li>
            ))}
          </ol>
        </div>

        <div className="mt-10 rounded-2xl bg-indigo-600 text-white p-8 text-center">
          <h2 className="text-2xl font-bold">Construisons votre offre conformité</h2>
          <p className="text-indigo-100 mt-2 text-sm max-w-2xl mx-auto leading-relaxed">
            Les modalités (marque blanche, périmètre, conditions) se définissent ensemble selon votre cabinet.
            Parlons-en : un échange suffit pour voir si c&apos;est pertinent pour vos clients.
          </p>
          <Link
            href="/contact"
            className="inline-block mt-6 bg-white text-indigo-700 font-semibold px-6 py-3 rounded-xl hover:bg-indigo-50 transition-colors"
          >
            Devenir partenaire
          </Link>
        </div>
      </section>

      <section className="py-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h3 className="font-semibold text-amber-900">⚖️ En toute transparence</h3>
          <p className="text-amber-800 text-sm mt-2 leading-relaxed">
            Ce programme se met en place avec vous : il ne s&apos;agit pas d&apos;un portail clé en main déjà déployé,
            mais d&apos;un partenariat que nous cadrons ensemble. Conditions et tarifs sur devis, validés avant tout
            engagement. Caelum n&apos;est pas un cabinet d&apos;avocats : pour les actes juridiques réservés, nous
            travaillons avec votre réseau.
          </p>
        </div>
      </section>
    </main>
  );
}
