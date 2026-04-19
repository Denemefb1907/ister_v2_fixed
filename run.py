#!/usr/bin/env python3
"""
İster Yönetimi v2 - Ana Başlatıcı
MVC Tasarım Deseni ile Uygulaması
"""
import os
import sys
from app import create_app

# Uygulamayı oluştur
app = create_app(os.environ.get('FLASK_ENV', 'development'))


if __name__ == '__main__':
    # Komut satırı argümanlarını kontrol et
    debug_mode = '--dev' in sys.argv
    
    if debug_mode:
        # Geliştirme modu
        print("🔧 Geliştirme Modu Aktif")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        # Üretim modu (Waitress sunucusu ile)
        try:
            from waitress import serve
            print("✅ İster Yönetim Sistemi v2 başlatıldı.")
            print("📍 Tarayıcıda açın: http://localhost:5000")
            serve(app, host='0.0.0.0', port=5000, threads=8)
        except ImportError:
            print("⚠️  Waitress bulunamadı. Flask development server kullanılıyor...")
            app.run(host='0.0.0.0', port=5000, debug=False)
