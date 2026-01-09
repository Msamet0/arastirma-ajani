"""
FastAPI ile Araştırma Ajanı API'si
Kullanım: uv run uvicorn api:app --reload
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

# Mevcut ajan fonksiyonlarını import et
from main import create_graph
from langchain_core.messages import HumanMessage

# ═══════════════════════════════════════════════════════════
#                    FASTAPI UYGULAMASI
# ═══════════════════════════════════════════════════════════

app = FastAPI(
    title="🔬 Araştırma Ajanı API",
    description="LangGraph tabanlı yapay zeka destekli araştırma servisi",
    version="1.0.0",
)

# CORS ayarları (frontend'lerin erişimi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da kısıtla!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════
#                    PYDANTIC MODELLERİ
# ═══════════════════════════════════════════════════════════

class ArastirmaIstegi(BaseModel):
    """Araştırma isteği için model"""
    konu: str = Field(
        ..., 
        min_length=3, 
        max_length=500,
        description="Araştırılacak konu",
        examples=["Yapay zeka nedir?", "Python ile web geliştirme"]
    )

class ArastirmaSonucu(BaseModel):
    """Araştırma sonucu için model"""
    basarili: bool = Field(description="İşlem başarılı mı?")
    ozet: str = Field(description="Araştırma özeti (Markdown formatında)")
    revizyon_sayisi: int = Field(description="Yapılan revizyon sayısı")
    konu: str = Field(description="Araştırılan konu")

class SaglikDurumu(BaseModel):
    """Sağlık kontrolü için model"""
    status: str
    message: str

# ═══════════════════════════════════════════════════════════
#                       ENDPOINT'LER
# ═══════════════════════════════════════════════════════════

@app.get("/", tags=["Genel"])
def ana_sayfa():
    """API ana sayfası"""
    return {
        "mesaj": "🔬 Araştırma Ajanı API'sine Hoş Geldiniz!",
        "docs": "/docs",
        "saglik": "/saglik"
    }


@app.get("/saglik", response_model=SaglikDurumu, tags=["Genel"])
def saglik_kontrolu():
    """API'nin çalışıp çalışmadığını kontrol eder"""
    return SaglikDurumu(
        status="ok",
        message="API çalışıyor!"
    )


@app.post("/arastir", response_model=ArastirmaSonucu, tags=["Araştırma"])
async def arastir(istek: ArastirmaIstegi):
    """
    Verilen konu hakkında AI destekli araştırma yapar.
    
    - **konu**: Araştırılacak konu (3-500 karakter)
    
    Örnek:
    ```json
    {"konu": "Kuantum bilgisayarlar nasıl çalışır?"}
    ```
    """
    try:
        # Graf oluştur
        graph = create_graph()
        
        # Ajanı çalıştır
        result = graph.invoke({
            "messages": [HumanMessage(content=istek.konu)],
            "query": istek.konu,
            "research_data": "",
            "summary": "",
            "revision_count": 0
        })
        
        return ArastirmaSonucu(
            basarili=True,
            ozet=result["summary"],
            revizyon_sayisi=result["revision_count"],
            konu=istek.konu
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Araştırma sırasında hata oluştu: {str(e)}"
        )


# ═══════════════════════════════════════════════════════════
#                    ÇALIŞTIRMA (Opsiyonel)
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
