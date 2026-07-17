import type { Metadata, Viewport } from "next";
import { Geist } from "next/font/google";
import { BottomNav } from "@/components/BottomNav";
import "./globals.css";

const geist = Geist({ subsets: ["latin"], variable: "--font-geist-sans" });

export const metadata: Metadata = {
  title: "Nous — mieux se comprendre à deux",
  description:
    "Une petite app locale pour comprendre les limites de l'autre et mieux communiquer, jour après jour.",
  applicationName: "Nous",
};

export const viewport: Viewport = {
  themeColor: "#fbf6f2",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" className={geist.variable}>
      <body>
        <div className="shell">{children}</div>
        <BottomNav />
      </body>
    </html>
  );
}
