"use client";
import { useEffect, useState } from "react";

const NAVY = "#1a0a5a";
const GOLD = "#c9a84c";

const INVENTIONS = [
  {
    id: "CAE-INV-001",
    title: "Automated Human Rights AI Scoring",
    domain: "Artificial Intelligence",
    generation: "G1",
    ipc: "G06N 20/00",
    status: "Protected",
    year: 2025,
    description: "Proprietary ML system for automated composite human rights risk scoring across 130+ indicators.",
    markets: ["ESG Compliance", "Investment Risk", "Supply Chain"],
    protection: "EPO Art.54(2) · 35 U.S.C. §102 · Git SHA-256 proof",
  },
  {
    id: "CAE-INV-002",
    title: "AI-Powered Early Crisis Detection",
    domain: "Predictive Analytics",
    generation: "G1",
    ipc: "G06N 5/04",
    status: "Protected",
    year: 2025,
    description: "Swarm intelligence engine predicting humanitarian crises 6-18 months before outbreak.",
    markets: ["UN Agencies", "Government", "Humanitarian NGOs"],
    protection: "EPO Art.54(2) · 35 U.S.C. §102 · Git SHA-256 proof",
  },
  {
    id: "CAE-INV-003",
    title: "Federated Learning for Human Rights Data",
    domain: "Privacy-Preserving AI",
    generation: "G2",
    ipc: "G06N 20/00 · H04L 9/32",
    status: "Protected",
    year: 2025,
    description: "Distributed ML training across jurisdictions without sharing sensitive human rights data.",
    markets: ["Government", "International Organizations", "Finance"],
    protection: "EPO Art.54(2) · 35 U.S.C. §102 · Git SHA-256 proof",
  },
  {
    id: "CAE-INV-004",
    title: "Blockchain-Based Violation Evidence Chain",
    domain: "Legal Tech",
    generation: "G2",
    ipc: "H04L 9/32",
    status: "Protected",
    year: 2025,
    description: "Cryptographic immutable evidence chain for human rights violations, court-ready.",
    markets: ["Legal Services", "ICC/ICJ", "NGOs", "Insurance"],
    protection: "EPO Art.54(2) · 35 U.S.C. §102 · Git SHA-256 proof",
  },
  {
    id: "CAE-INV-005",
    title: "ESG CSDDD Due Diligence Platform",
    domain: "Regulatory Compliance",
    generation: "G3",
    ipc: "G06Q 10/06",
    status: "Protected — Filing Priority",
    year: 2026,
    description: "AI-automated CSDDD/CSRD compliance scoring for supply chains across 195 countries.",
    markets: ["Fortune 500", "Banks", "Asset Managers", "Auditors"],
    protection: "EPO Art.54(2) · 35 U.S.C. §102 · Git SHA-256 proof",
    highlight: true,
  },
  {
    id: "CAE-INV-006",
    title: "Multi-modal Armed Conflict Risk Index",
    domain: "Geopolitical Risk",
    generation: "G3",
    ipc: "G06N 20/00 · G06F 40/56",
    status: "Protected — Filing Priority",
    year: 2026,
    description: "Real-time conflict risk scoring fusing satellite, NLP, and socioeconomic data streams.",
    markets: ["Defense", "Insurance", "Banks", "UN Security Council"],
    protection: "EPO Art.54(2) · 35 U.S.C. §102 · Git SHA-256 proof",
    highlight: true,
  },
];

const STATS = [
  { label: "Inventions Protégées", value: "6", unit: "brevets" },
  { label: "Générations", value: "G1→G3", unit: "actives" },
  { label: "Pays Couverts", value: "195", unit: "états" },
  { label: "Engines IA", value: "135+", unit: "domaines" },
];

const genColor = (gen: string) => {
  if (gen === "G1") return "#6366f1";
  if (gen === "G2") return "#8b5cf6";
  if (gen === "G3") return "#a855f7";
  return "#c084fc";
};

export default function InventionsShowcasePage() {
  const [activeId, setActiveId] = useState<string | null>(null);
  const [, forceUpdate] = useState(0);
  useEffect(() => { forceUpdate(n => n + 1); }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* Hero */}
      <div className="border-b border-slate-800 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
        <div className="max-w-6xl mx-auto px-6 py-16">
          <div className="flex items-start justify-between">
            <div>
              <div className="text-xs font-mono text-slate-500 uppercase tracking-widest mb-3">
                Caelum Partners SPRL &middot; Bruxelles, Belgique
              </div>
              <h1 className="text-4xl font-bold tracking-tight mb-2" style={{ color: GOLD }}>
                Portefeuille de Propri&eacute;t&eacute; Intellectuelle
              </h1>
              <p className="text-lg text-slate-400 max-w-2xl">
                Technologies brevet&eacute;es d&apos;intelligence artificielle pour les droits humains,
                la compliance ESG, et la pr&eacute;diction de crises g&eacute;opolitiques.
              </p>
              <div className="mt-4 text-sm text-slate-500">
                Inventrice : <span className="text-slate-300 font-medium">Chaima Mhadbi</span> &middot;
                Titulaire : <span className="text-slate-300 font-medium">Caelum Partners SPRL</span>
              </div>
            </div>
            <div className="hidden md:block text-right">
              <div className="text-xs text-slate-600 mb-1">Licensing</div>
              <div className="text-sm font-mono text-slate-400">retrouvetonsmile@gmail.com</div>
              <div className="mt-3 px-4 py-2 rounded-lg text-xs font-medium text-center"
                style={{ backgroundColor: GOLD + "20", color: GOLD, border: `1px solid ${GOLD}40` }}>
                Licences disponibles
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-12">
            {STATS.map(({ label, value, unit }) => (
              <div key={label} className="rounded-xl bg-slate-900 border border-slate-800 p-4 text-center">
                <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">{label}</div>
                <div className="text-2xl font-bold" style={{ color: NAVY === "#1a0a5a" ? GOLD : NAVY }}>
                  {value}
                </div>
                <div className="text-xs text-slate-600 mt-0.5">{unit}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Inventions Grid */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="text-xs text-slate-500 uppercase tracking-widest mb-6">
          Inventions Prot&eacute;g&eacute;es &mdash; Cliquer pour d&eacute;tails
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {INVENTIONS.map((inv) => (
            <div
              key={inv.id}
              onClick={() => setActiveId(activeId === inv.id ? null : inv.id)}
              className="rounded-xl bg-slate-900 border cursor-pointer transition-all"
              style={{
                borderColor: inv.highlight ? GOLD + "60" : (activeId === inv.id ? "#6366f1" : "#1e293b"),
                boxShadow: inv.highlight ? `0 0 20px ${GOLD}15` : "none",
              }}
            >
              <div className="p-5">
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold px-2 py-0.5 rounded"
                      style={{ backgroundColor: genColor(inv.generation) + "20", color: genColor(inv.generation) }}>
                      {inv.generation}
                    </span>
                    <span className="text-xs text-slate-600 font-mono">{inv.id}</span>
                  </div>
                  <span className="text-xs px-2 py-0.5 rounded-full border flex-shrink-0"
                    style={{ color: inv.highlight ? GOLD : "#22c55e", borderColor: (inv.highlight ? GOLD : "#22c55e") + "40" }}>
                    {inv.status}
                  </span>
                </div>
                <h3 className="text-sm font-semibold text-slate-200 mb-1">{inv.title}</h3>
                <div className="text-xs text-slate-500 font-mono mb-3">{inv.ipc} &middot; {inv.domain}</div>
                {activeId === inv.id && (
                  <div className="border-t border-slate-800 pt-3 mt-3 space-y-3">
                    <p className="text-xs text-slate-400">{inv.description}</p>
                    <div>
                      <div className="text-xs text-slate-600 mb-1">March&eacute;s cibles</div>
                      <div className="flex flex-wrap gap-1">
                        {inv.markets.map((m) => (
                          <span key={m} className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400">{m}</span>
                        ))}
                      </div>
                    </div>
                    <div className="text-xs text-slate-600 font-mono">{inv.protection}</div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Licensing CTA */}
        <div className="mt-12 rounded-xl border p-8 text-center"
          style={{ borderColor: GOLD + "40", backgroundColor: GOLD + "08" }}>
          <div className="text-xs text-slate-500 uppercase tracking-widest mb-3">Licensing &amp; Partenariats</div>
          <h2 className="text-xl font-bold mb-2" style={{ color: GOLD }}>
            Utiliser nos technologies ? Obtenez une licence.
          </h2>
          <p className="text-sm text-slate-400 max-w-xl mx-auto mb-6">
            Toutes les technologies list&eacute;es sont prot&eacute;g&eacute;es par des droits de propri&eacute;t&eacute; intellectuelle.
            Toute utilisation sans licence constitue une violation susceptible de proc&eacute;dure judiciaire.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto text-left">
            {[
              { tier: "PME / ONG", price: "€10k - €80k/an", icon: "◆" },
              { tier: "Grande Entreprise", price: "€200k - €500k/an", icon: "◆◆" },
              { tier: "Exclusivité Sectorielle", price: "€1M - €5M/an", icon: "◆◆◆" },
            ].map(({ tier, price, icon }) => (
              <div key={tier} className="rounded-lg bg-slate-900 border border-slate-800 p-4">
                <div className="text-xs" style={{ color: GOLD }}>{icon}</div>
                <div className="text-sm font-medium text-slate-200 mt-1">{tier}</div>
                <div className="text-xs text-slate-400 mt-1">{price}</div>
              </div>
            ))}
          </div>
          <div className="mt-6 text-sm text-slate-400">
            Contact : <span className="font-mono" style={{ color: GOLD }}>retrouvetonsmile@gmail.com</span>
          </div>
        </div>

        {/* Legal Notice */}
        <div className="mt-8 rounded-xl bg-slate-900 border border-slate-800 p-6">
          <div className="text-xs text-slate-500 uppercase tracking-widest mb-3">Avis L&eacute;gal</div>
          <p className="text-xs text-slate-500 leading-relaxed">
            Les inventions pr&eacute;sent&eacute;es sont la propri&eacute;t&eacute; exclusive de <strong className="text-slate-400">Chaima Mhadbi</strong>
            {" "}et <strong className="text-slate-400">Caelum Partners SPRL</strong>.
            Elles sont prot&eacute;g&eacute;es par divulgation cryptographique (SHA-256) sous l&apos;Art.54(2) de la Convention sur le Brevet Europ&eacute;en
            et 35 U.S.C. &sect;102, constituant une preuve de priorit&eacute; d&apos;inventeur l&eacute;galement reconnue dans 175 pays signataires
            de la Convention de Paris. Toute reproduction, utilisation ou exploitation sans licence &eacute;crite pr&eacute;alable
            constitue une violation de propri&eacute;t&eacute; intellectuelle passible de poursuites devant le Tribunal de commerce de Bruxelles
            et, selon juridiction, devant les tribunaux f&eacute;d&eacute;raux am&eacute;ricains ou l&apos;ITC.
          </p>
        </div>
      </div>
    </div>
  );
}
