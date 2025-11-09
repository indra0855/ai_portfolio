from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import json
import os
import uuid
import markdown
from datetime import datetime

# ---------- Paths ----------
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
BLOG_DIR = os.path.join(BASE_DIR, "blogs")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BLOG_DIR, exist_ok=True)

PROJECTS_JSON = os.path.join(DATA_DIR, "projects.json")
MESSAGES_JSON = os.path.join(DATA_DIR, "messages.json")

# ---------- Ensure necessary files exist ----------
if not os.path.exists(MESSAGES_JSON):
    with open(MESSAGES_JSON, "w", encoding="utf-8") as f:
        json.dump([], f, indent=2)

if not os.path.exists(PROJECTS_JSON):
    sample_projects = [
        {
            "id": "skin-cancer-cnn",
            "title": "Skin Cancer Detection (CNN)",
            "summary": "A convolutional neural network to classify skin lesion images.",
            "stack": ["TensorFlow", "Keras", "Python", "FastAPI", "Docker"],
            "github": "https://github.com/your-username/skin-cancer-cnn",
            "demo": "",
            "image": ""
        },
        {
            "id": "ai-art-generator",
            "title": "AI Art Generator",
            "summary": "A text-to-image AI that turns any description into digital art.",
            "stack": ["Streamlit, Diffusers, PyTorch, Transformers"],
            "github": "https://github.com/your-username/fake-news-bert",
            "demo": "",
            "image": ""
        }
    ]
    with open(PROJECTS_JSON, "w", encoding="utf-8") as f:
        json.dump(sample_projects, f, indent=2)

# ---------- FastAPI setup ----------
app = FastAPI(title="Indrajeet Kumbhar — AI/ML Portfolio")

# Serve static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Jinja2 setup
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# ✅ Global Jinja variable for current year
def get_current_year():
    return datetime.now().year

templates.env.globals["current_year"] = get_current_year


# ---------- Helper Functions ----------
def read_projects():
    with open(PROJECTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def read_messages():
    with open(MESSAGES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def append_message(msg: dict):
    messages = read_messages()
    messages.append(msg)
    with open(MESSAGES_JSON, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)

def list_blog_files():
    files = []
    for fn in os.listdir(BLOG_DIR):
        if fn.endswith(".md"):
            files.append(fn)
    files.sort(reverse=True)
    return files

def read_blog_markdown(filename):
    path = os.path.join(BLOG_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    html = markdown.markdown(text, extensions=["fenced_code", "codehilite"])
    title = filename.replace(".md", "")
    for line in text.splitlines():
        if line.strip().startswith("# "):
            title = line.strip().lstrip("# ").strip()
            break
    return {"title": title, "html": html, "raw": text, "filename": filename}


# ---------- Web Pages ----------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    projects = read_projects()[:3]  # show first 3 projects
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "featured": projects,
            "profile_photo": "/static/images/indra.jpg",  # ✅ your image
        },
    )

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    projects = read_projects()
    return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})

@app.get("/project/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: str):
    projects = read_projects()
    project = next((p for p in projects if p["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return templates.TemplateResponse("project_detail.html", {"request": request, "project": project})

@app.get("/blog", response_class=HTMLResponse)
async def blog_list(request: Request):
    files = list_blog_files()
    posts = []
    for fn in files:
        meta = read_blog_markdown(fn)
        posts.append({"title": meta["title"], "filename": fn})
    return templates.TemplateResponse("blog_list.html", {"request": request, "posts": posts})

@app.get("/blog/{post_filename}", response_class=HTMLResponse)
async def blog_post(request: Request, post_filename: str):
    if not post_filename.endswith(".md"):
        post_filename_full = f"{post_filename}.md"
    else:
        post_filename_full = post_filename
    try:
        meta = read_blog_markdown(post_filename_full)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("blog_post.html", {"request": request, "post": meta})

@app.get("/resume", response_class=FileResponse)
async def download_resume():
    resume_path = os.path.join(STATIC_DIR, "resume.pdf")
    if not os.path.exists(resume_path):
        raise HTTPException(status_code=404, detail="Resume not found. Place `resume.pdf` in static/ directory.")
    return FileResponse(resume_path, media_type="application/pdf", filename="resume.pdf")

@app.get("/contact", response_class=HTMLResponse)
async def contact_get(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


# ---------- API Endpoints ----------
class ContactIn(BaseModel):
    name: str
    email: str
    message: str

@app.post("/api/contact")
async def api_contact(contact: ContactIn):
    msg = {
        "id": str(uuid.uuid4()),
        "name": contact.name,
        "email": contact.email,
        "message": contact.message,
        "received_at": datetime.utcnow().isoformat() + "Z",
    }
    append_message(msg)
    return {"status": "ok", "message": "Message received"}

@app.get("/api/projects")
async def api_projects():
    return read_projects()

@app.get("/api/project/{project_id}")
async def api_project(project_id: str):
    projects = read_projects()
    project = next((p for p in projects if p["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.get("/api/blogs")
async def api_blogs():
    files = list_blog_files()
    result = []
    for fn in files:
        meta = read_blog_markdown(fn)
        result.append({"title": meta["title"], "filename": fn})
    return result

@app.get("/api/messages")
async def api_messages():
    # ⚠️ Only for demo, no authentication
    return read_messages()

# ---------- Health Check ----------
@app.get("/health")
async def health():
    return {"status": "ok"}
