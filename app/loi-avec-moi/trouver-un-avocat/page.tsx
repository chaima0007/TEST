"use client";

import Link from "next/link";
import { useState } from "react";
import ReadAloud from "@/components/ReadAloud";

type Spe = {
  id: string;
  emoji: string;
  t: string;
  quand: string;
  docs: string[];
  href?: string;
};

const specialisations: Spe[] = [
  {
    id: "famille",
    emoji: "👨‍👩‍👧",
    t: "Droit de la famille",
    quand: "Divorce, séparation, garde des enfants, pensions alimentaires, succession, filiation.",
    docs: [
      "Votre carte d'identité et celles des enfants concernés",
      "Acte de mariage / contrat de cohabitation, jugements déjà rendus",
      "Preuves de revenus des deux parties (fiches de paie, avertissement-extrait de rôle)",
      "Tout courrier, accord ou échange écrit lié au litige",
    ],
    href: "/loi-avec-moi/avocat/famille",
  },
  {
    id: "travail",
    emoji: "💼",
    t: "Droit du travail",
    quand: "Licenciement, démission, harcèlement, salaire impayé, accident de travail, contrat.",
    docs: [
      "Votre contrat de travail et son règlement de travail",
      "Les fiches de paie et le compte individuel",
      "La lettre de licenciement / C4 le cas échéant",
      "Emails, avertissements, certificats médicaux, témoignages",
    ],
    href: "/loi-avec-moi/avocat/travail",
  },
  {
    id: "penal",
    emoji: "⚖️",
    t: "Droit pénal",
    quand: "Vous êtes poursuivi·e, convoqué·e par la police, ou victime d'une infraction.",
    docs: [
      "La convocation, le procès-verbal ou la citation reçue",
      "Votre carte d'identité",
      "Tout élément de preuve (photos, messages, certificats médicaux)",
      "Les coordonnées des témoins éventuels",
    ],
    href: "/loi-avec-moi/avocat/penal",
  },
  {
    id: "bail",
    emoji: "🏠",
    t: "Bail & immobilier",
    quand: "Conflit de bail, caution non rendue, expulsion, vices, voisinage, copropriété.",
    href: "/loi-avec-moi/avocat/bail",
    docs: [
      "Le bail signé et l'état des lieux d'entrée/sortie",
      "Les preuves de paiement du loyer et de la caution",
      "Les photos et constats des problèmes",
      "Les courriers échangés avec le propriétaire / locataire",
    ],
  },
  {
    id: "etrangers",
    emoji: "🌍",
    t: "Droit des étrangers / séjour",
    quand: "Titre de séjour, regroupement familial, asile, recours contre une décision (CGRA, Office des étrangers).",
    docs: [
      "Votre passeport et tout titre de séjour / annexe reçus",
      "La décision contestée et son enveloppe (la date compte !)",
      "Les preuves de votre situation (travail, famille, logement)",
      "Tout document de procédure déjà entamée",
    ],
  },
  {
    id: "dettes",
    emoji: "💳",
    t: "Dettes & consommation",
    quand: "Surendettement, litige avec un commerçant, crédit, huissier, médiation de dettes.",
    docs: [
      "Les contrats et factures litigieux",
      "Les mises en demeure et courriers d'huissier",
      "Un relevé de vos dettes et de vos revenus/charges",
      "Les preuves de paiement déjà effectués",
    ],
  },
  {
    id: "accidents",
    emoji: "🚑",
    t: "Accidents & responsabilité",
    quand: "Accident de la route, dommage corporel, litige avec une assurance, faute médicale.",
    docs: [
      "Le constat d'accident et le PV de police",
      "Tous les certificats et rapports médicaux",
      "Les échanges avec l'assurance et son offre éventuelle",
      "Les justificatifs de frais et de pertes de revenus",
    ],
  },
  {
    id: "entreprise",
    emoji: "🏢",
    t: "Entreprise & commercial",
    quand: "Litige entre sociétés, contrats commerciaux, impayés B2B, faillite, statuts.",
    docs: [
      "Les statuts et données d'entreprise (numéro BCE)",
      "Les contrats et bons de commande concernés",
      "Les factures impayées et rappels",
      "La correspondance commerciale liée au litige",
    ],
  },
];

const readText = `Trouver le bon avocat, en Belgique. Important : nous ne sommes pas avocats et ceci ne remplace pas une consultation. Mais on vous oriente tout de suite vers la bonne spécialisation, et surtout, on vous dit quels documents préparer pour arriver prêt·e — ce qui fait gagner du temps et de l'argent. ${specialisations
  .map((s) => s.t + ". Quand : " + s.quand + " Documents à apporter : " + s.docs.join(", ") + ".")
  .join(" ")} Si vos revenus sont modestes, l'aide juridique peut être partiellement ou totalement gratuite, via le Bureau d'Aide Juridique. Le premier conseil de première ligne, lui, est gratuit pour tout le monde.`;

export default function TrouverUnAvocatPage() {
  const [open, setOpen] = useState<string | null>(null);

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
            Trouver le bon avocat
          </span>
          <h1 className="text-3xl sm:text-5xl font-bold tracking-tight leading-tight">La bonne spécialisation, vos documents prêts</h1>
          <p className="text-lg text-slate-300 mt-5 leading-relaxed">
            Réponse immédiate : on identifie <strong className="text-white">le type d&apos;avocat qu&apos;il vous faut</strong> et
            la <strong className="text-white">liste des documents à apporter</strong>. Vous arrivez préparé·e — ça fait
            gagner du temps et de l&apos;argent.
          </p>
          <div className="mt-7 flex justify-center">
            <ReadAloud text={readText} label="Tout écouter à voix haute" />
          </div>
        </div>
      </section>

      {/* Avertissement honnête */}
      <section className="px-6 -mt-px">
        <div className="max-w-3xl mx-auto mt-8 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-900 text-sm leading-relaxed">
            ⚠️ <strong>Important — soyons clairs :</strong> nous ne sommes pas avocats et cet outil <strong>ne remplace
            pas une consultation juridique</strong>. Pour défendre vos droits, <strong>consultez toujours un avocat</strong>.
            Notre rôle : vous orienter vers la bonne spécialisation et vous aider à <strong>tout préparer</strong> pour
            que votre rendez-vous soit efficace.
          </p>
        </div>
      </section>

      {/* Spécialisations cliquables */}
      <section className="py-14 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight text-center">Quelle est votre situation ?</h2>
        <p className="text-slate-500 mt-3 text-center">Touchez un domaine : on vous dit quand consulter et quoi apporter.</p>

        <div className="mt-8 space-y-3">
          {specialisations.map((s) => {
            const isOpen = open === s.id;
            return (
              <div key={s.id} className={`rounded-2xl border transition-all ${isOpen ? "border-indigo-300 shadow-md" : "border-slate-200"}`}>
                <button
                  type="button"
                  onClick={() => setOpen(isOpen ? null : s.id)}
                  aria-expanded={isOpen}
                  className="w-full text-left p-5 flex items-center gap-4"
                >
                  <span className="text-3xl flex-shrink-0" aria-hidden>{s.emoji}</span>
                  <span className="flex-1">
                    <span className="block font-bold tracking-tight">{s.t}</span>
                    <span className="block text-xs text-slate-500 mt-0.5">{s.quand}</span>
                  </span>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className={`w-5 h-5 text-slate-400 flex-shrink-0 transition-transform ${isOpen ? "rotate-180" : ""}`}><path d="M6 9l6 6 6-6" strokeLinecap="round" strokeLinejoin="round" /></svg>
                </button>
                {isOpen && (
                  <div className="px-5 pb-5 -mt-1 pl-[4.25rem]">
                    <p className="text-sm font-semibold text-slate-800 mb-2">📎 Documents à apporter à votre avocat :</p>
                    <ul className="space-y-2">
                      {s.docs.map((d, i) => (
                        <li key={i} className="flex items-start gap-2.5 text-sm text-slate-700 leading-relaxed">
                          <span className="flex-shrink-0 w-5 h-5 rounded-md border-2 border-indigo-300 mt-0.5" aria-hidden />
                          {d}
                        </li>
                      ))}
                    </ul>
                    {s.href && (
                      <Link href={s.href} className="inline-flex items-center gap-1.5 mt-4 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg px-4 py-2.5 transition-colors">
                        📖 Fiche détaillée &amp; documents officiels →
                      </Link>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </section>

      {/* Aide juridique gratuite */}
      <section className="py-12 px-6 bg-slate-50">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold tracking-tight">Un avocat coûte trop cher ? L&apos;aide juridique existe</h2>
          <div className="mt-6 space-y-4">
            <div className="bg-white rounded-2xl border border-emerald-200 p-5">
              <h3 className="font-bold tracking-tight text-emerald-900">1️⃣ Première ligne — gratuite pour tous</h3>
              <p className="text-slate-700 text-sm mt-2 leading-relaxed">
                Un premier conseil juridique bref, <strong>sans condition de revenus</strong> : on vous informe et on
                vous oriente. Idéal pour savoir si vous avez besoin d&apos;un avocat et lequel.
              </p>
            </div>
            <div className="bg-white rounded-2xl border border-indigo-200 p-5">
              <h3 className="font-bold tracking-tight text-indigo-900">2️⃣ Deuxième ligne (« pro deo ») — selon vos revenus</h3>
              <p className="text-slate-700 text-sm mt-2 leading-relaxed">
                Pour être assisté·e ou représenté·e par un avocat, <strong>partiellement ou totalement gratuitement</strong>,
                selon vos revenus. Le <strong>Bureau d&apos;Aide Juridique (BAJ)</strong> vérifie vos conditions et vous
                désigne un avocat.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Annuaires officiels */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight">Trouver un avocat — sources officielles</h2>
        <div className="mt-5 flex flex-col gap-2.5">
          <a href="https://avocats.be/fr" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
            🔗 AVOCATS.BE — annuaire des avocats & premier conseil (officiel)
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </a>
          <a href="https://avocats.be/fr/bureaux-daide-juridique" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
            🔗 Bureaux d&apos;Aide Juridique (BAJ) — coordonnées par région
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </a>
          <a href="https://justice.belgium.be/fr/besoin_dun_avis_juridique" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 text-sm font-medium text-indigo-700 bg-indigo-50 border border-indigo-200 hover:bg-indigo-100 rounded-lg px-4 py-2.5 transition-colors">
            🔗 SPF Justice — besoin d&apos;un avis juridique ? (officiel)
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3"><path d="M7 17L17 7M17 7H8M17 7v9" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </a>
        </div>
        <div className="mt-6 rounded-2xl border border-amber-200 bg-amber-50 p-5">
          <p className="text-amber-800 text-sm leading-relaxed">
            ⚖️ Les conditions de revenus de l&apos;aide juridique sont revues régulièrement : vérifiez les montants à
            jour auprès du BAJ. Informations générales tirées de sources officielles belges (AVOCATS.BE, SPF Justice).
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href="/loi-avec-moi" className="hover:text-slate-900">← Retour à « La loi avec moi »</Link>
      </footer>
    </main>
  );
}
