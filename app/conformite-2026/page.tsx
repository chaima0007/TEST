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

// Actions clés de conformité par norme — pour le formulaire « Suis-je déjà en règle ? ».
const CHECKS: Record<string, string[]> = {
  efacture: ["J'émets ET je reçois mes factures B2B en format électronique structuré (Peppol)"],
  rgpd: ["Je tiens un registre des traitements", "J'informe les personnes et gère les demandes (accès, effacement) et les incidents"],
  lanceurs: ["J'ai un canal de signalement interne sécurisé", "Je protège les lanceurs d'alerte contre les représailles"],
  nis2: ["J'ai des mesures de cybersécurité (MFA, sauvegardes, gestion des accès)", "Je sais notifier un incident au CCB", "La gouvernance cyber est suivie par la direction"],
  csrd: ["Je prépare un rapport de durabilité (normes ESRS)"],
  csddd: ["J'ai un devoir de vigilance sur ma chaîne de valeur"],
  ubo: ["Mes bénéficiaires effectifs sont déclarés au registre UBO", "Je confirme les données chaque année"],
  "ai-act": ["J'ai inventorié mes systèmes d'IA et leur niveau de risque"],
  eaa: ["Mon site/app respecte l'accessibilité (WCAG) + déclaration d'accessibilité"],
  dora: ["J'ai un cadre de gestion du risque informatique (TIC) + tests + notification d'incidents"],
  "transparence-salariale": ["J'indique une fourchette de rémunération dès l'offre d'emploi", "Je peux justifier mes écarts de rémunération F/H"],
  dac7: ["Je collecte et déclare les données des vendeurs au SPF Finances"],
  ppwr: ["Mes emballages respectent recyclabilité/étiquetage + documentation de conformité"],
  "delais-paiement": ["Mes CGV et contrats prévoient des délais de paiement ≤ 60 jours"],
  cbam: ["J'ai le statut de déclarant MACF + un suivi des émissions importées"],
  eudr: ["J'ai un système de diligence raisonnée (traçabilité) + déclaration"],
  aml: ["J'applique la vigilance client (KYC) + déclaration des opérations suspectes (CTIF)"],
};

export default function Conformite2026Page() {
  const [p, setP] = useState<Profil>({ tva: "", taille: "", secteur: "", donnees: "", ia: "", numerique_public: "", secteur_financier: "", plateforme: "", emballages: "", import_produits: "" });
  const [res, setRes] = useState<{ directs: Norme[]; cascade: Norme[] } | null>(null);
  const [coches, setCoches] = useState<Record<string, boolean>>({});
  const [raisonSociale, setRaisonSociale] = useState("");
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

  // Attestation / registre d'auto-évaluation — déclaration sur l'honneur, horodatée.
  // Honnêteté : ce n'est PAS une certification officielle (mention explicite sur le document).
  // Pas de dépendance : on ouvre une fenêtre imprimable → l'utilisateur « Enregistre en PDF ».
  function genererAttestation() {
    if (!res || res.directs.length === 0) return;
    const esc = (s: string) =>
      s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    const d = new Date();
    const dateFr = d.toLocaleDateString("fr-BE", { day: "2-digit", month: "long", year: "numeric" });
    const ref = "CAELUM-" + d.getFullYear() + String(d.getMonth() + 1).padStart(2, "0") + String(d.getDate()).padStart(2, "0") + "-" + String(d.getHours()).padStart(2, "0") + String(d.getMinutes()).padStart(2, "0");

    let totalAll = 0;
    let faitsAll = 0;
    const lignes = res.directs
      .map((n) => {
        const checks = CHECKS[n.id] || [];
        if (checks.length === 0) {
          return `<tr><td>${esc(n.nom)}</td><td>${esc(n.echeance)}</td><td class="na">—</td></tr>`;
        }
        const faits = checks.filter((_, i) => coches[`${n.id}:${i}`]).length;
        totalAll += checks.length;
        faitsAll += faits;
        const pctN = Math.round((faits / checks.length) * 100);
        const cls = pctN >= 80 ? "ok" : pctN >= 40 ? "mid" : "low";
        const detail = checks
          .map((c, i) => `<li class="${coches[`${n.id}:${i}`] ? "done" : "todo"}">${coches[`${n.id}:${i}`] ? "☑" : "☐"} ${esc(c)}</li>`)
          .join("");
        return `<tr><td>${esc(n.nom)}<ul class="detail">${detail}</ul></td><td>${esc(n.echeance)}</td><td class="${cls}">${pctN}%</td></tr>`;
      })
      .join("");
    const pctGlobal = totalAll ? Math.round((faitsAll / totalAll) * 100) : 0;
    const titre = raisonSociale.trim()
      ? `Auto-évaluation de conformité — ${esc(raisonSociale.trim())}`
      : "Auto-évaluation de conformité réglementaire";

    const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>${titre}</title>
<style>
  * { box-sizing: border-box; }
  body { font-family: -apple-system, "Segoe UI", Roboto, sans-serif; color: #1e293b; max-width: 760px; margin: 0 auto; padding: 40px 32px; line-height: 1.5; }
  .head { display: flex; align-items: center; gap: 10px; border-bottom: 2px solid #4f46e5; padding-bottom: 14px; }
  .logo { width: 34px; height: 34px; border-radius: 8px; background: linear-gradient(135deg,#6366f1,#4338ca); color:#fff; font-weight:800; display:flex; align-items:center; justify-content:center; }
  h1 { font-size: 20px; margin: 22px 0 4px; }
  .meta { color: #64748b; font-size: 12px; }
  .score { margin: 20px 0; padding: 16px; border: 1px solid #e2e8f0; border-radius: 12px; background:#f8fafc; }
  .big { font-size: 34px; font-weight: 800; }
  .ok { color: #059669; } .mid { color: #d97706; } .low { color: #e11d48; } .na { color:#94a3b8; }
  table { width: 100%; border-collapse: collapse; margin-top: 14px; font-size: 13px; }
  th, td { text-align: left; padding: 9px 10px; border-bottom: 1px solid #e2e8f0; vertical-align: top; }
  th { background:#f1f5f9; font-size: 11px; text-transform: uppercase; letter-spacing: .04em; color:#475569; }
  td:last-child, th:last-child { text-align: right; white-space: nowrap; font-weight: 700; }
  ul.detail { margin: 6px 0 0; padding-left: 0; list-style: none; font-size: 12px; color:#475569; }
  ul.detail li { margin: 2px 0; }
  li.done { color:#059669; } li.todo { color:#64748b; }
  .disclaimer { margin-top: 24px; padding: 12px 14px; border-left: 3px solid #f59e0b; background:#fffbeb; font-size: 12px; color:#92400e; border-radius: 0 8px 8px 0; }
  .foot { margin-top: 22px; font-size: 11px; color:#94a3b8; border-top: 1px solid #e2e8f0; padding-top: 12px; }
  @media print { body { padding: 0; } .noprint { display: none; } }
  .btn { display:inline-block; margin-top:18px; padding:10px 18px; background:#4f46e5; color:#fff; border:none; border-radius:8px; font-weight:600; cursor:pointer; font-size:14px; }
</style></head><body>
  <div class="head"><div class="logo">C</div><strong style="font-size:18px">Caelum</strong></div>
  <h1>${titre}</h1>
  <p class="meta">Référence ${ref} · Établie le ${dateFr} · Basée sur l'auto-déclaration du répondant</p>

  <div class="score">
    <div style="color:#64748b;font-size:13px">Niveau de conformité auto-déclaré</div>
    <div class="big ${pctGlobal >= 80 ? "ok" : pctGlobal >= 40 ? "mid" : "low"}">${pctGlobal}%</div>
    <div style="color:#64748b;font-size:12px">${faitsAll}/${totalAll} actions de conformité déclarées réalisées</div>
  </div>

  <table>
    <thead><tr><th>Norme applicable</th><th>Échéance</th><th>État</th></tr></thead>
    <tbody>${lignes}</tbody>
  </table>

  <div class="disclaimer">
    <strong>Nature du document.</strong> Cette attestation est une <strong>auto-évaluation déclarative</strong> établie
    par le répondant à partir de ses propres réponses. Elle ne constitue ni une certification officielle, ni un
    audit indépendant, ni un conseil juridique. Elle reflète une situation déclarée à la date indiquée et peut évoluer.
    Pour une validation formelle, faites appel à un professionnel (juriste, expert-comptable, auditeur agréé).
  </div>

  <div class="foot">Document généré via le simulateur de conformité Caelum — caelum. Conserver dans votre registre de conformité interne.</div>

  <button class="btn noprint" onclick="window.print()">Imprimer / Enregistrer en PDF</button>
</body></html>`;

    const w = window.open("", "_blank");
    if (!w) return;
    w.document.write(html);
    w.document.close();
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

            {/* 2e étape : Suis-je déjà EN RÈGLE ? (checklist) */}
            {res.directs.length > 0 && (() => {
              const items = res.directs.flatMap((n) => (CHECKS[n.id] || []).map((c, i) => ({ key: `${n.id}:${i}`, norme: n.nom, texte: c })));
              const total = items.length;
              const faits = items.filter((it) => coches[it.key]).length;
              const pct = total ? Math.round((faits / total) * 100) : 0;
              const manques = items.filter((it) => !coches[it.key]);
              // Classes Tailwind complètes (le JIT ne génère pas les noms dynamiques `bg-${x}-500`).
              const txtScore = pct >= 80 ? "text-emerald-600" : pct >= 40 ? "text-amber-600" : "text-rose-600";
              const barScore = pct >= 80 ? "bg-emerald-500" : pct >= 40 ? "bg-amber-500" : "bg-rose-500";
              return (
                <div className="mt-10 rounded-2xl border border-slate-200 p-6 bg-white">
                  <h3 className="text-xl font-bold">Êtes-vous déjà en règle ?</h3>
                  <p className="text-slate-600 text-sm mt-1">Cochez ce qui est déjà fait. Votre score se met à jour en direct.</p>

                  <div className="mt-5 space-y-4">
                    {res.directs.map((n) => (
                      (CHECKS[n.id] || []).length > 0 && (
                        <div key={n.id}>
                          <p className="font-semibold text-sm text-slate-800">{n.nom}</p>
                          <div className="mt-1.5 space-y-1.5">
                            {(CHECKS[n.id] || []).map((c, i) => {
                              const key = `${n.id}:${i}`;
                              return (
                                <label key={key} className="flex items-start gap-2.5 text-sm text-slate-700 cursor-pointer">
                                  <input
                                    type="checkbox"
                                    checked={!!coches[key]}
                                    onChange={(e) => setCoches({ ...coches, [key]: e.target.checked })}
                                    className="mt-0.5 h-4 w-4 rounded border-slate-300 text-indigo-600"
                                  />
                                  <span>{c}</span>
                                </label>
                              );
                            })}
                          </div>
                        </div>
                      )
                    ))}
                  </div>

                  {/* Score en règle */}
                  <div className="mt-6 rounded-xl bg-slate-50 border border-slate-200 p-4">
                    <p className="text-sm text-slate-500">Vous êtes en règle à</p>
                    <p className={`text-3xl font-bold ${txtScore}`}>{pct}%</p>
                    <div className="mt-2 h-2.5 w-full rounded-full bg-slate-200 overflow-hidden">
                      <div className={`h-full ${barScore}`} style={{ width: `${pct}%` }} />
                    </div>
                    {manques.length > 0 ? (
                      <div className="mt-3">
                        <p className="text-sm font-semibold text-slate-800">Ce qu&apos;il reste à faire ({manques.length}) :</p>
                        <ul className="mt-1 list-disc list-inside text-sm text-slate-600 space-y-0.5">
                          {manques.slice(0, 8).map((m) => <li key={m.key}>{m.texte}</li>)}
                        </ul>
                        <p className="mt-3 text-sm font-medium text-indigo-700">👉 Caelum peut combler ces écarts pour vous.</p>
                      </div>
                    ) : (
                      <p className="mt-3 text-sm font-medium text-emerald-700">🎉 Bravo : sur ces points, vous semblez en règle ! Une veille reste utile pour le rester.</p>
                    )}
                  </div>

                  {/* Attestation / registre de conformité (déclaration sur l'honneur, horodatée) */}
                  <div className="mt-5 rounded-xl border border-indigo-200 bg-indigo-50/60 p-4">
                    <p className="text-sm font-semibold text-slate-800">📄 Attestation d&apos;auto-évaluation</p>
                    <p className="text-xs text-slate-600 mt-1">
                      Générez un document horodaté à conserver dans votre registre de conformité interne (PDF via
                      l&apos;impression). C&apos;est une auto-déclaration, pas une certification officielle.
                    </p>
                    <input
                      type="text"
                      value={raisonSociale}
                      onChange={(e) => setRaisonSociale(e.target.value)}
                      placeholder="Raison sociale (facultatif)"
                      maxLength={120}
                      className="mt-3 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
                    />
                    <button
                      type="button"
                      onClick={genererAttestation}
                      className="mt-3 inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
                    >
                      📄 Générer l&apos;attestation
                    </button>
                  </div>
                </div>
              );
            })()}

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
