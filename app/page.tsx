import Link from "next/link";

const features = [
  {
    icon: "🔍",
    title: "Surveillance des Concurrents",
    desc: "Suivez en temps réel les changements de prix, fonctionnalités et stratégies de vos concurrents.",
  },
  {
    icon: "💰",
    title: "Analyse des Prix",
    desc: "Comparez les grilles tarifaires et détectez automatiquement toute variation de prix sur le marché.",
  },
  {
    icon: "📊",
    title: "Rapports Automatiques",
    desc: "Générez des rapports détaillés d'intelligence concurrentielle en un clic, prêts à partager.",
  },
];

const plans = [
  {
    name: "Starter",
    price: "29",
    color: "border-slate-200",
    badge: "",
    features: ["5 concurrents", "Alertes email", "Rapports mensuels", "Tableau de bord"],
  },
  {
    name: "Pro",
    price: "79",
    color: "border-indigo-500",
    badge: "Populaire",
    features: ["20 concurrents", "Alertes temps réel", "Rapports illimités", "API Access", "Export PDF"],
  },
  {
    name: "Enterprise",
    price: "199",
    color: "border-slate-200",
    badge: "",
    features: ["Illimité", "Alertes personnalisées", "Rapports sur mesure", "Support dédié", "SSO", "SLA 99,9%"],
  },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Nav */}
      <nav className="border-b border-slate-100 bg-white sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-bold">IQ</span>
            </div>
            <span className="text-lg font-bold text-slate-900">CompeteIQ</span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm text-slate-600">
            <a href="#features" className="hover:text-slate-900">Fonctionnalités</a>
            <a href="#pricing" className="hover:text-slate-900">Tarifs</a>
          </div>
          <Link
            href="/dashboard"
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
          >
            Accéder au Dashboard
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 py-24 text-center">
        <span className="inline-block bg-indigo-50 text-indigo-700 text-xs font-semibold px-3 py-1 rounded-full mb-6">
          Nouveau — IA intégrée pour l&apos;analyse concurrentielle
        </span>
        <h1 className="text-5xl font-bold text-slate-900 leading-tight mb-6 max-w-3xl mx-auto">
          L&apos;intelligence concurrentielle{" "}
          <span className="text-indigo-600">au service de votre croissance</span>
        </h1>
        <p className="text-xl text-slate-500 mb-10 max-w-2xl mx-auto">
          CompeteIQ vous permet de surveiller vos concurrents, analyser leur stratégie de prix et générer des rapports automatiques — tout en un seul outil.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/dashboard"
            className="bg-indigo-600 text-white px-8 py-3.5 rounded-lg text-base font-semibold hover:bg-indigo-700 transition-colors"
          >
            Commencer gratuitement
          </Link>
          <a
            href="#features"
            className="border border-slate-200 text-slate-700 px-8 py-3.5 rounded-lg text-base font-semibold hover:bg-slate-50 transition-colors"
          >
            Voir la démo
          </a>
        </div>
        <p className="text-sm text-slate-400 mt-4">Aucune carte bancaire requise · 14 jours d&apos;essai gratuit</p>

        {/* Hero visual */}
        <div className="mt-16 bg-slate-900 rounded-2xl p-6 text-left max-w-4xl mx-auto shadow-2xl">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-slate-500 text-xs ml-2">competeiq.io/dashboard</span>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            {[
              { label: "Concurrents suivis", value: "5", color: "text-indigo-400" },
              { label: "Alertes actives", value: "3", color: "text-amber-400" },
              { label: "Rapports générés", value: "3", color: "text-emerald-400" },
              { label: "Score de marché", value: "74%", color: "text-rose-400" },
            ].map((s) => (
              <div key={s.label} className="bg-slate-800 rounded-xl p-4">
                <p className="text-slate-400 text-xs mb-1">{s.label}</p>
                <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
              </div>
            ))}
          </div>
          <div className="space-y-2">
            {["Salesforce", "HubSpot", "Pipedrive"].map((c, i) => (
              <div key={c} className="flex items-center gap-3 bg-slate-800 rounded-lg px-4 py-2.5">
                <div className="w-6 h-6 rounded bg-indigo-600 flex items-center justify-center text-white text-xs font-bold">
                  {c[0]}
                </div>
                <span className="text-slate-200 text-sm flex-1">{c}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${i === 0 ? "bg-red-900/50 text-red-400" : i === 1 ? "bg-red-900/50 text-red-400" : "bg-amber-900/50 text-amber-400"}`}>
                  {i < 2 ? "Élevée" : "Moyenne"}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="bg-slate-50 py-24">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-slate-900 text-center mb-4">Tout ce dont vous avez besoin</h2>
          <p className="text-slate-500 text-center mb-16 max-w-xl mx-auto">
            Une plateforme complète pour comprendre votre marché et prendre des décisions éclairées.
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((f) => (
              <div key={f.title} className="bg-white rounded-2xl p-8 border border-slate-100 shadow-sm">
                <div className="text-4xl mb-4">{f.icon}</div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">{f.title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-24">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-slate-900 text-center mb-4">Tarifs simples et transparents</h2>
          <p className="text-slate-500 text-center mb-16">Commencez gratuitement, évoluez selon vos besoins.</p>
          <div className="grid md:grid-cols-3 gap-8">
            {plans.map((p) => (
              <div key={p.name} className={`rounded-2xl border-2 ${p.color} p-8 relative`}>
                {p.badge && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-indigo-600 text-white text-xs font-bold px-3 py-1 rounded-full">
                    {p.badge}
                  </span>
                )}
                <h3 className="text-xl font-bold text-slate-900 mb-2">{p.name}</h3>
                <div className="flex items-end gap-1 mb-6">
                  <span className="text-4xl font-bold text-slate-900">{p.price}€</span>
                  <span className="text-slate-400 mb-1">/mois</span>
                </div>
                <ul className="space-y-3 mb-8">
                  {p.features.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-sm text-slate-600">
                      <span className="text-emerald-500">✓</span> {f}
                    </li>
                  ))}
                </ul>
                <Link
                  href="/dashboard"
                  className={`block text-center py-3 rounded-lg text-sm font-semibold transition-colors ${p.badge ? "bg-indigo-600 text-white hover:bg-indigo-700" : "border border-slate-200 text-slate-700 hover:bg-slate-50"}`}
                >
                  Commencer
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-100 py-8">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-indigo-600 rounded flex items-center justify-center">
              <span className="text-white text-xs font-bold">IQ</span>
            </div>
            <span className="text-sm font-semibold text-slate-700">CompeteIQ</span>
          </div>
          <p className="text-xs text-slate-400">© 2026 CompeteIQ. Tous droits réservés.</p>
        </div>
      </footer>
    </div>
  );
}
