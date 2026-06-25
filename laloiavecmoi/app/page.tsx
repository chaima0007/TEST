import Link from "next/link";

// Page d'accueil du site indépendant « La loi avec moi ».
// Aucune référence à Caelum : c'est l'entrée d'un site juridique autonome.
// Oriente vers les 3 éditions (Belgique FR, Belgique NL, France) + l'accueil multilingue.

const editions = [
  {
    href: "/loi-avec-moi",
    flag: "🇧🇪",
    titre: "Belgique — Français",
    desc: "Vos droits en Belgique, expliqués simplement.",
    accent: "from-blue-600 to-blue-800",
  },
  {
    href: "/de-wet-met-mij",
    flag: "🇧🇪",
    titre: "België — Nederlands",
    desc: "Uw rechten in België, eenvoudig uitgelegd.",
    accent: "from-emerald-600 to-emerald-800",
  },
  {
    href: "/la-loi-avec-moi-france",
    flag: "🇫🇷",
    titre: "France",
    desc: "Vos droits en France, expliqués simplement.",
    accent: "from-blue-700 to-indigo-800",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-blue-950 to-slate-900 text-white">
        <div
          className="absolute inset-0 opacity-40"
          style={{
            background:
              "radial-gradient(60% 60% at 50% 0%, rgba(30,58,138,0.45) 0%, rgba(15,23,42,0) 70%)",
          }}
        />
        <div className="relative max-w-3xl mx-auto px-6 py-24 text-center">
          {/* Logo */}
          <div className="flex justify-center mb-8">
            <img
              src="/logo-laloiavecmoi-mark.svg"
              alt="La loi avec moi"
              width={84}
              height={84}
            />
          </div>
          <h1 className="text-4xl sm:text-6xl font-bold tracking-tight leading-tight">
            La loi avec moi
          </h1>
          <p className="mt-4 text-lg sm:text-xl font-semibold tracking-wide text-blue-200">
            Le droit accessible pour tous.
          </p>
          <p className="mt-6 text-lg text-slate-300 leading-relaxed">
            Comprenez vos droits en langage clair, <strong className="text-white">gratuitement</strong>,
            à partir des sources officielles. Choisissez votre espace ci-dessous.
          </p>
          <div className="mt-8">
            <Link
              href="/loi-avec-moi/bienvenue"
              className="inline-flex items-center gap-2 bg-white text-blue-900 hover:bg-slate-100 font-semibold px-6 py-3.5 rounded-xl transition-colors shadow-lg"
            >
              🌍 Accueil multilingue — Welcome · مرحبا →
            </Link>
          </div>
        </div>
      </section>

      {/* Éditions */}
      <section className="px-6 py-16 max-w-5xl mx-auto">
        <h2 className="text-2xl font-bold tracking-tight text-center">Choisissez votre espace</h2>
        <p className="text-slate-500 text-center mt-3">
          Chaque espace est dédié à un pays et une langue — rien n&apos;est mélangé.
        </p>
        <div className="mt-10 grid sm:grid-cols-3 gap-6">
          {editions.map((e) => (
            <Link
              key={e.href}
              href={e.href}
              className="group rounded-2xl border border-slate-200 p-6 hover:shadow-lg hover:-translate-y-0.5 transition-all"
            >
              <div
                className={`w-12 h-12 rounded-xl bg-gradient-to-br ${e.accent} flex items-center justify-center text-2xl`}
              >
                {e.flag}
              </div>
              <h3 className="font-bold tracking-tight mt-4 group-hover:text-blue-700 transition-colors">
                {e.titre}
              </h3>
              <p className="text-slate-600 text-sm mt-1.5 leading-relaxed">{e.desc}</p>
              <span className="inline-block mt-3 text-sm font-semibold text-blue-700">
                Entrer →
              </span>
            </Link>
          ))}
        </div>
      </section>

      {/* Confiance */}
      <section className="px-6 pb-16 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6">
          <h2 className="font-semibold text-amber-900">⚖️ En toute transparence</h2>
          <p className="text-amber-800 text-sm mt-2 leading-relaxed">
            « La loi avec moi » fournit de l&apos;<strong>information et de l&apos;orientation</strong> pour
            comprendre vos droits — ce n&apos;est <strong>pas un conseil juridique personnalisé</strong>
            (réservé aux professionnels agréés). Pour une décision importante, nous vous orientons vers le bon
            expert. L&apos;objectif&nbsp;: de la clarté, gratuitement, en toute sécurité.
          </p>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <p>« La loi avec moi » — Le droit accessible pour tous.</p>
        <Link href="/contact" className="inline-block mt-3 text-blue-700 hover:text-blue-900 font-medium">
          Nous contacter
        </Link>
      </footer>
    </main>
  );
}
