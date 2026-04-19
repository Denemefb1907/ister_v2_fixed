"""
Kimlik Doğrulama Utiliteleri
"""
from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    """Giriş yapmış kullanıcı gerekli dekoratörü"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'kullanici_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def get_session_user():
    """Oturumdaki kullanıcı bilgilerini döndür"""
    return {
        'kullanici_id': session.get('kullanici_id'),
        'kullanici_adi': session.get('kullanici_adi'),
        'ad_soyad': session.get('ad_soyad')
    }
