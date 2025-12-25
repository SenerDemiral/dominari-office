# fastapi-app/routers/offices.py
import json
from typing import Optional
from fastapi import Depends, APIRouter, BackgroundTasks, HTTPException
from .auth import get_current_user
from pydantic import BaseModel
from database import db
from services.mail_service import send_welcome_email_task # Birazdan oluşturacağız

router = APIRouter(prefix="/offices", tags=["Offices"])

class ClientCreate(BaseModel):
    name: str
    phone: str
    email: str

class StaffCreate(BaseModel):
    name: str
    phone: str
    email: str
    is_bookable: bool = True  # Svelte'den gelen veriye uyum sağlıyoruz
    role: Optional[str] = None     # Varsayılan değerlerle hata almayı önlüyoruz

@router.get("/{office_id}/clients")
async def get_clients(office_id: int):
    async with db.pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM fn_get_office_clients($1)", office_id)
        return [dict(row) for row in rows]
    
@router.post("/{office_id}/clients")
async def create_client(office_id: int, client: ClientCreate):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM add_client_to_office($1, $2, $3, $4)", 
            office_id, client.name, client.phone, client.email
        )
        
        if row:
            return dict(row)
        
        raise HTTPException(status_code=500, detail="Müşteri eklenirken bir hata oluştu")

@router.get("/{office_id}/staff")
async def get_staff(office_id: int, current_user: dict = Depends(get_current_user)):
    try:
        async with db.pool.acquire() as conn:
            # SQL fonksiyonunu TABLE döndüğü için SELECT * FROM ile çağırıyoruz
            rows = await conn.fetch("SELECT * FROM fn_get_office_staff($1)", office_id)
            
            # Record nesnelerini dict'e çeviriyoruz
            return [dict(row) for row in rows]
    except Exception as e:
        print(f"Hata detayı: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/{office_id}/staff")
async def create_staff(office_id: int, staff: StaffCreate, background_tasks: BackgroundTasks):
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM add_staff_to_office($1, $2, $3, $4, $5)",
            office_id, staff.name, staff.phone, staff.email, staff.is_bookable
        )
        
        if row and row['res_status'] == 'success':
            # Her success durumunda şifre üretilmiştir, mail gönderilir.
            background_tasks.add_task(
                send_welcome_email_task, 
                staff.email, staff.name, row['res_password']
            )
            return dict(row)
        elif row and row['res_status'] == 'info':
            # Zaten personelmiş, sadece bilgiyi dönüyoruz.
            return dict(row)
            
        raise HTTPException(status_code=400, detail="İşlem başarısız.")

@router.patch("/staff/settings/{ou_id}")
async def update_staff_settings(ou_id: int, settings: dict):
    try:
        async with db.pool.acquire() as conn:
            # dict'i jsonb olarak gönderiyoruz
            success = await conn.fetchval(
                "SELECT fn_update_office_user_settings($1, $2)", 
                ou_id, json.dumps(settings)
            )
            return {"success": success}
    except Exception as e:
        print(f"Update Hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))