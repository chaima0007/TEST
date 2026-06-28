"use client";

import Link from "next/link";
import { useState } from "react";

// Page « Veille réglementaire » — newsletter (Caelum, ENTREPRISES, séparé de La Loi Avec Moi).
// Canal possédé : à la fois produit (l'abonné reste informé) et marketing (on reste dans sa boîte mail).
// Réutilise /api/leads (sans credential, transmission via webhook env LEADS_WEBHOOK_URL).

const avantages = [
  "Une alerte dès qu'une norme qui vous concerne change.",
  "En clair : ce que ça change pour VOUS, et l'échéance.",
  "Les sources officielles, toujours citées et datées.",
  "Zéro spam : uniquement ce qui compte, quand ça compte.",
];

export default function VeillePage() {
  const [email, setEmail] = useState("");
  const [envoi, setEnvoi] = useState<"idle" | "envoi" | "ok" | "erreur">("idle");

  async function sabonner() {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      setEnvoi("erreur");
      return;
    }
    setEnvoi("envoi");
    try {
      const r = await fetch("/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim(), source: "newsletter-veille" }),
      });
      const data = await r.json();
      setEnvoi(data.ok ? "ok" : "erreur");
    } catch {
      setEnvoi("erreur");
    }
  }

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link href="/conformite" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">
            Les normes 2026 →
          </Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-2xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Veille réglementaire — gratuit
          </span>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
            Ne ratez plus jamais
            <span className="block bg-gradient-to-r from-indigo-300 to-sky-300 bg-clip-text text-transparent">
              un changement de loi
            </span>
          </h1>
          <p className="text-lg text-slate-300 mt-6 leading-relaxed">
            On surveille les normes des entreprises (e-facturation, NIS2, RGPD, CSRD/CSDDD, lanceurs d&apos;alerte)
            et on vous prévient, en clair, dès que quelque chose vous concerne.
          </p>

          {/* Formulaire */}
          <div className="mt-8 max-w-md mx-auto">
            {envoi === "ok" ? (
              <p className="rounded-xl bg-emerald-500/15 border border-emerald-400/30 text-emerald-200 px-4 py-3 font-semibold">
                ✅ Inscription reçue ! Vous serez prévenu·e dès qu&apos;une norme bouge.
              </p>
            ) : (
              <>
                <div className="flex flex-col sm:flex-row gap-3">
                  <label htmlFor="veille-email" className="sr-only">
                    Votre adresse e-mail
                  </label>
                  <input
                    id="veille-email"
                    type="email"
                    value={email}
                    onChange={(e) => {
                      setEmail(e.target.value);
                      if (envoi === "erreur") setEnvoi("idle");
                    }}
                    placeholder="vous@entreprise.be"
                    className="flex-1 rounded-xl border border-white/20 bg-white/10 text-white placeholder:text-slate-400 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-indigo-400"
                  />
                  <button
                    type="button"
                    onClick={sabonner}
                    disabled={envoi === "envoi"}
                    className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white font-semibold px-6 py-3 rounded-xl transition-colors whitespace-nowrap"
                  >
                    {envoi === "envoi" ? "Inscription…" : "M'abonner"}
                  </button>
                </div>
                {envoi === "erreur" && (
                  <p className="text-sm text-red-300 mt-2 text-left">Vérifiez votre adresse e-mail et réessayez.</p>
                )}
                <p className="text-xs text-slate-400 mt-3">
                  Gratuit · désinscription en un clic · vos données ne sont jamais partagées.
                </p>
              </>
            )}
          </div>
        </div>
      </section>

      <section className="max-w-3xl mx-auto px-6 py-14">
        <ul className="grid sm:grid-cols-2 gap-4">
          {avantages.map((a) => (
            <li key={a} className="flex items-start gap-3 rounded-xl border border-slate-200 p-4">
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5">
                <path
                  fillRule="evenodd"
                  d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4L8.5 12l6.8-6.8a1 1 0 011.4 0z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="text-slate-700 text-sm">{a}</span>
            </li>
          ))}
        </ul>

        <div className="mt-10 rounded-2xl border border-slate-200 p-6 text-center">
          <p className="text-slate-700">
            Besoin d&apos;aller plus loin que l&apos;info ?{" "}
            <Link href="/offres-conformite" className="font-semibold text-indigo-700 hover:text-indigo-900">
              Découvrez nos offres de mise en conformité →
            </Link>
          </p>
        </div>
      </section>
    </main>
  );
}
