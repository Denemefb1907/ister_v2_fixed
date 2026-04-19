"""
TA Dokuman (Traceability Matrix/Analysis) Modeli
"""
from app.models.base import BaseModel


class TAModel(BaseModel):
    """TA Dokuman Yönetimi Modeli"""
    
    def get_all(self, platform_id):
        """
        Platform'un TA dokümanlarını döndür
        
        Args:
            platform_id: Platform ID'si
            
        Returns:
            list: TA doküman listesi
        """
        cur = self.get_dict_cursor()
        
        cur.execute("""
            SELECT t.*, p.PlatformAdi,
                   (SELECT COUNT(*) FROM ta_sgo_baglanti WHERE TaID=t.TaID) AS SgoBaglanti
            FROM ta_dokuman t 
            JOIN platform_list p ON t.PlatformID=p.PlatformID
            WHERE t.PlatformID=%s 
            ORDER BY t.SiraNo
        """, (platform_id,))
        
        tas = cur.fetchall()
        
        for ta in tas:
            ta['Adi'] = f"TA-{ta['PlatformAdi'].replace(' ','')}-%03d" % ta['SiraNo']
        
        cur.close()
        return tas
    
    def get_by_id(self, ta_id):
        """
        TA dokümanını ID ile bul
        
        Args:
            ta_id: TA ID'si
            
        Returns:
            dict: TA doküman bilgileri
        """
        cur = self.get_dict_cursor()
        
        cur.execute("""
            SELECT t.*, p.PlatformAdi 
            FROM ta_dokuman t 
            JOIN platform_list p ON t.PlatformID=p.PlatformID 
            WHERE t.TaID=%s
        """, (ta_id,))
        
        ta = cur.fetchone()
        
        if ta:
            ta['Adi'] = f"TA-{ta['PlatformAdi'].replace(' ','')}-%03d" % ta['SiraNo']
            
            # TA Verilerini getir
            cur.execute(
                "SELECT * FROM ta_veri WHERE TaID=%s ORDER BY Sistem, Yon, Sira",
                (ta_id,)
            )
            ta['veriler'] = cur.fetchall()
            
            # TA-SGÖ Bağlantılarını getir
            cur.execute("""
                SELECT n.NodeID, n.Icerik, s.SeviyeAdi 
                FROM ta_sgo_baglanti b
                JOIN ister_node n ON b.NodeID=n.NodeID
                JOIN seviye_tanim s ON n.SeviyeID=s.SeviyeID
                WHERE b.TaID=%s
            """, (ta_id,))
            ta['sgo_ler'] = cur.fetchall()
        
        cur.close()
        return ta
    
    def create(self, platform_id, left_system='', right_system=''):
        """
        Yeni TA dokümanı oluştur
        
        Args:
            platform_id: Platform ID'si
            left_system: Sol sistem adı
            right_system: Sağ sistem adı
            
        Returns:
            int: Yeni TA ID'si
        """
        cur = self.get_dict_cursor()
        
        cur.execute(
            "SELECT COALESCE(MAX(SiraNo),0)+1 AS sira FROM ta_dokuman WHERE PlatformID=%s",
            (platform_id,)
        )
        order_no = cur.fetchone()['sira']
        
        cur2 = self.get_cursor()
        cur2.execute("""
            INSERT INTO ta_dokuman (PlatformID, SiraNo, SolSistemAdi, SagSistemAdi) 
            VALUES (%s, %s, %s, %s)
        """, (platform_id, order_no, left_system, right_system))
        
        self.commit()
        new_id = cur2.lastrowid
        
        cur.close()
        cur2.close()
        return new_id
    
    def update(self, ta_id, left_system='', right_system='', data_list=None):
        """
        TA dokümanını güncelle
        
        Args:
            ta_id: TA ID'si
            left_system: Sol sistem adı
            right_system: Sağ sistem adı
            data_list: TA veri listesi
        """
        cur = self.get_cursor()
        
        cur.execute("""
            UPDATE ta_dokuman 
            SET SolSistemAdi=%s, SagSistemAdi=%s 
            WHERE TaID=%s
        """, (left_system, right_system, ta_id))
        
        # TA Verilerini güncelle
        cur.execute("DELETE FROM ta_veri WHERE TaID=%s", (ta_id,))
        
        if data_list:
            for data in data_list:
                cur.execute("""
                    INSERT INTO ta_veri (TaID, Sistem, Yon, Icerik, Sira) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    ta_id,
                    data['sistem'],
                    data['yon'],
                    data['icerik'],
                    data.get('sira', 0)
                ))
        
        self.commit()
        cur.close()
    
    def link_sgo(self, ta_id, node_id):
        """
        TA'ya SGÖ isterini bağla
        
        Args:
            ta_id: TA ID'si
            node_id: İster (Node) ID'si
        """
        cur = self.get_dict_cursor()
        
        # Başka TA'ya bağlı mı kontrol et
        cur.execute("""
            SELECT b.TaID
            FROM ta_sgo_baglanti b
            JOIN ta_dokuman t ON b.TaID = t.TaID
            WHERE b.NodeID = %s AND b.TaID != %s AND t.TaID != (SELECT TaID FROM ta_dokuman WHERE TaID=%s LIMIT 1)
        """, (node_id, ta_id, ta_id))
        
        existing = cur.fetchone()
        
        if existing:
            cur.close()
            raise ValueError(f"Bu SGÖ, zaten TA#{existing['TaID']}'ye bağlı.")
        
        cur2 = self.get_cursor()
        cur2.execute(
            "INSERT IGNORE INTO ta_sgo_baglanti (TaID, NodeID) VALUES (%s, %s)",
            (ta_id, node_id)
        )
        self.commit()
        
        cur.close()
        cur2.close()
    
    def unlink_sgo(self, ta_id, node_id):
        """
        TA'dan SGÖ isterinin bağlantısını kaldır
        
        Args:
            ta_id: TA ID'si
            node_id: İster (Node) ID'si
        """
        cur = self.get_cursor()
        cur.execute(
            "DELETE FROM ta_sgo_baglanti WHERE TaID=%s AND NodeID=%s",
            (ta_id, node_id)
        )
        self.commit()
        cur.close()
