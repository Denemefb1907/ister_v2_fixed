"""
SQLite Schema Başlatıcı  —  İster Yönetim Sistemi v2
Uygulama ilk çalıştığında otomatik çağrılır (app/__init__.py içinden).
sqlite.db yoksa sıfırdan oluşturur; varsa sadece eksik tabloları/sütunları ekler.

Kullanım:
    from init_schema import init_schema
    init_schema(app)          # Flask app nesnesiyle
    # veya doğrudan:
    init_schema(db_path='sqlite.db')
"""
import sqlite3
import os


# ─────────────────────────────────────────────────────────────────────────────
# Tablo tanımları  (MySQL → SQLite dönüşümleri uygulandı)
#   - AUTO_INCREMENT       → INTEGER PRIMARY KEY AUTOINCREMENT
#   - TINYINT(1)           → INTEGER
#   - LONGTEXT / NVARCHAR  → TEXT
#   - JSON                 → TEXT  (uygulama zaten json.dumps/loads yapıyor)
#   - ENUM(...)            → TEXT  (CHECK kısıtı ile korunuyor)
#   - UNIQUE KEY adı (...)  → UNIQUE (...)
#   - CHARACTER SET / COLLATE satırları kaldırıldı
# ─────────────────────────────────────────────────────────────────────────────

_TABLES = """
CREATE TABLE IF NOT EXISTS kullanici (
    KullaniciID   INTEGER PRIMARY KEY AUTOINCREMENT,
    KullaniciAdi  TEXT NOT NULL UNIQUE,
    Sifre         TEXT NOT NULL,
    AdSoyad       TEXT,
    AktifMi       INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS konfig_list (
    KonfigID  INTEGER PRIMARY KEY AUTOINCREMENT,
    KonfigAdi TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS platform_list (
    PlatformID  INTEGER PRIMARY KEY AUTOINCREMENT,
    PlatformAdi TEXT NOT NULL,
    HavuzMu     INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS platform_konfig (
    PlatformKonfigID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlatformID       INTEGER NOT NULL,
    KonfigID         INTEGER NOT NULL,
    UNIQUE (PlatformID, KonfigID),
    FOREIGN KEY (PlatformID) REFERENCES platform_list(PlatformID) ON DELETE CASCADE,
    FOREIGN KEY (KonfigID)   REFERENCES konfig_list(KonfigID)     ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS seviye_tanim (
    SeviyeID   INTEGER PRIMARY KEY AUTOINCREMENT,
    PlatformID INTEGER NOT NULL,
    SeviyeNo   INTEGER NOT NULL,
    SeviyeAdi  TEXT    NOT NULL,
    UNIQUE (PlatformID, SeviyeNo),
    FOREIGN KEY (PlatformID) REFERENCES platform_list(PlatformID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS test_asama (
    TestAsamaID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlatformID  INTEGER NOT NULL,
    AsamaNo     INTEGER NOT NULL,
    AsamaAdi    TEXT    NOT NULL,
    UNIQUE (PlatformID, AsamaNo),
    FOREIGN KEY (PlatformID) REFERENCES platform_list(PlatformID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS test_yontemi (
    TestYontemiID INTEGER PRIMARY KEY AUTOINCREMENT,
    YontemAdi     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ister_node (
    NodeID           INTEGER PRIMARY KEY AUTOINCREMENT,
    PlatformID       INTEGER NOT NULL,
    SeviyeID         INTEGER NOT NULL,
    ParentID         INTEGER NULL,
    HavuzNodeID      INTEGER NULL,
    KonfigID         INTEGER NULL,
    NodeNumarasi     TEXT    NULL,
    GignBaslik       INTEGER DEFAULT 0,
    UstBaslikID      INTEGER NULL,
    IsterTipi        TEXT    DEFAULT 'G' CHECK (IsterTipi IN ('B','G')),
    HavuzKodu        TEXT    NULL,
    Icerik           TEXT,
    TestYontemiID    INTEGER NULL,
    IlgiliAsamaID    INTEGER NULL,
    DegistirildiMi   INTEGER DEFAULT 0,
    SiraNo           INTEGER DEFAULT 0,
    OlusturanID      INTEGER,
    OlusturmaTarihi  TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (PlatformID)    REFERENCES platform_list(PlatformID) ON DELETE CASCADE,
    FOREIGN KEY (SeviyeID)      REFERENCES seviye_tanim(SeviyeID),
    FOREIGN KEY (ParentID)      REFERENCES ister_node(NodeID)        ON DELETE CASCADE,
    FOREIGN KEY (KonfigID)      REFERENCES konfig_list(KonfigID),
    FOREIGN KEY (TestYontemiID) REFERENCES test_yontemi(TestYontemiID),
    FOREIGN KEY (OlusturanID)   REFERENCES kullanici(KullaniciID)
);

CREATE TABLE IF NOT EXISTS ister_baglanti (
    BaglantiID   INTEGER PRIMARY KEY AUTOINCREMENT,
    KaynakNodeID INTEGER NOT NULL,
    HedefNodeID  INTEGER NOT NULL,
    UNIQUE (KaynakNodeID, HedefNodeID),
    FOREIGN KEY (KaynakNodeID) REFERENCES ister_node(NodeID) ON DELETE CASCADE,
    FOREIGN KEY (HedefNodeID)  REFERENCES ister_node(NodeID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS test_sonuc (
    TestSonucID INTEGER PRIMARY KEY AUTOINCREMENT,
    NodeID      INTEGER NOT NULL,
    TestAsamaID INTEGER NOT NULL,
    Sonuc       TEXT    NOT NULL CHECK (Sonuc IN ('Basarili','Hatali')),
    Aciklama    TEXT,
    KullaniciID INTEGER,
    Tarih       TEXT    DEFAULT (datetime('now')),
    UNIQUE (NodeID, TestAsamaID),
    FOREIGN KEY (NodeID)      REFERENCES ister_node(NodeID)   ON DELETE CASCADE,
    FOREIGN KEY (TestAsamaID) REFERENCES test_asama(TestAsamaID) ON DELETE CASCADE,
    FOREIGN KEY (KullaniciID) REFERENCES kullanici(KullaniciID)
);

CREATE TABLE IF NOT EXISTS ta_dokuman (
    TaID         INTEGER PRIMARY KEY AUTOINCREMENT,
    PlatformID   INTEGER NOT NULL,
    SiraNo       INTEGER NOT NULL,
    HavuzTaID    INTEGER NULL,
    SolSistemAdi TEXT,
    SagSistemAdi TEXT,
    FOREIGN KEY (PlatformID) REFERENCES platform_list(PlatformID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ta_veri (
    TaVeriID INTEGER PRIMARY KEY AUTOINCREMENT,
    TaID     INTEGER NOT NULL,
    Sistem   TEXT    NOT NULL CHECK (Sistem IN ('sol','sag')),
    Yon      TEXT    NOT NULL CHECK (Yon    IN ('aldigi','verdigi')),
    Icerik   TEXT,
    Sira     INTEGER DEFAULT 0,
    FOREIGN KEY (TaID) REFERENCES ta_dokuman(TaID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ta_sgo_baglanti (
    BaglantiID INTEGER PRIMARY KEY AUTOINCREMENT,
    TaID       INTEGER NOT NULL,
    NodeID     INTEGER NOT NULL,
    UNIQUE (TaID, NodeID),
    FOREIGN KEY (TaID)    REFERENCES ta_dokuman(TaID)    ON DELETE CASCADE,
    FOREIGN KEY (NodeID)  REFERENCES ister_node(NodeID)  ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS degisiklik_log (
    LogID          INTEGER PRIMARY KEY AUTOINCREMENT,
    TabloAdi       TEXT,
    KayitID        INTEGER,
    AlanAdi        TEXT,
    EskiDeger      TEXT,
    YeniDeger      TEXT,
    Tur            TEXT NOT NULL DEFAULT '',
    KullaniciID    INTEGER,
    KullaniciAdi   TEXT,
    DegisimTarihi  TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS ister_tablo (
    TabloID          INTEGER PRIMARY KEY AUTOINCREMENT,
    NodeID           INTEGER NOT NULL,
    TabloAdi         TEXT,
    SutunBasliklari  TEXT,   -- JSON string
    Satirlar         TEXT,   -- JSON string
    OlusturanID      INTEGER,
    OlusturmaTarihi  TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (NodeID) REFERENCES ister_node(NodeID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS firma_gorusu (
    GorusID         INTEGER PRIMARY KEY AUTOINCREMENT,
    NodeID          INTEGER NOT NULL,
    PlatformID      INTEGER NOT NULL,
    FirmaAdi        TEXT    NOT NULL,
    GorusIcerik     TEXT,
    GorusOzet       TEXT,
    GorusKategori   TEXT,
    OlusturanID     INTEGER,
    OlusturmaTarihi TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (NodeID)     REFERENCES ister_node(NodeID)     ON DELETE CASCADE,
    FOREIGN KEY (PlatformID) REFERENCES platform_list(PlatformID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS firma_gorusu_yanit (
    YanitID         INTEGER PRIMARY KEY AUTOINCREMENT,
    GorusID         INTEGER NOT NULL,
    YanitIcerik     TEXT,
    YazanID         INTEGER,
    OlusturmaTarihi TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (GorusID) REFERENCES firma_gorusu(GorusID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ister_onay (
    OnayID      INTEGER PRIMARY KEY AUTOINCREMENT,
    NodeID      INTEGER NOT NULL,
    PlatformID  INTEGER NOT NULL,
    OnayDurumu  INTEGER DEFAULT 0,
    OnaylayanID INTEGER,
    OnayTarihi  TEXT,
    UNIQUE (NodeID, PlatformID),
    FOREIGN KEY (NodeID)     REFERENCES ister_node(NodeID)        ON DELETE CASCADE,
    FOREIGN KEY (PlatformID) REFERENCES platform_list(PlatformID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ister_bullet (
    BulletID        INTEGER PRIMARY KEY AUTOINCREMENT,
    NodeID          INTEGER NOT NULL,
    SiraNo          INTEGER DEFAULT 0,
    Icerik          TEXT    NOT NULL,
    OlusturanID     INTEGER,
    OlusturmaTarihi TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (NodeID) REFERENCES ister_node(NodeID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ister_fotograf (
    FotoID          INTEGER PRIMARY KEY AUTOINCREMENT,
    NodeID          INTEGER NOT NULL,
    FotoData        BLOB    NOT NULL,
    Aciklama        TEXT    NULL,
    OlusturmaTarihi TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (NodeID) REFERENCES ister_node(NodeID) ON DELETE CASCADE
);
"""

# ─────────────────────────────────────────────────────────────────────────────
# Başlangıç verileri  (INSERT OR IGNORE — tekrar çalıştırılabilir)
# ─────────────────────────────────────────────────────────────────────────────

_SEED = """
INSERT OR IGNORE INTO kullanici (KullaniciAdi, Sifre, AdSoyad, AktifMi)
    VALUES ('admin', 'admin123', 'Sistem Yöneticisi', 1);

INSERT OR IGNORE INTO platform_list (PlatformAdi, HavuzMu)
    VALUES ('HAVUZ', 1);

INSERT OR IGNORE INTO test_yontemi (YontemAdi) VALUES
    ('Fonksiyonel Test'),
    ('Belge Sunumu'),
    ('Performans Testi'),
    ('Güvenlik Testi'),
    ('Entegrasyon Testi');
"""

# ─────────────────────────────────────────────────────────────────────────────
# Sütun ekleme migrasyonları  (ALTER TABLE IF NOT EXISTS yok, elle kontrol)
# ─────────────────────────────────────────────────────────────────────────────

_MIGRATIONS = [
    # (tablo, sütun, tanım)
    ("ister_node",     "IsterTipi",     "TEXT DEFAULT 'G'"),
    ("ister_node",     "HavuzKodu",     "TEXT NULL"),
    ("ister_node",     "IlgiliAsamaID", "INTEGER NULL"),
    ("ister_node",     "SiraNo",        "INTEGER DEFAULT 0"),
    ("degisiklik_log", "Tur",           "TEXT NOT NULL DEFAULT ''"),
]


def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    cur = conn.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
    )
    return cur.fetchone() is not None


# ─────────────────────────────────────────────────────────────────────────────
# Ana fonksiyon
# ─────────────────────────────────────────────────────────────────────────────

def init_schema(app=None, db_path: str = None):
    """
    Tabloları oluştur, eksik sütunları ekle, seed verilerini yükle.

    Args:
        app:     Flask app nesnesi (config['SQLITE_PATH'] okunur)
        db_path: Doğrudan yol (app yoksa kullanılır), default 'sqlite.db'
    """
    if db_path is None:
        if app is not None:
            db_path = app.config.get('SQLITE_PATH', 'sqlite.db')
        else:
            db_path = 'sqlite.db'

    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.execute('PRAGMA journal_mode = WAL')

    # 1. Tabloları oluştur
    conn.executescript(_TABLES)

    # 2. Eksik sütunları ekle (migration)
    for table, column, definition in _MIGRATIONS:
        if _table_exists(conn, table) and not _column_exists(conn, table, column):
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
            print(f"[schema] Sütun eklendi: {table}.{column}")



    # Duplicate temizleme (ilk kayıt kalsın)

    # FK kapat
    conn.execute("PRAGMA foreign_keys = OFF")
    # SADECE test_yontemi temizle
    conn.execute("""
    DELETE FROM test_yontemi
    WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM test_yontemi
    GROUP BY YontemAdi
    )
    """)

    # UNIQUE index'leri oluştur (yoksa oluşturur)
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_test_yontemi_ad ON test_yontemi(YontemAdi)")
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_platform_ad ON platform_list(PlatformAdi)") 
    # FK tekrar aç
    conn.execute("PRAGMA foreign_keys = ON")

    # 3. Seed verilerini yükle
    conn.executescript(_SEED)

    conn.commit()
    conn.close()

    if app:
        app.logger.info('[schema] SQLite schema hazır  →  %s', db_path)
    else:
        print(f'[schema] SQLite schema hazır  →  {db_path}')


# ─────────────────────────────────────────────────────────────────────────────
# Doğrudan çalıştırma:  python init_schema.py
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'sqlite.db'
    init_schema(db_path=path)