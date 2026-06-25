"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

const niveaux = [
  {
    t: "L'État fédéral",
    color: "indigo",
    d: "Il gère ce qui concerne tout le pays : la justice, la police fédérale, l'armée, la sécurité sociale (pensions, chômage, soins de santé de base), les finances publiques, les affaires étrangères et l'intérieur.",
    pour: "Carte d'identité, pension, sécurité sociale, justice, impôts fédéraux.",
    ref: "Belgium.be — compétences fédérales",
    url: "https://www.belgium.be/fr/la_belgique/pouvoirs_publics/autorites_federales/competences_de_letat_federal",
  },
  {
    t: "Les Régions (3)",
    color: "emerald",
    d: "Flandre, Wallonie et Bruxelles-Capitale. Elles gèrent ce qui est lié au territoire : économie, emploi, logement, environnement, aménagement du territoire, transport, énergie.",
    pour: "Bail et logement, aides à l'emploi, primes, permis d'urbanisme, environnement.",
    ref: "Belgium.be — compétences des Régions",
    url: "https://www.belgium.be/fr/la_belgique/pouvoirs_publics/la_belgique_federale/competences/regions",
  },
  {
    t: "Les Communautés (3)",
    color: "rose",
    d: "Communauté française, flamande et germanophone. Elles gèrent ce qui est lié aux personnes et à la langue : l'enseignement, la culture, l'aide à la jeunesse, une partie de la santé.",
    pour: "École et enseignement, aide à la jeunesse, culture, langue.",
    ref: "Belgium.be — compétences des Communautés",
    url: "https://www.belgium.be/fr/la_belgique/pouvoirs_publics/la_belgique_federale/competences/communautes",
  },
];

const langues = [
  {
    region: "Flandre (Nord)",
    langue: "Néerlandais",
    note: "Région flamande. Les démarches régionales et l'enseignement se font en néerlandais.",
  },
  {
    region: "Wallonie (Sud)",
    langue: "Français",
    note: "Région wallonne. La plupart des démarches se font en français (sauf les communes germanophones de l'Est).",
  },
  {
    region: "Bruxelles-Capitale",
    langue: "Français & néerlandais",
    note: "Région officiellement bilingue : vous pouvez être servi dans les deux langues.",
  },
  {
    region: "Cantons de l'Est",
    langue: "Allemand",
    note: "Communauté germanophone (région d'Eupen). 3ᵉ langue officielle du pays.",
  },
];

const readText = `Comprendre la Belgique. La Belgique est un État fédéral à plusieurs niveaux de pouvoir. ${niveaux
  .map((n) => n.t + ". " + n.d + " Pour vous : " + n.pour)
  .join(" ")} Trois langues officielles : le néerlandais, le français et l'allemand. Savoir quel niveau gère quoi, c'est savoir où vous adresser.`;

const colorMap: Record<string, string> = {
  indigo: "border-indigo-200 bg-indigo-50 text-indigo-700",
  emerald: "border-emerald-200 bg-emerald-50 text-emerald-700",
  rose: "border-rose-200 bg-rose-50 text-rose-700",
};

export default function ComprendreLaBelgiquePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">L</span>
            </div>
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Comprendre le système belge
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Qui décide quoi en Belgique ?</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            La Belgique a plusieurs niveaux de pouvoir. Savoir lequel gère quoi, c&apos;est savoir
            <strong className="text-white"> où s&apos;adresser</strong> — et arrêter de se perdre entre les guichets.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Les niveaux de pouvoir */}
      <section className="py-16 px-6 max-w-5xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight text-center">Les trois niveaux, simplement</h2>
        <p className="text-slate-500 mt-3 text-center max-w-2xl mx-auto">
          Ils sont juridiquement égaux : aucun n&apos;est « au-dessus » de l&apos;autre. Chacun a ses domaines.
        </p>
        <div className="grid lg:grid-cols-3 gap-6 mt-10">
          {niveaux.map((n) => (
            <div key={n.t} className="rounded-2xl border border-slate-200 p-6 flex flex-col">
              <span className={`self-start text-xs font-bold uppercase tracking-wide rounded-full border px-3 py-1 ${colorMap[n.color]}`}>
                {n.t}
              </span>
              <p className="text-slate-700 text-sm mt-4 leading-relaxed flex-1">{n.d}</p>
              <div className="mt-4 rounded-xl bg-slate-50 border border-slate-100 p-3">
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">Pour vous, c&apos;est</p>
                <p className="text-sm text-slate-800 mt-1">{n.pour}</p>
              </div>
              <a href={n.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-xs font-medium text-indigo-700 mt-4 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-3 py-2 transition-colors">
                🔗 {n.ref}
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
              </a>
            </div>
          ))}
        </div>
      </section>

      {/* Langues & régions */}
      <section className="py-14 px-6 bg-slate-50">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight text-center">Les langues selon où vous êtes</h2>
          <p className="text-slate-500 mt-3 text-center max-w-2xl mx-auto">
            La Belgique a <strong>trois langues officielles</strong>. La langue de vos démarches dépend de la région.
          </p>
          <div className="grid sm:grid-cols-2 gap-5 mt-10">
            {langues.map((l) => (
              <div key={l.region} className="bg-white rounded-2xl border border-slate-200 p-5">
                <div className="flex items-center justify-between">
                  <h3 className="font-bold tracking-tight">{l.region}</h3>
                  <span className="text-xs font-semibold text-indigo-700 bg-indigo-50 border border-indigo-200 rounded-full px-3 py-1">{l.langue}</span>
                </div>
                <p className="text-slate-600 text-sm mt-2.5 leading-relaxed">{l.note}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Le réflexe utile */}
      <section className="py-16 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl bg-indigo-50 border border-indigo-100 p-6">
          <h3 className="font-bold text-indigo-900 tracking-tight">💡 Le réflexe qui fait gagner du temps</h3>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Avant une démarche, posez-vous : <strong>est-ce une question de territoire ou de personne ?</strong>
          </p>
          <ul className="mt-3 space-y-1.5 text-sm text-indigo-900/80">
            <li>• Logement, emploi, environnement → <strong>votre Région</strong></li>
            <li>• École, culture, aide à la jeunesse → <strong>votre Communauté</strong></li>
            <li>• Carte d&apos;identité, justice, pension, sécurité sociale → <strong>le Fédéral</strong></li>
          </ul>
        </div>
      </section>

      {/* Sources + disclaimer */}
      <section className="pb-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Présentation simplifiée de la structure de l&apos;État belge, d&apos;après les sources officielles
            (Belgium.be — le portail de l&apos;État fédéral). La répartition exacte des compétences est détaillée
            sur les liens officiels ci-dessus. Pour une démarche précise, adressez-vous au service compétent.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
