# 📘 İster Yönetimi v2 - Kapsamlı Kullanıcı Kılavuzu

**Versiyon:** 2.0 - Detaylı Sürüm  
**Son Güncelleme:** Nisan 2025  
**Dil:** Türkçe  
**Yazılım Mimarisi:** MVC (Model-View-Controller)

---

## 📋 İçindekiler

1. [Giriş](#giriş)
2. [Sistem Gereksinimleri](#sistem-gereksinimleri)
3. [Kuruluş ve Başlatma](#kuruluş-ve-başlatma)
4. [Ana Menü ve Navigasyon](#ana-menü-ve-navigasyon)
5. [Temel Kavramlar](#temel-kavramlar)
6. [Giriş Ekranı ve Kimlik Doğrulama](#giriş-ekranı-ve-kimlik-doğrulama)
7. [Platform Yönetimi - Detaylı](#platform-yönetimi)
8. [Konfigürasyon Yönetimi - Detaylı](#konfigürasyon-yönetimi)
9. [İster (Requirement) Yönetimi - Detaylı](#ister-requirement-yönetimi)
10. [Test Yönetimi - Detaylı](#test-yönetimi)
11. [TA Dokümantasyon - Detaylı](#ta-dokümantasyon)
12. [Karşılaştırma ve Traceability - Detaylı](#karşılaştırma-ve-traceability)
13. [Raporlar ve Dashboard - Detaylı](#raporlar-ve-dashboard)
14. [Kullanıcı Yönetimi](#kullanıcı-yönetimi)
15. [İleri Konular](#ileri-konular)
16. [Sık Sorulan Sorular (SSS)](#sık-sorulan-sorular)

---

## Giriş

### 🎯 Uygulamanın Amacı

**İster Yönetimi v2** (Requirements Management v2), yazılım geliştirme projelerinde isterleri (requirements), test planlarını ve entegrasyon matrislerini merkezi olarak yönetmek için tasarlanmış profesyonel bir web uygulamasıdır. 

Özellikle otomotiv yazılımı (ASPICE, AUTOSAR standartları) ve endüstriyel sistemler gibi kritik uygulamalarda, isterlerin tam traceability'si ve değişim yönetimi önem taşır. Bu uygulama bu ihtiyaçları karşılamak için geliştirilmiştir.

### 🏗️ Mimarisi

- **Backend:** Flask (Python) + MySQL
- **Frontend:** HTML5 + JavaScript + CSS3
- **Pattern:** MVC (Model-View-Controller)
- **Veri Tabanı:** MySQL 5.7+ (utf8mb4 encoding destekl)
- **Deployment:** Waitress WSGI Server (Üretim)

### 📦 Ana Özellikler

| Özellik | Açıklama |
|---------|----------|
| **Platform Yönetimi** | Proje/ürün platformlarını merkezî olarak tanımlama ve yönetme |
| **İster Ağacı** | Hiyerarşik ister yapısı (başlık → alt başlık → detay), sınırsız derinlik |
| **Seviye Tanımı** | İsterleri seviyelere göre sınıflandırma (Sistem, Alt Sistem, Modül, Komponent, vb.) |
| **Konfigürasyon** | Ürün varyantlarına özgü konfigürasyonlar (sürüm, dil, özellik seti, vb.) |
| **Test Aşamaları** | Farklı test seviyeleri tanımlama (Unit, Entegrasyon, Sistem, Kabul, vb.) |
| **Test Girişi** | Her ister için test sonuçlarını (Başarılı/Başarısız/Atlanmış) atama |
| **TA Dokümantasyon** | Traceability Matrix - İsterleri test adımlarıyla bağlantı kurma |
| **Design Elements** | Ister içinde tablo/liste (bullet point) ekleme |
| **Firma Görüşü** | Müşteri/paydaş yorum ve geri dönüş yönetimi |
| **İster Onayı** | Isterler için onay/sign-off mekanizması |
| **Karşılaştırma Araçları** | Havuz platform veya harici liste ile benzerlik analizi (Levenshtein algoritması) |
| **Raporlar & Dashboard** | Proje metrik, durum, test kapsama, onay durumu raporları |
| **Denetim Günlüğü** | Tüm ekleme/güncelleme/silme işlemlerinin tam tarihçesi |
| **Kullanıcı Yönetimi** | Sistem kullanıcıları, roller, şifre yönetimi |
| **Toplu Yükleme** | Excel/CSV dosyasından isterleri toplu olarak yükleme |

---

## Sistem Gereksinimleri

### 💻 Yazılım Gereksinimleri

- **Python:** 3.8 veya üzeri
- **MySQL:** 5.7 veya üzeri (8.0 önerilir)
- **Web Tarayıcısı:** Chrome, Firefox, Safari, Edge (son sürüm)
- **İnternet Bağlantısı:** Lokal ağ bağlantısı (internete açık değil)

### 📊 Sistem Kaynakları

- **RAM:** Minimum 2GB, önerilir 4GB+
- **Depo Alanı:** Minimum 500MB
- **İşlemci:** Dual-core veya daha iyi

### Python Bağımlılıkları

```
Flask==3.0.3                   # Web framework
Flask-MySQLdb==2.0.0           # MySQL bağdaştırıcı
mysqlclient==2.2.4             # MySQL Python istemcisi
waitress==3.0.0                # WSGI sunucusu (üretim)
```

---

## Kuruluş ve Başlatma

### 1️⃣ Kurulum Adımları

#### Adım 1: Bağımlılıkları Yükleme

```bash
cd /workspaces/ister_v2_fixed
pip install -r requirements.txt
```

#### Adım 2: Veritabanı Oluşturma

```bash
# Schema'yı MySQL'de çalıştır
mysql -u root -p < schema.sql
```

Veritabanı yapısını başlatmak için (yeni kurulum):
```bash
python init_schema.py
```

#### Adım 3: Konfigürasyon

`config.py` dosyasını düzenle ve MySQL bağlantı bilgilerini ayarla:

```python
MYSQL_HOST = 'localhost'        # Veritabanı sunucusu
MYSQL_USER = 'root'              # Kullanıcı adı
MYSQL_PASSWORD = '1234'          # Şifre
MYSQL_DB = 'ister_v2'            # Veritabanı adı
```

### 2️⃣ Uygulamayı Başlatma

#### Geliştirme Modu (Development)
```bash
python run.py --dev
```
- Debug modu: Açık
- Otomatik yeniden yükleme: Aktif
- URL: `http://localhost:5000`

#### Üretim Modu (Production)
```bash
python run.py
```
- WSGI sunucusu: Waitress
- Port: 5000 (ayarlanabilir)
- URL: `http://localhost:5000`

### 3️⃣ İlk Giriş

1. Tarayıcıyı açın: `http://localhost:5000`
2. Login sayfasına yönlendirileceksiniz
3. **Varsayılan kullanıcı:** 
   - Kullanıcı Adı: `admin`
   - Şifre: `admin` (değiştir!)

---

## Ana Menü ve Navigasyon

### 🏠 Ana Sayfa (Ana Menü)

Uygulamada giriş yaptıktan sonra ana menüye erişirsiniz. Buradan tüm modüllere ulaşılabilir.

#### Menü Seçenekleri

| Menü | Icon | Açıklama |
|------|------|----------|
| **Platform** | 🏢 | Platform ve havuz yönetimi |
| **Konfigürasyon** | ⚙️ | Genel konfigürasyonlar |
| **İster Ağacı** | 📊 | Ister oluşturma ve yönetme |
| **Test Girişi** | ✅ | Test sonuçları girişi |
| **TA Dokümantasyon** | 📄 | Traceability Matrix yönetimi |
| **Traceability** | 🔗 | İster-TA bağlantı haritası |
| **Karşılaştırma** | 🔀 | İster karşılaştırma araçları |
| **Raporlar** | 📈 | Proje raporları ve metrikleri |
| **Denetim Günlüğü** | 📋 | Tüm değişikliklerin kaydı |
| **Kullanıcı Yönetimi** | 👥 | Sistem kullanıcıları |
| **Çıkış** | 🚪 | Oturumu sonlandır |

---

## Temel Kavramlar

### 1. Platform (Proje)

**Platform**, bir projeyi veya ürünü temsil eder. Her platformun kendi isterleri, test aşamaları ve seviyeleri vardır.

**Örnek Platformlar:**
- GIGN v3.1 (Otomotiv Yazılım Projesi)
- MÖP v2.0 (Endüstriyel Sistem)
- Mobil Uygulama v1.0

### 2. Havuz Platform

Özel bir platform türüdür. Tüm ortak isterleri saklayan **şablon** görevi yapar. Diğer platformlar, havuz platform'dan konfigürasyonlarına göre ister alabilir.

**Sahibi:** Tipik olarak her projede **1 adedi** vardır.

### 3. Seviye (Level)

Her platform içinde isterlerin hiyerarşik seviyesi vardır:

```
Seviye 1 (Sistem Gerekliliği)
├── Seviye 2 (Alt Sistem)
│   ├── Seviye 3 (Modül)
│   │   ├── Seviye 4 (Detay)
```

**Yaygın Seviyeler:**
- **G (Sistem)** - Genel gerekilililikler
- **B (Alt Sistem)** - Alt sistem seviyeleri
- Sistem/Alt sistem/Modül/Komponent

### 4. Konfigürasyon

Ister'e özgü özellikler. Bir ister birden fazla konfigürasyona ait olabilir.

**Örnekler:**
- Sürüm (v1.0, v2.0)
- Varyant (Standart, Premium, Enterprise)
- Dil (TR, EN, DE)

### 5. Test Aşaması

Test edilecek farklı aşamalar:

- **Unit Test** - Birim testleri
- **İntegrasyon Testi** - Modüller arasında
- **Sistem Testi** - Tam sistem
- **Kabulanabilirlik Testi** - Müşteri tarafından

### 6. İster (Requirement)

Yazılım gereksiniminin açıklaması. Numara, başlık, konfigürasyon, test yöntemi vb. içerir.

**Örnek İster:**
```
Numara: GIGN-001-001
Başlık: Sistem başlatıldığında tanılama çalışacak
Konfigürasyon: GIGN v3.1
Seviye: Sistem
```

### 7. TA (Test Alignment / Traceability)

İsterler ile test dokümantasyon arasında bağlantı oluşturur. Her TA dokümantasyonu bir veya daha fazla isterle ilişkilidir.

---

## Platform Yönetimi

### 📍 Platform Sayfasına Erişim

**URL:** `http://localhost:5000/platform`  
**Ana Menü → Platform** veya Sol Menü → Platform

### 🎯 Platform Nedir? (Teknik Açıklama)

**Platform**, bir proje/ürün temsil eden konteynerdir. Veritabanında `platform_list` tablosuna kaydedilir:

```sql
platform_list
├── PlatformID (int) - Benzersiz kimlik
├── PlatformAdi (varchar) - Platform adı (ör: "GIGN v3.1")
├── HavuzMu (tinyint) - 0=Normal Platform, 1=Havuz Platform
└── OlusturmaTarihi (datetime) - Oluşturulduğu tarih
```

Bir platformun altında:
- **Seviyeleri** - İster hiyerarşisini tanımlar (seviye_tanim tablosu)
- **Test Aşamaları** - Test türlerini tanımlar (test_asama tablosu)
- **Konfigürasyonları** - Hangi konfiglarla çalışacağını belirtir (platform_konfig tablosu)
- **İsterleri** - Hiyerarşik ister ağacı (ister_node tablosu)

#### Örnek Platform Yapısı:

```
GIGN v3.1 (PlatformID=1)
├── Seviyeleri:
│   ├── 1. Sistem Gerekliliği
│   ├── 2. Alt Sistem Gerekliliği
│   ├── 3. Modül Gerekliliği
│   └── 4. Komponent Gerekliliği
├── Test Aşamaları:
│   ├── Unit Test
│   ├── Integration Test
│   ├── System Test
│   └── Acceptance Test
├── Konfigürasyonları:
│   ├── GIGN v3.1 TR
│   └── GIGN v3.1 EN
└── İsterleri: (hiyerarşik ağaç)
    ├── 1. Başlangıç Kontrolleri
    │   ├── 1.1 Sistem Başlatması
    │   ├── 1.2 Tan Kontrolleri
    │   └── 1.3 Sıcaklık Ölçümü
    ├── 2. Çalışma Modları
    │   └── 2.1 Normal İşletim
    └── 3. Acil Durumlar
        └── 3.1 Sistem Kapanması
```

### ➕ Yeni Platform Oluşturma - Detaylı Adım Adım

#### Adım 1: Platform Ekleme Formunu Aç

1. **Platform** sayfasında "**+ Yeni Platform Ekle**" düğmesine tıkla
2. Modal veya formu açılır:
   ```
   ┌─────────────────────────────────┐
   │ Yeni Platform Ekle              │
   ├─────────────────────────────────┤
   │ Platform Adı: [____________]    │
   │ Açıklama: [_________________]   │
   │                                 │
   │ [Vazgeç]              [Ekle]    │
   └─────────────────────────────────┘
   ```

#### Adım 2: Bilgi Gir

- **Platform Adı:** Projenin tam adı
  - ✅ Örnek: "GIGN v3.1", "Mobil App v1.0", "MÖP 2.0"
  - ❌ Kaçın: "Proje1", "Test", "Demo"
  
- **Açıklama:** (İsteğe bağlı) Projenin kısa tanımı

#### Adım 3: Ekle Tıkla

- "**Ekle**" düğmesine tıkla
- Sistem platformu veritabanına ekler (`INSERT INTO platform_list`)
- Başarılı ise: "Platform başarıyla oluşturuldu" mesajı
- Platform otomatik olarak listeye eklenir

#### Teknik Arka Planda Neler Oluyor?

```
1. API isteği: POST /api/platform
   ├─ İstek Verisi: {"PlatformAdi": "GIGN v3.1"}
   └─ Cevap: {"PlatformID": 1}

2. Veritabanı Saklı Yordamı (Backend):
   └─ INSERT INTO platform_list (PlatformAdi, HavuzMu)
      VALUES ('GIGN v3.1', 0)

3. Denetim Günlüğü (Logging):
   └─ Yeni platform oluşturulduğu kaydedilir:
      LogType: CREATE
      TabloAdi: platform_list
      KayitID: {generatedID}
      AlanAdi: Platform
      EskiDeger: '-'
      YeniDeger: 'GIGN v3.1'
      OlusturanKullanici: {loginKullaniciId}
      DegisimTarihi: NOW()
```

### ✏️ Platform Düzenleme - Detaylı

#### Adım 1: Düzenlenecek Platformu Bul

Platform listesinde platformu ara. Listede eksen için filtreler vardır:
- **Platform Adı Arama** - Adında metin ara
- **Sıralama** - Havuz platformu en üste gelir

#### Adım 2: Düzenleme Modu Aç

Platformun satırındaki **"✏️ Düzenle"** düğmesine tıkla:

```
Platform Adı: GIGN v3.1 [Tıklanabilir]
 ↓ (Düzenleme modu)
Platform Adı: [GIGN v3.1] (Input alanı)
                      [✓ Kaydet] [Ø İptal]
```

#### Adım 3: Değişiklik Yap ve Kaydet

- Platformun adını değiştir
- **"✓ Kaydet"** tıkla veya Enter
- Veritabanı güncellenir
- Denetim günlüğüne kaydedilir:
  ```
  EskiDeger: 'GIGN v3.1'
  YeniDeger: 'GIGN v3.1 TR'
  ```

#### Adım 4: İptal

- Değişiklik yapmayıp "**Ø İptal**" tıklanırsa değişiklikler atılır

### 🔄 Havuz Platform Tanımlama - Özel İşlem

#### Havuz Platform Nedir?

**Havuz Platform** (Pool Platform), tüm ortak isterlerin depolanıdığı **merkezi şablon** platformudur. Diğer platformlar, kendi konfigürasyonlarına göre havuztan ister alabilir.

**Özellikler:**
- Sistem içinde **yalnızca 1 adedi** olabilir
- Havuz isterleri `HavuzKodu` ile tanımlanır (g1, g2, ... / b1, b2, ...)
- Diğer platformlar havuzdan ister kopyalayabilir
- Veritabanında: `HavuzMu = 1` ile işaretlenir

#### Havuz Platform Oluşturma Adımları

1. **Normal Platform Oluştur** (Yukarıdaki adımları izle)
2. **Platform Adı:** "**Havuz**" veya "**Genel İster Havuzu**" olarak ayarla
3. **Sistem Otomatik Olarak Tanır** - `HavuzMu` alanı 1 olur
4. **Listede Görüntüleme** - Havuz platformu listenin en üstünde "(HAVUZ)" etiketiyle görüntülenir

```
Platform Listesi:
┌──────────────────────────────┬─────────────────┐
│ Platform Adı                 │ İşlemler        │
├──────────────────────────────┼─────────────────┤
│ Havuz                (HAVUZ) │ Düzenle | Sil   │
│ GIGN v3.1                    │ Düzenle | Sil   │
│ Mobil App v1.0               │ Düzenle | Sil   │
└──────────────────────────────┴─────────────────┘
```

#### Havuz'da İster Oluşturma Özel Kuralları

Havuz platformunda ister oluştururken `HavuzKodu` **otomatik** olarak oluşturulur:

```javascript
// Backend Logic:
if (platformu_havuz_mi) {
  if (ister_tipi === 'G') {
    // G = Generic/Genel
    current_g = MAX(HavuzKodu sayısal kısmı) + 1
    HavuzKodu = 'g' + current_g  // g1, g2, g3, ...
  } else if (ister_tipi === 'B') {
    // B = Branded/Marka Spesifik
    current_b = MAX(HavuzKodu sayısal kısmı) + 1
    HavuzKodu = 'b' + current_b  // b1, b2, b3, ...
  }
}
```

**Örnek:**
```
Havuz İsterleri:
├── g1 - Sistem Başlatması (Genel)
├── g2 - Çalışma Modları (Genel)
├── g3 - Acil Durumlar (Genel)
├── b1 - Sadece GIGN için (Branded)
└── b2 - Sadece Türkçe versiyonda (Branded)
```

### 🗑️ Platform Silme - Kritik İşlem

⚠️ **UYARI:** Bu işlem **GERİ ALINAMAZ!** Platform, tüm isterleri, test sonuçları, TA dokümantasyonları vb. ile birlikte silinir.

#### Silme Öncesi Kontroller

Silmeden önce sistem otomatik kontroller yapır:

```
if (platform_id === havuz_platformu) {
  ❌ HATA: "Havuz platformu silinemez!"
  // Havuz Havuz sililemez, çünkü diğer platformlar bağımlı
}

if (platform_da_ister_var_mı) {
  ⚠️ UYARI: "Bu platformda {sayı} ister var."
  "Silmek istediğinizden emin misiniz?"
  // Tüm isterler cascade silinecek
}
```

#### Silme Adımları

1. Silinecek platform satırında **"🗑️ Sil"** düğmesine tıkla
2. Onay penceresinde:
   ```
   ❌ Bu işlem GERİ ALINAMAZ!
   
   "GIGN v3.1" platformunu ve içindeki TÜM isterleri silmek istediğinizden emin misiniz?
   
   Platform İsterleri: 156
   Test Sonuçları: 343
   TA Dokümantasyonları: 12
   
   [Vazgeç]        [Evet, Sil]
   ```

3. "**Evet, Sil**" tıkla
4. Silme işlemi başlar:
   - Veritabanında CASCADE DELETE
   - Tüm ilgili tablolardan silinir:
     * ister_node (tüm isterleri)
     * test_sonuc (test sonuçları)
     * ta_sgo_baglanti (TA bağlantıları)
     * Diğer ilişkili veriler
   - Denetim günlüğüne kaydedilir

5. Başarı mesajı: "Platform başarıyla silindi"

### 📊 Seviyeleri Yönetme - Platform İçinde

Her platformun kendi seviyeleri vardır. Seviyeler, isterlerin hiyerarşik yapısını tanımlar.

#### Seviyeleri Görüntüleme

Platform sayfasında platformu seç → **"Seviyeleri Ayarla"** sekmesi

Mevcut seviyelerin listesini görsün:

```
┌─────────┬──────────────────────────┬────────┐
│ No      │ Seviye Adı               │ İşlem  │
├─────────┼──────────────────────────┼────────┤
│ 1       │ Sistem Gerekliliği       │ Sil    │
│ 2       │ Alt Sistem Gerekliliği   │ Sil    │
│ 3       │ Modül Gerekliliği        │ Sil    │
│ 4       │ Komponent Gerekliliği    │ Sil    │
└─────────┴──────────────────────────┴────────┘

[+ Yeni Seviye Ekle]
```

#### Yeni Seviye Ekleme

1. "**+ Yeni Seviye Ekle**" tıkla
2. Form açılır:
   ```
   Seviye Adı: [________________]
   Açıklama: [__________________]
   
   [Vazgeç]        [Ekle]
   ```

3. Seviye adını gir (ör: "Yazılım Modülü", "Komponent", "Alt Modül")
4. "**Ekle**" tıkla

**Teknik Arka Planda:**
```sql
INSERT INTO seviye_tanim (PlatformID, SeviyeNo, SeviyeAdi, OlusturmaTarihi)
VALUES ({PlatformID}, {auto_increment_no}, '{GirilenAd}', NOW())
```

#### Seviye Silme

Seviye silebilmek için **o seviyenin altında ister olmaması gerekir.**

Eğer altında ister varsa:
```
❌ HATA: "Bu seviye {sayı} istere sahip, silinemez!"
Çözüm: 
1. Tüm isterleri başka seviyeye taşı
2. Veya isterlerü sil
3. Sonra seviyeyi sil
```

### ⏱️ Test Aşamalarını Yönetme

Her platformda farklı test aşamaları olabilir.

#### Test Aşamsı Nedir?

Test aşaması, projenin test edilme seviyesini tanımlar:

```
Test Aşamaları Örneği:
├── 1. Unit Test (Birim Testi)
│   └─ Yazılımcı tarafından yapılan test
├── 2. Integration Test (Entegrasyon Testi)
│   └─ Modüller arasında test
├── 3. System Test (Sistem Testi)
│   └─ Tüm sistem test
└── 4. Acceptance Test (Kabul Testi)
    └─ Müşteri tarafından final test
```

Her test aşaması için her ister için bir test sonucu kaydedilir.

#### Test Aşaması Ekleme

1. Platform → **Test Aşamaları** sekmesi
2. **"+ Yeni Aşama Ekle"** tıkla
3. Form:
   ```
   Aşama Adı: [_________________________]
   Sıra No: (otomatik doldurulur)
   
   [Vazgeç]        [Ekle]
   ```

4. Aşama adını gir (ör: "Sistem Entegrasyon Testi")
5. "**Ekle**" tıkla

**Veritabanı:**
```sql
INSERT INTO test_asama (PlatformID, AsamaNo, AsamaAdi, OlusturmaTarihi)
VALUES ({PlatformID}, {otomatik_sira_no}, '{AsamaAdi}', NOW())
```

#### Test Aşaması Silme

Silmek için aşamada **hiç test sonucu olmaması gerekir.**

```
Silme Adımları:
1. Aşama satırında "Sil" tıkla
2. Onay: "Bu aşamanın test sonuçları silinecek. Devam?"
3. Evet tıkla
```

### 🔗 Konfigürasyonları Platformlara Atama

Bir platforma hangi konfigürasyonların uygun olduğunu belirtmek için bu işlem yapılır.

#### Konfigürasyon Atama Örneği

```
Platform: GIGN v3.1
├─ Atananlar:
│  ├─ GIGN v3.1 TR (Türkçe)
│  ├─ GIGN v3.1 EN (İngilizce)
│  └─ GIGN v3.1 DE (Almanca)
└─ Atalanmayanlar:
   └─ MÖP v2.0 (Başka proje için)
```

#### Atama İşlemi

1. Platform → **"Konfigürasyonlar"** sekmesi
2. Atanabilir konfigürasyonlar listesini gör
3. Atanacak konfigürasyonların **checkbox'ını işaretle**:
   ```
   ☐ GIGN v3.1 TR
   ☑ GIGN v3.1 EN
   ☐ GIGN v3.1 DE
   ☑ MÖP v2.0
   
   [Kaydet]
   ```

4. "**Kaydet**" tıkla
5. Seçili konfigürasyonlar bu platforma atanır
6. İster oluştururken bu konfiglardan seçim yapılabilir

---

## Konfigürasyon Yönetimi - Detaylı

### 📍 Konfigürasyon Sayfasına Erişim

**URL:** `http://localhost:5000/konfig`  
Ana Menü → **Konfigürasyon** veya Sol Menü → Konfigürasyon

### 🎯 Konfigürasyon Nedir?

Konfigürasyon, bir ürünün belirli bir varyantını veya versiyonunu tanımlar. Farklı konfigürasyonların farklı isterleri olabilir.

**Veritabanı Yapısı:**
```
konfig_list:
├── KonfigID (int) - Kimlik
├── KonfigAdi (varchar) - Konfigürasyon adı
└── OlusturmaTarihi (datetime)
```

**Örnek Konfigürasyonlar:**

```
┌─────────────────────────┐
│ Konfigürasyonlar        │
├─────────────────────────┤
│ GIGN v3.1 TR (Türkçe)   │
│ GIGN v3.1 EN (İngilizce)│
│ GIGN v3.2 Premium       │
│ MÖP v2.0 Standart       │
│ MÖP v2.0 Pro            │
└─────────────────────────┘
```

### ➕ Yeni Konfigürasyon Oluşturma

#### Adım 1: Sayfaya Gir ve Button Bul

Konfigürasyon sayfasında **"+ Yeni Konfigürasyon Ekle"** düğmesi görüntülenir.

#### Adım 2: Form Aç

Düğmeye tıkla → Modal/form açılır:

```
┌─────────────────────────────────┐
│ Yeni Konfigürasyon             │
├─────────────────────────────────┤
│ Konfigürasyon Adı:             │
│ [_________________________]     │
│                                 │
│ Açıklama (İsteğe bağlı):       │
│ [_________________________]     │
│                                 │
│ [Vazgeç]        [Ekle]         │
└─────────────────────────────────┘
```

#### Adım 3: Bilgi Gir

**Konfigürasyon Adı Kuralları:**

| ✅ Yapın | ❌ Yapmayın |
|---------|-----------|
| GIGN v3.1 TR | Conf1 |
| GIGN v3.1 EN | Türkçe |
| MÖP 2.0 Premium | Test |
| Platform A v1.0 | asd |

**Açıklama:** (İsteğe bağlı) Konfigürasyonun ne zaman kullanılacağını belirt
- "GIGN v3.1 Türkçe versiyonu"
- "Premium paket ile satılanlar"
- "Pilot müşteriler için"

#### Adım 4: Kaydet

- "**Ekle**" tıkla
- Veritabanına eklenir: `INSERT INTO konfig_list (KonfigAdi, OlusturmaTarihi) VALUES (...)`
- "Başarıyla eklendi" mesajı
- Konfig listesine eklenir

### 📋 Tüm Konfigürasyonları Görüntüleme

Konfigürasyon listeleme sayfası:

```
┌───────────────────────────────────┬──────────────────┐
│ Konfigürasyon Adı                 │ İşlemler         │
├───────────────────────────────────┼──────────────────┤
│ GIGN v3.1 TR                      │ Düzenle | Sil    │
│ GIGN v3.1 EN                      │ Düzenle | Sil    │
│ MÖP v2.0 Premium                  │ Düzenle | Sil    │
│ MÖP v2.0 Standart                 │ Düzenle | Sil    │
└───────────────────────────────────┴──────────────────┘

Toplam: 4 konfigürasyon
```

### ✏️ Konfigürasyon Düzenleme

#### Düzenleme Formunu Aç

Listede konfigürasyonun satırında **"✏️ Düzenle"** tıkla:

```
Satır Öncesi:    GIGN v3.1 TR  [Düzenle | Sil]
                      ↓
Satır Sonrası:   [GIGN v3.1 TR]  [✓ | Ø]
```

#### Metin Düzenle

Input alanında metni değiştir:
- Örn: "GIGN v3.1 TR" → "GIGN v3.1 TR (Eski)"

#### Değişikliği Kaydet

- **"✓"** tıkla = Kaydet
- **"Ø"** tıkla = İptal

**Denetim Günlüğü:**
```
TabloAdi: konfig_list
İşlem: UPDATE
AlanAdi: KonfigAdi
EskiDeger: GIGN v3.1 TR
YeniDeger: GIGN v3.1 TR (Eski)
KullaniciAdi: {Adınız}
DegisimTarihi: {Şu Tarih}
```

### 🗑️ Konfigürasyon Silme

#### Silme Öncesi Kontroller

Sistem otomatik kontrol eder:

```
if (konfig_herahangi_istere_bagly_mi) {
  ❌ HATA: "Bu konfigürasyon {sayı} istere atanmış, silinemez!"
  
  Çözüm:
  1. Konfigürasyonu platformlardan kaldır
  2. Veya isterlerıen konfigürasyonunu değiştir
  3. Sonra sil
}
```

#### Silme Adımları

1. Silinecek konfigürasyonun satırında **"🗑️ Sil"** tıkla
2. Onay penceresi:
   ```
   ⚠️ Emin misiniz?
   
   "GIGN v3.1 TR" konfigürasyonunu silmek istediğinizden emin misiniz?
   Bu işlem GERİ ALINAMAZ!
   
   [Vazgeç]       [Evet, Sil]
   ```

3. "**Evet, Sil**" tıkla
4. Veritabanından silinir: `DELETE FROM konfig_list WHERE KonfigID = ...`
5. Listeden kaybolur

### 🔗 Konfigürasyonları Platformlara Atama - Detaylı

Bu işlem, bir platformun hangi konfigürasyonlarla çalışacağını belirtir.

#### Neden Gerekli?

```
Örnek Senaryo:
├─ Havuz Platform (Tüm genel isterleri içerir)
│  └─────────────┬─────────────┐
│                 │             │
├─ GIGN v3.1     ├─ GIGN v3.2  ├─ MÖP v2.0
│ Atanan Konfig: │ Atanan Konfig:│ Atanan Konfig:
│ - TR           │ - EN         │ - Premium
│ - EN           │ - TR         │ - Standard
│                │              │
├─ İster Kümesi: ├─ İster Kümesi:├─ İster Kümesi:
│ g1, g2, g3 ... │ g2, g3, g4 ...│ g1, b1 (b=branded)
```

#### Atama İşlemi

##### Adım 1: Platform Seç

Konfigürasyon sayfasında veya Platform → **"Konfigürasyonlar"** sekmesine git

##### Adım 2: Atanabilir Konfigürasyonları Gör

```
Platform: GIGN v3.1
Atanabiiler Konfigürasyonlar:
│
├─ ☐ GIGN v3.1 TR
├─ ☐ GIGN v3.1 EN
├─ ☐ GIGN v3.1 DE
├─ ☐ MÖP v2.0 Premium
└─ ☐ MÖP v2.0 Standart
```

##### Adım 3: Seçim Yap

Bu platforma uygun konfigürasyonları seç:

```
Platform: GIGN v3.1
SAMAtanan Konfigürasyonlar (Seçili):
│
├─ ☑ GIGN v3.1 TR
├─ ☑ GIGN v3.1 EN
├─ ☐ GIGN v3.1 DE
├─ ☐ MÖP v2.0 Premium
└─ ☐ MÖP v2.0 Standart
```

##### Adım 4: Kaydet

- "**Kaydet**" düğmesine tıkla
- Veritabanında `platform_konfig` tablosuna kaydedilir:
  ```sql
  platform_konfig
  ├── PlatformID = {GIGN v3.1'in ID'si}
  ├── KonfigID = {GIGN v3.1 TR'nin ID'si}
  └── OlusturmaTarihi = NOW()
  
  (ve GIGN v3.1 EN için de aynı şekilde)
  ```

- Başarı mesajı: "Konfigürasyonlar başarıyla kaydedildi"

##### Adım 5: İster Oluşturma Sırasında Kullanım

Şimdi GIGN v3.1 platformunda ister oluştururken, sadece atanan konfigları seçebilirsin:

```
Yeni İster Formu - GIGN v3.1 Platformu:
├─ Platform: GIGN v3.1 ✓
├─ Seviye: Sistem Gerekliliği ✓
├─ Başlık: [Sistem Başlatması] ✓
├─ Atanan Konfigürasyon:
│  ├─ ☐ GIGN v3.1 TR
│  ├─ ☐ GIGN v3.1 EN
│  └─ (Diğerleri burada görünmez!)
└─ [Ekle] ✓
```

---

## İster (Requirement) Yönetimi

### 📊 İster Sayfasına Erişim

Ana Menü → **İster Ağacı** veya Sol Menü → İster Ağacı

### 🎯 İster Ağacı Yapısı

İster ağacı **hiyerarşik** olarak görüntülenir:

```
📦 Platform: GIGN v3.1
├── 📌 1. Sistem İsteri 1
│   ├── 1.1 Alt İster 1
│   ├── 1.2 Alt İster 2
│   └── 1.3 Alt İster 3
├── 📌 2. Sistem İsteri 2
│   └── 2.1 Alt İster
└── 📌 3. Sistem İsteri 3
```

### ➕ Yeni İster Ekleme

#### Adım 1: Platform Seç
1. "Platform Seç" dropdown'undan bir platform seç
2. İster ağacı görüntülenir

#### Adım 2: Başlık İsteri Ekleme (Üst Seviye)
1. "Yeni Başlık Ekle" düğmesine tıkla
2. Form açılacak:
   - **İster Tipi:** "Başlık" seç (hiyerarşinin üstü)
   - **Seviye:** En üst seviyeyi seç (örn: "1. Sistem")
   - **Başlık:** İster başlığını yaz
   - **Konfigürasyon:** Uygulanacak konfigürasyonları seç
   - **Test Yöntemi:** İsteğe bağlı
3. "Ekle" tıkla

#### Adım 3: Alt İster Ekleme
1. Bir başlık üzerine sağ tık yap veya başlığın yanındaki "➕" tıkla
2. "Alt İster Ekle" seç
3. Form açılacak:
   - **İster Tipi:** "Normal İster" seç
   - **Numara:** Otomatik doldurulur (örn: "1.1")
   - **Başlık:** İster başlığını yaz
   - **Seviye:** Alt seviyeleri seç (örn: "2. Alt Sistem")
   - Diğer alanları doldur
4. "Ekle" tıkla

### ✏️ İster Düzenleme

1. Düzenlemek istediğin isteri bul
2. Satırdaki "Düzenle" düğmesine tıkla
3. Gerekli alanları değiştir
4. "Kaydet" tıkla

### 🗑️ İster Silme

1. Silmek istediğin isteri bul
2. Satırda "Sil" düğmesine tıkla
3. Onay penceresinde "Evet" seç

**Uyarı:** İsteri silerken alt isterleri de otomatik silinir!

### 🔄 İster Sıralama

1. Ister ağacında bir isteri bul
2. Satırda "⬆️ / ⬇️" düğmelerine tıkla
3. İster yukarı veya aşağı taşınır

### 📑 İster İçine Tablo Ekleme (Kutucuk)

Bazı isterlerin içinde tablo/liste (bullet point) bulunabilir:

1. İsteri açıklamak için tablo eklemeyi istiyorsan
2. İster sayfasında "Tablo Ekle" seç
3. Tablo başlığı ve satırları ekle
4. "Kaydet" tıkla

---

## Test Yönetimi

### ✅ Test Girişi Sayfasına Erişim

Ana Menü → **Test Girişi** veya Sol Menü → Test Girişi

### 📝 Test Sonucu Girişi

1. Test Girişi sayfasında
2. Platform seç
3. Test aşamasını seç (Unit Test, Sistem Testi, vb.)
4. İster listesi görüntülenir
5. Her ister için test sonucunu gir:
   - **✅ Başarılı** - Test geçti
   - **❌ Başarısız** - Test eşleşmedi
   - **⏸️ Atlanmış** - Test yapılmadı
6. "Kaydet" tıkla

### 📊 Test Sonuçları Görüntüleme

1. İster ağacına geri dön
2. Sağ tarafta test sonuçları gösterilir
3. Yeşil/Kırmızı göstergeler test durumunu gösterir

---

## TA Dokümantasyon

### 📄 TA Nedir?

**TA (Traceability Alignment)** isterlerin test dokümantasyonuyla bağlantısıdır. Her test adımının hangi isterleri karşıladığını gösterir.

### 📋 TA Sayfasına Erişim

Ana Menü → **TA Dokümantasyon** veya Sol Menü → TA Dokümantasyon

### ➕ Yeni TA Dokümantasyonu Oluşturma

1. TA sayfasında "Yeni TA Ekle" tıkla
2. Form açılacak:
   - **Platform:** Hangi platforma ait
   - **Sıra No:** TA numarası (otomatik artış)
   - **Adı:** TA başlığı (örn: "Başlangıç Kontrolleri")
   - **Açıklama:** Kısa açıklama
3. "Ekle" tıkla

### 📊 TA'ya Test Verileri Ekleme

1. TA listesinden düzenlemek istediğin TA'yı seç
2. "Veriler" sekmesine git
3. "Veri Ekle" tıkla
4. Test adımlarını gir:
   - **Sistem:** Test edilen sistem bileşeni
   - **Yön:** Giriş veya Çıkış
   - **Sira:** Adım numarası
   - **Açıklama:** Test adımı açıklaması
5. "Kaydet" tıkla

### 🔗 TA'yı İsterlere Bağlama

1. TA listesinden TA'yı seç
2. "İster Bağlantıları" sekmesine git
3. "İster Ekle" tıkla
4. İster listesinden isterleri seç (checkbox ile)
5. "Kaydet" tıkla

---

## Karşılaştırma ve Traceability

### 🔀 Karşılaştırma Sayfasına Erişim

Ana Menü → **Karşılaştırma** veya Sol Menü → Karşılaştırma

### 📋 Havuz ile Karşılaştırma

Bu özellik, seçilen platformun isterleriyle havuz platform'unun isterleri arasında benzerlik bulur.

#### Adımlar:
1. Karşılaştırma sayfasında
2. Platform seç
3. Seviye seç (Sistem, Alt Sistem, vb.)
4. "Benzerlik Eşiği" ayarla (80% önerilir)
5. "Karşılaştır" tıkla

#### Sonuçlar:
- **✅ Eşleşen:** Havuzda benzer ister var
- **⚠️ Bilinmeyen:** Benzer ister bulunamadı
- **➕ Fazla:** Platformda fazla ister var

### 📝 Dış Listeyle Karşılaştırma

Harici bir dosya veya listeden isterleri yükle ve platformunuzla karşılaştır:

1. Karşılaştırma sayfasında "Dış Liste" sekmesine git
2. İster listesini gir (JSON formatı)
3. "Karşılaştır" tıkla

### 🔗 Traceability Matrisini Görüntüleme

Ana Menü → **Traceability** veya Sol Menü → Traceability

Bu sayfa isterlerin TA dokümantasyonlarla bağlantısını gösterir:

| İster No | İster Başlığı | Bağlantılı TA | Durumu |
|----------|---------------|---------------|--------|
| GIGN-001 | Başlangıç | TA-001, TA-002 | ✅ |
| GIGN-002 | İşlem | TA-001 | ✅ |
| GIGN-003 | Hata Yönetimi | - | ❌ Bağlantı Yok |

---

## Raporlar ve Dashboard

### 📊 Dashboard'a Erişim

Ana Menü → **Raporlar** veya Sol Menü → Raporlar

### 📈 Proje Metrikleri

Dashboard aşağıdaki bilgileri gösterir:

1. **İster Durumu**
   - Toplam ister sayısı
   - Seviyelere göre dağılım
   - Konfigürasyonlara göre dağılım

2. **Test Durumu**
   - Toplam test sayısı
   - Başarılı testler (%)
   - Başarısız testler (%)
   - Atlanmış testler

3. **TA Kapsama**
   - TA'yla bağlantılı isterlerin sayısı
   - Kapsama yüzdesi (%)

4. **Platformlar**
   - Aktif platformlar
   - Her platformun ister sayısı

### 📋 Mevcut Raporlar

1. **Firma Görüşleri Raporu**
   - Müşteri tarafından göndermiş yorumlar
   - Yanıtlar ve durum

2. **Onay Durumu Raporu**
   - İsterlerin onay durumu
   - Kimin tarafından onaylandığı
   - Tarihler

3. **Karşılaştırma Raporu**
   - İster benzerlik analizleri

### 📥 Rapor İndirme

Raporları Excel veya PDF formatında indir:

1. Rapor sayfasında
2. "Excel İndir" veya "PDF İndir" tıkla
3. Dosya bilgisayarına indirilir

---

## Sık Sorulan Sorular

### ❓ Giriş Şifremi Unuttum

1. Sistem yöneticisine haber ver
2. Yönetici "Kullanıcı Yönetimi" → Şifre Sıfırla
3. Yeni şifre kullanarak giriş yap

### ❓ Neden Ister Silemiyorum?

Muhtemel nedenler:
- İsteri altında başka isterler var (alt isterleri sil)
- İsteri TA'yla bağlantılı (bağlantıyı kaldır)

### ❓ Platform Adını Değiştirebilir miyim?

Evet! Platform satırında "Düzenle" tıkla ve adı değiştir.

### ❓ Havuz Platform'dan İster Nasıl Alırım?

1. Platformu oluştur
2. Konfigürasyonlarını belirle
3. "İster Seti Oluştur" tıkla
4. Havuz'dan konfigürasyonunuza uygun isterleri alır

### ❓ Test Sonuçlarını Düzenleyebilir miyim?

Evet! Test Girişi sayfasında test sonucunu değiştirebilirsin (kaydol sonrası).

### ❓ Yanlışlıkla Sildim, Geri Getirebilir miyim?

**Hayır**, çoğu silme işlemi kalıcıdır. Denetim Günlüğünü kontrol et ve ne silindiğini gör.

### ❓ Birden Fazla İsteriyi Aynı Anda Düzenleyebilir miyim?

Henüz değil, tek tek düzenleme yapın. Gelecek sürümlerde toplu işlemler eklenecek.

### ❓ İster İmport Yapabilir miyim?

Evet! **Toplu Yükleme** sayfasında Excel dosyasından isterleri yükleyebilirsin.

---

## Kullanıcı Yönetimi (Yönetici)

### 👥 Kullanıcı Sayfasına Erişim

Ana Menü → **Kullanıcı Yönetimi** (Sadece Yöneticiler)

### ➕ Yeni Kullanıcı Ekleme

1. Kullanıcı sayfasında "Yeni Kullanıcı Ekle" tıkla
2. Form:
   - **Kullanıcı Adı:** Giriş adı
   - **Ad Soyad:** Tam adı
   - **Şifre:** İlk şifre
   - **Yetki:** Yönetici veya Kullanıcı
3. "Ekle" tıkla

### ✏️ Kullanıcı Düzenleme

1. Kullanıcı listesinde kullanıcıyı bul
2. "Düzenle" tıkla
3. Alanları değiştir
4. "Kaydet" tıkla

### 🔒 Şifre Sıfırlama

1. Kullanıcı listesinde kullanıcıyı bul
2. "Şifre Sıfırla" tıkla
3. Yeni geçici şifre gösterilir
4. Kullanıcıya bildirdikten sonra değişmesi sağla

### 🗑️ Kullanıcı Silme

1. Kullanıcı listesinde kullanıcıyı bul
2. "Sil" tıkla
3. Onay penceresinde "Evet" seç

---

## Denetim Günlüğü (Audit Log)

Ana Menü → **Denetim Günlüğü** veya Sol Menü → Log

Tüm sistem değişiklikleri kaydedilir:

- Ne değişti?
- Kim tarafından değişti?
- Ne zaman değişti?
- Eski ve yeni değerler

### 🔍 Günlüğü Filtreleme

1. Günlük sayfasında
2. Filtreler:
   - **Tablo:** Hangi tabloda değişim?
   - **İşlem:** Ekleme, Güncelleme, Silme
   - **Tarih:** İçinde verilen tarih aralığı
3. "Filtrele" tıkla

---

## Düğmelerin Anlamları

| Düğme | Açıklama |
|-------|----------|
| ➕ Ekle | Yeni kayıt oluştur |
| ✏️ Düzenle | Kaydı değiştir |
| 🗑️ Sil | Kaydı sil |
| 💾 Kaydet | Değişiklikleri kaydet |
| 🔄 Geri | Değişiklikleri iptal et |
| ⬆️ / ⬇️ | Sıra değiştir |
| 📥 İndir | Dosya indir |
| 📤 Yükle | Dosya yükle |
| 🔍 Ara | Metin ara |
| 🔗 Bağla | Bağlantı oluştur |

---

## Hızlı İpuçları 💡

1. **Sekmeyi Yenile:** F5 veya Ctrl+R (tarayıcı)
2. **Otomatik Numara:** İster numaraları otomatik oluşturulur
3. **Kopyala-Yapıştır:** Tarayıcı Ctrl+C ve Ctrl+V'yi destekler
4. **Geri Git:** Tarayıcının geri düğmesini kullan
5. **Çıkış:** Çıkış seçeneğinden veya tarayıcı kapatıp açarak
6. **Dosya Format:** Excel dosyaları .xlsx olmalıdır

---

## Sorun Giderme

### 🔴 Veritabanı Bağlantısı Hatası

**Hata:** "MySQL bağlantısı başarısız"

**Çözüm:**
1. MySQL sunucusunun çalıştığını kontrol et
2. config.py'deki bağlantı bilgilerini kontrol et
3. Yeni baştan başlat: `python run.py`

### 🔴 500 Hata (İç Sunucu Hatası)

**Çözüm:**
1. Konsol çıktısını kontrol et
2. Veritabanı sorgusu hatalı olabilir
3. Yöneticiye haber ver

### 🔴 Sayfada Öğeler Yüklenmiyor

**Çözüm:**
1. Tarayıcı cache'sini temizle (Ctrl+Shift+Del)
2. Sekmeyi yenile (F5)
3. Tarayıcıyı kapat ve aç

### 🔴 Excel Dosyası Yükleme Yapılamıyor

**Çözüm:**
1. Dosyanın .xlsx formatında olduğunu kontrol et
2. Dosyada boş satır olmadığından emin ol
3. İlk satırın başlık içerdiğinden emin ol

---

## İletişim ve Destek

Sorun, hata veya öğrenme talebiniz için:

- **Sistem Yöneticiler:** Yönetici adresine e-posta gönder
- **Teknik Destek:** IT Destek (Dahili: 1234)
- **Özellik İsteği:** Sistem Yöneticisine sun

---

## Sürüm Tarihi

| Sürüm | Tarih | Değişiklik |
|--------|-------|-----------|
| 2.0 | Nisan 2025 | MVC mimarisi, yeni özellikler |
| 1.0 | Aralık 2024 | İlk sürüm |

---

**Not:** Bu kılavuz düzenli olarak güncellenmektedir. Son sürümü kontrol et.

**Hazırlandı:** Teknik Ekip  
**Son Güncelleme:** Nisan 2025
