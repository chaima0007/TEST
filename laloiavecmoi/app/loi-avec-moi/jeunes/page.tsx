import Link from "next/link";
import QuickExit from "@/components/QuickExit";

// Espace enfants & jeunes — La Loi Avec Moi. Langage très simple, ton rassurant, gros repères.
// Relie vers les pages/sujets existants. Numéros d'aide vérifiés (103, 112, 1712).
// Bouton « Quitter vite » : un·e jeune surpris·e en train de chercher de l'aide sort en 1 clic.

export const metadata = {
  title: "Espace enfants & jeunes — La Loi Avec Moi",
  description:
    "Tes droits expliqués simplement. Si tu as peur ou un souci, tu n'es pas seul·e : il y a toujours quelqu'un à qui en parler.",
};

const numeros = [
  { n: "103", t: "Écoute-Enfants", d: "Pour parler de tout, gratuitement et anonymement." },
  { n: "112", t: "Urgence", d: "Si tu es en danger tout de suite (police, pompiers, ambulance)." },
  { n: "1712", t: "Violences", d: "Si quelqu'un te fait du mal ou te fait peur." },
];

const cartes = [
  { emoji: "🆘", t: "Je suis en danger", d: "Quoi faire, tout de suite, si ça ne va pas du tout.", href: "/loi-avec-moi/en-danger", couleur: "border-rose-200" },
  { emoji: "🛡️", t: "Le harcèlement", d: "Si on t'embête, en vrai ou sur internet. Tu as le droit d'être protégé·e.", href: "/loi/harcelement_violences", couleur: "border-amber-200" },
  { emoji: "🏠", t: "Si tu es placé·e", d: "Tes droits, et comment te faire entendre.", href: "/loi-avec-moi/enfants-places", couleur: "border-emerald-200" },
  { emoji: "🚭", t: "La drogue, parlons-en", d: "Pour comprendre, sans jugement.", href: "/loi/drogues_prevention", couleur: "border-sky-200" },
  { emoji: "👪", t: "Ta famille", d: "Tes droits dans ta famille, et qui peut t'aider.", href: "/loi-avec-moi/famille", couleur: "border-indigo-200" },
  { emoji: "💼", t: "Ton premier job", d: "Job étudiant : ce que tu peux faire et tes droits.", href: "/loi/job_etudiant", couleur: "border-violet-200" },
  { emoji: "🧠", t: "Le quiz des droits", d: "Teste-toi en t'amusant — et découvre les vraies lois derrière tes droits.", href: "/loi-avec-moi/quiz", couleur: "border-fuchsia-200" },
  { emoji: "📜", t: "Les vrais textes de loi", d: "La Constitution et les grandes lois, en version originale. Oui, tu peux les lire !", href: "/loi-avec-moi/textes-de-loi", couleur: "border-yellow-200" },
];

export default function EspaceJeunesPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <header className="border-b border-slate-100">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link href="/loi-avec-moi" className="font-bold text-lg tracking-tight">
            La Loi Avec Moi
          </Link>
          <Link href="/loi-avec-moi" className="text-sm font-semibold text-indigo-700 hover:text-indigo-900">
            ← Accueil
          </Link>
        </div>
      </header>

      <section className="bg-gradient-to-b from-indigo-600 to-indigo-800 text-white py-16 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <div className="text-5xl mb-4">🌟</div>
          <h1 className="text-3xl md:text-4xl font-bold">Tes droits, expliqués simplement</h1>
          <p className="mt-4 text-indigo-100 text-lg leading-relaxed">
            Si tu as peur, un souci, ou juste une question : tu n&apos;es pas seul·e.
            Il y a toujours quelqu&apos;un à qui en parler. Et personne n&apos;a le droit de te faire du mal.
          </p>
        </div>
      </section>

      {/* Numéros d'aide */}
      <section className="max-w-3xl mx-auto px-6 -mt-8">
        <div className="grid sm:grid-cols-3 gap-4">
          {numeros.map((x) => (
            <div key={x.n} className="rounded-2xl bg-white border-2 border-rose-200 p-5 text-center shadow-sm">
              <div className="text-3xl font-black text-rose-600">{x.n}</div>
              <div className="font-bold mt-1">{x.t}</div>
              <p className="text-sm text-slate-600 mt-1">{x.d}</p>
            </div>
          ))}
        </div>
        <p className="text-center text-xs text-slate-400 mt-3">
          Tous ces numéros sont gratuits. Tu peux appeler même si tu hésites.
        </p>
      </section>

      {/* Cartes sujets */}
      <section className="max-w-5xl mx-auto px-6 py-14">
        <h2 className="text-2xl font-bold text-center mb-8">De quoi veux-tu parler ?</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5 stagger">
          {cartes.map((c) => (
            <Link
              key={c.t}
              href={c.href}
              className={`group rounded-2xl border-2 ${c.couleur} p-7 hover:shadow-lg hover:-translate-y-1 transition-all`}
            >
              <div className="text-4xl">{c.emoji}</div>
              <h3 className="font-bold text-lg mt-3 group-hover:text-indigo-700">{c.t}</h3>
              <p className="text-sm text-slate-600 mt-1 leading-relaxed">{c.d}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* Rappel doux */}
      <section className="max-w-3xl mx-auto px-6 pb-8">
        <div className="rounded-2xl bg-indigo-50 border border-indigo-100 p-7 text-center">
          <p className="text-slate-700 leading-relaxed">
            💛 Demander de l&apos;aide, ce n&apos;est pas être faible. C&apos;est être courageux·se.
            Tu as le droit d&apos;être écouté·e, protégé·e et respecté·e.
          </p>
        </div>
      </section>

      {/* Coin des parents */}
      <section className="max-w-3xl mx-auto px-6 pb-16">
        <div className="rounded-2xl border border-slate-200 p-6">
          <p className="text-sm font-semibold text-slate-800">👨‍👩‍👧 Pour les parents</p>
          <p className="mt-1 text-sm text-slate-600 leading-relaxed">
            Votre enfant est harcelé ? Des courriers prêts à remplir existent : signalement à
            l&apos;école, cyberharcèlement, harcèlement au travail.{" "}
            <Link href="/lettres" className="text-indigo-700 font-semibold hover:text-indigo-900">
              Générer un courrier →
            </Link>
          </p>
        </div>
      </section>

      <QuickExit />
    </main>
  );
}
