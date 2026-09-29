from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)
RNG = np.random.default_rng(2026)
SIZE = 64

def make_worker(helmet, vest, seed, stress=False):
    rr = np.random.default_rng(seed)
    im = Image.new("L", (SIZE, SIZE), 20)
    d = ImageDraw.Draw(im)
    d.rectangle([20,26,44,58], fill=105)
    d.ellipse([24,13,40,29], fill=145)
    if helmet:
        d.pieslice([20,7,44,25], 180, 360, fill=230)
        d.rectangle([21,15,43,18], fill=230)
    if vest:
        d.polygon([(20,27),(31,27),(29,57),(20,55)], fill=210)
        d.polygon([(44,27),(33,27),(35,57),(44,55)], fill=210)
        d.line([32,28,32,57], fill=40, width=2)
    arr=np.asarray(im).astype(np.float32)
    arr += rr.normal(0,10,arr.shape)
    if stress:
        im=Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
        d=ImageDraw.Draw(im)
        if rr.random()<0.45:
            x1=int(rr.integers(0,42)); y1=int(rr.integers(0,42))
            w=int(rr.integers(5,16)); h=int(rr.integers(5,16))
            d.rectangle([x1,y1,min(63,x1+w),min(63,y1+h)], fill=int(rr.integers(0,100)))
        if rr.random()<0.35:
            im=im.filter(ImageFilter.GaussianBlur(radius=float(rr.uniform(.4,1.5))))
        arr=np.asarray(im).astype(np.float32)*rr.uniform(.75,1.25)
    return np.clip(arr,0,255).astype(np.uint8)

def make_set(n, stress=False, offset=0):
    X=[]; y=[]
    for i in range(n):
        helmet=int(RNG.random()>0.20)
        vest=int(RNG.random()>0.25)
        X.append(make_worker(helmet,vest,offset+i,stress).ravel()/255.0)
        y.append(int(helmet and vest))
    return np.asarray(X),np.asarray(y)

X,y=make_set(3000)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.20,random_state=42,stratify=y)
model=Pipeline([("scale",StandardScaler()),("clf",LogisticRegression(max_iter=1500,random_state=42))])
model.fit(Xtr,ytr)

SX,Sy=make_set(800,stress=True,offset=10000)
sp=model.predict(SX)

metrics={
 "training_images":int(len(Xtr)),
 "test_images":int(len(Xte)),
 "stress_test_images":int(len(SX)),
 "stress_accuracy":float(accuracy_score(Sy,sp)),
 "stress_precision":float(precision_score(Sy,sp)),
 "stress_recall":float(recall_score(Sy,sp)),
 "stress_f1":float(f1_score(Sy,sp))
}

joblib.dump(model,ART/"ppe_model.joblib")
(ART/"metrics.json").write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
