"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

// Administratieve stappen (België) — Nederlandstalige fiche.
// Feiten gespiegeld op de geverifieerde Franstalige fiche (wet 29 juli 1991, Raad van State).
// Bronnen in het NL: Belgium.be, Federale Ombudsman, Raad van State, BOSA.

const fiches = [
  {
    title: "Een beslissing van de administratie moet gemotiveerd zijn",
    text: "Sinds de wet van 29 juli 1991 moet elke individuele administratieve handeling « formeel gemotiveerd » worden: de beslissing moet de feitelijke en juridische redenen vermelden. Legt een beslissing niets uit, dan is dat al een argument in uw voordeel.",
    ref: "BOSA — wet van 29 juli 1991",
    url: "https://bosa.belgium.be/nl",
  },
  {
    title: "De brief moet zeggen hoe en binnen welke termijn u kan reageren",
    text: "Wanneer de administratie u een beslissing betekent waartegen beroep mogelijk is, moet ze de beroepsmogelijkheid, de termijn en de vorm vermelden. Lees steeds de onderkant van de brief: daar staan vaak uw beroepsmogelijkheden. Ontbreken die vermeldingen, dan is de termijn mogelijk niet tegenstelbaar.",
    ref: "Belgium.be — administratie",
    url: "https://www.belgium.be/nl",
  },
  {
    title: "De termijnen zijn kort: noteer de datum van kennisgeving",
    text: "In administratieve zaken lopen de termijnen meestal vanaf de dag na de kennisgeving. Voor een annulatieberoep bij de Raad van State bedraagt de termijn 60 dagen. Noteer onmiddellijk de ontvangstdatum en wacht niet: een overschreden termijn sluit de deur vaak definitief.",
    ref: "Raad van State — procedure",
    url: "https://www.raadvst-consetat.be/",
  },
  {
    title: "Het administratief beroep (gratis) vóór de rechter",
    text: "Vóór u naar een rechtbank stapt, kunnen veel beslissingen worden aangevochten via een administratief beroep: u vraagt de administratie (of een hogere instantie) haar beslissing te herzien. Dat is gratis, schriftelijk, en lost het probleem vaak op zonder proces. Respecteer de vorm en de termijn vermeld op de beslissing.",
    ref: "Belgium.be — administratie",
    url: "https://www.belgium.be/nl",
  },
  {
    title: "De federale Ombudsman: gratis, en hij « bevriest » uw termijn",
    text: "Bij een geschil met een federale administratie kan u zich gratis tot de federale Ombudsman wenden. Groot voordeel: zijn tussenkomst schorst de beroepstermijn bij de Raad van State voor maximaal 4 maanden. Mislukt de bemiddeling, dan rest u dus nog tijd. (Gewesten en gemeenten hebben ook hun ombudsmannen.)",
    ref: "Federale Ombudsman",
    url: "https://www.federaalombudsman.be/nl",
  },
];

const readText = `Administratieve stappen. ${fiches.map((f) => f.title + ". " + f.text).join(" ")}`;

export default function AdministratiePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/de-wet-met-mij" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-emerald-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">W</span>
            </div>
            <span className="font-bold text-lg tracking-tight">De wet met mij</span>
          </Link>
          <Link href="/de-wet-met-mij/juridische-hulp" className="text-sm font-semibold text-emerald-700 hover:text-emerald-900">
            Juridische hulp →
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-emerald-100 text-sm font-medium mb-6">
            Administratieve stappen
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Beslissing van de administratie?</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Motivering, termijnen, gratis beroep, ombudsman: wat de wet voorziet, eenvoudig uitgelegd —
            met de officiële bron.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Alles voorlezen" lang="nl-BE" />
          </div>
        </div>
      </section>

      <section className="py-16 px-6 max-w-3xl mx-auto space-y-5">
        {fiches.map((f, i) => (
          <div key={i} className="rounded-2xl border border-slate-200 p-6">
            <div className="flex items-start gap-3">
              <span className="flex-shrink-0 w-7 h-7 rounded-full bg-emerald-600 text-white text-sm font-bold flex items-center justify-center mt-0.5">{i + 1}</span>
              <div>
                <h2 className="text-lg font-bold tracking-tight">{f.title}</h2>
                <p className="text-slate-700 text-sm mt-2 leading-relaxed">{f.text}</p>
                <a href={f.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-700 mt-3 bg-emerald-50 border border-emerald-200 hover:bg-emerald-100 rounded-lg px-3 py-2 transition-colors">
                  🔗 Officiële bron: {f.ref}
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
                </a>
              </div>
            </div>
          </div>
        ))}
      </section>

      <section className="pb-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Lees de beslissing volledig — vooral de onderkant (datum, motieven, beroepsmogelijkheden).
            Markeer de uiterste datum en handel snel. Bij twijfel: de federale Ombudsman (gratis) of een advocaat.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/de-wet-met-mij" className="hover:text-slate-900">← Terug naar « De wet met mij »</Link>
      </footer>
    </main>
  );
}
