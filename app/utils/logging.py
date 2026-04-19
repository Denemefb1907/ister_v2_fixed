"""
Değişiklik Günlüğü ve Logging Utiliteleri
"""
from datetime import datetime, timezone, timedelta
from enum import Enum
from flask import session
from app.utils.database import mysql


class LogType(Enum):
    """Günlük tür tanımları"""
    CREATE = "Ekleme"
    UPDATE = "Güncelleme"
    DELETE = "Silme"


def record_log(table_name, record_id, field_name, old_value, new_value, log_type):
    """
    Veritabanında değişiklik günlüğü kaydet
    
    Args:
        table_name: Tablo adı
        record_id: Kayıt ID'si
        field_name: Alan adı
        old_value: Eski değer
        new_value: Yeni değer
        log_type: Günlük türü (CREATE, UPDATE, DELETE)
    """
    # Aynı değer ise kaydetme
    if str(old_value or '') == str(new_value or ''):
        return
    
    cur = mysql.connection.cursor()
    
    # Saat dilimi: UTC+3 (Türkiye)
    tz = timezone(timedelta(hours=3))
    now = datetime.now(tz)
    
    try:
        cur.execute("""
            INSERT INTO degisiklik_log 
            (TabloAdi, KayitID, AlanAdi, EskiDeger, YeniDeger, KullaniciID, 
             KullaniciAdi, DegisimTarihi, Tur)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            table_name,
            record_id,
            field_name,
            str(old_value or ''),
            str(new_value or ''),
            session.get('kullanici_id'),
            session.get('kullanici_adi'),
            now,
            log_type if isinstance(log_type, str) else log_type.value
        ))
        mysql.connection.commit()
    except Exception as e:
        print(f"Günlük kayıt hatası: {e}")
    finally:
        cur.close()
