import { NextRequest } from "next/server";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

function randomDelta(base: number, variance: number) {
  return Math.round(base + (Math.random() - 0.5) * variance);
}

export async function GET(req: NextRequest) {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    start(controller) {
      let revenue = 2237;
      let prospects = 847;
      let emails = 312;
      let negotiations = 28;

      const sendEvent = (data: unknown) => {
        const payload = `data: ${JSON.stringify(data)}\n\n`;
        controller.enqueue(encoder.encode(payload));
      };

      sendEvent({
        type: "connected",
        timestamp: new Date().toISOString(),
        message: "Flux temps réel connecté",
      });

      const interval = setInterval(() => {
        const delta = Math.random();
        if (delta > 0.7) {
          revenue += randomDelta(0, 40);
          prospects += randomDelta(2, 3);
        }
        if (delta > 0.5) {
          emails += randomDelta(1, 2);
        }
        if (delta > 0.85 && negotiations < 35) {
          negotiations += 1;
        }

        sendEvent({
          type: "tick",
          timestamp: new Date().toISOString(),
          revenue,
          prospects,
          emails,
          negotiations,
          agentsActive: randomDelta(42, 4),
        });
      }, 4000);

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
