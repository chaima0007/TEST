import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geist = Geist({ subsets: ["latin"], variable: "--font-geist-sans" });

export const metadata: Metadata = {
  title: "La loi avec moi — Le droit accessible pour tous",
  description:
    "Comprenez vos droits en langage clair, gratuitement, à partir des sources officielles. Belgique (FR / NL) et France.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className={`${geist.variable} antialiased`}>{children}</body>
    </html>
  );
}
