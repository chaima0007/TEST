import "dotenv/config";
import { anthropic } from "@ai-sdk/anthropic";
import { Composio } from "@composio/core";
import { VercelProvider } from "@composio/vercel";
import { stepCountIs, streamText } from "ai";

// ── Vérifications : les clés viennent de l'environnement, JAMAIS du code ──
if (!process.env.COMPOSIO_API_KEY) {
  console.error(
    "❌ COMPOSIO_API_KEY manquante. Copie .env.example en .env et colle ta clé Composio.",
  );
  process.exit(1);
}
if (!process.env.ANTHROPIC_API_KEY) {
  console.error(
    "❌ ANTHROPIC_API_KEY manquante (mets-la dans .env, ou en variable d'environnement système).",
  );
  process.exit(1);
}

const composio = new Composio({ provider: new VercelProvider() });

// Identifiant utilisateur Composio (configurable dans .env)
const userId = process.env.COMPOSIO_USER_ID ?? "retrouvetonsmile";

const session = await composio.create(userId);
const tools = await session.tools();

// Le prompt peut être passé en argument : `npm start -- "envoie un email à ..."`
const prompt =
  process.argv.slice(2).join(" ") ||
  "Star the composiohq/composio repo on GitHub";

const stream = await streamText({
  model: anthropic("claude-opus-4-8"), // modèle Claude à jour
  prompt,
  stopWhen: stepCountIs(10),
  tools,
});

for await (const textPart of stream.textStream) {
  process.stdout.write(textPart);
}
process.stdout.write("\n");
