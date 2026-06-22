import type { Metadata } from "next";
import { Geist } from "next/font/google";
import { ToastProvider } from "@/components/Toast";
import { SpeedInsights } from "@vercel/speed-insights/next";
import "./globals.css";

const geist = Geist({ subsets: ["latin"], variable: "--font-geist-sans" });

export const metadata: Metadata = {
  title: "CompeteIQ — Intelligence Concurrentielle",
  description: "Suivez et analysez vos concurrents en temps réel",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" className={geist.variable}>
      <body className="min-h-screen bg-slate-50">
        <ToastProvider>{children}</ToastProvider>
        <SpeedInsights />
      </body>
    </html>
  );
}
