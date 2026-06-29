import Link from "next/link";

// FAQ Caelum — anticipe les problématiques clients, crée du maillage interne (liens)
// et de la réputation (transparence + données structurées JSON-LD pour Google).
// Rendu statique, honnête : aucune promesse en l'air, aucun faux avis.

export const dynamic = "force-static";
export const metadata = {
  title: "FAQ — vos questions sur la conformité 2026 | Caelum",
  description:
    "Toutes les réponses sur la conformité des entreprises en Belgique : e-facturation, RGPD, NIS2, CSRD, délais, sanctions, prix, aides publiques et confiance.",
};

type QA = { q: string; a: string; liens?: { label: string; href: string }[] };
type Section = { titre: string; items: QA[] };

const FAQ: Section[] = [
  {
    titre: "Suis-je concerné ?",
    items: [
      {
        q: "Comment savoir quelles obligations s'appliquent à mon entreprise ?",
        a: "Notre simulateur gratuit vous donne, en une minute, la liste exacte des normes qui vous concernent selon votre taille, votre secteur et votre activité — puis un score « suis-je déjà en règle ? ».",
        liens: [{ label: "Faire le test", href: "/conformite-2026" }],
      },
      {
        q: "Mon secteur a-t-il des obligations particulières ?",
        a: "Oui. Selon votre métier (commerce, horeca, construction, IT, finance, industrie, import-export…), certaines normes priment. Nous avons une page dédiée par secteur.",
        liens: [{ label: "Voir par secteur", href: "/conformite" }],
      },
      {
        q: "Je suis une petite structure : suis-je vraiment concerné ?",
        a: "Souvent oui, au moins pour l'e-facturation B2B, le RGPD et le registre UBO. D'autres obligations dépendent de seuils (par ex. la transparence salariale dès 100 travailleurs). Le simulateur fait le tri pour vous.",
        liens: [{ label: "Vérifier ma situation", href: "/conformite-2026" }],
      },
    ],
  },
  {
    titre: "Délais & sanctions",
    items: [
      {
        q: "Quelles sont les échéances 2026 à ne pas manquer ?",
        a: "E-facturation B2B (depuis 2026), CSRD, transparence salariale, PPWR, CBAM, NIS2, DORA… Chaque norme a sa date. Notre simulateur génère un calendrier (.ics) à ajouter à votre agenda.",
        liens: [{ label: "Mes échéances", href: "/conformite-2026" }],
      },
      {
        q: "Que risque-t-on en cas de non-conformité ?",
        a: "Selon la norme : amendes administratives, perte d'avantages (par ex. déduction TVA), retrait du marché, responsabilité renforcée du dirigeant. Chaque fiche norme précise la sanction et la source officielle.",
        liens: [{ label: "Détail des normes", href: "/conformite" }],
      },
    ],
  },
  {
    titre: "Comment Caelum m'aide",
    items: [
      {
        q: "Concrètement, que faites-vous pour moi ?",
        a: "Diagnostic, mise en conformité (e-facture, RGPD, NIS2…), veille réglementaire, documents tenus à jour, et montage de dossiers de subvention. On entre par l'urgent puis on vous garde en règle dans le temps.",
        liens: [{ label: "Nos offres", href: "/offres-conformite" }],
      },
      {
        q: "Puis-je obtenir une preuve de ma démarche ?",
        a: "Oui : le simulateur génère une attestation d'auto-évaluation horodatée à conserver dans votre registre de conformité interne. C'est une auto-déclaration, pas une certification officielle — nous le disons clairement.",
        liens: [{ label: "Générer mon attestation", href: "/conformite-2026" }],
      },
    ],
  },
  {
    titre: "Prix & financement",
    items: [
      {
        q: "Combien ça coûte ?",
        a: "Chaque mission fait l'objet d'un devis clair, validé avant de commencer. Pas de prestation inutile, pas de surprise.",
        liens: [{ label: "Demander un devis", href: "/contact" }],
      },
      {
        q: "Existe-t-il des aides pour financer la mise en conformité ?",
        a: "Oui. Des aides publiques régionales (chèques Wallonie jusqu'à 75 % en cybersécurité, kmo-portefeuille en Flandre) peuvent prendre en charge une partie d'un accompagnement conseil/formation. Le simulateur vous montre celles liées à vos obligations.",
        liens: [{ label: "Conformité finançable", href: "/conformite-2026" }],
      },
    ],
  },
  {
    titre: "Confiance & données",
    items: [
      {
        q: "Comment être sûr que vos informations sont fiables ?",
        a: "Chaque analyse renvoie à un texte légal officiel ou une donnée publique vérifiable — jamais à une opinion. Vous pouvez tracer la source de chaque information.",
        liens: [{ label: "Notre méthode", href: "/notre-force" }],
      },
      {
        q: "Que faites-vous de mes données ?",
        a: "Vos données servent uniquement à traiter votre demande ; elles ne sont ni vendues ni cédées. Vous pouvez demander leur accès, rectification ou suppression à tout moment (RGPD).",
        liens: [{ label: "Confidentialité", href: "/confidentialite" }],
      },
      {
        q: "Êtes-vous un cabinet d'avocats ?",
        a: "Non. Caelum outille et accompagne votre conformité ; pour les actes juridiques réservés, nous travaillons avec un réseau de professionnels. Les informations fournies ne constituent pas un conseil juridique individualisé.",
        liens: [{ label: "Mentions légales", href: "/mentions-legales" }],
      },
    ],
  },
  {
    titre: "Partenaires & international",
    items: [
      {
        q: "Je suis fiduciaire / comptable : puis-je proposer Caelum à mes clients ?",
        a: "Oui, via notre programme partenaire en marque blanche : vous gardez la relation client, nous assurons l'exécution.",
        liens: [{ label: "Programme fiduciaires", href: "/fiduciaires" }],
      },
      {
        q: "Travaillez-vous en anglais / néerlandais ?",
        a: "Oui. Le site existe en français, néerlandais et anglais, avec une traduction à la volée pour les autres langues — la version FR/NL fait foi pour le contenu juridique.",
        liens: [{ label: "English version", href: "/en" }],
      },
    ],
  },
];

export default function FAQPage() {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: FAQ.flatMap((s) =>
      s.items.map((it) => ({
        "@type": "Question",
        name: it.q,
        acceptedAnswer: { "@type": "Answer", text: it.a },
      })),
    ),
  };

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <header className="border-b border-slate-100">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link href="/conformite-2026" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Suis-je concerné ?</Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-slate-950 to-slate-900 text-white py-16 px-6">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold">Vos questions, nos réponses</h1>
          <p className="mt-3 text-slate-300">
            Tout ce qu'une entreprise a besoin de savoir sur la conformité 2026 — clairement, et avec nos sources.
          </p>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-6 py-12">
        {FAQ.map((s) => (
          <section key={s.titre} className="mb-10">
            <h2 className="text-xl font-bold text-slate-900 mb-4">{s.titre}</h2>
            <div className="space-y-4">
              {s.items.map((it) => (
                <article key={it.q} className="rounded-2xl border border-slate-200 p-5">
                  <h3 className="font-semibold text-slate-900">{it.q}</h3>
                  <p className="mt-2 text-sm text-slate-600 leading-relaxed">{it.a}</p>
                  {it.liens && (
                    <div className="mt-3 flex flex-wrap gap-3">
                      {it.liens.map((l) => (
                        <Link key={l.href} href={l.href} className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">
                          {l.label} →
                        </Link>
                      ))}
                    </div>
                  )}
                </article>
              ))}
            </div>
          </section>
        ))}

        <div className="rounded-2xl bg-indigo-600 text-white p-7 text-center">
          <h2 className="text-xl font-bold">Une question qui n'est pas ici ?</h2>
          <p className="text-indigo-100 mt-2 text-sm">On répond honnêtement, sans jargon, sous 24h.</p>
          <Link href="/contact" className="inline-block mt-5 bg-white text-indigo-700 font-semibold px-6 py-3 rounded-xl hover:bg-indigo-50 transition-colors">
            Poser ma question
          </Link>
        </div>
      </div>
    </main>
  );
}
