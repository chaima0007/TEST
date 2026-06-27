import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

type InvoiceStatus = "draft" | "sent" | "partially_paid" | "paid" | "overdue" | "cancelled";
type PaymentMethod = "stripe" | "bank_transfer" | "cheque" | "cash" | "other";

interface Payment {
  payment_id: string;
  amount: number;
  method: PaymentMethod;
  received_at: string;
  reference: string;
}

interface Invoice {
  invoice_id: string;
  prospect_id: string;
  company_name: string;
  sector: string;
  amount_ht: number;
  tva_pct: number;
  amount_ttc: number;
  tva_amount: number;
  amount_paid: number;
  amount_remaining: number;
  status: InvoiceStatus;
  due_days: number;
  created_at: string;
  sent_at: string | null;
  due_at: string | null;
  paid_at: string | null;
  cancelled_at: string | null;
  notes: string;
  payments: Payment[];
}

interface Summary {
  total: number;
  draft: number;
  sent: number;
  partially_paid: number;
  paid: number;
  overdue: number;
  cancelled: number;
  total_invoiced_ttc: number;
  total_collected_ttc: number;
  total_outstanding_ttc: number;
  total_overdue_ttc: number;
  collection_rate_pct: number;
  avg_days_to_pay: number | null;
}

interface Data {
  source: string;
  invoices: Invoice[];
  summary: Summary;
}

function daysAgo(d: number): string {
  const dt = new Date();
  dt.setDate(dt.getDate() - d);
  return dt.toISOString();
}

function daysFromNow(d: number): string {
  const dt = new Date();
  dt.setDate(dt.getDate() + d);
  return dt.toISOString();
}

function buildMockData(): Data {
  const invoices: Invoice[] = [
    {
      invoice_id: "INV-0001",
      prospect_id: "p001",
      company_name: "Plomberie Martin SARL",
      sector: "artisan",
      amount_ht: 465.67,
      tva_pct: 20,
      amount_ttc: 558.80,
      tva_amount: 93.13,
      amount_paid: 558.80,
      amount_remaining: 0,
      status: "paid",
      due_days: 30,
      created_at: daysAgo(20),
      sent_at: daysAgo(19),
      due_at: daysAgo(-11),
      paid_at: daysAgo(15),
      cancelled_at: null,
      notes: "",
      payments: [
        { payment_id: "PAY-00001", amount: 558.80, method: "stripe", received_at: daysAgo(15), reference: "ch_3NxABCD" },
      ],
    },
    {
      invoice_id: "INV-0002",
      prospect_id: "p005",
      company_name: "Immo Prestige",
      sector: "immobilier",
      amount_ht: 765.67,
      tva_pct: 20,
      amount_ttc: 918.80,
      tva_amount: 153.13,
      amount_paid: 918.80,
      amount_remaining: 0,
      status: "paid",
      due_days: 30,
      created_at: daysAgo(24),
      sent_at: daysAgo(23),
      due_at: daysAgo(7),
      paid_at: daysAgo(10),
      cancelled_at: null,
      notes: "Paiement virement bancaire",
      payments: [
        { payment_id: "PAY-00002", amount: 918.80, method: "bank_transfer", received_at: daysAgo(10), reference: "VIR-20240605" },
      ],
    },
    {
      invoice_id: "INV-0003",
      prospect_id: "p008",
      company_name: "Salon Élite",
      sector: "beauté",
      amount_ht: 299.00,
      tva_pct: 20,
      amount_ttc: 358.80,
      tva_amount: 59.80,
      amount_paid: 358.80,
      amount_remaining: 0,
      status: "paid",
      due_days: 15,
      created_at: daysAgo(16),
      sent_at: daysAgo(15),
      due_at: daysAgo(0),
      paid_at: daysAgo(12),
      cancelled_at: null,
      notes: "",
      payments: [
        { payment_id: "PAY-00003", amount: 179.40, method: "stripe", received_at: daysAgo(14), reference: "ch_3NxEFGH" },
        { payment_id: "PAY-00004", amount: 179.40, method: "stripe", received_at: daysAgo(12), reference: "ch_3NxIJKL" },
      ],
    },
    {
      invoice_id: "INV-0004",
      prospect_id: "p003",
      company_name: "Cabinet Dr. Lefèvre",
      sector: "médical",
      amount_ht: 649.00,
      tva_pct: 20,
      amount_ttc: 778.80,
      tva_amount: 129.80,
      amount_paid: 389.40,
      amount_remaining: 389.40,
      status: "partially_paid",
      due_days: 30,
      created_at: daysAgo(10),
      sent_at: daysAgo(9),
      due_at: daysFromNow(21),
      paid_at: null,
      cancelled_at: null,
      notes: "Paiement en 2 fois",
      payments: [
        { payment_id: "PAY-00005", amount: 389.40, method: "stripe", received_at: daysAgo(7), reference: "ch_3NxMNOP" },
      ],
    },
    {
      invoice_id: "INV-0005",
      prospect_id: "p011",
      company_name: "Notaire & Associés",
      sector: "juridique",
      amount_ht: 832.33,
      tva_pct: 20,
      amount_ttc: 998.80,
      tva_amount: 166.47,
      amount_paid: 0,
      amount_remaining: 998.80,
      status: "sent",
      due_days: 30,
      created_at: daysAgo(5),
      sent_at: daysAgo(4),
      due_at: daysFromNow(26),
      paid_at: null,
      cancelled_at: null,
      notes: "",
      payments: [],
    },
    {
      invoice_id: "INV-0006",
      prospect_id: "p002",
      company_name: "Restaurant La Cigale",
      sector: "restaurant",
      amount_ht: 732.33,
      tva_pct: 20,
      amount_ttc: 878.80,
      tva_amount: 146.47,
      amount_paid: 0,
      amount_remaining: 878.80,
      status: "overdue",
      due_days: 15,
      created_at: daysAgo(35),
      sent_at: daysAgo(34),
      due_at: daysAgo(19),
      paid_at: null,
      cancelled_at: null,
      notes: "Relance envoyée 2x",
      payments: [],
    },
    {
      invoice_id: "INV-0007",
      prospect_id: "p014",
      company_name: "Artisan Pro SARL",
      sector: "artisan",
      amount_ht: 415.67,
      tva_pct: 20,
      amount_ttc: 498.80,
      tva_amount: 83.13,
      amount_paid: 0,
      amount_remaining: 498.80,
      status: "draft",
      due_days: 30,
      created_at: daysAgo(1),
      sent_at: null,
      due_at: null,
      paid_at: null,
      cancelled_at: null,
      notes: "En attente de validation interne",
      payments: [],
    },
    {
      invoice_id: "INV-0008",
      prospect_id: "p010",
      company_name: "BTP Expert SARL",
      sector: "artisan",
      amount_ht: 299.00,
      tva_pct: 20,
      amount_ttc: 358.80,
      tva_amount: 59.80,
      amount_paid: 0,
      amount_remaining: 0,
      status: "cancelled",
      due_days: 30,
      created_at: daysAgo(12),
      sent_at: null,
      due_at: null,
      paid_at: null,
      cancelled_at: daysAgo(10),
      notes: "Prospect perdu",
      payments: [],
    },
  ];

  // Compute summary
  const nonCancelled = invoices.filter(i => i.status !== "cancelled");
  const totalInvoiced = nonCancelled.reduce((s, i) => s + i.amount_ttc, 0);
  const totalCollected = invoices.reduce((s, i) => s + i.amount_paid, 0);
  const totalOutstanding = invoices
    .filter(i => !["paid", "cancelled"].includes(i.status))
    .reduce((s, i) => s + i.amount_remaining, 0);
  const totalOverdue = invoices
    .filter(i => i.status === "overdue")
    .reduce((s, i) => s + i.amount_remaining, 0);
  const paid = invoices.filter(i => i.status === "paid");
  const paidWithDays = paid.filter(i => i.sent_at && i.paid_at);
  const avgDays = paidWithDays.length > 0
    ? Math.round(paidWithDays.reduce((s, i) => {
        const sentMs = new Date(i.sent_at!).getTime();
        const paidMs = new Date(i.paid_at!).getTime();
        return s + (paidMs - sentMs) / 86400000;
      }, 0) / paidWithDays.length * 10) / 10
    : null;

  const summary: Summary = {
    total: invoices.length,
    draft: invoices.filter(i => i.status === "draft").length,
    sent: invoices.filter(i => i.status === "sent").length,
    partially_paid: invoices.filter(i => i.status === "partially_paid").length,
    paid: paid.length,
    overdue: invoices.filter(i => i.status === "overdue").length,
    cancelled: invoices.filter(i => i.status === "cancelled").length,
    total_invoiced_ttc: Math.round(totalInvoiced * 100) / 100,
    total_collected_ttc: Math.round(totalCollected * 100) / 100,
    total_outstanding_ttc: Math.round(totalOutstanding * 100) / 100,
    total_overdue_ttc: Math.round(totalOverdue * 100) / 100,
    collection_rate_pct: totalInvoiced > 0 ? Math.round(totalCollected / totalInvoiced * 1000) / 10 : 0,
    avg_days_to_pay: avgDays,
  };

  return { source: "mock", invoices, summary };
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const [listRes, sumRes] = await Promise.all([
        fetch(`${SWARM_API_URL}/invoices`, { next: { revalidate: 15 } }),
        fetch(`${SWARM_API_URL}/invoices/summary`, { next: { revalidate: 15 } }),
      ]);
      if (listRes.ok && sumRes.ok) {
        return NextResponse.json({
          source: "live",
          invoices: await listRes.json(),
          summary: await sumRes.json(),
        });
      }
    } catch { /* fall through */ }
  }
  return NextResponse.json(buildMockData());
}
