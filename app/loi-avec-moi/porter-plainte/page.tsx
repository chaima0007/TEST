"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Porter plainte en Belgique : vos droits, le refus d'acter, le comportement anormal de la police.
// Faits vérifiés via sources officielles : Belgium.be, SPF Justice, Ministère public (om-mp.be),
// Police fédérale (police.be), Comité P (comitep.be).

const droitsExiger = [
  {
    t: "Une attestation de dépôt de plainte",
    d: "La police vous remet une attestation : c'est la preuve que vous avez porté plainte. Elle contient la référence du procès-verbal et des adresses de services qui peuvent vous aider.",
  },
  {
    t: "Le numéro de PV et le parquet compétent",
    d: "Demandez le numéro du procès-verbal (pour suivre votre dossier) et quel parquet — de quelle commune — est compétent. Notez-les soigneusement.",
  },
  {
    t: "Une copie gratuite de votre audition",
    d: "Vous avez le droit d'obtenir gratuitement une copie du texte de votre audition. Sauf exception, elle vous est remise immédiatement. Relisez-la avant de signer.",
  },
  {
    t: "Vous déclarer « personne lésée »",
    d: "En déposant une déclaration de personne lésée (formulaire remis par la police, transmis au parquet du procureur du Roi), vous serez tenu·e informé·e des suites et pourrez faire valoir vos droits.",
  },
  {
    t: "De l'aide si vous en avez besoin",
    d: "La police peut faire appel au service d'assistance policière aux victimes ou vous orienter vers un service spécialisé. Si vous ne parlez pas la langue, signalez-le : un interprète peut intervenir.",
  },
];

const siRefus = [
  {
    t: "La police est OBLIGÉE d'acter votre plainte",
    d: "La loi est claire : pour des faits qui peuvent constituer une infraction, les services de police doivent dresser procès-verbal. Le refus d'acter n'est pas un choix laissé au policier.",
    fort: true,
  },
  {
    t: "1 · Écrivez directement au procureur du Roi",
    d: "Vous pouvez porter plainte par courrier — de préférence en recommandé — adressé au procureur du Roi du parquet compétent. Soyez le plus factuel·le possible : dates, lieux, personnes, faits, sans interprétation.",
  },
  {
    t: "2 · Déposez une déclaration de personne lésée au parquet",
    d: "Cette déclaration peut se faire au secrétariat du parquet, même sans plainte préalable à la police. Vous acquérez la qualité de personne lésée.",
  },
  {
    t: "3 · Signalez le refus au Comité P",
    d: "Le refus d'acter est un dysfonctionnement. Le Comité P (contrôle externe des services de police) peut être saisi — voir les coordonnées plus bas.",
  },
  {
    t: "4 · Faites-vous accompagner",
    d: "Un avocat, ou une association comme la Ligue des Droits Humains, peut vous aider à rédiger et à faire valoir vos droits. L'aide juridique peut être gratuite selon vos revenus.",
  },
];

const sources = [
  { label: "Belgium.be — Plaintes et déclarations (victime)", url: "https://www.belgium.be/fr/justice/victime/plaintes_et_declarations" },
  { label: "SPF Justice — Audition et droits de la victime", url: "https://justice.belgium.be/fr/themes_et_dossiers/que_faire_comme/victime/procedure/audition_et_droits" },
  { label: "Ministère public — Que faire en tant que victime", url: "https://www.om-mp.be/fr/que-faire/victime" },
  { label: "Comité P — Déposer plainte (formulaire en ligne)", url: "https://comitep.be/deacuteposer-plainte.html" },
  { label: "Police fédérale — Formulaire de plainte (insatisfait du service)", url: "https://www.police.be/5998/fr/contact/insatisfait-de-nos-services/complaints-form" },
];

const readText = `Porter plainte en Belgique : vos droits. ${droitsExiger
  .map((x) => x.t + ". " + x.d)
  .join(" ")} Si le commissariat refuse votre plainte : ${siRefus
  .map((x) => x.t + ". " + x.d)
  .join(" ")} Si la police adopte un comportement anormal, ou si vous êtes témoin de faits, vous pouvez saisir le Comité P, qui contrôle les services de police, par son formulaire en ligne ou par courrier. Restez factuel, gardez vos preuves. Tout ceci est une information générale : pour défendre vos droits, consultez un avocat.`;

export default function PorterPlaintePage() {
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Porter plainte · vos droits face à la police
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Porter plainte, sereinement</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Ce que vous avez le <strong className="text-white">droit d&apos;exiger</strong>, ce qu&apos;il faut faire si le
            commissariat <strong className="text-white">refuse votre plainte</strong>, et comment réagir face à un
            comportement anormal de la police. Pas à pas, sans dramatiser.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-indigo-100 bg-indigo-50/50 p-5">
          <AgentAvocat
            name="Maître Léa"
            role="Référente · droits du citoyen"
            accent="indigo"
            message="Respirez. Vous avez des droits clairs, et des solutions existent même si ça coince. On les voit ensemble, calmement."
          />
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles belges — <strong>pas un conseil juridique
            personnalisé</strong>. Pour une situation grave ou un litige avec la police, <strong>consultez un avocat</strong>.
          </p>
        </div>
      </section>

      {/* Ce que vous avez le droit d'exiger */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">✅ Ce que vous avez le droit d&apos;exiger</h2>
        <p className="text-slate-600 mt-2 text-sm leading-relaxed">Au moment de porter plainte, vous pouvez demander :</p>
        <div className="mt-6 space-y-4">
          {droitsExiger.map((x, i) => (
            <div key={i} className="rounded-2xl border border-slate-200 p-5">
              <h3 className="font-bold tracking-tight">{x.t}</h3>
              <p className="text-slate-700 text-sm mt-2 leading-relaxed">{x.d}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Si le commissariat refuse */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">🚫 Si le commissariat refuse votre plainte</h2>
          <p className="text-slate-600 mt-2 text-sm leading-relaxed">
            Cela arrive — et c&apos;est contraire à la loi. Voici comment faire acter votre plainte autrement :
          </p>
          <div className="mt-6 space-y-4">
            {siRefus.map((x, i) => (
              <div
                key={i}
                className={`rounded-2xl p-5 ${x.fort ? "border-2 border-rose-200 bg-rose-50" : "border border-slate-200 bg-white"}`}
              >
                <h3 className={`font-bold tracking-tight ${x.fort ? "text-rose-900" : ""}`}>{x.t}</h3>
                <p className={`text-sm mt-2 leading-relaxed ${x.fort ? "text-rose-900/80" : "text-slate-700"}`}>{x.d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Comportement anormal / témoin */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <div className="flex items-start gap-4 mb-6">
          <AgentAvocat name="Maître Sami" role="Référent · contrôle de la police" accent="sky" size={84} />
        </div>
        <h2 className="text-2xl font-bold tracking-tight">👀 Comportement anormal de la police, ou vous êtes témoin ?</h2>
        <p className="text-slate-700 mt-3 text-sm leading-relaxed">
          Que vous soyez directement concerné·e ou simple <strong>témoin</strong> d&apos;un comportement qui vous semble
          anormal (abus, violence, refus d&apos;agir, propos déplacés), il existe un service dédié : le
          <strong> Comité P</strong>, organe indépendant qui contrôle les services de police. Restez
          <strong> factuel·le</strong>, notez la date, l&apos;heure, le lieu, le service concerné, et conservez vos
          preuves (photos, vidéos, témoignages).
        </p>

        <div className="mt-6 rounded-2xl border-2 border-sky-200 bg-sky-50 p-6">
          <h3 className="font-bold tracking-tight text-sky-900">Comité P — comment le saisir</h3>
          <ul className="mt-3 space-y-2 text-sm text-sky-900/90 leading-relaxed">
            <li>📝 <strong>En ligne</strong> : formulaire de plainte sur le site officiel du Comité P.</li>
            <li>✉️ <strong>Par courrier</strong> : Comité permanent de contrôle des services de police (Comité P), Rue de Louvain 48/7, 1000 Bruxelles.</li>
            <li>☎️ <strong>Par téléphone</strong> (suivi de dossier) : +32 (0)2 286 28 11, en semaine 9h–12h et 14h–16h (ayez votre numéro de dossier).</li>
          </ul>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://comitep.be/deacuteposer-plainte.html" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-semibold text-white bg-sky-600 hover:bg-sky-700 rounded-lg px-4 py-2.5 transition-colors">
              🔗 Déposer plainte au Comité P (officiel)
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
            <a href="https://www.police.be/5998/fr/contact/insatisfait-de-nos-services/complaints-form" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-sky-700 bg-white border border-sky-200 hover:bg-sky-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 Police fédérale — formulaire « insatisfait de nos services »
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
          </div>
        </div>

        <div className="mt-5 rounded-2xl border border-rose-200 bg-rose-50 p-5">
          <p className="text-rose-900 text-sm leading-relaxed">
            🆘 Danger immédiat ou violence en cours ? Appelez d&apos;abord le <a href="tel:112" className="font-bold underline">112</a>.
            Pour une urgence non vitale, le <a href="tel:101" className="font-bold underline">101</a> (police).
          </p>
        </div>
      </section>

      {/* Sources officielles */}
      <section className="pb-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-xl font-bold tracking-tight">📚 Sources officielles</h2>
        <div className="mt-4 flex flex-col gap-2.5">
          {sources.map((s) => (
            <a key={s.url} href={s.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 {s.label}
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
            </a>
          ))}
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
