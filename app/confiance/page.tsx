import Link from "next/link";

// Trust Center Caelum — « Sécurité & Confiance » (standard B2B des plateformes entreprise).
// Honnêteté radicale : on décrit nos pratiques RÉELLES + ce qu'on n'a pas encore (pattern
// « objectif » pour les certifications). Daté. Aucun badge ni certification inventé.

export const dynamic = "force-static";
export const metadata = {
  title: "Sécurité & Confiance (Trust Center) — Caelum",
  description:
    "Nos pratiques de sécurité, de protection des données (RGPD) et de fiabilité — décrites honnêtement, sources et méthode vérifiables.",
};

const MAJ = "juin 2026";

const cartes = [
  { t: "Données en Europe (RGPD)", d: "Données personnelles limitées au strict nécessaire (formulaire de contact). Finalité unique, pas de revente, droits d'accès/rectification/suppression." },
  { t: "Zéro secret dans le code", d: "Aucun identifiant, mot de passe ou clé d'API dans le code source — vérifié. Les secrets vivent dans des variables d'environnement." },
  { t: "Surface d'attaque réduite", d: "Site en grande partie pré-rendu (statique) : moins de code exécuté côté serveur, moins de risques." },
  { t: "Sources officielles vérifiables", d: "Chaque information juridique renvoie à un texte légal officiel (sources de confiance « tier1 »), jamais à une opinion." },
  { t: "Supervision humaine", d: "L'automatisation accélère, mais un humain valide chaque livrable avant qu'il ne parte." },
  { t: "Transparence vérifiable", d: "Notre plateforme d'auto-supervision rend compte en public de ce qu'elle vérifie et corrige." },
];

const sections = [
  {
    titre: "Protection des données (RGPD)",
    points: [
      "Collecte minimale : seules les données du formulaire (nom, e-mail, organisation, message).",
      "Finalité unique : vous recontacter. Aucune revente ni cession à des tiers.",
      "Vos droits : accès, rectification, suppression sur simple demande.",
      "Réclamation possible auprès de l'Autorité de protection des données (Belgique).",
    ],
  },
  {
    titre: "Sécurité applicative",
    points: [
      "Validation et limites de taille sur les formulaires (rejet des charges anormales).",
      "Aucun credential en clair dans le code ; configuration par variables d'environnement.",
      "Dégradation maîtrisée : en cas d'indisponibilité d'un service amont, réponse contrôlée (HTTP 502), jamais de fuite d'erreur.",
      "Dépendances suivies ; build reproductible.",
    ],
  },
  {
    titre: "Fiabilité & disponibilité",
    points: [
      "Hébergement Vercel (voir mentions légales) ; pages statiques servies via CDN pour tenir la charge.",
      "Plateforme d'auto-supervision interne (résilience mesurée, scénarios simulés, alertes).",
      "Objectif : publier un indicateur de disponibilité public à mesure de la montée en charge.",
    ],
  },
  {
    titre: "Méthode & sources",
    points: [
      "Chaque réponse réglementaire est datée et sourcée (texte officiel).",
      "Liste de sources de confiance maintenue ; détection des sources qui changent.",
      "Veille : suivi de la fraîcheur des contenus pour signaler ce qui doit être revérifié.",
    ],
  },
];

export default function Confiance() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg">Caelum</span>
          </Link>
          <Link href="/contact" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Demander plus d&apos;infos</Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-slate-950 to-slate-900 text-white py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-5">
            Trust Center · mis à jour : {MAJ}
          </span>
          <h1 className="text-3xl sm:text-4xl font-bold">Sécurité & Confiance</h1>
          <p className="mt-3 text-slate-300 max-w-2xl">
            Ce que nous faisons pour protéger vos données et mériter votre confiance — décrit honnêtement,
            avec nos sources et notre méthode vérifiables.
          </p>
        </div>
      </section>

      <section className="max-w-4xl mx-auto px-6 py-12">
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {cartes.map((c) => (
            <div key={c.t} className="rounded-2xl border border-slate-200 p-5">
              <h2 className="font-semibold text-slate-900 text-sm">{c.t}</h2>
              <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">{c.d}</p>
            </div>
          ))}
        </div>

        <div className="mt-10 grid md:grid-cols-2 gap-6">
          {sections.map((s) => (
            <div key={s.titre} className="rounded-2xl border border-slate-200 p-6">
              <h2 className="font-bold text-slate-900">{s.titre}</h2>
              <ul className="mt-3 space-y-2">
                {s.points.map((p) => (
                  <li key={p} className="flex items-start gap-2 text-sm text-slate-600">
                    <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5">
                      <path fillRule="evenodd" d="M16.7 5.3a1 1 0 010 1.4l-7.5 7.5a1 1 0 01-1.4 0L3.3 9.7a1 1 0 011.4-1.4L8.5 12l6.8-6.8a1 1 0 011.4 0z" clipRule="evenodd" />
                    </svg>
                    <span>{p}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Honnêteté sur les certifications */}
        <div className="mt-8 rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h2 className="font-semibold text-amber-900">En toute transparence — certifications</h2>
          <p className="text-amber-800 text-sm mt-2 leading-relaxed">
            Caelum ne dispose pas encore de certification SOC 2 ou ISO 27001. Nous préférons le dire clairement
            plutôt que d'afficher un badge que nous n'avons pas. Ces démarches seront engagées à mesure de notre
            croissance et des exigences de nos clients grands comptes. En attendant, les pratiques ci-dessus sont
            réelles et vérifiables, et nous répondons volontiers à vos questionnaires de sécurité.
          </p>
        </div>

        <div className="mt-8 rounded-2xl bg-slate-900 text-white p-7 text-center">
          <h2 className="text-xl font-bold">Un questionnaire de sécurité à remplir ?</h2>
          <p className="text-slate-300 mt-2 text-sm">Envoyez-le nous : on y répond précisément, sans langue de bois.</p>
          <Link href="/contact" className="inline-block mt-5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-3 rounded-xl transition-colors">
            Nous contacter
          </Link>
        </div>

        <p className="text-center text-xs text-slate-400 mt-6">
          Voir aussi : <Link href="/confidentialite" className="text-indigo-700 hover:underline">Confidentialité</Link> ·{" "}
          <Link href="/mentions-legales" className="text-indigo-700 hover:underline">Mentions légales</Link> ·{" "}
          <Link href="/plateforme-autonome" className="text-indigo-700 hover:underline">Transparence (plateforme)</Link>
        </p>
      </section>
    </main>
  );
}
