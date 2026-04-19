"""
Ana Sayfa ve Navigasyon Controller'ı (Blueprint)
"""
from flask import Blueprint, render_template
from app.utils.auth import login_required
from app.utils.logging import LogType

main_bp = Blueprint('main', __name__, url_prefix='')


@main_bp.route('/ana_menu')
@login_required
def ana_menu():
    """Ana menü sayfası"""
    return render_template('ana_menu.html')


@main_bp.route('/platform')
@login_required
def platform_sayfasi():
    """Platform yönetim sayfası"""
    return render_template('platform.html')


@main_bp.route('/konfig')
@login_required
def konfig_sayfasi():
    """Konfigürasyon yönetim sayfası"""
    return render_template('konfig.html')


@main_bp.route('/ister')
@login_required
def ister_sayfasi():
    """İster yönetim sayfası"""
    return render_template('ister.html')


@main_bp.route('/test_girisi')
@login_required
def test_girisi_sayfasi():
    """Test giriş sayfası"""
    return render_template('test_girisi.html')


@main_bp.route('/traceability')
@login_required
def traceability_sayfasi():
    """Traceability (izlenebilirlik) sayfası"""
    return render_template('traceability.html')


@main_bp.route('/ta_dokuman')
@login_required
def ta_dokuman_sayfasi():
    """TA Doküman sayfası"""
    return render_template('ta_dokuman.html')


@main_bp.route('/log')
@login_required
def log_sayfasi():
    """Değişiklik günlüğü sayfası"""
    return render_template('log.html', LogTur=LogType)


@main_bp.route('/kullanici')
@login_required
def kullanici_sayfasi():
    """Kullanıcı yönetim sayfası"""
    return render_template('kullanici.html')


@main_bp.route('/havuz_ister')
@login_required
def havuz_ister_sayfasi():
    """Havuz ister sayfası"""
    return render_template('havuz_ister.html')


@main_bp.route('/platform_ister')
@login_required
def platform_ister_sayfasi():
    """Platform ister sayfası"""
    return render_template('platform_ister.html')


@main_bp.route('/karsilastirma')
@login_required
def karsilastirma_sayfasi():
    """Karşılaştırma sayfası"""
    return render_template('karsilastirma.html')


@main_bp.route('/raporlar')
@login_required
def raporlar_sayfasi():
    """Raporlar sayfası"""
    return render_template('raporlar.html')
