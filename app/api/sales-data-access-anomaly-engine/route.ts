import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockUsers = [
  {
    user_id: "usr_001", user_name: "Alice Chen", role: "sales_rep", region: "West",
    anomaly_level: "none", anomaly_risk: "low",
    primary_anomaly_type: "none", recommended_action: "no_action",
    access_volume_score: 5.0, behavioral_deviation_score: 3.0,
    data_sensitivity_score: 8.0, authentication_risk_score: 2.0,
    anomaly_composite: 4.7, is_active_threat: false, requires_immediate_action: false,
    estimated_data_exposure_mb: 0.5,
    anomaly_signal: "normal access pattern — behavior within expected parameters",
    download_volume_mb: 10.2,
  },
  {
    user_id: "usr_002", user_name: "Marcus Hayes", role: "sales_rep", region: "East",
    anomaly_level: "low", anomaly_risk: "low",
    primary_anomaly_type: "off_hours", recommended_action: "log_alert",
    access_volume_score: 22.0, behavioral_deviation_score: 18.0,
    data_sensitivity_score: 15.0, authentication_risk_score: 10.0,
    anomaly_composite: 17.2, is_active_threat: false, requires_immediate_action: false,
    estimated_data_exposure_mb: 4.8,
    anomaly_signal: "elevated off-hours access — 34% sessions outside business hours",
    download_volume_mb: 27.9,
  },
  {
    user_id: "usr_003", user_name: "Sofia Reyes", role: "sales_manager", region: "Central",
    anomaly_level: "elevated", anomaly_risk: "moderate",
    primary_anomaly_type: "bulk_export", recommended_action: "security_review",
    access_volume_score: 55.0, behavioral_deviation_score: 48.0,
    data_sensitivity_score: 40.0, authentication_risk_score: 20.0,
    anomaly_composite: 42.5, is_active_threat: false, requires_immediate_action: false,
    estimated_data_exposure_mb: 89.1,
    anomaly_signal: "bulk export spike — 4 large exports in 3 days, 2.1x normal volume",
    download_volume_mb: 209.6,
  },
  {
    user_id: "usr_004", user_name: "Ryan Blackwell", role: "sales_rep", region: "Southeast",
    anomaly_level: "high", anomaly_risk: "high",
    primary_anomaly_type: "credential_sharing", recommended_action: "account_suspend",
    access_volume_score: 72.0, behavioral_deviation_score: 68.0,
    data_sensitivity_score: 62.0, authentication_risk_score: 58.0,
    anomaly_composite: 65.8, is_active_threat: true, requires_immediate_action: true,
    estimated_data_exposure_mb: 312.4,
    anomaly_signal: "credential sharing suspected — 3 unusual IPs, concurrent sessions detected",
    download_volume_mb: 474.8,
  },
  {
    user_id: "usr_005", user_name: "Priya Nair", role: "sales_rep", region: "Northeast",
    anomaly_level: "critical", anomaly_risk: "critical",
    primary_anomaly_type: "data_exfiltration", recommended_action: "immediate_lockdown",
    access_volume_score: 95.0, behavioral_deviation_score: 92.0,
    data_sensitivity_score: 88.0, authentication_risk_score: 85.0,
    anomaly_composite: 90.8, is_active_threat: true, requires_immediate_action: true,
    estimated_data_exposure_mb: 1242.0,
    anomaly_signal: "data exfiltration risk — 3 personal email exports, 5.8x normal download volume",
    download_volume_mb: 1368.1,
  },
  {
    user_id: "usr_006", user_name: "Jordan Walsh", role: "sales_rep", region: "Northwest",
    anomaly_level: "none", anomaly_risk: "low",
    primary_anomaly_type: "none", recommended_action: "no_action",
    access_volume_score: 4.0, behavioral_deviation_score: 6.0,
    data_sensitivity_score: 5.0, authentication_risk_score: 3.0,
    anomaly_composite: 4.6, is_active_threat: false, requires_immediate_action: false,
    estimated_data_exposure_mb: 0.3,
    anomaly_signal: "normal access pattern — behavior within expected parameters",
    download_volume_mb: 7.1,
  },
  {
    user_id: "usr_007", user_name: "Caleb Stone", role: "sales_ops", region: "Southwest",
    anomaly_level: "elevated", anomaly_risk: "moderate",
    primary_anomaly_type: "privilege_abuse", recommended_action: "security_review",
    access_volume_score: 48.0, behavioral_deviation_score: 52.0,
    data_sensitivity_score: 60.0, authentication_risk_score: 30.0,
    anomaly_composite: 48.3, is_active_threat: true, requires_immediate_action: false,
    estimated_data_exposure_mb: 156.7,
    anomaly_signal: "privilege access anomaly — 42 privileged record accesses vs avg 8",
    download_volume_mb: 324.5,
  },
  {
    user_id: "usr_008", user_name: "Nina Cross", role: "sales_rep", region: "Central",
    anomaly_level: "low", anomaly_risk: "moderate",
    primary_anomaly_type: "off_hours", recommended_action: "log_alert",
    access_volume_score: 28.0, behavioral_deviation_score: 25.0,
    data_sensitivity_score: 20.0, authentication_risk_score: 15.0,
    anomaly_composite: 22.8, is_active_threat: false, requires_immediate_action: false,
    estimated_data_exposure_mb: 14.6,
    anomaly_signal: "minor access anomaly — composite score 23, off-hours pattern noted",
    download_volume_mb: 64.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const level  = searchParams.get("level");
  const risk   = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-data-access-anomaly-engine`);
      if (level) url.searchParams.set("level", level);
      if (risk)  url.searchParams.set("risk",  risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let users = [...mockUsers];
  if (level) users = users.filter((u) => u.anomaly_level === level);
  if (risk)  users = users.filter((u) => u.anomaly_risk   === risk);

  const level_counts:  Record<string, number> = {};
  const risk_counts:   Record<string, number> = {};
  const type_counts:   Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_comp = 0, total_access = 0, total_behavioral = 0, total_sensitivity = 0, total_auth = 0, total_exposure = 0;

  for (const u of mockUsers) {
    level_counts[u.anomaly_level]          = (level_counts[u.anomaly_level] || 0) + 1;
    risk_counts[u.anomaly_risk]            = (risk_counts[u.anomaly_risk] || 0) + 1;
    type_counts[u.primary_anomaly_type]    = (type_counts[u.primary_anomaly_type] || 0) + 1;
    action_counts[u.recommended_action]    = (action_counts[u.recommended_action] || 0) + 1;
    total_comp        += u.anomaly_composite;
    total_access      += u.access_volume_score;
    total_behavioral  += u.behavioral_deviation_score;
    total_sensitivity += u.data_sensitivity_score;
    total_auth        += u.authentication_risk_score;
    total_exposure    += u.estimated_data_exposure_mb;
  }

  const n = mockUsers.length;

  return NextResponse.json({
    users,
    summary: {
      total:                              n,
      level_counts,
      risk_counts,
      type_counts,
      action_counts,
      avg_anomaly_composite:              Math.round((total_comp        / n) * 10) / 10,
      active_threat_count:                mockUsers.filter((u) => u.is_active_threat).length,
      immediate_action_count:             mockUsers.filter((u) => u.requires_immediate_action).length,
      avg_access_volume_score:            Math.round((total_access      / n) * 10) / 10,
      avg_behavioral_deviation_score:     Math.round((total_behavioral  / n) * 10) / 10,
      avg_data_sensitivity_score:         Math.round((total_sensitivity / n) * 10) / 10,
      avg_authentication_risk_score:      Math.round((total_auth        / n) * 10) / 10,
      total_data_exposure_mb:             Math.round(total_exposure * 10) / 10,
    },
  });
}
