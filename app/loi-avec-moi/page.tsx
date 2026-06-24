"use client";

import Link from "next/link";
import BanniereLangues from "@/components/BanniereLangues";

const themes = [
  {
    t: "En danger ? Où aller",
    d: "Violences, agression, détresse, enfant ou animal en danger : les numéros d'aide gratuits, par situation, à appeler en un tap.",
    href: "/loi-avec-moi/en-danger",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M12 3l7 4v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V7l7-4z" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M12 8v4M12 15.5v.5" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    t: "Si vous avez faim",
    d: "Aide alimentaire près de chez vous : CPAS, Croix-Rouge, Restos du Cœur, épiceries sociales. Adresses officielles.",
    href: "/loi-avec-moi/aide-alimentaire",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M6 3v7a3 3 0 006 0V3M9 3v18M18 3c-1.5 0-2.5 2-2.5 5s1 4 2.5 4v9" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    t: "Trouver le bon avocat",
    d: "La bonne spécialisation selon votre situation, les documents à apporter, et l'aide juridique gratuite (pro deo). Vous arrivez préparé·e.",
    href: "/loi-avec-moi/trouver-un-avocat",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M12 3v4M5 7h14M7 7l-3 7a3 3 0 006 0L7 7zM17 7l-3 7a3 3 0 006 0l-3-7zM9 21h6M12 7v14" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    t: "Porter plainte & police",
    d: "Ce que vous pouvez exiger, que faire si le commissariat refuse votre plainte, et comment signaler un comportement anormal de la police (Comité P).",
    href: "/loi-avec-moi/porter-plainte",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M4 4h11l5 5v11H4z" strokeLinejoin="round" />
        <path d="M8 13h8M8 16h5" strokeLinecap="round" />
        <path d="M12 4v5h5" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    t: "En cas d'injustice",
    d: "Discrimination, problème avec une administration, la police, un commerçant : le bon service officiel à contacter, souvent gratuit.",
    href: "/loi-avec-moi/en-cas-injustice",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M12 3v18M5 7h14M7 7l-3 7a3 3 0 006 0L7 7zM17 7l-3 7a3 3 0 006 0l-3-7z" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    t: "Vos droits à l'aéroport",
    d: "Vol retardé, annulé, refus d'embarquement, bagage perdu : ce que la loi européenne garantit et combien réclamer.",
    href: "/loi-avec-moi/droits-aeroport",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 00-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5L21 16z" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    t: "Chômage : pouvez-vous travailler ?",
    d: "Travailler en touchant des allocations : la déclaration obligatoire (carte eC3.2), l'impact sur vos allocations et les pièges à éviter. Sources ONEM.",
    href: "/loi-avec-moi/chomage",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <rect x="3" y="7" width="18" height="13" rx="2" />
        <path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2" strokeLinecap="round" />
        <path d="M3 12h18" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    t: "Conflit de voisinage",
    d: "Bruit, plantations, vues, mitoyenneté : les voies amiables (médiation, conciliation gratuite au juge de paix) et l'arbitrage, du plus simple au plus formel.",
    href: "/loi-avec-moi/voisinage",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M3 10l5-4 5 4v9H3z" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M13 12l4-3 4 3v7h-8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
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
    href: "/loi-avec-moi/consommation",
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
    href: "/loi-avec-moi/famille",
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
    href: "/loi-avec-moi/creer-entreprise",
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
    href: "/loi-avec-moi/demarches",
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
  {
    t: "Belge à l'étranger",
    d: "Papiers perdus ou volés loin de chez vous, ambassade la plus proche, que faire en cas de crise ou de guerre.",
    href: "/loi-avec-moi/belge-a-letranger",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M2 12h20M12 2a15 15 0 010 20M12 2a15 15 0 000 20" strokeLinecap="round" />
        <circle cx="12" cy="12" r="10" />
      </svg>
    ),
  },
  {
    t: "Protéger les animaux",
    d: "Animal trouvé, blessé, maltraité ou perdu, partir en vacances : leurs droits et qui contacter, par situation.",
    href: "/loi-avec-moi/animaux",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <circle cx="6.5" cy="11" r="1.6" /><circle cx="10" cy="7.5" r="1.6" />
        <circle cx="14" cy="7.5" r="1.6" /><circle cx="17.5" cy="11" r="1.6" />
        <path d="M12 12c-2.2 0-4 1.7-4 3.7 0 1.6 1.3 2.3 2.6 2.3.7 0 1-.3 1.4-.3s.7.3 1.4.3c1.3 0 2.6-.7 2.6-2.3 0-2-1.8-3.7-4-3.7z" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    t: "La loi à la mer",
    d: "À la plage, sur la côte belge : ce que je peux faire et pas (chiens, feu, camping, baignade) et les drapeaux de sécurité.",
    href: "/loi-avec-moi/loi-a-la-mer",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M3 16c1.5 0 1.5 1.5 3 1.5S10.5 16 12 16s1.5 1.5 3 1.5 1.5-1.5 3-1.5 1.5 1.5 3 1.5M3 20c1.5 0 1.5 1.5 3 1.5S10.5 20 12 20s1.5 1.5 3 1.5 1.5-1.5 3-1.5 1.5 1.5 3 1.5" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M15 12V4l5 2-5 2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    t: "La loi en forêt",
    d: "Bivouac, camping sauvage, feu, promenade : où dormir légalement en forêt belge et ce que je risque. Aires de bivouac officielles.",
    href: "/loi-avec-moi/loi-en-foret",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M12 3l4 6h-2.5l3 5H13v7h-2v-7H7.5l3-5H8l4-6z" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    t: "Déchets & environnement",
    d: "Jeter un papier dans la rue, la forêt ou la mer : l'amende que tu risques, et l'impact réel sur la nature. Chiffres officiels.",
    href: "/loi-avec-moi/dechets-environnement",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <path d="M4 7h16M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2M6 7l1 13a2 2 0 002 2h6a2 2 0 002-2l1-13" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M10 11v6M14 11v6" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    t: "Vivre en communauté",
    d: "Musique trop forte, poubelles au mauvais moment, uriner en rue, parties communes : les règles du vivre-ensemble et ce qu'on risque.",
    href: "/loi-avec-moi/vivre-en-communaute",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
        <circle cx="8" cy="8" r="2.5" /><circle cx="16" cy="8" r="2.5" />
        <path d="M3.5 19c0-2.5 2-4.5 4.5-4.5s4.5 2 4.5 4.5M12 19c0-2.5 2-4.5 4.5-4.5s4 2 4 4.5" strokeLinecap="round" />
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
      <BanniereLangues theme="indigo" />
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
          <p className="mt-4 text-base sm:text-lg font-semibold tracking-wide text-indigo-200">
            Le droit accessible pour tous.
          </p>
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

      {/* Quiz CTA */}
      <section className="px-6 pb-4 max-w-5xl mx-auto">
        <Link href="/loi-avec-moi/quiz" className="group block relative overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-600 to-indigo-800 text-white p-8 sm:p-10 hover:shadow-xl transition-all">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_90%_10%,rgba(255,255,255,0.15),transparent_55%)]" />
          <div className="relative z-10 sm:flex items-center justify-between gap-6">
            <div>
              <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/15 border border-white/20 text-sm font-medium mb-4">
                🧠 Quiz gratuit
              </span>
              <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">Connais-tu tes droits ?</h2>
              <p className="text-indigo-100 mt-3 max-w-xl leading-relaxed">
                8 situations du quotidien en Belgique. Chaque réponse est expliquée et renvoie vers une fiche sourcée.
                Aucun piège — juste de quoi apprendre en 3 minutes.
              </p>
            </div>
            <span className="mt-6 sm:mt-0 flex-shrink-0 inline-flex items-center gap-2 rounded-2xl bg-white text-indigo-700 font-semibold px-6 py-3.5 group-hover:translate-x-1 transition-transform">
              Commencer le quiz →
            </span>
          </div>
        </Link>
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
        <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2">
          <Link href="/loi-avec-moi/nos-assistants" className="text-indigo-700 hover:text-indigo-900 font-medium">Qui sont nos assistants ?</Link>
          <Link href="/la-loi-avec-moi-france" className="text-indigo-700 hover:text-indigo-900 font-medium">🇫🇷 Voir la version France →</Link>
          <Link href="/" className="hover:text-slate-900">← Accueil Caelum</Link>
        </div>
      </footer>
    </main>
  );
}
