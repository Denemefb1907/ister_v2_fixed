"""
Test Modeli - Test Aşamaları ve Sonuçları
"""
from app.models.base import BaseModel


class TestModel(BaseModel):
    """Test Aşama ve Sonuç Yönetimi Modeli"""
    
    # ── TEST AŞAMALARI ────────────────────────────────────────────────────────
    
    def get_phases(self, platform_id):
        """
        Platform'un test aşamalarını döndür
        
        Args:
            platform_id: Platform ID'si
            
        Returns:
            list: Test aşaması listesi
        """
        cur = self.get_dict_cursor()
        cur.execute(
            "SELECT * FROM test_asama WHERE PlatformID=%s ORDER BY AsamaNo",
            (platform_id,)
        )
        phases = cur.fetchall()
        cur.close()
        return phases
    
    def create_phase(self, platform_id, phase_name):
        """
        Yeni test aşaması oluştur
        
        Args:
            platform_id: Platform ID'si
            phase_name: Aşama adı
            
        Returns:
            int: Yeni aşama ID'si
        """
        cur = self.get_dict_cursor()
        cur.execute(
            "SELECT COALESCE(MAX(AsamaNo),0)+1 AS sira FROM test_asama WHERE PlatformID=%s",
            (platform_id,)
        )
        order_no = cur.fetchone()['sira']
        
        cur2 = self.get_cursor()
        cur2.execute(
            "INSERT INTO test_asama (PlatformID, AsamaNo, AsamaAdi) VALUES (%s, %s, %s)",
            (platform_id, order_no, phase_name)
        )
        self.commit()
        new_id = cur2.lastrowid
        
        cur.close()
        cur2.close()
        return new_id
    
    def update_phase(self, phase_id, phase_name):
        """
        Test aşamasını güncelle
        
        Args:
            phase_id: Aşama ID'si
            phase_name: Yeni aşama adı
        """
        cur = self.get_cursor()
        cur.execute(
            "UPDATE test_asama SET AsamaAdi=%s WHERE TestAsamaID=%s",
            (phase_name, phase_id)
        )
        self.commit()
        cur.close()
    
    def delete_phase(self, phase_id):
        """
        Test aşamasını sil
        
        Args:
            phase_id: Aşama ID'si
        """
        cur = self.get_cursor()
        cur.execute("DELETE FROM test_asama WHERE TestAsamaID=%s", (phase_id,))
        self.commit()
        cur.close()
    
    # ── TEST SONUÇLARI ────────────────────────────────────────────────────────
    
    def get_results(self, platform_id, phase_id=None):
        """
        Test sonuçlarını döndür
        
        Args:
            platform_id: Platform ID'si
            phase_id: Opsiyonel - Aşama ID'si
            
        Returns:
            list: Test sonuç listesi
        """
        cur = self.get_dict_cursor()
        
        q = """
        SELECT ts.*, n.Icerik AS NodeIcerik, ta.AsamaAdi,
               s.SeviyeAdi, s.SeviyeNo,
               pn.Icerik AS ParentIcerik
        FROM test_sonuc ts
        JOIN ister_node n ON ts.NodeID=n.NodeID
        JOIN test_asama ta ON ts.TestAsamaID=ta.TestAsamaID
        JOIN seviye_tanim s ON n.SeviyeID=s.SeviyeID
        LEFT JOIN ister_node pn ON n.ParentID=pn.NodeID
        WHERE ta.PlatformID=%s
        """
        
        params = [platform_id]
        
        if phase_id:
            q += " AND ts.TestAsamaID=%s"
            params.append(phase_id)
        
        q += " ORDER BY ts.NodeID"
        
        cur.execute(q, params)
        results = cur.fetchall()
        
        for r in results:
            if r.get('Tarih'):
                r['Tarih'] = r['Tarih'].strftime('%d.%m.%Y %H:%M')
        
        cur.close()
        return results
    
    def get_untested_nodes(self, platform_id, phase_id=None):
        """
        Test sonucu girilmemiş isterleri döndür
        
        Args:
            platform_id: Platform ID'si
            phase_id: Opsiyonel - Aşama ID'si
            
        Returns:
            list: Test edilmemiş ister listesi
        """
        cur = self.get_dict_cursor()
        
        q = """
        SELECT n.NodeID, n.Icerik, n.ParentID, s.SeviyeAdi, s.SeviyeNo,
               pn.Icerik AS ParentIcerik, ppn.Icerik AS GrandParentIcerik
        FROM ister_node n
        JOIN seviye_tanim s ON n.SeviyeID=s.SeviyeID
        LEFT JOIN ister_node pn ON n.ParentID=pn.NodeID
        LEFT JOIN ister_node ppn ON pn.ParentID=ppn.NodeID
        WHERE n.PlatformID=%s
        AND n.NodeID NOT IN (
            SELECT DISTINCT ParentID FROM ister_node 
            WHERE ParentID IS NOT NULL AND PlatformID=%s
        )
        """
        
        params = [platform_id, platform_id]
        
        if phase_id:
            q += " AND n.NodeID NOT IN (SELECT NodeID FROM test_sonuc WHERE TestAsamaID=%s)"
            params.append(phase_id)
        
        cur.execute(q, params)
        nodes = cur.fetchall()
        cur.close()
        
        return nodes
    
    def save_result(self, node_id, phase_id, result, explanation='', user_id=None):
        """
        Test sonucunu kaydet
        
        Args:
            node_id: İster ID'si
            phase_id: Aşama ID'si
            result: Sonuç (Basarili, Hatali, vb.)
            explanation: Açıklama (opsiyonel)
            user_id: Kullanıcı ID'si (opsiyonel)
        """
        cur = self.get_dict_cursor()
        
        cur.execute(
            "SELECT * FROM test_sonuc WHERE NodeID=%s AND TestAsamaID=%s",
            (node_id, phase_id)
        )
        existing = cur.fetchone()
        
        cur2 = self.get_cursor()
        
        if existing:
            cur2.execute(
                "UPDATE test_sonuc SET Sonuc=%s, Aciklama=%s, KullaniciID=%s, Tarih=NOW() WHERE TestSonucID=%s",
                (result, explanation, user_id, existing['TestSonucID'])
            )
        else:
            cur2.execute(
                "INSERT INTO test_sonuc (NodeID, TestAsamaID, Sonuc, Aciklama, KullaniciID) VALUES (%s, %s, %s, %s, %s)",
                (node_id, phase_id, result, explanation, user_id)
            )
        
        self.commit()
        cur.close()
        cur2.close()
