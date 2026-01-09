# 1. İçinde Python olan hazır bir sistem seçiyoruz
FROM python:3.12-slim

# 2. 'uv' paket yöneticisini sisteme yüklüyoruz (Senin projen uv kullanıyor)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Konteyner içinde '/app' adlı bir klasör aç ve oraya yerleş
WORKDIR /app

# 4. Sadece kütüphane listelerini kopyala (Hız için)
COPY pyproject.toml uv.lock ./

# 5. Kütüphaneleri yükle
RUN uv sync --frozen

# 6. Projenin geri kalan dosyalarını (main.py vb.) kopyala
COPY . .

# 7. API port'unu dışa aç
EXPOSE 8000

# 8. FastAPI uygulamasını başlat
CMD ["uv", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]