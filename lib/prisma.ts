import { PrismaClient } from "@/lib/generated/prisma/client";
import { PrismaLibSql } from "@prisma/adapter-libsql";

// Singleton partagé : en dev, Next recharge les modules à chaud et créerait
// sinon une nouvelle connexion à chaque requête. On le mémorise sur globalThis.
const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };

const adapter = new PrismaLibSql({ url: process.env.DATABASE_URL ?? "file:./dev.db" });

export const prisma =
  globalForPrisma.prisma ?? new PrismaClient({ adapter } as never);

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}
