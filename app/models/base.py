"""
Model Yönetim Başlığı
"""


class BaseModel:
    """Temel Model Sınıfı"""
    
    def __init__(self, db):
        """
        Modeli başlat
        
        Args:
            db: Veritabanı bağlantı nesnesi
        """
        self.db = db
    
    def get_dict_cursor(self):
        """Sözlük imleçi döndür"""
        import MySQLdb.cursors
        return self.db.connection.cursor(MySQLdb.cursors.DictCursor)
    
    def get_cursor(self):
        """Normal imleç döndür"""
        return self.db.connection.cursor()
    
    def commit(self):
        """Değişiklikleri kaydet"""
        self.db.connection.commit()
