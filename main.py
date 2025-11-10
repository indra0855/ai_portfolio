# from fastapi import FastAPI, Request, Form, HTTPException
# from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel, EmailStr
# from typing import List
# import json
# import os
# import uuid
# import markdown
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime
# from dotenv import load_dotenv
# import os
# load_dotenv()
# # Email Configuration
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
# NOTIFICATION_EMAIL = "indrajeetkumbhar23121@gmail.com"  # Your Gmail address to receive notifications
# SMTP_USERNAME = "indrajeetkumbhar23121@gmail.com"  # Your Gmail address
# SMTP_PASSWORD =os.getenv("emailpassword")  # Set this environment variable securely

# # ---------- Paths ----------
# BASE_DIR = os.path.dirname(__file__)
# DATA_DIR = os.path.join(BASE_DIR, "data")
# BLOG_DIR = os.path.join(BASE_DIR, "blogs")
# STATIC_DIR = os.path.join(BASE_DIR, "static")
# TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# os.makedirs(DATA_DIR, exist_ok=True)
# os.makedirs(BLOG_DIR, exist_ok=True)

# PROJECTS_JSON = os.path.join(DATA_DIR, "projects.json")
# MESSAGES_JSON = os.path.join(DATA_DIR, "messages.json")

# # ---------- Ensure necessary files exist ----------
# if not os.path.exists(MESSAGES_JSON):
#     with open(MESSAGES_JSON, "w", encoding="utf-8") as f:
#         json.dump([], f, indent=2)

# if not os.path.exists(PROJECTS_JSON):
#     sample_projects = [
#         {
#             "id": "skin-cancer-cnn",
#             "title": "Skin Cancer Detection (CNN)",
#             "summary": "A convolutional neural network to classify skin lesion images.",
#             "stack": ["TensorFlow", "Keras", "Python", "FastAPI", "Docker"],
#             "github": "https://github.com/your-username/skin-cancer-cnn",
#             "demo": "",
#             "image": ""
#         },
#         {
#             "id": "fake-news-bert",
#             "title": "Fake News Detection (BERT)",
#             "summary": "Fine-tuned BERT model to detect fake news articles.",
#             "stack": ["Hugging Face", "Transformers", "PyTorch", "FastAPI"],
#             "github": "https://github.com/your-username/fake-news-bert",
#             "demo": "",
#             "image": ""
#         }
#     ]
#     with open(PROJECTS_JSON, "w", encoding="utf-8") as f:
#         json.dump(sample_projects, f, indent=2)

# # ---------- FastAPI setup ----------
# app = FastAPI(title="Indrajeet Kumbhar — AI/ML Portfolio")

# # Serve static files
# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# # Jinja2 setup
# templates = Jinja2Templates(directory=TEMPLATES_DIR)

# # ✅ Global Jinja variable for current year
# def get_current_year():
#     return datetime.now().year

# templates.env.globals["current_year"] = get_current_year


# # ---------- Helper Functions ----------
# def send_notification_email(subject: str, body: str, from_email: str = None):
#     """Send an email notification using configured SMTP settings"""
#     if not SMTP_PASSWORD:
#         error_msg = """
#         EMAIL_PASSWORD environment variable not set!
        
#         To fix this:
#         1. Generate a Gmail App Password:
#            - Go to https://myaccount.google.com/security
#            - Enable 2-Step Verification if not enabled
#            - Go to 'App passwords' under 2-Step Verification
#            - Select 'Mail' and 'Windows Computer'
#            - Click 'Generate' to get a 16-character password
        
#         2. Set the environment variable:
#            In PowerShell, run:
#            $env:EMAIL_PASSWORD = "your-16-character-app-password"
#         """
#         print(error_msg)
#         return False
        
#     try:
#         print(f"Attempting to send email to {NOTIFICATION_EMAIL}")
#         msg = MIMEMultipart()
#         msg['From'] = SMTP_USERNAME  # Always use your Gmail address as sender
#         msg['To'] = NOTIFICATION_EMAIL
#         msg['Subject'] = subject
        
#         # Add a more professional email body
#         email_body = f"""
#         New Contact Form Submission

#         {body}

#         ---
#         This is an automated notification from your portfolio website.
#         """
#         msg.attach(MIMEText(email_body, 'plain'))
        
#         print("Connecting to Gmail SMTP server...")
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             print("Starting TLS encryption...")
#             server.starttls()
#             print("Attempting login...")
#             server.login(SMTP_USERNAME, SMTP_PASSWORD)
#             print("Sending email...")
#             server.send_message(msg)
#             print(f"✅ Email sent successfully to {NOTIFICATION_EMAIL}")
#         return True
#     except smtplib.SMTPAuthenticationError as auth_error:
#         print(f"""
#         ❌ Gmail authentication failed!
#         Error: {str(auth_error)}
        
#         Common issues:
#         1. App Password not set correctly
#         2. Using regular Gmail password instead of App Password
#         3. 2-Step Verification not enabled
        
#         Please follow the setup steps above to fix this.
#         """)
#         return False
#     except Exception as e:
#         print(f"❌ Failed to send email: {str(e)}")
#         return False

# def read_projects():
#     with open(PROJECTS_JSON, "r", encoding="utf-8") as f:
#         return json.load(f)

# def read_messages():
#     with open(MESSAGES_JSON, "r", encoding="utf-8") as f:
#         return json.load(f)

# def append_message(msg: dict):
#     messages = read_messages()
#     messages.append(msg)
#     with open(MESSAGES_JSON, "w", encoding="utf-8") as f:
#         json.dump(messages, f, indent=2)

# def list_blog_files():
#     files = []
#     for fn in os.listdir(BLOG_DIR):
#         if fn.endswith(".md"):
#             files.append(fn)
#     files.sort(reverse=True)
#     return files

# def read_blog_markdown(filename):
#     path = os.path.join(BLOG_DIR, filename)
#     if not os.path.exists(path):
#         raise FileNotFoundError
#     with open(path, "r", encoding="utf-8") as f:
#         text = f.read()
#     html = markdown.markdown(text, extensions=["fenced_code", "codehilite"])
#     title = filename.replace(".md", "")
#     for line in text.splitlines():
#         if line.strip().startswith("# "):
#             title = line.strip().lstrip("# ").strip()
#             break
#     return {"title": title, "html": html, "raw": text, "filename": filename}


# # ---------- Web Pages ----------
# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     projects = read_projects()[:3]  # show first 3 projects
#     return templates.TemplateResponse(
#         "index.html",
#         {
#             "request": request,
#             "featured": projects,
#             "profile_photo": "/static/images/indra.jpg",  # ✅ your image
#         },
#     )

# @app.get("/about", response_class=HTMLResponse)
# async def about(request: Request):
#     return templates.TemplateResponse("about.html", {"request": request})

# @app.get("/projects", response_class=HTMLResponse)
# async def projects_page(request: Request):
#     projects = read_projects()
#     return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})

# @app.get("/project/{project_id}", response_class=HTMLResponse)
# async def project_detail(request: Request, project_id: str):
#     projects = read_projects()
#     project = next((p for p in projects if p["id"] == project_id), None)
#     if not project:
#         raise HTTPException(status_code=404, detail="Project not found")
#     return templates.TemplateResponse("project_detail.html", {"request": request, "project": project})

# @app.get("/blog", response_class=HTMLResponse)
# async def blog_list(request: Request):
#     files = list_blog_files()
#     posts = []
#     for fn in files:
#         meta = read_blog_markdown(fn)
#         posts.append({"title": meta["title"], "filename": fn})
#     return templates.TemplateResponse("blog_list.html", {"request": request, "posts": posts})

# @app.get("/blog/{post_filename}", response_class=HTMLResponse)
# async def blog_post(request: Request, post_filename: str):
#     if not post_filename.endswith(".md"):
#         post_filename_full = f"{post_filename}.md"
#     else:
#         post_filename_full = post_filename
#     try:
#         meta = read_blog_markdown(post_filename_full)
#     except FileNotFoundError:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return templates.TemplateResponse("blog_post.html", {"request": request, "post": meta})

# @app.get("/resume", response_class=FileResponse)
# async def download_resume():
#     resume_path = os.path.join(STATIC_DIR, "resume.pdf")
#     if not os.path.exists(resume_path):
#         raise HTTPException(status_code=404, detail="Resume not found. Place `resume.pdf` in static/ directory.")
#     return FileResponse(resume_path, media_type="application/pdf", filename="resume.pdf")


# # New: Render an embedded resume viewer page so users can view the PDF in-browser
# @app.get("/resume/view", response_class=HTMLResponse)
# async def resume_view(request: Request):
#     resume_path = "/static/resume.pdf"
#     # The template will embed the PDF using <embed> or provide a download fallback
#     return templates.TemplateResponse("resume.html", {"request": request, "resume_path": resume_path})

# @app.get("/contact", response_class=HTMLResponse)
# async def contact_get(request: Request):
#     return templates.TemplateResponse("contact.html", {"request": request})


# # ---------- API Endpoints ----------
# class ContactIn(BaseModel):
#     name: str
#     email: EmailStr  # This adds email validation
#     message: str

# @app.post("/api/contact")
# async def api_contact(contact: ContactIn):
#     msg = {
#         "id": str(uuid.uuid4()),
#         "name": contact.name,
#         "email": contact.email,
#         "message": contact.message,
#         "received_at": datetime.utcnow().isoformat() + "Z",
#     }
#     append_message(msg)
    
#     # Send email notification
#     subject = f"New Contact Form Message from {contact.name}"
#     body = f"""New message received from your portfolio website:
    
# Name: {contact.name}
# Email: {contact.email}
# Message:
# {contact.message}

# Sent at: {msg['received_at']}
# """
#     email_sent = send_notification_email(subject, body, contact.email)
    
#     return {
#         "status": "ok", 
#         "message": "Message received and notification sent" if email_sent else "Message received but notification failed"
#     }

# @app.get("/api/projects")
# async def api_projects():
#     return read_projects()

# @app.get("/api/project/{project_id}")
# async def api_project(project_id: str):
#     projects = read_projects()
#     project = next((p for p in projects if p["id"] == project_id), None)
#     if not project:
#         raise HTTPException(status_code=404, detail="Project not found")
#     return project

# @app.get("/api/blogs")
# async def api_blogs():
#     files = list_blog_files()
#     result = []
#     for fn in files:
#         meta = read_blog_markdown(fn)
#         result.append({"title": meta["title"], "filename": fn})
#     return result

# @app.get("/api/messages")
# async def api_messages():
#     # ⚠️ Only for demo, no authentication
#     return read_messages()

# # ---------- Health Check ----------
# @app.get("/health")
# async def health():
#     return {"status": "ok"}

# # Test email endpoint (remove in production)
# @app.get("/api/test-email")
# async def test_email():
#     """Test the email configuration"""
#     if not SMTP_PASSWORD:
#         return {
#             "status": "error",
#             "message": "EMAIL_PASSWORD not set. Please set it first."
#         }
    
#     success = send_notification_email(
#         "Test Email from Portfolio Website",
#         "This is a test email to verify your email configuration is working correctly."
#     )
    
#     if success:
#         return {
#             "status": "success",
#             "message": "Test email sent successfully! Check your inbox."
#         }
#     else:
#         return {
#             "status": "error",
#             "message": "Failed to send test email. Check the server logs for details."
#         }


from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from typing import List
import json
import os
import uuid
import markdown
from datetime import datetime
from dotenv import load_dotenv
import httpx   # async http client for SendGrid API

# Load .env (for local/dev). In production use Render secrets/env vars instead.
load_dotenv()

# ---------- Email / SendGrid config ----------
SENDGRID_API_KEY = os.getenv("sendgridapi")        # set this in .env or Render secrets
SENDGRID_FROM_EMAIL = "indrajeetkumbhar23121@gmail.com"
NOTIFICATION_EMAIL = "indrajeetkumbhar23121@gmail.com" # recipient

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
            "id": "fake-news-bert",
            "title": "Fake News Detection (BERT)",
            "summary": "Fine-tuned BERT model to detect fake news articles.",
            "stack": ["Hugging Face", "Transformers", "PyTorch", "FastAPI"],
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


# ---------- Helper Functions (SendGrid) ----------
async def send_notification_email(subject: str, body: str, from_email: str | None = None, to_email: str | None = None):
    """
    Send email via SendGrid API.
    Returns True on success, False on failure.
    """
    if not SENDGRID_API_KEY:
        print("❌ SENDGRID_API_KEY is not set. Please set it in environment or .env.")
        return False

    from_email = SENDGRID_FROM_EMAIL
    to_email = to_email or NOTIFICATION_EMAIL

    url = "https://api.sendgrid.com/v3/mail/send"
    payload = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": subject
            }
        ],
        "from": {"email": from_email},
        "content": [
            {"type": "text/plain", "value": body},
            {"type": "text/html", "value": "<pre style='white-space:pre-wrap'>{}</pre>".format(body)}
        ]
    }
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            r = await client.post(url, json=payload, headers=headers)
            if 200 <= r.status_code < 300:
                print(f"✅ SendGrid accepted message to {to_email} (status {r.status_code})")
                return True
            else:
                print(f"❌ SendGrid failed: status={r.status_code}, body={r.text}")
                return False
    except Exception as e:
        print("❌ Exception sending via SendGrid:", str(e))
        return False


# ---------- File helpers (unchanged) ----------
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


@app.get("/resume/view", response_class=HTMLResponse)
async def resume_view(request: Request):
    resume_path = "/static/resume.pdf"
    return templates.TemplateResponse("resume.html", {"request": request, "resume_path": resume_path})

@app.get("/contact", response_class=HTMLResponse)
async def contact_get(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


# ---------- API Endpoints ----------
class ContactIn(BaseModel):
    name: str
    email: EmailStr  # This adds email validation
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
    
    # Send email notification (async)
    subject = f"New Contact Form Message from {contact.name}"
    body = f"""New message received from your portfolio website:
    
Name: {contact.name}
Email: {contact.email}
Message:
{contact.message}

Sent at: {msg['received_at']}
"""
    email_sent = await send_notification_email(subject, body, from_email=contact.email, to_email=NOTIFICATION_EMAIL)
    
    return {
        "status": "ok", 
        "message": "Message received and notification sent" if email_sent else "Message received but notification failed"
    }

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

# Test email endpoint (remove in production)
@app.get("/api/test-email")
async def test_email():
    """Test the email configuration"""
    if not SENDGRID_API_KEY:
        return {
            "status": "error",
            "message": "SENDGRID_API_KEY not set. Please set it first."
        }
    
    success = await send_notification_email(
        "Test Email from Portfolio Website",
        "This is a test email to verify your email configuration is working correctly."
    )
    
    if success:
        return {
            "status": "success",
            "message": "Test email sent successfully! Check your inbox."
        }
    else:
        return {
            "status": "error",
            "message": "Failed to send test email. Check the server logs for details."
        }
