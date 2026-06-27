import type { Metadata } from "next";
import SosFloatingButtonFR from "@/components/SosFloatingButtonFR";

export const metadata: Metadata = {
  title: "La Loi Avec Moi — France · vos droits expliqués simplement",
  description:
    "Comprendre vos droits et obligations en France, simplement et avec des sources officielles. Un espace clair, séparé du site belge.",
};

export default function LoiAvecMoiFranceLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <SosFloatingButtonFR />
    </>
  );
}
