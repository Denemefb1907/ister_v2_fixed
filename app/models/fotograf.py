"""
Fotoğraf Model
"""
from .base import BaseModel


class FotografModel(BaseModel):
    """Fotoğraf Modeli"""

    def ekle(self, node_id, foto_data, aciklama=''):
        """
        Yeni fotoğraf ekle
        
        Args:
            node_id: İster Node ID
            foto_data: Base64 fotoğraf verisi
            aciklama: Fotoğraf açıklaması
            
        Returns:
            Eklenen fotoğraf ID'si
        """
        cur = self.get_dict_cursor()
        try:
            cur.execute(
                """INSERT INTO ister_fotograf (NodeID, FotoData, Aciklama) 
                   VALUES (%s, %s, %s)""",
                (node_id, foto_data, aciklama)
            )
            self.commit()
            return cur.lastrowid
        finally:
            cur.close()

    def listesi(self, node_id):
        """
        Node'a ait fotoğrafları listele
        
        Args:
            node_id: İster Node ID
            
        Returns:
            Fotoğraf listesi
        """
        cur = self.get_dict_cursor()
        try:
            cur.execute(
                """SELECT FotoID, NodeID, FotoData, Aciklama, OlusturmaTarihi
                   FROM ister_fotograf 
                   WHERE NodeID = %s 
                   ORDER BY OlusturmaTarihi DESC""",
                (node_id,)
            )
            return cur.fetchall()
        finally:
            cur.close()

    def sil(self, foto_id):
        """
        Fotoğrafı sil
        
        Args:
            foto_id: Fotoğraf ID'si
            
        Returns:
            Silinen satır sayısı
        """
        cur = self.get_cursor()
        try:
            cur.execute(
                "DELETE FROM ister_fotograf WHERE FotoID = %s",
                (foto_id,)
            )
            self.commit()
            return cur.rowcount
        finally:
            cur.close()

    def git(self, foto_id):
        """
        Fotoğrafı ID'ye göre getir
        
        Args:
            foto_id: Fotoğraf ID'si
            
        Returns:
            Fotoğraf verileri
        """
        cur = self.get_dict_cursor()
        try:
            cur.execute(
                """SELECT FotoID, NodeID, FotoData, Aciklama, OlusturmaTarihi
                   FROM ister_fotograf 
                   WHERE FotoID = %s""",
                (foto_id,)
            )
            return cur.fetchone()
        finally:
            cur.close()

    def listesi_meta(self, node_id):
        """FotoData olmadan sadece metadata döner"""
        cur = self.get_dict_cursor()
        try:
            cur.execute(
                """SELECT FotoID, NodeID, Aciklama, OlusturmaTarihi
                FROM ister_fotograf
                WHERE NodeID = %s
                ORDER BY OlusturmaTarihi DESC""",
                (node_id,)
            )
            return cur.fetchall()
        finally:
            cur.close()
