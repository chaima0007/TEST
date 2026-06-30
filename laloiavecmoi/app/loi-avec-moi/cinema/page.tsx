import Link from "next/link";

// Page « cinéma » — easter-egg promotionnel (bande-annonce façon film catastrophe).
// VOLONTAIREMENT séparée : non liée à la navigation, noindex, pour ne pas perturber
// l'expérience rassurante du vrai site. La bande-annonce est un asset statique autonome
// (public/cinema.html) embarqué en iframe pour isoler totalement son CSS/JS de l'app.

export const metadata = {
  title: "Bande-annonce — La Loi Avec Moi",
  description: "Page promotionnelle (easter-egg). Le vrai site reste calme et rassurant.",
  robots: { index: false, follow: false },
};

export default function CinemaPage() {
  return (
    <main className="min-h-screen bg-black">
      <iframe
        src="/cinema.html"
        title="Bande-annonce La Loi Avec Moi"
        className="w-screen border-0"
        style={{ height: "100vh", display: "block" }}
      />
      <div className="fixed top-3 left-3 z-50">
        <Link
          href="/loi-avec-moi"
          className="inline-flex items-center gap-1 rounded-full bg-black/50 px-3 py-1.5 text-sm text-white backdrop-blur hover:bg-black/70"
        >
          ← Retour au site
        </Link>
      </div>
    </main>
  );
}
