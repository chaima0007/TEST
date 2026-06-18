import { PrismaClient } from "../lib/generated/prisma/client";
import { PrismaLibSql } from "@prisma/adapter-libsql";
import bcrypt from "bcryptjs";

const adapter = new PrismaLibSql({ url: "file:./dev.db" });
const prisma = new PrismaClient({ adapter } as never);

const competitorData = [
  {
    name: "Salesforce",
    website: "salesforce.com",
    industry: "CRM",
    description: "Leader mondial du CRM cloud, offrant une suite complète d'outils de vente et de service client.",
    threatLevel: "high",
    logo: "SF",
    color: "#00A1E0",
    founded: 1999,
    employees: "70 000+",
    revenue: "31,4 Md$",
    marketShare: 23.8,
    lastUpdated: "2026-06-15",
    pricing: [
      { name: "Starter", price: 25, features: "Contact Management, Email Integration, Mobile App" },
      { name: "Professional", price: 80, features: "Collaboration Tools, API Access, Forecasting" },
      { name: "Enterprise", price: 165, features: "Advanced Analytics, Custom Workflows, AI Features" },
      { name: "Unlimited", price: 330, features: "Unlimited Customization, Premier Support" },
    ],
    features: [
      { name: "Intelligence Artificielle (Einstein)", available: true, quality: "Excellent" },
      { name: "Automatisation des ventes", available: true, quality: "Excellent" },
      { name: "Intégration email", available: true, quality: "Bien" },
      { name: "Rapports avancés", available: true, quality: "Excellent" },
      { name: "Application mobile", available: true, quality: "Bien" },
      { name: "API ouverte", available: true, quality: "Excellent" },
    ],
    news: [
      { date: "2026-06-10", title: "Salesforce lance Einstein Copilot v3", type: "product" },
      { date: "2026-05-20", title: "Augmentation des prix de 12%", type: "pricing" },
    ],
  },
  {
    name: "HubSpot",
    website: "hubspot.com",
    industry: "CRM / Marketing",
    description: "Plateforme inbound marketing et CRM populaire auprès des PME.",
    threatLevel: "high",
    logo: "HS",
    color: "#FF7A59",
    founded: 2006,
    employees: "7 000+",
    revenue: "2,2 Md$",
    marketShare: 8.4,
    lastUpdated: "2026-06-14",
    pricing: [
      { name: "Gratuit", price: 0, features: "CRM de base, Email limité, Formulaires" },
      { name: "Starter", price: 20, features: "Email Marketing, Live Chat" },
      { name: "Professional", price: 890, features: "Automation avancée, Reporting" },
      { name: "Enterprise", price: 3600, features: "Teams, Custom Objects" },
    ],
    features: [
      { name: "Intelligence Artificielle", available: true, quality: "Bien" },
      { name: "Automatisation marketing", available: true, quality: "Excellent" },
      { name: "Intégration email", available: true, quality: "Excellent" },
      { name: "Rapports avancés", available: true, quality: "Bien" },
      { name: "Application mobile", available: true, quality: "Bien" },
      { name: "API ouverte", available: true, quality: "Bien" },
    ],
    news: [
      { date: "2026-06-05", title: "HubSpot AI intègre GPT-5", type: "product" },
    ],
  },
  {
    name: "Pipedrive",
    website: "pipedrive.com",
    industry: "CRM Ventes",
    description: "CRM orienté ventes conçu pour les équipes commerciales, avec une interface visuelle de pipeline.",
    threatLevel: "medium",
    logo: "PD",
    color: "#2C3E50",
    founded: 2010,
    employees: "900+",
    revenue: "100 M$",
    marketShare: 3.1,
    lastUpdated: "2026-06-12",
    pricing: [
      { name: "Essential", price: 15, features: "Pipeline Management, Import/Export, API Access" },
      { name: "Advanced", price: 29, features: "Email Sync, Automations" },
      { name: "Professional", price: 59, features: "Revenue Forecasting, AI Insights" },
      { name: "Power", price: 69, features: "Project Planning, Phone Support" },
    ],
    features: [
      { name: "Intelligence Artificielle", available: true, quality: "Moyen" },
      { name: "Automatisation des ventes", available: true, quality: "Bien" },
      { name: "Intégration email", available: true, quality: "Bien" },
      { name: "Rapports avancés", available: false, quality: "-" },
      { name: "Application mobile", available: true, quality: "Excellent" },
      { name: "API ouverte", available: true, quality: "Bien" },
    ],
    news: [
      { date: "2026-05-30", title: "Pipedrive lance AI Sales Assistant", type: "product" },
    ],
  },
  {
    name: "Zoho CRM",
    website: "zoho.com",
    industry: "CRM Suite",
    description: "Suite complète d'applications business avec CRM intégré, solution économique pour les PME.",
    threatLevel: "medium",
    logo: "ZO",
    color: "#E42527",
    founded: 1996,
    employees: "15 000+",
    revenue: "1 Md$",
    marketShare: 4.2,
    lastUpdated: "2026-06-10",
    pricing: [
      { name: "Gratuit", price: 0, features: "3 utilisateurs, Leads, Contacts" },
      { name: "Standard", price: 14, features: "Scoring, Workflows, Campagnes" },
      { name: "Professional", price: 23, features: "Inventory, Validation Rules" },
      { name: "Enterprise", price: 40, features: "AI (Zia), Custom Modules, Multi-currency" },
    ],
    features: [
      { name: "Intelligence Artificielle (Zia)", available: true, quality: "Bien" },
      { name: "Automatisation des ventes", available: true, quality: "Bien" },
      { name: "Intégration email", available: true, quality: "Moyen" },
      { name: "Rapports avancés", available: true, quality: "Bien" },
      { name: "Application mobile", available: true, quality: "Moyen" },
      { name: "API ouverte", available: true, quality: "Bien" },
    ],
    news: [
      { date: "2026-06-01", title: "Zoho One intègre 55 nouvelles applications", type: "product" },
    ],
  },
  {
    name: "Monday.com",
    website: "monday.com",
    industry: "Gestion de projet / CRM",
    description: "Plateforme de gestion du travail avec capacités CRM.",
    threatLevel: "low",
    logo: "MN",
    color: "#F6517C",
    founded: 2012,
    employees: "1 800+",
    revenue: "729 M$",
    marketShare: 2.9,
    lastUpdated: "2026-06-08",
    pricing: [
      { name: "Individuel", price: 0, features: "2 sièges, Tableaux de bord, 200 items" },
      { name: "Basic", price: 9, features: "Items illimités, 5 Go stockage" },
      { name: "Standard", price: 12, features: "Timeline, Intégrations" },
      { name: "Pro", price: 19, features: "Automatisations, Formules" },
    ],
    features: [
      { name: "Intelligence Artificielle", available: true, quality: "Moyen" },
      { name: "Automatisation des ventes", available: false, quality: "-" },
      { name: "Intégration email", available: true, quality: "Moyen" },
      { name: "Rapports avancés", available: true, quality: "Moyen" },
      { name: "Application mobile", available: true, quality: "Bien" },
      { name: "API ouverte", available: true, quality: "Bien" },
    ],
    news: [
      { date: "2026-05-18", title: "Monday AI automatise la création de tasks", type: "product" },
    ],
  },
];

async function main() {
  console.log("Seeding database...");

  const hashedPassword = await bcrypt.hash("demo123", 10);
  const user = await prisma.user.upsert({
    where: { email: "demo@competeiq.com" },
    update: {},
    create: {
      email: "demo@competeiq.com",
      name: "Demo User",
      password: hashedPassword,
      company: "CompeteIQ Inc.",
    },
  });

  await prisma.competitor.deleteMany({ where: { userId: user.id } });

  for (const c of competitorData) {
    const { pricing, features, news, ...rest } = c;
    const competitor = await prisma.competitor.create({
      data: {
        ...rest,
        userId: user.id,
        pricingPlans: { create: pricing.map((p) => ({ ...p, currency: "€", interval: "mois" })) },
        features: { create: features },
        news: { create: news },
      },
    });
    console.log(`Created: ${competitor.name}`);
  }

  await prisma.alert.deleteMany({ where: { userId: user.id } });
  await prisma.alert.createMany({
    data: [
      { type: "pricing", message: "Salesforce augmente ses prix de 12%", isRead: false, userId: user.id },
      { type: "feature", message: "HubSpot lance une nouvelle fonctionnalité IA", isRead: false, userId: user.id },
      { type: "acquisition", message: "Salesforce acquiert DataRobot pour 1,2 Md$", isRead: false, userId: user.id },
      { type: "product", message: "Pipedrive lance AI Sales Assistant en bêta", isRead: true, userId: user.id },
    ],
  });

  await prisma.report.deleteMany({ where: { userId: user.id } });
  await prisma.report.createMany({
    data: [
      { title: "Analyse concurrentielle Q2 2026", description: "Vue d'ensemble du paysage CRM.", pages: 24, userId: user.id },
      { title: "Comparaison des prix — Juin 2026", description: "Analyse des stratégies de tarification.", pages: 12, userId: user.id },
      { title: "Rapport de fonctionnalités IA", description: "Comparaison des capacités IA des CRM.", pages: 18, userId: user.id },
    ],
  });

  console.log("Seeding complete!");
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
