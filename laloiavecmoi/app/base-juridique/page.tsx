import Link from "next/link";
import fs from "node:fs";
import path from "node:path";
import BaseJuridiqueClient from "./BaseJuridiqueClient";

// Page "Base juridique vérifiée" — charge les réponses sourcées de data/belgium/*.json (serveur)
// et délègue l'affichage + la recherche/filtre au composant client.
// Source de vérité unique = la base vérifiée.

type Source = { type?: string; url?: string; intitule?: string };
type Contact = { nom?: string; numero?: string; lien?: string; pour?: string; dispo?: string };
type Fait = {
  id: string;
  question: string;
  reponse: string;
  reference_legale?: string;
  alerte_delai?: string;
  contacts?: Contact[];
  sources?: Source[];
  date_verification?: string;
};
type Module = { module: string; titre: string; domaine?: string; faits: Fait[] };

function chargerModules(): Module[] {
  const dir = path.join(process.cwd(), "data", "belgium");
  let fichiers: string[] = [];
  try {
    fichiers = fs.readdirSync(dir).filter((f) => f.endsWith(".json") && !f.startsWith("_"));
  } catch {
    return [];
  }
  const mods: Module[] = [];
  for (const f of fichiers.sort()) {
    try {
      const d = JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8"));
      if (d && Array.isArray(d.faits) && d.faits.length) mods.push(d);
    } catch {
      /* ignore fichier illisible */
    }
  }
  return mods.sort((a, b) => (a.titre || "").localeCompare(b.titre || ""));
}

export const metadata = {
  title: "Base juridique vérifiée — La Loi Avec Moi",
  description:
    "Toutes nos réponses juridiques, chacune avec sa source officielle, sa référence légale et sa date de vérification. Recherche et filtre par domaine.",
};

export default function BaseJuridiquePage() {
  const modules = chargerModules();
  const totalFaits = modules.reduce((n, m) => n + m.faits.length, 0);

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
            {totalFaits} réponses sur {modules.length} domaines — chacune avec sa source officielle,
            sa référence légale et sa date de vérification.
          </p>
        </div>
      </section>

      <BaseJuridiqueClient modules={modules} />
    </main>
  );
}
