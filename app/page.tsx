"use client";

import Link from "next/link";
import { useState, useEffect, useRef } from "react";

const navLinks = [
  { label: "Produit", href: "#features" },
  { label: "Tarifs", href: "#pricing" },
  { label: "Ressources", href: "#stats" },
  { label: "Entreprise", href: "#trusted" },
  { label: "Investisseurs", href: "/pitch" },
];

const features = [
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
      </svg>
    ),
    title: "Surveillance en temps réel",
    desc: "Détectez instantanément chaque changement de vos concurrents : prix, fonctionnalités, équipe, levées de fonds.",
    color: "from-blue-500/10 to-blue-600/5",
    accent: "text-blue-600",
    border: "border-blue-100",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
      </svg>
    ),
    title: "Analyse intelligente des prix",
    desc: "Comparez automatiquement les grilles tarifaires et recevez des alertes dès qu'un concurrent ajuste ses prix.",
    color: "from-violet-500/10 to-violet-600/5",
    accent: "text-violet-600",
    border: "border-violet-100",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456Z" />
      </svg>
    ),
    title: "Rapports IA automatiques",
    desc: "Générez des rapports d'intelligence concurrentielle complets en un clic, avec recommandations stratégiques.",
    color: "from-emerald-500/10 to-emerald-600/5",
    accent: "text-emerald-600",
    border: "border-emerald-100",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
      </svg>
    ),
    title: "Alertes personnalisées",
    desc: "Définissez vos propres critères d'alerte et soyez notifié immédiatement sur le canal de votre choix.",
    color: "from-amber-500/10 to-amber-600/5",
    accent: "text-amber-600",
    border: "border-amber-100",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 14.25v2.25m3-4.5v4.5m3-6.75v6.75m3-9v9M6 20.25h12A2.25 2.25 0 0 0 20.25 18V6A2.25 2.25 0 0 0 18 3.75H6A2.25 2.25 0 0 0 3.75 6v12A2.25 2.25 0 0 0 6 20.25Z" />
      </svg>
    ),
    title: "Comparaison multi-concurrents",
    desc: "Visualisez en un tableau toutes vos données concurrentielles pour prendre les meilleures décisions.",
    color: "from-rose-500/10 to-rose-600/5",
    accent: "text-rose-600",
    border: "border-rose-100",
  },
  {
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
      </svg>
    ),
    title: "Sécurité enterprise",
    desc: "Chiffrement bout en bout, SSO, audit logs et conformité RGPD. Vos données restent vos données.",
    color: "from-slate-500/10 to-slate-600/5",
    accent: "text-slate-600",
    border: "border-slate-200",
  },
];

const plans = [
  {
    name: "Starter",
    price: "39",
    desc: "Parfait pour démarrer votre veille concurrentielle. Essai 14 jours gratuit.",
    features: ["5 concurrents suivis", "Alertes email", "Rapports mensuels", "Tableau de bord", "Support communauté", "Alertes IA basiques", "Export CSV"],
    popular: false,
  },
  {
    name: "Pro",
    price: "79",
    desc: "Pour les équipes qui veulent garder une longueur d'avance.",
    features: ["20 concurrents suivis", "Alertes temps réel", "Rapports illimités", "API Access", "Export PDF & CSV", "Support prioritaire", "Insights IA avancés", "Analyse prédictive des prix"],
    popular: true,
  },
  {
    name: "Enterprise",
    price: "249",
    desc: "Pour les grandes organisations avec des besoins avancés.",
    features: ["Concurrents illimités", "Alertes personnalisées", "Rapports sur mesure", "Support dédié 24/7", "SSO & SAML", "SLA 99,9%", "Onboarding guidé", "CSM dédié", "Rapports personnalisés"],
    popular: false,
  },
];

const stats = [
  { value: "2 400+", label: "Entreprises actives" },
  { value: "98%", label: "Satisfaction client" },
  { value: "15 min", label: "Mise en place" },
  { value: "3,2x", label: "ROI moyen" },
];

const logos = ["Salesforce", "HubSpot", "Pipedrive", "Zoho", "Monday", "Notion"];

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
      <nav className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${scrolled ? "bg-white/90 backdrop-blur-md shadow-sm border-b border-slate-100" : "bg-transparent"}`}>
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center shadow-sm">
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
            <Link href="/login"
              className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors shadow-sm shadow-blue-200">
              Essai gratuit
            </Link>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden pt-16">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-blue-950 to-slate-900" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_60%_0%,rgba(59,130,246,0.25),transparent_70%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_10%_80%,rgba(139,92,246,0.15),transparent_60%)]" />
        {/* Grid lines */}
        <div className="absolute inset-0 opacity-[0.04]"
          style={{ backgroundImage: "linear-gradient(rgba(255,255,255,.6) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.6) 1px,transparent 1px)", backgroundSize: "60px 60px" }} />

        <div className="relative max-w-7xl mx-auto px-6 text-center py-24">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-400/20 text-blue-300 text-xs font-semibold px-4 py-1.5 rounded-full mb-8 backdrop-blur-sm">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" />
            IA intégrée · Nouveau en 2026
          </div>

          {/* Headline */}
          <h1 className="text-5xl md:text-7xl font-black text-white leading-[1.05] mb-8 tracking-tight max-w-5xl mx-auto">
            Gardez toujours{" "}
            <span className="bg-gradient-to-r from-blue-400 via-blue-300 to-violet-400 bg-clip-text text-transparent">
              une longueur
            </span>{" "}
            <br className="hidden md:block" />
            d&apos;avance sur vos concurrents
          </h1>

          <p className="text-lg md:text-xl text-slate-400 mb-12 max-w-2xl mx-auto leading-relaxed">
            CompeteIQ surveille vos concurrents 24h/24, analyse leurs stratégies en temps réel
            et vous envoie des alertes intelligentes pour ne jamais rater une opportunité.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-6">
            <Link href="/login"
              className="inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 text-white text-base font-bold px-8 py-4 rounded-xl transition-all shadow-lg shadow-blue-900/50 hover:shadow-blue-700/50 hover:-translate-y-0.5">
              Commencer gratuitement
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4"><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
            </Link>
            <Link href="/dashboard"
              className="inline-flex items-center justify-center gap-2 bg-white/5 hover:bg-white/10 border border-white/10 text-white text-base font-semibold px-8 py-4 rounded-xl transition-all backdrop-blur-sm">
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-blue-400"><path fillRule="evenodd" d="M2 10a8 8 0 1 1 16 0 8 8 0 0 1-16 0Zm6.39-2.908a.75.75 0 0 1 .766.027l3.5 2.25a.75.75 0 0 1 0 1.262l-3.5 2.25A.75.75 0 0 1 8 12.25v-4.5a.75.75 0 0 1 .39-.658Z" clipRule="evenodd" /></svg>
              Voir la démo live
            </Link>
          </div>
          <p className="text-sm text-slate-500">Sans carte bancaire · 14 jours d&apos;essai · Annulez à tout moment</p>

          {/* Dashboard preview */}
          <div className="mt-16 relative max-w-5xl mx-auto">
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-600/30 via-violet-600/20 to-blue-600/30 rounded-2xl blur-xl" />
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
                    competeiq.io/dashboard
                  </div>
                </div>
              </div>
              {/* Dashboard UI */}
              <div className="p-6">
                {/* Stat row */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-5">
                  {[
                    { label: "Concurrents", value: "5", change: "+2 ce mois", color: "text-blue-400", bg: "bg-blue-500/10" },
                    { label: "Alertes actives", value: "3", change: "2 non lues", color: "text-amber-400", bg: "bg-amber-500/10" },
                    { label: "Rapports", value: "3", change: "1 nouveau", color: "text-emerald-400", bg: "bg-emerald-500/10" },
                    { label: "Score marché", value: "74%", change: "+4pts", color: "text-violet-400", bg: "bg-violet-500/10" },
                  ].map((s) => (
                    <div key={s.label} className={`${s.bg} rounded-xl p-4 border border-white/5`}>
                      <p className="text-slate-500 text-xs mb-1">{s.label}</p>
                      <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
                      <p className="text-slate-600 text-xs mt-1">{s.change}</p>
                    </div>
                  ))}
                </div>
                {/* Competitor list */}
                <div className="space-y-2">
                  {[
                    { name: "Salesforce", share: 78, threat: "Élevée", tc: "bg-red-900/40 text-red-400", color: "#00A1E0" },
                    { name: "HubSpot", share: 55, threat: "Élevée", tc: "bg-red-900/40 text-red-400", color: "#FF7A59" },
                    { name: "Pipedrive", share: 32, threat: "Moyenne", tc: "bg-amber-900/40 text-amber-400", color: "#1A1A1A" },
                  ].map((c) => (
                    <div key={c.name} className="flex items-center gap-4 bg-slate-800/60 rounded-xl px-4 py-3 border border-white/5">
                      <div className="w-7 h-7 rounded-lg flex items-center justify-center text-white text-xs font-bold flex-shrink-0" style={{ backgroundColor: c.color }}>
                        {c.name[0]}
                      </div>
                      <span className="text-slate-200 text-sm font-medium w-24 flex-shrink-0">{c.name}</span>
                      <div className="flex-1 bg-slate-700/50 rounded-full h-1.5 hidden sm:block">
                        <div className="h-1.5 rounded-full bg-blue-500" style={{ width: `${c.share}%` }} />
                      </div>
                      <span className={`text-xs px-2.5 py-0.5 rounded-full font-medium flex-shrink-0 ${c.tc}`}>{c.threat}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Trusted by ── */}
      <section id="trusted" className="py-16 border-y border-slate-100 bg-slate-50">
        <div className="max-w-7xl mx-auto px-6">
          <p className="text-center text-sm font-semibold text-slate-400 uppercase tracking-widest mb-10">
            Utilisé pour surveiller les leaders du marché
          </p>
          <div className="flex flex-wrap items-center justify-center gap-6 md:gap-12">
            {logos.map((name) => (
              <div key={name} className="text-slate-300 font-bold text-lg md:text-xl tracking-tight select-none hover:text-slate-400 transition-colors cursor-default">
                {name}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Stats ── */}
      <section id="stats" ref={statsRef} className="py-24 bg-gradient-to-br from-blue-600 to-blue-700 text-white overflow-hidden relative">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_80%_50%,rgba(99,102,241,0.3),transparent_70%)]" />
        <div className="relative max-w-7xl mx-auto px-6">
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 text-center">
            {stats.map((s) => (
              <div key={s.label} className="space-y-1">
                <p className="text-4xl md:text-5xl font-black tracking-tight">{s.value}</p>
                <p className="text-blue-200 text-sm font-medium">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section id="features" className="py-28">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-20">
            <span className="text-blue-600 font-semibold text-sm uppercase tracking-widest">Fonctionnalités</span>
            <h2 className="text-4xl md:text-5xl font-black mt-3 mb-5 text-slate-900 leading-tight">
              Tout ce qu&apos;il vous faut<br className="hidden md:block" /> pour dominer votre marché
            </h2>
            <p className="text-slate-500 text-lg max-w-xl mx-auto">
              Une plateforme tout-en-un conçue pour les équipes marketing, produit et direction.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f) => (
              <div key={f.title}
                className={`group relative bg-gradient-to-br ${f.color} border ${f.border} rounded-2xl p-7 hover:shadow-lg hover:-translate-y-1 transition-all duration-300`}>
                <div className={`${f.accent} mb-5`}>{f.icon}</div>
                <h3 className="font-bold text-slate-900 text-lg mb-2">{f.title}</h3>
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
              <span className="text-blue-400 font-semibold text-sm uppercase tracking-widest">Intelligence artificielle</span>
              <h2 className="text-4xl md:text-5xl font-black mt-3 mb-6 leading-tight">
                Des insights<br />
                <span className="bg-gradient-to-r from-blue-400 to-violet-400 bg-clip-text text-transparent">
                  générés par l&apos;IA
                </span>
              </h2>
              <p className="text-slate-400 text-lg mb-8 leading-relaxed">
                Notre moteur IA analyse des milliers de signaux chaque heure — modifications de site web, offres d&apos;emploi, brevets, avis clients — pour vous donner une vision 360° de chaque concurrent.
              </p>
              <ul className="space-y-4 mb-10">
                {[
                  "Résumés automatiques des changements importants",
                  "Prédiction des mouvements tarifaires",
                  "Détection de nouvelles fonctionnalités avant le lancement",
                  "Alertes sur les recrutements stratégiques",
                ].map((item) => (
                  <li key={item} className="flex items-start gap-3 text-slate-300 text-sm">
                    <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5">
                      <path fillRule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.857-9.809a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z" clipRule="evenodd" />
                    </svg>
                    {item}
                  </li>
                ))}
              </ul>
              <Link href="/dashboard"
                className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold px-7 py-3.5 rounded-xl transition-colors">
                Explorer le tableau de bord
                <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4"><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
              </Link>
            </div>
            {/* Right side visual */}
            <div className="relative">
              <div className="absolute -inset-4 bg-gradient-to-r from-blue-600/20 to-violet-600/20 rounded-3xl blur-2xl" />
              <div className="relative bg-slate-900 rounded-2xl border border-white/10 p-6 space-y-3">
                {/* Alert cards */}
                {[
                  { icon: "💰", title: "Changement de prix détecté", body: "Salesforce a augmenté son plan Enterprise de 8% ce matin.", time: "Il y a 2h", color: "border-amber-500/30 bg-amber-500/5" },
                  { icon: "🚀", title: "Nouvelle fonctionnalité", body: "HubSpot vient de lancer l'intégration native avec Slack.", time: "Il y a 5h", color: "border-indigo-500/30 bg-indigo-500/5" },
                  { icon: "🤝", title: "Partenariat stratégique", body: "Pipedrive annonce un partenariat exclusif avec Microsoft Teams.", time: "Hier", color: "border-emerald-500/30 bg-emerald-500/5" },
                ].map((a) => (
                  <div key={a.title} className={`border ${a.color} rounded-xl p-4`}>
                    <div className="flex items-start gap-3">
                      <span className="text-xl">{a.icon}</span>
                      <div className="flex-1 min-w-0">
                        <p className="text-white font-semibold text-sm">{a.title}</p>
                        <p className="text-slate-400 text-xs mt-0.5 leading-relaxed">{a.body}</p>
                      </div>
                      <span className="text-slate-600 text-xs flex-shrink-0">{a.time}</span>
                    </div>
                  </div>
                ))}
                <div className="text-center pt-2">
                  <span className="text-xs text-slate-600">+ 14 autres alertes non lues</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Pricing ── */}
      <section id="pricing" className="py-28">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <span className="text-blue-600 font-semibold text-sm uppercase tracking-widest">Tarifs</span>
            <h2 className="text-4xl md:text-5xl font-black mt-3 mb-4 text-slate-900">
              Un plan pour chaque ambition
            </h2>
            <p className="text-slate-500 text-lg">Commencez gratuitement. Évoluez sans friction.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {plans.map((p) => (
              <div key={p.name} className={`relative rounded-2xl p-8 transition-all hover:shadow-xl ${
                p.popular
                  ? "bg-slate-900 text-white shadow-2xl scale-[1.02] ring-2 ring-blue-500"
                  : "bg-white border border-slate-200 hover:border-slate-300"
              }`}>
                {p.popular && (
                  <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-gradient-to-r from-blue-600 to-blue-500 text-white text-xs font-bold px-4 py-1 rounded-full shadow-lg">
                    Le plus populaire
                  </div>
                )}
                <h3 className={`font-bold text-xl mb-1 ${p.popular ? "text-white" : "text-slate-900"}`}>{p.name}</h3>
                <p className={`text-sm mb-6 ${p.popular ? "text-slate-400" : "text-slate-500"}`}>{p.desc}</p>
                <div className="flex items-end gap-1 mb-8">
                  <span className={`text-5xl font-black ${p.popular ? "text-white" : "text-slate-900"}`}>{p.price}€</span>
                  <span className={`mb-1.5 text-sm ${p.popular ? "text-slate-400" : "text-slate-400"}`}>/mois</span>
                </div>
                <ul className="space-y-3 mb-8">
                  {p.features.map((f) => (
                    <li key={f} className={`flex items-center gap-2.5 text-sm ${p.popular ? "text-slate-300" : "text-slate-600"}`}>
                      <svg viewBox="0 0 16 16" fill="currentColor" className={`w-4 h-4 flex-shrink-0 ${p.popular ? "text-blue-400" : "text-blue-600"}`}>
                        <path fillRule="evenodd" d="M12.416 3.376a.75.75 0 0 1 .208 1.04l-5 7.5a.75.75 0 0 1-1.154.114l-3-3a.75.75 0 0 1 1.06-1.06l2.353 2.353 4.493-6.74a.75.75 0 0 1 1.04-.207Z" clipRule="evenodd" />
                      </svg>
                      {f}
                    </li>
                  ))}
                </ul>
                <Link href="/login"
                  className={`block text-center py-3.5 rounded-xl text-sm font-bold transition-all ${
                    p.popular
                      ? "bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-900/50"
                      : "border-2 border-slate-200 hover:border-blue-500 hover:text-blue-600 text-slate-700"
                  }`}>
                  Commencer avec {p.name}
                </Link>
              </div>
            ))}
          </div>

          <p className="text-center text-sm text-slate-400 mt-10">
            Tous les plans incluent 14 jours d&apos;essai gratuit · Pas de carte bancaire requise
          </p>
        </div>
      </section>

      {/* ── CTA Banner ── */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(59,130,246,0.3),transparent_70%)]" />
        <div className="relative max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-4xl md:text-6xl font-black text-white leading-tight mb-6">
            Prêt à surveiller<br />
            <span className="bg-gradient-to-r from-blue-400 to-violet-400 bg-clip-text text-transparent">
              votre marché ?
            </span>
          </h2>
          <p className="text-slate-400 text-lg mb-10 max-w-xl mx-auto">
            Rejoignez 2 400+ entreprises qui utilisent CompeteIQ pour garder une longueur d&apos;avance.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/login"
              className="inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 text-white font-bold text-base px-10 py-4 rounded-xl transition-all shadow-lg shadow-blue-900/50 hover:-translate-y-0.5">
              Créer un compte gratuit
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4"><path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" /></svg>
            </Link>
            <Link href="/dashboard"
              className="inline-flex items-center justify-center gap-2 bg-white/5 hover:bg-white/10 border border-white/10 text-white font-semibold text-base px-10 py-4 rounded-xl transition-all backdrop-blur-sm">
              Voir la démo
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
                <div className="w-7 h-7 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white text-xs font-black">IQ</span>
                </div>
                <span className="text-white font-bold">CompeteIQ</span>
              </div>
              <p className="text-slate-500 text-sm leading-relaxed">
                La plateforme d&apos;intelligence concurrentielle pour les équipes modernes.
              </p>
            </div>
            {[
              { title: "Produit", links: ["Fonctionnalités", "Tarifs", "Changelog", "Roadmap"] },
              { title: "Ressources", links: ["Documentation", "Blog", "Cas clients", "Webinaires"] },
              { title: "Entreprise", links: ["À propos", "Carrières", "Partenaires", "Contact"] },
            ].map((col) => (
              <div key={col.title}>
                <h4 className="text-white font-semibold text-sm mb-4">{col.title}</h4>
                <ul className="space-y-3">
                  {col.links.map((l) => (
                    <li key={l}>
                      <a href="#" className="text-slate-500 hover:text-slate-300 text-sm transition-colors">{l}</a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <div className="border-t border-white/5 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-slate-600 text-xs">© 2026 CompeteIQ. Tous droits réservés.</p>
            <div className="flex gap-6">
              {["Confidentialité", "CGU", "Cookies"].map((l) => (
                <a key={l} href="#" className="text-slate-600 hover:text-slate-400 text-xs transition-colors">{l}</a>
              ))}
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
