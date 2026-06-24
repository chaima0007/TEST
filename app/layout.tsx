import type { Metadata } from "next";
import { Geist } from "next/font/google";
import { ToastProvider } from "@/components/Toast";
import { SpeedInsights } from "@vercel/speed-insights/next";
import ChatWidget from "@/components/ChatWidget";
import "./globals.css";

const geist = Geist({ subsets: ["latin"], variable: "--font-geist-sans" });

export const metadata: Metadata = {
  title: "Caelum — Studio web & data",
  description: "Sites web, tableaux de bord et automatisations sur-mesure pour les PME et indépendants. Conçus avec soin, livrés rapidement.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" className={geist.variable}>
      <body className="min-h-screen bg-slate-50">
        <ToastProvider>{children}</ToastProvider>
        <ChatWidget />
        <SpeedInsights />
      </body>
    </html>
  );
}
