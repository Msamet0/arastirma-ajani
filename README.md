# 🔬 Araştırma Ajanı (Research Agent)

LangGraph tabanlı yapay zeka destekli araştırma asistanı.

## 🚀 Hızlı Başlangıç (Docker ile)

### Gereksinimler
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) kurulu olmalı

### Kurulum

```bash
# 1. Projeyi klonla
git clone https://github.com/KULLANICI_ADIN/research_demo.git
cd research_demo

# 2. .env dosyası oluştur
cp .env.example .env
# Ardından .env dosyasını düzenleyip API anahtarlarını ekle

# 3. Çalıştır
docker-compose up --build
```

## 🔑 Gerekli API Anahtarları

`.env` dosyasında şu değişkenler olmalı:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## 🛠️ Geliştirme (Docker Olmadan)

Eğer Docker kullanmak istemiyorsan:

```bash
# uv paket yöneticisini kur
pip install uv

# Bağımlılıkları yükle
uv sync

# Çalıştır
uv run main.py
```

## 📁 Proje Yapısı

```
research_demo/
├── main.py              # Ana uygulama
├── Dockerfile           # Docker image tanımı
├── docker-compose.yml   # Docker servis konfigürasyonu
├── pyproject.toml       # Python bağımlılıkları
└── .env                 # API anahtarları (git'e eklenmez)
```
