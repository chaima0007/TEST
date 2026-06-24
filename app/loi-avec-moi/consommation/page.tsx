"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Consommation & achats » (Belgique).
// Faits vérifiés : SPF Economie (rétractation, garantie), Belgium.be,
// Service de Médiation pour le Consommateur. Code de droit économique, Livre VI.

const pointsCles = [
  {
    t: "Achat à distance : 14 jours pour changer d'avis",
    d: "Pour un achat en ligne ou à distance (téléphone, démarchage), vous avez 14 jours pour vous rétracter, sans devoir vous justifier. Le délai court à partir de la réception du colis (et vous pouvez même renoncer avant de l'avoir reçu).",
  },
  {
    t: "Vous pouvez essayer, pas « user »",
    d: "Vous avez le droit d'examiner le bien comme vous le feriez en magasin (essayer un vêtement, par exemple). Mais si vous l'utilisez au point de laisser des traces inévitables, le vendeur peut réduire le remboursement. Gardez l'emballage et les étiquettes.",
  },
  {
    t: "Remboursement complet sous 14 jours",
    d: "Après avoir été informé de votre rétractation, le vendeur doit vous rembourser dans les 14 jours — frais de livraison standard inclus. Il peut attendre d'avoir récupéré le bien (ou la preuve de l'envoi) avant de rembourser.",
  },
  {
    t: "Garantie légale de 2 ans (en plus de toute garantie commerciale)",
    d: "Pour tout achat d'un consommateur auprès d'une entreprise dans l'UE, une garantie légale de 2 ans s'applique sur un produit neuf, à partir de la livraison. Elle couvre les défauts de conformité. C'est un droit légal : il s'ajoute à toute « garantie » commerciale payante du magasin.",
  },
  {
    t: "Certains achats n'ont PAS de droit de rétractation",
    d: "Le délai de 14 jours ne s'applique pas à tout : produits sur mesure ou personnalisés, biens périssables, contenus numériques téléchargés avec votre accord, journaux, billets datés (concerts, voyages)… Vérifiez toujours les exceptions avant d'acheter.",
  },
];

const litige = [
  {
    n: "1",
    t: "Réclamez par écrit au vendeur",
    d: "Décrivez le problème, ce que vous demandez (réparation, remplacement, remboursement) et un délai. Gardez une copie datée (e-mail ou recommandé). C'est la base de tout recours.",
  },
  {
    n: "2",
    t: "Le Service de Médiation pour le Consommateur",
    d: "Si le vendeur ne réagit pas, ce service public fédéral peut intervenir gratuitement comme intermédiaire pour trouver une solution amiable, ou vous orienter vers le bon organisme.",
  },
  {
    n: "3",
    t: "Signalez au SPF Economie / allez en justice",
    d: "Vous pouvez signaler une pratique illégale au SPF Economie (Point de contact). En dernier recours, le juge de paix (petits litiges) tranche. Un avocat ou une assurance « protection juridique » peut aider.",
  },
];

const documentsOfficiels = [
  {
    label: "SPF Economie — Droit de rétractation (vente à distance)",
    url: "https://economie.fgov.be/fr/themes/protection-des-consommateurs/faire-valoir-ses-droits/achats/annuler-un-achat/quand-pouvez-vous/droit-de-retractation-en-cas",
  },
  {
    label: "SPF Economie — La garantie : quels sont vos droits ?",
    url: "https://economie.fgov.be/fr/themes/protection-des-consommateurs/faire-valoir-ses-droits/garantie/quels-sont-vos-droits",
  },
  {
    label: "Belgium.be — Garanties & protection du consommateur",
    url: "https://www.belgium.be/fr/economie/commerce_et_consommation/protection_du_consommateur/garanties",
  },
  {
    label: "Service de Médiation pour le Consommateur",
    url: "https://mediationconsommateur.be/fr",
  },
];

const readText = `Consommation et achats en Belgique : vos droits. Cette page s'appuie sur des sources officielles du SPF Economie et ne remplace pas un conseil personnalisé. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} En cas de litige : réclamez d'abord par écrit au vendeur, puis faites appel au Service de Médiation pour le Consommateur, gratuit, et en dernier recours au SPF Economie ou à la justice. Conservez toujours vos preuves d'achat et vos échanges écrits.`;

export default function ConsommationPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">L</span>
            </div>
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.20),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🛒 Consommation · vos achats protégés
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Achats — vos droits, sourcés</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Rétractation de 14 jours, garantie légale de 2 ans, remboursement, litige : ce que la loi vous garantit,
            adossé aux <strong className="text-white">sources officielles du SPF Economie</strong>. Vous achetez mieux
            informé·e, et vous savez réagir.
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
            name="Maître Élodie"
            role="Référente · droit de la consommation"
            accent="emerald"
            message="Un achat qui tourne mal, ça arrive à tout le monde. La bonne nouvelle : la loi est plutôt de votre côté. Gardez vos preuves, et réclamez par écrit — ça suffit souvent."
          />
        </div>
      </section>

      {/* Encadré le bon réflexe */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-emerald-300 bg-emerald-50 p-5">
          <p className="text-emerald-900 text-sm leading-relaxed">
            🧾 <strong>Le réflexe gagnant :</strong> conservez TOUT (facture, ticket, e-mails, photos du défaut).
            La garantie légale de <strong>2 ans</strong> et le droit de rétractation de <strong>14 jours</strong> sont
            des droits légaux — gratuits — qui s&apos;ajoutent à toute « garantie » payante proposée en magasin.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles, <strong>pas un conseil juridique
            personnalisé</strong>. Des exceptions existent (produits personnalisés, contenus numériques…) :
            vérifiez votre cas sur le SPF Economie.
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
          Le SPF Economie est l&apos;autorité de protection des consommateurs. Ces pages font foi et sont tenues à jour.
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
            Le Service de Médiation pour le Consommateur intervient gratuitement. Pour un litige plus lourd, un avocat
            (gratuitement / à coût réduit selon vos revenus grâce au Bureau d&apos;Aide Juridique) ou votre assurance
            « protection juridique » peut vous accompagner.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://mediationconsommateur.be/fr" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 Service de Médiation pour le Consommateur
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <Link href="/loi-avec-moi/avocat/dettes" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              💶 Fiche « Dettes & consommation » →
            </Link>
            <Link href="/loi-avec-moi/trouver-un-avocat" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              ⚖️ Trouver le bon avocat & aide juridique →
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
