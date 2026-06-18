import { defineConfig } from "vitest/config";
import { resolve } from "node:path";

export default defineConfig({
  resolve: {
    alias: { "@": resolve(__dirname, ".") },
  },
  test: {
    // Les tests ne ciblent que la logique pure (analyzer, matcher) — pas de DB.
    include: ["lib/**/__tests__/**/*.test.ts"],
    environment: "node",
  },
});
