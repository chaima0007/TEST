"use client";

import Link from "next/link";

export default function PitchPage() {
  return (
    <div className="min-h-screen bg-white text-slate-900 font-sans">

      {/* ── HEADER ── */}
      <header className="border-b border-slate-200 bg-white sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-indigo-700 rounded-lg flex items-center justify-center shadow-sm">
              <span className="text-white text-xs font-black tracking-tight">IQ</span>
            </div>
            <span className="text-lg font-bold text-slate-900">CompeteIQ</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden sm:flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-widest">
              <svg className="w-3.5 h-3.5 text-slate-300" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5 9V7a5 5 0 0 1 10 0v2a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2Zm8-2v2H7V7a3 3 0 0 1 6 0Z" clipRule="evenodd" />
              </svg>
              Dossier de présentation — Confidentiel
            </span>
            <Link href="/"
              className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors px-3 py-1.5 rounded-lg hover:bg-slate-100">
              Retour au site
            </Link>
          </div>
        </div>
      </header>

      {/* ── HERO ── */}
      <section className="bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900 text-white py-24 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-indigo-500/15 border border-indigo-400/25 text-indigo-300 text-xs font-semibold px-4 py-1.5 rounded-full mb-8">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse" />
            Dossier investisseur — Juin 2026
          </div>

          <h1 className="text-5xl md:text-6xl font-black leading-tight mb-6 tracking-tight">
            La plateforme d&apos;intelligence{" "}
            <span className="bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent">
              concurrentielle
            </span>
            <br />
            pour les équipes modernes
          </h1>

          <p className="text-slate-400 text-xl max-w-2xl mx-auto mb-14 leading-relaxed">
            CompeteIQ automatise la veille concurrentielle grâce à l&apos;IA — de la surveillance
            temps réel aux rapports stratégiques en un clic. SaaS B2B, MRR scalable, stack enterprise.
          </p>

          {/* Hero Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
            {[
              { value: "11", label: "Pages produit", sub: "couverture complète" },
              { value: "100%", label: "Sécurité enterprise", sub: "SSO · RGPD · Audit logs" },
              { value: "Next.js 16", label: "Stack moderne", sub: "TypeScript · Tailwind" },
              { value: "Prêt", label: "À déployer", sub: "zéro dette technique" },
            ].map((s) => (
              <div key={s.label}
                className="bg-white/5 border border-white/10 rounded-2xl px-5 py-6 text-center backdrop-blur-sm">
                <p className="text-3xl font-black text-white mb-1">{s.value}</p>
                <p className="text-sm font-semibold text-indigo-300 mb-0.5">{s.label}</p>
                <p className="text-xs text-slate-500">{s.sub}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── LE PROBLÈME ── */}
      <section className="py-24 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="mb-14 text-center">
            <span className="text-indigo-600 font-semibold text-sm uppercase tracking-widest">Le problème</span>
            <h2 className="text-4xl font-black mt-3 text-slate-900">
              Sans veille, les équipes naviguent à l&apos;aveugle
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-8 h-8">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
                  </svg>
                ),
                color: "text-rose-500",
                bg: "bg-rose-50 border-rose-100",
                title: "Réactivité zéro face aux mouvements concurrents",
                desc: "Les équipes apprennent les changements de prix ou de fonctionnalités de leurs concurrents par leurs propres clients — souvent trop tard. En moyenne, une entreprise met 3 semaines à détecter un mouvement majeur d&apos;un concurrent direct.",
              },
              {
                icon: (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-8 h-8">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18 9 11.25l4.306 4.306a11.95 11.95 0 0 1 5.814-5.518l2.74-1.22m0 0-5.94-2.281m5.94 2.28-2.28 5.941" />
                  </svg>
                ),
                color: "text-amber-500",
                bg: "bg-amber-50 border-amber-100",
                title: "Décisions stratégiques prises sur des données périmées",
                desc: "Les rapports concurrentiels sont réalisés manuellement, une à deux fois par an. Entre-temps, le marché évolue : nouvelles offres, nouvelles acquisitions, repositionnements tarifaires. Les comités de direction pilotent avec 6 mois de retard.",
              },
              {
                icon: (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-8 h-8">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                  </svg>
                ),
                color: "text-violet-500",
                bg: "bg-violet-50 border-violet-100",
                title: "Un poste d&apos;analyste coûteux pour un output insuffisant",
                desc: "Les entreprises qui ont les moyens recrutent un ou plusieurs analystes marché. Coût : 60 000 à 90 000 €/an par profil. Résultat : un rapport tous les deux mois, qui ne couvre que 3 à 5 concurrents et ignore les signaux faibles.",
              },
            ].map((p) => (
              <div key={p.title} className={`border rounded-2xl p-7 ${p.bg}`}>
                <div className={`${p.color} mb-4`}>{p.icon}</div>
                <h3 className="font-bold text-slate-900 text-lg mb-3">{p.title}</h3>
                <p className="text-slate-600 text-sm leading-relaxed">{p.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── LA SOLUTION ── */}
      <section className="py-24 px-6 bg-slate-50">
        <div className="max-w-6xl mx-auto">
          <div className="mb-14 text-center">
            <span className="text-indigo-600 font-semibold text-sm uppercase tracking-widest">La solution</span>
            <h2 className="text-4xl font-black mt-3 text-slate-900">
              CompeteIQ — votre radar concurrentiel en temps réel
            </h2>
            <p className="text-slate-500 text-lg mt-4 max-w-2xl mx-auto">
              Une plateforme SaaS tout-en-un qui surveille, analyse et alerte automatiquement
              sur chaque mouvement de vos concurrents — 24h/24, 7j/7.
            </p>
          </div>

          {/* Dashboard mockup */}
          <div className="max-w-5xl mx-auto">
            <div className="relative">
              <div className="absolute -inset-1 bg-gradient-to-r from-indigo-600/20 via-violet-600/15 to-indigo-600/20 rounded-2xl blur-xl" />
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
                  <div className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
                    <span className="text-xs text-slate-500">Live</span>
                  </div>
                </div>

                {/* Dashboard content */}
                <div className="p-6">
                  {/* Page header */}
                  <div className="flex items-center justify-between mb-5">
                    <div>
                      <h3 className="text-white font-semibold text-base">Tableau de bord</h3>
                      <p className="text-slate-500 text-xs">Vue d&apos;ensemble de votre veille concurrentielle</p>
                    </div>
                    <div className="flex items-center gap-1.5 text-xs text-slate-500">
                      <span className="w-1.5 h-1.5 rounded-full bg-green-400 inline-block" />
                      Mis à jour à 09:42
                    </div>
                  </div>

                  {/* Stat row */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-5">
                    {[
                      { label: "Concurrents suivis", value: "5", trend: "+2 ce mois", color: "text-indigo-400", bg: "bg-indigo-500/10", border: "border-indigo-500/20" },
                      { label: "Alertes actives", value: "3", trend: "2 non lues", color: "text-amber-400", bg: "bg-amber-500/10", border: "border-amber-500/20" },
                      { label: "Rapports générés", value: "3", trend: "Stable", color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/20" },
                      { label: "Score de marché", value: "74%", trend: "+4 pts", color: "text-violet-400", bg: "bg-violet-500/10", border: "border-violet-500/20" },
                    ].map((s) => (
                      <div key={s.label} className={`${s.bg} border ${s.border} rounded-xl p-4`}>
                        <p className="text-slate-500 text-xs mb-1">{s.label}</p>
                        <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
                        <p className="text-slate-600 text-xs mt-1">{s.trend}</p>
                      </div>
                    ))}
                  </div>

                  {/* Quick actions */}
                  <div className="rounded-lg bg-gradient-to-r from-indigo-600 to-indigo-700 px-4 py-3 flex items-center justify-between mb-4">
                    <p className="text-white text-xs font-medium">Actions rapides</p>
                    <div className="flex gap-2">
                      {["Ajouter concurrent", "Générer rapport", "Comparer"].map((a) => (
                        <span key={a} className="text-xs bg-white/10 border border-white/20 text-white px-3 py-1 rounded-md">{a}</span>
                      ))}
                    </div>
                  </div>

                  {/* Competitor table */}
                  <div className="bg-slate-800/60 rounded-xl overflow-hidden border border-white/5">
                    <div className="grid grid-cols-[1fr_auto_auto] gap-x-4 px-4 py-2 bg-slate-800 border-b border-white/5">
                      {["Concurrent", "Secteur", "Menace"].map((h) => (
                        <span key={h} className="text-xs font-semibold text-slate-400 uppercase tracking-wide">{h}</span>
                      ))}
                    </div>
                    {[
                      { name: "Salesforce", industry: "CRM", threat: "Élevée", tc: "text-rose-400 bg-rose-900/30", color: "#00A1E0", logo: "SF" },
                      { name: "HubSpot", industry: "CRM / Marketing", threat: "Élevée", tc: "text-rose-400 bg-rose-900/30", color: "#FF7A59", logo: "HS" },
                      { name: "Pipedrive", industry: "CRM Ventes", threat: "Moyenne", tc: "text-amber-400 bg-amber-900/30", color: "#2C3E50", logo: "PD" },
                      { name: "Zoho CRM", industry: "CRM Suite", threat: "Moyenne", tc: "text-amber-400 bg-amber-900/30", color: "#E42527", logo: "ZO" },
                      { name: "Monday.com", industry: "Gestion / CRM", threat: "Faible", tc: "text-emerald-400 bg-emerald-900/30", color: "#F6517C", logo: "MN" },
                    ].map((c) => (
                      <div key={c.name} className="grid grid-cols-[1fr_auto_auto] gap-x-4 items-center px-4 py-2.5 border-b border-white/5 last:border-0">
                        <div className="flex items-center gap-2.5">
                          <div className="w-6 h-6 rounded-md flex items-center justify-center text-white text-[9px] font-bold flex-shrink-0" style={{ backgroundColor: c.color }}>
                            {c.logo}
                          </div>
                          <span className="text-slate-200 text-xs font-medium">{c.name}</span>
                        </div>
                        <span className="text-slate-400 text-xs hidden sm:block">{c.industry}</span>
                        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${c.tc}`}>{c.threat}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Feature highlights */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 mt-12">
            {[
              { icon: "01", title: "Surveillance temps réel", desc: "Prix, fonctionnalités, équipes, recrutements — chaque signal capturé instantanément." },
              { icon: "02", title: "Rapports IA en 1 clic", desc: "Des analyses stratégiques complètes générées automatiquement avec recommandations." },
              { icon: "03", title: "Alertes intelligentes", desc: "Notifications configurables sur Slack, email, ou webhook dès qu&apos;un événement clé survient." },
              { icon: "04", title: "Comparaison multi-concurrents", desc: "Tableau de bord unifié pour visualiser toutes vos données côte à côte." },
              { icon: "05", title: "Analyse de prix prédictive", desc: "L&apos;IA prédit les prochains mouvements tarifaires pour que vous anticicipiez, pas subissiez." },
              { icon: "06", title: "Sécurité enterprise", desc: "SSO/SAML, chiffrement E2E, audit logs, conformité RGPD. SLA 99,9%." },
            ].map((f) => (
              <div key={f.title} className="bg-white border border-slate-200 rounded-xl p-6">
                <div className="text-indigo-300 font-black text-2xl mb-3">{f.icon}</div>
                <h3 className="font-bold text-slate-900 mb-2">{f.title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── MARCHÉ ── */}
      <section className="py-24 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="mb-14 text-center">
            <span className="text-indigo-600 font-semibold text-sm uppercase tracking-widest">Opportunité de marché</span>
            <h2 className="text-4xl font-black mt-3 text-slate-900">
              Un marché de $8,4B en forte croissance
            </h2>
            <p className="text-slate-500 text-lg mt-4 max-w-xl mx-auto">
              Le marché de l&apos;intelligence concurrentielle est porté par la digitalisation
              des équipes commerciales et l&apos;essor de l&apos;IA générative.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-16">
            {[
              {
                label: "TAM",
                full: "Total Addressable Market",
                value: "$8,4B",
                desc: "Marché global de l&apos;intelligence concurrentielle (2025). CAGR : +14,2% jusqu&apos;en 2030.",
                color: "from-indigo-600 to-indigo-700",
                ring: "ring-indigo-200",
              },
              {
                label: "SAM",
                full: "Serviceable Addressable Market",
                value: "$1,2B",
                desc: "Segment SaaS B2B ciblant les PME et ETI (10 à 500 salariés) en Europe et Amérique du Nord.",
                color: "from-violet-500 to-violet-600",
                ring: "ring-violet-200",
              },
              {
                label: "SOM",
                full: "Serviceable Obtainable Market",
                value: "$24M",
                desc: "Cible réaliste à 3 ans, représentant 2% du SAM. Équivalent à ~3 000 clients à 8 000 $/an ARR moyen.",
                color: "from-slate-700 to-slate-800",
                ring: "ring-slate-200",
              },
            ].map((m) => (
              <div key={m.label} className={`rounded-2xl p-8 text-white bg-gradient-to-br ${m.color} relative overflow-hidden ring-4 ${m.ring}`}>
                <div className="absolute -top-6 -right-6 w-24 h-24 bg-white/5 rounded-full" />
                <div className="absolute -bottom-4 -left-4 w-16 h-16 bg-white/5 rounded-full" />
                <div className="relative">
                  <div className="inline-block bg-white/15 text-white text-xs font-black px-3 py-1 rounded-full mb-4 uppercase tracking-wider">
                    {m.label}
                  </div>
                  <p className="text-4xl font-black mb-1">{m.value}</p>
                  <p className="text-white/60 text-xs mb-4 font-medium">{m.full}</p>
                  <p className="text-white/80 text-sm leading-relaxed" dangerouslySetInnerHTML={{ __html: m.desc }} />
                </div>
              </div>
            ))}
          </div>

          {/* Market context */}
          <div className="grid md:grid-cols-3 gap-6 text-center">
            {[
              { value: "14,2%", label: "CAGR projeté", sub: "2025–2030, tous segments confondus" },
              { value: "2 400+", label: "Entreprises actives", sub: "utilisent CompeteIQ dès aujourd&apos;hui" },
              { value: "3,2×", label: "ROI moyen client", sub: "mesuré sur les 12 premiers mois" },
            ].map((s) => (
              <div key={s.label} className="bg-slate-50 border border-slate-200 rounded-xl p-7">
                <p className="text-4xl font-black text-indigo-600 mb-1">{s.value}</p>
                <p className="font-semibold text-slate-900 mb-1">{s.label}</p>
                <p className="text-slate-500 text-sm" dangerouslySetInnerHTML={{ __html: s.sub }} />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── TRACTION & ROADMAP ── */}
      <section className="py-24 px-6 bg-slate-50">
        <div className="max-w-6xl mx-auto">
          <div className="mb-14 text-center">
            <span className="text-indigo-600 font-semibold text-sm uppercase tracking-widest">Traction & Roadmap</span>
            <h2 className="text-4xl font-black mt-3 text-slate-900">
              Plan de croissance 18 mois
            </h2>
          </div>

          <div className="relative">
            {/* Timeline line */}
            <div className="absolute left-[50%] top-0 bottom-0 w-px bg-indigo-100 hidden md:block" />

            <div className="space-y-8">
              {[
                {
                  phase: "Phase 1",
                  period: "T3 2026 — T4 2026",
                  title: "Lancement & Acquisition",
                  side: "left",
                  color: "bg-indigo-600",
                  items: [
                    "Lancement commercial — Plan Starter à 29€/mois",
                    "Objectif : 300 clients payants d&apos;ici décembre 2026",
                    "Intégrations Slack + Notion + HubSpot",
                    "MRR cible : 15 000 €",
                  ],
                },
                {
                  phase: "Phase 2",
                  period: "T1 2027 — T2 2027",
                  title: "Expansion & Upsell",
                  side: "right",
                  color: "bg-violet-600",
                  items: [
                    "Lancement plan Enterprise avec SSO/SAML",
                    "Expansion Europe : UK, Allemagne, Espagne",
                    "Moteur IA prédictif (mouvements tarifaires)",
                    "MRR cible : 60 000 €",
                  ],
                },
                {
                  phase: "Phase 3",
                  period: "T3 2027 — T4 2027",
                  title: "Scale & Consolidation",
                  side: "left",
                  color: "bg-slate-700",
                  items: [
                    "Marketplace d&apos;intégrations (50+ connecteurs)",
                    "API publique pour intégrations custom",
                    "Programme partenaires revendeurs",
                    "ARR cible : 2 M€ — Breakeven opérationnel",
                  ],
                },
              ].map((ph) => (
                <div key={ph.phase}
                  className={`md:flex md:items-start gap-8 ${ph.side === "right" ? "md:flex-row-reverse" : ""}`}>
                  {/* Content */}
                  <div className="md:w-1/2 bg-white border border-slate-200 rounded-2xl p-7">
                    <div className={`inline-block text-white text-xs font-black px-3 py-1 rounded-full mb-4 ${ph.color}`}>
                      {ph.phase}
                    </div>
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="font-bold text-slate-900 text-xl">{ph.title}</h3>
                      <span className="text-xs text-slate-400 font-medium ml-3 mt-0.5 flex-shrink-0">{ph.period}</span>
                    </div>
                    <ul className="space-y-2.5">
                      {ph.items.map((item) => (
                        <li key={item} className="flex items-start gap-2.5 text-slate-600 text-sm">
                          <svg viewBox="0 0 16 16" fill="currentColor" className="w-4 h-4 text-indigo-400 flex-shrink-0 mt-0.5">
                            <path fillRule="evenodd" d="M12.416 3.376a.75.75 0 0 1 .208 1.04l-5 7.5a.75.75 0 0 1-1.154.114l-3-3a.75.75 0 0 1 1.06-1.06l2.353 2.353 4.493-6.74a.75.75 0 0 1 1.04-.207Z" clipRule="evenodd" />
                          </svg>
                          <span dangerouslySetInnerHTML={{ __html: item }} />
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Spacer for opposite side */}
                  <div className="hidden md:block md:w-1/2" />
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── STACK & ARCHITECTURE ── */}
      <section className="py-24 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="mb-14 text-center">
            <span className="text-indigo-600 font-semibold text-sm uppercase tracking-widest">Stack technique</span>
            <h2 className="text-4xl font-black mt-3 text-slate-900">
              Architecture moderne, scalable, sans dette
            </h2>
            <p className="text-slate-500 text-lg mt-4 max-w-xl mx-auto">
              Conçu pour supporter 100 000 utilisateurs dès le départ. Zéro compromis sur la sécurité ou la performance.
            </p>
          </div>

          {/* Tech badges */}
          <div className="flex flex-wrap gap-3 justify-center mb-14">
            {[
              { name: "Next.js 16", color: "bg-slate-900 text-white" },
              { name: "TypeScript", color: "bg-blue-600 text-white" },
              { name: "Tailwind CSS", color: "bg-cyan-500 text-white" },
              { name: "Prisma ORM", color: "bg-indigo-600 text-white" },
              { name: "Node.js", color: "bg-green-600 text-white" },
              { name: "PostgreSQL", color: "bg-blue-800 text-white" },
              { name: "Vercel Edge", color: "bg-slate-800 text-white" },
              { name: "SSO / SAML", color: "bg-violet-600 text-white" },
              { name: "RGPD", color: "bg-emerald-600 text-white" },
              { name: "API REST", color: "bg-rose-600 text-white" },
            ].map((t) => (
              <span key={t.name} className={`${t.color} text-sm font-semibold px-5 py-2 rounded-full`}>
                {t.name}
              </span>
            ))}
          </div>

          {/* Architecture cards */}
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                icon: (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 17.25v1.007a3 3 0 0 1-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0 1 15 18.257V17.25m6-12V15a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 15V5.25m18 0A2.25 2.25 0 0 0 18.75 3H5.25A2.25 2.25 0 0 0 3 5.25m18 0H3" />
                  </svg>
                ),
                title: "Frontend performant",
                desc: "Next.js 16 avec App Router, Server Components et streaming SSR. Core Web Vitals au vert. LCP < 1,2s.",
              },
              {
                icon: (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 14.25h13.5m-13.5 0a3 3 0 0 1-3-3m3 3a3 3 0 1 0 0 6h13.5a3 3 0 1 0 0-6m-16.5-3a3 3 0 0 1 3-3h13.5a3 3 0 0 1 3 3m-19.5 0a4.5 4.5 0 0 1 .9-2.7L5.737 5.1a3.375 3.375 0 0 1 2.7-1.35h7.126c1.062 0 2.062.5 2.7 1.35l2.587 3.45a4.5 4.5 0 0 1 .9 2.7m0 0a3 3 0 0 1-3 3m0 3h.008v.008h-.008v-.008Zm0-6h.008v.008h-.008v-.008Zm-3 6h.008v.008h-.008v-.008Zm0-6h.008v.008h-.008v-.008Z" />
                  </svg>
                ),
                title: "Backend scalable",
                desc: "API Routes Next.js, Prisma ORM sur PostgreSQL (Supabase). Architecture multi-tenant avec row-level security.",
              },
              {
                icon: (
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
                  </svg>
                ),
                title: "Sécurité enterprise",
                desc: "SSO/SAML, chiffrement AES-256, audit logs immuables, conformité RGPD/ISO 27001. SLA 99,9%.",
              },
            ].map((c) => (
              <div key={c.title} className="border border-slate-200 rounded-2xl p-7 bg-slate-50">
                <div className="text-indigo-600 mb-4">{c.icon}</div>
                <h3 className="font-bold text-slate-900 mb-2">{c.title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{c.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── VALORISATION ── */}
      <section className="py-24 px-6 bg-slate-50">
        <div className="max-w-6xl mx-auto">
          <div className="mb-14 text-center">
            <span className="text-indigo-600 font-semibold text-sm uppercase tracking-widest">Valorisation</span>
            <h2 className="text-4xl font-black mt-3 text-slate-900">
              3 scénarios d&apos;acquisition
            </h2>
            <p className="text-slate-500 text-lg mt-4 max-w-xl mx-auto">
              Basés sur des multiples sectoriels SaaS B2B observés en 2025–2026 (source : Crunchbase, PitchBook).
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {[
              {
                scenario: "Conservateur",
                multiple: "4× ARR",
                target: "ARR Année 1 : 180 K€",
                valuation: "720 K€",
                note: "Acquisition technologique ou acqui-hire. Idéal pour une startup en quête d&apos;une équipe front-end experte Next.js.",
                color: "border-slate-300 bg-white",
                badge: "bg-slate-100 text-slate-600",
                popular: false,
              },
              {
                scenario: "Standard",
                multiple: "8× ARR",
                target: "ARR Année 2 : 720 K€",
                valuation: "5,76 M€",
                note: "Valorisation de marché. Acquisition par un éditeur de CRM ou d&apos;outils marketing souhaitant intégrer la veille concurrentielle.",
                color: "border-indigo-500 bg-white ring-2 ring-indigo-200 shadow-xl",
                badge: "bg-indigo-600 text-white",
                popular: true,
              },
              {
                scenario: "Premium",
                multiple: "12× ARR",
                target: "ARR Année 3 : 2 M€",
                valuation: "24 M€",
                note: "Prime stratégique. Acquisition par un leader (Salesforce, HubSpot, Semrush) pour consolider leur offre competitive intelligence.",
                color: "border-slate-300 bg-white",
                badge: "bg-slate-100 text-slate-600",
                popular: false,
              },
            ].map((v) => (
              <div key={v.scenario} className={`relative rounded-2xl p-8 border ${v.color} transition-all`}>
                {v.popular && (
                  <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-indigo-600 text-white text-xs font-bold px-4 py-1 rounded-full shadow">
                    Scénario privilégié
                  </div>
                )}
                <div className={`inline-block text-xs font-bold px-3 py-1 rounded-full mb-5 ${v.badge}`}>
                  {v.scenario}
                </div>
                <div className="mb-5">
                  <p className="text-4xl font-black text-slate-900">{v.valuation}</p>
                  <p className="text-sm text-indigo-600 font-semibold mt-1">{v.multiple} — {v.target}</p>
                </div>
                <p className="text-slate-500 text-sm leading-relaxed">{v.note}</p>
              </div>
            ))}
          </div>

          <p className="text-center text-sm text-slate-400 mt-8">
            Ces projections sont indicatives et basées sur des hypothèses de croissance raisonnables.
            Due diligence complète disponible sur demande.
          </p>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="py-24 px-6 bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-black mb-6 leading-tight">
            Prêt à discuter{" "}
            <span className="bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent">
              d&apos;une opportunité ?
            </span>
          </h2>
          <p className="text-slate-400 text-lg mb-10 max-w-xl mx-auto">
            Que vous soyez investisseur, fonds de PE ou acquéreur stratégique,
            notre équipe est disponible pour une présentation confidentielle complète.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-10">
            <a href="mailto:contact@competeiq.io"
              className="inline-flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-lg px-10 py-5 rounded-xl transition-all shadow-lg shadow-indigo-900/50 hover:-translate-y-0.5">
              <svg viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
                <path d="M3 4a2 2 0 0 0-2 2v1.161l8.441 4.221a1.25 1.25 0 0 0 1.118 0L19 7.162V6a2 2 0 0 0-2-2H3Z" />
                <path d="m19 8.839-7.77 3.885a2.75 2.75 0 0 1-2.46 0L1 8.839V14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8.839Z" />
              </svg>
              Prendre contact
            </a>
            <a href="mailto:contact@competeiq.io"
              className="inline-flex items-center justify-center gap-2 bg-white/5 hover:bg-white/10 border border-white/10 text-white font-semibold text-lg px-10 py-5 rounded-xl transition-all backdrop-blur-sm">
              contact@competeiq.io
            </a>
          </div>

          <div className="flex flex-wrap gap-6 justify-center text-sm text-slate-500">
            {["NDA disponible sur demande", "Data room accessible sous 48h", "Réponse garantie en 24h"].map((item) => (
              <div key={item} className="flex items-center gap-2">
                <svg viewBox="0 0 16 16" fill="currentColor" className="w-3.5 h-3.5 text-indigo-400 flex-shrink-0">
                  <path fillRule="evenodd" d="M12.416 3.376a.75.75 0 0 1 .208 1.04l-5 7.5a.75.75 0 0 1-1.154.114l-3-3a.75.75 0 0 1 1.06-1.06l2.353 2.353 4.493-6.74a.75.75 0 0 1 1.04-.207Z" clipRule="evenodd" />
                </svg>
                {item}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer className="bg-slate-950 border-t border-white/5 py-8 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-indigo-600 rounded-md flex items-center justify-center">
              <span className="text-white text-[9px] font-black">IQ</span>
            </div>
            <span className="text-white font-bold text-sm">CompeteIQ</span>
          </div>
          <p className="text-slate-600 text-xs text-center">
            Ce document est confidentiel et destiné exclusivement à son destinataire.
            Toute reproduction ou diffusion est interdite sans accord écrit.
          </p>
          <p className="text-slate-600 text-xs">© 2026 CompeteIQ. Tous droits réservés.</p>
        </div>
      </footer>

    </div>
  );
}
