"""
Kullanıcı Modeli
"""
from app.models.base import BaseModel


class UserModel(BaseModel):
    """Kullanıcı Modeli"""
    
    def get_by_credentials(self, username, password):
        """
        Kullanıcı adı ve şifre ile kullanıcı bul
        
        Args:
            username: Kullanıcı adı
            password: Şifre
            
        Returns:
            dict: Kullanıcı bilgileri veya None
        """
        cur = self.get_dict_cursor()
        cur.execute("""
            SELECT * FROM kullanici 
            WHERE KullaniciAdi=%s AND Sifre=%s AND AktifMi=1
        """, (username, password))
        user = cur.fetchone()
        cur.close()
        return user
    
    def get_by_id(self, user_id):
        """
        ID ile kullanıcı bul
        
        Args:
            user_id: Kullanıcı ID'si
            
        Returns:
            dict: Kullanıcı bilgileri veya None
        """
        cur = self.get_dict_cursor()
        cur.execute("SELECT * FROM kullanici WHERE KullaniciID=%s", (user_id,))
        user = cur.fetchone()
        cur.close()
        return user
    
    def get_all(self):
        """
        Tüm kullanıcıları döndür
        
        Returns:
            list: Kullanıcı listesi
        """
        cur = self.get_dict_cursor()
        cur.execute("SELECT * FROM kullanici ORDER BY AdSoyad")
        users = cur.fetchall()
        cur.close()
        return users
