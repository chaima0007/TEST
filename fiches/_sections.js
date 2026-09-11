const {chromium}=require("playwright");const path=require("path");
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:794,height:1123}});
await p.goto("file://"+path.resolve(process.argv[2]));
const r=await p.evaluate(()=>{
  const out=[];
  document.querySelectorAll(".sheet > *").forEach(el=>{
    const st=getComputedStyle(el);
    out.push({tag:el.className||el.tagName, h:Math.round(el.getBoundingClientRect().height), mb:st.marginBottom,
      txt:(el.querySelector("h2")?el.querySelector("h2").textContent:el.textContent.trim().slice(0,32))});
  });
  return out;
});
r.forEach(x=>console.log(String(x.h).padStart(5), x.mb.padStart(6), (x.txt||"").slice(0,44)));
console.log("total", r.reduce((a,x)=>a+x.h+parseFloat(x.mb),0));
await b.close();})();
