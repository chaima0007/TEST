import { PrismaClient } from "../lib/generated/prisma/client";
import { PrismaLibSql } from "@prisma/adapter-libsql";

const adapter = new PrismaLibSql({ url: "file:./dev.db" });
const prisma = new PrismaClient({ adapter } as never);

// Profils freelance de démonstration pour alimenter le matching.
const profiles = [
  { name: "Alice Martin", skills: "Next.js, TypeScript, React, Prisma", seniority: "senior", minBudget: 8000, locations: "remote, Paris", bio: "Dev full-stack TS, 8 ans d'XP produit." },
  { name: "Karim Benali", skills: "Python, SQL, dbt", seniority: "senior", minBudget: 15000, locations: "remote", bio: "Data engineer, pipelines analytiques." },
  { name: "Léa Dubois", skills: "React, Tailwind, Design", seniority: "mid", minBudget: 2000, locations: "Paris, remote", bio: "Intégratrice front / UI." },
];

async function main() {
  for (const p of profiles) {
    const existing = await prisma.freelanceProfile.findFirst({ where: { name: p.name } });
    if (existing) {
      await prisma.freelanceProfile.update({ where: { id: existing.id }, data: p });
    } else {
      await prisma.freelanceProfile.create({ data: p });
    }
  }
  const count = await prisma.freelanceProfile.count();
  console.log(`✅ ${count} profil(s) freelance en base.`);
}

main()
  .catch((e) => { console.error(e); process.exit(1); })
  .finally(() => prisma.$disconnect());
