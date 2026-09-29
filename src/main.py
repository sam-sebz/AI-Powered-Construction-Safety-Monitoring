from pathlib import Path
import io,json,joblib,numpy as np
from PIL import Image
from fastapi import FastAPI,UploadFile,File,HTTPException
from pydantic import BaseModel,Field
from fastapi.responses import FileResponse
from .db import init_db,add_incident,list_incidents

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/"artifacts"
UI=ROOT/"ui"
app=FastAPI(title="Construction PPE Monitoring")

class IncidentIn(BaseModel):
    event_type:str
    severity:str
    description:str
    compliance:int|None=None
    source:str="api"

class ZoneIn(BaseModel):
    person_detected:bool
    distance_m:float=Field(ge=0)
    confidence:float=Field(ge=0,le=1)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/health")
def health():
    return {"status":"ok"}

@app.get("/api/metrics")
def metrics():
    p=ART/"metrics.json"
    return json.loads(p.read_text()) if p.exists() else {}

@app.post("/api/predict")
async def predict(file:UploadFile=File(...)):
    if file.content_type not in {"image/png","image/jpeg","image/webp"}:
        raise HTTPException(415,"Upload a PNG JPEG or WEBP image")
    model_path=ART/"ppe_model.joblib"
    if not model_path.exists():
        raise HTTPException(503,"Model missing. Run python src/train_model.py")
    raw=await file.read()
    try:
        im=Image.open(io.BytesIO(raw)).convert("L").resize((64,64))
    except Exception:
        raise HTTPException(400,"Invalid image")
    x=np.asarray(im).astype(np.float32).ravel()[None,:]/255.0
    pred=int(joblib.load(model_path).predict(x)[0])
    label="compliant" if pred else "non_compliant"
    iid=add_incident("ppe_check","normal" if pred else "high",f"PPE result: {label}",pred,"image_upload")
    return {"compliance":label,"incident_id":iid}

@app.post("/api/zone-event")
def zone_event(x:ZoneIn):
    violation=bool(x.person_detected and x.distance_m<10 and x.confidence>=.60)
    if violation:
        add_incident("restricted_zone","high","Person entered restricted zone",None,"rule_engine")
    return {"violation":violation,"severity":"high" if violation else "normal"}

@app.post("/api/incidents")
def create_incident(x:IncidentIn):
    return {"id":add_incident(**x.model_dump())}

@app.get("/api/incidents")
def incidents():
    return list_incidents()

@app.get("/")
def root():
    return FileResponse(UI/"index.html")
