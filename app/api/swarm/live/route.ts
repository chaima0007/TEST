import { NextRequest } from "next/server";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

// ── Agent event generator ─────────────────────────────────────────────────────

const DIVISION_AGENTS = [
  // Division 1
  { id: "1.0", div: 1, label: "Détecteur Manager",    divName: "Détection" },
  { id: "1.1", div: 1, label: "Spider Web",            divName: "Détection" },
  { id: "1.2", div: 1, label: "PageSpeed Analyzer",   divName: "Détection" },
  { id: "1.3", div: 1, label: "Données Entreprise",   divName: "Détection" },
  { id: "1.5", div: 1, label: "SEO Scanner",          divName: "Détection" },
  // Division 2
  { id: "2.0", div: 2, label: "Rédacteur Manager",    divName: "Rédaction" },
  { id: "2.1", div: 2, label: "Le Factuel",            divName: "Rédaction" },
  { id: "2.2", div: 2, label: "L'Amical",              divName: "Rédaction" },
  { id: "2.6", div: 2, label: "Paris & IDF",           divName: "Rédaction" },
  { id: "2.7", div: 2, label: "Secteur Premium",       divName: "Rédaction" },
  { id: "2.8", div: 2, label: "Artisans & TPE",        divName: "Rédaction" },
  // Division 3
  { id: "3.0", div: 3, label: "Négo Manager",          divName: "Négociation" },
  { id: "3.1", div: 3, label: "Gestionnaire Objections", divName: "Négociation" },
  { id: "3.5", div: 3, label: "Closer Rapide",         divName: "Négociation" },
  { id: "3.7", div: 3, label: "Relanceur J+4",         divName: "Négociation" },
  // Division 4
  { id: "4.0", div: 4, label: "Production Manager",   divName: "Production" },
  { id: "4.1", div: 4, label: "Dev Optimizer",         divName: "Production" },
  { id: "4.3", div: 4, label: "UX Enhancer",           divName: "Production" },
  // Division 5
  { id: "5.0", div: 5, label: "Finance Manager",       divName: "Finance" },
  { id: "5.2", div: 5, label: "RGPD Compliance",       divName: "Finance" },
  { id: "5.5", div: 5, label: "Stripe Ops",            divName: "Finance" },
  // Division 6
  { id: "6.0", div: 6, label: "Branding Manager",      divName: "Branding" },
  { id: "6.1", div: 6, label: "LinkedIn Writer",        divName: "Branding" },
  { id: "6.8", div: 6, label: "Editorial Calendar",    divName: "Branding" },
];

const DIV_COLORS: Record<number, string> = {
  1: "#6366f1",
  2: "#8b5cf6",
  3: "#ec4899",
  4: "#f59e0b",
  5: "#10b981",
  6: "#06b6d4",
};

const EVENT_TEMPLATES = [
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} a détecté ${Math.floor(Math.random() * 40 + 5)} nouveaux prospects`,
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} a rédigé un email (taux réponse estimé ${Math.floor(Math.random() * 20 + 15)}%)`,
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} a ouvert un thread de négociation`,
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} a validé la conformité RGPD d'un prospect`,
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} a généré un lien Stripe (${Math.floor(Math.random() * 600 + 200)}€)`,
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} a livré un package de production`,
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} a publié un post LinkedIn`,
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} a analysé le PageSpeed : score ${Math.floor(Math.random() * 40 + 20)}/100`,
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} a relancé un prospect fantôme (J+4)`,
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} a fermé une négociation avec succès`,
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} — Thompson Sampling sélectionné comme variante optimale`,
  (a: typeof DIVISION_AGENTS[0]) => `${a.label} a mis à jour le calendrier éditorial`,
];

const SEVERITIES = ["info", "info", "info", "success", "success", "warning"] as const;

function randomAgent() {
  return DIVISION_AGENTS[Math.floor(Math.random() * DIVISION_AGENTS.length)];
}

function generateEvent(seq: number) {
  const agent = randomAgent();
  const template = EVENT_TEMPLATES[Math.floor(Math.random() * EVENT_TEMPLATES.length)];
  const severity = SEVERITIES[Math.floor(Math.random() * SEVERITIES.length)];
  return {
    id: seq,
    type: "agent_event",
    timestamp: new Date().toISOString(),
    agent_id: agent.id,
    division: agent.div,
    division_name: agent.divName,
    color: DIV_COLORS[agent.div],
    severity,
    message: template(agent),
  };
}

// ── SSE Route ─────────────────────────────────────────────────────────────────

export async function GET(req: NextRequest) {
  const encoder = new TextEncoder();
  let seq = 0;

  const stream = new ReadableStream({
    start(controller) {
      const send = (data: unknown) => {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(data)}\n\n`));
      };

      // Burst 8 historical events on connect
      for (let i = 0; i < 8; i++) {
        send(generateEvent(seq++));
      }

      // Then send 1-2 events every ~3 seconds
      const interval = setInterval(() => {
        const count = Math.random() > 0.6 ? 2 : 1;
        for (let i = 0; i < count; i++) {
          send(generateEvent(seq++));
        }
      }, 3000);

      req.signal.addEventListener("abort", () => {
        clearInterval(interval);
        controller.close();
      });
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
    },
  });
}
