from fastapi import FastAPI, UploadFile, File, Body, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from document_parser import parse_file
from embeddings import get_embeddings, chunk_text
from qdrant_utils import insert_embeddings, search_embeddings
import os
import tempfile
import logging

app = FastAPI()
logger = logging.getLogger("uvicorn.error")

# CORS (open in dev, restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Serve frontend
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
if not os.path.exists(frontend_path):
    raise RuntimeError(f"Frontend directory not found: {frontend_path}")

app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/")
async def root():
    return RedirectResponse(url="/frontend/index.html")

# Favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join(frontend_path, "favicon.ico"))

# Allowed file types
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

# Upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        ext = file.filename.split(".")[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return JSONResponse({"message": "Invalid file type"}, status_code=400)

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Parse + embed
        text_chunks = parse_file(tmp_path)
        vectors = get_embeddings(text_chunks, source=file.filename)
        insert_embeddings(vectors)

        return JSONResponse({
            "message": f"Uploaded {file.filename}",
            "chunks": len(text_chunks)
        })

    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return JSONResponse({"message": f"Upload failed: {str(e)}"}, status_code=500)

# Ask endpoint (JSON input)
@app.post("/ask")
async def ask_question(payload: dict = Body(...)):
    try:
        question = payload.get("question")
        if not question:
            return JSONResponse({"answer": "No question provided."}, status_code=400)

        results = search_embeddings(question)
        if results:
            answer = "\n\n".join([r["text"] for r in results])
            sources = list(set(r["source"] for r in results))
            return JSONResponse({"answer": answer, "sources": sources})

        return JSONResponse({"answer": "No relevant content found."})

    except Exception as e:
        logger.error(f"Ask error: {str(e)}")
        return JSONResponse({"answer": f"Error: {str(e)}"}, status_code=500)

# CMS import endpoint
@app.post("/import_cms")
async def import_cms(content: str = Form(...), source: str = Form("CMS")):
    try:
        text_chunks = chunk_text(content)
        vectors = get_embeddings(text_chunks, source=source)
        insert_embeddings(vectors)
        return JSONResponse({
            "message": f"Imported CMS content: {source}",
            "chunks": len(text_chunks)
        })
    except Exception as e:
        logger.error(f"CMS import error: {str(e)}")
        return JSONResponse({"message": f"Import failed: {str(e)}"}, status_code=500)
