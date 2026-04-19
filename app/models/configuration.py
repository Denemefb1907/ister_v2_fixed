"""
Konfigürasyon Modeli
"""
from app.models.base import BaseModel


class ConfigurationModel(BaseModel):
    """Konfigürasyon Yönetimi Modeli"""
    
    def get_all(self):
        """
        Tüm konfigürasyonları döndür
        
        Returns:
            list: Konfigürasyon listesi
        """
        cur = self.get_dict_cursor()
        cur.execute("SELECT * FROM konfig_list ORDER BY KonfigAdi")
        configs = cur.fetchall()
        cur.close()
        return configs
    
    def get_by_id(self, config_id):
        """
        Konfigürasyonu ID ile bul
        
        Args:
            config_id: Konfigürasyon ID'si
            
        Returns:
            dict: Konfigürasyon bilgileri veya None
        """
        cur = self.get_dict_cursor()
        cur.execute("SELECT * FROM konfig_list WHERE KonfigID=%s", (config_id,))
        config = cur.fetchone()
        cur.close()
        return config
    
    def create(self, name):
        """
        Yeni konfigürasyon oluştur
        
        Args:
            name: Konfigürasyon adı
            
        Returns:
            int: Yeni konfigürasyon ID'si
        """
        cur = self.get_cursor()
        cur.execute("INSERT INTO konfig_list (KonfigAdi) VALUES (%s)", (name,))
        self.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id
    
    def update(self, config_id, name):
        """
        Konfigürasyonu güncelle
        
        Args:
            config_id: Konfigürasyon ID'si
            name: Yeni konfigürasyon adı
        """
        cur = self.get_cursor()
        cur.execute(
            "UPDATE konfig_list SET KonfigAdi=%s WHERE KonfigID=%s",
            (name, config_id)
        )
        self.commit()
        cur.close()
    
    def delete(self, config_id):
        """
        Konfigürasyonu sil
        
        Args:
            config_id: Konfigürasyon ID'si
        """
        cur = self.get_cursor()
        cur.execute("DELETE FROM konfig_list WHERE KonfigID=%s", (config_id,))
        self.commit()
        cur.close()
    
    def get_by_platform(self, platform_id):
        """
        Platform'a bağlı konfigürasyonları döndür
        
        Args:
            platform_id: Platform ID'si
            
        Returns:
            list: Konfigürasyon ID listesi
        """
        cur = self.get_dict_cursor()
        cur.execute(
            "SELECT KonfigID FROM platform_konfig WHERE PlatformID=%s",
            (platform_id,)
        )
        results = cur.fetchall()
        cur.close()
        return [r['KonfigID'] for r in results]
    
    def set_platform_configs(self, platform_id, config_ids):
        """
        Platform'un konfigürasyonlarını belirle
        
        Args:
            platform_id: Platform ID'si
            config_ids: Konfigürasyon ID listesi
        """
        cur = self.get_cursor()
        cur.execute(
            "DELETE FROM platform_konfig WHERE PlatformID=%s",
            (platform_id,)
        )
        for config_id in config_ids:
            cur.execute(
                "INSERT INTO platform_konfig (PlatformID, KonfigID) VALUES (%s, %s)",
                (platform_id, config_id)
            )
        self.commit()
        cur.close()
