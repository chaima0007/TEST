"use client";

import { useEffect, useState, useCallback } from "react";

type ThreatLevel = "benign" | "suspicious" | "malicious" | "apt";

interface ThreatActor {
  actor_id: string;
  ip_addresses: string[];
  first_seen: number;
  last_seen: number;
  attack_count: number;
  threat_types: string[];
  targeted_endpoints: string[];
  threat_level: ThreatLevel;
  confidence: number;
  persistence_hours: number;
}

interface EndpointVulnerability {
  endpoint: string;
  attack_count: number;
  unique_attackers: number;
  threat_types: string[];
  risk_score: number;
  recommended_actions: string[];
}

interface Summary {
  total_events: number;
  total_actors: number;
  actor_level_counts: Record<ThreatLevel, number>;
  total_endpoints_targeted: number;
  avg_endpoint_risk_score: number;
  high_risk_endpoint_count: number;
  apt_count: number;
  malicious_count: number;
}

interface ApiData {
  actors: ThreatActor[];
  endpoints: EndpointVulnerability[];
  summary: Summary;
  last_updated: string;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

const LEVEL_LABEL: Record<ThreatLevel, string> = {
  apt: "APT", malicious: "Malveillant", suspicious: "Suspect", benign: "Bénin",
};

const LEVEL_COLOR: Record<ThreatLevel, string> = {
  apt: "text-red-300 bg-red-900/40 border-red-700/50",
  malicious: "text-orange-400 bg-orange-900/30 border-orange-700/40",
  suspicious: "text-amber-400 bg-amber-900/20 border-amber-700/30",
  benign: "text-slate-400 bg-slate-800 border-slate-700",
};

const LEVEL_DOT: Record<ThreatLevel, string> = {
  apt: "bg-red-400 animate-pulse",
  malicious: "bg-orange-400 animate-pulse",
  suspicious: "bg-amber-400",
  benign: "bg-slate-500",
};

function ThreatBadge({ level }: { level: ThreatLevel }) {
  return (
    <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-bold border ${LEVEL_COLOR[level]}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${LEVEL_DOT[level]}`} />
      {LEVEL_LABEL[level]}
    </span>
  );
}

function RiskBar({ score }: { score: number }) {
  const color = score >= 75 ? "bg-red-500" : score >= 50 ? "bg-orange-500" : score >= 25 ? "bg-amber-500" : "bg-emerald-500";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${score}%` }} />
      </div>
      <span className="text-xs text-slate-400 w-8 text-right">{Math.round(score)}</span>
    </div>
  );
}

function relTime(ts: number) {
  const diff = Date.now() / 1000 - ts;
  if (diff < 60) return "À l'instant";
  if (diff < 3600) return `Il y a ${Math.round(diff / 60)}min`;
  if (diff < 86400) return `Il y a ${Math.round(diff / 3600)}h`;
  return `Il y a ${Math.round(diff / 86400)}j`;
}

// ─── Actor Modal ──────────────────────────────────────────────────────────────

function ActorModal({ actor, onClose }: { actor: ThreatActor; onClose: () => void }) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/60" />
      <div
        className="relative bg-slate-900 border border-slate-700 rounded-xl w-full max-w-xl shadow-2xl overflow-y-auto max-h-[90vh]"
        onClick={e => e.stopPropagation()}
      >
        <div className="p-5 border-b border-slate-800 flex items-start justify-between gap-3">
          <div>
            <h2 className="text-white font-semibold font-mono">{actor.ip_addresses[0]}</h2>
            <p className="text-slate-400 text-sm mt-0.5">
              {actor.attack_count} attaque{actor.attack_count > 1 ? "s" : ""} · {actor.persistence_hours.toFixed(1)}h persistance
            </p>
          </div>
          <div className="flex items-center gap-2">
            <ThreatBadge level={actor.threat_level} />
            <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none p-1">×</button>
          </div>
        </div>

        <div className="p-5 space-y-4">
          {/* Timeline */}
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-500">Première activité</div>
              <div className="text-sm text-white font-medium mt-0.5">{relTime(actor.first_seen)}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-500">Dernière activité</div>
              <div className="text-sm text-white font-medium mt-0.5">{relTime(actor.last_seen)}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-500">Confiance niveau</div>
              <div className="text-sm text-indigo-400 font-bold mt-0.5">{Math.round(actor.confidence * 100)}%</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-500">Endpoints ciblés</div>
              <div className="text-sm text-white font-medium mt-0.5">{actor.targeted_endpoints.length}</div>
            </div>
          </div>

          {/* Threat types */}
          <div>
            <p className="text-xs font-semibold text-red-400 uppercase tracking-wide mb-2">Types d'attaques</p>
            <div className="flex flex-wrap gap-1.5">
              {actor.threat_types.map(t => (
                <span key={t} className="px-2 py-0.5 bg-red-900/30 border border-red-800/40 text-red-300 text-xs rounded font-mono">
                  {t}
                </span>
              ))}
            </div>
          </div>

          {/* Endpoints */}
          <div>
            <p className="text-xs font-semibold text-amber-400 uppercase tracking-wide mb-2">Endpoints ciblés</p>
            <div className="space-y-1">
              {actor.targeted_endpoints.map(ep => (
                <div key={ep} className="text-xs font-mono text-slate-300 bg-slate-800 rounded px-2 py-1">{ep}</div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── Endpoint Modal ───────────────────────────────────────────────────────────

function EndpointModal({ vuln, onClose }: { vuln: EndpointVulnerability; onClose: () => void }) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/60" />
      <div
        className="relative bg-slate-900 border border-slate-700 rounded-xl w-full max-w-xl shadow-2xl overflow-y-auto max-h-[90vh]"
        onClick={e => e.stopPropagation()}
      >
        <div className="p-5 border-b border-slate-800 flex items-start justify-between gap-3">
          <div>
            <h2 className="text-white font-semibold font-mono text-sm">{vuln.endpoint}</h2>
            <p className="text-slate-400 text-sm mt-0.5">{vuln.attack_count} attaque{vuln.attack_count > 1 ? "s" : ""} · {vuln.unique_attackers} IP distincte{vuln.unique_attackers > 1 ? "s" : ""}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none p-1">×</button>
        </div>

        <div className="p-5 space-y-4">
          {/* Risk score */}
          <div className="bg-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 mb-1">Score de risque</div>
            <div className={`text-3xl font-bold mb-2 ${vuln.risk_score >= 75 ? "text-red-400" : vuln.risk_score >= 50 ? "text-orange-400" : vuln.risk_score >= 25 ? "text-amber-400" : "text-emerald-400"}`}>
              {Math.round(vuln.risk_score)}/100
            </div>
            <RiskBar score={vuln.risk_score} />
          </div>

          {/* Threat types */}
          <div>
            <p className="text-xs font-semibold text-red-400 uppercase tracking-wide mb-2">Vecteurs d'attaque</p>
            <div className="flex flex-wrap gap-1.5">
              {vuln.threat_types.map(t => (
                <span key={t} className="px-2 py-0.5 bg-red-900/30 border border-red-800/40 text-red-300 text-xs rounded font-mono">
                  {t}
                </span>
              ))}
            </div>
          </div>

          {/* Hardening recommendations */}
          {vuln.recommended_actions.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-sky-400 uppercase tracking-wide mb-2">Recommandations de durcissement</p>
              <ul className="space-y-2">
                {vuln.recommended_actions.map((r, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300 bg-slate-800 rounded-lg p-2.5">
                    <span className="text-sky-400 mt-0.5 flex-shrink-0">→</span>{r}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Main page ────────────────────────────────────────────────────────────────

const LEVEL_FILTERS: { key: ThreatLevel | "all"; label: string }[] = [
  { key: "all", label: "Tous" },
  { key: "apt", label: "APT" },
  { key: "malicious", label: "Malveillants" },
  { key: "suspicious", label: "Suspects" },
  { key: "benign", label: "Bénins" },
];

type Tab = "actors" | "endpoints";

export default function ThreatIntelPage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<Tab>("actors");
  const [levelFilter, setLevelFilter] = useState<ThreatLevel | "all">("all");
  const [selectedActor, setSelectedActor] = useState<ThreatActor | null>(null);
  const [selectedEndpoint, setSelectedEndpoint] = useState<EndpointVulnerability | null>(null);

  const load = useCallback(async () => {
    try {
      const res = await fetch("/api/threat-intel", { cache: "no-store" });
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const filteredActors = data?.actors.filter(a => levelFilter === "all" || a.threat_level === levelFilter) ?? [];

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const summary = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 py-8 space-y-6">

        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Intelligence des Menaces</h1>
            <p className="text-slate-400 text-sm mt-1">
              Profilage des acteurs malveillants et analyse de vulnérabilité des endpoints
            </p>
          </div>
          {data && (
            <span className="text-xs text-slate-500">
              Mis à jour {new Date(data.last_updated).toLocaleTimeString("fr-FR")}
            </span>
          )}
        </div>

        {/* KPIs */}
        {summary && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Acteurs détectés", value: `${summary.total_actors}`, sub: `${summary.total_events} événements`, color: "text-white" },
              { label: "APT identifiés", value: `${summary.apt_count}`, sub: `${summary.malicious_count} malveillants`, color: "text-red-400" },
              { label: "Endpoints à risque", value: `${summary.high_risk_endpoint_count}`, sub: `sur ${summary.total_endpoints_targeted} ciblés`, color: "text-orange-400" },
              { label: "Risque moyen EP", value: `${summary.avg_endpoint_risk_score.toFixed(0)}/100`, sub: "score de vulnérabilité", color: "text-amber-400" },
            ].map(k => (
              <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p className="text-xs text-slate-500 font-medium uppercase tracking-wide">{k.label}</p>
                <p className={`text-2xl font-bold mt-1 ${k.color}`}>{k.value}</p>
                <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
              </div>
            ))}
          </div>
        )}

        {/* APT alert banner */}
        {summary && summary.apt_count > 0 && (
          <div className="bg-red-950/40 border border-red-700/50 rounded-xl p-4 flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-red-400 animate-pulse flex-shrink-0" />
            <div>
              <p className="text-red-300 text-sm font-semibold">
                {summary.apt_count} acteur{summary.apt_count > 1 ? "s" : ""} APT détecté{summary.apt_count > 1 ? "s" : ""}
              </p>
              <p className="text-red-400/70 text-xs mt-0.5">
                Menace persistante avancée — investigation immédiate recommandée
              </p>
            </div>
          </div>
        )}

        {/* Tab selector */}
        <div className="flex gap-2 border-b border-slate-800 pb-0">
          {([["actors", "Acteurs"], ["endpoints", "Endpoints vulnérables"]] as [Tab, string][]).map(([key, label]) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={`px-4 py-2 text-sm font-medium transition-colors border-b-2 -mb-px ${
                tab === key ? "border-indigo-500 text-white" : "border-transparent text-slate-400 hover:text-white"
              }`}
            >
              {label}
              {key === "actors" && data && <span className="ml-1.5 text-xs opacity-60">({data.actors.length})</span>}
              {key === "endpoints" && data && <span className="ml-1.5 text-xs opacity-60">({data.endpoints.length})</span>}
            </button>
          ))}
        </div>

        {tab === "actors" && (
          <div className="space-y-4">
            {/* Level filters */}
            <div className="flex gap-1.5 flex-wrap">
              {LEVEL_FILTERS.map(f => (
                <button
                  key={f.key}
                  onClick={() => setLevelFilter(f.key as ThreatLevel | "all")}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                    levelFilter === f.key ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
                  }`}
                >
                  {f.label}
                  {f.key !== "all" && summary && (
                    <span className="ml-1 opacity-60">({summary.actor_level_counts[f.key]})</span>
                  )}
                </button>
              ))}
            </div>

            {/* Actor cards */}
            <div className="space-y-2">
              {filteredActors.length === 0 && (
                <p className="text-slate-500 text-sm text-center py-8">Aucun acteur pour ce niveau</p>
              )}
              {filteredActors.map(actor => (
                <div
                  key={actor.actor_id}
                  onClick={() => setSelectedActor(actor)}
                  className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-colors"
                >
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div className="flex items-center gap-3">
                      <ThreatBadge level={actor.threat_level} />
                      <code className="text-white text-sm font-mono">{actor.ip_addresses[0]}</code>
                    </div>
                    <div className="text-right flex-shrink-0">
                      <div className="text-indigo-400 font-bold">{Math.round(actor.confidence * 100)}%</div>
                      <div className="text-xs text-slate-500">confiance</div>
                    </div>
                  </div>

                  <div className="grid grid-cols-4 gap-2 text-center mb-3">
                    {[
                      { label: "Attaques", value: actor.attack_count },
                      { label: "Types", value: actor.threat_types.length },
                      { label: "Endpoints", value: actor.targeted_endpoints.length },
                      { label: "Persistance", value: `${actor.persistence_hours.toFixed(0)}h` },
                    ].map(({ label, value }) => (
                      <div key={label} className="bg-slate-800 rounded-lg p-2">
                        <div className="text-sm font-bold text-white">{value}</div>
                        <div className="text-[10px] text-slate-500">{label}</div>
                      </div>
                    ))}
                  </div>

                  <div className="flex gap-1.5 flex-wrap">
                    {actor.threat_types.slice(0, 4).map(t => (
                      <span key={t} className="text-[10px] font-mono px-1.5 py-0.5 bg-slate-800 text-slate-400 rounded">{t}</span>
                    ))}
                    {actor.threat_types.length > 4 && (
                      <span className="text-[10px] text-slate-500">+{actor.threat_types.length - 4}</span>
                    )}
                  </div>

                  <div className="flex justify-between mt-2">
                    <span className="text-[10px] text-slate-500">Dernière activité: {relTime(actor.last_seen)}</span>
                    <span className="text-[10px] text-slate-600">→ Voir détails</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {tab === "endpoints" && (
          <div className="space-y-2">
            {(data?.endpoints ?? []).map(vuln => (
              <div
                key={vuln.endpoint}
                onClick={() => setSelectedEndpoint(vuln)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-colors"
              >
                <div className="flex items-start justify-between gap-3 mb-3">
                  <code className="text-white text-sm font-mono">{vuln.endpoint}</code>
                  <div className="text-right flex-shrink-0">
                    <div className={`text-lg font-bold ${vuln.risk_score >= 75 ? "text-red-400" : vuln.risk_score >= 50 ? "text-orange-400" : vuln.risk_score >= 25 ? "text-amber-400" : "text-emerald-400"}`}>
                      {Math.round(vuln.risk_score)}
                    </div>
                    <div className="text-[10px] text-slate-500">risque</div>
                  </div>
                </div>
                <RiskBar score={vuln.risk_score} />
                <div className="flex items-center gap-4 mt-2 text-xs text-slate-500">
                  <span>{vuln.attack_count} attaque{vuln.attack_count > 1 ? "s" : ""}</span>
                  <span>{vuln.unique_attackers} attaquant{vuln.unique_attackers > 1 ? "s" : ""}</span>
                  <span>{vuln.recommended_actions.length} recommandation{vuln.recommended_actions.length > 1 ? "s" : ""}</span>
                </div>
                <div className="flex gap-1.5 flex-wrap mt-2">
                  {vuln.threat_types.map(t => (
                    <span key={t} className="text-[10px] font-mono px-1.5 py-0.5 bg-slate-800 text-slate-400 rounded">{t}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedActor && <ActorModal actor={selectedActor} onClose={() => setSelectedActor(null)} />}
      {selectedEndpoint && <EndpointModal vuln={selectedEndpoint} onClose={() => setSelectedEndpoint(null)} />}
    </div>
  );
}
