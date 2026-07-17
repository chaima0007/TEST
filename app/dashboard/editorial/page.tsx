"use client";

import { useEffect, useState } from "react";
import type { EditorialItem, WeeklyTheme, ContentType, ContentStatus } from "@/lib/editorial-data";

interface EditorialData {
  items: EditorialItem[];
  themes: WeeklyTheme[];
  type_meta: Record<ContentType, { label: string; color: string; bg: string }>;
  status_meta: Record<ContentStatus, { label: string; color: string; dot: string }>;
}

const DAY_NAMES = ["", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"];

// ── Icon ──────────────────────────────────────────────────────────────────────

function IconCalendar({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
    </svg>
  );
}

function IconAgent({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <circle cx="10" cy="7" r="3" />
      <path d="M4 17a6 6 0 0112 0H4z" />
    </svg>
  );
}

// ── Item Card ──────────────────────────────────────────────────────────────────

function ItemCard({
  item,
  typeMeta,
  statusMeta,
}: {
  item: EditorialItem;
  typeMeta: EditorialData["type_meta"];
  statusMeta: EditorialData["status_meta"];
}) {
  const tm = typeMeta[item.content_type];
  const sm = statusMeta[item.status];

  return (
    <div className="bg-white rounded-lg border border-slate-200 p-3 hover:shadow-sm transition-shadow">
      {/* Type + status row */}
      <div className="flex items-center justify-between mb-2">
        <span className={`text-[11px] font-medium px-2 py-0.5 rounded-full ${tm.bg} ${tm.color}`}>
          {tm.label}
        </span>
        <span className="flex items-center gap-1 text-[11px]">
          <span className={`w-1.5 h-1.5 rounded-full ${sm.dot}`} />
          <span className={sm.color}>{sm.label}</span>
        </span>
      </div>

      {/* Day + title */}
      <p className="text-[10px] text-slate-400 mb-0.5">{DAY_NAMES[item.day]} {item.date.slice(5, 10).replace("-", "/")}</p>
      <p className="text-xs font-semibold text-slate-800 leading-tight">{item.title}</p>

      {item.hook && (
        <p className="text-[11px] text-slate-500 mt-1.5 italic line-clamp-2">"{item.hook}"</p>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between mt-2.5">
        <span className="flex items-center gap-1 text-[10px] text-slate-400">
          <IconAgent className="w-3 h-3" />
          Agent {item.agent_id}
        </span>
        {item.estimated_impressions && (
          <span className="text-[10px] text-indigo-500 font-medium">
            ~{(item.estimated_impressions / 1000).toFixed(1)}k vues
          </span>
        )}
      </div>
    </div>
  );
}

// ── Week Column ───────────────────────────────────────────────────────────────

function WeekColumn({
  theme,
  items,
  typeMeta,
  statusMeta,
}: {
  theme: WeeklyTheme;
  items: EditorialItem[];
  typeMeta: EditorialData["type_meta"];
  statusMeta: EditorialData["status_meta"];
}) {
  const publishedCount = items.filter((i) => i.status === "published").length;
  const readyCount = items.filter((i) => i.status === "ready").length;

  return (
    <div className="min-w-[260px] flex-1">
      {/* Week header */}
      <div
        className="rounded-xl px-4 py-3 mb-3 text-white"
        style={{ backgroundColor: theme.color }}
      >
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-bold opacity-80">Semaine {theme.week}</span>
          <span className="text-[11px] opacity-70">{items.length} contenus</span>
        </div>
        <p className="text-sm font-semibold leading-tight">{theme.theme}</p>
        <p className="text-[11px] opacity-60 mt-1">
          {theme.start_date.slice(5).replace("-", "/")} → {theme.end_date.slice(5).replace("-", "/")}
        </p>
        {/* Progress micro-bar */}
        <div className="mt-2 flex gap-1">
          {publishedCount > 0 && (
            <div className="h-1 rounded-full bg-white flex-shrink-0" style={{ width: `${(publishedCount / items.length) * 100}%`, opacity: 0.9 }} />
          )}
          {readyCount > 0 && (
            <div className="h-1 rounded-full bg-white flex-shrink-0" style={{ width: `${(readyCount / items.length) * 100}%`, opacity: 0.5 }} />
          )}
          <div className="h-1 rounded-full bg-white/20 flex-1" />
        </div>
      </div>

      {/* Items */}
      <div className="space-y-2">
        {items.length === 0 ? (
          <p className="text-xs text-slate-400 text-center py-4">Aucun contenu planifié</p>
        ) : (
          items
            .sort((a, b) => a.day - b.day)
            .map((item) => (
              <ItemCard key={item.item_id} item={item} typeMeta={typeMeta} statusMeta={statusMeta} />
            ))
        )}
      </div>
    </div>
  );
}

// ── Stats Row ─────────────────────────────────────────────────────────────────

function StatsRow({ items }: { items: EditorialItem[] }) {
  const byStatus = items.reduce<Record<string, number>>((acc, i) => {
    acc[i.status] = (acc[i.status] ?? 0) + 1;
    return acc;
  }, {});
  const totalImpressions = items.reduce((s, i) => s + (i.estimated_impressions ?? 0), 0);

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
      {[
        { label: "Total contenus", value: items.length, color: "text-slate-700" },
        { label: "Publiés", value: byStatus["published"] ?? 0, color: "text-green-600" },
        { label: "Prêts", value: byStatus["ready"] ?? 0, color: "text-blue-600" },
        { label: "Impressions estimées", value: `${(totalImpressions / 1000).toFixed(0)}k`, color: "text-indigo-600" },
      ].map((s) => (
        <div key={s.label} className="bg-white rounded-xl border border-slate-200 px-4 py-3">
          <p className={`text-xl font-bold ${s.color}`}>{s.value}</p>
          <p className="text-xs text-slate-500 mt-0.5">{s.label}</p>
        </div>
      ))}
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

type FilterType = ContentType | "all";

export default function EditorialPage() {
  const [data, setData] = useState<EditorialData | null>(null);
  const [typeFilter, setTypeFilter] = useState<FilterType>("all");

  useEffect(() => {
    fetch("/api/editorial")
      .then((r) => r.json())
      .then(setData);
  }, []);

  const filteredItems = data?.items.filter(
    (i) => typeFilter === "all" || i.content_type === typeFilter
  ) ?? [];

  const allTypes: FilterType[] = ["all", "linkedin_post", "case_study", "article", "newsletter", "cv_update"];

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-pink-600 via-fuchsia-600 to-indigo-600 px-6 py-10">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/20 backdrop-blur flex items-center justify-center">
              <IconCalendar className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Calendrier Éditorial</h1>
              <p className="text-sm text-white/70">Agent 6.8 · Contenu planifié sur 4 semaines</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-6">
        {data && <StatsRow items={data.items} />}

        {/* Type filter */}
        <div className="flex flex-wrap gap-2 mb-6">
          {allTypes.map((t) => {
            const label =
              t === "all"
                ? "Tout"
                : data?.type_meta[t as ContentType]?.label ?? t;
            const count = t === "all" ? data?.items.length : data?.items.filter((i) => i.content_type === t).length;
            return (
              <button
                key={t}
                onClick={() => setTypeFilter(t)}
                className={`text-xs px-3 py-1.5 rounded-full border font-medium transition-colors ${
                  typeFilter === t
                    ? "bg-fuchsia-600 text-white border-fuchsia-600"
                    : "bg-white text-slate-600 border-slate-200 hover:border-slate-300"
                }`}
              >
                {label} {count !== undefined && <span className="opacity-60">({count})</span>}
              </button>
            );
          })}
        </div>

        {/* Calendar grid */}
        {!data ? (
          <div className="text-center py-16 text-slate-400 text-sm">Chargement…</div>
        ) : (
          <div className="flex gap-4 overflow-x-auto pb-4">
            {data.themes.map((theme) => {
              const weekItems = filteredItems.filter((i) => i.week === theme.week);
              return (
                <WeekColumn
                  key={theme.week}
                  theme={theme}
                  items={weekItems}
                  typeMeta={data.type_meta}
                  statusMeta={data.status_meta}
                />
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
