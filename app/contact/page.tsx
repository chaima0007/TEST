"use client";

import Link from "next/link";
import { useState } from "react";

const BESOINS = ["Site web", "Tableau de bord", "Automatisation", "Je ne sais pas encore"];

export default function ContactPage() {
  const [form, setForm] = useState({ name: "", email: "", company: "", tier: "", message: "" });
  const [status, setStatus] = useState<"idle" | "sending" | "ok" | "error">("idle");
  const [error, setError] = useState("");

  function update(field: string, value: string) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("sending");
    setError("");
    try {
      const res = await fetch("/api/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (res.ok && data.ok) {
        setStatus("ok");
      } else {
        setStatus("error");
        setError(data.error ?? "Une erreur est survenue.");
      }
    } catch {
      setStatus("error");
      setError("Impossible d'envoyer pour le moment. Veuillez réessayer.");
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-white text-slate-900">
      {/* Header */}
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-violet-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link href="/" className="text-sm text-slate-500 hover:text-slate-900">← Retour</Link>
        </div>
      </header>

      <div className="max-w-2xl mx-auto px-6 py-16">
        <div className="text-center mb-10">
          <span className="inline-block px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-xs font-medium mb-4">
            Premier échange sans engagement
          </span>
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight">Parlons de votre projet</h1>
          <p className="text-slate-500 mt-3">
            Site web, tableau de bord ou automatisation : laissez vos coordonnées,
            nous vous recontactons sous 24h pour en discuter et vous proposer un devis clair.
          </p>
        </div>

        {status === "ok" ? (
          <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-8 text-center">
            <div className="text-4xl mb-3">✅</div>
            <h2 className="text-xl font-semibold text-emerald-800">Merci {form.name.split(" ")[0]} !</h2>
            <p className="text-emerald-700 mt-2">
              Votre demande est bien enregistrée. Nous revenons vers vous très vite à {form.email}.
            </p>
            <Link href="/" className="inline-block mt-6 text-sm text-emerald-700 underline">Retour à l&apos;accueil</Link>
          </div>
        ) : (
          <form onSubmit={submit} className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div className="grid sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium mb-1.5">Nom *</label>
                <input required value={form.name} onChange={(e) => update("name", e.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Votre nom" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1.5">Email *</label>
                <input required type="email" value={form.email} onChange={(e) => update("email", e.target.value)}
                  className="w-full rounded-lg border border-slate-300 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="votre@email.com" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1.5">Organisation</label>
              <input value={form.company} onChange={(e) => update("company", e.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Votre entreprise (facultatif)" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1.5">Votre besoin</label>
              <select value={form.tier} onChange={(e) => update("tier", e.target.value)}
                className="w-full rounded-lg border border-slate-300 px-3 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="">— Sélectionnez —</option>
                {BESOINS.map((t) => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1.5">Message</label>
              <textarea value={form.message} onChange={(e) => update("message", e.target.value)} rows={4}
                className="w-full rounded-lg border border-slate-300 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Décrivez votre projet en quelques mots…" />
            </div>

            {status === "error" && (
              <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">{error}</p>
            )}

            <button type="submit" disabled={status === "sending"}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-medium rounded-lg px-4 py-3 transition-colors">
              {status === "sending" ? "Envoi…" : "Envoyer ma demande"}
            </button>
            <p className="text-xs text-slate-400 text-center">
              Pas de spam. Vos données restent confidentielles (RGPD).
            </p>
          </form>
        )}
      </div>
    </main>
  );
}
