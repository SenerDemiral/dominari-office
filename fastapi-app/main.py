# fastapi-app/main.py
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import db
from routers import auth, offices, users
from services.mail_service import send_welcome_email_task

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(title="Dominari SaaS API", root_path="/api", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Parçaları birleştiriyoruz
app.include_router(auth.router)
app.include_router(offices.router)
app.include_router(users.router)

@app.get("/health")
async def health():
    return {"status": "up"}


@app.get("/test-mail")
async def test_mail(background_tasks: BackgroundTasks):
    # Kendi mail adresini yaz buraya
    background_tasks.add_task(send_welcome_email_task, "sener@dominari.cloud", "Şener", "123456")
    return {"message": "Test maili kuyruğa atıldı, kontrol et!"}