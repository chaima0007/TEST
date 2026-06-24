"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Créer son entreprise » (Belgique).
// Faits vérifiés : SPF Economie (BCE, mentions obligatoires site web),
// business.belgium.be, guichets d'entreprises agréés. Frais BCE 2026.

const pointsCles = [
  {
    t: "Choisir son statut : indépendant en personne physique ou société",
    d: "Le plus simple pour démarrer est l'indépendant en personne physique (rapide, peu coûteux, mais votre patrimoine personnel n'est pas séparé de l'activité). La société (souvent une SRL) protège mieux votre patrimoine mais coûte plus cher à constituer (acte notarié, publication au Moniteur belge — souvent 1 300 € à 1 800 € au total). Le bon choix dépend de votre risque, vos revenus et vos projets.",
  },
  {
    t: "L'inscription à la BCE est obligatoire — avant de commencer",
    d: "Toute activité doit être enregistrée à la Banque-Carrefour des Entreprises (BCE) au plus tard le jour du début de l'activité. Vous recevez un numéro d'entreprise unique à 10 chiffres. On passe par un guichet d'entreprises agréé (Xerius, Acerta, Partena, Liantis, UCM, Securex…). En 2026, l'inscription coûte 111,50 € par unité d'établissement.",
  },
  {
    t: "Votre numéro d'entreprise devient votre numéro de TVA",
    d: "Si votre activité est assujettie à la TVA, votre numéro d'entreprise précédé de « BE » devient votre numéro de TVA. Vous devez activer votre numéro de TVA (via le guichet ou le SPF Finances) avant de facturer avec TVA. Certaines petites activités peuvent relever du régime de franchise TVA — renseignez-vous.",
  },
  {
    t: "Affiliations sociales : caisse d'assurances sociales + mutuelle",
    d: "Comme indépendant, vous devez vous affilier à une caisse d'assurances sociales pour indépendants (cotisations sociales) et être en ordre de mutuelle. C'est ce qui vous ouvre vos droits (soins de santé, pension, etc.). Le guichet d'entreprises et la caisse sociale vous guident dans l'ordre des démarches.",
  },
  {
    t: "Votre site et vos factures doivent porter des mentions légales",
    d: "Sur votre site web et vos factures, la loi impose d'afficher clairement : dénomination, numéro d'entreprise (BCE), numéro de TVA (si assujetti), adresse du siège, e-mail et téléphone. Pour un e-commerce, ajoutez des Conditions Générales de Vente (CGV) et le droit de rétractation. Si vous traitez des données clients, le RGPD s'applique (politique de confidentialité, base légale).",
  },
];

const etapes = [
  {
    n: "1",
    t: "Validez l'idée et faites un plan financier",
    d: "Estimez vos revenus, vos charges, votre seuil de rentabilité. Un plan financier est d'ailleurs obligatoire pour constituer une société. Beaucoup de structures (guichets, organismes régionaux) accompagnent gratuitement les starters.",
  },
  {
    n: "2",
    t: "Choisissez la forme juridique (et voyez un notaire si société)",
    d: "Indépendant en personne physique pour démarrer léger, ou société (SRL…) pour protéger votre patrimoine. La constitution d'une société passe en général par un notaire (statuts, publication au Moniteur belge).",
  },
  {
    n: "3",
    t: "Inscrivez-vous via un guichet d'entreprises agréé",
    d: "Le guichet vous inscrit à la BCE (numéro d'entreprise), active votre TVA si besoin, et vous oriente vers la caisse d'assurances sociales. Vérifiez aussi les autorisations propres à votre métier (accès à la profession, licences, autorisations communales).",
  },
];

const documentsOfficiels = [
  {
    label: "Business.belgium.be — Créer son entreprise (portail officiel)",
    url: "https://business.belgium.be/fr/gerer_votre_entreprise/creation_d_entreprise",
  },
  {
    label: "SPF Economie — Inscription à la Banque-Carrefour des Entreprises (BCE)",
    url: "https://economie.fgov.be/fr/themes/entreprises/banque-carrefour-des/inscription-la-banque",
  },
  {
    label: "SPF Economie — Informations obligatoires sur votre site / e-commerce",
    url: "https://economie.fgov.be/fr/e-commerce/mettre-en-place-vos-supports/les-informations-obligatoires",
  },
  {
    label: "Belgium.be — Indépendants & entreprises",
    url: "https://www.belgium.be/fr/economie/entreprise",
  },
];

const readText = `Créer son entreprise en Belgique : les bases pour démarrer en règle. Cette page s'appuie sur des sources officielles (SPF Economie, business.belgium.be) et ne remplace pas un conseil personnalisé. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} Les étapes : validez votre idée et votre plan financier, choisissez la forme juridique, puis inscrivez-vous via un guichet d'entreprises agréé qui vous enregistre à la Banque-Carrefour des Entreprises, active votre TVA et vous oriente vers la caisse d'assurances sociales.`;

export default function CreerEntreprisePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(245,158,11,0.18),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🚀 Créer son entreprise
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Lancer votre activité, en règle</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Statut, inscription à la BCE, TVA, affiliations, mentions légales d&apos;un site : les bases pour
            démarrer sereinement et sans mauvaise surprise, <strong className="text-white">adossées aux sources
            officielles</strong>.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-amber-100 bg-amber-50/60 p-5">
          <AgentAvocat
            name="Nadia"
            role="Assistante · droit des entreprises"
            accent="amber"
            message="Se lancer fait peur, mais le parcours est balisé. L'essentiel : vous inscrire à la BCE avant de démarrer, et bien choisir votre statut. Un guichet d'entreprises agréé fait une grande partie des démarches avec vous."
          />
        </div>
      </section>

      {/* Encadré le bon réflexe */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-300 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ✅ <strong>L&apos;ordre qui évite les ennuis :</strong> plan financier → choix du statut →
            inscription BCE via un guichet d&apos;entreprises agréé (numéro d&apos;entreprise) → activation TVA →
            affiliation caisse sociale. Et tout cela <strong>avant</strong> votre première facture.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil juridique ou
            comptable personnalisé</strong>. Les montants, régimes TVA et autorisations varient selon l&apos;activité
            et la Région : faites-vous accompagner par un guichet d&apos;entreprises ou un comptable.
          </p>
        </div>
      </section>

      {/* Points clés */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">Les points clés</h2>
        <div className="mt-6 space-y-4">
          {pointsCles.map((p, i) => (
            <div key={i} className="rounded-2xl border border-slate-200 p-5">
              <h3 className="font-bold tracking-tight">{p.t}</h3>
              <p className="text-slate-700 text-sm mt-2 leading-relaxed">{p.d}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Étapes */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Les étapes pour démarrer</h2>
          <div className="mt-6 space-y-4">
            {etapes.map((e) => (
              <div key={e.n} className="rounded-2xl border border-slate-200 bg-white p-5 flex gap-4">
                <span className="flex-shrink-0 w-9 h-9 rounded-full bg-amber-100 text-amber-800 font-bold flex items-center justify-center">{e.n}</span>
                <div>
                  <h3 className="font-bold tracking-tight">{e.t}</h3>
                  <p className="text-slate-700 text-sm mt-2 leading-relaxed">{e.d}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Documents officiels de référence */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">📚 Les sources officielles</h2>
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">
          Le portail business.belgium.be et le SPF Economie font autorité et tiennent leurs pages à jour.
        </p>
        <div className="mt-5 flex flex-col gap-2.5">
          {documentsOfficiels.map((d) => (
            <a key={d.url} href={d.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-50 rounded-lg px-4 py-2.5 transition-colors">
              🔗 {d.label}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
          ))}
        </div>
      </section>

      {/* Aide */}
      <section className="pb-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-indigo-200 bg-indigo-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Besoin d&apos;aller plus loin ?</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed">
            Un guichet d&apos;entreprises agréé et un comptable sont vos meilleurs alliés au démarrage. Pour les
            statuts d&apos;une société, les contrats ou un litige, un avocat (gratuitement / à coût réduit selon vos
            revenus grâce au Bureau d&apos;Aide Juridique) peut vous accompagner.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://business.belgium.be/fr/gerer_votre_entreprise/creation_d_entreprise" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 Business.belgium.be — Créer son entreprise
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/loi-avec-moi/avocat/entreprise" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🏢 Fiche « Avocat en droit de l&apos;entreprise » →
            </Link>
            <Link href="/loi-avec-moi/trouver-un-avocat" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              ⚖️ Trouver le bon avocat &amp; aide juridique →
            </Link>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à tous les sujets</Link>
      </footer>
    </main>
  );
}
