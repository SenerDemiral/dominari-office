# fastapi-app/routers/auth.py
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
import json
from database import db # database.py'dan havuzu çekiyoruz
from datetime import datetime

# app yerine router tanımlıyoruz
router = APIRouter(tags=["Auth"]) 

# Bu satır FastAPI'ye "Token'ı Header'dan al" emrini verir
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Token'dan user_id'yi çıkaran asıl kahraman
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Decode ederken senin SECRET_KEY ve algoritmanı kullanıyoruz
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # BURASI KRİTİK: Login'de "user_id" verdiğin için buradan da "user_id" ile alıyoruz
        u_id = payload.get("user_id") 
        
        if u_id is None:
            raise HTTPException(status_code=401, detail="Token içeriği hatalı")
            
        return {"id": int(u_id)} # Fonksiyonun geri kalanı için standart id dönüyoruz
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Yetkisiz erişim veya geçersiz token")


class LoginSchema(BaseModel):
    phone: str
    password: str

@router.post("/login") # @app değil @router
async def login(data: LoginSchema):
    print(f"Giriş isteği geldi: {data.phone}") # 1. Adım
    async with db.pool.acquire() as conn:
        print("DB bağlantısı alındı...") # 2. Adım
        result_raw = await conn.fetchval("SELECT fn_login($1, $2)", data.phone, data.password)
        print("DB'den yanıt geldi.") # 3. Adım
        if not result_raw:
            raise HTTPException(status_code=401, detail="Giriş başarısız")

        res = json.loads(result_raw) if isinstance(result_raw, str) else result_raw
        print("JSON parse edildi.") # 4. Adım

        if not res.get("success"):
            raise HTTPException(status_code=401, detail=res.get("message", "Hatalı giriş"))

        token_payload = {"user_id": res["user"]["id"]}
        print("Token hazırlanıyor...") # 5. Adım

        token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
        print("Token oluşturuldu!") # 6. Adım

        return {
            "token": token,
            "user": res["user"],
            "offices": res["offices"]
        }

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    try:
        async with db.pool.acquire() as conn:
            # Tek sorgu, tek paket!
            login_data_raw = await conn.fetchval("SELECT fn_virtual_login($1)", current_user["id"])
            
            # asyncpg bazen string döner, bazen dict döner. Garantiye alalım:
            if isinstance(login_data_raw, str):
                login_data = json.loads(login_data_raw)
            else:
                login_data = login_data_raw

            return login_data
    except Exception as e:
        print(f"Virtual Login Hatası: {e}")
        raise HTTPException(status_code=500, detail="Oturum tazelenemedi")
