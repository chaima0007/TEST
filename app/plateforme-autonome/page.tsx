import Link from "next/link";
import fs from "node:fs";
import path from "node:path";

// « Forme de vie » de la plateforme autonome — Caelum.
// Lit data/autonomous_platform_report.json + data/platform_vitals.json (générés par
// scripts/autonomous_platform.py) et affiche l'organisme : pouls, signes vitaux, scénarios.
// Rendu statique : figé au build, léger, sans dépendance.

export const dynamic = "force-static";
export const metadata = {
  title: "Plateforme autonome — forme de vie | Caelum",
  description: "L'état vivant de la plateforme : pouls, résilience, scénarios simulés et sceau de protocole.",
};

type Scenario = { scenario: string; type?: string; verdict: string; mitigation?: string;
  p95_ms?: number; p99_ms?: number; pct_sous_200ms?: number; pct_corpus?: number;
  urls_impactees_moy?: number; pages_estimees?: number;
  urls_testees?: number; vivantes_pct?: number; mortes?: number;
  modules?: number; frais?: number; a_reverifier?: number; prioritaire?: number; sources_modifiees?: number;
  reponses?: number; depuis_naissance?: number; battements_sans_croissance?: number;
  plan_pct?: number; plan_faits?: number; plan_total?: number; prochaine_etape?: string;
  caelum_normes?: number; caelum_sources?: number; caelum_aides?: number };

function lire(rel: string): Record<string, unknown> {
  try {
    return JSON.parse(fs.readFileSync(path.join(process.cwd(), rel), "utf-8"));
  } catch {
    return {};
  }
}

const COULEUR: Record<string, string> = {
  OK: "text-emerald-700 bg-emerald-50 border-emerald-200",
  ALERTE: "text-amber-700 bg-amber-50 border-amber-200",
  CRITIQUE: "text-rose-700 bg-rose-50 border-rose-200",
};

export default function PlateformeAutonome() {
  const rapport = lire("data/autonomous_platform_report.json") as {
    corpus?: Record<string, number>; scenarios?: Scenario[]; sante?: { protocole: string; verdict: string; sortie?: string }[];
    sceau?: Record<string, unknown>; vie?: Record<string, unknown>; genere_le?: string; monte_carlo_n?: number;
  };
  const todo = lire("data/platform_todo.json") as {
    total?: number; par_priorite?: Record<string, number>;
    taches?: { id: string; titre: string; categorie: string; priorite: string; action_suggeree: string; humain: boolean; organe: string }[];
  };
  const vitals = lire("data/platform_vitals.json") as {
    etat_vie?: string; battements?: number; age_jours?: number; resilience?: number; naissance?: string;
    voix?: string; historique?: { ts: string; resilience: number; etat_vie: string }[];
  };

  const corpus = rapport.corpus || {};
  const scenarios = rapport.scenarios || [];
  const sceau = (rapport.sceau || {}) as Record<string, unknown>;
  const resilience = Number(vitals.resilience ?? sceau.score_resilience ?? 0);
  const vivant = Object.keys(vitals).length > 0;
  const etatStr = String(vitals.etat_vie || "");
  const enForme = etatStr.includes("🟢") || etatStr.includes("🐣");

  const etat = scenarios.filter((s) => s.type === "etat");
  const stress = scenarios.filter((s) => s.type === "stress");

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-white/10">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-lg flex items-center justify-center">
              <span className="text-white text-xs font-black">C</span>
            </div>
            <span className="font-bold text-lg">Caelum</span>
          </Link>
          <Link href="/" className="text-sm text-slate-400 hover:text-white">← Retour</Link>
        </div>
      </header>

      {/* Cœur vivant */}
      <section className="max-w-5xl mx-auto px-6 pt-14 pb-8 text-center">
        <div className="relative inline-flex items-center justify-center">
          <span className={`absolute inline-flex h-24 w-24 rounded-full ${enForme ? "bg-emerald-500/30" : "bg-amber-500/30"} ${vivant ? "animate-ping" : ""}`} />
          <span className={`relative inline-flex h-24 w-24 rounded-full items-center justify-center text-4xl ${enForme ? "bg-emerald-500/20 border border-emerald-400/40" : "bg-amber-500/20 border border-amber-400/40"}`}>
            ❤️
          </span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-bold mt-6">Plateforme autonome — forme de vie</h1>
        <p className="mt-3 text-lg">
          {vivant ? (
            <span className="font-semibold">{etatStr}</span>
          ) : (
            <span className="text-slate-400">En sommeil — lancez <code className="text-slate-300">python3 scripts/autonomous_platform.py</code></span>
          )}
        </p>
        {vivant && (
          <p className="text-slate-400 text-sm mt-2">
            Pouls {vitals.battements} battement(s) · âge {vitals.age_jours} jour(s) ·
            née le {String(vitals.naissance || "").slice(0, 10)}
          </p>
        )}
        {vivant && vitals.voix && (
          <p className="mt-5 max-w-2xl mx-auto rounded-2xl border border-white/10 bg-white/5 px-5 py-4 text-slate-200 italic">
            🗣️ « {vitals.voix} »
          </p>
        )}
      </section>

      {/* Signes vitaux */}
      <section className="max-w-5xl mx-auto px-6 grid sm:grid-cols-4 gap-4">
        {[
          { label: "Résilience", val: `${resilience}%`, sub: "scénarios verts" },
          { label: "Sceau", val: String(sceau.statut || "—"), sub: "protocole" },
          { label: "Réponses", val: String(corpus.reponses ?? "—"), sub: `${corpus.modules ?? "—"} domaines` },
          { label: "Sources", val: String(corpus.sources ?? "—"), sub: `${corpus.sources_officielles ?? "—"} officielles` },
        ].map((c) => (
          <div key={c.label} className="rounded-2xl border border-white/10 bg-white/5 p-5">
            <p className="text-xs uppercase tracking-wide text-slate-400">{c.label}</p>
            <p className="text-2xl font-bold mt-1">{c.val}</p>
            <p className="text-xs text-slate-500 mt-1">{c.sub}</p>
          </div>
        ))}
      </section>

      {/* Barre de résilience */}
      <section className="max-w-5xl mx-auto px-6 mt-8">
        <div className="h-3 w-full rounded-full bg-white/10 overflow-hidden">
          <div className={`h-full ${resilience >= 80 ? "bg-emerald-500" : resilience >= 50 ? "bg-amber-500" : "bg-rose-500"}`} style={{ width: `${resilience}%` }} />
        </div>
      </section>

      {/* État actuel */}
      {etat.length > 0 && (
        <section className="max-w-5xl mx-auto px-6 mt-12">
          <h2 className="text-xl font-bold">État actuel</h2>
          <p className="text-slate-400 text-sm mt-1">Ce que vit la plateforme aujourd&apos;hui (seul un CRITIQUE ici bloque).</p>
          <div className="mt-4 grid sm:grid-cols-2 gap-3">
            {etat.map((s) => (
              <div key={s.scenario} className={`rounded-xl border bg-white/5 p-4 ${COULEUR[s.verdict] || "border-white/10"}`}>
                <div className="flex items-center justify-between gap-2">
                  <span className="font-semibold text-sm text-slate-100">{s.scenario}</span>
                  <span className="text-xs font-bold">{s.verdict}</span>
                </div>
                {typeof s.vivantes_pct === "number" && (
                  <p className="text-xs text-slate-300 mt-1">{s.urls_testees} URL testées · {s.vivantes_pct}% vivantes{s.mortes ? ` · ${s.mortes} mortes` : ""}</p>
                )}
                {typeof s.frais === "number" && (
                  <p className="text-xs text-slate-300 mt-1">🟢 {s.frais} frais · 🟠 {s.a_reverifier} à revérifier · 🔴 {s.prioritaire} prioritaire{s.sources_modifiees ? ` · ${s.sources_modifiees} sources modifiées` : ""}</p>
                )}
                {typeof s.depuis_naissance === "number" && (
                  <p className="text-xs text-slate-300 mt-1">📈 +{s.depuis_naissance} réponses depuis la naissance · {s.battements_sans_croissance} battement(s) sans croissance</p>
                )}
                {typeof s.plan_pct === "number" && (
                  <p className="text-xs text-slate-300 mt-1">🎯 plan {s.plan_pct}% ({s.plan_faits}/{s.plan_total}) · prochaine étape : {s.prochaine_etape || "—"}</p>
                )}
                {typeof s.caelum_normes === "number" && (
                  <p className="text-xs text-slate-300 mt-1">🏢 {s.caelum_normes} normes · {s.caelum_sources} sources · {s.caelum_aides} aides publiques</p>
                )}
                {s.mitigation && <p className="text-xs text-slate-400 mt-1.5">🛡️ {s.mitigation}</p>}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Scénarios extrêmes (stress) */}
      {stress.length > 0 && (
        <section className="max-w-5xl mx-auto px-6 mt-10">
          <h2 className="text-xl font-bold">Scénarios extrêmes imaginés</h2>
          <p className="text-slate-400 text-sm mt-1">Stress-tests : ils mesurent la résistance, ils ne bloquent pas.</p>
          <div className="mt-4 grid sm:grid-cols-3 gap-3">
            {stress.map((s) => (
              <div key={s.scenario} className={`rounded-xl border bg-white/5 p-4 ${COULEUR[s.verdict] || "border-white/10"}`}>
                <span className="font-semibold text-sm text-slate-100">{s.scenario}</span>
                <p className="text-xs font-bold mt-1">{s.verdict}</p>
                {typeof s.p95_ms === "number" && <p className="text-xs text-slate-400 mt-1">p95 {s.p95_ms}ms · {s.pct_sous_200ms}% &lt;200ms</p>}
                {typeof s.pct_corpus === "number" && <p className="text-xs text-slate-400 mt-1">~{s.urls_impactees_moy} URLs ({s.pct_corpus}%)</p>}
                {typeof s.pages_estimees === "number" && <p className="text-xs text-slate-400 mt-1">{s.pages_estimees} pages</p>}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* À corriger (décisions humaines) */}
      {Array.isArray(sceau.alertes_etat_a_corriger) && (sceau.alertes_etat_a_corriger as string[]).length > 0 && (
        <section className="max-w-5xl mx-auto px-6 mt-10">
          <div className="rounded-2xl border border-amber-400/30 bg-amber-500/10 p-5">
            <h2 className="font-bold text-amber-200">⚠️ Ce qu&apos;il reste à décider (humain)</h2>
            <ul className="mt-2 list-disc list-inside text-sm text-amber-100/90">
              {(sceau.alertes_etat_a_corriger as string[]).map((a) => <li key={a}>{a}</li>)}
            </ul>
          </div>
        </section>
      )}

      {/* Autoguérison — soins proposés */}
      {Array.isArray(todo.taches) && todo.taches.length > 0 && (
        <section className="max-w-5xl mx-auto px-6 mt-10">
          <h2 className="text-xl font-bold">🩺 Soins proposés (autoguérison)</h2>
          <p className="text-slate-400 text-sm mt-1">
            La plateforme propose, l&apos;humain décide. {todo.par_priorite?.haute ?? 0} haute ·
            {" "}{todo.par_priorite?.moyenne ?? 0} moyenne · {todo.par_priorite?.basse ?? 0} basse.
          </p>
          <div className="mt-4 grid gap-3">
            {todo.taches.map((t) => {
              const c = t.priorite === "haute" ? "border-rose-400/40 bg-rose-500/10"
                : t.priorite === "moyenne" ? "border-amber-400/40 bg-amber-500/10" : "border-white/10 bg-white/5";
              return (
                <div key={t.id} className={`rounded-xl border p-4 ${c}`}>
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-semibold text-sm text-slate-100">{t.titre}</span>
                    <span className="text-[11px] whitespace-nowrap px-2 py-0.5 rounded-full bg-white/10 text-slate-200">
                      {t.priorite} · {t.humain ? "🧑 humain" : "🤖 auto"}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 mt-1.5">→ {t.action_suggeree}</p>
                  <p className="text-[11px] text-slate-500 mt-1">{t.categorie} · via {t.organe}</p>
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* Mémoire (dernières pulsations) */}
      {Array.isArray(vitals.historique) && vitals.historique.length > 0 && (
        <section className="max-w-5xl mx-auto px-6 mt-10 mb-16">
          <h2 className="text-xl font-bold">Mémoire — dernières pulsations</h2>
          <div className="mt-4 flex items-end gap-1 h-24">
            {vitals.historique.slice(-40).map((h, i) => (
              <div key={i} className="flex-1 bg-indigo-500/70 rounded-t" style={{ height: `${Math.max(4, h.resilience)}%` }} title={`${h.resilience}% · ${h.ts.slice(0, 16)}`} />
            ))}
          </div>
          <p className="text-xs text-slate-500 mt-2">Chaque barre = un battement (run). Hauteur = résilience.</p>
        </section>
      )}

      <footer className="border-t border-white/10 py-8 px-6 text-center text-xs text-slate-500">
        Organisme de supervision (métaphore assumée). Données : <code>autonomous_platform.py</code> ·
        {rapport.genere_le ? ` généré le ${rapport.genere_le.slice(0, 16)}` : ""} · simulations = modèles locaux.
      </footer>
    </main>
  );
}
