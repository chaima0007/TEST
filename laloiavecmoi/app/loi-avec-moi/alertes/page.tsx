import Link from "next/link";
import fs from "node:fs";
import path from "node:path";
import AlertesClient from "./AlertesClient";

// Page « Suivre mes dossiers » — suivi personnalisé.
// Choix des domaines suivis stocké LOCALEMENT (navigateur, localStorage) : aucune
// donnée personnelle envoyée, aucun compte requis. L'envoi e-mail/push (webhook)
// est une évolution réservée à une décision de la fondatrice.

type Actu = { id: string; titre: string; domaine?: string; detail?: string; date?: string; type: string; lien_fiche?: string };

function chargerActus(): Actu[] {
  const file = path.join(process.cwd(), "data", "actualites", "actualites_juridiques.json");
  try {
    const d = JSON.parse(fs.readFileSync(file, "utf-8"));
    return Array.isArray(d?.items) ? d.items : [];
  } catch {
    return [];
  }
}

function chargerDomaines(): string[] {
  const file = path.join(process.cwd(), "data", "community", "questions_publiques.json");
  try {
    const d = JSON.parse(fs.readFileSync(file, "utf-8"));
    const cats = d?.categories || {};
    return Object.keys(cats).filter((k) => k && k !== "Autres").sort();
  } catch {
    return [];
  }
}

export const dynamic = "force-static";

export const metadata = {
  title: "Suivre mes dossiers — La Loi Avec Moi",
  description:
    "Choisissez les domaines juridiques qui vous concernent et gardez un œil sur leurs évolutions. Suivi privé, sans compte ni donnée personnelle.",
};

export default function Page() {
  const actus = chargerActus();
  const domaines = chargerDomaines();

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-3xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/loi-avec-moi/actualites" className="text-sm text-indigo-700 hover:text-indigo-900 font-medium">
            Toutes les actualités →
          </Link>
        </div>
      </header>

      <section className="max-w-3xl mx-auto px-6 pt-10 pb-4">
        <p className="text-sm font-semibold text-indigo-600 uppercase tracking-wide">Suivi personnalisé</p>
        <h1 className="mt-1 text-3xl sm:text-4xl font-bold tracking-tight">Suivre mes dossiers</h1>
        <p className="mt-3 max-w-2xl text-slate-600">
          Cochez les domaines qui vous concernent : vous verrez en priorité leurs évolutions.
          Votre sélection reste <strong>privée sur votre appareil</strong> — pas de compte, pas
          d&apos;e-mail demandé, aucune donnée personnelle envoyée.
        </p>
      </section>

      <AlertesClient domaines={domaines} actus={actus} />
    </main>
  );
}
