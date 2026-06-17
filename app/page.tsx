"use client";

import Link from "next/link";
import { useState, useEffect, useRef } from "react";

const navLinks = [
  { label: "Produit", href: "#features" },
  { label: "Solutions", href: "#pricing" },
  { label: "Cas clients", href: "#trusted" },
  { label: "Entreprise", href: "#stats" },
  { label: "Investisseurs", href: "/pitch" },
];

const offers = [
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418" />
      </svg>
    ),
    title: "Intelligence 360°",
    desc: "Surveillance totale de votre marché : concurrents, pricing, M&A, recrutements, brevets. Rapport hebdomadaire livré à votre équipe dirigeante.",
    color: "from-blue-500/10 to-blue-600/5",
    accent: "text-blue-600",
    border: "border-blue-100",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0M3.124 7.5A8.969 8.969 0 0 1 5.292 3m13.416 0a8.969 8.969 0 0 1 2.168 4.5" />
      </svg>
    ),
    title: "Alerte Décisionnelle",
    desc: "Notification immédiate des signaux critiques. Votre équipe réagit avant le marché. Zéro information manquée.",
    color: "from-violet-500/10 to-violet-600/5",
    accent: "text-violet-600",
    border: "border-violet-100",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
      </svg>
    ),
    title: "Rapport Exécutif Mensuel",
    desc: "Analyse stratégique clé en main produite par notre moteur IA et validée par nos analystes. Présentable en CODIR.",
    color: "from-emerald-500/10 to-emerald-600/5",
    accent: "text-emerald-600",
    border: "border-emerald-100",
  },
];

const plans = [
  {
    name: "Offre Essentiel",
    desc: "Pour les équipes qui démarrent leur veille stratégique.",
    features: [
      "Surveillance des concurrents clés",
      "Alertes email hebdomadaires",
      "Rapport mensuel exécutif",
      "Tableau de bord direction",
      "Support dédié",
      "Conformité RGPD",
      "Export PDF & PowerPoint",
    ],
    popular: false,
    cta: "Demander un devis",
  },
  {
    name: "Offre Performance",
    desc: "Pour les directions qui veulent l'avantage compétitif.",
    features: [
      "Surveillance marché étendue",
      "Alertes temps réel multicanal",
      "Rapports CODIR illimités",
      "API & intégrations SI",
      "Analyse prédictive IA",
      "Support prioritaire 24/7",
      "CSM dédié",
      "SLA 99,8% garanti",
    ],
    popular: true,
    cta: "Prendre contact",
  },
  {
    name: "Offre Stratégique",
    desc: "Pour les Grands Comptes et groupes internationaux.",
    features: [
      "Périmètre marché illimité",
      "Alertes décisionnelles personnalisées",
      "Rapports sur mesure & co-construits",
      "Support dédié 24/7 — SLA 4h",
      "SSO & SAML / ISO 27001",
      "Onboarding guidé par nos experts",
      "Accès analystes stratégiques",
      "Multi-entités & consolidation groupe",
      "Revues trimestrielles direction",
    ],
    popular: false,
    cta: "Demander un devis",
  },
];

const stats = [
  { value: "350+", label: "ETI & Grands Comptes" },
  { value: "99,8%", label: "Disponibilité SLA" },
  { value: "< 2h", label: "Mise en place" },
  { value: "4,8x", label: "ROI moyen documenté" },
];

const clientLogos = [
  "Groupe Legrand",
  "Schneider Digital",
  "BNP Paribas AM",
  "TotalEnergies",
  "Sopra Steria",
  "Capgemini",
];

function useCountUp(target: number, duration = 1500, start = false) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!start) return;
    let startTime: number | null = null;
    const step = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      setCount(Math.floor(progress * target));
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, [target, duration, start]);
  return count;
}

export default function Home() {
  const [scrolled, setScrolled] = useState(false);
  const [statsVisible, setStatsVisible] = useState(false);
  const statsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setStatsVisible(true); },
      { threshold: 0.3 }
    );
    if (statsRef.current) observer.observe(statsRef.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div className="min-h-screen bg-white text-slate-900 overflow-x-hidden">

      {/* ── Navigation ── */}
      <nav className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${scrolled ? "bg-white/95 backdrop-blur-md shadow-sm border-b border-slate-100" : "bg-transparent"}`}>
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg flex items-center justify-center shadow-sm">
              <span className="text-white text-xs font-black tracking-tight">IQ</span>
            </div>
            <span className="text-lg font-bold text-slate-900">CompeteIQ</span>
          </div>

          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((l) => (
              <a key={l.label} href={l.href}
                className="px-4 py-2 text-sm text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors font-medium">
                {l.label}
              </a>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <Link href="/login" className="hidden sm:block text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors px-3 py-2">
              Connexion
            </Link>
            <Link href="/contact"
              className="bg-slate-900 hover:bg-slate-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors shadow-sm">
              Demander une démonstration
            </Link>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden pt-16">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_60%_0%,rgba(30,64,175,0.2),transparent_65%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_10%_80%,rgba(15,23,42,0.8),transparent_60%)]" />
        {/* Subtle grid */}
        <div className="absolute inset-0 opacity-[0.03]"
          style={{ backgroundImage: "linear-gradient(rgba(255,255,255,.6) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.6) 1px,transparent 1px)", backgroundSize: "80px 80px" }} />

        <div className="relative max-w-7xl mx-auto px-6 text-center py-24">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 text-slate-300 text-xs font-semibold px-5 py-2 rounded-full mb-10 backdrop-blur-sm tracking-wide">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
            Partenaire stratégique de confiance depuis 2024
          </div>

          {/* Headline */}
          <h1 className="text-5xl md:text-7xl font-black text-white leading-[1.05] mb-8 tracking-tight max-w-5xl mx-auto">
            Votre avantage{" "}
            <span className="bg-gradient-to-r from-blue-300 via-slate-200 to-blue-200 bg-clip-text text-transparent">
              concurrentiel décisif
            </span>
          </h1>

          <p className="text-lg md:text-xl text-slate-400 mb-12 max-w-2xl mx-auto leading-relaxed font-light">
            Intelligence stratégique en temps réel pour les dirigeants, VP et équipes C-level
            qui prennent des décisions qui comptent. Un ROI documenté à 4,8x dès les 90 premiers jours.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-6">
            <Link href="/contact"
              className="inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 text-white text-base font-bold px-9 py-4 rounded-xl transition-all shadow-lg shadow-blue-900/40 hover:shadow-blue-700/50 hover:-translate-y-0.5">
              Demander une démonstration
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4"><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
            </Link>
            <Link href="/contact"
              className="inline-flex items-center justify-center gap-2 bg-white/5 hover:bg-white/10 border border-white/10 text-white text-base font-semibold px-9 py-4 rounded-xl transition-all backdrop-blur-sm">
              Parler à un expert
            </Link>
          </div>

          {/* Dashboard preview */}
          <div className="mt-20 relative max-w-5xl mx-auto">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-900/40 via-slate-700/20 to-blue-900/40 rounded-2xl blur-xl" />
            <div className="relative bg-slate-900 rounded-2xl border border-white/10 shadow-2xl overflow-hidden">
              {/* Window chrome */}
              <div className="flex items-center gap-2 px-5 py-3.5 bg-slate-800/80 border-b border-white/5">
                <div className="flex gap-1.5">
                  <div className="w-3 h-3 rounded-full bg-red-500/70" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500/70" />
                  <div className="w-3 h-3 rounded-full bg-green-500/70" />
                </div>
                <div className="flex-1 mx-4">
                  <div className="bg-slate-700/60 rounded-md px-3 py-1 text-xs text-slate-400 text-center w-fit mx-auto">
                    competeiq.io/dashboard — Intelligence stratégique
                  </div>
                </div>
              </div>
              {/* Dashboard UI */}
              <div className="p-6">
                {/* Stat row */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-5">
                  {[
                    { label: "Signaux détectés", value: "142", change: "+18 cette semaine", color: "text-blue-400", bg: "bg-blue-500/10" },
                    { label: "Alertes critiques", value: "7", change: "3 décisionnelles", color: "text-amber-400", bg: "bg-amber-500/10" },
                    { label: "Rapports CODIR", value: "12", change: "1 en attente", color: "text-emerald-400", bg: "bg-emerald-500/10" },
                    { label: "Score position", value: "81%", change: "+6pts ce mois", color: "text-violet-400", bg: "bg-violet-500/10" },
                  ].map((s) => (
                    <div key={s.label} className={`${s.bg} rounded-xl p-4 border border-white/5`}>
                      <p className="text-slate-500 text-xs mb-1">{s.label}</p>
                      <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
                      <p className="text-slate-600 text-xs mt-1">{s.change}</p>
                    </div>
                  ))}
                </div>
                {/* Market list */}
                <div className="space-y-2">
                  {[
                    { name: "Groupe Legrand", share: 78, status: "M&A détecté", sc: "bg-red-900/40 text-red-400", color: "#C41E3A" },
                    { name: "Schneider Digital", share: 61, status: "Recrutement stratégique", sc: "bg-amber-900/40 text-amber-400", color: "#3D8B37" },
                    { name: "Sopra Steria", share: 44, status: "Offre ajustée", sc: "bg-blue-900/40 text-blue-400", color: "#003087" },
                  ].map((c) => (
                    <div key={c.name} className="flex items-center gap-4 bg-slate-800/60 rounded-xl px-4 py-3 border border-white/5">
                      <div className="w-7 h-7 rounded-lg flex items-center justify-center text-white text-xs font-bold flex-shrink-0" style={{ backgroundColor: c.color }}>
                        {c.name[0]}
                      </div>
                      <span className="text-slate-200 text-sm font-medium w-36 flex-shrink-0">{c.name}</span>
                      <div className="flex-1 bg-slate-700/50 rounded-full h-1.5 hidden sm:block">
                        <div className="h-1.5 rounded-full bg-blue-500" style={{ width: `${c.share}%` }} />
                      </div>
                      <span className={`text-xs px-2.5 py-0.5 rounded-full font-medium flex-shrink-0 ${c.sc}`}>{c.status}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Clients de référence ── */}
      <section id="trusted" className="py-16 border-y border-slate-100 bg-slate-50">
        <div className="max-w-7xl mx-auto px-6">
          <p className="text-center text-sm font-semibold text-slate-400 uppercase tracking-widest mb-10">
            Ils nous font confiance
          </p>
          <div className="flex flex-wrap items-center justify-center gap-8 md:gap-16">
            {clientLogos.map((name) => (
              <div key={name} className="text-slate-400 font-bold text-base md:text-lg tracking-tight select-none hover:text-slate-600 transition-colors cursor-default">
                {name}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Stats ── */}
      <section id="stats" ref={statsRef} className="py-24 bg-slate-950 text-white overflow-hidden relative">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_80%_50%,rgba(30,64,175,0.15),transparent_70%)]" />
        <div className="relative max-w-7xl mx-auto px-6">
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-12 text-center">
            {stats.map((s) => (
              <div key={s.label} className="space-y-2">
                <p className="text-4xl md:text-5xl font-black tracking-tight text-white">{s.value}</p>
                <p className="text-slate-400 text-sm font-medium uppercase tracking-widest">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Offres ── */}
      <section id="features" className="py-28">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-20">
            <span className="text-slate-500 font-semibold text-xs uppercase tracking-widest">Nos offres</span>
            <h2 className="text-4xl md:text-5xl font-black mt-3 mb-5 text-slate-900 leading-tight">
              Intelligence stratégique<br className="hidden md:block" /> clé en main
            </h2>
            <p className="text-slate-500 text-lg max-w-xl mx-auto font-light">
              Trois offres conçues pour les dirigeants, les équipes de direction et les groupes internationaux.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {offers.map((f) => (
              <div key={f.title}
                className={`group relative bg-gradient-to-br ${f.color} border ${f.border} rounded-2xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300`}>
                <div className={`${f.accent} mb-6`}>{f.icon}</div>
                <h3 className="font-bold text-slate-900 text-xl mb-3">{f.title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Feature spotlight ── */}
      <section className="py-20 bg-slate-950 text-white overflow-hidden">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <span className="text-blue-400 font-semibold text-xs uppercase tracking-widest">Moteur analytique</span>
              <h2 className="text-4xl md:text-5xl font-black mt-3 mb-6 leading-tight">
                Des décisions<br />
                <span className="bg-gradient-to-r from-blue-300 to-slate-200 bg-clip-text text-transparent">
                  fondées sur les faits
                </span>
              </h2>
              <p className="text-slate-400 text-lg mb-8 leading-relaxed font-light">
                Notre moteur IA analyse des milliers de signaux chaque heure — modifications stratégiques, offres d&apos;emploi, brevets, mouvements M&A, avis clients — pour donner à votre direction une vision 360° du marché, sans bruit parasite.
              </p>
              <ul className="space-y-4 mb-10">
                {[
                  "Synthèses exécutives hebdomadaires prêtes à présenter",
                  "Anticipation des mouvements tarifaires et repositionnements",
                  "Détection de signaux faibles avant la presse spécialisée",
                  "Veille RH et recrutements stratégiques concurrents",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-3 text-slate-300 text-sm font-light">
                    <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5">
                      <path fillRule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.857-9.809a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z" clipRule="evenodd" />
                    </svg>
                    {item}
                  </li>
                ))}
              </ul>
              <Link href="/contact"
                className="inline-flex items-center gap-2 bg-white text-slate-900 hover:bg-slate-100 font-semibold px-7 py-3.5 rounded-xl transition-colors">
                Planifier une démonstration
                <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4"><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
              </Link>
            </div>
            {/* Right side visual — alert cards */}
            <div className="relative">
              <div className="absolute -inset-4 bg-gradient-to-r from-blue-900/20 to-slate-800/20 rounded-3xl blur-2xl" />
              <div className="relative bg-slate-900 rounded-2xl border border-white/10 p-6 space-y-3">
                {[
                  { icon: "M&A", title: "Signal M&A détecté", body: "Groupe Legrand a déposé une LOI confidentielle pour l'acquisition d'un concurrent direct en Allemagne.", time: "Il y a 1h", color: "border-red-500/30 bg-red-500/5", badge: "text-red-400" },
                  { icon: "RH", title: "Recrutement stratégique", body: "Schneider Digital recrute 12 ingénieurs IA spécialisés en pricing dynamique — repositionnement offre B2B probable.", time: "Il y a 4h", color: "border-amber-500/30 bg-amber-500/5", badge: "text-amber-400" },
                  { icon: "PX", title: "Ajustement tarifaire", body: "Sopra Steria a modifié sa grille Grands Comptes (+11%). Votre positionnement prix est désormais plus favorable.", time: "Hier", color: "border-blue-500/30 bg-blue-500/5", badge: "text-blue-400" },
                ].map((a) => (
                  <div key={a.title} className={`border ${a.color} rounded-xl p-4`}>
                    <div className="flex items-start gap-3">
                      <span className={`text-xs font-black px-2 py-1 rounded-md bg-white/5 ${a.badge} flex-shrink-0`}>{a.icon}</span>
                      <div className="flex-1 min-w-0">
                        <p className="text-white font-semibold text-sm">{a.title}</p>
                        <p className="text-slate-400 text-xs mt-0.5 leading-relaxed">{a.body}</p>
                      </div>
                      <span className="text-slate-600 text-xs flex-shrink-0 whitespace-nowrap">{a.time}</span>
                    </div>
                  </div>
                ))}
                <div className="text-center pt-2">
                  <span className="text-xs text-slate-600">+ 9 autres signaux en attente de validation</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Solutions (Pricing sans prix) ── */}
      <section id="pricing" className="py-28 bg-slate-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <span className="text-slate-500 font-semibold text-xs uppercase tracking-widest">Solutions</span>
            <h2 className="text-4xl md:text-5xl font-black mt-3 mb-4 text-slate-900">
              Une offre calibrée<br />à votre ambition
            </h2>
            <p className="text-slate-500 text-lg font-light">Tarifs sur devis — À partir de 990&nbsp;€/mois.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {plans.map((p) => (
              <div key={p.name} className={`relative rounded-2xl p-8 transition-all hover:shadow-xl ${
                p.popular
                  ? "bg-slate-900 text-white shadow-2xl ring-2 ring-blue-600"
                  : "bg-white border border-slate-200 hover:border-slate-300"
              }`}>
                {p.popular && (
                  <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-xs font-bold px-5 py-1 rounded-full shadow-lg tracking-wide">
                    Recommandée
                  </div>
                )}
                <h3 className={`font-bold text-xl mb-2 ${p.popular ? "text-white" : "text-slate-900"}`}>{p.name}</h3>
                <p className={`text-sm mb-8 font-light ${p.popular ? "text-slate-400" : "text-slate-500"}`}>{p.desc}</p>
                <ul className="space-y-3 mb-10">
                  {p.features.map((f) => (
                    <li key={f} className={`flex items-start gap-2.5 text-sm ${p.popular ? "text-slate-300" : "text-slate-600"}`}>
                      <svg viewBox="0 0 16 16" fill="currentColor" className={`w-4 h-4 flex-shrink-0 mt-0.5 ${p.popular ? "text-blue-400" : "text-blue-600"}`}>
                        <path fillRule="evenodd" d="M12.416 3.376a.75.75 0 0 1 .208 1.04l-5 7.5a.75.75 0 0 1-1.154.114l-3-3a.75.75 0 0 1 1.06-1.06l2.353 2.353 4.493-6.74a.75.75 0 0 1 1.04-.207Z" clipRule="evenodd" />
                      </svg>
                      {f}
                    </li>
                  ))}
                </ul>
                <Link href="/contact"
                  className={`block text-center py-3.5 rounded-xl text-sm font-bold transition-all ${
                    p.popular
                      ? "bg-blue-600 hover:bg-blue-500 text-white shadow-lg"
                      : "border-2 border-slate-200 hover:border-slate-900 hover:text-slate-900 text-slate-700"
                  }`}>
                  {p.cta}
                </Link>
              </div>
            ))}
          </div>

          <p className="text-center text-sm text-slate-400 mt-10 font-light">
            Toutes les offres incluent un accompagnement à la mise en place et une revue trimestrielle avec votre équipe.
          </p>
        </div>
      </section>

      {/* ── CTA Final ── */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(30,64,175,0.25),transparent_70%)]" />
        <div className="relative max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-4xl md:text-6xl font-black text-white leading-tight mb-6">
            Planifier une démonstration<br />
            <span className="bg-gradient-to-r from-blue-300 to-slate-300 bg-clip-text text-transparent">
              de 30 minutes
            </span>
          </h2>
          <p className="text-slate-400 text-lg mb-4 max-w-xl mx-auto font-light">
            Nos experts vous présentent une analyse de votre marché en direct, calibrée à votre secteur et vos enjeux compétitifs.
          </p>
          <p className="text-slate-500 text-sm mb-10">
            Nos experts vous rappellent sous 24h ouvrées.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/contact"
              className="inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 text-white font-bold text-base px-10 py-4 rounded-xl transition-all shadow-lg shadow-blue-900/50 hover:-translate-y-0.5">
              Planifier une démonstration
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4"><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
            </Link>
            <Link href="/contact"
              className="inline-flex items-center justify-center gap-2 bg-white/5 hover:bg-white/10 border border-white/10 text-white font-semibold text-base px-10 py-4 rounded-xl transition-all backdrop-blur-sm">
              Parler à un expert
            </Link>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="bg-slate-950 border-t border-white/5 py-14">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-10 mb-12">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-7 h-7 bg-slate-800 rounded-lg flex items-center justify-center">
                  <span className="text-white text-xs font-black">IQ</span>
                </div>
                <span className="text-white font-bold">CompeteIQ</span>
              </div>
              <p className="text-slate-500 text-sm leading-relaxed font-light">
                Partenaire d&apos;intelligence stratégique pour les ETI et Grands Comptes exigeants.
              </p>
            </div>
            {[
              { title: "Solutions", links: ["Intelligence 360°", "Alerte Décisionnelle", "Rapport Exécutif", "Cas clients"] },
              { title: "Entreprise", links: ["À propos", "Carrières", "Partenaires", "Contact"] },
              { title: "Confiance & Sécurité", links: ["ISO 27001", "Conformité RGPD", "Politique de confidentialité", "Mentions légales", "CGU"] },
            ].map((col) => (
              <div key={col.title}>
                <h4 className="text-white font-semibold text-sm mb-4">{col.title}</h4>
                <ul className="space-y-3">
                  {col.links.map((l) => (
                    <li key={l}>
                      <a href="#" className="text-slate-500 hover:text-slate-300 text-sm transition-colors font-light">{l}</a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <div className="border-t border-white/5 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-slate-600 text-xs">© 2026 CompeteIQ. Tous droits réservés.</p>
            <div className="flex flex-wrap gap-6 justify-center">
              {["Mentions légales", "Politique de confidentialité", "CGU", "Conformité RGPD", "ISO 27001"].map((l) => (
                <a key={l} href="#" className="text-slate-600 hover:text-slate-400 text-xs transition-colors">{l}</a>
              ))}
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
