"use client";
import { useEffect, useState } from "react";

const API_URL = "/api/glass-blowing-silicosis-rights";
const TITLE = "Droits Travailleurs Souffleurs de Verre — Silicose";
const COLOR = "#0891b2";

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value, 0), 100);
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={`${(pct / 100) * circ} ${circ}`}
        strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy + 5} textAnchor="middle" fontSize={14} fontWeight="bold" fill={color}>{Math.round(pct)}</text>
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: any; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu"|"indicateurs"|"recommandations">("apercu");
  return (
    <div style={{ position:"fixed",inset:0,background:"rgba(0,0,0,0.5)",zIndex:50,display:"flex",alignItems:"center",justifyContent:"center" }} onClick={onClose}>
      <div style={{ background:"white",borderRadius:12,padding:24,maxWidth:480,width:"90%",maxHeight:"80vh",overflow:"auto" }} onClick={e=>e.stopPropagation()}>
        <div style={{ display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:16 }}>
          <h3 style={{ fontWeight:700,fontSize:18 }}>{entity.entity}</h3>
          <button onClick={onClose} style={{ border:"none",background:"none",fontSize:20,cursor:"pointer" }}>×</button>
        </div>
        <div style={{ display:"flex",gap:8,marginBottom:16 }}>
          {(["apercu","indicateurs","recommandations"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)} style={{ padding:"4px 12px",borderRadius:20,border:"1px solid #e5e7eb",background:tab===t?COLOR:"white",color:tab===t?"white":"#374151",cursor:"pointer",fontSize:13 }}>{t.charAt(0).toUpperCase()+t.slice(1)}</button>
          ))}
        </div>
        {tab==="apercu" && <div><p style={{ color:"#6b7280",fontSize:14 }}>Score composite : <strong>{entity.composite_score}</strong></p><p style={{ color:"#6b7280",fontSize:14 }}>Niveau de risque : <strong>{entity.risk_level}</strong></p></div>}
        {tab==="indicateurs" && <div>{Object.entries(entity).map(([k,v])=><p key={k} style={{ fontSize:13,color:"#374151" }}><strong>{k}</strong> : {String(v)}</p>)}</div>}
        {tab==="recommandations" && <div><p style={{ fontSize:14,color:"#6b7280" }}>Renforcer les mécanismes de due diligence et la traçabilité de la chaîne d&apos;approvisionnement conformément à la CSDDD 2024/1760.</p></div>}
      </div>
    </div>
  );
}

export default function Page() {
  const [data, setData] = useState<any>(null);
  const [selected, setSelected] = useState<any>(null);

  useEffect(() => {
    fetch(API_URL).then(r=>r.json()).then(d=>setData(d.payload ?? d));
  }, []);

  if (!data) return <div style={{ padding:32,textAlign:"center",color:"#6b7280" }}>Chargement…</div>;

  return (
    <div style={{ padding:32,maxWidth:900,margin:"0 auto" }}>
      <h1 style={{ fontSize:28,fontWeight:800,marginBottom:8 }}>{TITLE}</h1>
      <p style={{ color:"#6b7280",marginBottom:24 }}>Score moyen : <strong style={{ color:COLOR }}>{data.avg_composite}</strong> | Distribution : {JSON.stringify(data.distribution)}</p>
      <div style={{ display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(220px,1fr))",gap:16 }}>
        {data.entities?.map((e: any) => (
          <div key={e.entity} onClick={()=>setSelected(e)} style={{ background:"white",borderRadius:12,padding:20,boxShadow:"0 1px 3px rgba(0,0,0,0.1)",cursor:"pointer",border:`2px solid ${e.risk_level==="critique"?"#ef4444":e.risk_level==="élevé"?"#f97316":e.risk_level==="modéré"?"#eab308":"#22c55e"}` }}>
            <GaugeRing value={e.composite_score} color={COLOR} />
            <p style={{ fontWeight:700,marginTop:8,fontSize:14 }}>{e.entity}</p>
            <p style={{ fontSize:12,color:"#6b7280",textTransform:"uppercase" }}>{e.risk_level}</p>
          </div>
        ))}
      </div>
      {selected && <DetailModal entity={selected} onClose={()=>setSelected(null)} />}
    </div>
  );
}
