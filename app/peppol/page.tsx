import Link from "next/link";

// Guide neutre « Choisir sa solution Peppol » — Caelum (répond à OPP-PEPPOL-COMPARATEUR).
// Honnêteté : Caelum n'est PAS un access point ; on oriente sans parti pris ni prix inventé.
// On nomme des catégories et des exemples cités par la presse, sans classement commercial.

export const dynamic = "force-static";
export const metadata = {
  title: "Choisir sa solution Peppol (e-facturation B2B) — guide neutre | Caelum",
  description:
    "E-facturation B2B obligatoire en Belgique depuis 2026 : quelle solution Peppol selon votre profil ? Guide neutre, critères de choix et check-list émission/réception.",
};

const routes = [
  {
    profil: "Vous avez déjà un logiciel comptable moderne",
    exemples: "Ex. cités par la presse : WinBooks, Exact Online, Odoo…",
    repondre: "Souvent, une simple mise à jour de votre logiciel suffit : il devient capable d'émettre et recevoir via Peppol. C'est généralement la voie la moins coûteuse si vous êtes déjà équipé.",
  },
  {
    profil: "Petite structure / indépendant sans logiciel complexe",
    exemples: "Plateformes Peppol simples, parfois avec appli mobile (facturer juste après l'intervention).",
    repondre: "Des solutions légères permettent d'émettre/recevoir sans système comptable lourd, à partir de quelques euros par mois selon l'outil. Objectif : être conforme sans devenir expert.",
  },
  {
    profil: "Grande entreprise / ERP",
    exemples: "Connecteur d'access point via API / protocole AS4, intégré à l'ERP.",
    repondre: "L'enjeu est l'intégration ERP et la validation (BIS 3.0). Vérifiez la couverture géographique de l'access point et la qualité des rapports d'erreur.",
  },
];

const criteres = [
  "Émission ET réception (les deux sont obligatoires).",
  "Compatibilité avec votre logiciel/ERP actuel (connecteur/API).",
  "Validation BIS 3.0 avant envoi + rapports d'erreur clairs.",
  "Modèle de prix adapté : à l'usage (volume variable) vs abonnement (flux prévisibles).",
  "Couverture géographique (Belgique + international si vous facturez à l'étranger).",
  "Support et accompagnement à la bascule.",
];

const checklist = [
  "Mon entreprise a un identifiant Peppol (inscrite sur le réseau).",
  "Je peux ÉMETTRE une facture électronique structurée.",
  "Je peux RECEVOIR une facture entrante (et je la vois passer).",
  "J'ai testé au moins un cycle complet émission → réception.",
  "Je sais gérer le self-billing si concerné (tolérance jusqu'au 30/06/2026).",
];

export default function PeppolPage() {
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
          <Link href="/conformite/e-facturation" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">La fiche sourcée</Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-slate-950 to-slate-900 text-white py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-5">
            E-facturation B2B · guide neutre
          </span>
          <h1 className="text-3xl sm:text-4xl font-bold">Quelle solution Peppol pour vous ?</h1>
          <p className="mt-3 text-slate-300 max-w-2xl">
            Depuis 2026, la facture B2B doit passer par Peppol — le PDF par e-mail ne suffit plus.
            La bonne nouvelle : souvent plus simple qu'on ne le croyait. Voici comment choisir, sans parti pris.
          </p>
        </div>
      </section>

      <section className="max-w-4xl mx-auto px-6 py-12">
        <h2 className="text-xl font-bold">Votre profil → la bonne voie</h2>
        <div className="mt-4 grid gap-4">
          {routes.map((r, i) => (
            <div key={i} className="rounded-2xl border border-slate-200 p-5">
              <h3 className="font-bold text-slate-900">{r.profil}</h3>
              <p className="text-sm text-slate-700 mt-2">{r.repondre}</p>
              <p className="text-xs text-slate-500 mt-2">{r.exemples}</p>
            </div>
          ))}
        </div>

        <h2 className="text-xl font-bold mt-10">Les 6 critères pour comparer</h2>
        <ul className="mt-3 grid sm:grid-cols-2 gap-2">
          {criteres.map((c) => (
            <li key={c} className="flex items-start gap-2 text-sm text-slate-700 rounded-lg border border-slate-200 p-3">
              <span className="text-indigo-600 font-bold">→</span>{c}
            </li>
          ))}
        </ul>

        <div className="mt-10 rounded-2xl border border-emerald-200 bg-emerald-50 p-6">
          <h2 className="font-bold text-emerald-900">Check-list : suis-je vraiment prêt ?</h2>
          <ul className="mt-3 space-y-2">
            {checklist.map((c) => (
              <li key={c} className="flex items-start gap-2 text-sm text-emerald-900">
                <span>☐</span>{c}
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-8 rounded-2xl bg-slate-900 text-white p-7 text-center">
          <h2 className="text-lg font-bold">On vous oriente, sans rien vous vendre</h2>
          <p className="text-slate-300 text-sm mt-2 max-w-2xl mx-auto">
            Caelum n'est pas un access point Peppol et ne touche aucune commission : ce guide est neutre.
            Le choix de l'access point est libre (une dizaine existent en Belgique). On vous aide à savoir
            ce qui vous concerne et à vérifier que vous êtes prêt.
          </p>
          <Link href="/conformite-2026" className="inline-block mt-5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-3 rounded-xl transition-colors">
            Vérifier ma conformité
          </Link>
        </div>

        <p className="text-center text-xs text-slate-400 mt-6">
          Information générale (sources : SPF Économie, presse économique belge 2026). Les exemples de logiciels
          sont cités à titre indicatif, sans classement ni recommandation commerciale.
        </p>
      </section>
    </main>
  );
}
