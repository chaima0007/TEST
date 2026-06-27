"use client";

import { useEffect, useState } from "react";
import type { LinkedInPost, CVEntry, CaseStudy } from "@/lib/branding-data";

interface BrandingData {
  agent: {
    id: string;
    name: string;
    expertise: string[];
    stats: { postsGenerated: number; cvEntriesCreated: number; caseStudiesWritten: number; estimatedImpressions: number };
  };
  linkedin_posts: LinkedInPost[];
  cv_entries: CVEntry[];
  case_studies: CaseStudy[];
}

// ── Icons ──────────────────────────────────────────────────────────────────

function IconLinkedIn({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
    </svg>
  );
}

function IconCopy({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
      <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
    </svg>
  );
}

function IconCheck({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
    </svg>
  );
}

function IconDownload({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor">
      <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
    </svg>
  );
}

function downloadTxt(filename: string, content: string) {
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function ExportButton({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="inline-flex items-center gap-1.5 text-[12px] font-medium px-3 py-1.5 rounded-md bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 hover:border-slate-300 transition-colors"
    >
      <IconDownload className="w-3.5 h-3.5" />
      {label}
    </button>
  );
}

// ── Copy button ───────────────────────────────────────────────────────────────

function CopyButton({ text, label = "Copier" }: { text: string; label?: string }) {
  const [copied, setCopied] = useState(false);
  const handle = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button
      onClick={handle}
      className={`inline-flex items-center gap-1.5 text-[12px] font-medium px-3 py-1.5 rounded-md transition-all duration-150 ${
        copied
          ? "bg-green-100 text-green-700"
          : "bg-slate-100 text-slate-600 hover:bg-slate-200"
      }`}
    >
      {copied ? <IconCheck className="w-3.5 h-3.5" /> : <IconCopy className="w-3.5 h-3.5" />}
      {copied ? "Copié !" : label}
    </button>
  );
}

// ── LinkedIn Post Card ────────────────────────────────────────────────────────

function PostCard({ post }: { post: LinkedInPost }) {
  const [expanded, setExpanded] = useState(false);
  const fullText = `${post.hook}\n\n${post.body}\n\n${post.hashtags.map((h) => `#${h}`).join(" ")}`;

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-100 flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center flex-shrink-0">
            <IconLinkedIn className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="text-[13px] font-semibold text-slate-900">{post.title}</p>
            <div className="flex items-center gap-3 mt-0.5">
              <span className="text-[11px] text-slate-400">{post.char_count} car.</span>
              <span className="text-[11px] text-blue-600 font-medium">~{post.impressions_estimate.toLocaleString("fr-FR")} impressions est.</span>
            </div>
          </div>
        </div>
        <CopyButton text={fullText} label="Copier le post" />
      </div>

      {/* Hook — always visible */}
      <div className="px-5 pt-4">
        <p className="text-[14px] font-bold text-slate-900 leading-snug">{post.hook}</p>
      </div>

      {/* Body — expandable */}
      <div className="px-5 pb-4">
        {expanded ? (
          <pre className="mt-3 text-[13px] text-slate-700 leading-relaxed whitespace-pre-wrap font-sans">
            {post.body}
          </pre>
        ) : (
          <p className="mt-2 text-[13px] text-slate-500 line-clamp-2">
            {post.body.split("\n")[0]}
          </p>
        )}

        <button
          onClick={() => setExpanded((e) => !e)}
          className="mt-3 text-[12px] text-blue-600 font-medium hover:underline"
        >
          {expanded ? "Réduire ↑" : "Lire le post complet ↓"}
        </button>

        {/* Hashtags */}
        {expanded && (
          <div className="flex flex-wrap gap-1.5 mt-3">
            {post.hashtags.map((tag) => (
              <span key={tag} className="text-[11px] text-blue-600 font-medium bg-blue-50 px-2 py-0.5 rounded-full">
                #{tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ── CV Entry Card ─────────────────────────────────────────────────────────────

const CATEGORY_COLORS: Record<string, string> = {
  "Expérience": "bg-blue-100 text-blue-700",
  "Compétences": "bg-green-100 text-green-700",
  "Réalisation": "bg-purple-100 text-purple-700",
};

function CVCard({ entry }: { entry: CVEntry }) {
  const bulletText = entry.bullets.map((b) => `• ${b}`).join("\n");
  const fullText = `${entry.title} (${entry.period})\n${bulletText}\n\nMots-clés : ${entry.keywords.join(", ")}`;

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${CATEGORY_COLORS[entry.category] ?? "bg-slate-100 text-slate-600"}`}>
              {entry.category}
            </span>
            <span className="text-[11px] text-slate-400">{entry.period}</span>
            <span className="text-[11px] font-semibold text-pink-600">Impact {entry.impact_score}/10</span>
          </div>
          <p className="text-[13px] font-semibold text-slate-900 leading-snug">{entry.title}</p>
        </div>
        <CopyButton text={fullText} label="Copier" />
      </div>

      <ul className="space-y-2">
        {entry.bullets.map((b, i) => (
          <li key={i} className="flex gap-2 text-[12px] text-slate-700 leading-relaxed">
            <span className="text-pink-500 font-bold flex-shrink-0 mt-0.5">•</span>
            <span>{b}</span>
          </li>
        ))}
      </ul>

      <div className="mt-3 pt-3 border-t border-slate-100">
        <p className="text-[10px] text-slate-400 font-medium mb-1.5">MOTS-CLÉS ATS</p>
        <div className="flex flex-wrap gap-1">
          {entry.keywords.map((kw) => (
            <span key={kw} className="text-[10px] bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded font-mono">
              {kw}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Case Study Card ───────────────────────────────────────────────────────────

function CaseCard({ cs }: { cs: CaseStudy }) {
  const fullText = `ÉTUDE DE CAS — ${cs.client_alias}\nSecteur : ${cs.sector}\n\nAVANT :\n${cs.problem_before}\n\nACTION :\n${cs.action_taken}\n\nAPRÈS :\n${cs.result_after}\n\nCitation client :\n${cs.client_quote}`;

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div className="px-5 py-3 border-b border-slate-100 flex items-center justify-between">
        <div>
          <p className="text-[13px] font-semibold text-slate-900">{cs.client_alias}</p>
          <p className="text-[11px] text-slate-400">{cs.sector}</p>
        </div>
        <CopyButton text={fullText} label="Copier l'étude" />
      </div>

      <div className="grid sm:grid-cols-3 divide-y sm:divide-y-0 sm:divide-x divide-slate-100">
        <div className="px-5 py-4">
          <p className="text-[10px] font-bold text-red-500 uppercase tracking-wide mb-2">Avant — Le problème</p>
          <p className="text-[12px] text-slate-700 leading-relaxed">{cs.problem_before}</p>
        </div>
        <div className="px-5 py-4">
          <p className="text-[10px] font-bold text-blue-600 uppercase tracking-wide mb-2">Action — Ce qu'on a fait</p>
          <p className="text-[12px] text-slate-700 leading-relaxed">{cs.action_taken}</p>
        </div>
        <div className="px-5 py-4">
          <p className="text-[10px] font-bold text-green-600 uppercase tracking-wide mb-2">Après — Le résultat</p>
          <p className="text-[12px] text-slate-700 leading-relaxed">{cs.result_after}</p>
        </div>
      </div>

      {/* Quote */}
      <div className="px-5 py-4 bg-slate-50 border-t border-slate-100">
        <blockquote className="text-[13px] text-slate-600 italic leading-relaxed">
          {cs.client_quote}
        </blockquote>
      </div>

      {/* Metrics */}
      <div className="px-5 py-3 border-t border-slate-100 flex flex-wrap gap-4">
        {Object.entries(cs.metrics).map(([k, v]) => (
          <div key={k} className="text-center">
            <p className="text-[15px] font-bold text-slate-900 tabular-nums">{typeof v === "number" && v > 100 ? `${v.toLocaleString("fr-FR")}` : v}</p>
            <p className="text-[10px] text-slate-400">{k.replace(/_/g, " ")}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Skeleton ──────────────────────────────────────────────────────────────────

function Sk({ className }: { className?: string }) {
  return <div className={`animate-pulse bg-slate-100 rounded-lg ${className}`} />;
}

// ── Page ──────────────────────────────────────────────────────────────────────

type Tab = "linkedin" | "cv" | "cases";

export default function BrandingPage() {
  const [data, setData] = useState<BrandingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<Tab>("linkedin");

  useEffect(() => {
    fetch("/api/branding")
      .then((r) => r.json())
      .then((d: BrandingData) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const TABS: { key: Tab; label: string; count?: number }[] = [
    { key: "linkedin", label: "Posts LinkedIn", count: data?.linkedin_posts.length },
    { key: "cv", label: "Entrées CV", count: data?.cv_entries.length },
    { key: "cases", label: "Études de cas", count: data?.case_studies.length },
  ];

  return (
    <div className="space-y-5 pb-12">
      {/* Header */}
      <div className="flex items-start justify-between pt-1">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-7 h-7 rounded-lg bg-pink-100 flex items-center justify-center text-base">✨</div>
            <span className="text-[11px] font-bold text-pink-600 uppercase tracking-widest">Agent 6.0 — Documentation & Personal Branding</span>
          </div>
          <h1 className="text-[22px] font-semibold text-slate-900 tracking-tight">
            Mon Profil Expert — LinkedIn & CV
          </h1>
          <p className="text-[13px] text-slate-500 mt-0.5">
            L'agent 6.0 documente chaque victoire du swarm en contenu LinkedIn percutant et en entrées CV quantifiées.
          </p>
        </div>
      </div>

      {/* Agent profile strip */}
      {!loading && data && (
        <div className="rounded-xl overflow-hidden" style={{ background: "linear-gradient(135deg, #EC4899 0%, #8B5CF6 60%, #6366F1 100%)" }}>
          <div className="px-6 py-5 flex flex-col sm:flex-row sm:items-center gap-5">
            <div className="w-14 h-14 rounded-xl bg-white/20 flex items-center justify-center text-3xl flex-shrink-0">✨</div>
            <div className="flex-1">
              <p className="text-[11px] font-bold text-pink-200 uppercase tracking-widest mb-0.5">Expert IA en Communication</p>
              <p className="text-white font-bold text-lg leading-tight">{data.agent.name}</p>
              <div className="flex flex-wrap gap-1.5 mt-2">
                {data.agent.expertise.map((e) => (
                  <span key={e} className="text-[10px] text-white/80 bg-white/15 px-2 py-0.5 rounded-full font-medium">{e}</span>
                ))}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 flex-shrink-0">
              {[
                { label: "Posts générés", value: data.agent.stats.postsGenerated },
                { label: "Entrées CV", value: data.agent.stats.cvEntriesCreated },
                { label: "Études de cas", value: data.agent.stats.caseStudiesWritten },
                { label: "Impressions est.", value: `${(data.agent.stats.estimatedImpressions / 1000).toFixed(0)}k` },
              ].map((s) => (
                <div key={s.label} className="text-center">
                  <p className="text-2xl font-bold text-white tabular-nums">{s.value}</p>
                  <p className="text-[10px] text-white/60">{s.label}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-1 border-b border-slate-200">
        {TABS.map((t) => (
          <button
            key={t.key}
            onClick={() => setTab(t.key)}
            className={`flex items-center gap-1.5 px-4 py-2 text-[13px] font-medium transition-colors border-b-2 -mb-px ${
              tab === t.key
                ? "border-pink-500 text-pink-600"
                : "border-transparent text-slate-500 hover:text-slate-700"
            }`}
          >
            {t.label}
            {t.count !== undefined && (
              <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded-full ${tab === t.key ? "bg-pink-100 text-pink-600" : "bg-slate-100 text-slate-500"}`}>
                {t.count}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="space-y-4">
          <Sk className="h-48" />
          <Sk className="h-48" />
          <Sk className="h-48" />
        </div>
      ) : (
        <>
          {tab === "linkedin" && (
            <div className="space-y-4">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2 text-[12px] text-slate-500 bg-blue-50 border border-blue-100 rounded-lg px-4 py-2.5 flex-1">
                  <IconLinkedIn className="w-4 h-4 text-blue-600 flex-shrink-0" />
                  <span>Cliquez sur <strong>"Copier le post"</strong> puis collez directement dans LinkedIn. Chaque post est formaté pour le fil LinkedIn mobile et desktop.</span>
                </div>
                {data && (
                  <ExportButton
                    label="Exporter tout (.txt)"
                    onClick={() => {
                      const content = data.linkedin_posts
                        .map((p, i) =>
                          `═══ POST ${i + 1} — ${p.title} ═══\n\n${p.hook}\n\n${p.body}\n\n${p.hashtags.map((h) => `#${h}`).join(" ")}`
                        )
                        .join("\n\n" + "─".repeat(60) + "\n\n");
                      downloadTxt("linkedin-posts-swarm.txt", content);
                    }}
                  />
                )}
              </div>
              {data?.linkedin_posts.map((p) => <PostCard key={p.post_id} post={p} />)}
            </div>
          )}

          {tab === "cv" && (
            <div className="space-y-4">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2 text-[12px] text-slate-500 bg-pink-50 border border-pink-100 rounded-lg px-4 py-2.5 flex-1">
                  <span className="text-pink-500 flex-shrink-0">✨</span>
                  <span>Entrées CV au format <strong>STAR</strong> avec keywords ATS intégrés. Copiez chaque section dans votre CV Word, Canva ou LinkedIn.</span>
                </div>
                {data && (
                  <ExportButton
                    label="Exporter CV (.txt)"
                    onClick={() => {
                      const content = data.cv_entries
                        .map((e) =>
                          `[${e.category.toUpperCase()}] ${e.title} — ${e.period}\n\n${e.bullets.map((b) => `• ${b}`).join("\n")}\n\nMots-clés ATS : ${e.keywords.join(", ")}`
                        )
                        .join("\n\n" + "─".repeat(60) + "\n\n");
                      downloadTxt("cv-swarm-architect.txt", content);
                    }}
                  />
                )}
              </div>
              {data?.cv_entries.map((e) => <CVCard key={e.entry_id} entry={e} />)}
            </div>
          )}

          {tab === "cases" && (
            <div className="space-y-5">
              <div className="flex items-center gap-2 text-[12px] text-slate-500 bg-green-50 border border-green-100 rounded-lg px-4 py-2.5">
                <span className="text-green-500 flex-shrink-0">📁</span>
                <span>Études de cas <strong>Avant/Après</strong> utilisables en portfolio, proposition commerciale ou post LinkedIn long-format.</span>
              </div>
              {data?.case_studies.map((c) => <CaseCard key={c.case_id} cs={c} />)}
            </div>
          )}
        </>
      )}
    </div>
  );
}
