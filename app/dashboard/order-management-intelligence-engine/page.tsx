"use client";

import { useEffect, useState, useCallback } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

interface Order {
  order_id: string;
  region: string;
  order_risk: string;
  order_pattern: string;
  order_severity: string;
  recommended_action: string;
  fulfillment_score: number;
  inventory_score: number;
  quality_score: number;
  logistics_score: number;
  order_composite: number;
  has_delivery_risk: boolean;
  requires_client_alert: boolean;
  estimated_delay_days: number;
  order_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_order_composite: number;
  delivery_risk_count: number;
  client_alert_count: number;
  avg_fulfillment_score: number;
  avg_inventory_score: number;
  avg_quality_score: number;
  avg_logistics_score: number;
  avg_estimated_delay_days: number;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

const RISK_COLORS: Record<string, string> = {
  low: "text-emerald-400",
  moderate: "text-amber-400",
  high: "text-orange-400",
  critical: "text-red-400",
};
const RISK_BG: Record<string, string> = {
  low: "bg-emerald-400/10 border-emerald-400/30",
  moderate: "bg-amber-400/10 border-amber-400/30",
  high: "bg-orange-400/10 border-orange-400/30",
  critical: "bg-red-400/10 border-red-400/30",
};
const SEV_COLORS: Record<string, string> = {
  on_schedule: "text-emerald-400",
  at_risk: "text-amber-400",
  delayed: "text-orange-400",
  blocked: "text-red-400",
};

function fmtLabel(s: string): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

// ─── Gauge Ring ──────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36, cx = 44, cy = 44;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(value / 100, 1);
  const dash = pct * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={`${dash} ${circ - dash}`} strokeLinecap="round"
          transform={`rotate(-90 ${cx} ${cy})`}
        />
        <text x={cx} y={cy + 5} textAnchor="middle" fontSize="14" fontWeight="bold" fill="white">
          {value.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

// ─── DistBar ─────────────────────────────────────────────────────────────────

function DistBar({
  title,
  counts,
  colors,
}: {
  title: string;
  counts: Record<string, number>;
  colors: Record<string, string>;
}) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
      <p className="text-xs text-slate-400 mb-2">{title}</p>
      <div className="flex rounded overflow-hidden h-3 mb-2">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#64748b" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs" style={{ color: colors[k] || "#94a3b8" }}>
            {fmtLabel(k)}: {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── Detail Modal ─────────────────────────────────────────────────────────────

function DetailModal({ order, onClose }: { order: Order; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 relative"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white text-lg"
        >
          &times;
        </button>
        <h3 className="text-white font-bold text-lg mb-1">{order.order_id}</h3>
        <p className="text-slate-400 text-sm mb-4">
          {order.region} &middot; {fmtLabel(order.order_risk)} risk &middot;{" "}
          {fmtLabel(order.order_severity)}
        </p>

        {/* Tabs */}
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-orange-500/20 text-orange-300 border border-orange-500/40"
                  : "text-slate-400 border border-slate-700 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="space-y-2">
            {[
              { label: "Fulfillment", value: order.fulfillment_score },
              { label: "Inventory", value: order.inventory_score },
              { label: "Quality", value: order.quality_score },
              { label: "Logistics", value: order.logistics_score },
              { label: "Composite", value: order.order_composite },
            ].map(({ label, value }) => (
              <div key={label} className="flex items-center gap-3">
                <span className="text-slate-400 text-xs w-28">{label}</span>
                <div className="flex-1 bg-slate-800 rounded-full h-2">
                  <div
                    className="h-2 rounded-full bg-orange-400"
                    style={{ width: `${Math.min(value, 100)}%` }}
                  />
                </div>
                <span className="text-white text-xs w-10 text-right">{value.toFixed(1)}</span>
              </div>
            ))}
            <div className="pt-2 border-t border-slate-800 text-xs text-slate-400 flex justify-between">
              <span>Est. Delay</span>
              <span className="text-orange-300 font-semibold">
                {order.estimated_delay_days}d
              </span>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4">
            <p className="text-slate-200 text-sm leading-relaxed">{order.order_signal}</p>
            <div className="mt-3 flex gap-3 flex-wrap text-xs">
              <span
                className={`px-2 py-0.5 rounded border ${RISK_BG[order.order_risk]} ${RISK_COLORS[order.order_risk]}`}
              >
                {fmtLabel(order.order_risk)} risk
              </span>
              <span className="text-slate-400">{fmtLabel(order.order_pattern)}</span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3">
            <div className="bg-amber-900/30 border border-amber-700/40 rounded-lg p-4">
              <p className="text-amber-300 text-sm font-semibold">
                {fmtLabel(order.recommended_action)}
              </p>
            </div>
            <div className="flex gap-4 text-xs text-slate-400 flex-wrap">
              <span>
                Delivery Risk:{" "}
                <span className={order.has_delivery_risk ? "text-red-400" : "text-emerald-400"}>
                  {order.has_delivery_risk ? "Yes" : "No"}
                </span>
              </span>
              <span>
                Client Alert:{" "}
                <span
                  className={order.requires_client_alert ? "text-orange-400" : "text-emerald-400"}
                >
                  {order.requires_client_alert ? "Required" : "Not required"}
                </span>
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function OrderManagementIntelligencePage() {
  const [orders, setOrders]       = useState<Order[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [riskFilter, setRisk]     = useState("all");
  const [patFilter, setPat]       = useState("all");
  const [selected, setSelected]   = useState<Order | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (riskFilter !== "all") params.set("risk", riskFilter);
    if (patFilter  !== "all") params.set("pattern", patFilter);
    const res  = await fetch(`/api/order-management-intelligence-engine?${params}`);
    const data = await res.json();
    setOrders(data.orders ?? []);
    setSummary(data.summary ?? null);
    setLoading(false);
  }, [riskFilter, patFilter]);

  useEffect(() => { load(); }, [load]);

  const RISK_TABS = ["all", "low", "moderate", "high", "critical"];
  const PAT_TABS  = [
    "all", "none", "fulfillment_delay", "inventory_shortage",
    "supplier_failure", "quality_hold", "logistics_bottleneck",
  ];

  const gaugeColor = (v: number) =>
    v >= 60 ? "#f87171" : v >= 40 ? "#fb923c" : v >= 20 ? "#fbbf24" : "#34d399";

  const dists = [
    {
      title: "Risk Distribution",
      counts: summary?.risk_counts ?? {},
      colors: { low: "#34d399", moderate: "#fbbf24", high: "#fb923c", critical: "#f87171" },
    },
    {
      title: "Pattern Distribution",
      counts: summary?.pattern_counts ?? {},
      colors: {
        none: "#64748b",
        fulfillment_delay: "#fb923c",
        inventory_shortage: "#fbbf24",
        supplier_failure: "#f87171",
        quality_hold: "#c084fc",
        logistics_bottleneck: "#f472b6",
      },
    },
    {
      title: "Severity Distribution",
      counts: summary?.severity_counts ?? {},
      colors: {
        on_schedule: "#34d399",
        at_risk: "#fbbf24",
        delayed: "#fb923c",
        blocked: "#f87171",
      },
    },
    {
      title: "Action Distribution",
      counts: summary?.action_counts ?? {},
      colors: {
        no_action: "#64748b",
        order_monitoring: "#38bdf8",
        expedite_fulfillment: "#fbbf24",
        supplier_escalation: "#fb923c",
        inventory_reallocation: "#a78bfa",
        quality_inspection: "#c084fc",
        logistics_rerouting: "#f472b6",
        customer_notification: "#f59e0b",
        emergency_procurement: "#f87171",
      },
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal order={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Order Management Intelligence Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Fulfillment risk per order — delivery delays, inventory shortages, supplier failures,
          quality holds, and logistics bottlenecks
        </p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          {[
            { label: "Total Orders",      value: summary.total.toString() },
            { label: "Avg Composite",     value: summary.avg_order_composite.toFixed(1) },
            { label: "Delivery Risk",     value: summary.delivery_risk_count.toString() },
            { label: "Client Alerts",     value: summary.client_alert_count.toString() },
            { label: "Avg Delay (d)",     value: summary.avg_estimated_delay_days.toFixed(1) },
            { label: "Critical Orders",   value: (summary.risk_counts["critical"] ?? 0).toString() },
          ].map(({ label, value }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-lg p-4">
              <p className="text-slate-400 text-xs">{label}</p>
              <p className="text-white text-xl font-bold mt-1">{value}</p>
            </div>
          ))}
        </div>
      )}

      {/* Gauge Rings */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 mb-6">
          <p className="text-slate-400 text-xs mb-4">
            Average Sub-Scores (0–100, higher = more risk)
          </p>
          <div className="flex flex-wrap gap-8 justify-center">
            <GaugeRing
              value={summary.avg_fulfillment_score}
              label="Fulfillment"
              color={gaugeColor(summary.avg_fulfillment_score)}
            />
            <GaugeRing
              value={summary.avg_inventory_score}
              label="Inventory"
              color={gaugeColor(summary.avg_inventory_score)}
            />
            <GaugeRing
              value={summary.avg_quality_score}
              label="Quality"
              color={gaugeColor(summary.avg_quality_score)}
            />
            <GaugeRing
              value={summary.avg_logistics_score}
              label="Logistics"
              color={gaugeColor(summary.avg_logistics_score)}
            />
          </div>
        </div>
      )}

      {/* Distribution Bars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
        {dists.map((d) => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filters */}
      <div className="space-y-2 mb-6">
        <div className="flex flex-wrap gap-2">
          {RISK_TABS.map((r) => (
            <button
              key={r}
              onClick={() => setRisk(r)}
              className={`px-3 py-1 rounded text-xs font-medium border transition-colors ${
                riskFilter === r
                  ? "bg-orange-500/20 text-orange-300 border-orange-500/40"
                  : "text-slate-400 border-slate-700 hover:text-white hover:border-orange-700"
              }`}
            >
              {fmtLabel(r)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {PAT_TABS.map((p) => (
            <button
              key={p}
              onClick={() => setPat(p)}
              className={`px-3 py-1 rounded text-xs font-medium border transition-colors ${
                patFilter === p
                  ? "bg-orange-500/20 text-orange-300 border-orange-500/40"
                  : "text-slate-400 border-slate-700 hover:text-white hover:border-orange-700"
              }`}
            >
              {fmtLabel(p)}
            </button>
          ))}
        </div>
      </div>

      {/* Order Cards */}
      {loading ? (
        <div className="text-slate-400 text-center py-12">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {orders.map((order) => (
            <button
              key={order.order_id}
              onClick={() => setSelected(order)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-left hover:border-orange-700 transition-colors"
            >
              {/* Header row */}
              <div className="flex items-center justify-between mb-1">
                <span className="text-white font-semibold text-sm">{order.order_id}</span>
                <span
                  className={`text-xs font-medium ${RISK_COLORS[order.order_risk] ?? "text-slate-400"}`}
                >
                  {fmtLabel(order.order_risk)}
                </span>
              </div>

              <p className="text-slate-400 text-xs mb-2">{order.region}</p>

              {/* Severity badge */}
              <p
                className={`text-xs mb-1 ${SEV_COLORS[order.order_severity] ?? "text-slate-400"}`}
              >
                {fmtLabel(order.order_severity)}
              </p>

              {/* Composite bar */}
              <div className="flex items-center gap-2 mb-2">
                <div className="flex-1 bg-slate-800 rounded-full h-1.5">
                  <div
                    className="h-1.5 rounded-full bg-orange-400"
                    style={{ width: `${Math.min(order.order_composite, 100)}%` }}
                  />
                </div>
                <span className="text-xs text-slate-300">
                  {order.order_composite.toFixed(0)}
                </span>
              </div>

              {/* Pattern */}
              <p className="text-slate-500 text-xs truncate mb-2">
                {fmtLabel(order.order_pattern)}
              </p>

              {/* Delay */}
              {order.estimated_delay_days > 0 && (
                <p className="text-xs text-amber-400 mb-2">
                  {order.estimated_delay_days}d est. delay
                </p>
              )}

              {/* Flag badges */}
              <div className="flex gap-2 flex-wrap">
                {order.has_delivery_risk && (
                  <span className="text-xs bg-orange-400/10 text-orange-400 border border-orange-400/30 px-1.5 py-0.5 rounded">
                    DELIVERY RISK
                  </span>
                )}
                {order.requires_client_alert && (
                  <span className="text-xs bg-amber-900/40 text-amber-300 border border-amber-700/40 px-1.5 py-0.5 rounded">
                    CLIENT ALERT
                  </span>
                )}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
