"use client";

import Link from "next/link";
import { useState, useEffect } from "react";

const navLinks = [
  { label: "Services", href: "#services" },
  { label: "Tarifs", href: "/tarifs" },
  { label: "Simulation", href: "/simulation" },
  { label: "Notre force", href: "/notre-force" },
  { label: "Contact", href: "/contact" },
];

const services = [
  {
    title: "Sites web sur-mesure",
    desc: "Des sites modernes, rapides et soignés qui inspirent confiance dès la première seconde. Pensés pour vos clients, pas pour faire joli.",
    points: ["Design moderne & responsive", "Optimisé mobile et rapidité", "Livré en quelques jours"],
    accent: "from-indigo-500/15 to-indigo-600/5",
    ring: "text-indigo-300",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <rect x="3" y="4" width="18" height="14" rx="2" />
        <path d="M3 9h18M7 14h6" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    title: "Tableaux de bord",
    desc: "Visualisez votre activité en un coup d'œil : ventes, clients, performance. Vos données enfin claires et exploitables.",
    points: ["Sur-mesure selon vos besoins", "Données en temps réel", "Simple à utiliser au quotidien"],
    accent: "from-emerald-500/15 to-emerald-600/5",
    ring: "text-emerald-400",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path d="M3 3v18h18" strokeLinecap="round" />
        <path d="M7 14l3-4 3 3 4-6" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    title: "Automatisations",
    desc: "Libérez-vous des tâches répétitives. On automatise ce qui vous fait perdre du temps pour que vous vous concentriez sur l'essentiel.",
    points: ["Gain de temps mesurable", "Moins d'erreurs manuelles", "Adapté à vos outils"],
    accent: "from-indigo-500/15 to-indigo-700/5",
    ring: "text-violet-400",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <circle cx="12" cy="12" r="3" />
        <path d="M12 2v4M12 18v4M2 12h4M18 12h4M5 5l3 3M16 16l3 3M19 5l-3 3M8 16l-3 3" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    title: "Business plan & stratégie",
    desc: "Un plan d'affaires clair et professionnel pour convaincre, lever des fonds ou structurer votre croissance. Analyse, chiffrage et stratégie inclus.",
    points: ["Plan d'affaires structuré", "Analyse marché & chiffrage", "Présentation prête à pitcher"],
    accent: "from-amber-500/15 to-amber-600/5",
    ring: "text-amber-400",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-7 h-7">
        <path d="M4 4v16h16" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M8 16l3-5 3 2 4-7" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
];

const steps = [
  { n: "1", title: "On écoute", desc: "On comprend votre besoin réel — pas de jargon, pas de blabla. Un échange simple de 20 minutes." },
  { n: "2", title: "On conçoit", desc: "On vous propose une solution claire et un devis transparent. Vous validez avant qu'on commence." },
  { n: "3", title: "On livre vite", desc: "Vous recevez un résultat fonctionnel en quelques jours, et on reste disponible après la livraison." },
];

const values = [
  { title: "Sur-mesure, jamais de modèle générique", desc: "Chaque projet est conçu pour VOTRE activité, pas copié-collé." },
  { title: "Rapidité de livraison", desc: "On travaille vite et bien. Vous voyez un résultat concret en quelques jours." },
  { title: "Transparence totale", desc: "Devis clair, prix annoncés, aucune surprise. Vous savez toujours où vous en êtes." },
  { title: "Automatisation maîtrisée", desc: "Nos outils automatisés sont supervisés et contrôlés — la puissance de l'IA, avec la fiabilité d'un suivi humain." },
];

export default function Home() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <div className="min-h-screen bg-white text-slate-900 overflow-x-hidden">

      {/* ── Navigation ── */}
      <nav className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${scrolled ? "bg-white/95 backdrop-blur-md shadow-sm border-b border-slate-100" : "bg-transparent"}`}>
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center shadow-sm">
              <span className="text-white text-xs font-black tracking-tight">C</span>
            </div>
            <span className={`text-lg font-bold transition-colors ${scrolled ? "text-slate-900" : "text-white"}`}>Caelum</span>
          </div>

          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((l) => (
              <a key={l.label} href={l.href}
                className={`px-4 py-2 text-sm rounded-lg transition-colors font-medium ${scrolled ? "text-slate-600 hover:text-slate-900 hover:bg-slate-100" : "text-slate-200 hover:text-white hover:bg-white/10"}`}>
                {l.label}
              </a>
            ))}
          </div>

          <Link href="/contact"
            className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors shadow-sm">
            Demander un devis
          </Link>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden pt-16 text-center px-6">
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_60%_0%,rgba(37,99,235,0.25),transparent_65%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_15%_85%,rgba(124,58,237,0.18),transparent_60%)]" />
        <div className="absolute inset-0 opacity-[0.04]"
          style={{ backgroundImage: "linear-gradient(rgba(255,255,255,.6) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.6) 1px,transparent 1px)", backgroundSize: "80px 80px" }} />

        <div className="relative z-10 max-w-4xl">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-8">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            Studio web &amp; data — Bruxelles
          </span>

          <h1 className="text-4xl sm:text-6xl font-bold tracking-tight text-white leading-[1.1]">
            Des outils digitaux
            <span className="block bg-gradient-to-r from-indigo-300 to-sky-300 bg-clip-text text-transparent">
              qui font avancer votre activité
            </span>
          </h1>

          <p className="text-lg sm:text-xl text-slate-300 mt-6 max-w-2xl mx-auto leading-relaxed">
            Sites web, tableaux de bord et automatisations sur-mesure.
            <span className="block mt-2 text-white font-medium">La qualité d&apos;une agence, au prix d&apos;un freelance bruxellois.</span>
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-10">
            <Link href="/contact"
              className="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-indigo-600/20">
              Démarrer un projet
            </Link>
            <a href="#services"
              className="w-full sm:w-auto bg-white/10 hover:bg-white/15 border border-white/15 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors">
              Voir nos services
            </a>
          </div>

          <p className="text-slate-400 text-sm mt-6">Réponse sous 24h · Premier échange sans engagement</p>
        </div>
      </section>

      {/* ── Services ── */}
      <section id="services" className="py-24 px-6 max-w-7xl mx-auto">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="text-indigo-600 font-semibold text-sm uppercase tracking-wide">Nos services</span>
          <h2 className="text-3xl sm:text-4xl font-bold mt-3">Ce que nous construisons pour vous</h2>
          <p className="text-slate-500 mt-4">Trois savoir-faire, une même exigence : du concret qui vous sert vraiment.</p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {services.map((s) => (
            <div key={s.title} className={`rounded-2xl border border-slate-200 p-7 bg-gradient-to-b ${s.accent} hover:shadow-lg hover:-translate-y-1 transition-all`}>
              <div className={`w-14 h-14 rounded-xl bg-slate-900 ${s.ring} flex items-center justify-center mb-5`}>
                {s.icon}
              </div>
              <h3 className="text-xl font-bold">{s.title}</h3>
              <p className="text-slate-600 mt-3 text-sm leading-relaxed">{s.desc}</p>
              <ul className="mt-5 space-y-2">
                {s.points.map((p) => (
                  <li key={p} className="flex items-center gap-2 text-sm text-slate-700">
                    <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-emerald-500 flex-shrink-0">
                      <path fillRule="evenodd" d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4L8.5 12l6.8-6.8a1 1 0 011.4 0z" clipRule="evenodd" />
                    </svg>
                    {p}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* ── Méthode ── */}
      <section id="methode" className="py-24 px-6 bg-slate-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <span className="text-indigo-600 font-semibold text-sm uppercase tracking-wide">Notre méthode</span>
            <h2 className="text-3xl sm:text-4xl font-bold mt-3">Simple, rapide, sans surprise</h2>
            <p className="text-slate-500 mt-4">De votre idée à un résultat en ligne, en trois étapes claires.</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {steps.map((st) => (
              <div key={st.n} className="relative bg-white rounded-2xl border border-slate-200 p-7">
                <div className="w-11 h-11 rounded-full bg-indigo-600 text-white font-bold flex items-center justify-center text-lg mb-4">{st.n}</div>
                <h3 className="text-lg font-bold">{st.title}</h3>
                <p className="text-slate-600 mt-2 text-sm leading-relaxed">{st.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Crédibilité / Notre force ── */}
      <section className="py-24 px-6 max-w-7xl mx-auto">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="text-indigo-600 font-semibold text-sm uppercase tracking-wide">Pourquoi nous faire confiance</span>
          <h2 className="text-3xl sm:text-4xl font-bold mt-3 tracking-tight">Une méthode rigoureuse, pas du hasard</h2>
          <p className="text-slate-500 mt-4">Ce qui se passe en coulisse pour que chaque livrable tienne la route.</p>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="rounded-2xl border border-slate-200 p-7 hover:shadow-lg transition-shadow">
            <div className="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-5">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
                <path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M12 3l7 4v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V7l7-4z" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <h3 className="text-lg font-bold tracking-tight">Sources officielles &amp; vérifiables</h3>
            <p className="text-slate-600 mt-2 text-sm leading-relaxed">
              Nos analyses s&apos;appuient sur des textes légaux et des données publiques que l&apos;on peut
              citer et tracer — pas sur des suppositions. Vous savez toujours d&apos;où vient l&apos;information.
            </p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-7 hover:shadow-lg transition-shadow">
            <div className="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-5">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
                <path d="M3 3v18h18" strokeLinecap="round" />
                <path d="M7 15l3-3 3 2 4-6" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            <h3 className="text-lg font-bold tracking-tight">Moteur de simulation multi-scénarios</h3>
            <p className="text-slate-600 mt-2 text-sm leading-relaxed">
              Avant chaque recommandation, on teste des milliers de scénarios pour ne garder que ce
              qui tient vraiment. Vous décidez sur des chiffres éprouvés, pas sur une intuition.
            </p>
          </div>
          <div className="rounded-2xl border border-slate-200 p-7 hover:shadow-lg transition-shadow">
            <div className="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-5">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-6 h-6">
                <circle cx="12" cy="8" r="4" />
                <path d="M4 21c0-4 3.5-6 8-6s8 2 8 6" strokeLinecap="round" />
              </svg>
            </div>
            <h3 className="text-lg font-bold tracking-tight">Supervision humaine systématique</h3>
            <p className="text-slate-600 mt-2 text-sm leading-relaxed">
              La puissance de l&apos;automatisation, toujours validée par un regard humain avant livraison.
              La rapidité de l&apos;IA, la fiabilité d&apos;un vrai suivi.
            </p>
          </div>
        </div>
      </section>

      {/* ── Approche / valeurs ── */}
      <section id="approche" className="py-24 px-6 max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <span className="text-indigo-600 font-semibold text-sm uppercase tracking-wide">Notre approche</span>
            <h2 className="text-3xl sm:text-4xl font-bold mt-3">Un partenaire, pas juste un prestataire</h2>
            <p className="text-slate-500 mt-4 leading-relaxed">
              Nous sommes une jeune structure à taille humaine. Ça veut dire un interlocuteur
              direct, des décisions rapides, et un vrai soin apporté à chaque projet — comme si
              c'était le nôtre.
            </p>
            <Link href="/contact"
              className="inline-block mt-8 bg-slate-900 hover:bg-slate-700 text-white font-semibold px-7 py-3 rounded-xl transition-colors">
              Parlons de votre projet
            </Link>
          </div>
          <div className="grid sm:grid-cols-2 gap-5">
            {values.map((v) => (
              <div key={v.title} className="rounded-xl border border-slate-200 p-5">
                <h3 className="font-semibold text-slate-900">{v.title}</h3>
                <p className="text-slate-500 text-sm mt-2 leading-relaxed">{v.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Services express ── */}
      <section className="py-20 px-6 bg-slate-50">
        <div className="max-w-5xl mx-auto text-center">
          <span className="text-indigo-600 font-semibold text-sm uppercase tracking-wide">Services express</span>
          <h2 className="text-3xl sm:text-4xl font-bold mt-3">Besoin d&apos;aller vite ? On est là.</h2>
          <p className="text-slate-500 mt-4 max-w-2xl mx-auto">La rapidité sans sacrifier la qualité — c&apos;est notre marque de fabrique.</p>
          <div className="grid sm:grid-cols-3 gap-5 mt-10">
            <div className="bg-white rounded-2xl border-2 border-emerald-300 p-6">
              <div className="text-emerald-600 font-bold text-sm">🎁 GRATUIT</div>
              <h3 className="text-lg font-bold mt-2">Audit express 24h</h3>
              <p className="text-slate-500 text-sm mt-2">Un diagnostic offert de votre site ou de votre besoin, sous 24h. Sans engagement.</p>
            </div>
            <div className="bg-white rounded-2xl border border-slate-200 p-6">
              <div className="text-indigo-600 font-bold text-sm">⚡ RAPIDE</div>
              <h3 className="text-lg font-bold mt-2">Devis en 1h</h3>
              <p className="text-slate-500 text-sm mt-2">Une réponse claire et un prix en moins d&apos;une heure. On ne vous fait pas attendre.</p>
            </div>
            <div className="bg-white rounded-2xl border border-slate-200 p-6">
              <div className="text-violet-600 font-bold text-sm">🚀 EXPRESS</div>
              <h3 className="text-lg font-bold mt-2">Site express 48h</h3>
              <p className="text-slate-500 text-sm mt-2">Pour les projets simples, votre site en ligne en 48h chrono.</p>
            </div>
          </div>
          <Link href="/contact" className="inline-block mt-10 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-emerald-600/20">
            Demander mon audit gratuit
          </Link>
        </div>
      </section>

      {/* ── CTA final ── */}
      <section className="py-24 px-6">
        <div className="max-w-4xl mx-auto rounded-3xl bg-gradient-to-br from-slate-900 to-slate-950 px-8 py-16 text-center relative overflow-hidden">
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.25),transparent_60%)]" />
          <div className="relative z-10">
            <h2 className="text-3xl sm:text-4xl font-bold text-white">Une idée ? Un besoin ?</h2>
            <p className="text-slate-300 mt-4 max-w-xl mx-auto">
              Parlons-en 20 minutes, sans engagement. On vous dit honnêtement ce qu'on peut
              faire pour vous — et combien ça coûte.
            </p>
            <Link href="/contact"
              className="inline-block mt-8 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-indigo-600/30">
              Demander un devis gratuit
            </Link>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t border-slate-100 py-10 px-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-slate-500">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-md flex items-center justify-center">
              <span className="text-white text-[10px] font-black">C</span>
            </div>
            <span className="font-semibold text-slate-700">Caelum</span>
            <span className="text-slate-400">· Studio web &amp; data · Bruxelles</span>
          </div>
          <div className="flex items-center gap-4 flex-wrap">
            <a href="#services" className="hover:text-slate-900">Services</a>
            <Link href="/assistant-reglementaire" className="hover:text-slate-900">Assistant réglementaire</Link>
            <Link href="/contact" className="hover:text-slate-900">Contact</Link>
            <Link href="/mentions-legales" className="hover:text-slate-900">Mentions légales</Link>
            <Link href="/confidentialite" className="hover:text-slate-900">Confidentialité</Link>
            <Link href="/cgv" className="hover:text-slate-900">CGV</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
