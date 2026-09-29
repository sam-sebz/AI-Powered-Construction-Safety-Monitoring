import asyncio,io,httpx
from PIL import Image
from src.main import app
from src.db import init_db

init_db()

async def main():
    transport=httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport,base_url="http://test") as c:
        assert (await c.get("/api/health")).status_code==200
        im=Image.new("L",(64,64),20)
        b=io.BytesIO(); im.save(b,format="PNG"); b.seek(0)
        r=await c.post("/api/predict",files={"file":("x.png",b.getvalue(),"image/png")})
        assert r.status_code==200
        z=await c.post("/api/zone-event",json={"person_detected":True,"distance_m":5,"confidence":.9})
        assert z.json()["violation"] is True
    print("P1 smoke tests passed")

asyncio.run(main())
