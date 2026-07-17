import Link from "next/link";
import fs from "node:fs";
import path from "node:path";
import CommunauteClient from "./CommunauteClient";

// Section « Questions de la communauté » — index public navigable des questions
// juridiques (issues du corpus officiel vérifié). Rendu statique : on passe un
// index compact au client (recherche + filtre par catégorie). Réponse complète
// sur la fiche liée (/loi/[module]#id).

type QPub = {
  id: string;
  question: string;
  domaine: string;
  module: string;
  reponse_resume: string;
  lien_module: string;
  fait_id: string;
};

function chargerQuestions(): QPub[] {
  const file = path.join(process.cwd(), "data", "community", "questions_publiques.json");
  try {
    const d = JSON.parse(fs.readFileSync(file, "utf-8"));
    const arr = Array.isArray(d?.questions) ? d.questions : [];
    return arr.map((q: Record<string, string>) => ({
      id: q.id,
      question: q.question,
      domaine: q.domaine || "Autres",
      module: q.module,
      reponse_resume: q.reponse_resume || "",
      lien_module: q.module,
      fait_id: (q.lien_fiche || "").split("#")[1] || "",
    }));
  } catch {
    return [];
  }
}

export const dynamic = "force-static";

export const metadata = {
  title: "Questions de la communauté — La Loi Avec Moi",
  description:
    "Parcourez les questions juridiques les plus fréquentes des citoyens en Belgique, chacune liée à une réponse sourcée et vérifiée.",
};

export default function Page() {
  const questions = chargerQuestions();

  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="flex items-center gap-2.5">
            <img src="/logo-laloiavecmoi-mark.svg" alt="" className="w-9 h-9" />
            <span className="font-bold text-lg tracking-tight">La Loi Avec Moi</span>
          </Link>
          <Link href="/base-juridique" className="text-sm text-indigo-700 hover:text-indigo-900 font-medium">
            Base juridique →
          </Link>
        </div>
      </header>

      <section className="max-w-5xl mx-auto px-6 pt-10 pb-2">
        <p className="text-sm font-semibold text-indigo-600 uppercase tracking-wide">Communauté</p>
        <h1 className="mt-1 text-3xl sm:text-4xl font-bold tracking-tight">Questions de la communauté</h1>
        <p className="mt-3 max-w-2xl text-slate-600">
          Les interrogations juridiques que se posent les citoyens, regroupées et accessibles à
          tous. Chaque question renvoie vers une réponse claire, sourcée officiellement et datée.
          Vous n&apos;êtes pas seul·e à vous poser ces questions.
        </p>
        <p className="mt-2 text-xs text-slate-400">
          {questions.length} questions publiques · issues de la base vérifiée · aucune donnée personnelle.
        </p>
      </section>

      <CommunauteClient questions={questions} />
    </main>
  );
}
