"""
Fotoğraf API Controller'ı (Blueprint)
İster fotoğrafları CRUD işlemleri
"""
from flask import Blueprint, jsonify, request, session
from app.utils.database import mysql
from app.utils.auth import login_required
from app.utils.logging import record_log, LogType
from app.models.fotograf import FotografModel

fotograf_api_bp = Blueprint('fotograf_api', __name__, url_prefix='/api')


@fotograf_api_bp.route('/ister_fotograf/<int:node_id>', methods=['GET'])
@login_required
def ister_fotograf_listesi(node_id):
    """
    Belirli bir node'a ait fotoğrafları döner.
    
    Args:
        node_id: İster Node ID
        
    Returns:
        Fotoğraf listesi (FotoID, NodeID, FotoData, Aciklama, OlusturmaTarihi)
    """
    fm = FotografModel(mysql)
    fotograflar = fm.listesi(node_id)
    return jsonify(fotograflar)


@fotograf_api_bp.route('/ister_fotograf', methods=['POST'])
@login_required
def ister_fotograf_ekle():
    """
    Yeni fotoğraf ekler.
    
    Body: {
        NodeID: int,
        FotoData: string (base64),
        Aciklama: string (optional)
    }
    
    Returns:
        Eklenen fotoğraf ID'si
    """
    d = request.json
    fm = FotografModel(mysql)
    
    try:
        foto_id = fm.ekle(
            d['NodeID'],
            d['FotoData'],
            d.get('Aciklama', '')
        )
        record_log(
            'ister_fotograf',
            foto_id,
            'Fotoğraf',
            '-',
            f"Node {d['NodeID']} - {d.get('Aciklama', 'Açıklama Yok')}",
            LogType.CREATE.value
        )
        return jsonify({'FotoID': foto_id, 'hata': None})
    except Exception as e:
        return jsonify({'hata': str(e)})


@fotograf_api_bp.route('/ister_fotograf/<int:foto_id>', methods=['DELETE'])
@login_required
def ister_fotograf_sil(foto_id):
    """
    Fotoğrafı sil.
    
    Args:
        foto_id: Fotoğraf ID'si
        
    Returns:
        Silinen satır sayısı
    """
    fm = FotografModel(mysql)
    
    try:
        # Önce fotoğrafı bul (log kaydı için)
        foto = fm.git(foto_id)
        if not foto:
            return jsonify({'hata': 'Fotoğraf bulunamadı'})
        
        # Sil
        silinen = fm.sil(foto_id)
        
        if silinen > 0:
            record_log(
                'ister_fotograf',
                foto_id,
                'Fotoğraf',
                '-',
                f"Node {foto['NodeID']}",
                LogType.DELETE.value
            )
        
        return jsonify({'silinen': silinen, 'hata': None})
    except Exception as e:
        return jsonify({'hata': str(e)})


@fotograf_api_bp.route('/ister_fotograf/<int:foto_id>/indir', methods=['GET'])
@login_required
def ister_fotograf_indir(foto_id):
    """
    Fotoğrafı indir.
    
    Args:
        foto_id: Fotoğraf ID'si
        
    Returns:
        Fotoğraf verileri
    """
    fm = FotografModel(mysql)
    
    try:
        foto = fm.git(foto_id)
        if not foto:
            return jsonify({'hata': 'Fotoğraf bulunamadı'}), 404
        
        return jsonify(foto)
    except Exception as e:
        return jsonify({'hata': str(e)}), 500
