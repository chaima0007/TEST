"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";

const steps = [
  {
    t: "1. Signalez le vol à la police locale",
    d: "En cas de vol, allez au commissariat le plus proche et demandez un document attestant le vol (procès-verbal). Il vous sera utile pour l'ambassade et les assurances.",
  },
  {
    t: "2. Bloquez vos documents avec DOC STOP",
    d: "Appelez DOC STOP, le service gratuit qui bloque vos documents d'identité belges perdus ou volés, pour éviter toute fraude. Numéro gratuit : 00800 2123 2123 (depuis l'étranger, sinon +32 2 518 2123).",
    phone: "00800 2123 2123",
  },
  {
    t: "3. Contactez l'ambassade ou le consulat belge",
    d: "Contactez la représentation belge du pays où vous êtes. Elle vous explique la marche à suivre pour rentrer ou continuer votre voyage.",
  },
  {
    t: "4. Demandez un titre de voyage provisoire",
    d: "Si vous ne pouvez pas rentrer sans document, l'ambassade peut, dans certains cas, délivrer un passeport provisoire ou un titre de voyage (« ETD ») pour rentrer en Belgique.",
  },
];

const avant = [
  {
    t: "Prenez une assurance avant de partir",
    d: "Dans l'UE/EEE + Suisse : la Carte Européenne d'Assurance Maladie (CEAM) est GRATUITE via votre mutuelle et couvre les soins médicaux nécessaires. Hors UE, une assurance assistance-rapatriement est vivement conseillée : sans elle, des soins ou un rapatriement peuvent coûter des dizaines de milliers d'euros. Vérifiez aussi ce que couvre déjà votre carte bancaire.",
    cta: "Carte Européenne d'Assurance Maladie (officiel)",
    url: "https://www.belgium.be/fr/sante/en_voyage/carte_europeenne",
  },
  {
    t: "Inscrivez-vous sur « Travellers Online »",
    d: "Avant un voyage, enregistrez-vous gratuitement sur le service des Affaires étrangères. En cas de crise (catastrophe, attentat, guerre), l'État sait que vous êtes sur place et peut vous contacter.",
    cta: "Travellers Online (officiel)",
    url: "https://travellersonline.diplomatie.be/",
  },
  {
    t: "Vérifiez les conseils aux voyageurs",
    d: "Les Affaires étrangères publient un avis par pays (sécurité, zones à éviter, situation de guerre). À consulter avant ET pendant le voyage.",
    cta: "Conseils aux voyageurs (officiel)",
    url: "https://diplomatie.belgium.be/fr/conseils-aux-voyageurs",
  },
  {
    t: "Faites des copies de vos papiers",
    d: "Gardez une photo de votre passeport et de votre carte d'identité dans votre téléphone et dans votre boîte mail. Ça accélère énormément les démarches sur place.",
  },
];

const readText = `Belge à l'étranger : que faire si vous perdez vos papiers. ${steps
  .map((s) => s.t + ". " + s.d)
  .join(" ")} Avant de partir : ${avant.map((a) => a.t + ". " + a.d).join(" ")} L'annuaire officiel des ambassades belges est toujours à jour sur le site des Affaires étrangères.`;

export default function BelgeALetrangerPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La loi avec moi</span>
          </Link>
          <Link href="/loi-avec-moi/mes-droits-maintenant" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">Mes droits →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(79,70,229,0.25),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Belge à l&apos;étranger
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Vos papiers perdus ou volés loin de chez vous</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Perdre ses papiers à l&apos;étranger, c&apos;est stressant. Voici les bons réflexes, étape par étape —
            et comment joindre l&apos;ambassade belge la plus proche.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Bouton annuaire officiel — toujours à jour */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border-2 border-indigo-200 bg-indigo-50 p-6 text-center">
          <h2 className="text-xl font-bold tracking-tight text-indigo-900">Trouver l&apos;ambassade belge la plus proche</h2>
          <p className="text-indigo-900/80 text-sm mt-2 leading-relaxed max-w-xl mx-auto">
            L&apos;annuaire officiel des Affaires étrangères est <strong>tenu à jour en permanence</strong> (adresses,
            téléphones, horaires). On vous y envoie directement — c&apos;est la source la plus fiable, surtout en cas
            de crise.
          </p>
          <a
            href="https://diplomatie.belgium.be/fr/ambassades-et-consulats"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 mt-5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-3.5 rounded-xl transition-colors shadow-lg shadow-indigo-600/30"
          >
            🌍 Ouvrir l&apos;annuaire officiel des ambassades
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </a>
        </div>
      </section>

      {/* Étapes */}
      <section className="pb-8 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">Si on vous vole (ou si vous perdez) vos papiers</h2>
        <div className="mt-6 space-y-4">
          {steps.map((s, i) => (
            <div key={i} className="rounded-2xl border border-slate-200 p-5">
              <h3 className="text-lg font-bold tracking-tight">{s.t}</h3>
              <p className="text-slate-700 text-sm mt-2 leading-relaxed">{s.d}</p>
              {s.phone && (
                <a href={`tel:${s.phone.replace(/\s/g, "")}`} className="inline-flex items-center gap-2 mt-3 bg-rose-600 hover:bg-rose-700 text-white text-sm font-semibold rounded-lg px-4 py-2 transition-colors">
                  📞 Appeler DOC STOP — {s.phone}
                </a>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Avant de partir */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Avant de partir : les bons réflexes</h2>
          <div className="mt-6 space-y-4">
            {avant.map((a, i) => (
              <div key={i} className="bg-white rounded-2xl border border-slate-200 p-5">
                <h3 className="text-lg font-bold tracking-tight">{a.t}</h3>
                <p className="text-slate-700 text-sm mt-2 leading-relaxed">{a.d}</p>
                {a.url && (
                  <a href={a.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-xs font-medium text-indigo-700 mt-3 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-3 py-2 transition-colors">
                    🔗 {a.cta}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Note guerre / honnêteté */}
      <section className="py-12 px-6 max-w-3xl mx-auto space-y-5">
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-5">
          <h3 className="font-semibold text-rose-900">⚠️ En cas de guerre ou de crise</h3>
          <p className="text-rose-800 text-sm mt-2 leading-relaxed">
            Dans certains pays, des ambassades peuvent être <strong>fermées ou inaccessibles</strong> (conflit,
            catastrophe). C&apos;est pourquoi on ne fige pas une liste ici : l&apos;annuaire officiel et les conseils
            aux voyageurs sont mis à jour en temps réel et indiquent l&apos;ambassade « de repli » compétente.
            Si vous êtes inscrit·e sur Travellers Online, l&apos;État peut vous joindre directement.
          </p>
        </div>
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Informations générales tirées des sources officielles belges (SPF Affaires étrangères —
            diplomatie.belgium.be). Pour votre situation précise, suivez les instructions de l&apos;ambassade ou
            du consulat compétent.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
