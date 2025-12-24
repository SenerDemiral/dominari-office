# fastapi-app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict
from database import db  # Veritabanı pool'unun olduğu yer
from routers.auth import get_current_user  # JWT/Auth servisinden gelen fonksiyon

router = APIRouter(prefix="/api/users", tags=["users"])

# Request (İstek) gövdesi için Pydantic modeli
class PasswordReset(BaseModel):
    new_password: str

@router.put("/me/password")
async def reset_my_password(
    data: PasswordReset, 
    current_user: dict = Depends(get_current_user)
):
    async with db.pool.acquire() as conn:
        # PostgreSQL fonksiyonunu çağırıyoruz
        row = await conn.fetchrow(
            "SELECT * FROM fn_update_user_password($1, $2)",
            current_user["id"], data.new_password
        )
        
        if row and row['res_status'] == 'success':
            return {
                "status": "success",
                "message": row['res_message']
            }
            
        raise HTTPException(status_code=400, detail="Şifre güncellenemedi.")