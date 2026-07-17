"use client";

import Link from "next/link";
import ReadAloud from "@/components/ReadAloud";
import AgentAvocat from "@/components/AgentAvocat";

// Page « Travail & emploi » — Édition FRANCE.
// Faits vérifiés : Code du travail (art. L3141-1 et s. congés payés),
// service-public.fr (démission F2883, rupture conventionnelle R42522),
// code.travail.gouv.fr. Distinct de l'édition belge.

const pointsCles = [
  {
    t: "Démission : pas de durée légale unique de préavis",
    d: "La loi ne fixe pas un préavis universel de démission en CDI. Sa durée vient, dans l'ordre, de votre convention collective, de votre contrat, ou des usages de la profession — en pratique 1 à 3 mois (souvent 3 mois pour les cadres). Le préavis démarre à la remise de la lettre en main propre ou à la première présentation du recommandé. Vérifiez toujours votre convention collective.",
  },
  {
    t: "Rupture conventionnelle : l'accord à l'amiable encadré",
    d: "Employeur et salarié peuvent rompre le CDI d'un commun accord. La convention fixe l'indemnité (au moins égale à l'indemnité légale de licenciement) et la date de fin. Après signature, chacun dispose d'un délai de rétractation de 15 jours calendaires. Ensuite, la convention doit être homologuée par l'administration. C'est la seule rupture amiable qui ouvre droit au chômage.",
  },
  {
    t: "Congés payés : 2,5 jours ouvrables par mois",
    d: "Vous acquérez 2,5 jours ouvrables de congés payés par mois de travail effectif, soit 30 jours ouvrables (5 semaines) pour une année complète. La période de référence va, sauf accord, du 1er juin au 31 mai. Si l'employeur compte en jours ouvrés, l'équivalence est 6 ouvrables = 5 ouvrés (donc 25 jours ouvrés). Base légale : articles L3141-1 et suivants du Code du travail.",
  },
  {
    t: "Licenciement : il faut une cause réelle et sérieuse",
    d: "Un employeur ne peut pas vous licencier sans motif. La cause doit être réelle (objective, exacte, vérifiable) et sérieuse (assez grave). La procédure impose une convocation à un entretien préalable par recommandé ou remise en main propre, l'entretien ayant lieu au minimum 5 jours ouvrables après. Vous pouvez vous y faire assister.",
  },
  {
    t: "Contester : 12 mois pour saisir les prud'hommes",
    d: "Pour contester la rupture de votre contrat de travail, vous disposez en principe de 12 mois à compter de la réception de la notification du licenciement pour saisir le conseil de prud'hommes. Le délai démarre le lendemain de la réception. Passé ce délai, l'action n'est plus recevable — n'attendez pas.",
  },
];

const litige = [
  {
    n: "1",
    t: "Demandez les choses par écrit",
    d: "Bulletin de paie erroné, heures non payées, congés refusés : adressez une demande écrite (recommandé avec accusé de réception) à votre employeur, précise et datée. Gardez une copie de tout : contrat, fiches de paie, courriels. C'est la base de tout dossier.",
  },
  {
    n: "2",
    t: "Faites-vous conseiller gratuitement",
    d: "Le service public « Code du travail numérique » répond gratuitement en ligne. L'inspection du travail (DREETS) peut intervenir. Les représentants du personnel (CSE) et les syndicats vous accompagnent. Renseignez-vous avant d'agir : beaucoup de litiges se règlent sans procès.",
  },
  {
    n: "3",
    t: "Le conseil de prud'hommes",
    d: "Si le désaccord persiste, le conseil de prud'hommes tranche les litiges entre salarié et employeur. La saisine est possible sans avocat. Selon vos revenus, l'aide juridictionnelle peut financer un avocat. Attention au délai (souvent 12 mois pour la rupture).",
  },
];

const documentsOfficiels = [
  {
    label: "Service-Public.fr — Démission d'un salarié (CDI)",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F2883",
  },
  {
    label: "Service-Public.fr — Délais de la rupture conventionnelle",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/R42522",
  },
  {
    label: "Service-Public.fr — Congés payés du salarié (privé)",
    url: "https://www.service-public.gouv.fr/particuliers/vosdroits/F2258",
  },
  {
    label: "Code du travail numérique (gratuit, officiel)",
    url: "https://code.travail.gouv.fr/",
  },
];

const readText = `Travail et emploi en France : vos droits. Cette page s'appuie sur le Code du travail et des sources officielles (service-public.fr, code.travail.gouv.fr) et ne remplace pas un conseil personnalisé. ${pointsCles
  .map((p) => p.t + ". " + p.d)
  .join(" ")} En cas de litige : demandez par écrit en recommandé, faites-vous conseiller gratuitement par le Code du travail numérique ou l'inspection du travail, puis saisissez le conseil de prud'hommes en respectant le délai de douze mois pour une rupture.`;

export default function TravailFrancePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/la-loi-avec-moi-france" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi <span className="text-blue-700">· France</span></span>
          </Link>
          <Link href="/la-loi-avec-moi-france" className="text-sm font-semibold text-blue-700 hover:text-blue-900">Tous les sujets →</Link>
        </div>
      </header>

      <section className="relative overflow-hidden bg-gradient-to-b from-blue-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(99,102,241,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            🇫🇷 Travail &amp; emploi
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">Salarié — connaissez vos droits</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Préavis, rupture conventionnelle, congés payés, licenciement : l&apos;essentiel du Code du travail, adossé aux
            <strong className="text-white"> sources officielles (service-public.fr, code.travail.gouv.fr)</strong>.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Agent rassurant */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border border-indigo-100 bg-indigo-50/60 p-5">
          <AgentAvocat
            name="Karim"
            role="Assistant · droit du travail (France)"
            accent="indigo"
            message="Au travail, vos droits sont solides — encore faut-il les connaître. Le réflexe gagnant : tout par écrit, on garde chaque fiche de paie, et on ne laisse jamais filer le délai de 12 mois pour contester un licenciement."
          />
        </div>
      </section>

      {/* Encadré le bon réflexe */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-indigo-300 bg-indigo-50 p-5">
          <p className="text-indigo-900 text-sm leading-relaxed">
            🔑 <strong>À retenir :</strong> après une rupture conventionnelle, vous avez <strong>15 jours</strong> pour
            vous rétracter. Et pour contester un licenciement aux prud&apos;hommes, vous avez en général
            <strong> 12 mois</strong> à compter de la notification — pas un de plus.
          </p>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6">
        <div className="max-w-3xl mx-auto mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ Information générale fondée sur des sources officielles françaises, <strong>pas un conseil juridique
            personnalisé</strong>. Beaucoup de règles (préavis notamment) dépendent de votre <strong>convention
            collective</strong> : vérifiez-la, ou interrogez le Code du travail numérique (gratuit).
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
                <span className="flex-shrink-0 w-9 h-9 rounded-full bg-indigo-100 text-indigo-800 font-bold flex items-center justify-center">{e.n}</span>
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
          Service-public.fr et le Code du travail numérique (édité par le ministère du Travail) sont les références
          françaises. Ces pages font foi et sont tenues à jour.
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
            Le Code du travail numérique répond gratuitement à vos questions. L&apos;inspection du travail (DREETS)
            contrôle le respect du droit. Le conseil de prud&apos;hommes tranche les litiges, sans avocat obligatoire,
            et l&apos;aide juridictionnelle peut financer un avocat selon vos revenus.
          </p>
          <div className="mt-4 flex flex-col gap-2.5">
            <a href="https://code.travail.gouv.fr/" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-blue-700 bg-white border border-blue-200 hover:bg-blue-100 rounded-lg px-4 py-2.5 transition-colors">
              🔗 Code du travail numérique — réponses gratuites
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
        <Link href="/loi-avec-moi/travail" className="text-slate-500 hover:text-slate-900">🇧🇪 Version Belgique</Link>
      </footer>
    </main>
  );
}
