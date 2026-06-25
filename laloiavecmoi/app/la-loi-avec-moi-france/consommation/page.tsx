"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Consommation » — Édition FRANCE.
// Faits vérifiés : service-public.gouv.fr, economie.gouv.fr (DGCCRF),
// Code de la consommation. Distinct de l'édition belge.

const pointsCles = [
  {
    t: "Achat à distance : 14 jours pour vous rétracter",
    d: "Pour un achat en ligne, par téléphone ou par correspondance, vous disposez de 14 jours à compter de la réception du produit pour le retourner, sans avoir à vous justifier. Le vendeur doit vous informer de ce droit ; à défaut, le délai peut être prolongé.",
  },
  {
    t: "Garantie légale de conformité : 2 ans",
    d: "Tout bien vendu par un professionnel à un particulier (neuf, d'occasion ou reconditionné) est couvert pendant 2 ans à compter de la livraison par la garantie légale de conformité. Elle est gratuite et obligatoire : elle s'ajoute à toute garantie commerciale payante du vendeur.",
  },
  {
    t: "Vices cachés : 2 ans après la découverte",
    d: "Indépendamment de la garantie de conformité, la garantie des vices cachés vous protège contre un défaut grave non visible à l'achat. Vous avez 2 ans à partir de la découverte du vice pour agir. Elle peut jouer même longtemps après l'achat.",
  },
  {
    t: "Le professionnel doit réparer ou remplacer",
    d: "En cas de défaut couvert par la garantie de conformité, vous pouvez exiger la réparation ou le remplacement du bien, sans frais. Si aucune des deux solutions n'est possible dans un délai raisonnable, vous pouvez demander une réduction du prix ou le remboursement.",
  },
  {
    t: "Certains achats n'ouvrent PAS de droit de rétractation",
    d: "Le délai de 14 jours ne s'applique pas à tout : biens personnalisés ou sur mesure, denrées périssables, contenus numériques téléchargés avec votre accord, billets datés (spectacles, voyages), journaux… Vérifiez toujours les exceptions avant d'acheter.",
  },
];

const litige = [
  {
    n: "1",
    t: "Réclamez par écrit au vendeur",
    d: "Décrivez le problème, ce que vous demandez (réparation, remplacement, remboursement) et fixez un délai. Conservez une copie datée (e-mail ou lettre recommandée). C'est la base de tout recours.",
  },
  {
    n: "2",
    t: "Saisissez le médiateur de la consommation (gratuit)",
    d: "Si le vendeur ne répond pas, vous pouvez saisir gratuitement le médiateur de la consommation dont dépend le professionnel (ses coordonnées figurent sur le site ou les CGV du vendeur). C'est une étape amiable avant la justice.",
  },
  {
    n: "3",
    t: "Signalez sur SignalConso / allez au tribunal",
    d: "Vous pouvez signaler une pratique sur SignalConso (plateforme de la DGCCRF). En dernier recours, le tribunal judiciaire (juge des contentieux de la protection pour les petits litiges) tranche. Une assurance « protection juridique » peut aider.",
  },
];

const documentsOfficiels = [
  {
    label: "Service-Public.fr — Garantie légale de conformité",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F11094",
  },
  {
    label: "Economie.gouv.fr (DGCCRF) — La garantie légale de conformité",
    url: "https://www.economie.gouv.fr/particuliers/mes-droits-conso/bien-consommer/tout-savoir-sur-la-garantie-legale-de-conformite",
  },
  {
    label: "Service-Public.fr — Droit de rétractation",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F10485",
  },
  {
    label: "SignalConso — signaler un problème de consommation",
    url: "https://signal.conso.gouv.fr/",
  },
];

const readText = `Consommation et achats en France : vos droits. Cette page s'appuie sur des sources officielles (service-public.fr, DGCCRF) et ne remplace pas un conseil personnalisé. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} En cas de litige : réclamez d'abord par écrit au vendeur, puis saisissez gratuitement le médiateur de la consommation, et en dernier recours signalez sur SignalConso ou allez au tribunal. Conservez toujours vos preuves d'achat et vos échanges écrits.`;

export default function ConsommationFrancePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/la-loi-avec-moi-france" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi <span className="text-blue-700">· France</span></span>
          </Link>
          <Link href="/la-loi-avec-moi-france" className="text-sm font-semibold text-blue-700 hover:text-blue-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-blue-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.20),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🇫🇷 Consommation · vos achats protégés
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Achats — vos droits, sourcés</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Rétractation de 14 jours, garantie légale de 2 ans, vices cachés, litige : ce que la loi française vous
            garantit, adossé aux <strong className="text-white">sources officielles (service-public.fr, DGCCRF)</strong>.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-emerald-100 bg-emerald-50/60 p-5">
          <AgentAvocat
            name="Juliette"
            role="Assistante · droit de la consommation (France)"
            accent="emerald"
            message="Un achat qui tourne mal, ça arrive à tout le monde. La bonne nouvelle : en France, la loi est plutôt de votre côté. Gardez vos preuves et réclamez par écrit — ça suffit très souvent."
          />
        </div>
      </section>

      {/* Encadré le bon réflexe */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-emerald-300 bg-emerald-50 p-5">
          <p className="text-emerald-900 text-sm leading-relaxed">
            🧾 <strong>Le réflexe gagnant :</strong> conservez TOUT (facture, ticket, e-mails, photos du défaut).
            La garantie légale de conformité de <strong>2 ans</strong> et le droit de rétractation de
            <strong> 14 jours</strong> sont des droits légaux — gratuits — qui s&apos;ajoutent à toute « garantie »
            payante proposée en magasin.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles françaises, <strong>pas un conseil juridique
            personnalisé</strong>. Des exceptions existent (produits personnalisés, contenus numériques…) :
            vérifiez votre cas sur service-public.fr.
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

      {/* En cas de litige */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">En cas de litige : la marche à suivre</h2>
          <div className="mt-6 space-y-4">
            {litige.map((e) => (
              <div key={e.n} className="rounded-2xl border border-slate-200 bg-white p-5 flex gap-4">
                <span className="flex-shrink-0 w-9 h-9 rounded-full bg-emerald-100 text-emerald-800 font-bold flex items-center justify-center">{e.n}</span>
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
          Service-public.fr et la DGCCRF (economie.gouv.fr) sont les références françaises de la protection des
          consommateurs. Ces pages font foi et sont tenues à jour.
        </p>
        <div className="mt-5 flex flex-col gap-2.5">
          {documentsOfficiels.map((d) => (
            <a key={d.url} href={d.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-50 rounded-lg px-4 py-2.5 transition-colors">
              🔗 {d.label}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
          ))}
        </div>
      </section>

      {/* Aide */}
      <section className="pb-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-blue-200 bg-blue-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-blue-900">Besoin d&apos;aller plus loin ?</h2>
          <p className="text-blue-900/80 text-sm mt-2 leading-relaxed">
            Le médiateur de la consommation intervient gratuitement. Pour un litige plus lourd, une association de
            consommateurs agréée ou votre assurance « protection juridique » peut vous accompagner. SignalConso
            permet aussi d&apos;alerter les autorités.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://signal.conso.gouv.fr/" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 SignalConso — signaler un problème
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/la-loi-avec-moi-france" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-100 rounded-lg px-4 py-2.5 transition-colors">
              ← Retour à tous les sujets (France)
            </Link>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/la-loi-avec-moi-france" className="hover:text-slate-900">← Retour à tous les sujets</Link>
        <span className="mx-2 text-slate-300">·</span>
        <Link href="/loi-avec-moi/consommation" className="text-slate-500 hover:text-slate-900">🇧🇪 Version Belgique</Link>
      </footer>
    </main>
  );
}
