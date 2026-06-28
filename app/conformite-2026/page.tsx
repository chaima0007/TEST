"use client";

import Link from "next/link";
import { useState } from "react";

// Page « Conformité 2026 » + simulateur « Suis-je concerné ? » — Caelum (ENTREPRISES, séparé de La Loi Avec Moi).
// Données alignées sur data/caelum/conformite_entreprises.json (chiffres vérifiés, post-Omnibus 2026).

type Norme = {
  id: string;
  nom: string;
  change: string;
  sanction: string;
  echeance: string;
  concerne: (p: Profil) => "oui" | "cascade" | "non";
};

type Profil = { tva: string; taille: string; secteur: string; donnees: string };

// taille en nombre d'employés (seuils simplifiés, croisés avec le CA dans les libellés)
const TAILLES = [
  { id: "lt50", label: "Moins de 50", n: 25 },
  { id: "50_249", label: "50 à 249", n: 150 },
  { id: "250_999", label: "250 à 999", n: 500 },
  { id: "1000_4999", label: "1 000 à 4 999", n: 2500 },
  { id: "5000", label: "5 000 et +", n: 6000 },
];

function nEmp(taille: string) {
  return TAILLES.find((t) => t.id === taille)?.n ?? 0;
}

const NORMES: Norme[] = [
  {
    id: "efacture",
    nom: "Facturation électronique B2B",
    change: "Factures B2B en format électronique structuré (Peppol) obligatoires. Le PDF simple perd sa valeur fiscale.",
    sanction: "Amendes + perte de la déduction TVA",
    echeance: "Depuis le 01/01/2026",
    concerne: (p) => (p.tva === "oui" ? "oui" : "non"),
  },
  {
    id: "rgpd",
    nom: "RGPD — protection des données",
    change: "Toute entreprise qui traite des données (clients, employés, prospects, cookies) doit être en règle.",
    sanction: "Jusqu'à 20 M€ ou 4 % du CA mondial",
    echeance: "En vigueur",
    concerne: (p) => (p.donnees === "oui" ? "oui" : "non"),
  },
  {
    id: "lanceurs",
    nom: "Lanceurs d'alerte",
    change: "Canal de signalement interne sécurisé obligatoire et protection contre les représailles.",
    sanction: "Sanctions pénales + administratives",
    echeance: "En vigueur",
    concerne: (p) => (nEmp(p.taille) >= 50 ? "oui" : "non"),
  },
  {
    id: "nis2",
    nom: "NIS2 — cybersécurité",
    change: "Mesures de cybersécurité, gestion des incidents, enregistrement au CCB. Responsabilité du dirigeant renforcée.",
    sanction: "10 M€ ou 2 % du CA mondial (essentielles) · 7 M€ ou 1,4 % (importantes)",
    echeance: "En vigueur (18/10/2024)",
    concerne: (p) => (p.secteur === "oui" && nEmp(p.taille) >= 50 ? "oui" : "non"),
  },
  {
    id: "csrd",
    nom: "CSRD — rapport de durabilité",
    change: "Reporting de durabilité (ESRS). Champ réduit par l'Omnibus : > 1 000 salariés et > 450 M€ de CA.",
    sanction: "Selon transposition + risque de perte de marchés",
    echeance: "Exercices ≥ 01/01/2027",
    concerne: (p) => (nEmp(p.taille) >= 1000 ? "oui" : nEmp(p.taille) >= 250 ? "cascade" : "non"),
  },
  {
    id: "csddd",
    nom: "CSDDD — devoir de vigilance",
    change: "Vigilance sur la chaîne de valeur. Vise les très grands groupes : > 5 000 salariés et > 1,5 Md€ de CA.",
    sanction: "Jusqu'à 3 % du CA mondial",
    echeance: "Application 26/07/2029",
    concerne: (p) => (nEmp(p.taille) >= 5000 ? "oui" : nEmp(p.taille) >= 250 ? "cascade" : "non"),
  },
];

export default function Conformite2026Page() {
  const [p, setP] = useState<Profil>({ tva: "", taille: "", secteur: "", donnees: "" });
  const [res, setRes] = useState<{ directs: Norme[]; cascade: Norme[] } | null>(null);

  const pret = p.tva && p.taille && p.secteur && p.donnees;

  function analyser() {
    if (!pret) return;
    const directs = NORMES.filter((n) => n.concerne(p) === "oui");
    const cascade = NORMES.filter((n) => n.concerne(p) === "cascade");
    setRes({ directs, cascade });
  }

  function Choix({
    titre,
    cle,
    options,
  }: {
    titre: string;
    cle: keyof Profil;
    options: { id: string; label: string }[];
  }) {
    return (
      <div>
        <h3 className="font-semibold text-slate-800 mb-3">{titre}</h3>
        <div className="flex flex-wrap gap-2">
          {options.map((o) => (
            <button
              key={o.id}
              type="button"
              onClick={() => {
                setP({ ...p, [cle]: o.id });
                setRes(null);
              }}
              className={
                "px-4 py-2 rounded-full border text-sm font-medium transition-colors " +
                (p[cle] === o.id
                  ? "bg-indigo-600 border-indigo-600 text-white"
                  : "bg-white border-slate-300 text-slate-700 hover:border-indigo-400")
              }
            >
              {o.label}
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg tracking-tight">Caelum</span>
          </Link>
          <Link
            href="/contact"
            className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-colors"
          >
            Demander un devis
          </Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 to-slate-900 text-white py-20 px-6">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_0%,rgba(37,99,235,0.22),transparent_60%)]" />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <span className="inline-block px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-slate-200 text-sm font-medium mb-6">
            Conformité 2026
          </span>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight leading-tight">
            Les normes ont changé.
            <span className="block bg-gradient-to-r from-indigo-300 to-sky-300 bg-clip-text text-transparent">
              La solution, c&apos;est nous.
            </span>
          </h1>
          <p className="text-lg text-slate-300 mt-6 leading-relaxed">
            Dès qu&apos;une norme qui vous concerne change, on vous prévient, on vous l&apos;explique en clair,
            et on vous met en conformité — automatiquement quand c&apos;est possible, avec un expert quand il le faut.
          </p>
        </div>
      </section>

      {/* Simulateur */}
      <section className="py-16 px-6 max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold text-center">Suis-je concerné ?</h2>
        <p className="text-slate-500 text-center mt-2 mb-8">4 questions, et vous savez exactement où vous en êtes.</p>

        <div className="bg-white rounded-2xl border border-slate-200 p-7 space-y-7 shadow-sm">
          <Choix
            titre="1. Êtes-vous assujetti à la TVA en Belgique ?"
            cle="tva"
            options={[{ id: "oui", label: "Oui" }, { id: "non", label: "Non" }]}
          />
          <Choix titre="2. Combien d'employés ?" cle="taille" options={TAILLES} />
          <Choix
            titre="3. Secteur critique ? (énergie, transport, santé, eau, numérique, finance…)"
            cle="secteur"
            options={[{ id: "oui", label: "Oui" }, { id: "non", label: "Non / je ne sais pas" }]}
          />
          <Choix
            titre="4. Traitez-vous des données personnelles (clients, employés) ?"
            cle="donnees"
            options={[{ id: "oui", label: "Oui" }, { id: "non", label: "Non" }]}
          />

          <button
            type="button"
            onClick={analyser}
            disabled={!pret}
            className={
              "w-full py-3.5 rounded-xl font-semibold transition-colors " +
              (pret
                ? "bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-600/20"
                : "bg-slate-200 text-slate-400 cursor-not-allowed")
            }
          >
            Voir les normes qui me concernent
          </button>
        </div>

        {res && (
          <div className="mt-10">
            <h3 className="text-xl font-bold">
              {res.directs.length} norme{res.directs.length > 1 ? "s" : ""} vous concerne
              {res.directs.length > 1 ? "nt" : ""} directement
            </h3>
            {res.directs.length === 0 && (
              <p className="mt-2 text-slate-600 text-sm">
                Aucune obligation lourde directe d&apos;après vos réponses — mais lisez l&apos;effet cascade ci-dessous,
                et la veille reste utile pour ne rien rater.
              </p>
            )}
            <div className="mt-5 grid gap-4">
              {res.directs.map((n) => (
                <article key={n.id} className="rounded-2xl border border-slate-200 p-5 bg-white">
                  <div className="flex items-start justify-between gap-3">
                    <h4 className="font-semibold text-lg text-slate-900">{n.nom}</h4>
                    <span className="text-xs whitespace-nowrap px-2 py-1 rounded-full bg-red-50 text-red-700 border border-red-200">
                      {n.echeance}
                    </span>
                  </div>
                  <p className="mt-2 text-slate-600 text-sm leading-relaxed">{n.change}</p>
                  <p className="mt-3 text-sm font-medium text-red-700">⚠️ Sanction : {n.sanction}</p>
                </article>
              ))}
            </div>

            {res.cascade.length > 0 && (
              <div className="mt-8">
                <h3 className="text-lg font-bold text-slate-800">L&apos;effet cascade (à anticiper)</h3>
                <p className="text-slate-600 text-sm mt-1">
                  Vous n&apos;êtes pas directement visé, mais vos grands clients le sont : ils répercutent leurs
                  obligations sur leurs fournisseurs. Être prêt = garder (et gagner) ces marchés.
                </p>
                <div className="mt-4 grid gap-4">
                  {res.cascade.map((n) => (
                    <article key={n.id} className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
                      <h4 className="font-semibold text-slate-900">{n.nom}</h4>
                      <p className="mt-1 text-slate-700 text-sm">{n.change}</p>
                    </article>
                  ))}
                </div>
              </div>
            )}

            <div className="mt-8 rounded-2xl bg-indigo-600 text-white p-7 text-center">
              <h3 className="text-xl font-bold">On vous met en conformité</h3>
              <p className="text-indigo-100 mt-2 text-sm leading-relaxed">
                Diagnostic, mise en règle (automatisée quand c&apos;est possible), et veille continue.
                Et le combo gagnant : on cherche aussi la subvention publique qui finance votre mise en conformité.
              </p>
              <Link
                href="/contact"
                className="inline-block mt-5 bg-white text-indigo-700 font-semibold px-7 py-3 rounded-xl hover:bg-indigo-50 transition-colors"
              >
                Parler de ma conformité
              </Link>
            </div>
          </div>
        )}
      </section>

      {/* Transparence */}
      <section className="py-12 px-6 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h3 className="font-semibold text-amber-900">⚖️ En toute transparence</h3>
          <p className="text-amber-800 text-sm mt-2 leading-relaxed">
            Ce simulateur donne une première orientation à partir de seuils officiels (post-Omnibus 2026). Les seuils
            et montants peuvent évoluer ; on vérifie toujours votre situation précise avant tout engagement. Pas de
            promesse en l&apos;air : c&apos;est ce qui fait notre crédibilité.
          </p>
        </div>
      </section>
    </main>
  );
}
