import Link from "next/link";
import fs from "node:fs";
import path from "node:path";

// Fil « Actualités juridiques » — rendu statique depuis data/actualites.
// Items 100 % réels (veille officielle + mises à jour de fiches). Aucune
// actualité fabriquée ; l'enrichissement externe est déclaré honnêtement.

type Actu = {
  id: string;
  type: string;
  titre: string;
  domaine?: string;
  detail?: string;
  date?: string;
  regions?: string[];
  priorite?: string;
  statut?: string;
  lien_fiche?: string;
};

function charger(): { items: Actu[]; enrichissement: string; genere: string } {
  const file = path.join(process.cwd(), "data", "actualites", "actualites_juridiques.json");
  try {
    const d = JSON.parse(fs.readFileSync(file, "utf-8"));
    return {
      items: Array.isArray(d?.items) ? d.items : [],
      enrichissement: d?.enrichissement_externe || "",
      genere: d?.genere_le || "",
    };
  } catch {
    return { items: [], enrichissement: "", genere: "" };
  }
}

const STYLE: Record<string, { label: string; cls: string }> = {
  veille: { label: "Veille", cls: "bg-amber-50 text-amber-700" },
  a_reverifier: { label: "À revérifier", cls: "bg-rose-50 text-rose-700" },
  mise_a_jour_fiche: { label: "Mise à jour", cls: "bg-emerald-50 text-emerald-700" },
};

export const dynamic = "force-static";

export const metadata = {
  title: "Actualités juridiques — La Loi Avec Moi",
  description:
    "Les évolutions du droit belge qui vous concernent : signaux de veille officielle et mises à jour de nos fiches vérifiées.",
};

export default function Page() {
  const { items, enrichissement } = charger();
  const moduleDepuis = (lien?: string) => (lien || "").replace("/fiche/", "").replace("/loi/", "").split("#")[0];

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/loi-avec-moi/alertes" className="text-sm text-indigo-700 hover:text-indigo-900 font-medium">
            Suivre mes dossiers →
          </Link>
        </div>
      </header>

      <section className="max-w-4xl mx-auto px-6 pt-10 pb-4">
        <p className="text-sm font-semibold text-indigo-600 uppercase tracking-wide">Veille</p>
        <h1 className="mt-1 text-3xl sm:text-4xl font-bold tracking-tight">Actualités juridiques</h1>
        <p className="mt-3 max-w-2xl text-slate-600">
          Rester à la pointe : les changements de loi connus et attendus, et les fiches que nous
          venons de re-sourcer. Chaque information provient de sources officielles — nous
          n&apos;inventons aucune actualité.
        </p>
        {enrichissement && (
          <p className="mt-3 text-xs rounded-lg bg-slate-50 border border-slate-200 px-3 py-2 text-slate-500">
            Transparence : {enrichissement}
          </p>
        )}
      </section>

      <section className="max-w-4xl mx-auto px-6 pb-16">
        <ul className="space-y-3">
          {items.map((it) => {
            const s = STYLE[it.type] || { label: it.type, cls: "bg-slate-100 text-slate-600" };
            const mod = moduleDepuis(it.lien_fiche);
            const inner = (
              <>
                <div className="flex flex-wrap items-center gap-2">
                  <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${s.cls}`}>{s.label}</span>
                  {it.domaine && <span className="text-[11px] text-slate-500">{it.domaine}</span>}
                  {it.regions && it.regions.length > 0 && (
                    <span className="text-[11px] text-slate-500">{it.regions.join(" · ")}</span>
                  )}
                  {it.date && <span className="text-[11px] text-slate-400 ml-auto">{it.date}</span>}
                </div>
                <p className="mt-2 font-semibold text-slate-900">{it.titre}</p>
                {it.detail && <p className="mt-1 text-sm text-slate-600">{it.detail}</p>}
                {mod && (
                  <span className="mt-2 inline-block text-sm text-indigo-700 font-medium">Voir la fiche →</span>
                )}
              </>
            );
            return (
              <li key={it.id}>
                {mod ? (
                  <Link
                    href={`/loi/${mod}`}
                    className="block rounded-2xl border border-slate-200 p-4 hover:border-indigo-300 hover:bg-indigo-50/40 transition"
                  >
                    {inner}
                  </Link>
                ) : (
                  <div className="rounded-2xl border border-slate-200 p-4">{inner}</div>
                )}
              </li>
            );
          })}
        </ul>

        {items.length === 0 && (
          <p className="mt-10 text-center text-slate-500">
            Aucune actualité pour le moment. Revenez bientôt, ou{" "}
            <Link href="/loi-avec-moi/alertes" className="text-indigo-700 font-medium">
              activez le suivi de vos dossiers
            </Link>
            .
          </p>
        )}
      </section>
    </main>
  );
}
