import Link from "next/link";
import fs from "node:fs";
import path from "node:path";
import BaseJuridiqueClient from "./BaseJuridiqueClient";

// Page "Base juridique vérifiée" — INDEX LÉGER + recherche (rendu statique).
// On ne charge PAS les 242 réponses complètes (trop lourd) : on passe un index compact
// (domaine + questions) ; les réponses complètes vivent sur /loi/[domaine] (rapides).

type FaitLeger = { id: string; question: string };
type ModuleLeger = { module: string; titre: string; faits: FaitLeger[] };

function chargerIndex(): ModuleLeger[] {
  const dir = path.join(process.cwd(), "data", "belgium");
  let fichiers: string[] = [];
  try {
    fichiers = fs.readdirSync(dir).filter((f) => f.endsWith(".json") && !f.startsWith("_"));
  } catch {
    return [];
  }
  const mods: ModuleLeger[] = [];
  for (const f of fichiers.sort()) {
    try {
      const d = JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8"));
      if (d && Array.isArray(d.faits) && d.faits.length) {
        mods.push({
          module: d.module,
          titre: d.titre,
          faits: d.faits.map((x: { id: string; question: string }) => ({ id: x.id, question: x.question })),
        });
      }
    } catch {
      /* ignore */
    }
  }
  return mods.sort((a, b) => (a.titre || "").localeCompare(b.titre || ""));
}

// Rendu statique : index figé au build → page légère servie instantanément, tient la charge.
export const dynamic = "force-static";

export const metadata = {
  title: "Base juridique vérifiée — La Loi Avec Moi",
  description:
    "Toutes nos réponses juridiques par domaine, chacune sourcée et datée. Recherchez votre question ou choisissez un domaine.",
};

export default function BaseJuridiquePage() {
  const index = chargerIndex();
  const totalFaits = index.reduce((n, m) => n + m.faits.length, 0);

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">
            ← Accueil
          </Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-blue-950 to-slate-900 text-white py-16 px-6">
        <div className="max-w-5xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold">Base juridique vérifiée</h1>
          <p className="mt-3 text-blue-100 max-w-2xl">
            {totalFaits} réponses sur {index.length} domaines — chacune sourcée et datée. Cherchez votre question
            ou choisissez un domaine.
          </p>
        </div>
      </section>

      <BaseJuridiqueClient index={index} />
    </main>
  );
}
