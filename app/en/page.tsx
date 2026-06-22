"use client";

export default function EnglishLandingPage() {
  return (
    <div style={{ fontFamily: "sans-serif", maxWidth: 900, margin: "0 auto", padding: "48px 24px" }}>
      {/* Header */}
      <div style={{ textAlign: "center", marginBottom: 56 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: "#0891b2", letterSpacing: 2, marginBottom: 12 }}>
          CAELUM PARTNERS SRL — BRUSSELS, BELGIUM
        </div>
        <h1 style={{ fontSize: 42, fontWeight: 900, color: "#0f172a", lineHeight: 1.15, marginBottom: 20 }}>
          CaelumSwarm™<br />
          <span style={{ color: "#0891b2" }}>AI Compliance Platform</span>
        </h1>
        <p style={{ fontSize: 18, color: "#475569", maxWidth: 640, margin: "0 auto 32px", lineHeight: 1.7 }}>
          Automated CSDDD 2024/1760 compliance scoring for your entire supply chain.
          340+ sector engines. Real-time risk assessment. EU-ready reporting.
        </p>
        <a href="/en/contact" style={{
          display: "inline-block", padding: "14px 36px", background: "#0891b2",
          color: "#fff", borderRadius: 8, fontWeight: 700, fontSize: 16,
          textDecoration: "none", marginRight: 12,
        }}>
          Request a Demo
        </a>
        <a href="/dashboard" style={{
          display: "inline-block", padding: "14px 36px", background: "#f1f5f9",
          color: "#0f172a", borderRadius: 8, fontWeight: 700, fontSize: 16,
          textDecoration: "none",
        }}>
          View Platform
        </a>
      </div>

      {/* Why CaelumSwarm */}
      <div style={{ background: "#f8fafc", borderRadius: 16, padding: "40px 36px", marginBottom: 40 }}>
        <h2 style={{ fontSize: 24, fontWeight: 800, color: "#0f172a", marginBottom: 8 }}>
          Why CaelumSwarm™?
        </h2>
        <p style={{ color: "#64748b", marginBottom: 28, fontSize: 15 }}>
          The EU Corporate Sustainability Due Diligence Directive (CSDDD) 2024/1760 requires large companies
          to identify, prevent and remediate human rights and environmental risks in their supply chains.
          Non-compliance = fines up to 5% of global turnover.
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 20 }}>
          {[
            { icon: "⚡", title: "340+ Sector Engines", desc: "AI scoring engines covering every industry from textiles to fintech" },
            { icon: "🎯", title: "8-Entity Scoring", desc: "Proprietary composite algorithm across 4 risk levels: critical, high, moderate, low" },
            { icon: "📊", title: "Real-Time Dashboards", desc: "Visual risk maps with certification tracking (ISO 26000, SA8000, CSDDD)" },
            { icon: "🔒", title: "IP Protected", desc: "BOIP i-DEPOT registered — methodology protected under Belgian & EU law" },
          ].map(item => (
            <div key={item.title} style={{ background: "#fff", borderRadius: 12, padding: 20, border: "1px solid #e2e8f0" }}>
              <div style={{ fontSize: 28, marginBottom: 10 }}>{item.icon}</div>
              <div style={{ fontWeight: 700, color: "#0f172a", marginBottom: 6 }}>{item.title}</div>
              <div style={{ fontSize: 13, color: "#64748b", lineHeight: 1.6 }}>{item.desc}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Target clients */}
      <div style={{ marginBottom: 40 }}>
        <h2 style={{ fontSize: 22, fontWeight: 800, color: "#0f172a", marginBottom: 20 }}>Who needs this?</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {[
            "Large EU companies with 500+ employees and €150M+ global turnover (CSDDD phase 1)",
            "SMEs in supply chains of large EU corporations (contractual compliance requirements)",
            "Legal & compliance teams preparing for CSDDD audits",
            "ESG consultancies advising clients on due diligence obligations",
            "Banks and investors assessing portfolio CSDDD exposure",
          ].map(item => (
            <div key={item} style={{ display: "flex", gap: 12, alignItems: "flex-start", padding: "12px 16px", background: "#f0fdf4", borderRadius: 8, border: "1px solid #bbf7d0" }}>
              <span style={{ color: "#16a34a", fontWeight: 700, flexShrink: 0 }}>✓</span>
              <span style={{ fontSize: 14, color: "#166534" }}>{item}</span>
            </div>
          ))}
        </div>
      </div>

      {/* CTA */}
      <div style={{ background: "#0f172a", borderRadius: 16, padding: "40px 36px", textAlign: "center" }}>
        <h2 style={{ fontSize: 26, fontWeight: 800, color: "#fff", marginBottom: 12 }}>
          Ready to assess your supply chain?
        </h2>
        <p style={{ color: "#94a3b8", marginBottom: 28, fontSize: 15 }}>
          Get a free demo tailored to your industry sector.
        </p>
        <a href="/en/contact" style={{
          display: "inline-block", padding: "14px 36px", background: "#0891b2",
          color: "#fff", borderRadius: 8, fontWeight: 700, fontSize: 16,
          textDecoration: "none",
        }}>
          Contact Us — legal@caelumpartners.eu
        </a>
      </div>

      <div style={{ textAlign: "center", marginTop: 32, fontSize: 12, color: "#94a3b8" }}>
        © 2024-2026 Caelum Partners SRL — CaelumSwarm™ is a registered trademark.
        Boulevard Auguste Reyers 32, 1030 Schaerbeek, Brussels, Belgium
      </div>
    </div>
  );
}
