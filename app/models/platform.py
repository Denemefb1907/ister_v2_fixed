"""
Platform Modeli
"""
from app.models.base import BaseModel


class PlatformModel(BaseModel):
    """Platform Yönetimi Modeli"""
    
    def get_all(self):
        """
        Tüm platformları döndür
        
        Returns:
            list: Platform listesi
        """
        cur = self.get_dict_cursor()
        cur.execute("SELECT * FROM platform_list ORDER BY HavuzMu DESC, PlatformAdi")
        platforms = cur.fetchall()
        for p in platforms:
            p['HavuzMu'] = 1 if p.get('HavuzMu') else 0
        cur.close()
        return platforms
    
    def get_by_id(self, platform_id):
        """
        Platform'u ID ile bul
        
        Args:
            platform_id: Platform ID'si
            
        Returns:
            dict: Platform bilgileri veya None
        """
        cur = self.get_dict_cursor()
        cur.execute("SELECT * FROM platform_list WHERE PlatformID=%s", (platform_id,))
        platform = cur.fetchone()
        cur.close()
        return platform
    
    def create(self, name):
        """
        Yeni platform oluştur
        
        Args:
            name: Platform adı
            
        Returns:
            int: Yeni platform ID'si
        """
        cur = self.get_cursor()
        cur.execute(
            "INSERT INTO platform_list (PlatformAdi, HavuzMu) VALUES (%s, 0)",
            (name,)
        )
        self.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id
    
    def update(self, platform_id, name):
        """
        Platform güncelle
        
        Args:
            platform_id: Platform ID'si
            name: Yeni platform adı
        """
        cur = self.get_cursor()
        cur.execute(
            "UPDATE platform_list SET PlatformAdi=%s WHERE PlatformID=%s",
            (name, platform_id)
        )
        self.commit()
        cur.close()
    
    def delete(self, platform_id):
        """
        Platform sil
        
        Args:
            platform_id: Platform ID'si
        """
        cur = self.get_cursor()
        cur.execute("DELETE FROM platform_list WHERE PlatformID=%s", (platform_id,))
        self.commit()
        cur.close()
    
    def get_pool_platform(self):
        """
        Havuz platformunu bul
        
        Returns:
            dict: Havuz platformu bilgileri veya None
        """
        cur = self.get_dict_cursor()
        cur.execute("SELECT * FROM platform_list WHERE HavuzMu=1 LIMIT 1")
        pool = cur.fetchone()
        cur.close()
        return pool
