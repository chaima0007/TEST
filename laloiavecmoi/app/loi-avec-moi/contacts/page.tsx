import Link from "next/link";
import fs from "node:fs";
import path from "node:path";

// Page « Qui contacter » — La Loi Avec Moi. Annuaire des services/numéros utiles, agrégé
// automatiquement depuis les contacts de la base vérifiée (data/belgium). Rendu statique.

type Contact = { nom?: string; numero?: string; lien?: string; pour?: string };

function aggregerContacts(): { nom: string; numero?: string; lien?: string; pour: string[] }[] {
  const dir = path.join(process.cwd(), "data", "belgium");
  const map = new Map<string, { nom: string; numero?: string; lien?: string; pour: Set<string> }>();
  try {
    for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".json") && !x.startsWith("_"))) {
      let d: { faits?: { contacts?: Contact[] }[] };
      try {
        d = JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8"));
      } catch {
        continue;
      }
      for (const fait of d.faits || []) {
        for (const c of fait.contacts || []) {
          if (!c.nom || (!c.numero && !c.lien)) continue; // garder l'actionnable (numéro ou lien)
          const key = (c.nom + "|" + (c.numero || c.lien || "")).toLowerCase();
          if (!map.has(key)) map.set(key, { nom: c.nom, numero: c.numero, lien: c.lien, pour: new Set() });
          if (c.pour) map.get(key)!.pour.add(c.pour);
        }
      }
    }
  } catch {
    /* ignore */
  }
  return Array.from(map.values())
    .map((c) => ({ ...c, pour: Array.from(c.pour).slice(0, 3) }))
    .sort((a, b) => a.nom.localeCompare(b.nom));
}

export const dynamic = "force-static";

export const metadata = {
  title: "Qui contacter — La Loi Avec Moi",
  description:
    "Annuaire des services et numéros utiles en Belgique : urgences, CPAS, police, lignes d'écoute, médiateurs, autorités.",
};

export default function ContactsPage() {
  const contacts = aggregerContacts();
  const avecNumero = contacts.filter((c) => c.numero);
  const autres = contacts.filter((c) => !c.numero);

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-4xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="font-bold text-lg tracking-tight">
            La Loi Avec Moi
          </Link>
          <Link href="/loi-avec-moi/urgences" className="text-sm font-semibold text-rose-600 hover:text-rose-800">
            Urgences & délais →
          </Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-blue-950 to-slate-900 text-white py-14 px-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold">Qui contacter</h1>
          <p className="mt-3 text-blue-100 max-w-2xl">
            {contacts.length} services et numéros utiles, rassemblés depuis nos réponses. En danger
            immédiat : <strong className="text-white">112</strong>.
          </p>
        </div>
      </section>

      <section className="max-w-4xl mx-auto px-6 py-12">
        <h2 className="text-2xl font-bold">📞 Avec un numéro direct</h2>
        <div className="mt-5 grid gap-3 sm:grid-cols-2">
          {avecNumero.map((c) => (
            <div key={c.nom + c.numero} className="rounded-xl border border-slate-200 p-4">
              <div className="font-semibold text-slate-900">{c.nom}</div>
              <a href={`tel:${(c.numero || "").replace(/\s/g, "")}`} className="text-indigo-700 font-bold">
                {c.numero}
              </a>
              {c.pour.length > 0 && <p className="text-xs text-slate-500 mt-1">{c.pour.join(" · ")}</p>}
            </div>
          ))}
        </div>

        <h2 className="text-2xl font-bold mt-12">🔗 Services & autorités (en ligne)</h2>
        <div className="mt-5 grid gap-3 sm:grid-cols-2">
          {autres.map((c) => (
            <div key={c.nom + (c.lien || "")} className="rounded-xl border border-slate-200 p-4">
              <div className="font-semibold text-slate-900">{c.nom}</div>
              {c.lien && (
                <a
                  href={c.lien}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-indigo-700 text-sm hover:underline break-all"
                >
                  {c.lien.replace(/^https?:\/\//, "")}
                </a>
              )}
              {c.pour.length > 0 && <p className="text-xs text-slate-500 mt-1">{c.pour.join(" · ")}</p>}
            </div>
          ))}
        </div>

        <p className="text-xs text-slate-400 mt-10 border-t border-slate-100 pt-4">
          Annuaire indicatif rassemblé depuis nos réponses sourcées. Pour une situation précise, vérifiez le
          service compétent. En danger immédiat : 112. © La Loi Avec Moi.
        </p>
      </section>
    </main>
  );
}
