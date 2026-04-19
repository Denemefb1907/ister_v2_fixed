"""
Kimlik Doğrulama Controller'ı (Blueprint)
"""
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.user import UserModel
from app.utils.database import mysql

auth_bp = Blueprint('auth', __name__, url_prefix='')


@auth_bp.route('/')
def index():
    """Ana sayfa - giriş yapmışsa ana menüye, yoksa login sayfasına yönlendir"""
    if 'kullanici_id' in session:
        return redirect(url_for('main.ana_menu'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Kullanıcı giriş sayfası"""
    error = None
    
    if request.method == 'POST':
        username = request.form.get('kullanici_adi', '')
        password = request.form.get('sifre', '')
        
        user_model = UserModel(mysql)
        user = user_model.get_by_credentials(username, password)
        
        if user:
            session['kullanici_id'] = user['KullaniciID']
            session['kullanici_adi'] = user['KullaniciAdi']
            session['ad_soyad'] = user['AdSoyad']
            session.permanent = True
            
            return redirect(url_for('main.ana_menu'))
        else:
            error = 'Kullanıcı adı veya şifre hatalı.'
    
    return render_template('login.html', hata=error)


@auth_bp.route('/logout')
def logout():
    """Kullanıcı çıkış"""
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/cikis')
def cikis():
    """Çıkış (logout için alternatif route)"""
    session.clear()
    return redirect(url_for('auth.login'))
