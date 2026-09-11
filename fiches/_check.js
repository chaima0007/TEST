const {chromium}=require("playwright");
const fs=require("fs"), path=require("path");
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:794,height:1123}});
  const files=process.argv.slice(2);
  for(const f of files){
    await p.goto("file://"+path.resolve(f));
    await p.waitForTimeout(150);
    const m=await p.evaluate(()=>{
      const s=document.querySelector(".sheet");
      return {h:s.scrollHeight, w:s.scrollWidth, over:s.scrollHeight>1123, wide:s.scrollWidth>794};
    });
    console.log(f.padEnd(22), "hauteur", String(m.h).padStart(5), m.over?"DÉBORDE ("+(m.h-1123)+"px)":"ok", m.wide?"LARGEUR DÉBORDE":"");
    await p.screenshot({path:"/tmp/claude-0/-home-user-TEST/339c4d73-8697-51e6-a8bb-07bbbb86e761/scratchpad/fiche-"+path.basename(f,".dc.html")+".png"});
  }
  await b.close();
})();
