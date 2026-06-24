import Link from "next/link";
import BanniereLangues from "@/components/BanniereLangues";

const themes = [
  {
    t: "En danger ? Où aller",
    d: "Violences, agression, détresse, enfant en danger, cyberharcèlement : les numéros d'aide gratuits français, par situation, à appeler en un tap.",
    href: "/la-loi-avec-moi-france/en-danger",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M12 3l7 4v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V7l7-4z" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M12 8v4M12 15.5v.5" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    t: "Logement & bail",
    d: "Vos droits de locataire ou de propriétaire : bail, dépôt de garantie, préavis, réparations, encadrement des loyers.",
    href: "/la-loi-avec-moi-france/logement",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M3 11l9-7 9 7" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M5 10v10h14V10" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    t: "Travail & emploi",
    d: "Contrat, préavis, congés, rupture conventionnelle, salaire : ce que le Code du travail prévoit pour les salariés en France.",
    href: "/la-loi-avec-moi-france/travail",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <rect x="3" y="7" width="18" height="13" rx="2" />
        <path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    t: "Consommation",
    d: "Garanties, droit de rétractation, achats en ligne, litiges : vos protections de consommateur en France.",
    href: "/la-loi-avec-moi-france/consommation",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M6 6h15l-1.5 9h-12z" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M6 6L5 3H3" strokeLinecap="round" />
        <circle cx="9" cy="20" r="1" /><circle cx="18" cy="20" r="1" />
      </svg>
    ),
  },
  {
    t: "Famille & vie privée",
    d: "Mariage, PACS, séparation, succession, et vos droits sur vos données personnelles (RGPD / CNIL).",
    href: "/la-loi-avec-moi-france/famille",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <circle cx="9" cy="8" r="3" /><circle cx="17" cy="9" r="2" />
        <path d="M3 20c0-3 2.5-5 6-5s6 2 6 5M16 14c2.5 0 5 1.5 5 4" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    t: "Démarches administratives",
    d: "Comprendre un courrier de l'administration, vos délais, vos recours, où vous adresser. On débroussaille.",
    href: "/la-loi-avec-moi-france/demarches",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <rect x="5" y="3" width="14" height="18" rx="2" />
        <path d="M9 8h6M9 12h6M9 16h4" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    t: "Trouver le bon avocat",
    d: "Aide juridictionnelle, annuaire officiel des avocats, consultations gratuites, honoraires : le bon avocat, au bon prix.",
    href: "/la-loi-avec-moi-france/trouver-un-avocat",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M12 3v7M5 10h14M6 10l-3 6a3 3 0 006 0zM18 10l-3 6a3 3 0 006 0z" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M9 21h6" strokeLinecap="round" />
      </svg>
    ),
  },
];

export default function LoiAvecMoiFrancePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <BanniereLangues theme="blue" href="/la-loi-avec-moi-france/bienvenue" />
      {/* Header */}
      <header className="border-b border-slate-100">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/la-loi-avec-moi-france" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">L</span>
            </div>
            <span className="font-bold text-lg tracking-tight">La loi avec moi <span className="text-blue-700">· France</span></span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-medium text-slate-500 hover:text-slate-900">🇧🇪 Version Belgique →</Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-blue-950 to-slate-900 text-white py-24 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.28),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🇫🇷 Édition France
          </span>
          <h1 className="text-4xl sm:text-6xl font-bold tracking-tight leading-tight">Vos droits, expliqués simplement</h1>
          <p className="mt-4 text-base sm:text-lg font-semibold tracking-wide text-blue-200">
            Le droit accessible pour tous.
          </p>
          <p className="text-lg text-slate-300 mt-6 leading-relaxed max-w-2xl mx-auto">
            Comprendre la loi en France sans jargon, avec des <strong className="text-white">sources officielles</strong>.
            Un espace clair, pensé pour le mobile — et entièrement <strong className="text-white">distinct</strong> du site belge.
          </p>
          <div className="mt-8">
            <Link href="/la-loi-avec-moi-france/en-danger" className="inline-flex items-center gap-2 bg-white text-blue-900 hover:bg-slate-100 font-semibold px-6 py-3.5 rounded-xl transition-colors shadow-lg">
              En danger ? Trouver de l&apos;aide tout de suite →
            </Link>
          </div>
        </div>
      </section>

      {/* Bandeau de lancement honnête */}
      <section className="bg-blue-50 border-b border-blue-100 px-6 py-4">
        <p className="max-w-3xl mx-auto text-center text-sm text-blue-900/80 leading-relaxed">
          ✅ <strong>Les 6 rubriques de l&apos;édition France sont en ligne</strong>, chacune vérifiée sur des sources
          officielles françaises (service-public.fr, CNIL, Légifrance, Défenseur des droits). Nous continuons à les
          enrichir et à les tenir à jour.
        </p>
      </section>

      {/* Thèmes */}
      <section className="py-20 px-6 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold tracking-tight text-center">Choisissez votre sujet</h2>
        <p className="text-slate-500 mt-3 text-center max-w-2xl mx-auto">
          Chaque rubrique va à l&apos;essentiel : ce que dit la loi, vos droits, et où vérifier la source officielle.
        </p>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 mt-12">
          {themes.map((th) =>
            th.href ? (
              <Link key={th.t} href={th.href} className="group rounded-2xl border border-slate-200 p-7 hover:shadow-lg hover:-translate-y-1 hover:border-blue-300 transition-all">
                <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-700 flex items-center justify-center mb-5">{th.icon}</div>
                <h3 className="text-lg font-bold tracking-tight">{th.t}</h3>
                <p className="text-slate-600 mt-2 text-sm leading-relaxed">{th.d}</p>
                <span className="inline-block mt-4 text-blue-700 font-semibold text-sm group-hover:translate-x-1 transition-transform">Voir mes droits →</span>
              </Link>
            ) : (
              <div key={th.t} className="rounded-2xl border border-slate-200 p-7 opacity-80">
                <div className="w-12 h-12 rounded-xl bg-slate-100 text-slate-400 flex items-center justify-center mb-5">{th.icon}</div>
                <h3 className="text-lg font-bold tracking-tight text-slate-700">{th.t}</h3>
                <p className="text-slate-500 mt-2 text-sm leading-relaxed">{th.d}</p>
                <span className="inline-block mt-4 text-slate-400 font-medium text-xs">Bientôt disponible</span>
              </div>
            )
          )}
        </div>
      </section>

      {/* CTA Quiz */}
      <section className="px-6 pb-4">
        <Link href="/la-loi-avec-moi-france/quiz" className="group block max-w-4xl mx-auto rounded-3xl bg-gradient-to-br from-blue-600 to-blue-800 text-white p-8 sm:p-10 hover:shadow-xl transition-shadow">
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6 justify-between">
            <div>
              <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/15 text-white/90 text-xs font-semibold mb-3">🧠 Quiz gratuit</span>
              <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">Connaissez-vous vraiment vos droits ?</h2>
              <p className="text-blue-100 mt-2 text-sm sm:text-base leading-relaxed max-w-xl">
                8 questions sur des situations du quotidien en France. Chaque réponse est expliquée et renvoie vers une fiche sourcée.
              </p>
            </div>
            <span className="flex-shrink-0 inline-flex items-center gap-2 bg-white text-blue-800 font-semibold px-6 py-3.5 rounded-xl group-hover:translate-x-1 transition-transform">
              Faire le quiz →
            </span>
          </div>
        </Link>
      </section>

      {/* Confiance / source */}
      <section className="py-16 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-2xl font-bold tracking-tight">Notre engagement : la justesse avant tout</h2>
          <p className="text-slate-600 mt-4 leading-relaxed">
            La loi française n&apos;est pas la loi belge. Chaque information de cette édition est rédigée et vérifiée
            spécifiquement pour la France, et renvoie vers la source officielle. Nous ne réinventons pas la loi :
            nous la rendons claire.
          </p>
          <p className="text-slate-400 text-sm mt-6">
            Conçu et développé par Caelum Partners — méthode combinant des agents IA spécialisés et une supervision humaine systématique.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-10 px-6 text-center text-sm text-slate-500">
        <p>« La loi avec moi · France » — informations générales, ne remplace pas un conseil juridique personnalisé.</p>
        <div className="mt-3 flex flex-wrap items-center justify-center gap-x-5 gap-y-2">
          <Link href="/la-loi-avec-moi-france/nos-assistants" className="text-blue-700 hover:text-blue-900 font-medium">Qui sont nos assistants ?</Link>
          <Link href="/loi-avec-moi" className="text-blue-700 hover:text-blue-900 font-medium">🇧🇪 Voir la version Belgique →</Link>
        </div>
      </footer>
    </main>
  );
}
