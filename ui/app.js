async function refresh(){
 const m=await fetch("/api/metrics").then(r=>r.json());
 document.querySelector("#metrics").textContent=JSON.stringify(m,null,2);
 const rows=await fetch("/api/incidents").then(r=>r.json());
 document.querySelector("#rows").innerHTML=rows.map(x=>`<tr><td>${x.created_at}</td><td>${x.event_type}</td><td>${x.severity}</td><td>${x.description}</td></tr>`).join("");
}
async function check(){
 const f=document.querySelector("#img").files[0]; if(!f)return;
 const fd=new FormData(); fd.append("file",f);
 const j=await fetch("/api/predict",{method:"POST",body:fd}).then(r=>r.json());
 document.querySelector("#result").textContent=JSON.stringify(j,null,2);
 refresh();
}
refresh();
