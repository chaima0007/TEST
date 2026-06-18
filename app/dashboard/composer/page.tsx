"use client";

import { useEffect, useState } from "react";

interface SubjectVariant { variant_key: string; subject: string }
interface Template {
  template_id: string;
  name: string;
  channel: string;
  description: string;
  tags: string[];
  subject_variants: SubjectVariant[];
  required_variables: string[];
}

interface ComposedEmail {
  template_id: string;
  variant_key: string;
  subject: string;
  body_text: string;
  body_html: string;
  channel: string;
  is_complete: boolean;
  missing_vars: string[];
}

const TAG_COLORS: Record<string, string> = {
  cold: "bg-blue-900/50 text-blue-300",
  warm: "bg-emerald-900/50 text-emerald-300",
  post_quote: "bg-violet-900/50 text-violet-300",
  intro: "bg-indigo-900/50 text-indigo-300",
  followup: "bg-amber-900/50 text-amber-300",
  urgency: "bg-red-900/50 text-red-300",
  social_proof: "bg-teal-900/50 text-teal-300",
  demo: "bg-cyan-900/50 text-cyan-300",
  breakup: "bg-slate-700 text-slate-300",
};

const VAR_DEFAULTS: Record<string, string> = {
  contact_name: "M. Dupont",
  company_name: "Plomberie Martin",
  sector: "artisan",
  pagespeed: "28",
  revenue_loss: "320",
  agent_name: "Sophie",
  case_company: "Resto Le Midi",
  case_traffic: "34",
  case_leads: "8",
  case_pagespeed_gain: "42",
  quote_total: "590",
};

function TagBadge({ tag }: { tag: string }) {
  return (
    <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${TAG_COLORS[tag] ?? "bg-slate-700 text-slate-400"}`}>
      {tag}
    </span>
  );
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    });
  };
  return (
    <button
      onClick={copy}
      className="text-xs text-slate-500 hover:text-slate-200 transition-colors px-2 py-1 rounded hover:bg-slate-700"
    >
      {copied ? "Copié ✓" : "Copier"}
    </button>
  );
}

export default function ComposerPage() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedId, setSelectedId] = useState<string>("");
  const [variantKey, setVariantKey] = useState("A");
  const [variables, setVariables] = useState<Record<string, string>>({});
  const [composed, setComposed] = useState<ComposedEmail | null>(null);
  const [composing, setComposing] = useState(false);
  const [preview, setPreview] = useState<"text" | "html">("text");
  const [tagFilter, setTagFilter] = useState<string>("all");

  useEffect(() => {
    setLoading(true);
    fetch("/api/composer")
      .then((r) => r.json())
      .then((d) => {
        setTemplates(d.templates ?? []);
        if (d.templates?.length > 0) {
          const first = d.templates[0];
          setSelectedId(first.template_id);
          initVars(first);
        }
      })
      .finally(() => setLoading(false));
  }, []);

  function initVars(tmpl: Template) {
    const init: Record<string, string> = {};
    for (const v of tmpl.required_variables) {
      init[v] = VAR_DEFAULTS[v] ?? "";
    }
    setVariables(init);
    setComposed(null);
  }

  function selectTemplate(id: string) {
    const tmpl = templates.find((t) => t.template_id === id);
    if (!tmpl) return;
    setSelectedId(id);
    setVariantKey(tmpl.subject_variants[0]?.variant_key ?? "A");
    initVars(tmpl);
  }

  async function compose() {
    if (!selectedId) return;
    setComposing(true);
    try {
      const res = await fetch("/api/composer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ template_id: selectedId, variables, variant_key: variantKey }),
      });
      const data = await res.json();
      setComposed(data);
    } finally {
      setComposing(false);
    }
  }

  const selected = templates.find((t) => t.template_id === selectedId);

  const allTags = Array.from(new Set(templates.flatMap((t) => t.tags)));
  const filteredTemplates = tagFilter === "all" ? templates : templates.filter((t) => t.tags.includes(tagFilter));

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div>
        <h1 className="text-2xl font-bold text-white">Compositeur d'Emails</h1>
        <p className="text-slate-400 text-sm mt-1">
          Sélectionnez un template, renseignez les variables et prévisualisez l'email généré
        </p>
      </div>

      {loading ? (
        <div className="text-slate-500 text-center py-16">Chargement…</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Template selector */}
          <div className="space-y-3">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Templates</p>

              {/* Tag filter pills */}
              <div className="flex flex-wrap gap-1.5 mb-3">
                <button
                  onClick={() => setTagFilter("all")}
                  className={`text-xs px-2 py-0.5 rounded transition-colors ${tagFilter === "all" ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}
                >
                  Tous
                </button>
                {allTags.map((tag) => (
                  <button
                    key={tag}
                    onClick={() => setTagFilter(tag)}
                    className={`text-xs px-2 py-0.5 rounded transition-colors ${tagFilter === tag ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}
                  >
                    {tag}
                  </button>
                ))}
              </div>

              <div className="space-y-1">
                {filteredTemplates.map((t) => (
                  <button
                    key={t.template_id}
                    onClick={() => selectTemplate(t.template_id)}
                    className={`w-full text-left rounded-lg p-3 transition-colors ${selectedId === t.template_id ? "bg-indigo-900/40 border border-indigo-700/50" : "hover:bg-slate-800 border border-transparent"}`}
                  >
                    <p className="text-sm font-medium text-white">{t.name}</p>
                    <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">{t.description}</p>
                    <div className="flex flex-wrap gap-1 mt-1.5">
                      {t.tags.map((tag) => <TagBadge key={tag} tag={tag} />)}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Variable inputs + compose */}
          <div className="space-y-4">
            {selected ? (
              <>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                  <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">
                    Variables ({selected.required_variables.length})
                  </p>
                  <div className="space-y-3">
                    {selected.required_variables.map((v) => (
                      <div key={v}>
                        <label className="block text-xs text-slate-400 mb-1 font-mono">{"{" + v + "}"}</label>
                        <input
                          type="text"
                          value={variables[v] ?? ""}
                          onChange={(e) => setVariables((prev) => ({ ...prev, [v]: e.target.value }))}
                          placeholder={VAR_DEFAULTS[v] ?? v}
                          className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 transition-colors"
                        />
                      </div>
                    ))}
                  </div>
                </div>

                {/* Subject variant selector */}
                {selected.subject_variants.length > 1 && (
                  <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                    <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-3">Objet — variante</p>
                    <div className="space-y-2">
                      {selected.subject_variants.map((sv) => (
                        <button
                          key={sv.variant_key}
                          onClick={() => setVariantKey(sv.variant_key)}
                          className={`w-full text-left rounded-lg p-3 border transition-colors ${variantKey === sv.variant_key ? "border-indigo-600 bg-indigo-950/30" : "border-slate-700 hover:bg-slate-800"}`}
                        >
                          <span className="text-xs font-bold text-indigo-400 mr-2">{sv.variant_key}</span>
                          <span className="text-sm text-slate-300">{sv.subject}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                <button
                  onClick={compose}
                  disabled={composing}
                  className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-semibold transition-colors"
                >
                  {composing ? "Génération…" : "Générer l'email →"}
                </button>
              </>
            ) : (
              <div className="text-slate-500 text-center py-8">Sélectionnez un template</div>
            )}
          </div>

          {/* Preview panel */}
          <div className="space-y-3">
            {composed ? (
              <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <div className="px-4 py-3 border-b border-slate-800 flex items-center justify-between">
                  <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Aperçu</p>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setPreview("text")}
                      className={`text-xs px-2 py-1 rounded transition-colors ${preview === "text" ? "bg-slate-700 text-white" : "text-slate-500 hover:text-white"}`}
                    >
                      Texte
                    </button>
                    <button
                      onClick={() => setPreview("html")}
                      className={`text-xs px-2 py-1 rounded transition-colors ${preview === "html" ? "bg-slate-700 text-white" : "text-slate-500 hover:text-white"}`}
                    >
                      HTML
                    </button>
                  </div>
                </div>

                {!composed.is_complete && (
                  <div className="mx-4 mt-3 bg-amber-950/30 border border-amber-800/40 rounded-lg p-3">
                    <p className="text-amber-400 text-xs font-semibold mb-1">Variables manquantes :</p>
                    <div className="flex flex-wrap gap-1">
                      {composed.missing_vars.map((v) => (
                        <span key={v} className="font-mono text-xs bg-amber-900/40 text-amber-300 px-1.5 py-0.5 rounded">
                          {"{" + v + "}"}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="p-4 space-y-3">
                  {/* Subject */}
                  <div className="bg-slate-800/60 rounded-lg p-3">
                    <div className="flex items-center justify-between mb-1">
                      <p className="text-[10px] text-slate-500 uppercase font-semibold">Objet</p>
                      <CopyButton text={composed.subject} />
                    </div>
                    <p className="text-sm text-white font-medium">{composed.subject}</p>
                  </div>

                  {/* Body */}
                  <div className="bg-slate-800/60 rounded-lg p-3">
                    <div className="flex items-center justify-between mb-2">
                      <p className="text-[10px] text-slate-500 uppercase font-semibold">Corps</p>
                      <CopyButton text={preview === "text" ? composed.body_text : composed.body_html} />
                    </div>
                    {preview === "text" ? (
                      <pre className="text-xs text-slate-300 whitespace-pre-wrap leading-relaxed font-sans">
                        {composed.body_text}
                      </pre>
                    ) : (
                      <div
                        className="text-xs text-slate-300 leading-relaxed prose prose-sm prose-invert max-w-none"
                        dangerouslySetInnerHTML={{ __html: composed.body_html }}
                      />
                    )}
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center">
                <p className="text-slate-600 text-sm">L'aperçu apparaîtra ici après génération</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
