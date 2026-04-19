"""
Seviye Modeli - İster Seviyeleri
"""
from app.models.base import BaseModel


class LevelModel(BaseModel):
    """İster Seviye Yönetimi Modeli"""
    
    def get_levels(self, platform_id):
        """
        Platform'un seviyelerini döndür
        
        Args:
            platform_id: Platform ID'si
            
        Returns:
            list: Seviye listesi
        """
        cur = self.get_dict_cursor()
        cur.execute(
            "SELECT * FROM seviye_tanim WHERE PlatformID=%s ORDER BY SeviyeNo",
            (platform_id,)
        )
        levels = cur.fetchall()
        cur.close()
        return levels
    
    def get_levels_with_phases(self, platform_id):
        """
        Seviyeleri + test aşamalarını birleşik döndür
        (İster ekleme dropdown'u için)
        
        Args:
            platform_id: Platform ID'si
            
        Returns:
            list: Seviye ve aşama listesi
        """
        cur = self.get_dict_cursor()
        
        cur.execute(
            "SELECT SeviyeID, SeviyeNo, SeviyeAdi, 'seviye' AS tip, NULL AS AsamaID FROM seviye_tanim WHERE PlatformID=%s ORDER BY SeviyeNo",
            (platform_id,)
        )
        levels = cur.fetchall()
        
        # Son seviyeyi bul — test isterleri bu seviyede oluşturulacak
        last_level_id = levels[-1]['SeviyeID'] if levels else None
        
        cur.execute(
            "SELECT TestAsamaID, AsamaNo, AsamaAdi FROM test_asama WHERE PlatformID=%s ORDER BY AsamaNo",
            (platform_id,)
        )
        phases = cur.fetchall()
        
        # Test aşamaları için gerçek SeviyeID (son seviye), AsamaID ayrı
        phase_list = []
        if last_level_id:
            phase_list = [
                {
                    'SeviyeID': last_level_id,
                    'SeviyeNo': 999,
                    'SeviyeAdi': p['AsamaAdi'],
                    'tip': 'asama',
                    'AsamaID': p['TestAsamaID']
                }
                for p in phases
            ]
        
        cur.close()
        return list(levels) + phase_list
    
    def create(self, platform_id, level_name):
        """
        Yeni seviye oluştur
        
        Args:
            platform_id: Platform ID'si
            level_name: Seviye adı
            
        Returns:
            int: Yeni seviye ID'si
        """
        cur = self.get_dict_cursor()
        cur.execute(
            "SELECT COALESCE(MAX(SeviyeNo),0)+1 AS sira FROM seviye_tanim WHERE PlatformID=%s",
            (platform_id,)
        )
        order_no = cur.fetchone()['sira']
        
        cur2 = self.get_cursor()
        cur2.execute(
            "INSERT INTO seviye_tanim (PlatformID, SeviyeNo, SeviyeAdi) VALUES (%s, %s, %s)",
            (platform_id, order_no, level_name)
        )
        self.commit()
        new_id = cur2.lastrowid
        
        cur.close()
        cur2.close()
        return new_id
    
    def update(self, level_id, level_name):
        """
        Seviyeyi güncelle
        
        Args:
            level_id: Seviye ID'si
            level_name: Yeni seviye adı
        """
        cur = self.get_cursor()
        cur.execute(
            "UPDATE seviye_tanim SET SeviyeAdi=%s WHERE SeviyeID=%s",
            (level_name, level_id)
        )
        self.commit()
        cur.close()
    
    def delete(self, level_id):
        """
        Seviyeyi sil
        
        Args:
            level_id: Seviye ID'si
        """
        cur = self.get_cursor()
        cur.execute("DELETE FROM seviye_tanim WHERE SeviyeID=%s", (level_id,))
        self.commit()
        cur.close()
