"""
Seviye (Level) API Controller'ı (Blueprint)
"""
from flask import Blueprint, request, jsonify
from app.models.level import LevelModel
from app.utils.auth import login_required
from app.utils.database import mysql

level_api_bp = Blueprint('level_api', __name__, url_prefix='/api')


@level_api_bp.route('/platform/<int:platform_id>/seviye', methods=['GET'])
@login_required
def get_levels(platform_id):
    """Platform'un seviyelerini döndür"""
    model = LevelModel(mysql)
    levels = model.get_levels(platform_id)
    return jsonify(levels)


@level_api_bp.route('/platform/<int:platform_id>/seviye_ve_asama', methods=['GET'])
@login_required
def get_levels_with_phases(platform_id):
    """Seviyeleri + test aşamalarını döndür"""
    model = LevelModel(mysql)
    data = model.get_levels_with_phases(platform_id)
    return jsonify(data)


@level_api_bp.route('/platform/<int:platform_id>/seviye', methods=['POST'])
@login_required
def create_level(platform_id):
    """Yeni seviye oluştur"""
    data = request.json
    
    if not data or 'SeviyeAdi' not in data:
        return jsonify({'error': 'Seviye adı gerekli'}), 400
    
    model = LevelModel(mysql)
    new_id = model.create(platform_id, data['SeviyeAdi'])
    
    # Seviyenin sırasını bul
    levels = model.get_levels(platform_id)
    new_level = next((l for l in levels if l['SeviyeID'] == new_id), {})
    
    return jsonify({
        'SeviyeID': new_id,
        'SeviyeNo': new_level.get('SeviyeNo', 0),
        'SeviyeAdi': data['SeviyeAdi']
    }), 201


@level_api_bp.route('/seviye/<int:level_id>', methods=['PUT'])
@login_required
def update_level(level_id):
    """Seviye güncelle"""
    data = request.json
    
    if not data or 'SeviyeAdi' not in data:
        return jsonify({'error': 'Seviye adı gerekli'}), 400
    
    model = LevelModel(mysql)
    model.update(level_id, data['SeviyeAdi'])
    
    return jsonify({'ok': True})


@level_api_bp.route('/seviye/<int:level_id>', methods=['DELETE'])
@login_required
def delete_level(level_id):
    """Seviye sil"""
    model = LevelModel(mysql)
    model.delete(level_id)
    
    return jsonify({'ok': True})
