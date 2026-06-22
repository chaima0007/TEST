"use client";
import { useEffect, useState } from "react";

const COLOR = "#f59e0b";
const DOMAIN = "videocommerce-advertising";
const TITLE = "Video Commerce Advertising";

type Entity = { name: string; composite_score: number; risk_level: string; estimated_videocommerce_index: number };
type Data = { entities: Entity[]; avg_composite: number; distribution: Record<string, number> };

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const offset = circ - (value / 100) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        fontSize={16} fontWeight="bold" fill={color}>{value}</text>
    </svg>
  );
}

function deriveCerts(score: number) {
  return [
    { id: "ISO-26000", label: "ISO 26000", status: score >= 75 ? "certified" : score >= 50 ? "in-progress" : "not-certified" },
    { id: "SA8000", label: "SA8000", status: score >= 80 ? "certified" : score >= 55 ? "in-progress" : "not-certified" },
    { id: "FAIR-TRADE", label: "Fair Trade", status: score >= 70 ? "certified" : score >= 45 ? "in-progress" : "not-certified" },
    { id: "CSDDD", label: "CSDDD 2024/1760", status: score >= 65 ? "certified" : score >= 40 ? "in-progress" : "not-certified" },
    { id: "ILO-C182", label: "OIT C182", status: score >= 60 ? "certified" : score >= 35 ? "in-progress" : "not-certified" },
  ];
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signaux"|"certs"|"actions">("scores");
  const certs = deriveCerts(entity.composite_score);
  const CERT_COLOR: Record<string,string> = { certified: "#16a34a", "in-progress": "#d97706", "not-certified": "#dc2626" };
  return (
    <div style={{ position:"fixed",inset:0,background:"rgba(0,0,0,0.5)",display:"flex",alignItems:"center",justifyContent:"center",zIndex:1000 }} onClick={onClose}>
      <div style={{ background:"#fff",borderRadius:16,padding:32,maxWidth:540,width:"90%",maxHeight:"80vh",overflowY:"auto" }} onClick={e=>e.stopPropagation()}>
        <div style={{ display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:20 }}>
          <h2 style={{ fontSize:18,fontWeight:700,color:"#1e293b",margin:0 }}>{entity.name}</h2>
          <button onClick={onClose} style={{ border:"none",background:"none",fontSize:22,cursor:"pointer",color:"#6b7280" }}>×</button>
        </div>
        <div style={{ display:"flex",gap:8,marginBottom:20 }}>
          {(["scores","signaux","certs","actions"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)} style={{ padding:"6px 14px",borderRadius:8,border:"none",cursor:"pointer",fontWeight:tab===t?700:400,background:tab===t?COLOR:"#f1f5f9",color:tab===t?"#fff":"#374151",fontSize:13 }}>{t}</button>
          ))}
        </div>
        {tab==="scores" && (
          <div style={{ display:"flex",flexDirection:"column",gap:10 }}>
            {[["Score composite",entity.composite_score],["Indice video commerce",entity.estimated_videocommerce_index]].map(([label,val])=>(
              <div key={String(label)} style={{ background:"#f8fafc",borderRadius:8,padding:"10px 16px" }}>
                <div style={{ fontSize:12,color:"#6b7280",marginBottom:4 }}>{label}</div>
                <div style={{ fontSize:20,fontWeight:700,color:COLOR }}>{val}</div>
              </div>
            ))}
          </div>
        )}
        {tab==="signaux" && (
          <div style={{ fontSize:14,color:"#374151",lineHeight:1.7 }}>
            <p><strong>Niveau de risque :</strong> <span style={{ color: entity.risk_level==="critique"?"#dc2626":entity.risk_level==="élevé"?"#d97706":entity.risk_level==="modéré"?"#2563eb":"#16a34a",fontWeight:700 }}>{entity.risk_level.toUpperCase()}</span></p>
            <p>Analyse conformité CSDDD pour la chaîne d&apos;approvisionnement video commerce. Risques liés aux conditions de travail dans la production vidéo et les studios partenaires.</p>
          </div>
        )}
        {tab==="certs" && (
          <div style={{ display:"flex",flexDirection:"column",gap:8 }}>
            {certs.map(c=>(
              <div key={c.id} style={{ display:"flex",justifyContent:"space-between",alignItems:"center",background:"#f8fafc",borderRadius:8,padding:"10px 16px" }}>
                <span style={{ fontWeight:600,fontSize:14 }}>{c.label}</span>
                <span style={{ fontSize:12,fontWeight:700,color:CERT_COLOR[c.status],background:c.status==="certified"?"#dcfce7":c.status==="in-progress"?"#fef9c3":"#fee2e2",padding:"3px 10px",borderRadius:9999 }}>{c.status}</span>
              </div>
            ))}
          </div>
        )}
        {tab==="actions" && (
          <div style={{ fontSize:14,color:"#374151",lineHeight:1.8 }}>
            <p>• Auditer les studios de production vidéo partenaires</p>
            <p>• Vérifier les pratiques des agences créatrices</p>
            <p>• Mettre en place un code de conduite video commerce</p>
            <p>• Certifier ISO 26000 pour la plateforme et ses fournisseurs clés</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default function VideocommerceAdvertisingPage() {
  const [data, setData] = useState<Data | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch(`/api/${DOMAIN}`).then(r=>r.json()).then(d=>setData(d.payload ?? d));
  }, []);

  const RISK_COLOR: Record<string,string> = { critique:"#dc2626", élevé:"#d97706", modéré:"#2563eb", faible:"#16a34a" };

  return (
    <div style={{ padding:32,fontFamily:"sans-serif",maxWidth:1100,margin:"0 auto" }}>
      <h1 style={{ fontSize:26,fontWeight:"bold",color:"#1e293b",marginBottom:4 }}>{TITLE}</h1>
      <p style={{ color:"#6b7280",marginBottom:28 }}>Analyse conformité CSDDD 2024/1760 — Chaîne d&apos;approvisionnement Video Commerce</p>

      {data ? (
        <>
          <div style={{ display:"flex",gap:16,marginBottom:28,flexWrap:"wrap" }}>
            <div style={{ background:"#fff",border:"1px solid #e5e7eb",borderRadius:12,padding:20,flex:1,minWidth:180 }}>
              <div style={{ fontSize:12,color:"#6b7280",marginBottom:8 }}>Score moyen</div>
              <GaugeRing value={Math.round(data.avg_composite)} color={COLOR} />
            </div>
            <div style={{ background:"#fff",border:"1px solid #e5e7eb",borderRadius:12,padding:20,flex:1,minWidth:180 }}>
              <div style={{ fontSize:12,color:"#6b7280",marginBottom:8 }}>Distribution des risques</div>
              {Object.entries(data.distribution).map(([level,count])=>(
                <div key={level} style={{ display:"flex",justifyContent:"space-between",marginBottom:6 }}>
                  <span style={{ fontSize:13,color:RISK_COLOR[level],fontWeight:600 }}>{level}</span>
                  <span style={{ fontSize:13,fontWeight:700 }}>{count}</span>
                </div>
              ))}
            </div>
          </div>

          <div style={{ display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(300px,1fr))",gap:16 }}>
            {data.entities.map(entity=>(
              <div key={entity.name} onClick={()=>setSelected(entity)}
                style={{ background:"#fff",border:"1px solid #e5e7eb",borderRadius:12,padding:20,cursor:"pointer",transition:"box-shadow 0.2s" }}
                onMouseEnter={e=>(e.currentTarget.style.boxShadow="0 4px 12px rgba(0,0,0,0.1)")}
                onMouseLeave={e=>(e.currentTarget.style.boxShadow="none")}>
                <div style={{ display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:12 }}>
                  <span style={{ fontWeight:600,fontSize:14,color:"#1e293b",flex:1,marginRight:8 }}>{entity.name}</span>
                  <span style={{ fontSize:11,fontWeight:700,color:RISK_COLOR[entity.risk_level],background:entity.risk_level==="critique"?"#fee2e2":entity.risk_level==="élevé"?"#fef9c3":entity.risk_level==="modéré"?"#dbeafe":"#dcfce7",padding:"3px 10px",borderRadius:9999,whiteSpace:"nowrap" }}>{entity.risk_level}</span>
                </div>
                <GaugeRing value={Math.round(entity.composite_score)} color={RISK_COLOR[entity.risk_level]} />
              </div>
            ))}
          </div>
        </>
      ) : (
        <div style={{ textAlign:"center",padding:60,color:"#9ca3af" }}>Chargement des données...</div>
      )}

      {selected && <DetailModal entity={selected} onClose={()=>setSelected(null)} />}
    </div>
  );
}
