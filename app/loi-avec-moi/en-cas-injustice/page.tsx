"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// En cas d'injustice : quel service contacter (Belgique). Routeur vers les recours officiels.
// Faits vérifiés : Unia (unia.be), Médiateur fédéral (mediateurfederal.be), Institut pour l'égalité
// des femmes et des hommes (igvm-iefh.belgium.be), Service de Médiation pour le Consommateur,
// Comité P (comitep.be), Belgium.be.

type Recours = {
  emoji: string;
  t: string;
  quand: string;
  service: string;
  detail: string;
  lien?: { label: string; url: string };
  tel?: string;
  interne?: string;
};

const recours: Recours[] = [
  {
    emoji: "⚖️",
    t: "Discrimination",
    quand: "Traité·e injustement à cause de votre origine, couleur, handicap, âge, religion, conviction, orientation sexuelle, état de santé…",
    service: "Unia — Institut interfédéral pour l'égalité des chances",
    detail: "Signalement gratuit et confidentiel. Unia peut vous informer, vous orienter et, si besoin, intervenir.",
    lien: { label: "unia.be — signaler une discrimination", url: "https://www.unia.be/fr/signaler-une-discrimination" },
    tel: "0800 12 800",
  },
  {
    emoji: "♀️",
    t: "Inégalité ou violence de genre",
    quand: "Discrimination ou violence liée au sexe, au genre, à la grossesse, à la maternité ou à la transition.",
    service: "Institut pour l'égalité des femmes et des hommes",
    detail: "Service public spécialisé dans les discriminations fondées sur le sexe et le genre. Accueil et accompagnement gratuits.",
    lien: { label: "igvm-iefh.belgium.be (officiel)", url: "https://igvm-iefh.belgium.be/fr" },
  },
  {
    emoji: "🏛️",
    t: "Problème avec une administration",
    quand: "Un service public fédéral ne répond pas, fait une erreur, ou vous traite mal (impôts, sécurité sociale, asile, mobilité…).",
    service: "Médiateur fédéral (Ombudsman)",
    detail: "Organe indépendant qui examine gratuitement les plaintes contre les administrations fédérales. Pour les Régions, il existe aussi des médiateurs (wallon, flamand, bruxellois).",
    lien: { label: "mediateurfederal.be — déposer une plainte", url: "https://www.mediateurfederal.be/fr" },
  },
  {
    emoji: "👮",
    t: "Comportement d'un policier",
    quand: "Abus, violence, refus d'acter une plainte, propos déplacés — que vous soyez concerné·e ou témoin.",
    service: "Comité P (contrôle des services de police)",
    detail: "Organe indépendant. Voir notre fiche dédiée pour la marche à suivre, l'adresse et le formulaire.",
    interne: "/loi-avec-moi/porter-plainte",
  },
  {
    emoji: "🛒",
    t: "Litige avec un commerçant / une entreprise",
    quand: "Achat, abonnement, facture contestée, service non rendu : un conflit de consommation.",
    service: "Service de Médiation pour le Consommateur",
    detail: "Service public fédéral qui aide gratuitement à résoudre les litiges entre consommateurs et entreprises, à l'amiable.",
    lien: { label: "mediationconsommateur.be (officiel)", url: "https://mediationconsommateur.be/fr" },
  },
  {
    emoji: "🕊️",
    t: "Atteinte aux droits humains",
    quand: "Une situation qui touche vos droits fondamentaux et ne relève pas d'un service ci-dessus.",
    service: "Institut fédéral pour la protection des droits humains (IFDH) / Ligue des Droits Humains",
    detail: "L'IFDH couvre les « zones blanches » non prises en charge par un autre organe. La Ligue des Droits Humains accompagne aussi les citoyens.",
    lien: { label: "federalinstituthumanrights.be (officiel)", url: "https://federalinstituthumanrights.be/fr/" },
  },
  {
    emoji: "📑",
    t: "Vous voulez agir en justice",
    quand: "Faire reconnaître votre droit devant un tribunal, ou simplement savoir si vous avez un dossier solide.",
    service: "Avocat & aide juridique",
    detail: "Le premier conseil juridique est gratuit pour tous ; l'aide juridique « pro deo » peut couvrir l'avocat selon vos revenus.",
    interne: "/loi-avec-moi/trouver-un-avocat",
  },
];

const readText = `En cas d'injustice, en Belgique : quel service contacter. Vous n'êtes pas seul·e, et il existe presque toujours un recours gratuit. ${recours
  .map((r) => r.t + ". " + r.quand + " Service : " + r.service + ". " + r.detail)
  .join(" ")} En cas de danger immédiat, appelez toujours le 112. Ceci est une information générale et ne remplace pas un conseil juridique personnalisé.`;

export default function EnCasInjusticePage() {
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
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(16,185,129,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            En cas d&apos;injustice · quel service contacter
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Une injustice ? Voici qui contacter</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Discrimination, administration, police, litige, droits humains : pour chaque situation, le
            <strong className="text-white"> bon service officiel</strong> — souvent gratuit. On vous y emmène directement.
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
            name="Inès"
            role="Assistante · recours & droits"
            accent="emerald"
            message="Se sentir traité·e injustement, c'est éprouvant. La bonne nouvelle : il existe presque toujours un recours, et souvent gratuit."
          />
        </div>
      </section>

      {/* Recours */}
      <section className="py-14 px-6 max-w-3xl mx-auto space-y-4">
        {recours.map((r, i) => (
          <div key={i} className="rounded-2xl border border-slate-200 p-6">
            <h2 className="text-lg font-bold tracking-tight flex items-center gap-2.5">
              <span className="text-2xl" aria-hidden>{r.emoji}</span>{r.t}
            </h2>
            <p className="text-slate-500 text-sm mt-1.5 leading-relaxed italic">{r.quand}</p>
            <div className="mt-4 rounded-xl bg-slate-50 border border-slate-100 p-4">
              <p className="font-semibold text-sm text-slate-900">➡️ {r.service}</p>
              <p className="text-slate-700 text-sm mt-1.5 leading-relaxed">{r.detail}</p>
              <div className="mt-3 flex flex-col gap-2">
                {r.tel && (
                  <a href={`tel:${r.tel.replace(/\s/g, "")}`} className="inline-flex items-center justify-between gap-3 rounded-lg bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 px-4 py-2.5 transition-colors">
                    <span className="text-sm font-semibold text-emerald-900">Appeler (gratuit)</span>
                    <span className="text-emerald-700 font-bold text-sm">📞 {r.tel}</span>
                  </a>
                )}
                {r.lien && (
                  <a href={r.lien.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-white border border-indigo-200 hover:bg-indigo-50 rounded-lg px-4 py-2.5 transition-colors">
                    🔗 {r.lien.label}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
                  </a>
                )}
                {r.interne && (
                  <Link href={r.interne} className="inline-flex items-center gap-1.5 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg px-4 py-2.5 transition-colors">
                    📖 Voir la fiche détaillée →
                  </Link>
                )}
              </div>
            </div>
          </div>
        ))}
      </section>

      {/* Danger immédiat */}
      <section className="pb-8 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-5">
          <p className="text-rose-900 text-sm leading-relaxed">
            🆘 En danger immédiat ? Appelez le <a href="tel:112" className="font-bold underline">112</a>. Besoin d&apos;aide
            tout de suite (violences, détresse) ? Voir <Link href="/loi-avec-moi/en-danger" className="font-bold underline">« En danger ? Où aller »</Link>.
          </p>
        </div>
      </section>

      {/* Disclaimer */}
      <section className="pb-14 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Ces services sont <strong>officiels, indépendants et souvent gratuits</strong>. Coordonnées vérifiées
            auprès de sources officielles belges. Information générale — pour un litige précis, faites-vous accompagner
            par un avocat.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
