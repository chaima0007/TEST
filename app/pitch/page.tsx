"use client";

import { useState } from "react";
import Link from "next/link";

export default function PitchPage() {
  const [formData, setFormData] = useState({
    nom: "",
    entreprise: "",
    poste: "",
    ca: "",
    message: "",
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-white text-slate-900 font-sans">

      {/* ── HEADER ── */}
      <header className="border-b border-slate-200 bg-white sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
              style={{ background: "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)" }}>
              <span className="text-xs font-black tracking-tight" style={{ color: "#D4AF37" }}>IQ</span>
            </div>
            <div>
              <span className="text-lg font-black text-slate-900 tracking-tight">CompeteIQ</span>
              <span className="hidden sm:inline text-xs text-slate-400 ml-2 font-medium">— Intelligence Stratégique</span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-2 border border-amber-200 bg-amber-50 rounded-full px-4 py-1.5">
              <svg className="w-3.5 h-3.5 text-amber-600" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5 9V7a5 5 0 0 1 10 0v2a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2Zm8-2v2H7V7a3 3 0 0 1 6 0Z" clipRule="evenodd" />
              </svg>
              <span className="text-xs font-bold text-amber-700 uppercase tracking-widest">
                Document confidentiel — Réservé aux décideurs
              </span>
            </div>
            <Link href="/"
              className="text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors px-3 py-1.5 rounded-lg hover:bg-slate-100">
              Retour au site
            </Link>
          </div>
        </div>
      </header>

      {/* ── HERO ── */}
      <section className="py-28 px-6" style={{ background: "linear-gradient(135deg, #0a0a0a 0%, #111827 50%, #0f172a 100%)" }}>
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 border rounded-full px-5 py-2 mb-10 text-xs font-bold uppercase tracking-widest"
            style={{ borderColor: "rgba(212,175,55,0.3)", color: "#D4AF37", background: "rgba(212,175,55,0.08)" }}>
            <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ backgroundColor: "#D4AF37" }} />
            Intelligence Concurrentielle de Rang Enterprise
          </div>

          <h1 className="text-5xl md:text-6xl font-black leading-tight mb-8 text-white tracking-tight">
            Chaque décision stratégique que vos
            <br />
            <span className="relative inline-block mt-2">
              <span style={{ color: "#D4AF37" }}>concurrents prennent</span>
            </span>
            <br />
            <span className="text-white">vous coûte de l&apos;argent.</span>
          </h1>

          <p className="text-slate-300 text-xl max-w-3xl mx-auto mb-6 leading-relaxed font-light">
            CompeteIQ vous le dit avant eux.
          </p>

          <p className="text-slate-500 text-base max-w-2xl mx-auto mb-14 leading-relaxed">
            Nous ne sommes pas un outil de veille. Nous sommes le partenaire stratégique que vos concurrents
            n&apos;ont pas encore découvert — et qui fait toute la différence.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="#contact"
              className="inline-flex items-center justify-center gap-2 text-slate-900 font-black text-base px-10 py-4 rounded-xl transition-all shadow-2xl hover:-translate-y-0.5"
              style={{ background: "linear-gradient(135deg, #D4AF37 0%, #f0d060 100%)" }}>
              Planifier une démonstration stratégique
              <svg className="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clipRule="evenodd" />
              </svg>
            </a>
            <a href="#tarifs"
              className="inline-flex items-center justify-center gap-2 text-white font-semibold text-base px-10 py-4 rounded-xl transition-all border border-white/10 hover:bg-white/5">
              Voir les offres
            </a>
          </div>
        </div>
      </section>

      {/* ── COÛT DE L'IGNORANCE ── */}
      <section className="py-24 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="mb-16 text-center">
            <span className="font-bold text-sm uppercase tracking-widest" style={{ color: "#D4AF37" }}>
              Le coût de l&apos;ignorance concurrentielle
            </span>
            <h2 className="text-4xl font-black mt-3 text-slate-900 leading-tight">
              Ce que vous ne savez pas vous coûte déjà
            </h2>
            <p className="text-slate-500 text-lg mt-4 max-w-2xl mx-auto">
              Les chiffres que vos concurrents ne veulent pas que vous connaissiez.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                stat: "340 K€",
                source: "Bain & Company, 2024",
                title: "Coût moyen d’une réaction tardive",
                desc: "C’est le manque à gagner médian subi par une ETI lorsqu’elle détecte avec plus de 3 semaines de retard un mouvement pricing de son concurrent principal. Marge perdue, clients churned, renégociations forcées.",
                color: "border-rose-200 bg-rose-50",
                statColor: "text-rose-600",
              },
              {
                stat: "73 %",
                source: "Forrester Research, 2025",
                title: "Des décisions stratégiques sur données périmées",
                desc: "Près des trois quarts des comités de direction prennent leurs décisions d’investissement produit et de positionnement tarifaire sur des données concurrentielles vieilles de plus de 6 mois. Le marché n’attend pas.",
                color: "border-amber-200 bg-amber-50",
                statColor: "text-amber-600",
              },
              {
                stat: "21 jours",
                source: "IDC Market Pulse, 2025",
                title: "Délai moyen de détection d’un mouvement concurrent",
                desc: "En l’absence de veille structurée, les entreprises apprennent les lancements produits, baisses de prix et acquisitions de leurs concurrents par leurs propres clients — en moyenne 3 semaines après l’événement.",
                color: "border-slate-200 bg-slate-50",
                statColor: "text-slate-800",
              },
            ].map((item) => (
              <div key={item.title} className={`border-2 rounded-2xl p-8 ${item.color}`}>
                <p className={`text-5xl font-black mb-2 ${item.statColor}`}>{item.stat}</p>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">{item.source}</p>
                <h3 className="font-black text-slate-900 text-lg mb-3 leading-snug">{item.title}</h3>
                <p className="text-slate-600 text-sm leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── NOTRE APPROCHE ── */}
      <section className="py-24 px-6" style={{ background: "#0a0a0a" }}>
        <div className="max-w-6xl mx-auto">
          <div className="mb-16 text-center">
            <span className="font-bold text-sm uppercase tracking-widest" style={{ color: "#D4AF37" }}>
              Notre approche
            </span>
            <h2 className="text-4xl font-black mt-3 text-white leading-tight">
              Pas un outil. Un partenaire stratégique.
            </h2>
            <p className="text-slate-400 text-lg mt-4 max-w-2xl mx-auto">
              CompeteIQ déploie trois piliers interdépendants pour transformer votre intelligence
              concurrentielle en avantage compétitif durable.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-1">
            {[
              {
                number: "01",
                pilier: "Surveillance",
                title: "Capturer chaque signal avant vos concurrents",
                desc: "Monitoring 24h/24 de plus de 200 sources structurées et non-structurées : pages pricing, job postings, levées de fonds, brevets déposés, communiqués de presse, avis clients, mouvements RH. Aucun signal faible ne passe au travers.",
                features: ["Crawling temps réel sur 200+ sources", "Détection de signaux faibles par NLP", "Alertes configurables sous 15 minutes"],
              },
              {
                number: "02",
                pilier: "Analyse",
                title: "Transformer les données en décisions actionnables",
                desc: "Nos analystes seniors et notre moteur IA synthétisent les signaux en recommandations stratégiques prêtes pour le CODIR. Pas des tableaux de données — des analyses contextualisées avec impact business chiffré.",
                features: ["Rapports CODIR clé-en-main", "Modélisation d’impact financier", "Benchmarks sectoriels trimestriels"],
              },
              {
                number: "03",
                pilier: "Action",
                title: "Passer de l’insight à l’exécution en 48h",
                desc: "Un CSM dédié orchestre la transformation de chaque alerte en plan d’action. Revues stratégiques mensuelles avec votre équipe dirigeante. Recommandations pricing, produit et go-to-market calibrées pour votre contexte spécifique.",
                features: ["CSM Senior dédié (offre Stratégique)", "Revues mensuelles avec le CODIR", "Plans d’action sous 48h garantis"],
              },
            ].map((p, i) => (
              <div key={p.pilier}
                className={`p-10 ${i === 1 ? "border-x border-white/10" : ""}`}
                style={{ background: i === 1 ? "rgba(212,175,55,0.05)" : "transparent" }}>
                <div className="flex items-center gap-3 mb-6">
                  <span className="text-xs font-black uppercase tracking-widest" style={{ color: "#D4AF37" }}>{p.number}</span>
                  <div className="h-px flex-1" style={{ background: "rgba(212,175,55,0.3)" }} />
                  <span className="text-xs font-black uppercase tracking-widest text-white">{p.pilier}</span>
                </div>
                <h3 className="font-black text-white text-xl mb-4 leading-snug">{p.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed mb-6">{p.desc}</p>
                <ul className="space-y-2.5">
                  {p.features.map((f) => (
                    <li key={f} className="flex items-start gap-2.5 text-sm text-slate-300">
                      <svg className="w-4 h-4 flex-shrink-0 mt-0.5" viewBox="0 0 16 16" fill="currentColor" style={{ color: "#D4AF37" }}>
                        <path fillRule="evenodd" d="M12.416 3.376a.75.75 0 0 1 .208 1.04l-5 7.5a.75.75 0 0 1-1.154.114l-3-3a.75.75 0 0 1 1.06-1.06l2.353 2.353 4.493-6.74a.75.75 0 0 1 1.04-.207Z" clipRule="evenodd" />
                      </svg>
                      {f}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── PREUVES SOCIALES ── */}
      <section className="py-24 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="mb-16 text-center">
            <span className="font-bold text-sm uppercase tracking-widest" style={{ color: "#D4AF37" }}>
              Résultats clients
            </span>
            <h2 className="text-4xl font-black mt-3 text-slate-900 leading-tight">
              Le ROI n&apos;est pas une promesse. C&apos;est un historique.
            </h2>
            <p className="text-slate-500 text-lg mt-4 max-w-2xl mx-auto">
              Trois exemples parmi les 240+ entreprises qui nous font confiance.
            </p>
          </div>

          <div className="space-y-6">
            {[
              {
                secteur: "ETI Industrielle — Équipements B2B",
                ca: "85 M€ de CA",
                employes: "420 collaborateurs",
                badge: "12 M€ préservés",
                badgeColor: "bg-emerald-100 text-emerald-800 border border-emerald-200",
                title: "Alerte pricing J-14 : 12 M€ de chiffre d’affaires préservé",
                quote: "Nous avons reçu l’alerte CompeteIQ un mercredi matin. Notre principal concurrent allait baisser ses prix de 18% sur notre segment core trois jours plus tard. Nous avons convoqué un CODIR d’urgence, ajusté notre politique tarifaire et anticipé la communication clients. Sans CompeteIQ, nous aurions perdu entre 10 et 14 millions d’euros de contrats en cours de renouvellement.",
                auteur: "Directeur Commercial",
                resultats: ["Détection 14 jours avant l’annonce officielle", "Rétention de 97% des contrats en renouvellement", "ROI CompeteIQ : 124× sur l’année"],
              },
              {
                secteur: "Groupe Retail — Distribution Nationale",
                ca: "320 M€ de CA",
                employes: "1 800 collaborateurs",
                badge: "+38% parts de marché",
                badgeColor: "bg-blue-100 text-blue-800 border border-blue-200",
                title: "Lancement produit repositionné : +38% de parts de marché en 6 mois",
                quote: "Notre lancement prévu pour septembre allait droit dans le mur. CompeteIQ nous a montré en août que deux de nos concurrents principaux lançaient simultanément des produits très proches. Nous avons décalé d’un mois, repositionné notre angle marketing sur un segment adjacent et lancé avec un avantage différenciant clair. Le résultat a dépassé toutes nos projections.",
                auteur: "Directrice Marketing & Innovation",
                resultats: ["+38 points de parts de marché sur la catégorie", "Lancement repositionné en 4 semaines", "Économie de 2,3 M€ sur le budget d’acquisition client"],
              },
              {
                secteur: "SaaS B2B — Logiciels RH",
                ca: "Série A en cours",
                employes: "65 collaborateurs",
                badge: "Levée accélérée",
                badgeColor: "bg-purple-100 text-purple-800 border border-purple-200",
                title: "Dossier concurrentiel CompeteIQ : levée de fonds accélérée de 4 mois",
                quote: "Nos investisseurs nous demandaient systématiquement pourquoi nous gagnerions face à nos concurrents. Avec le dossier concurrentiel CompeteIQ, nous avions des réponses précises, sourcées, actualisées en temps réel. Le lead investor a qualifié notre niveau de connaissance marché d’exceptionnel. Nous avons closé notre Série A en 8 semaines au lieu des 12 à 14 habituelles.",
                auteur: "CEO & Co-fondateur",
                resultats: ["Levée de 4,2 M€ — Série A closée en 8 semaines", "Valorisation supérieure de 22% aux estimations initiales", "Dossier concurrentiel complet généré en 48h"],
              },
            ].map((cas) => (
              <div key={cas.title} className="border border-slate-200 rounded-2xl p-8 hover:border-slate-300 transition-colors">
                <div className="flex flex-col lg:flex-row gap-8">
                  <div className="flex-1">
                    <div className="flex flex-wrap items-center gap-3 mb-5">
                      <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">{cas.secteur}</span>
                      <span className="text-xs text-slate-400">·</span>
                      <span className="text-xs text-slate-500">{cas.ca}</span>
                      <span className="text-xs text-slate-400">·</span>
                      <span className="text-xs text-slate-500">{cas.employes}</span>
                      <span className={`text-xs font-black px-3 py-1 rounded-full ml-auto lg:ml-0 ${cas.badgeColor}`}>
                        {cas.badge}
                      </span>
                    </div>
                    <h3 className="font-black text-slate-900 text-xl mb-4 leading-snug">{cas.title}</h3>
                    <blockquote className="text-slate-600 text-sm leading-relaxed italic border-l-2 pl-4 mb-4" style={{ borderColor: "#D4AF37" }}>
                      &quot;{cas.quote}&quot;
                    </blockquote>
                    <p className="text-xs text-slate-400 font-medium">— {cas.auteur}</p>
                  </div>
                  <div className="lg:w-72 bg-slate-50 rounded-xl p-6 border border-slate-100">
                    <p className="text-xs font-black text-slate-400 uppercase tracking-widest mb-4">Résultats mesurés</p>
                    <ul className="space-y-3">
                      {cas.resultats.map((r) => (
                        <li key={r} className="flex items-start gap-2.5 text-sm text-slate-700 font-medium">
                          <svg className="w-4 h-4 flex-shrink-0 mt-0.5" viewBox="0 0 16 16" fill="currentColor" style={{ color: "#D4AF37" }}>
                            <path fillRule="evenodd" d="M12.416 3.376a.75.75 0 0 1 .208 1.04l-5 7.5a.75.75 0 0 1-1.154.114l-3-3a.75.75 0 0 1 1.06-1.06l2.353 2.353 4.493-6.74a.75.75 0 0 1 1.04-.207Z" clipRule="evenodd" />
                          </svg>
                          {r}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Badges de confiance */}
          <div className="mt-14 flex flex-wrap justify-center gap-8 items-center">
            {[
              { label: "240+ entreprises clientes", icon: "building" },
              { label: "NDA sur demande", icon: "lock" },
              { label: "RGPD conforme", icon: "shield" },
              { label: "SLA 99,9%", icon: "check" },
              { label: "ISO 27001 (en cours)", icon: "cert" },
            ].map((badge) => (
              <div key={badge.label} className="flex items-center gap-2 text-sm font-semibold text-slate-500">
                <svg className="w-4 h-4 text-slate-400" viewBox="0 0 16 16" fill="currentColor">
                  <path fillRule="evenodd" d="M12.416 3.376a.75.75 0 0 1 .208 1.04l-5 7.5a.75.75 0 0 1-1.154.114l-3-3a.75.75 0 0 1 1.06-1.06l2.353 2.353 4.493-6.74a.75.75 0 0 1 1.04-.207Z" clipRule="evenodd" />
                </svg>
                {badge.label}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── GRILLE TARIFAIRE ── */}
      <section id="tarifs" className="py-24 px-6 bg-slate-50">
        <div className="max-w-6xl mx-auto">
          <div className="mb-16 text-center">
            <span className="font-bold text-sm uppercase tracking-widest" style={{ color: "#D4AF37" }}>
              Offres & Tarification
            </span>
            <h2 className="text-4xl font-black mt-3 text-slate-900 leading-tight">
              Investissez dans votre avantage concurrentiel
            </h2>
            <p className="text-slate-500 text-lg mt-4 max-w-2xl mx-auto">
              Chaque offre est pensée pour un profil d&apos;organisation spécifique.
              Tous les plans incluent une période d&apos;essai de 14 jours, sans engagement.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {/* Essentiel */}
            <div className="bg-white border-2 border-slate-200 rounded-2xl p-8">
              <div className="mb-6">
                <p className="text-xs font-black uppercase tracking-widest text-slate-400 mb-2">Essentiel</p>
                <div className="flex items-baseline gap-1 mb-1">
                  <span className="text-5xl font-black text-slate-900">990</span>
                  <span className="text-xl font-bold text-slate-500">€</span>
                  <span className="text-slate-400 text-sm font-medium">/mois</span>
                </div>
                <p className="text-xs text-slate-400">Engagé annuellement — soit 11 880 €/an</p>
              </div>
              <p className="text-sm text-slate-600 mb-6 leading-relaxed">
                Pour les PME qui veulent passer d&apos;une veille artisanale à une surveillance structurée de leur environnement concurrentiel.
              </p>
              <ul className="space-y-3 mb-8">
                {[
                  "Jusqu’à 10 concurrents surveillés",
                  "Rapports mensuels automatisés",
                  "Alertes email configurables",
                  "Dashboard temps réel",
                  "Support email (J+2)",
                  "Onboarding guidé inclus",
                ].map((f) => (
                  <li key={f} className="flex items-start gap-2.5 text-sm text-slate-700">
                    <svg className="w-4 h-4 flex-shrink-0 mt-0.5 text-slate-400" viewBox="0 0 16 16" fill="currentColor">
                      <path fillRule="evenodd" d="M12.416 3.376a.75.75 0 0 1 .208 1.04l-5 7.5a.75.75 0 0 1-1.154.114l-3-3a.75.75 0 0 1 1.06-1.06l2.353 2.353 4.493-6.74a.75.75 0 0 1 1.04-.207Z" clipRule="evenodd" />
                    </svg>
                    {f}
                  </li>
                ))}
              </ul>
              <a href="#contact"
                className="block w-full text-center py-3.5 rounded-xl font-bold text-slate-700 border-2 border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition-all text-sm">
                Démarrer l&apos;essai gratuit
              </a>
            </div>

            {/* Performance */}
            <div className="relative bg-white border-2 rounded-2xl p-8 shadow-2xl"
              style={{ borderColor: "#D4AF37" }}>
              <div className="absolute -top-4 left-1/2 -translate-x-1/2 text-slate-900 text-xs font-black px-5 py-1.5 rounded-full shadow-lg"
                style={{ background: "linear-gradient(135deg, #D4AF37 0%, #f0d060 100%)" }}>
                LE PLUS CHOISI
              </div>
              <div className="mb-6">
                <p className="text-xs font-black uppercase tracking-widest mb-2" style={{ color: "#D4AF37" }}>Performance</p>
                <div className="flex items-baseline gap-1 mb-1">
                  <span className="text-5xl font-black text-slate-900">2 490</span>
                  <span className="text-xl font-bold text-slate-500">€</span>
                  <span className="text-slate-400 text-sm font-medium">/mois</span>
                </div>
                <p className="text-xs text-slate-400">Engagé annuellement — soit 29 880 €/an</p>
              </div>
              <p className="text-sm text-slate-600 mb-6 leading-relaxed">
                Pour les ETI et entreprises en croissance qui ont besoin d&apos;une veille temps réel pour alimenter leurs décisions commerciales et produit.
              </p>
              <ul className="space-y-3 mb-8">
                {[
                  "Jusqu’à 25 concurrents surveillés",
                  "Rapports hebdomadaires automatisés",
                  "Alertes temps réel (délai < 15 min)",
                  "Accès API complet",
                  "Intégrations Slack, Teams, HubSpot",
                  "Support prioritaire (J+4h)",
                  "Analyse prédictive des prix",
                  "Export PPTX pour le CODIR",
                ].map((f) => (
                  <li key={f} className="flex items-start gap-2.5 text-sm text-slate-700">
                    <svg className="w-4 h-4 flex-shrink-0 mt-0.5" viewBox="0 0 16 16" fill="currentColor" style={{ color: "#D4AF37" }}>
                      <path fillRule="evenodd" d="M12.416 3.376a.75.75 0 0 1 .208 1.04l-5 7.5a.75.75 0 0 1-1.154.114l-3-3a.75.75 0 0 1 1.06-1.06l2.353 2.353 4.493-6.74a.75.75 0 0 1 1.04-.207Z" clipRule="evenodd" />
                    </svg>
                    {f}
                  </li>
                ))}
              </ul>
              <a href="#contact"
                className="block w-full text-center py-3.5 rounded-xl font-black text-slate-900 transition-all text-sm hover:-translate-y-0.5 shadow-lg"
                style={{ background: "linear-gradient(135deg, #D4AF37 0%, #f0d060 100%)" }}>
                Démarrer l&apos;essai gratuit
              </a>
            </div>

            {/* Stratégique */}
            <div className="bg-slate-900 border-2 border-slate-700 rounded-2xl p-8 text-white">
              <div className="mb-6">
                <p className="text-xs font-black uppercase tracking-widest text-slate-400 mb-2">Stratégique</p>
                <div className="flex items-baseline gap-1 mb-1">
                  <span className="text-3xl font-black text-white leading-none">Sur devis</span>
                </div>
                <p className="text-xs font-bold mt-1" style={{ color: "#D4AF37" }}>À partir de 6 500 €/mois</p>
              </div>
              <p className="text-sm text-slate-400 mb-6 leading-relaxed">
                Pour les Grands Comptes et groupes qui exigent un niveau de service partenaire — SLA garanti, CSM dédié et rapports CODIR sur mesure.
              </p>
              <ul className="space-y-3 mb-8">
                {[
                  "Concurrents illimités",
                  "Rapports CODIR sur mesure",
                  "CSM Senior dédié",
                  "SLA garanti 99,9% (contractuel)",
                  "SSO / SAML / SCIM",
                  "Audit logs immuables",
                  "Data résidence EU garantie",
                  "Revues stratégiques mensuelles",
                  "Formation équipes dirigeantes",
                ].map((f) => (
                  <li key={f} className="flex items-start gap-2.5 text-sm text-slate-300">
                    <svg className="w-4 h-4 flex-shrink-0 mt-0.5" viewBox="0 0 16 16" fill="currentColor" style={{ color: "#D4AF37" }}>
                      <path fillRule="evenodd" d="M12.416 3.376a.75.75 0 0 1 .208 1.04l-5 7.5a.75.75 0 0 1-1.154.114l-3-3a.75.75 0 0 1 1.06-1.06l2.353 2.353 4.493-6.74a.75.75 0 0 1 1.04-.207Z" clipRule="evenodd" />
                    </svg>
                    {f}
                  </li>
                ))}
              </ul>
              <a href="#contact"
                className="block w-full text-center py-3.5 rounded-xl font-bold transition-all text-sm border border-white/20 hover:bg-white/10 text-white">
                Demander un devis personnalisé
              </a>
            </div>
          </div>

          <p className="text-center text-sm text-slate-400 mt-8">
            Tous les prix sont HT. Engagement annuel. Paiement mensuel ou annuel disponible.
            <br />
            Offre sur mesure disponible pour les groupes &gt; 5 000 collaborateurs.
          </p>
        </div>
      </section>

      {/* ── PROCESSUS D'ONBOARDING ── */}
      <section className="py-24 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="mb-16 text-center">
            <span className="font-bold text-sm uppercase tracking-widest" style={{ color: "#D4AF37" }}>
              Processus d&apos;onboarding
            </span>
            <h2 className="text-4xl font-black mt-3 text-slate-900 leading-tight">
              Opérationnel en 2 heures. Sérieusement.
            </h2>
            <p className="text-slate-500 text-lg mt-4 max-w-2xl mx-auto">
              Notre processus d&apos;activation a été conçu pour zéro friction. Vous prenez une décision de 6 chiffres — le démarrage doit être à la hauteur.
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-6 relative">
            <div className="hidden md:block absolute top-12 left-[12.5%] right-[12.5%] h-px bg-slate-200" />

            {[
              {
                step: "01",
                duration: "15 min",
                title: "Signature du NDA",
                desc: "Accord de confidentialité mutuel signé électroniquement. Vos informations stratégiques restent dans un cadre légal dès le premier échange.",
              },
              {
                step: "02",
                duration: "45 min",
                title: "Brief stratégique",
                desc: "Session de découverte avec votre CSM dédié : cartographie de vos concurrents prioritaires, objectifs stratégiques, signaux à surveiller.",
              },
              {
                step: "03",
                duration: "30 min",
                title: "Configuration",
                desc: "Paramétrage de votre espace, activation des alertes, intégration avec vos outils (Slack, Teams, CRM). Zéro effort IT de votre côté.",
              },
              {
                step: "04",
                duration: "Go-live",
                title: "Mise en surveillance",
                desc: "Vos premiers rapports arrivent dans les 24h. Votre premier brief stratégique avec insights actionnables est remis dans la semaine.",
              },
            ].map((etape, i) => (
              <div key={etape.step} className="relative flex flex-col items-center text-center">
                <div className="relative mb-6 flex items-center justify-center">
                  <div className="w-24 h-24 rounded-full border-2 bg-white flex flex-col items-center justify-center z-10 shadow-sm"
                    style={{ borderColor: "#D4AF37" }}>
                    <span className="text-xs font-black uppercase tracking-widest" style={{ color: "#D4AF37" }}>{etape.step}</span>
                    <span className="text-xs text-slate-500 font-medium mt-0.5">{etape.duration}</span>
                  </div>
                </div>
                <h3 className="font-black text-slate-900 text-base mb-2">{etape.title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{etape.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── ÉQUIPE ── */}
      <section className="py-24 px-6 bg-slate-50">
        <div className="max-w-6xl mx-auto">
          <div className="mb-16 text-center">
            <span className="font-bold text-sm uppercase tracking-widest" style={{ color: "#D4AF37" }}>
              L&apos;équipe
            </span>
            <h2 className="text-4xl font-black mt-3 text-slate-900 leading-tight">
              Des experts qui ont fait leurs preuves
            </h2>
            <p className="text-slate-500 text-lg mt-4 max-w-2xl mx-auto">
              CompeteIQ est construit par des professionnels qui ont opéré dans les environnements
              les plus exigeants — conseil stratégique, data engineering, gestion de grands comptes.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {[
              {
                initiales: "ML",
                nom: "Marc Lefèvre",
                titre: "Head of Strategic Intelligence",
                ancien: "McKinsey & Company · 8 ans",
                desc: "Ex-consultant Senior chez McKinsey, spécialisé en stratégie compétitive et due diligence concurrentielle pour des groupes du CAC 40. A dirigé plus de 60 missions d’intelligence stratégique en Europe.",
                tags: ["Stratégie", "M&A", "CAC 40", "Intelligence compétitive"],
              },
              {
                initiales: "SC",
                nom: "Sophie Chen",
                titre: "Lead Data Engineer",
                ancien: "Palantir Technologies · 6 ans",
                desc: "Ancienne Data Engineer chez Palantir où elle a architecé des pipelines de traitement de données pour des clients gouvernementaux et industriels. Experte en NLP appliqué à l’analyse de marché.",
                tags: ["Data Engineering", "NLP", "IA", "Temps réel"],
              },
              {
                initiales: "AT",
                nom: "Alexandre Tournier",
                titre: "VP Customer Success",
                ancien: "Gartner · 10 ans",
                desc: "Ancien directeur de comptes stratégiques chez Gartner, il a accompagné plus de 80 COMEX dans la structuration de leur veille et leur processus de décision basé sur la donnée marché.",
                tags: ["Grands Comptes", "CODIR", "Change Management"],
              },
            ].map((personne) => (
              <div key={personne.nom} className="bg-white border border-slate-200 rounded-2xl p-8">
                <div className="flex items-center gap-4 mb-5">
                  <div className="w-14 h-14 rounded-xl flex items-center justify-center text-white font-black text-lg flex-shrink-0"
                    style={{ background: "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)" }}>
                    {personne.initiales}
                  </div>
                  <div>
                    <p className="font-black text-slate-900 text-base">{personne.nom}</p>
                    <p className="text-sm font-semibold text-slate-500">{personne.titre}</p>
                    <p className="text-xs mt-0.5 font-bold" style={{ color: "#D4AF37" }}>
                      ex-{personne.ancien}
                    </p>
                  </div>
                </div>
                <p className="text-slate-600 text-sm leading-relaxed mb-5">{personne.desc}</p>
                <div className="flex flex-wrap gap-2">
                  {personne.tags.map((tag) => (
                    <span key={tag} className="text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-600">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA & FORMULAIRE ── */}
      <section id="contact" className="py-28 px-6" style={{ background: "linear-gradient(135deg, #0a0a0a 0%, #111827 50%, #0f172a 100%)" }}>
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <span className="font-bold text-sm uppercase tracking-widest" style={{ color: "#D4AF37" }}>
              Prochaine étape
            </span>
            <h2 className="text-4xl md:text-5xl font-black mt-3 text-white leading-tight">
              Planifier une démonstration stratégique
            </h2>
            <p className="text-slate-400 text-lg mt-4 max-w-2xl mx-auto">
              30 minutes avec un expert CompeteIQ. Nous analysons votre paysage concurrentiel
              en direct et vous montrons ce que nous détecterions dès demain.
            </p>
          </div>

          {submitted ? (
            <div className="max-w-xl mx-auto bg-white/5 border border-white/10 rounded-2xl p-12 text-center">
              <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6"
                style={{ background: "rgba(212,175,55,0.15)", border: "2px solid rgba(212,175,55,0.4)" }}>
                <svg className="w-8 h-8" viewBox="0 0 20 20" fill="currentColor" style={{ color: "#D4AF37" }}>
                  <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="text-white font-black text-2xl mb-3">Demande reçue.</h3>
              <p className="text-slate-400 leading-relaxed">
                Votre CSM dédié vous contactera dans les 4 heures ouvrées pour confirmer votre créneau.
                Préparez-vous pour une démonstration qui changera votre regard sur votre marché.
              </p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="max-w-2xl mx-auto space-y-5">
              <div className="grid sm:grid-cols-2 gap-5">
                <div>
                  <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                    Nom complet *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.nom}
                    onChange={(e) => setFormData({ ...formData, nom: e.target.value })}
                    placeholder="Jean Dupont"
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-slate-600 text-sm focus:outline-none focus:border-amber-400/50 transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                    Entreprise *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.entreprise}
                    onChange={(e) => setFormData({ ...formData, entreprise: e.target.value })}
                    placeholder="Groupe Dupont SA"
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-slate-600 text-sm focus:outline-none focus:border-amber-400/50 transition-colors"
                  />
                </div>
              </div>
              <div className="grid sm:grid-cols-2 gap-5">
                <div>
                  <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                    Poste *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.poste}
                    onChange={(e) => setFormData({ ...formData, poste: e.target.value })}
                    placeholder="Directeur Commercial"
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-slate-600 text-sm focus:outline-none focus:border-amber-400/50 transition-colors"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                    CA de l&apos;entreprise
                  </label>
                  <select
                    value={formData.ca}
                    onChange={(e) => setFormData({ ...formData, ca: e.target.value })}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white text-sm focus:outline-none focus:border-amber-400/50 transition-colors appearance-none"
                    style={{ background: "rgba(255,255,255,0.05)" }}>
                    <option value="" className="bg-slate-900">Sélectionner</option>
                    <option value="< 5M€" className="bg-slate-900">Moins de 5 M€</option>
                    <option value="5-25M€" className="bg-slate-900">5 à 25 M€</option>
                    <option value="25-100M€" className="bg-slate-900">25 à 100 M€</option>
                    <option value="100-500M€" className="bg-slate-900">100 à 500 M€</option>
                    <option value="> 500M€" className="bg-slate-900">Plus de 500 M€</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                  Contexte & objectifs (optionnel)
                </label>
                <textarea
                  rows={4}
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  placeholder="Décrivez votre environnement concurrentiel, vos enjeux actuels, ce que vous cherchez à résoudre..."
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-slate-600 text-sm focus:outline-none focus:border-amber-400/50 transition-colors resize-none"
                />
              </div>
              <button
                type="submit"
                className="w-full py-4 rounded-xl font-black text-slate-900 text-base transition-all hover:-translate-y-0.5 shadow-xl"
                style={{ background: "linear-gradient(135deg, #D4AF37 0%, #f0d060 100%)" }}>
                Planifier ma démonstration stratégique
              </button>
              <p className="text-center text-xs text-slate-600">
                Réponse garantie sous 4h ouvrées · NDA disponible sur demande · Échange 100% confidentiel
              </p>
            </form>
          )}
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer className="border-t py-10 px-6" style={{ background: "#050505", borderColor: "rgba(255,255,255,0.05)" }}>
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg flex items-center justify-center"
              style={{ background: "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)", border: "1px solid rgba(212,175,55,0.3)" }}>
              <span className="text-xs font-black" style={{ color: "#D4AF37" }}>IQ</span>
            </div>
            <div>
              <span className="text-white font-bold text-sm">CompeteIQ</span>
              <span className="text-slate-600 text-xs ml-2">Intelligence Stratégique</span>
            </div>
          </div>
          <p className="text-slate-600 text-xs text-center max-w-sm">
            Ce document est confidentiel et destiné exclusivement aux décideurs identifiés.
            Toute reproduction ou diffusion est interdite sans accord écrit préalable.
          </p>
          <div className="flex items-center gap-6">
            <a href="mailto:contact@competeiq.io" className="text-slate-500 hover:text-white text-xs transition-colors">
              contact@competeiq.io
            </a>
            <p className="text-slate-600 text-xs">© 2026 CompeteIQ</p>
          </div>
        </div>
      </footer>

    </div>
  );
}
