import type { Metadata } from "next";
import SosFloatingButton from "@/components/SosFloatingButton";

export const metadata: Metadata = {
  title: "La Loi Avec Moi — vos droits expliqués simplement",
  description:
    "Comprendre vos droits et obligations en Belgique, en langage clair et à partir des sources officielles. Gratuit. Lettres prêtes à envoyer, lecture vocale, accès rapide à vos droits.",
};

export default function LoiAvecMoiLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <SosFloatingButton />
    </>
  );
}
