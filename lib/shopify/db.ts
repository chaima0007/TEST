import { PrismaClient } from "@/lib/generated/prisma/client";
import { PrismaLibSql } from "@prisma/adapter-libsql";

const globalForPrisma = globalThis as unknown as { shopifyPrisma?: PrismaClient };

export function prisma(): PrismaClient {
  if (!globalForPrisma.shopifyPrisma) {
    const adapter = new PrismaLibSql({ url: process.env.DATABASE_URL ?? "file:./dev.db" });
    globalForPrisma.shopifyPrisma = new PrismaClient({ adapter });
  }
  return globalForPrisma.shopifyPrisma;
}
