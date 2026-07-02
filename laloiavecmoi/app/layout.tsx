import type { Metadata } from "next";
import { Fraunces, Public_Sans } from "next/font/google";
import "./globals.css";
import BarreAccessibilite from "@/components/BarreAccessibilite";

// Identité typographique « cabinet éditorial » :
// - Fraunces (serif à empattements, du caractère) pour les titres → autorité, confiance
// - Public Sans (humaniste, très lisible) pour le texte → clarté institutionnelle
const display = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
});
const sans = Public_Sans({ subsets: ["latin"], variable: "--font-sans-app" });

export const metadata: Metadata = {
  title: {
    default: "La Loi Avec Moi — Le droit accessible pour tous",
    template: "%s · La Loi Avec Moi",
  },
  description:
    "Comprenez vos droits en langage clair, gratuitement, à partir des sources officielles. Belgique (FR / NL) et France.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className={`${display.variable} ${sans.variable} antialiased`}>
        {children}
        <BarreAccessibilite />
      </body>
    </html>
  );
}
