"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

// Wonen & huur (België) — Nederlandstalige fiche.
// Belgische huurregels (gewestelijk). Feiten gespiegeld op de reeds geverifieerde
// Franstalige fiche, met officiële Nederlandstalige bronnen.

const fiches = [
  {
    title: "De huurwaarborg is geplafonneerd",
    text: "Op een geblokkeerde rekening op uw naam mag de waarborg niet meer dan 2 maanden huur bedragen (in alle gewesten). Onder de vorm van een bankwaarborg kan dat oplopen tot 3 maanden.",
    ref: "Vlaanderen.be — huren en verhuren",
    url: "https://www.vlaanderen.be/wonen-en-energie/huren-en-verhuren",
  },
  {
    title: "De waarborg moet u terugbetaald worden",
    text: "Op het einde van de huur moet de verhuurder uw waarborg vrijgeven. Gebeurt dat niet, dan kan u dit opeisen; laattijdige terugbetaling kan een vergoeding meebrengen.",
    ref: "Belgium.be — huisvesting",
    url: "https://www.belgium.be/nl/huisvesting",
  },
  {
    title: "Een plaatsbeschrijving beschermt u",
    text: "De plaatsbeschrijving bij intrede (en bij uittrede) legt de staat van de woning vast. Zonder plaatsbeschrijving is het voor de verhuurder zeer moeilijk om u schade aan te rekenen.",
    ref: "Vlaanderen.be — plaatsbeschrijving",
    url: "https://www.vlaanderen.be/wonen-en-energie/huren-en-verhuren",
  },
  {
    title: "U kan opzeggen met een opzegtermijn",
    text: "Bij een huurovereenkomst van 9 jaar kan de huurder op elk moment opzeggen met een opzegtermijn van 3 maanden (de eerste jaren kan een vergoeding verschuldigd zijn).",
    ref: "Vlaanderen.be — opzeg van de huur",
    url: "https://www.vlaanderen.be/wonen-en-energie/huren-en-verhuren",
  },
  {
    title: "De huur wordt maar één keer per jaar geïndexeerd",
    text: "De verhuurder mag de huurprijs maximaal één keer per jaar indexeren, op de verjaardag van de overeenkomst, en alleen als het contract dat schriftelijk voorziet.",
    ref: "Belgium.be — huisvesting",
    url: "https://www.belgium.be/nl/huisvesting",
  },
  {
    title: "Grote herstellingen zijn voor de verhuurder",
    text: "Het gewone onderhoud is voor u; de grote herstellingen (dak, verwarming, ouderdom) zijn voor rekening van de verhuurder.",
    ref: "Vlaanderen.be — huren en verhuren",
    url: "https://www.vlaanderen.be/wonen-en-energie/huren-en-verhuren",
  },
];

const readText = `Uw rechten als huurder. ${fiches.map((f) => f.title + ". " + f.text).join(" ")}`;

export default function WonenPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/de-wet-met-mij" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">De wet met mij</span>
          </Link>
          <Link href="/de-wet-met-mij/werk" className="text-sm font-semibold text-emerald-700 hover:text-emerald-900">
            Rechten op het werk →
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-emerald-100 text-sm font-medium mb-6">
            Wonen & huur
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Uw rechten als huurder</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Waarborg, plaatsbeschrijving, opzeg, herstellingen: wat de wet voorziet, eenvoudig uitgelegd —
            met de officiële bron om indien nodig te tonen.
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
            ⚖️ De huurwetgeving is <strong>geregionaliseerd</strong> in België: de regels verschillen lichtjes
            tussen Brussel, Wallonië en Vlaanderen. Deze fiches geven de grote principes. Laat u bij een
            geschil bijstaan (advocaat, juridische bijstand of een woondienst van uw gewest).
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/de-wet-met-mij" className="hover:text-slate-900">← Terug naar « De wet met mij »</Link>
      </footer>
    </main>
  );
}
