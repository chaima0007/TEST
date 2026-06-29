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

type Profil = { tva: string; taille: string; secteur: string; donnees: string; ia: string; numerique_public: string; secteur_financier: string; plateforme: string; emballages: string; import_produits: string };

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
  {
    id: "ubo",
    nom: "Registre UBO — bénéficiaires effectifs",
    change: "Déclarer ses bénéficiaires effectifs au registre UBO et CONFIRMER les données chaque année (même sans changement).",
    sanction: "Amende administrative de 250 € à 50 000 € + risque de radiation de la BCE",
    echeance: "Déclaration sous 30 j + confirmation annuelle",
    concerne: () => "oui",
  },
  {
    id: "ai-act",
    nom: "AI Act — règlement IA",
    change: "Obligations graduées selon le risque pour qui développe, fournit ou UTILISE des systèmes d'IA.",
    sanction: "Jusqu'à 35 M€ ou 7 % du CA mondial (pratiques interdites) · 15 M€ ou 3 % (autres)",
    echeance: "Échelonné : 2025 → 2027",
    concerne: (p) => (p.ia === "oui" ? "oui" : "non"),
  },
  {
    id: "eaa",
    nom: "Accessibilité numérique (European Accessibility Act)",
    change: "Sites, applis, e-commerce et services numériques grand public doivent être accessibles (+ déclaration d'accessibilité).",
    sanction: "Amendes (jusqu'à ~200 000 € par manquement) · retrait possible du marché",
    echeance: "Depuis le 28/06/2025",
    concerne: (p) => (p.numerique_public === "oui" ? "oui" : "non"),
  },
  {
    id: "dora",
    nom: "DORA — résilience numérique (secteur financier)",
    change: "Cadre de gestion du risque informatique (TIC), tests de résilience, notification des incidents majeurs et maîtrise des prestataires informatiques tiers.",
    sanction: "Mesures et sanctions administratives (BNB/FSMA)",
    echeance: "En application (17/01/2025)",
    concerne: (p) => (p.secteur_financier === "oui" ? "oui" : "non"),
  },
  {
    id: "transparence-salariale",
    nom: "Transparence salariale (égalité F/H)",
    change: "Fourchette de rémunération dès l'offre d'emploi, critères objectifs, droit à l'information ; reporting de l'écart salarial dès 100 travailleurs.",
    sanction: "Selon transposition + évaluation conjointe si écart injustifié > 5 %",
    echeance: "Transposition au plus tard le 07/06/2026",
    concerne: (p) => (nEmp(p.taille) >= 100 ? "oui" : nEmp(p.taille) >= 1 ? "cascade" : "non"),
  },
  {
    id: "dac7",
    nom: "DAC7 — plateformes numériques",
    change: "Les opérateurs de plateformes doivent collecter les données de leurs vendeurs et les déclarer chaque année au SPF Finances.",
    sanction: "Amendes administratives (non-déclaration / déclaration tardive)",
    echeance: "En vigueur (déclaration annuelle)",
    concerne: (p) => (p.plateforme === "oui" ? "oui" : "non"),
  },
  {
    id: "ppwr",
    nom: "PPWR — emballages",
    change: "Réduction du suremballage, recyclabilité, contenu recyclé, étiquetage harmonisé et documentation de conformité pour les emballages mis sur le marché.",
    sanction: "Surveillance du marché : retrait/rappel possible des emballages non conformes",
    echeance: "À partir du 12/08/2026",
    concerne: (p) => (p.emballages === "oui" ? "oui" : "non"),
  },
  {
    id: "delais-paiement",
    nom: "Délais de paiement B2B",
    change: "Délai de paiement légal de 30 jours entre entreprises ; au-delà de 60 jours = en principe abusif.",
    sanction: "Intérêts de retard + indemnité forfaitaire ; clause abusive écartée",
    echeance: "En vigueur (01/02/2022)",
    concerne: (p) => (p.tva === "oui" ? "oui" : "non"),
  },
  {
    id: "cbam",
    nom: "CBAM — ajustement carbone aux frontières",
    change: "Importer acier, ciment, aluminium, engrais, électricité ou hydrogène = statut de déclarant MACF + déclaration des émissions.",
    sanction: "Sanctions + blocage possible à l'importation",
    echeance: "Régime définitif (01/01/2026)",
    concerne: (p) => (p.import_produits === "oui" ? "oui" : "non"),
  },
  {
    id: "eudr",
    nom: "EUDR — déforestation importée",
    change: "Mettre sur le marché bois, cacao, café, soja, caoutchouc, huile de palme, bovins = diligence raisonnée « zéro déforestation ».",
    sanction: "Sanctions + interdiction de mise sur le marché",
    echeance: "Application échelonnée",
    concerne: (p) => (p.import_produits === "oui" ? "oui" : "non"),
  },
  {
    id: "aml",
    nom: "Anti-blanchiment (LBC/FT)",
    change: "Vigilance client (KYC), conservation des données et déclaration des opérations suspectes à la CTIF.",
    sanction: "Sanctions administratives (BNB/FSMA) et pénales",
    echeance: "En vigueur",
    concerne: (p) => (p.secteur_financier === "oui" ? "oui" : "non"),
  },
];

export default function Conformite2026Page() {
  const [p, setP] = useState<Profil>({ tva: "", taille: "", secteur: "", donnees: "", ia: "", numerique_public: "", secteur_financier: "", plateforme: "", emballages: "", import_produits: "" });
  const [res, setRes] = useState<{ directs: Norme[]; cascade: Norme[] } | null>(null);
  const [email, setEmail] = useState("");
  const [envoi, setEnvoi] = useState<"idle" | "envoi" | "ok" | "erreur">("idle");

  const pret = p.tva && p.taille && p.secteur && p.donnees && p.ia && p.numerique_public && p.secteur_financier && p.plateforme && p.emballages && p.import_produits;

  async function envoyerLead() {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      setEnvoi("erreur");
      return;
    }
    setEnvoi("envoi");
    try {
      const r = await fetch("/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email.trim(),
          profil: p,
          normes: res ? res.directs.map((n) => n.nom) : [],
          source: "simulateur-conformite-2026",
        }),
      });
      const data = await r.json();
      setEnvoi(data.ok ? "ok" : "erreur");
    } catch {
      setEnvoi("erreur");
    }
  }

  function analyser() {
    if (!pret) return;
    const directs = NORMES.filter((n) => n.concerne(p) === "oui");
    const cascade = NORMES.filter((n) => n.concerne(p) === "cascade");
    setRes({ directs, cascade });
  }

  // Échéances concrètes connues (sinon : rappel personnel à 14 jours). Dates vérifiées (sources Caelum).
  const ECHEANCES_ISO: Record<string, string> = {
    csrd: "2027-01-01",
    csddd: "2029-07-26",
    "transparence-salariale": "2027-06-07",
    ppwr: "2026-08-12",
    cbam: "2027-05-31",
  };

  function genererICS() {
    if (!res) return;
    const normes = [...res.directs, ...res.cascade];
    if (normes.length === 0) return;
    const today = new Date();
    const fmt = (d: Date) =>
      `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, "0")}${String(d.getDate()).padStart(2, "0")}`;
    const stamp = fmt(today) + "T090000Z";
    const lignes: string[] = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Caelum//Conformite//FR", "CALSCALE:GREGORIAN"];
    normes.forEach((n, i) => {
      let dateStr = ECHEANCES_ISO[n.id];
      let titre = `Conformité : ${n.nom}`;
      if (!dateStr) {
        const r = new Date(today);
        r.setDate(r.getDate() + 14);
        dateStr = `${r.getFullYear()}-${String(r.getMonth() + 1).padStart(2, "0")}-${String(r.getDate()).padStart(2, "0")}`;
        titre = `Rappel conformité : ${n.nom}`;
      }
      const dt = dateStr.replace(/-/g, "");
      lignes.push(
        "BEGIN:VEVENT",
        `UID:caelum-${n.id}-${i}@caelum`,
        `DTSTAMP:${stamp}`,
        `DTSTART;VALUE=DATE:${dt}`,
        `SUMMARY:${titre}`,
        `DESCRIPTION:${(n.change || "").replace(/\n/g, " ").slice(0, 250)} — via Caelum`,
        "END:VEVENT",
      );
    });
    lignes.push("END:VCALENDAR");
    const blob = new Blob([lignes.join("\r\n")], { type: "text/calendar;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "echeances-conformite-caelum.ics";
    a.click();
    URL.revokeObjectURL(url);
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
        <p className="text-slate-500 text-center mt-2 mb-8">Quelques questions, et vous savez exactement où vous en êtes.</p>

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
          <Choix
            titre="5. Utilisez-vous de l'intelligence artificielle (outils, automatisation) ?"
            cle="ia"
            options={[{ id: "oui", label: "Oui" }, { id: "non", label: "Non / je ne sais pas" }]}
          />
          <Choix
            titre="6. Proposez-vous un site/service numérique au grand public (e-commerce, app) ?"
            cle="numerique_public"
            options={[{ id: "oui", label: "Oui" }, { id: "non", label: "Non" }]}
          />
          <Choix
            titre="7. Êtes-vous une entité du secteur financier (banque, assurance, investissement, paiement, crypto) ?"
            cle="secteur_financier"
            options={[{ id: "oui", label: "Oui" }, { id: "non", label: "Non" }]}
          />
          <Choix
            titre="8. Exploitez-vous une plateforme numérique mettant en relation des vendeurs/prestataires avec des clients ?"
            cle="plateforme"
            options={[{ id: "oui", label: "Oui" }, { id: "non", label: "Non" }]}
          />
          <Choix
            titre="9. Mettez-vous sur le marché des produits emballés ou des emballages ?"
            cle="emballages"
            options={[{ id: "oui", label: "Oui" }, { id: "non", label: "Non" }]}
          />
          <Choix
            titre="10. Importez-vous des marchandises carbone (acier, ciment, aluminium, engrais…) ou commercialisez-vous des produits à risque de déforestation (bois, cacao, café, soja…) ?"
            cle="import_produits"
            options={[{ id: "oui", label: "Oui" }, { id: "non", label: "Non / je ne sais pas" }]}
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
            {/* Score de conformité visuel */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 mb-6">
              <div className="flex items-center justify-between gap-4 flex-wrap">
                <div>
                  <p className="text-sm text-slate-500">Votre diagnostic de conformité</p>
                  <p className="text-2xl font-bold text-slate-900">
                    {res.directs.length} obligation{res.directs.length > 1 ? "s" : ""} directe{res.directs.length > 1 ? "s" : ""}
                    {res.cascade.length > 0 && <span className="text-slate-500 text-lg font-semibold"> · {res.cascade.length} en cascade</span>}
                  </p>
                  <p className="text-xs text-slate-400 mt-1">sur {NORMES.length} normes analysées</p>
                </div>
                <button
                  type="button"
                  onClick={genererICS}
                  className="rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-4 py-2.5 shadow-sm"
                >
                  📅 Ajouter mes échéances à mon agenda (.ics)
                </button>
              </div>
              {/* Barre : part des normes à traiter */}
              <div className="mt-4 h-2.5 w-full rounded-full bg-slate-200 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-indigo-500 to-rose-500"
                  style={{ width: `${Math.min(100, Math.round(((res.directs.length + res.cascade.length) / NORMES.length) * 100))}%` }}
                />
              </div>
              <p className="text-xs text-slate-500 mt-2">
                Caelum peut prendre en charge ces obligations pour vous — automatiquement quand c&apos;est possible.
              </p>
            </div>

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

            <div className="mt-8 rounded-2xl border border-slate-200 bg-slate-50 p-7">
              {envoi === "ok" ? (
                <p className="text-center text-emerald-700 font-semibold">
                  ✅ Merci ! Votre rapport personnalisé arrive. On vous recontacte pour la mise en conformité.
                </p>
              ) : (
                <>
                  <h3 className="text-lg font-bold text-slate-900">Recevoir mon rapport par e-mail</h3>
                  <p className="text-slate-600 text-sm mt-1">
                    Le détail des normes qui vous concernent + les premières actions. Sans engagement.
                  </p>
                  <div className="flex flex-col sm:flex-row gap-3 mt-4">
                    <label htmlFor="lead-email" className="sr-only">
                      Votre adresse e-mail
                    </label>
                    <input
                      id="lead-email"
                      type="email"
                      value={email}
                      onChange={(e) => {
                        setEmail(e.target.value);
                        if (envoi === "erreur") setEnvoi("idle");
                      }}
                      placeholder="vous@entreprise.be"
                      className="flex-1 rounded-xl border border-slate-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <button
                      type="button"
                      onClick={envoyerLead}
                      disabled={envoi === "envoi"}
                      className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white font-semibold px-6 py-3 rounded-xl transition-colors"
                    >
                      {envoi === "envoi" ? "Envoi…" : "Recevoir mon rapport"}
                    </button>
                  </div>
                  {envoi === "erreur" && (
                    <p className="text-sm text-red-600 mt-2">
                      Vérifiez votre adresse e-mail et réessayez.
                    </p>
                  )}
                  <p className="text-xs text-slate-400 mt-3">
                    Vos données servent uniquement à vous recontacter. Aucun partage à des tiers.
                  </p>
                </>
              )}
            </div>

            <div className="mt-6 rounded-2xl bg-indigo-600 text-white p-7 text-center">
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
