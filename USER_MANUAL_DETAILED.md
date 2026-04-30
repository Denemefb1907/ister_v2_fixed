# 📘 İster Yönetimi v2 - Kapsamlı Kullanıcı Kılavuzu (Detaylı)

**Versiyon:** 2.0 - Profesyonel Sürüm  
**Son Güncelleme:** Nisan 2025  
**Dil:** Türkçe  
**Mimarisi:** MVC + MySQL + Flask

---

## 📚 İçindekiler

- [Platform Yönetimi](#platform-yönetimi)
  - [Platform Oluşturma](#yeni-platform-oluşturma)
  - [Havuz Platform Tanımlama](#havuz-platform-tanımlama)
  - [Seviyeleri Ayarlama](#seviyeleri-ayarlama)
  - [Test Aşamaları](#test-aşamalarını-yönetme)
- [Konfigürasyon Yönetimi](#konfigürasyon-yönetimi)
  - [Konfigürasyon Oluşturma](#yeni-konfigürasyon-oluşturma)
  - [Platformlara Atama](#konfigürasyonları-platformlara-atama)
- [İster (Requirement) Yönetimi](#ister-requirement-yönetimi-detaylı)
  - [İster Ağacı Yapısı](#ister-ağacı-yapısı)
  - [İster Ekleme](#yeni-ister-ekleme-adım-adım)
  - [İster Düzenleme](#ister-düzenleme-detaylı)
  - [İster Silme](#ister-silme-kritik-işlem)
  - [İster Sıralama](#ister-sıralama)
  - [İster İçinde Tablo](#ister-içine-tablo-ekleme-design-element)
- [Test Yönetimi](#test-yönetimi-detaylı)
  - [Test Sonucu Girişi](#test-sonucu-girişi-adım-adım)
  - [Test Sonuçları Görüntüleme](#test-sonuçları-görüntüleme)
- [TA Dokümantasyon](#ta-dokümantasyon-detaylı)
  - [TA Oluşturma](#yeni-ta-oluşturma)
  - [TA'ya Veri Ekleme](#taveriş-ekleme)
  - [İsterlere Bağlama](#taveryı-isterlere-bağlama)
- [Karşılaştırma & Traceability](#karşılaştırma-ve-traceability-detaylı)
  - [Havuz Karşılaştırması](#havuz-ile-karşılaştırma)
  - [Traceability Matrisi](#traceability-matrisini-görüntüleme)
- [Raporlar ve Dashboard](#raporlar-ve-dashboard-detaylı)
  - [Dashboard Metrikleri](#proje-metrikleri-dashboard)
  - [Rapor Türleri](#mevcut-raporlar)
- [Kullanıcı Yönetimi](#kullanıcı-yönetimi-yönetici)
- [İleri Konular](#ileri-konular)
- [Sorun Giderme](#sorun-giderme)

---

### 🏗️ Teknik Mimarisi

```
┌──────────────────────────────────────────┐
│ Frontend (Templates)                     │
│ HTML5 + JavaScript + CSS3                │
│ (ister.html, platform.html, vb.)         │
└─────────────┬──────────────────────────────┘
              │ (AJAX/REST API)
┌─────────────▼──────────────────────────────┐
│ Backend (Flask + Blueprints)               │
│ Controllers/API:                           │
│ - requirement_api.py (İster Management)    │
│ - platform_api.py (Platform Management)    │
│ - test_api.py (Test Management)            │
│ - ta_api.py (TA Documentation)             │
│ - comparison_api.py (Karşılaştırma)        │
└─────────────┬──────────────────────────────┘
              │ (SQL Queries)
┌─────────────▼──────────────────────────────┐
│ Database (MySQL 8.0)                       │
│ Tables:                                    │
│ - ister_node (İsterler)                    │
│ - platform_list (Platformlar)              │
│ - test_asama (Test Aşamaları)              │
│ - test_sonuc (Test Sonuçları)              │
│ - ta_dokuman (TA Dokümantasyonu)           │
│ - ta_sgo_baglanti (TA-İster Bağlantısı)   │
│ - degisiklik_log (Denetim Günlüğü)        │
└───────────────────────────────────────────┘
```

### 📦 Ana Özellikler Özeti

| Özellik | Detay |
|---------|-------|
| **Platform Yönetimi** | Proje/ürün merkezî tanımlaması |
| **Hiyerarşik İster Ağacı** | Sınırsız derinlikteki ister yapısı |
| **Seviye Tanımlama** | İster seviyelerini kendileme özelleştirme |
| **Konfigürasyon** | Ürün varyantlarına özgü isterleri |
| **Test Yönetimi** | Farklı test aşamalarında sonuçları kayıt |
| **TA Dokümantasyonu** | Traceability matris oluşturma |
| **Karşılaştırma** | Benzerlik analizi (Levenshtein) |
| **Raporlar** | Proje durumu, test kapsama, onay raporları |
| **Denetim Günlüğü** | Tüm işlemlerin tarihçesi |
| **Kullanıcı Yönetimi** | Üyelik ve yetkilendirme |

---

## Platform Yönetimi

### 📍 Platform Sayfasına Erişim

**URL:** `http://localhost:5000/platform`  
**Navigasyon:** Ana Menü → Platform (veya Sol Menü)

### 🎯 Platform Nedir? (Teknik Açıklama)

```
Veritabanı Yapısı (platform_list Tablosu):
┌────────────────────────────────────────┐
│ PlatformID   │ 1                        │
│ PlatformAdi  │ "GIGN v3.1"              │
│ HavuzMu      │ 0 (Normal platform)      │
│ OlusturmaTarihi │ 2024-04-20 14:30      │
└────────────────────────────────────────┘

Platform İlişkiler:
GIGN v3.1 (PlatformID=1)
├─ Seviyeleri (seviye_tanim tablosu)
│  └─ SeviyeNo: 1,2,3,4
├─ Test Aşamaları (test_asama tablosu)
│  └─ Unit, Integration, System, etc.
├─ Konfigürasyonları (platform_konfig tablosu)
│  └─ Hangi konfigler uygulanır?
└─ İsterleri (ister_node tablosu)
   └─ Hiyerarşik ister ağacı
```

### ➕ Yeni Platform Oluşturma - Kapsamlı Adımlar

#### 1️⃣ Platformlar Sayfasını Aç
```
URL: http://localhost:5000/platform
Görünüm:
┌─────────────────────────────────────────────────────┐
│ Platform Yönetimi                                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│                               [+ Yeni Platform Ekle]│
│                                                     │
│ ┌─────────────────────────────────────────────┐     │
│ │ Platform Adı                  │ İşlemler    │     │
│ ├─────────────────────────────────────────────┤     │
│ │ GIGN v3.1              │ Düzenle | Sil | ⋯ │     │
│ │ Mobil App v1.0        │ Düzenle | Sil | ⋯ │      │
│ └─────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

#### 2️⃣ "Yeni Platform" Tıkla
Form açılır:

```
┌──────────────────────────────────────────┐
│ ✎ Yeni Platform Oluştur                  │
├──────────────────────────────────────────┤
│                                          │
│ Platform Adı:                           │
│ [GIGN v3.1________________________]      │
│                                          │
│                                         |
│                                          |
│                                          │
│ [   İptal   ]        [   Kaydet  ]      │
└──────────────────────────────────────────┘
```

#### 3️⃣ Gerekli Alanları Doldur

| Alan | Kuralı | Örnek |
|------|--------|-------|
| **Platform Adı** | Benzersiz, tanımlayıcı | "GIGN v3.1", "MÖP 2.0 Basic" |

#### 4️⃣ Arka Planda Veri Tabanı Saklama

```python
# backend/Flask API (platform_api.py):
@app.route('/api/platform', methods=['POST'])
@login_required
def create_platform():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO platform_list (PlatformAdi, HavuzMu) VALUES (%s, 0)",
        (data['PlatformAdi'],)
    )
    mysql.connection.commit()
    platform_id = cur.lastrowid  # Otomatik ID
    
    # Denetim Günlüğüne Kayıt:
    record_log('platform_list', platform_id, 'Platform', 
               '-', data['PlatformAdi'], LogType.CREATE.value)
    
    cur.close()
    return jsonify({'PlatformID': platform_id})
```

#### 5️⃣ Başarı ve Sonraki Adımlar

Platform oluşturulur ve listeye eklenir:

```
Sonraki Yapılacaklar:
1. Seviyeleri tanımla (İster hiyerarşisini oluştur)
2. Test aşamalarını tanımla
3. Konfigürasyonları ata
4. İsterler oluşturmaya başla
```

### 🔄 Havuz Platform Tanımlama - Özel İşlem

#### Havuz Platform Nedir?

```
Şekil: Havuz Platform Mimarisi
┌──────────────────────────────────────┐
│ HAVUZ PLATFORM (Merkezi)             │
│ ├─ g1 (Genel İster 1)                │
│ ├─ g2 (Genel İster 2)                │
│ ├─ g3 (Genel İster 3)                │
│ ├─ b1 (Branded İster 1)              │
│ └─ b2 (Branded İster 2)              │
└────────┬──────────────────────┬──────┘
         │ Kopyala              │ Kopyala
         ▼                      ▼
    ┌─────────────┐        ┌──────────────┐
    │ GIGN v3.1   │        │ MÖP v2.0     │
    │ (g1,g2,b1)  │        │ (g1,g2,g3)   │
    └─────────────┘        └──────────────┘
```

**Amaç:** Tüm projelerin ortak isterleri bir yerde olsun. Projeler gerekli olanları kopyalasın.

#### Havuz Platform Oluşturma

1. Normal platform oluştur (yukarıdaki adımları izle)
2. Platform Adı olarak: `Havuz`, `Genel Havuz`, veya `Common Pool` yazfb
3. Sistem otomatik tanır: `HavuzMu = 1` olur
4. Platformlar listesinde `(HAVUZ)` etiketi gösterilir

```
Platform Listesi:
┌─────────────────────────────────┬──────────┐
│ Platform Adı                    │ Tür      │
├─────────────────────────────────┼──────────┤
│ Havuz                (HAVUZ) ★   │ Merkezi  │
│ GIGN v3.1                       │ Normal   │
│ MÖP v2.0                        │ Normal   │
└─────────────────────────────────┴──────────┘
```

#### Havuz Platform'un İsterleri

Havuz platform'da isterler özel kodlarla yapırlandırılır:

```
G Tipi (Genel):  g1, g2, g3, g4, ...
B Tipi (Branded): b1, b2, b3, ...

Veritabanı:
ister_node.HavuzKodu = 'g1' (generic)
ister_node.HavuzKodu = 'b1' (branded)

Otomatik Numaralandırma:
Yeni g tipi ister eklersen:
└─ MAX(HavuzKodu) + 1
   MAX('g5')'nin sayısal kısmı = 5
   Yeni kod = 'g' + (5+1) = 'g6'
```
### 🗑️ Platform Silme - ⚠️ KRİTİK İŞLEM

#### Silme Öncesi Sistem Kontrolleri

```python
# Veritabanı Kontrolleri:
if platform_id == havuz_platform_id:
    ❌ FELİER: "Havuz platformu silinemez!"
    
if platform_da_ister_var():
    ⚠️ UYARI: f"{ister_sayisi} ister silinecek"
    ⚠️ UYARI: f"{test_sonuc_sayisi} test sonucu silinecek"
    ⚠️ UYARI: f"{ta_dokuman_sayisi} TA kaydı etkilenecek"
```

#### Silme Süreci

1. "**Sil**" tıkla
2. Onay Penceresi:

```
┌──────────────────────────────────┐
│ ⚠️  UYARI: Bu İşlem GERİ ALINAMAZ  │
├──────────────────────────────────┤
│                                  │
│ Platform "GIGN v3.1" silmek      │
│ istediğinizden emin misiniz?     │
│                                  │
│ Silinecek Veriler:               │
│ • 156 ister                       │
│ • 343 test sonucu                │
│ • 12 TA dokümantasyonu           │
│ • Tüm ilişkili veriler           │
│                                  │
│ [Vazgeç]      [Evet, Sil]       │
└──────────────────────────────────┘
```

3. "**Evet, Sil**" tıklanırsa kaskad silme başlar:

```sql
-- Backend Silme Kodu:
BEGIN TRANSACTION;

-- 1. İster bağlantılarını temizle
DELETE FROM ta_sgo_baglanti WHERE NodeID IN (
    SELECT NodeID FROM ister_node WHERE PlatformID=?
);

-- 2. Test sonuçlarını sil
DELETE FROM test_sonuc WHERE NodeID IN (
    SELECT NodeID FROM ister_node WHERE PlatformID=?
);

-- 3. Firma görüşlerini sil
DELETE FROM firma_gorusu WHERE NodeID IN (
    SELECT NodeID FROM ister_node WHERE PlatformID=?
);

-- 4. İster onaylarını sil
DELETE FROM ister_onay WHERE NodeID IN (
    SELECT NodeID FROM ister_node WHERE PlatformID=?
);

-- 5. İsterleri sil
DELETE FROM ister_node WHERE PlatformID=?;

-- 6. Test aşamalarını sil
DELETE FROM test_asama WHERE PlatformID=?;

-- 7. Seviyeleri sil
DELETE FROM seviye_tanim WHERE PlatformID=?;

-- 8. Platform-Konfigürasyon bağlantılarını sil
DELETE FROM platform_konfig WHERE PlatformID=?;

-- 9. Son olarak platformu sil
DELETE FROM platform_list WHERE PlatformID=?;

-- Denetim Günlüğü:
INSERT INTO degisiklik_log (...) VALUES (
    'platform_list', ?, 'Platform', 'GIGN v3.1', '-', 'DELETE'
);

COMMIT;
```

### 📋 Seviyeleri Ayarlama - Platform İçinde

#### Seviyeler Nedir?

Seviyeleri ister hiyerarşisini tanımlar:

```
Sistem Gerekliliği (Level 1)
│ ├─ Üst Sistem Gerekliliği (Level 2)
│ │  ├─ Modül Gerekliliği (Level 3)
│ │  │  └─ Komponent Gerekliliği (Leveli 4)

Veritabanı (seviye_tanim):
├── SeviyeID
├── PlatformID
├── SeviyeNo (1, 2, 3, 4, ...)
├── SeviyeAdi ("Sistem", "Alt Sistem", ...)
└── OlusturmaTarihi
```

#### Mevcut Seviyeleri Görüntüleme

Platform → **"Seviyeler"** sekmesi

```
┌────────┬─────────────────────────────────┐
│ No     │ Seviye Adı                      │
├────────┼─────────────────────────────────┤
│ 1      │ Sistem Gerekliliği              │
│ 2      │ Alt Sistem Gerekliliği          │
│ 3      │ Modül Gerekliliği               │
│ 4      │ Komponent Gerekliliği           │
└────────┴─────────────────────────────────┘
```

#### Yeni Seviye Ekleme

1. "+Ekle" tıkla
2. Form:
```
Seviye Adı: [___________________]
[İptal]  [Kaydet]
```
3. Seviye adı gir: "Yazılım Modülü", "Komponent", "Özellik", etc.
4. "Kaydet" tıkla

## Konfigürasyon Yönetimi 

### 📍 Konfigürasyon Sayfasına Erişim

**URL:** `http://localhost:5000/konfig`  
**Navigasyon:** Ana Menü → Konfigürasyon

### ➕ Yeni Konfigürasyon Oluşturma

Konfigürasyon Sayfası:

```
┌──────────────────────────────────────────┐
│ Konfigürasyon Yönetimi                   │
├──────────────────────────────────────────┤
│                                          │
│ [Ara...]                                 │
│                                          │
│ Mevcut Konfigürasyonlar:                 │
│ ┌──────────────────────────────────┐     │
│ │ #   │ Konfigürasyon Adı│İşlem    │     │
│ ├──────────────────────────────────┤     │
│ │ GIGN 3.1 TR │ 2024-03-2│Düz|Sil  │     │
│ │ GIGN 3.1 EN │ 2024-03-20│Düz|Sil │     │
│ │ MÖP 2.0 Pro │ 2024-04-10│Düz|Sil │     │
│ └──────────────────────────────────┘     │
└──────────────────────────────────────────┘
```

#### Adımlar

1. "** + Yeni Konfigürasyon **" tıkla
2. Form açılır:

```
┌──────────────────────────────────────┐
│ Yeni Konfigürasyon Ekle              │
├──────────────────────────────────────┤
│ Konfigürasyon Adı: *                 │
│ [ ____________ ]                     │
│                                      │
│   [İptal]        [Kaydet]            │
│                                      │
│                                      │
│                                      │
└──────────────────────────────────────┘
```
3. Adı girdikten sonra kaydete tıklayın.
4. Veritabanına kaydedilir.

### ✏️ Konfigürasyon Düzenleme

Satırda "**Düzenle**" tıkla 
Metni değiştirin ve "Kaydet" tıklayın.

### 🗑️ Konfigürasyon Silme

Satırda "**Sil**" tıkla:

⚠️ Onay Penceresi:

Sil?

[OK]  [Cancel]

**Silme Kuralları:**
- Bir konfigürasyon eğer hiç istere atanmamışsa kolayca silinebilir
- Eğer istere atanmışsa error verilir:
  ```
  ❌ HATA: Bu konfigürasyon {sayı} istere atanmış, silinemez!
  ```

### 🔗 Konfigürasyonları Platformlara Atama 

Platform → **"Konfigürasyonlar"** sekmesi

```
Platform: GİGN v3.1

Atanabilir Konfigürasyonlar Listesi:
┌─────────────────────┐
│ ☐ GIGN v3.1 TR  │
│ ☑ GIGN v3.1 EN  │
│ ☐ MÖP 2.0 Pro   │
│ ☐ iOS v1.0      │
└─────────────────────┘

[Kaydet]
```
Atanacak konfigleri seçin (checkbox):
- GIGN v3.1 TR → ☑
- GIGN v3.1 EN → ☑
  
---

## İster Yönetimi

### 📍 İster Sayfasına Erişim

**URL:** `http://localhost:5000/ister`  
**Navigasyon:** Ana Menü → İster Ağacı

### 🎯 İster Ağacı Yapısı - Kapsamlı

#### İster Tipi

```
İster Tipi = 'B' (Başlık / Branch)
└─ Alt isterler gruplaştıran başlık
   IsterTipi köyünde 'B' olur
   Kendisi de bir isterdir (parasite yok)

İster Tipi = 'G' (Genel / General)
└─ Normal, yapılması gereken bir fonksiyon
   Test edilebilir, ölçülebilir
   Veritabanında IsterTipi = 'G'
```

#### Örnek Ister Ağacı

```
Platform: GIGN v3.1

1. Başlangıç Kontrolleri (B=Başlık, Level=1, SiraNo=1)
   ├─ 1.1 Sistem Başlatması (G=Genel, Level=2, SiraNo=1)
   ├─ 1.2 Tan Kontrolleri (G=Genel, Level=2, SiraNo=2)
   └─ 1.3 Sıcaklık Ölçümü (G=Genel, Level=2, SiraNo=3)

2. Çalışma Modları (B=Başlık, Level=1, SiraNo=2)
   ├─ 2.1 Normal İşletim (G=Genel, Level=2, SiraNo=1)
   │   ├─ 2.1.1 Veri Toplama (G=Genel, Level=3, SiraNo=1)
   │   └─ 2.1.2 Analiz (G=Genel, Level=3, SiraNo=2)
   └─ 2.2 Tanı Veri Oku (G=Genel, Level=2, SiraNo=2)

3. Hatalar (B=Başlık, Level=1, SiraNo=3)
   └─ 3.1 Sistem Kapanması (G=Genel, Level=2, SiraNo=1)

Veritabanı İlişkileri:
NodeID | ParentID | SeviyeNo | Icerik
1      | NULL     | 1        | "Başlangıç Kontrolleri"
2      | 1        | 2        | "Sistem Başlatması"
3      | 1        | 2        | "Tan Kontrolleri"
4      | NULL     | 1        | "Çalışma Modları"
5      | 4        | 2        | "Normal İşletim"
```

### ➕ Yeni İster Ekleme - Adım Adım

#### 1️⃣ Platform Seç

```
Sayfa Yapısı:
┌────────────────────────────────────────┐
│ Platform: [GIGN v3.1 ▼]               │
│            (Otomatik yükle)            │
└────────────────────────────────────────┘

Sol Panel:            Sağ Panel:
─────────────        ──────────
Ister Ağacı          Seçilen İster Detayları
```

#### 2️⃣ Başlık İsteri Ekleme

Platform seçilir seçilmez:

```
Sol Panel Butonları:
[+ Başlık Ekle] [+ İster Ekle]
```

"**+ Başlık Ekle**" tıkla:

```
┌─────────────────────────────────────┐
│ Yeni Başlık İsteri Ekle              │
├─────────────────────────────────────┤
│ Platform: GIGN v3.1       ✓ (sabit) │
│ Seviye: [Sistem Gerekliliği ▼]      │
│ İster Tipi: ◉ Başlık  ○ Normal      │
│ Başlık: [_________________]         │
│ Konfigürasyonlar:                   │
│   ☐ GIGN v3.1 TR                    │
│   ☐ GIGN v3.1 EN                    │
│ Test Yöntemi: [Seçiniz ▼]           │
│ Açıklama: [________________]         │
│                                      │
│ [Vazgeç]           [Ekle]           │
└─────────────────────────────────────┘
```

Doldur:
- **Seviye:** "Sistem Gerekliliği" (ilk seviye)
- **İster Tipi:** Başlık seçili
- **Başlık:** "Başlangıç Kontrolleri"
- **Konfigürasyonlar:** Seçilmeye bırak (tüm konfig için)

"**Ekle**" tıkla

**Backend İşlemi:**
```python
# 1. Numarası otomatik üret
if not parent_id:  # Root başlık
    # Mevcut başlık count'ını al
    cur.execute("SELECT COUNT(*) as cnt FROM ister_node 
                 WHERE PlatformID=%s AND ParentID IS NULL", (platform_id,))
    count = cur.fetchone()['cnt']
    node_number = str(count + 1)  # "1", "2", "3", ...
else:
    # Alt ister
    parent_node = get_node(parent_id)
    parent_number = parent_node['NodeNumarasi']
    # Alt count'ını al
    cur.execute("SELECT COUNT(*) as cnt FROM ister_node 
                 WHERE ParentID=%s", (parent_id,))
    count = cur.fetchone()['cnt']
    node_number = f"{parent_number}.{count + 1}"  # "1.1", "1.2", ...

# 2. SiraNo auto-increment
cur.execute("SELECT COALESCE(MAX(SiraNo), 0) + 1 as next_sira " +
              "FROM ister_node WHERE ParentID IS NULL AND PlatformID=%s",
              (platform_id,))
sira_no = cur.fetchone()['next_sira']

# 3. Insert
cur.execute("""INSERT INTO ister_node (
    PlatformID, SeviyeID, ParentID, NodeNumarasi,
    IsterTipi, Icerik, SiraNo, KonfigID, OlusturanID
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
    (platform_id, level_id, None, node_number,
     'B', 'Başlangıç Kontrolleri', sira_no,
     config_id, session['kullanici_id'])
)
new_node_id = cur.lastrowid

# 4. Denetim Günlüğü
record_log('ister_node', new_node_id, 'Node', 
           '-', 'Başlangıç Kontrolleri', LogType.CREATE.value)
```

**Sonuç:** Sol panele başlık eklenir:

```
Sol Panel:
┌────────────────────────────────┐
│ 📦 1. Başlangıç Kontrolleri     │
│                                │
│ Seçiniz veya alt ister ekleyin!│
│ [+ Alt İster Ekle]             │
└────────────────────────────────┘
```

#### 3️⃣ Alt İster Ekleme

Başlığa sağ tık yap veya başlığın yanındaki **"+ Alt İster"** tıkla:

```
┌──────────────────────────────────┐
│ Yeni Alt İster Ekle              │
├──────────────────────────────────┤
│ Üst İster: 1. Başlangıç...  ✓    │
│ Seviye: [Alt Sistem ▼]           │
│ İster Tipi: ○ Başlık ◉ Normal    │
│ İster No: 1.1 (otomatik) ✓       │
│ Başlık: [Sistem Başlatması__]    │
│ Konfigürasyon: [GIGN 3.1 TR seçili
│ Test Yöntemi: [Black Box ▼]      │
│ Açıklama: [Sistem başlatıldık... ]
│                                  │
│ [Vazgeç]          [Ekle]        │
└──────────────────────────────────┘
```

Doldur ve Ekle tıkla.

**Backend:**
```python
# parentID avtomatik doldurulur
parent_id = request.json['ParentID']  # Üst ister NodeID'si
parent_node = get_node(parent_id)
parent_number = parent_node['NodeNumarasi']  # "1"

# Alt işter sayısını bul
cur.execute("SELECT COUNT(*) + 1 as next_sub FROM ister_node 
             WHERE ParentID=%s", (parent_id,))
sub_count = cur.fetchone()['next_sub']  # 1

# Numara: parent.sub = "1.1"
new_number = f"{parent_number}.{sub_count}"

# Insert
cur.execute("""INSERT INTO ister_node (...) VALUES (...)""",
    (platform_id, level_id, parent_id, new_number,
     'G', 'Sistem Başlatması', 1, config_id, session['kullanici_id'])
)
```

**Sonuç:** Ağaca eklenir:

```
Sol Panel:
┌──────────────────────────────────┐
│ 📦 1. Başlangıç Kontrolleri      │
│    ├─ 1.1 Sistem Başlatması     │
│    │   [+ Alt Ekle]             │
│    └─ (Sağa kaydırıldı)         │
│                                 │
│ 📦 [+ Başlık Ekle]              │
└──────────────────────────────────┘
```

### ✏️ İster Düzenleme - Detaylı

#### Düzenlenecek İsteri Seç

Sol panelde isterin satırı üzerine git ve sağ tık yap:

```
1.1 Sistem Başlatması  [✏️] [🗑️] [⬆️⬇️]
```

#### Düzenleme Formunu Aç

"**✏️ Düzenle**" tıkla

```
┌──────────────────────────────────────┐
│ İster Düzenle: 1.1                   │
├──────────────────────────────────────┤
│ Numarası: 1.1 (değişebilir)           │
│ Başlık: [Sistem Başlatması_______]    │
│ Seviye: [Alt Sistem ▼]                │
│ Konfigürasyon: [GIGN 3.1 TR seçili]   │
│ Test Yöntemi: [Black Box seçili ▼]    │
│ Açıklama: [Sistem başlatıldığında...] │
│ İlgili Aşama: [İşletim Aşaması ▼]     │
│                                      │
│ [Vazgeç]           [Kaydet]         │
└──────────────────────────────────────┘
```

#### Değişiklik Yap

Örneğin açıklamayı uzat:

```
Eski: "Sistem başlatıldığında"
Yeni: "Sistem başlatıldığında tüm donanım kontrolleri yapılacak"
```

#### Kaydet

"**Kaydet**" tıkla

**Backend Update:**
```python
old_node = get_node_data(node_id)
updates = {}

for field in ['Icerik', 'SeviyeID', 'KonfigID', 'TestYontemiID', ...]:
    if field in request.json:
        new_val = request.json[field]
        old_val = old_node.get(field)
        if str(old_val or '') != str(new_val or ''):
            updates[field] = new_val
            # Log
            record_log('ister_node', node_id, field, 
                       old_val, new_val, LogType.UPDATE.value)

if updates:
    update_node(node_id, updates)
```

### 🗑️ İster Silme - Kritik

#### Silme Kuralları

```
if ister_grubu_ve_alt_ister_var:
    ❌ HATA: "Bu başlığın altında isterleri var!"
    → Çözüm: Alt isterleri bir sil, sonra başlığı sil

if ta_bakili_var:
    ⚠️ UYARI: "{n} TA'ya bağlı"
    → TA bağlantıları silinecek

if test_sonucu_var:
    ⚠️ UYARI: "{n} test sonucu silinecek"
```

#### Silemme Adımları

"🗑️ Sil" tıkla:

```
┌──────────────────────────────┐
│ ⚠️  UYARI                     │
├──────────────────────────────┤
│ "1.1 Sistem Başlatması"      │
│ isteirini silmek istediğiniz) │
│ emin misiniz?                │
│                              │
│ Silinecek Veriler:           │
│ • 1 ister                    │
│ • 5 test sonucu              │
│ • 2 TA bağlantısı           │
│                              │
│ Bu işlem GERİ ALINAMAZ!      │
│                              │
│ [Vazgeç]   [Evet, Sil]      │
└──────────────────────────────┘
```

"**Evet, Sil**" tıkla

**Backend Silme:**
```python
# Cascade silme
cur.execute("DELETE FROM ta_sgo_baglanti WHERE NodeID=%s", (node_id,))
cur.execute("DELETE FROM test_sonuc WHERE NodeID=%s", (node_id,))
cur.execute("DELETE FROM firma_gorusu WHERE NodeID=%s", (node_id,))
cur.execute("DELETE FROM ister_onay WHERE NodeID=%s", (node_id,))
cur.execute("DELETE FROM ister_tablo WHERE NodeID=%s", (node_id,))
cur.execute("DELETE FROM ister_node WHERE NodeID=%s", (node_id,))

# Log
record_log('ister_node', node_id, 'Node', 
           old_icerik, '-', LogType.DELETE.value)

mysql.connection.commit()
```

### 🔄 İster Sıralama

Sol panelinde isterler sıralanabilir:

```
1.1 Sistem Başlatması  [⬆️] [⬇️]
1.2 Tan Kontrolleri    [⬆️] [⬇️]
1.3 Sıcaklık Ölçümü   [⬆️] [⬇️]
```

**⬆️ Tıkla** = Birisini yukarı taşı

```python
# Veritabanı İşlemi:
current_node = get_node(node_id)
current_sira = current_node['SiraNo']

# Kardeş node'ları bul (aynı ParentID)
siblings = get_siblings(current_node['ParentID'])
current_idx = siblings.index(current_node)

# Hedef (yukarı): idx - 1
target_idx = current_idx - 1
target_node = siblings[target_idx]

# Sıraları değiştir
update_sira(current_node['NodeID'], target_node['SiraNo'])
update_sira(target_node['NodeID'], current_node['SiraNo'])
```

---

## Test Yönetimi - Detaylı

### 📍 Test Girişi Sayfasına Erişim

**URL:** `http://localhost:5000/test_girisi`  
**Navigasyon:** Ana Menü → Test Girişi

### 🎯 Test Yönetimi İş Akışı

```
İş Akışı:
1. Platform seç
   ↓
2. Test Aşaması seç (Unit, Integration, System, vb.)
   ↓
3. İster listesini gör
   ↓
4. Her ister için test sonucunu seç (Başarılı/Başarısız/Atlanmış)
   ↓
5. Kaydet
   ↓
6. Denetim Günlüğüne kaydı tutuluş

Veritabanı (test_sonuc):
├── TestSonucID (int, PK)
├── NodeID (fk → ister_node) - Hangi ister?
├── TestAsamaID (fk → test_asama) - Hangi aşama?
├── Sonuc (enum: 'P'=Pass, 'F'=Fail, 'S'=Skip)
├── KayitliyenID (fk → kullanici)
└── Tarih (datetime)
```

### ✅ Test Sonucu Girişi - Adım Adım

#### 1️⃣ Sayfayı Aç

Test Girişi sayfasında karşı gelene:

```
┌────────────────────────────────────────┐
│ Test Sonucu Girişi                     │
├────────────────────────────────────────┤
│ Platform: [GIGN v3.1 ▼]               │
│ Test Aşaması: [Unit Test ▼]           │
│                                        │
│ [Yükle]  [Tümü Başarılı] [Tümü Atla]  │
└────────────────────────────────────────┘

İster Listesi:
┌─────┬────────────────────┬──────────────┐
│ No  │ İster Başlığı      │ Test Sonucu  │
├─────┼────────────────────┼──────────────┤
│ 1.1 │ Sistem Başlaması   │ ( ) Seçiniz  │
│ 1.2 │ Tan Kontrolleri    │ ( ) Seçiniz  │
│ 1.3 │ Sıcaklık Ölçümü    │ ( ) Seçiniz  │
└─────┴────────────────────┴──────────────┘
```

#### 2️⃣ Platform & Aşama Seç

```
Platform: [GIGN v3.1 ▼] seç
Test Aşaması: [Unit Test ▼] seç

→ İster listesi otomatik yüklenecek
```

#### 3️⃣ Test Sonuçları Gir

Her satır için:

- **✅ Başarılı (Pass)** - Test geçti
- **❌ Başarısız (Fail)** - Test eşleşmedi
- **⏸️ Atlanmış (Skip)** - Test yapılmadı

```
1.1 Sistem Başlaması:    ◉ Başarılı
1.2 Tan Kontrolleri:     ○ Başarılı  ◉ Başarısız  ○ Atlanmış
1.3 Sıcaklık Ölçümü:     ◉ Başarılı
```

#### 4️⃣ Kaydet

Sayfanın altında:

```
[Kaydet]
```

Tıkla → Veritabanına insert/update:

```python
# Backend:
for item in request.json['test_results']:
    node_id = item['NodeID']
    phase_id = item['TestAsamaID']
    result = item['Sonuc']  # 'P', 'F', or 'S'
    
    # Varsa update, yoksa insert
    cur.execute("SELECT * FROM test_sonuc 
                 WHERE NodeID=%s AND TestAsamaID=%s",
                 (node_id, phase_id))
    existing = cur.fetchone()
    
    if existing:
        cur.execute("UPDATE test_sonuc SET Sonuc=%s, Tarih=NOW() 
                    WHERE NodeID=%s AND TestAsamaID=%s",
                    (result, node_id, phase_id))
        # Log UPDATE
    else:
        cur.execute("INSERT INTO test_sonuc (NodeID, TestAsamaID, Sonuc, Tarih) 
                    VALUES (%s, %s, %s, NOW())",
                    (node_id, phase_id, result))
        # Log INSERT

mysql.connection.commit()
```

### 📊 Test Sonuçları Görüntüleme

İster ağacında geri dön → Sağ tarafta test sonuçları gösterilir:

```
İster: "1.1 Sistem Başlatması"

Test Sonuçları:
┌──────────────────┬──────────┐
│ Test Aşaması     │ Sonuç    │
├──────────────────┼──────────┤
│ Unit Test        │ ✅ Geçti  │
│ Integration Test │ ❌ Başarısız│
│ System Test      │ ⏸️ Atlanmış │
└──────────────────┴──────────┘

Genel Durum: 33% (1/3 başarılı)
```

---

## TA Dokümantasyon - Detaylı

### 📍 TA Sayfasına Erişim

**URL:** `http://localhost:5000/raporlar` (veya ta_dokuman.html)  
**Navigasyon:** Ana Menü → TA Dokümantasyon

### 🎯 TA Nedir? (Traceability Alignment)

```
SORU: "Ister XYZ'nin test nasıl yapıldığını bilir misin?"

CEVAP: TA dokümantasyonu ile isterler → test adımlarına bağlanır.

Veritabanı (ta_dokuman):
├── TaID (int, PK)
├── PlatformID (fk)
├── SiraNo (1, 2, 3, ...)
├── Adi ("TA-GIGN-001")
├── Aciklama ("Systems Level TA")
├── Olusturmac Tarihi
└── DuzenlenmeTarihi

Veritabanı (ta_veri):
├── TaVeriID
├── TaID (fk → ta_dokuman)
├── Sistem (Test edilen bileşen)
├── Yon (Giriş/Çıkış)
├── Sira (1, 2, 3...)
└── Aciklama

Veritabanı (ta_sgo_baglanti):
├── BaglantıID
├── TaID (fk → ta_dokuman)
├── NodeID (fk → ister_node)
└── EklenmeTarihi
```

### ➕ Yeni TA Dokümantasyonu Oluşturma

```
TA Sayfası:
┌────────────────────────────────────────┐
│ TA Dokümantasyonu Yönetimi             │
├────────────────────────────────────────┤
│ Platform: [GIGN v3.1 ▼]               │
│ [+ Yeni TA Ekle]                      │
│                                        │
│ Mevcut TA'lar:                         │
│ ├─ TA-GIGN-001 (System Test)           │
│ ├─ TA-GIGN-002 (Integration)           │
│ └─ TA-GIGN-003 (Unit Test)            │
└────────────────────────────────────────┘
```

1. "**+ Yeni TA Ekle**" tıkla
2. Form açılır:

```
┌─────────────────────────────────────┐
│ Yeni TA Dokümantasyonu Oluştur       │
├─────────────────────────────────────┤
│ Platform: GIGN v3.1        ✓ (sabit)│
│ Sıra No: 1 (otomatik)      ✓        │
│ Adı: [TA-GIGN-001___________]       │
│ Açıklama: [System Level Test ___]   │
│ Versiyon: [1.0_______]              │
│                                     │
│ [Vazgeç]          [Oluştur]        │
└─────────────────────────────────────┘
```

3. Bilgileri doldur ve Oluştur tıkla
4. TA dokümantasyonu oluşturulur

### 📝 TA'ya Test Verileri Ekleme

TA oluşturulduktan sonra, test adımlarını ekle:

```
TA-GIGN-001 Detayı:

┌────────────┬──────────┬─────────┐
│ Sistem     │ Yön      │ Sıra    │
├────────────┼──────────┼─────────┤
│ (test edilen bileşen)        │
│ Giriş: (Giriş değerleri)     │
│ Çıkış: (Beklenen çıkış)      │
└────────────┴──────────┴─────────┘

[+ Test Adımı Ekle]
```

1. "**+ Veri Ekle**" tıkla
2. Form:

```
┌──────────────────────────────────────┐
│ Test Adımı Ekle                      │
├──────────────────────────────────────┤
│ Sistem: [Sensor_________________]   │
│ Yön: [Giriş ▼]                      │
│ Sıra No: 1                           │
│ Açıklama: [5V voltaj ver____________]
│                                      │
│ [Vazgeç]          [Ekle]             │
└──────────────────────────────────────┘
```

3. Doldur ve Ekle

Her test adımı TA'ya eklenir ve veritabanında ta_veri hesabına kaydedilir.

### 🔗 TA'yı İsterlere Bağlama

```
AMAÇ: "Bu TA handeki isterleri testi ediyor?" sorusuna cevap bulmak.

Bağlantı Örneği:
TA-GIGN-001
├─ Bağlantılı İsterler:
│  ├─ 1.1 Sistem Başlatması
│  ├─ 1.2 Tan Kontrolleri
│  └─ 2.1 Normal İşletim
```

TA Detay → **"İster Bağlantıları"** sekmesi

```
Mevcut Bağlantılar:
┌─────────────────────────────────────────┐
│ 1.1 Sistem Başlatması    [Bağlantıyı Kaldır]
│ 1.2 Tan Kontrolleri      [Bağlantıyı Kaldır]
│ 2.1 Normal İşletim       [Bağlantıyı Kaldır]
└─────────────────────────────────────────┘

[+ İster Ekle]
```

1. "**+ İster Ekle**" tıkla
2. İster listesi açılır (platform içindeki tüm isterler)
3. Bağlanacak isterleri çek (checkbox)
4. "Bağla" tıkla

**Backend:**
```python
for ister_id in selected_isters:
    cur.execute("""INSERT INTO ta_sgo_baglanti (TaID, NodeID) 
                   VALUES (%s, %s)""", (ta_id, ister_id))
mysql.connection.commit()
```

---

## Karşılaştırma ve Traceability - Detaylı

### 🔀 Karşılaştırma Sayfasına Erişim

**URL:** `http://localhost:5000/karsilastirma`  
**Navigasyon:** Ana Menü → Karşılaştırma

### 📋 Havuz ile Karşılaştırma

Amaç: "Platformun isterleri havuz platformda zaten var mı?"

```
Havuz Platform'daki İsterler:
g1, g2, g3, g4, g5, ...
b1, b2, ...

GIGN v3.1 Platform'daki İsterler:
1.1 Sistem Başlatması
1.2 Tan Kontrolleri
1.3 Sıcaklık Ölçümü

SORGU: "1.1 Sistem Başlatması" havuzda benzer bir şey var mı?
CEVAP: Evet! "g1 - Sistem Başlatması" %95 benzerlikle eşleşti.
```

#### Benzerlik Algoritması (Levenshtein)

```python
def levenshtein_distance(s1, s2):
    """
    İki string arasındaki edit distance'i hesapla.
    Kaç düzenleme gerekli?
    """
    # Örn: "Sistem Başlatması" vs "Sistem Güncelleme"
    # Edit distance = 3 (çünkü 3 karakter farklı)
    
    if not s1: return len(s2)
    if not s2: return len(s1)
    
    s1, s2 = s1.lower(), s2.lower()
    prev = list(range(len(s2) + 1))
    
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            if c1 == c2:
                curr.append(prev[j])
            else:
                curr.append(min(prev[j], curr[-1], prev[j+1]) + 1)
        prev = curr
    
    return prev[-1]

def similarity_ratio(s1, s2):
    """
    0-100% benzerlik oranı.
    """
    if not s1 and not s2: return 100
    if not s1 or not s2: return 0
    
    max_len = max(len(s1), len(s2))
    if max_len == 0: return 100
    
    distance = levenshtein_distance(s1, s2)
    ratio = (1 - distance / max_len) * 100
    return round(ratio, 1)

# Örn:
# similarity_ratio("Sistem Başlatması", "Sistem Başlatması") = 100%
# similarity_ratio("Sistem Başlatması", "Sistem Güncelleme") = 70.5%
# similarity_ratio("Sistem Başlatması", "Test") = 15.2%
```

#### Karşılaştırma Adımları

1. Platform seç: "GIGN v3.1"
2. Seviye seç: "Alt Sistem" (Level 2)
3. Benzerlik Eşiği: "80%" (varsayılan)
4. "Karşılaştır" tıkla

```python
# Backend:
# 1. GIGN v3.1'in o seviyedeki tüm isterleri al
platform_isters = get_isters(platform_id, level_no)

# 2. Havuz platform'un tüm isterleri al
pool_isters = get_isters(pool_platform_id, level_no)

# 3. Her platform isteri için havuzda karşılık arama
results = []
for p_ister in platform_isters:
    matched = False
    best_match = None
    best_ratio = 0
    
    for h_ister in pool_isters:
        ratio = similarity_ratio(p_ister['Icerik'], h_ister['Icerik'])
        
        if ratio >= threshold (80):
            matched = True
            if ratio > best_ratio:
                best_match = h_ister
                best_ratio = ratio
    
    results.append({
        'platform_ister': p_ister,
        'matched': matched,
        'best_match': best_match,
        'ratio': best_ratio
    })

return results
```

#### Sonuç Gösterimi

```
Karşılaştırma Sonuçları:
┌──────────────────────────────────────┐
│ Platform İsteri        │ Eşleşme      │
├──────────────────────────────────────┤
│ 1.1 Sistem Başlama...  │ ✅ g1 (%98)  │
│ 1.2 Tan Kontrolleri    │ ✅ g2 (%95)  │
│ 1.3 Sıcaklık Ölçümü    │ ⚠️ g3 (%72)  │
│ 1.4 Yeni İster Kritermetin... │ ❌ Eşleşmedi├──────────────────────────────────────┤

Havuzda Fazla İsterler:
├─ g4 - Sistem Reset
├─ b1 - Premium Feature
└─ b2 - Branded Özellik
```

### 🔗 Traceability Matrisini Görüntüleme

**Amaç:** İster ve TA bağlantılarını görmek

**URL:** `http://localhost:5000/traceability`

```
Traceability Matrix:
┌──────────┬───────────────────┬─────────────┐
│ İster No │ İster Başlığı     │ Bağlı TA'lar│
├──────────┼───────────────────┼─────────────┤
│ 1.1      │ Sistem Başlaması  │ TA-001 ✅   │
│ 1.2      │ Tan Kontrolleri   │ TA-001 ✅   │
│ 1.3      │ Sıcaklık Ölçümü   │ TA-002 ✅   │
│ 1.4      │ Sistem Reset      │ ❌ Bağlı YOK │
│ 2.1      │ Normal İşletim    │ TA-002 ✅   │
│ 2.2      │ Veri Toplama      │ TA-003 ✅   │
└──────────┴───────────────────┴─────────────┘

Kapsama: 83% (5/6 ister bağlı)
```

---

## Raporlar ve Dashboard - Detaylı

### 📊 Dashboard'a Erişim

**URL:** `http://localhost:5000/raporlar`  
**Navigasyon:** Ana Menü → Raporlar

### 📈 Proje Metrikleri (Dashboard)

```
Dashboard Paneli:
┌────────────────────────────────────────────────┐
│ Dashboard - Proje Durumu                       │
├────────────────────────────────────────────────┤
│                                                │
│ ☐ İster Durumu        ☐ Test Kapsama         │
│ ├─ Toplam: 156        ├─ Başarılı: 128 (82%)│
│ ├─ Level 1: 8         ├─ Başarısız: 22 (14%)│
│ ├─ Level 2: 45        └─ Atlanmış: 6 (4%)   │
│ ├─ Level 3: 78                               │
│ └─ Level 4: 25        ☐ TA Kapsama          │
│                       ├─ Bağlı: 143 (92%)    │
│ ☐ Platform Durumu     └─ Bağlı Yok: 13 (8%) │
│ ├─ Aktif: 3                                  │
│ ├─ Planlanmış: 1      ☐ Onay Durumu         │
│ └─ Bitmiş: 0          ├─ Onaylı: 156 (100%) │
│                       ├─ Bekleme: 0          │
│                       └─ Red: 0              │
└────────────────────────────────────────────────┘
```

### 📋 Mevcut Raporlar

1. **Firma Görüşleri Raporu**
   ```
   Müşterilerarından Alınan Yorumlar:
   ├─ Total: 12
   ├─ Açık: 5
   ├─ Kapalı: 7
   └─ Yanıt Beklemede: 3
   ```

2. **Onay Durumu Raporu**
   ```
   İsterlerin Onay Durumu:
   ├─ Onaylı: 156 (100%)
   ├─ Reddedilen: 0
   ├─ Bekleme: 0
   └─ Tanımlanmadı: 0
   ```

3. **Karşılaştırma Raporu**
   ```
   Havuz Karşılaştırması Sonuçları:
   ├─ Eşleşmiş: 140 (%90)
   ├─ Kısmi Eşleşmiş: 10 (%6)
   ├─ Eşleşmemiş: 6 (%4)
   └─ Fazla: 2
   ```

4. **Test Raporu**
   ```
   Test Durumu (Tüm Aşamalar):
   ├─ Unit Test: 94% geçti
   ├─ Integration: 87% geçti
   ├─ System: 92% geçti
   └─ Acceptance: 100% geçti
   ```

### 📥 Rapor İndirme

Raporları farklı formatlarda indir:

```
[📥 Excel İndir] [📥 PDF İndir] [🖨️ Yazdır]
```

Backend Excel Generation (xlsxwriter):
```python
import xlsxwriter

def export_report_to_excel(report_data):
    workbook = xlsxwriter.Workbook('report.xlsx')
    worksheet = workbook.add_worksheet()
    
    # Headers
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': 'white'
    })
    
    worksheet.write('A1', 'İster No', header_format)
    worksheet.write('B1', 'Başlık', header_format)
    worksheet.write('C1', 'Seviye', header_format)
    
    # Data
    for row, ister in enumerate(report_data['isters'], start=1):
        worksheet.write(row, 0, ister['NodeNumarasi'])
        worksheet.write(row, 1, ister['Icerik'])
        worksheet.write(row, 2, ister['SeviyeAdi'])
    
    workbook.close()
    return 'report.xlsx'
```

---

## Kullanıcı Yönetimi (Yönetici)

### 👥 Kullanıcı Sayfasına Erişim

**URL:** `http://localhost:5000/kullanici`  
**Navigasyon:** Ana Menü → Kullanıcı Yönetimi (Sadece Yönetici görebilir)

### ➕ Yeni Kullanıcı Ekleme

```
Kullanıcı Yönetimi:
┌──────────────────────────────────┐
│ [+ Yeni Kullanıcı Ekle]          │
│                                  │
│ Mevcut Kullanıcılar:             │
│ ├─ admin (Yönetici)              │
│ ├─ user1 (Kullanıcı)             │
│ └─ user2 (Kullanıcı)             │
└──────────────────────────────────┘
```

1. "**+ Yeni Kullanıcı Ekle**" tıkla
2. Form:

```
┌──────────────────────────────┐
│ Yeni Kullanıcı Ekle          │
├──────────────────────────────┤
│ Kullanıcı Adı: [____]        │
│ Ad Soyad: [__________]       │
│ E-Posta: [__________]        │
│ İlk Şifre: [__________]      │
│ Yetki: ◉ Kullanıcı           │
│        ○ Yönetici            │
│                              │
│ [Vazgeç]   [Ekle]           │
└──────────────────────────────┘
```

3. Bilgileri doldur ve Ekle

**Backend:**
```python
cur.execute("""INSERT INTO kullanici 
              (KullaniciAdi, AdSoyad, Email, Sifre, YetkiLevel) 
              VALUES (%s, %s, %s, %s, %s)""",
            (username, fullname, email, 
             hash_password(initial_password),
             'admin' if is_admin else 'user')
)
mysql.connection.commit()
```

### ✏️ Kullanıcı Düzenleme

Kullanıcı satırında "**Düzenle**" tıkla:

```
admin [Düzenle | Sil | 🔒 Şifre Sıfırla]
```

Düzenleyebilecekler:
- Ad Soyad
- E-Posta
- Yetki Seviyesi

### 🔒 Şifre Sıfırlama

1. Kullanıcı satırında "**🔒 Şifre Sıfırla**" tıkla
2. Geçici şifre oluşturulur
3. Yeni şifre gösterilir:

```
Şifre Başarıyla Sıfırlandı!

Geçici Şifre: ****XmP9$
Kullanıcıya bildirin ve
ilk girişte değiştirmesini söyleyin.
```

### 🗑️ Kullanıcı Silme

Kullanıcı satırında "**Sil**" tıkla → Onay → Sil

---

## İleri Konular

### 🔍 Denetim Günlüğü (Audit Log)

**URL:** `http://localhost:5000/log`

```
Denetim Günlüğü (degisiklik_log Tablosu):
┌──────────┬────────────┬──────────┬──────────┬──────────┐
│ Tarih    │ Kullanıcı  │ İşlem    │ Tablo    │ Detay    │
├──────────┼────────────┼──────────┼──────────┼──────────┤
│ 14:30    │ admin      │ INSERT   │ ister_node│ Created │
│ 14:31    │ user1      │ UPDATE   │ ister_node│ Modified│
│ 14:35    │ admin      │ DELETE   │ konfig_list
│ Silindi  │
└──────────┴────────────┴──────────┴──────────┴──────────┘

Her Değişiklik İçin:
├─ TabloAdi: Hangi tabloda?
├─ KayitID: Hangi kayıt?
├─ AlanAdi: Hangi alan?
├─ EskiDeger: Eski değer
├─ YeniDeger: Yeni değer
├─ KullaniciID: Kimin yaptığı?
├─ DegisimTarihi: Ne zaman?
└─ Tur: İşlem tipi (CREATE/UPDATE/DELETE)
```

### 🎯 Toplu Yükleme (Bulk Upload)

İsterler Excel dosyasından toplu olarak yüklenebilir.

Dosya Formatı (Excel):

```
┌──────┬──────────────────┬────────────┬─────────────┐
│ No   │ Başlık           │ Seviye     │ Açıklama    │
├──────┼──────────────────┼────────────┼─────────────┤
│1    │ Başlangıç Kont... │ 1. Sistem  │ ...         │
│1.1  │ Sistem Başlat... │ 2. Alt Sis│ ...         │
│1.2  │ Tan Kontrolleri  │ 2. Alt Sis│ ...         │
└──────┴──────────────────┴────────────┴─────────────┘
```

Upload Adımları:
1. Hazırlanmış Excel dosyası yükle
2. Sistem sütunları eşleştir
3. Doğrulama yap (dublicate check, vb.)
4. Yükle

---

## Sorun Giderme

### 🔴 Yaygın Hatalar

| Hata | Sebep | Çözüm |
|------|-------|-------|
| "MySQL Bağlantısı Başarısız" | MySQL sunucu kapalı | `systemctl start mysql` |
| "500 İç Sunucu Hatası" | Veritabanı hatası | Logs'u kontrol et |
| "Yükleme Yapılamıyor" | Dosya formatı yanlış | .xlsx formatında olup olmadığını kontrol et |
| "Özk Silemiyor" | Alt ister/bağlantı var | Alt öğeleri sil önce |

### 🔧 Temel Diagnostikler

**Python Console'dan Kontrol:**
```bash
# Veritabanı bağlantısı test
python -c "import MySQLdb; conn = MySQLdb.connect(host='localhost', user='root', password='1234', db='ister_v2'); print('OK')"

# Flask sunucusu başlat
python run.py --dev
# veya
python run.py
```

### 📋 Log Dosyaları

```
Uygulama Logları:
├─ stdout (terminal output)
├─ stderr (error output)
└─ MySQL logs (/var/log/mysql/error.log)
```
