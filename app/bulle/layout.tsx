import type { Metadata } from "next";
import "./bulle.css";

export const metadata: Metadata = {
  title: "Bulle — parler ensemble, parents & enfants",
  description:
    "Une bulle douce pour aider parents et enfants à nommer leurs émotions et à désamorcer les conflits. Sans surveillance, sans pub, sans collecte de données.",
};

export default function BulleLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="bulle">
      <div className="mx-auto max-w-4xl px-4 py-6 sm:py-10">{children}</div>
    </div>
  );
}
