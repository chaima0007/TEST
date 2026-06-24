"use client";

import Link from "next/link";

const themes = [
  {
    t: "Logement & bail",
    d: "Vos droits de locataire ou de propriétaire : bail, caution, préavis, réparations, indexation du loyer.",
    href: "/loi-avec-moi/logement",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M3 11l9-7 9 7" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M5 10v10h14V10" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    t: "Travail & emploi",
    d: "Contrat, préavis, congés, licenciement, salaire : ce que la loi prévoit pour les travailleurs en Belgique.",
    href: "/loi-avec-moi/travail",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <rect x="3" y="7" width="18" height="13" rx="2" />
        <path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    t: "Consommation",
    d: "Garanties, droit de rétractation, achats en ligne, litiges avec un commerçant : vos protections de consommateur.",
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
    d: "Mariage, cohabitation, séparation, succession, et vos droits sur vos données personnelles (RGPD).",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <circle cx="9" cy="8" r="3" /><circle cx="17" cy="9" r="2" />
        <path d="M3 20c0-3 2.5-5 6-5s6 2 6 5M16 14c2.5 0 5 1.5 5 4" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    t: "Créer son entreprise",
    d: "Statuts, obligations légales, mentions d'un site, facturation, RGPD : les bases pour démarrer en règle.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M3 21h18M5 21V8l7-4 7 4v13" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M9 21v-6h6v6" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    t: "Démarches administratives",
    d: "Comprendre une lettre de l'administration, vos délais, vos recours, où vous adresser. On débroussaille.",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <rect x="5" y="3" width="14" height="18" rx="2" />
        <path d="M9 8h6M9 12h6M9 16h4" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    t: "Comprendre la Belgique",
    d: "Qui décide quoi ? Fédéral, Régions, Communautés, langues : savoir à quel niveau s'adresser selon votre démarche.",
    href: "/loi-avec-moi/comprendre-la-belgique",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <circle cx="12" cy="12" r="9" />
        <path d="M3 12h18M12 3c2.5 2.5 2.5 15 0 18M12 3c-2.5 2.5-2.5 15 0 18" strokeLinecap="round" />
      </svg>
    ),
  },
];

const sources = [
  { name: "Moniteur belge / Justel", desc: "Tous les textes de loi belges officiels" },
  { name: "EUR-Lex", desc: "Le droit de l'Union européenne" },
  { name: "SPF Justice, Économie, Finances", desc: "Les droits du citoyen, sources publiques" },
];

export default function LoiAvecMoiPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      {/* Header */}
      <header className="border-b border-slate-100">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">L</span>
            </div>
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <div className="hidden sm:flex items-center gap-1">
            <Link href="/loi-avec-moi/mes-droits-maintenant" className="px-3 py-2 text-sm rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 font-medium">Mes droits</Link>
            <Link href="/loi-avec-moi/modeles" className="px-3 py-2 text-sm rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 font-medium">Lettres</Link>
            <Link href="/loi-avec-moi/enfants-places" className="px-3 py-2 text-sm rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 font-medium">Enfants placés</Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-24 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            La loi avec moi · gratuit
          </span>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
            Vos droits et obligations,
            <span className="block bg-gradient-to-r from-indigo-300 to-sky-300 bg-clip-text text-transparent">enfin expliqués simplement</span>
          </h1>
          <p className="text-lg text-slate-300 mt-6 leading-relaxed">
            Comprendre la loi belge ne devrait pas demander un avocat à chaque question.
            On vous explique vos droits <strong className="text-white">en langage clair</strong>, à partir des
            sources officielles — gratuitement.
          </p>
          <Link href="/contact" className="inline-block mt-8 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-indigo-600/30">
            Poser une question
          </Link>
        </div>
      </section>

      {/* Accès rapide */}
      <section className="py-20 px-6 max-w-5xl mx-auto">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <span className="text-indigo-600 font-semibold text-sm uppercase tracking-wide">Accès rapide</span>
          <h2 className="text-3xl font-bold mt-3 tracking-tight">Où voulez-vous aller ?</h2>
          <p className="text-slate-500 mt-4">Trois espaces clairs. Choisissez celui dont vous avez besoin maintenant.</p>
        </div>
        <div className="grid sm:grid-cols-3 gap-6">
          <Link href="/loi-avec-moi/mes-droits-maintenant" className="group rounded-2xl border-2 border-rose-200 p-7 hover:shadow-lg hover:-translate-y-1 transition-all">
            <div className="w-12 h-12 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center mb-5">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6"><path d="M12 3l7 4v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V7l7-4z" strokeLinecap="round" strokeLinejoin="round" /><path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </div>
            <h3 className="text-lg font-bold tracking-tight">Mes droits maintenant</h3>
            <p className="text-slate-600 mt-2 text-sm leading-relaxed">Police, perte de carte d&apos;identité, si on vous fait du mal. Droits essentiels + lecture vocale.</p>
            <span className="inline-block mt-4 text-rose-600 font-semibold text-sm group-hover:translate-x-1 transition-transform">Accéder →</span>
          </Link>
          <Link href="/loi-avec-moi/modeles" className="group rounded-2xl border-2 border-indigo-200 p-7 hover:shadow-lg hover:-translate-y-1 transition-all">
            <div className="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-5">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6"><path d="M4 4h11l5 5v11H4z" strokeLinejoin="round" /><path d="M9 13h6M9 16h6" strokeLinecap="round" /></svg>
            </div>
            <h3 className="text-lg font-bold tracking-tight">Lettres pré-écrites</h3>
            <p className="text-slate-600 mt-2 text-sm leading-relaxed">Plainte, harcèlement à l&apos;école, demande d&apos;avocat, lettre au juge. À copier et envoyer.</p>
            <span className="inline-block mt-4 text-indigo-600 font-semibold text-sm group-hover:translate-x-1 transition-transform">Accéder →</span>
          </Link>
          <Link href="/loi-avec-moi/enfants-places" className="group rounded-2xl border-2 border-emerald-200 p-7 hover:shadow-lg hover:-translate-y-1 transition-all">
            <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-5">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6"><circle cx="12" cy="8" r="3.5" /><path d="M5 21c0-3.5 3-6 7-6s7 2.5 7 6" strokeLinecap="round" /></svg>
            </div>
            <h3 className="text-lg font-bold tracking-tight">Enfants placés</h3>
            <p className="text-slate-600 mt-2 text-sm leading-relaxed">Tes droits, parler à ton juge, demander un avocat. Écrit avec douceur, lisible à voix haute.</p>
            <span className="inline-block mt-4 text-emerald-600 font-semibold text-sm group-hover:translate-x-1 transition-transform">Accéder →</span>
          </Link>
        </div>
      </section>

      {/* Thèmes */}
      <section className="py-16 px-6 max-w-6xl mx-auto">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="text-indigo-600 font-semibold text-sm uppercase tracking-wide">Ce qu&apos;on peut éclaircir</span>
          <h2 className="text-3xl sm:text-4xl font-bold mt-3 tracking-tight">Les sujets du quotidien</h2>
          <p className="text-slate-500 mt-4">Les questions que tout le monde se pose un jour — sans savoir où chercher.</p>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {themes.map((th) =>
            th.href ? (
              <Link key={th.t} href={th.href} className="group rounded-2xl border border-slate-200 p-7 hover:shadow-lg hover:-translate-y-1 hover:border-indigo-300 transition-all">
                <div className="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-5">{th.icon}</div>
                <h3 className="text-lg font-bold tracking-tight">{th.t}</h3>
                <p className="text-slate-600 mt-2 text-sm leading-relaxed">{th.d}</p>
                <span className="inline-block mt-4 text-indigo-600 font-semibold text-sm group-hover:translate-x-1 transition-transform">Voir mes droits →</span>
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

      {/* Sources officielles */}
      <section className="py-20 px-6 bg-slate-50">
        <div className="max-w-4xl mx-auto text-center">
          <span className="text-indigo-600 font-semibold text-sm uppercase tracking-wide">Sources officielles</span>
          <h2 className="text-3xl font-bold mt-3 tracking-tight">On cite toujours d&apos;où vient l&apos;info</h2>
          <p className="text-slate-500 mt-4 max-w-2xl mx-auto">
            Chaque explication s&apos;appuie sur des textes officiels et vérifiables. Pas d&apos;opinion, pas d&apos;à-peu-près.
          </p>
          <div className="grid sm:grid-cols-3 gap-5 mt-10">
            {sources.map((s) => (
              <div key={s.name} className="bg-white rounded-xl border border-slate-200 p-5 text-left">
                <h3 className="font-semibold text-slate-900 text-sm">{s.name}</h3>
                <p className="text-slate-500 text-sm mt-1.5">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Disclaimer honnête */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h3 className="font-semibold text-amber-900">⚖️ En toute transparence</h3>
          <p className="text-amber-800 text-sm mt-2 leading-relaxed">
            « La loi avec moi » fournit de l&apos;<strong>information et de l&apos;orientation</strong> pour comprendre
            vos droits — ce n&apos;est <strong>pas un conseil juridique personnalisé</strong> (une activité réservée
            aux professionnels agréés). Pour toute décision importante ou litige, nous vous orientons vers le
            bon expert (avocat, notaire, médiateur). L&apos;objectif : vous donner de la clarté, gratuitement,
            en toute sécurité.
          </p>
        </div>
      </section>

      {/* CTA */}
      <section className="px-6 pb-24 text-center">
        <h2 className="text-3xl font-bold tracking-tight">Une question juridique vous bloque ?</h2>
        <p className="text-slate-500 mt-3">Posez-la simplement — on vous répond clairement, gratuitement.</p>
        <Link href="/contact" className="inline-block mt-7 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-indigo-600/20">
          Poser ma question
        </Link>
      </section>

      {/* Footer mini */}
      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/" className="hover:text-slate-900">← Retour à l&apos;accueil Caelum</Link>
      </footer>
    </main>
  );
}
