import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.config import settings

app = FastAPI(title=settings.service_name)


def ensure_upload_dir():
    os.makedirs(settings.upload_dir, exist_ok=True)


@app.on_event("startup")
def on_startup():
    ensure_upload_dir()


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.service_name}


@app.get("/ready")
def ready():
    # minimal readiness: directory exists
    ensure_upload_dir()
    return {"status": "ready"}


@app.post("/media/upload")
async def upload_media(file: UploadFile = File(...)):
    ensure_upload_dir()

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are allowed")

    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in [".png", ".jpg", ".jpeg", ".webp"]:
        # allow missing extension too; we’ll default to .jpg
        ext = ext if ext else ".jpg"

    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(settings.upload_dir, filename)

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    with open(path, "wb") as f:
        f.write(content)

    return {"filename": filename, "path": f"/media/{filename}"}


@app.get("/media/{filename}")
def get_media(filename: str):
    path = os.path.join(settings.upload_dir, filename)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)
