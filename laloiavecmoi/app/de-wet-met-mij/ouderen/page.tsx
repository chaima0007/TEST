"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

// Bescherming van ouderen — ouderenmis(be)handeling (Vlaanderen) — Nederlandstalige fiche.
// Feiten gespiegeld op de reeds geverifieerde Franstalige fiche (maltraitance_aines.json),
// met officiële Vlaamse bronnen (Vlaanderen.be, hulplijn 1712, VLOCO).

const fiches = [
  {
    title: "Wat is ouderenmis(be)handeling?",
    text: "Het gaat om elke vorm van geweld of verwaarlozing tegenover een oudere persoon: lichamelijk, psychisch, seksueel, maar ook financieel geweld of verwaarlozing (verkeerde medicatie, geen schone kleren, onvoldoende verzorging). Misbruik van iemands kwetsbare toestand is strafbaar.",
    ref: "Strafwetboek — misbruik van de zwakke toestand (art. 442quater) en geweldsmisdrijven",
    url: "https://www.vlaanderen.be/gezondheid-en-welzijn/conflicten-en-misdrijven/hulp-en-melding/geweld-en-misbruik-bij-ouderen",
  },
  {
    title: "U bent (of ziet) een mishandelde oudere: wie bellen?",
    text: "Bij mishandeling thuis kunt u — net als familie of vrienden — gratis bellen naar 1712, de hulplijn voor geweld, misbruik en kindermishandeling. Gaat het om mishandeling in een woonzorgcentrum, dan kunt u terecht bij de Woonzorglijn. De hulp is gratis en anoniem.",
    ref: "Vlaanderen.be — geweld en misbruik bij ouderen (hulplijn 1712, Woonzorglijn)",
    url: "https://www.vlaanderen.be/gezondheid-en-welzijn/conflicten-en-misdrijven/hulp-en-melding/geweld-en-misbruik-bij-ouderen",
  },
  {
    title: "Financieel misbruik telt ook mee",
    text: "Een veelvoorkomende vorm bij ouderen is financieel misbruik: geld of bezittingen afnemen, misbruik van een volmacht of bankkaart, druk uitoefenen om documenten te tekenen. Ook daarvoor kunt u terecht bij 1712 om uw situatie te bespreken.",
    ref: "Hulplijn 1712 — ouderenmis(be)handeling (incl. financieel geweld)",
    url: "https://www.1712.be/nl/soorten-geweld/ouderenmisbehandeling",
  },
  {
    title: "Professionals: contacteer VLOCO",
    text: "Komt u beroepsmatig in contact met ouderen en vermoedt u mis(be)handeling, dan kunt u terecht bij het Vlaams Ondersteuningscentrum Ouderenmis(be)handeling (VLOCO), het aanspreekpunt voor professionals. Iedereen — buur, familie, zorgverlener — kan een verschil maken door het gesprek aan te durven gaan.",
    ref: "Hulplijn 1712 — doorverwijzing naar VLOCO (vloco.be)",
    url: "https://www.1712.be/nl/soorten-geweld/ouderenmisbehandeling",
  },
];

const readText = `Bescherming van ouderen. ${fiches.map((f) => f.title + ". " + f.text).join(" ")}`;

export default function OuderenPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/de-wet-met-mij" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">De wet met mij</span>
          </Link>
          <Link href="/de-wet-met-mij/geweld" className="text-sm font-semibold text-emerald-700 hover:text-emerald-900">
            Geweld & slachtofferhulp →
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-emerald-100 text-sm font-medium mb-6">
            Bescherming van ouderen
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Ouderen beschermen tegen mishandeling</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Herkennen, wie bellen, financieel misbruik en hulp voor professionals:
            duidelijk uitgelegd — met de officiële bron erbij.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Alles voorlezen" lang="nl-BE" />
          </div>
        </div>
      </section>

      <section className="px-6 max-w-3xl mx-auto -mt-8 relative z-10">
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-5 shadow-sm">
          <p className="text-rose-900 text-sm leading-relaxed">
            🆘 <strong>In gevaar?</strong> Bel de <strong>politie 101</strong> of de <strong>noodcentrale 112</strong>.
            Voor advies en een luisterend oor: <strong>1712</strong> (gratis, anoniem) — ook voor familie en getuigen.
          </p>
        </div>
      </section>

      <section className="py-12 px-6 max-w-3xl mx-auto space-y-5">
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
            ⚖️ Deze fiches geven algemene informatie en vervangen geen persoonlijk juridisch advies. Een oudere persoon
            heeft <strong>altijd</strong> recht op respect en veiligheid. Twijfel niet om het gesprek aan te gaan of 1712
            te bellen — ook bij een vermoeden.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/de-wet-met-mij" className="hover:text-slate-900">← Terug naar « De wet met mij »</Link>
      </footer>
    </main>
  );
}
