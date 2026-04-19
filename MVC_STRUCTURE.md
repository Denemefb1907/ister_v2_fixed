# İster Yönetimi v2 - MVC Mimarisi

Uygulamanız MVC (Model-View-Controller) design pattern'ına göre yeniden yapılandırılmıştır.

## 📁 Proje Yapısı

```
ister_yonetimi_v2/
├── app/                          # Uygulama paketi
│   ├── __init__.py              # Flask uygulamasını başlatıcı
│   ├── controllers/             # Controller'lar (Blueprint'ler)
│   │   ├── auth.py              # Kimlik doğrulama
│   │   ├── main.py              # Ana sayfa ve navigasyon
│   │   ├── platform_api.py      # Platform API'si
│   │   ├── config_api.py        # Konfigürasyon API'si
│   │   ├── level_api.py         # Seviye API'si
│   │   ├── requirement_api.py   # İster API'si
│   │   ├── test_api.py          # Test API'si
│   │   ├── ta_api.py            # TA Dokuman API'si
│   │   ├── dashboard_api.py     # Dashboard API'si
│   │   └── comparison_api.py    # Karşılaştırma API'si
│   ├── models/                  # Model'ler (İş Mantığı)
│   │   ├── base.py              # Temel Model sınıfı
│   │   ├── user.py              # Kullanıcı Modeli
│   │   ├── platform.py          # Platform Modeli
│   │   ├── configuration.py     # Konfigürasyon Modeli
│   │   ├── level.py             # Seviye Modeli
│   │   ├── requirement.py       # İster Modeli
│   │   ├── test.py              # Test Modeli
│   │   ├── ta.py                # TA Modeli
│   │   └── dashboard.py         # Dashboard Modeli
│   └── utils/                   # Yardımcı fonksiyonlar
│       ├── auth.py              # Kimlik doğrulama utilleri
│       ├── database.py          # Veritabanı bağlantısı
│       ├── logging.py           # Günlük sistemи
│       └── helpers.py           # Genel yardımcı fonksiyonlar
├── templates/                   # HTML şablonları (değiştirilmedi)
├── static/                      # Statik dosyalar (JS, CSS, vb.)
├── config.py                    # Konfigürasyon dosyası
├── run.py                       # Uygulama başlatıcı
├── requirements.txt             # Python bağımlılıkları
├── README.md                    # Bu dosya
└── ...

```

## 🏗️ MVC Yapısının Açıklaması

### 1. **Model** (`app/models/`)
- Veritabanı işlemleri ve iş mantığını içerir
- Her model bir veritabanı tablosu veya entity için sorumludur
- SQL sorgularını ve veri manipülasyonunu yönetir

**Modeller:**
- `UserModel` - Kullanıcı yönetimi
- `PlatformModel` - Platform yönetimi
- `ConfigurationModel` - Konfigürasyon yönetimi
- `LevelModel` - İster seviyeleri
- `RequirementModel` - İster ağacı ve hiyerarşi
- `TestModel` - Test aşamaları ve sonuçları
- `TAModel` - Traceability Matrix'ler
- `DashboardModel` - Raporlar ve metrikleri

### 2. **Controller** (`app/controllers/`)
- HTTP isteklerini işler
- Model'leri çağırır ve veri işler
- JSON API'si olarak çalışır
- Blueprint'ler şeklinde organize edilir

**Controller'lar:**
- `auth.py` - Giriş/Çıkış ve kimlik doğrulama
- `main.py` - Sayfa yönlendiricileri (View'ler)
- `platform_api.py` - Platform CRUD işlemleri
- `config_api.py` - Konfigürasyon CRUD işlemleri
- `level_api.py` - Seviye CRUD işlemleri
- `requirement_api.py` - İster CRUD işlemleri
- `test_api.py` - Test yönetimi
- `ta_api.py` - TA Dokuman yönetimi
- `dashboard_api.py` - Raporlar ve dashboard
- `comparison_api.py` - Karşılaştırma işlemleri

### 3. **View** (`templates/`)
- HTML şablonları (değiştirilmedi)
- Frontend ile etkileşim sağlar
- HTML, CSS ve JavaScript içerir

### 4. **Utils** (`app/utils/`)
- Yardımcı fonksiyonlar
- Cross-cutting concerns (kimlik doğrulama, logging, vb.)

**Utilities:**
- `auth.py` - Giriş gerekli dekoratörü
- `database.py` - Veritabanı bağlantısı yönetimi
- `logging.py` - Değişiklik günlüğü kaydı
- `helpers.py` - Genel yardımcı fonksiyonlar (metin benzerliği, vb.)

## 🚀 Başlatma

### Geliştirme Modu

```bash
python run.py --dev
```

- Debug modu açık olur
- Otomatik reload yapılır
- http://localhost:5000

### Üretim Modu

```bash
python run.py
```

- Waitress sunucusu kullanılır
- Debug modu kapalı
- Üretim ortamına hazır

## 📝 Dizin Yapısı İlişkileri

```
Client (Browser)
    ↓
Flask Routes (Controllers) ← Blueprints
    ↓
Models (Business Logic) ← Database Operations
    ↓
MySQL Database
```

## 🔄 Request Akışı Örneği

1. **Browser** → `/api/platform` isteği gönderir
2. **Controller** → `platform_api.py` isteği yakalır
3. **Model** → `PlatformModel` verileri getir
4. **Database** → SQL sorgusu çalıştır
5. **Model** → Verileri işle ve return et
6. **Controller** → JSON olarak yanıt düzenle
7. **Browser** → JSON yanıtı al

## 🔐 Güvenlik Özellikleri

- **Kimlik Doğrulama**: `@login_required` dekoratörü
- **Session Yönetimi**: Flask session ile
- **Günlük Kaydı**: Tüm değişiklikler kaydedilir
- **Hata Işleme**: Global error handlers

## 📊 Veritabanı Bağlantısı

- **Driver**: Flask-MySQLdb
- **Connection Pool**: MySQLdb
- **Konfigürasyon**: `config.py` dosyasında

## 🎛️ Konfigürasyon

`config.py` dosyasından:
- MySQL bağlantı bilgileri
- Flask ayarları
- Ortama özel konfigürasyonlar

Ortamlar:
- `development` - Geliştirme ortamı
- `production` - Üretim ortamı
- `testing` - Test ortamı

## 📚 Model Kullanım Örneği

```python
from app.models.platform import PlatformModel
from app.utils.database import mysql

model = PlatformModel(mysql)
platforms = model.get_all()
```

## 🔗 API Endpoint'leri

### Platform
- `GET /api/platform` - Tüm platformları getir
- `POST /api/platform` - Platform oluştur
- `PUT /api/platform/<id>` - Platform güncelle
- `DELETE /api/platform/<id>` - Platform sil

### Konfigürasyon
- `GET /api/konfig` - Konfigürasyonları getir
- `POST /api/konfig` - Konfigürasyon oluştur
- `PUT /api/konfig/<id>` - Konfigürasyon güncelle
- `DELETE /api/konfig/<id>` - Konfigürasyon sil

### İster
- `GET /api/platform/<id>/ister_agaci` - İster ağacı
- `POST /api/ister_node` - İster oluştur
- `PUT /api/ister_node/<id>` - İster güncelle
- `DELETE /api/ister_node/<id>` - İster sil

### Test
- `GET /api/test_sonuc` - Test sonuçları
- `POST /api/test_sonuc` - Test sonucu kaydet

### TA Dokuman
- `GET /api/platform/<id>/ta` - TA listesi
- `POST /api/platform/<id>/ta` - TA oluştur
- `PUT /api/ta/<id>` - TA güncelle

## ⚙️ Ortam Değişkenleri

```bash
FLASK_ENV=development          # development, production, testing
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DB=database_name
SECRET_KEY=your_secret_key
```

## 🧪 Yeniden Yapılandırma Avantajları

✅ **Kodun Ayrılması**: Models, Controllers, Views ayrı dizinler  
✅ **Tekrar Kullanılabilirlik**: Model'ler birden fazla Controller'da kullanılabilir  
✅ **Test Kolaylığı**: Her katman bağımsız test edilebilir  
✅ **Bakım Kolaylığı**: Değişiklikler izole ve yönetilebilir  
✅ **Skalabilite**: Yeni özellikler kolay eklenir  
✅ **Blueprint'ler**: Modüler yapı ve DRY prensibi  

## 📖 İlgili Dosyalar

- `templates/` - Tüm HTML şablonları (değiştirilmedi)
- `static/` - CSS, JavaScript, resimler
- `schema.sql` - Veritabanı şeması
- `requirements.txt` - Python paketi bağımlılıkları

---

**Versiyon**: 2.0 MVC  
**Son Güncelleme**: 2024
