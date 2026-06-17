import { prisma } from "@/lib/prisma";

// Paramètres auto-ajustables du pipeline (boucle de rétroaction).
export const MIN_BUDGET_KEY = "minBudgetThreshold";
export const DEFAULT_MIN_BUDGET = 500;

export async function getMinBudgetThreshold(): Promise<number> {
  const row = await prisma.pipelineSetting.findUnique({ where: { key: MIN_BUDGET_KEY } });
  if (!row) return DEFAULT_MIN_BUDGET;
  const n = parseFloat(row.value);
  return Number.isNaN(n) ? DEFAULT_MIN_BUDGET : n;
}

export async function setMinBudgetThreshold(value: number): Promise<void> {
  await prisma.pipelineSetting.upsert({
    where: { key: MIN_BUDGET_KEY },
    create: { key: MIN_BUDGET_KEY, value: String(value) },
    update: { value: String(value) },
  });
}
