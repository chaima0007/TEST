"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Droits des passagers à l'aéroport (Belgique). Faits vérifiés : Belgium.be, SPF Mobilité &
// Transports (mobilit.belgium.be), Centre Européen des Consommateurs Belgique (cecbelgique.be).
// Base légale : règlement européen (CE) n°261/2004.

const indemnites = [
  { dist: "Jusqu'à 1 500 km", montant: "250 €" },
  { dist: "Entre 1 500 et 3 500 km", montant: "400 €" },
  { dist: "Plus de 3 500 km", montant: "600 €" },
];

const situations = [
  {
    emoji: "⏱️",
    t: "Vol retardé",
    d: "Dès que le retard dépasse 3 heures à l'arrivée, vous pouvez avoir droit à une indemnité forfaitaire (selon la distance). En cas de retard important, la compagnie doit aussi vous prendre en charge : repas et rafraîchissements, hébergement à l'hôtel si nécessaire, et la possibilité de passer deux appels / e-mails.",
  },
  {
    emoji: "❌",
    t: "Vol annulé",
    d: "Vous avez le choix entre le remboursement du billet ou un réacheminement vers votre destination. Si le vol de remplacement proposé ne vous convient pas, le billet doit être remboursé. Une indemnité peut aussi être due selon le délai de prévenance.",
  },
  {
    emoji: "🚷",
    t: "Refus d'embarquement (surbooking)",
    d: "La compagnie cherche d'abord des volontaires (contre avantages). Si elle refuse l'embarquement contre votre gré, vous avez droit au choix entre remboursement ou réacheminement, PLUS une indemnité de 250 € à 600 € selon la distance.",
  },
  {
    emoji: "🧳",
    t: "Bagage perdu, retardé ou abîmé",
    d: "Signalez-le immédiatement au comptoir de la compagnie et faites établir un constat (P.I.R.) avant de quitter l'aéroport. Conservez votre étiquette de bagage et vos justificatifs : la compagnie est responsable dans les limites et délais prévus par la convention de Montréal.",
  },
  {
    emoji: "♿",
    t: "Mobilité réduite (PMR)",
    d: "Vous avez droit à une assistance gratuite pour vous déplacer dans l'aéroport et embarquer/débarquer. Signalez votre besoin à la compagnie au moins 48 h avant le vol pour garantir l'assistance.",
  },
];

const pasDroit = [
  "Vous vous êtes présenté·e en retard à l'enregistrement.",
  "Il vous manque un document indispensable (passeport, visa valide…).",
  "Le problème vient de « circonstances extraordinaires » indépendantes de la compagnie (météo dangereuse, grève externe, sécurité). L'indemnité forfaitaire peut alors ne pas être due — mais l'assistance (repas, hébergement) reste souvent obligatoire.",
];

const sources = [
  { label: "Belgium.be — Droits des passagers aériens", url: "https://www.belgium.be/fr/mobilite/en_avion_et_en_bateau/droits_des_passagers/droits_des_passagers_aeriens" },
  { label: "SPF Mobilité & Transports — Droits des passagers", url: "https://mobilit.belgium.be/fr/aviation/passagers" },
  { label: "Centre Européen des Consommateurs Belgique — Retard / annulation de vol", url: "https://www.cecbelgique.be/themes/voyages/voyage-en-avion/retard-de-vol" },
];

const readText = `Vos droits à l'aéroport, en Belgique, basés sur le règlement européen 261/2004. ${situations
  .map((s) => s.t + ". " + s.d)
  .join(" ")} Montants d'indemnité selon la distance : 250 euros jusqu'à 1500 km, 400 euros entre 1500 et 3500 km, 600 euros au-delà. Vous n'avez pas droit à l'indemnité si vous arrivez en retard à l'enregistrement, s'il vous manque un document, ou en cas de circonstances extraordinaires. En Belgique, l'autorité compétente est la Denied Boarding Authority du SPF Mobilité. Ceci est une information générale et ne remplace pas un conseil juridique.`;

export default function DroitsAeroportPage() {
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(14,165,233,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            ✈️ À l&apos;aéroport · droits des passagers
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Vos droits à l&apos;aéroport</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Vol retardé, annulé, refusé, bagage perdu : ce que la loi européenne vous garantit, et
            <strong className="text-white"> combien vous pouvez réclamer</strong>. Simple et concret.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-sky-100 bg-sky-50/60 p-5">
          <AgentAvocat
            name="Nora"
            role="Assistante · droits des voyageurs"
            accent="sky"
            message="Un vol qui dérape, ça gâche le voyage — mais vous avez des droits chiffrés. On regarde ce que vous pouvez réclamer."
          />
        </div>
      </section>

      {/* Tableau indemnités */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">💶 Combien pouvez-vous réclamer ?</h2>
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">
          Indemnité forfaitaire en cas de retard ≥ 3 h à l&apos;arrivée, d&apos;annulation ou de refus d&apos;embarquement —
          selon la distance du vol :
        </p>
        <div className="mt-5 grid sm:grid-cols-3 gap-3">
          {indemnites.map((x) => (
            <div key={x.dist} className="rounded-2xl border-2 border-sky-200 bg-sky-50 p-5 text-center">
              <p className="text-3xl font-black text-sky-700">{x.montant}</p>
              <p className="text-xs text-sky-900/70 mt-1.5 font-medium">{x.dist}</p>
            </div>
          ))}
        </div>
        <p className="text-xs text-slate-500 mt-3 leading-relaxed">
          Montants fixés par le règlement européen (CE) n°261/2004. Le montant exact peut être réduit en cas de
          réacheminement proche de l&apos;horaire initial.
        </p>
      </section>

      {/* Situations */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Votre situation</h2>
          <div className="mt-6 space-y-4">
            {situations.map((s, i) => (
              <div key={i} className="rounded-2xl border border-slate-200 bg-white p-5">
                <h3 className="font-bold tracking-tight flex items-center gap-2"><span aria-hidden>{s.emoji}</span>{s.t}</h3>
                <p className="text-slate-700 text-sm mt-2 leading-relaxed">{s.d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Quand on n'a PAS droit */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">⚠️ Quand l&apos;indemnité n&apos;est pas due</h2>
        <ul className="mt-5 space-y-2.5">
          {pasDroit.map((d, i) => (
            <li key={i} className="flex items-start gap-2.5 text-sm text-slate-700 leading-relaxed">
              <span className="flex-shrink-0 text-amber-500 mt-0.5" aria-hidden>•</span>
              {d}
            </li>
          ))}
        </ul>
      </section>

      {/* Comment réclamer */}
      <section className="pb-6 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-indigo-200 bg-indigo-50 p-6">
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Comment réclamer ?</h2>
          <ol className="mt-3 space-y-2 text-sm text-indigo-900/90 leading-relaxed list-decimal list-inside">
            <li>Adressez d&apos;abord une demande écrite à la compagnie aérienne (gardez une copie et vos preuves).</li>
            <li>Sans réponse satisfaisante, saisissez en Belgique la <strong>« Denied Boarding Authority »</strong> du SPF Mobilité &amp; Transports.</li>
            <li>Pour un litige transfrontalier, le Centre Européen des Consommateurs (CEC) peut vous aider gratuitement.</li>
          </ol>
        </div>
      </section>

      {/* Sources */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-xl font-bold tracking-tight">📚 Sources officielles</h2>
        <div className="mt-4 flex flex-col gap-2.5">
          {sources.map((s) => (
            <a key={s.url} href={s.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 {s.label}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
          ))}
        </div>
        <div className="mt-6 rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Information générale fondée sur le droit européen et des sources officielles belges. Les règles
            évoluent (une réforme européenne est en discussion) : vérifiez toujours la source officielle pour votre
            cas. Ceci ne remplace pas un conseil juridique personnalisé.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
