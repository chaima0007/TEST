import type { Metadata } from "next";
import OutreachClient from "@/components/OutreachClient";

export const metadata: Metadata = {
  title: "Prospection — CompeteIQ",
  description:
    "Pipeline d'agents orchestrés pour contacter les entreprises sans site internet.",
};

export default function OutreachPage() {
  return <OutreachClient />;
}
