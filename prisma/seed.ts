import { PrismaClient } from "../lib/generated/prisma/client";
import { PrismaLibSql } from "@prisma/adapter-libsql";
import bcrypt from "bcryptjs";

const adapter = new PrismaLibSql({ url: "file:./dev.db" });
const prisma = new PrismaClient({ adapter } as any);

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

  // ── Swarm seed data ────────────────────────────────────────────────────────
  console.log("Seeding swarm data...");

  const cycle = await prisma.swarmCycle.upsert({
    where: { cycleKey: "cycle_20260617_demo" },
    update: {},
    create: {
      cycleKey: "cycle_20260617_demo",
      startedAt: new Date("2026-06-17T06:00:00Z"),
      completedAt: new Date("2026-06-17T06:04:32Z"),
      prospectsFound: 847,
      emailsSent: 312,
      revenueEur: 2237,
      divisionStatuses: JSON.stringify({
        "1": "success", "2": "success", "3": "success", "4": "success", "5": "success",
      }),
    },
  });

  await prisma.swarmJob.deleteMany({ where: { cycleId: cycle.id } });
  await prisma.swarmJob.createMany({
    data: [
      { companyId: "rest_girard_001", companyName: "Restaurant Le Bouchon Lyonnais", sector: "Restauration", website: "https://bouchon-lyonnais.fr", stage: "paid", assignedAgent: "4.1", quoteEur: 149, paymentConfirmed: true, status: "success", cycleId: cycle.id },
      { companyId: "med_moreau_002", companyName: "Cabinet Dr. Moreau", sector: "Médical", website: "https://dr-moreau-paris.fr", stage: "paid", assignedAgent: "4.4", quoteEur: 189, paymentConfirmed: true, status: "success", cycleId: cycle.id },
      { companyId: "sport_elite_003", companyName: "Gymnase Sport Elite", sector: "Associations", website: "https://sport-elite-lyon.fr", stage: "paid", assignedAgent: "4.1", quoteEur: 129, paymentConfirmed: true, status: "success", cycleId: cycle.id },
      { companyId: "plomb_durand_004", companyName: "Plomberie Durand Frères", sector: "Artisans", website: "https://durand-plomberie.fr", stage: "negotiation", assignedAgent: "3.5", status: "running", cycleId: cycle.id },
      { companyId: "immo_cote_005", companyName: "Agence Immo Côte d'Azur", sector: "Immobilier", website: "https://immo-cotedazur.fr", stage: "outreach", assignedAgent: "2.2", status: "pending", cycleId: cycle.id },
      { companyId: "auto_marseille_006", companyName: "Auto École Marseille Centre", sector: "Formation", website: "https://autoecole-marseille.fr", stage: "negotiation", assignedAgent: "3.2", status: "running", cycleId: cycle.id },
      { companyId: "boulangerie_perrin_007", companyName: "Boulangerie Artisanale Perrin", sector: "Artisans", website: "https://perrin-boulangerie.fr", stage: "detection", assignedAgent: "1.1", status: "pending", cycleId: cycle.id },
      { companyId: "compta_petit_008", companyName: "Comptabilité Petit & Associés", sector: "Juridique", website: "https://petit-associes.fr", stage: "outreach", assignedAgent: "2.1", status: "pending", cycleId: cycle.id },
      { companyId: "garage_moto_009", companyName: "Garage Moto Azur", sector: "Garages", website: "https://moto-azur.fr", stage: "paid", assignedAgent: "4.1", quoteEur: 159, paymentConfirmed: true, status: "success", cycleId: cycle.id },
      { companyId: "cabinet_kine_010", companyName: "Cabinet Kinésithérapie Leblanc", sector: "Médical", website: "https://kine-leblanc.fr", stage: "outreach", assignedAgent: "2.3", status: "pending", cycleId: cycle.id },
    ],
  });

  await prisma.swarmTransaction.deleteMany({});
  await prisma.swarmTransaction.createMany({
    data: [
      { companyId: "rest_girard_001", companyName: "Restaurant Le Bouchon Lyonnais", sector: "Restauration", amountEur: 149, stripeChargeId: "ch_demo_001_girard" },
      { companyId: "med_moreau_002", companyName: "Cabinet Dr. Moreau", sector: "Médical", amountEur: 189, stripeChargeId: "ch_demo_002_moreau" },
      { companyId: "sport_elite_003", companyName: "Gymnase Sport Elite", sector: "Associations", amountEur: 129, stripeChargeId: "ch_demo_003_sport" },
      { companyId: "garage_moto_009", companyName: "Garage Moto Azur", sector: "Garages", amountEur: 159, stripeChargeId: "ch_demo_009_moto" },
    ],
  });

  await prisma.swarmProspect.deleteMany({});
  const sectorProspects = [
    { companyId: "art_001", name: "Électricité Bonneau", sector: "Artisans & Bâtiment", website: "https://electricite-bonneau.fr", pagespeedScore: 28, loadTimeMs: 6200, agentSource: "1.1" },
    { companyId: "rest_002", name: "Crêperie Bretonne Morvan", sector: "Restauration", website: "https://creperie-morvan.fr", pagespeedScore: 19, loadTimeMs: 8100, agentSource: "1.2" },
    { companyId: "med_003", name: "Cabinet Dentaire Rossi", sector: "Médical", website: "https://dentaire-rossi.fr", pagespeedScore: 35, loadTimeMs: 5400, agentSource: "1.3" },
    { companyId: "eco_004", name: "Boutique Bio Primeurs", sector: "E-commerce Local", website: "https://primeurs-bio.fr", pagespeedScore: 22, loadTimeMs: 7300, agentSource: "1.4" },
    { companyId: "immo_005", name: "Agence Immobilière Duval", sector: "Immobilier", website: "https://agence-duval.fr", pagespeedScore: 41, loadTimeMs: 4800, agentSource: "1.5" },
  ];
  for (const p of sectorProspects) {
    await prisma.swarmProspect.upsert({ where: { companyId: p.companyId }, update: {}, create: { ...p, mobileResponsive: false } });
  }

  console.log("Seeding complete!");
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
