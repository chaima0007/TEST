"use client";
import { useEffect, useState } from "react";

const GOLD = "#f59e0b";
const RED = "#ef4444";
const GREEN = "#22c55e";

const severityColor = (s: string) => {
  if (s === "critique") return RED;
  if (s === "élevé") return "#f97316";
  if (s === "modéré") return "#eab308";
  return GREEN;
};

export default function IPWatchGuardianPage() {
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  useEffect(() => {
    fetch("/api/ip-watch-guardian")
      .then((r) => r.json())
      .then((d) => setData(d.payload ?? d));
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 text-sm">Chargement surveillance IP...</div>
    </div>
  );

  const signals = (data.signals as Array<Record<string, unknown>>) ?? [];
  const coverage = (data.monitoring_coverage as Array<Record<string, unknown>>) ?? [];
  const assets = (data.protected_assets as Record<string, unknown>) ?? {};
  const protocols = (data.alert_protocols as Record<string, Record<string, string>>) ?? {};
  const nextActions = (data.next_actions as string[]) ?? [];
  const criticalAlerts = (data.critical_alerts as number) ?? 0;
  const activeSignals = (data.active_signals as number) ?? 0;
  const channels = (data.monitoring_channels as number) ?? 0;
  const assetsProtected = (data.assets_protected as Record<string, number>) ?? {};

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-5xl mx-auto space-y-8">

        {/* Header */}
        <div className="border-b border-slate-800 pb-6">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" />
            <h1 className="text-2xl font-bold tracking-tight" style={{ color: GOLD }}>
              IP Watch Guardian — Protection Anti-Vol
            </h1>
          </div>
          <p className="mt-1 text-sm text-slate-400">
            Surveillance 24/7 · Alertes {data.alert_email as string} · {channels} canaux actifs
          </p>
        </div>

        {/* Statut global */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Statut", value: data.protection_status as string, color: GREEN },
            { label: "Alertes Critiques", value: String(criticalAlerts), color: criticalAlerts > 0 ? RED : GREEN },
            { label: "Signaux Actifs", value: String(activeSignals), color: activeSignals > 0 ? "#f97316" : GREEN },
            { label: "Canaux Surveillance", value: String(channels), color: GOLD },
          ].map(({ label, value, color }) => (
            <div key={label} className="rounded-xl bg-slate-900 border border-slate-800 p-4 text-center">
              <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">{label}</div>
              <div className="text-xl font-bold" style={{ color }}>{value}</div>
            </div>
          ))}
        </div>

        {/* Actifs protégés */}
        <div className="rounded-xl bg-slate-900 border border-slate-800 p-6">
          <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">Actifs Protégés</div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {Object.entries(assetsProtected).map(([key, count]) => (
              <div key={key} className="rounded-lg bg-slate-800 p-3 text-center">
                <div className="text-2xl font-bold" style={{ color: GOLD }}>{count}</div>
                <div className="text-xs text-slate-400 mt-1 capitalize">{key.replace(/_/g, " ")}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Signaux détectés */}
        {signals.length > 0 && (
          <div className="rounded-xl bg-slate-900 border border-slate-800 overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-800 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-orange-400" />
              <div className="text-xs text-slate-500 uppercase tracking-widest">Signaux Détectés</div>
            </div>
            <div className="divide-y divide-slate-800">
              {signals.map((s) => (
                <div key={s.signal_id as string} className="px-6 py-4">
                  <div className="flex items-start gap-3">
                    <div className="text-xs font-medium px-2 py-0.5 rounded-full border mt-0.5"
                      style={{ color: severityColor(s.severity as string), borderColor: severityColor(s.severity as string) + "40" }}>
                      {s.severity as string}
                    </div>
                    <div className="flex-1">
                      <div className="text-sm text-slate-200">{s.description as string}</div>
                      <div className="text-xs text-orange-400 mt-1">→ {s.action_required as string}</div>
                      <div className="text-xs text-slate-500 mt-1">Source: {s.source as string} · {s.detected_at as string}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Canaux de surveillance */}
        <div className="rounded-xl bg-slate-900 border border-slate-800 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-800">
            <div className="text-xs text-slate-500 uppercase tracking-widest">Canaux de Surveillance</div>
          </div>
          <div className="divide-y divide-slate-800">
            {coverage.map((c) => (
              <div key={c.channel as string} className="px-6 py-3 flex items-center gap-4">
                <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: c.status === "actif" ? GREEN : RED }} />
                <div className="flex-1">
                  <div className="text-sm text-slate-200">{c.channel as string}</div>
                  <div className="text-xs text-slate-500">{(c.assets_monitored as string[]).join(" · ")}</div>
                </div>
                <div className="text-xs text-slate-400 text-right">{c.check_frequency as string}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Protocoles d'alerte */}
        <div className="rounded-xl bg-slate-900 border border-slate-800 p-6">
          <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">Protocoles d&apos;Alerte</div>
          <div className="space-y-3">
            {Object.entries(protocols).map(([level, proto]) => (
              <div key={level} className="rounded-lg bg-slate-800 p-3">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-bold capitalize" style={{ color: severityColor(level) }}>{level}</span>
                  <span className="text-xs text-slate-400">— {proto.delai_alerte}</span>
                </div>
                <div className="text-xs text-slate-300">{proto.action}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Inventions protégées */}
        {assets.inventions && (
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-6">
            <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">Inventions Protégées</div>
            <div className="space-y-2">
              {(assets.inventions as string[]).map((inv) => (
                <div key={inv} className="flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: GOLD }} />
                  <div className="text-sm text-slate-300">{inv}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actions prioritaires */}
        <div className="rounded-xl border p-5" style={{ borderColor: GOLD + "40", backgroundColor: GOLD + "10" }}>
          <div className="text-xs font-semibold mb-3" style={{ color: GOLD }}>Actions Prioritaires — À Faire Maintenant</div>
          <div className="space-y-2">
            {nextActions.map((action, i) => (
              <div key={i} className="flex items-start gap-2">
                <span className="text-xs font-mono" style={{ color: GOLD }}>{i + 1}.</span>
                <span className="text-xs text-slate-300">{action}</span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
