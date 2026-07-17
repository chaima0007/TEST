"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { NL_THEMES } from "@/data/nl/fiches";

// Zoekpagina voor « De wet met mij » (NL).
// Doorzoekt ALLE fiches uit één bron (data/nl/fiches.ts) — geen duplicatie.
// Tolerant voor accenten en hoofdletters; toont het thema en linkt naar de fiche.

type Treffer = {
  themaSlug: string;
  themaTitel: string;
  emoji: string;
  title: string;
  text: string;
  ref: string;
  url: string;
};

const ALLE: Treffer[] = NL_THEMES.flatMap((t) =>
  t.fiches.map((f) => ({
    themaSlug: t.slug,
    themaTitel: t.titel,
    emoji: t.emoji,
    title: f.title,
    text: f.text,
    ref: f.ref,
    url: f.url,
  }))
);

function normaliseer(s: string): string {
  return s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

export default function ZoekenPage() {
  const [q, setQ] = useState("");

  const resultaten = useMemo(() => {
    const termen = normaliseer(q).split(/\s+/).filter(Boolean);
    if (termen.length === 0) return ALLE;
    return ALLE.filter((r) => {
      const hooiberg = normaliseer(`${r.title} ${r.text} ${r.ref} ${r.themaTitel}`);
      return termen.every((term) => hooiberg.includes(term));
    });
  }, [q]);

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/de-wet-met-mij" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">De wet met mij</span>
          </Link>
          <Link href="/de-wet-met-mij" className="text-sm font-semibold text-emerald-700 hover:text-emerald-900">
            ← Alle onderwerpen
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-950 to-slate-900 text-white py-16 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight leading-tight">Zoek in al uw rechten</h1>
          <p className="text-base text-slate-300 mt-4 leading-relaxed">
            Typ een woord (bv. « huurwaarborg », « ontslag », « onderhoudsgeld ») en vind meteen het juiste antwoord,
            met de officiële bron erbij.
          </p>
          <div className="mt-6">
            <input
              type="search"
              autoFocus
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Waarover heeft u een vraag?"
              aria-label="Zoek in de fiches"
              className="w-full max-w-xl mx-auto block rounded-xl border border-white/20 bg-white/95 text-slate-900 px-5 py-3.5 text-base shadow-lg outline-none focus:ring-2 focus:ring-emerald-400"
            />
          </div>
        </div>
      </section>

      <section className="py-10 px-6 max-w-3xl mx-auto">
        <p className="text-sm text-slate-500 mb-5" aria-live="polite">
          {resultaten.length} resultaat{resultaten.length === 1 ? "" : "en"}
          {q.trim() ? <> voor « {q.trim()} »</> : null}
        </p>

        {resultaten.length === 0 ? (
          <div className="rounded-2xl border border-slate-200 p-8 text-center text-slate-600">
            <p>Geen resultaat. Probeer een ander woord of bekijk{" "}
              <Link href="/de-wet-met-mij" className="text-emerald-700 font-semibold hover:underline">alle onderwerpen</Link>.
            </p>
          </div>
        ) : (
          <ul className="space-y-4">
            {resultaten.map((r, i) => (
              <li key={`${r.themaSlug}-${i}`} className="rounded-2xl border border-slate-200 p-5 hover:border-emerald-300 transition-colors">
                <Link href={`/de-wet-met-mij/${r.themaSlug}`} className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-700 hover:text-emerald-900">
                  <span>{r.emoji}</span> {r.themaTitel} →
                </Link>
                <h2 className="text-lg font-bold tracking-tight mt-2">{r.title}</h2>
                <p className="text-slate-700 text-sm mt-1.5 leading-relaxed">{r.text}</p>
                <a href={r.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-700 mt-3 bg-emerald-50 border border-emerald-200 hover:bg-emerald-100 rounded-lg px-3 py-2 transition-colors">
                  🔗 Officiële bron: {r.ref}
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
                </a>
              </li>
            ))}
          </ul>
        )}
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/de-wet-met-mij" className="hover:text-slate-900">← Terug naar « De wet met mij »</Link>
      </footer>
    </main>
  );
}
