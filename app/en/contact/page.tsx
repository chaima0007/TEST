"use client";
import { useState } from "react";

export default function EnglishContactPage() {
  const [sent, setSent] = useState(false);

  return (
    <div style={{ fontFamily: "sans-serif", maxWidth: 720, margin: "0 auto", padding: "48px 24px" }}>
      <div style={{ marginBottom: 8, fontSize: 13, color: "#0891b2", fontWeight: 700 }}>
        CAELUM PARTNERS SRL
      </div>
      <h1 style={{ fontSize: 32, fontWeight: 900, color: "#0f172a", marginBottom: 8 }}>
        Request a Demo
      </h1>
      <p style={{ color: "#64748b", marginBottom: 36, fontSize: 15 }}>
        Our team will contact you within 24 hours to schedule a personalized demonstration
        of CaelumSwarm™ for your sector.
      </p>

      {sent ? (
        <div style={{ background: "#f0fdf4", border: "1px solid #86efac", borderRadius: 12, padding: 32, textAlign: "center" }}>
          <div style={{ fontSize: 40, marginBottom: 12 }}>✓</div>
          <div style={{ fontWeight: 700, color: "#16a34a", fontSize: 18 }}>Message received!</div>
          <div style={{ color: "#166534", marginTop: 8 }}>We will contact you within 24 hours.</div>
        </div>
      ) : (
        <div style={{ background: "#f8fafc", borderRadius: 16, padding: 32, border: "1px solid #e2e8f0" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            {[
              { label: "Company name", type: "text", placeholder: "Acme Corporation" },
              { label: "Your name", type: "text", placeholder: "John Smith" },
              { label: "Professional email", type: "email", placeholder: "john@company.com" },
              { label: "Country", type: "text", placeholder: "Belgium, France, Germany..." },
            ].map(field => (
              <div key={field.label}>
                <label style={{ fontSize: 13, fontWeight: 600, color: "#374151", display: "block", marginBottom: 6 }}>
                  {field.label}
                </label>
                <input type={field.type} placeholder={field.placeholder} style={{
                  width: "100%", padding: "10px 14px", borderRadius: 8,
                  border: "1px solid #d1d5db", fontSize: 14, color: "#0f172a",
                  boxSizing: "border-box" as const,
                }} />
              </div>
            ))}
            <div>
              <label style={{ fontSize: 13, fontWeight: 600, color: "#374151", display: "block", marginBottom: 6 }}>
                What is your main compliance challenge?
              </label>
              <textarea placeholder="Tell us about your supply chain and CSDDD obligations..." style={{
                width: "100%", padding: "10px 14px", borderRadius: 8,
                border: "1px solid #d1d5db", fontSize: 14, color: "#0f172a",
                minHeight: 100, boxSizing: "border-box" as const, resize: "vertical",
              }} />
            </div>
            <button onClick={() => setSent(true)} style={{
              padding: "14px", background: "#0891b2", color: "#fff",
              border: "none", borderRadius: 8, fontWeight: 700, fontSize: 16,
              cursor: "pointer",
            }}>
              Send Request
            </button>
          </div>
        </div>
      )}

      <div style={{ marginTop: 40, padding: 24, background: "#f8fafc", borderRadius: 12, border: "1px solid #e2e8f0" }}>
        <div style={{ fontWeight: 700, color: "#0f172a", marginBottom: 16 }}>Direct contact</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 10, fontSize: 14, color: "#475569" }}>
          <div>📧 <strong>legal@caelumpartners.eu</strong></div>
          <div>📍 Boulevard Auguste Reyers 32, 1030 Schaerbeek, Brussels, Belgium</div>
          <div>⚖️ Belgian law — CSDDD EU 2024/1760 compliance experts</div>
        </div>
      </div>
    </div>
  );
}
