import { prisma } from "@/lib/prisma";

const DEMO_USER_EMAIL = "demo@competeiq.com";

export async function getDemoUser() {
  const user = await prisma.user.findUnique({ where: { email: DEMO_USER_EMAIL } });
  return user;
}

export async function requireDemoUser() {
  const user = await getDemoUser();
  if (!user) throw new Error("User not found");
  return user;
}
