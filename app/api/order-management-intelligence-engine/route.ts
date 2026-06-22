import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[order-management-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// ─── Scoring helpers (mirrors Python engine) ──────────────────────────────────

function fulfillmentScore(o: (typeof mockOrders)[number]): number {
  let s = 0;
  if (o.days_past_promise_date >= 10) s += 40;
  else if (o.days_past_promise_date >= 5) s += 22;
  else if (o.days_past_promise_date >= 2) s += 8;

  if (o.order_completion_pct <= 0.30) s += 35;
  else if (o.order_completion_pct <= 0.60) s += 18;
  else if (o.order_completion_pct <= 0.80) s += 6;

  if (o.warehouse_processing_delay_days >= 5) s += 25;
  else if (o.warehouse_processing_delay_days >= 2) s += 12;

  return Math.min(s, 100);
}

function inventoryScore(o: (typeof mockOrders)[number]): number {
  let s = 0;
  if (o.inventory_availability_pct <= 0.30) s += 40;
  else if (o.inventory_availability_pct <= 0.55) s += 22;
  else if (o.inventory_availability_pct <= 0.75) s += 8;

  if (o.backorder_item_count >= 8) s += 35;
  else if (o.backorder_item_count >= 4) s += 18;
  else if (o.backorder_item_count >= 1) s += 6;

  if (o.supplier_on_time_rate_pct <= 0.50) s += 25;
  else if (o.supplier_on_time_rate_pct <= 0.70) s += 12;

  return Math.min(s, 100);
}

function qualityScore(o: (typeof mockOrders)[number]): number {
  let s = 0;
  if (o.quality_hold_count >= 5) s += 45;
  else if (o.quality_hold_count >= 2) s += 25;
  else if (o.quality_hold_count >= 1) s += 10;

  if (o.quality_rejection_rate_pct >= 0.15) s += 30;
  else if (o.quality_rejection_rate_pct >= 0.05) s += 15;

  if (o.contract_sla_breach_count >= 3) s += 25;
  else if (o.contract_sla_breach_count >= 1) s += 12;

  return Math.min(s, 100);
}

function logisticsScore(o: (typeof mockOrders)[number]): number {
  let s = 0;
  if (o.transit_delay_days >= 10) s += 40;
  else if (o.transit_delay_days >= 5) s += 22;
  else if (o.transit_delay_days >= 2) s += 8;

  if (o.carrier_performance_score <= 0.40) s += 35;
  else if (o.carrier_performance_score <= 0.65) s += 18;
  else if (o.carrier_performance_score <= 0.80) s += 6;

  if (o.customs_clearance_days >= 10) s += 25;
  else if (o.customs_clearance_days >= 5) s += 12;

  return Math.min(s, 100);
}

function detectPattern(o: (typeof mockOrders)[number]): string {
  if (o.days_past_promise_date >= 7 && o.order_completion_pct <= 0.60) return "fulfillment_delay";
  if (o.inventory_availability_pct <= 0.40 && o.backorder_item_count >= 3) return "inventory_shortage";
  if (o.supplier_on_time_rate_pct <= 0.55 && o.backorder_item_count >= 4) return "supplier_failure";
  if (o.quality_hold_count >= 3 && o.quality_rejection_rate_pct >= 0.10) return "quality_hold";
  if (o.transit_delay_days >= 7 && o.carrier_performance_score <= 0.55) return "logistics_bottleneck";
  return "none";
}

function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function severityLevel(composite: number): string {
  if (composite >= 60) return "blocked";
  if (composite >= 40) return "delayed";
  if (composite >= 20) return "at_risk";
  return "on_schedule";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") {
    if (pattern === "fulfillment_delay" || pattern === "inventory_shortage") return "emergency_procurement";
    return "customer_notification";
  }
  if (risk === "high") {
    if (pattern === "fulfillment_delay") return "expedite_fulfillment";
    if (pattern === "inventory_shortage") return "inventory_reallocation";
    if (pattern === "supplier_failure") return "supplier_escalation";
    if (pattern === "quality_hold") return "quality_inspection";
    if (pattern === "logistics_bottleneck") return "logistics_rerouting";
    return "order_monitoring";
  }
  if (risk === "moderate") return "customer_notification";
  return "no_action";
}

function orderSignal(
  o: (typeof mockOrders)[number],
  pattern: string,
  composite: number,
): string {
  if (composite < 20) {
    return "Order fulfillment on track — inventory, quality and logistics within SLA benchmarks";
  }
  const label =
    pattern !== "none"
      ? pattern.replace(/_/g, " ").replace(/^\w/, (c) => c.toUpperCase())
      : "Order at risk";
  return (
    `${label} — ${o.days_past_promise_date}d past promise — ` +
    `${Math.round(o.order_completion_pct * 100)}% complete — ` +
    `$${Math.round(o.order_value_usd / 1000)}k order — ` +
    `composite ${Math.round(composite)}`
  );
}

function scoreOrder(o: (typeof mockOrders)[number]) {
  const fs = Math.round(fulfillmentScore(o) * 10) / 10;
  const is_ = Math.round(inventoryScore(o) * 10) / 10;
  const qs = Math.round(qualityScore(o) * 10) / 10;
  const ls = Math.round(logisticsScore(o) * 10) / 10;

  const composite = Math.min(
    Math.round((fs * 0.30 + is_ * 0.25 + qs * 0.25 + ls * 0.20) * 100) / 100,
    100.0,
  );

  const pattern = detectPattern(o);
  const risk = riskLevel(composite);
  const severity = severityLevel(composite);
  const action = recommendedAction(risk, pattern);

  const has_delivery_risk =
    composite >= 40 || o.days_past_promise_date >= 5 || o.inventory_availability_pct <= 0.50;
  const requires_client_alert =
    composite >= 25 || o.escalation_requested >= 0.5 || o.contract_sla_breach_count >= 1;
  const estimated_delay_days = Math.max(
    0,
    Math.round((o.days_past_promise_date + o.transit_delay_days) * (composite / 100)),
  );

  return {
    order_id: o.order_id,
    region: o.region,
    order_risk: risk,
    order_pattern: pattern,
    order_severity: severity,
    recommended_action: action,
    fulfillment_score: fs,
    inventory_score: is_,
    quality_score: qs,
    logistics_score: ls,
    order_composite: composite,
    has_delivery_risk,
    requires_client_alert,
    estimated_delay_days,
    order_signal: orderSignal(o, pattern, composite),
  };
}

// ─── Raw mock order inputs ────────────────────────────────────────────────────

const mockOrders = [
  {
    order_id: "OR-001", region: "West",
    days_past_promise_date: 0, fulfillment_cycle_time_days: 3.0,
    order_completion_pct: 0.95, warehouse_processing_delay_days: 0,
    inventory_availability_pct: 0.92, supplier_on_time_rate_pct: 0.95,
    backorder_item_count: 0, substitute_product_available: 1.0,
    quality_hold_count: 0, quality_rejection_rate_pct: 0.01,
    carrier_performance_score: 0.95, transit_delay_days: 0,
    customs_clearance_days: 0, client_priority_tier: 2,
    contract_sla_breach_count: 0, order_value_usd: 18000,
    repeat_order_client: 1.0, escalation_requested: 0.0,
  },
  {
    order_id: "OR-002", region: "East",
    days_past_promise_date: 1, fulfillment_cycle_time_days: 4.5,
    order_completion_pct: 0.85, warehouse_processing_delay_days: 1,
    inventory_availability_pct: 0.80, supplier_on_time_rate_pct: 0.88,
    backorder_item_count: 0, substitute_product_available: 1.0,
    quality_hold_count: 0, quality_rejection_rate_pct: 0.02,
    carrier_performance_score: 0.90, transit_delay_days: 1,
    customs_clearance_days: 0, client_priority_tier: 3,
    contract_sla_breach_count: 0, order_value_usd: 9500,
    repeat_order_client: 0.0, escalation_requested: 0.0,
  },
  {
    order_id: "OR-003", region: "Central",
    days_past_promise_date: 3, fulfillment_cycle_time_days: 7.0,
    order_completion_pct: 0.70, warehouse_processing_delay_days: 2,
    inventory_availability_pct: 0.65, supplier_on_time_rate_pct: 0.75,
    backorder_item_count: 2, substitute_product_available: 0.5,
    quality_hold_count: 1, quality_rejection_rate_pct: 0.04,
    carrier_performance_score: 0.78, transit_delay_days: 2,
    customs_clearance_days: 1, client_priority_tier: 2,
    contract_sla_breach_count: 1, order_value_usd: 32000,
    repeat_order_client: 1.0, escalation_requested: 0.0,
  },
  {
    order_id: "OR-004", region: "Northeast",
    days_past_promise_date: 5, fulfillment_cycle_time_days: 9.0,
    order_completion_pct: 0.55, warehouse_processing_delay_days: 3,
    inventory_availability_pct: 0.48, supplier_on_time_rate_pct: 0.65,
    backorder_item_count: 3, substitute_product_available: 0.4,
    quality_hold_count: 1, quality_rejection_rate_pct: 0.06,
    carrier_performance_score: 0.72, transit_delay_days: 3,
    customs_clearance_days: 2, client_priority_tier: 1,
    contract_sla_breach_count: 1, order_value_usd: 75000,
    repeat_order_client: 1.0, escalation_requested: 0.5,
  },
  {
    order_id: "OR-005", region: "Southeast",
    days_past_promise_date: 8, fulfillment_cycle_time_days: 14.0,
    order_completion_pct: 0.45, warehouse_processing_delay_days: 4,
    inventory_availability_pct: 0.35, supplier_on_time_rate_pct: 0.50,
    backorder_item_count: 5, substitute_product_available: 0.2,
    quality_hold_count: 2, quality_rejection_rate_pct: 0.09,
    carrier_performance_score: 0.60, transit_delay_days: 6,
    customs_clearance_days: 3, client_priority_tier: 1,
    contract_sla_breach_count: 2, order_value_usd: 125000,
    repeat_order_client: 1.0, escalation_requested: 1.0,
  },
  {
    order_id: "OR-006", region: "APAC",
    days_past_promise_date: 4, fulfillment_cycle_time_days: 10.0,
    order_completion_pct: 0.60, warehouse_processing_delay_days: 2,
    inventory_availability_pct: 0.72, supplier_on_time_rate_pct: 0.80,
    backorder_item_count: 1, substitute_product_available: 0.6,
    quality_hold_count: 4, quality_rejection_rate_pct: 0.12,
    carrier_performance_score: 0.82, transit_delay_days: 1,
    customs_clearance_days: 6, client_priority_tier: 2,
    contract_sla_breach_count: 1, order_value_usd: 55000,
    repeat_order_client: 0.5, escalation_requested: 0.0,
  },
  {
    order_id: "OR-007", region: "EMEA",
    days_past_promise_date: 10, fulfillment_cycle_time_days: 20.0,
    order_completion_pct: 0.30, warehouse_processing_delay_days: 6,
    inventory_availability_pct: 0.25, supplier_on_time_rate_pct: 0.40,
    backorder_item_count: 9, substitute_product_available: 0.1,
    quality_hold_count: 3, quality_rejection_rate_pct: 0.11,
    carrier_performance_score: 0.45, transit_delay_days: 8,
    customs_clearance_days: 5, client_priority_tier: 1,
    contract_sla_breach_count: 3, order_value_usd: 320000,
    repeat_order_client: 1.0, escalation_requested: 1.0,
  },
  {
    order_id: "OR-008", region: "LATAM",
    days_past_promise_date: 15, fulfillment_cycle_time_days: 30.0,
    order_completion_pct: 0.10, warehouse_processing_delay_days: 10,
    inventory_availability_pct: 0.10, supplier_on_time_rate_pct: 0.20,
    backorder_item_count: 15, substitute_product_available: 0.0,
    quality_hold_count: 10, quality_rejection_rate_pct: 0.30,
    carrier_performance_score: 0.10, transit_delay_days: 15,
    customs_clearance_days: 15, client_priority_tier: 1,
    contract_sla_breach_count: 5, order_value_usd: 500000,
    repeat_order_client: 1.0, escalation_requested: 1.0,
  },
];

// Pre-score all mock orders
const scoredOrders = mockOrders.map(scoreOrder);

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/order-management-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let orders = [...scoredOrders];
  if (risk)    orders = orders.filter((o) => o.order_risk    === risk);
  if (pattern) orders = orders.filter((o) => o.order_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_ful = 0, total_inv = 0, total_qua = 0, total_log = 0, total_delay = 0;

  for (const o of scoredOrders) {
    risk_counts[o.order_risk]           = (risk_counts[o.order_risk] || 0) + 1;
    pattern_counts[o.order_pattern]     = (pattern_counts[o.order_pattern] || 0) + 1;
    severity_counts[o.order_severity]   = (severity_counts[o.order_severity] || 0) + 1;
    action_counts[o.recommended_action] = (action_counts[o.recommended_action] || 0) + 1;
    total_comp  += o.order_composite;
    total_ful   += o.fulfillment_score;
    total_inv   += o.inventory_score;
    total_qua   += o.quality_score;
    total_log   += o.logistics_score;
    total_delay += o.estimated_delay_days;
  }

  const n = scoredOrders.length;

  return sealResponse(NextResponse.json(sealResponse({
    orders,
    summary: {
      total:                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_order_composite:      Math.round((total_comp / n) * 10) / 10,
      delivery_risk_count:      scoredOrders.filter((o) => o.has_delivery_risk).length,
      client_alert_count:       scoredOrders.filter((o) => o.requires_client_alert).length,
      avg_fulfillment_score:    Math.round((total_ful / n) * 10) / 10,
      avg_inventory_score:      Math.round((total_inv / n) * 10) / 10,
      avg_quality_score:        Math.round((total_qua / n) * 10) / 10,
      avg_logistics_score:      Math.round((total_log / n) * 10) / 10,
      avg_estimated_delay_days: Math.round((total_delay / n) * 10) / 10,
    },
  } as Record<string,unknown>)));
}
