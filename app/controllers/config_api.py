"""
Konfigürasyon API Controller'ı (Blueprint)
"""
from flask import Blueprint, request, jsonify
from app.models.configuration import ConfigurationModel
from app.utils.auth import login_required
from app.utils.database import mysql
from app.utils.logging import record_log, LogType

config_api_bp = Blueprint('config_api', __name__, url_prefix='/api')


@config_api_bp.route('/konfig', methods=['GET'])
@login_required
def get_configurations():
    """Tüm konfigürasyonları döndür"""
    model = ConfigurationModel(mysql)
    configs = model.get_all()
    return jsonify(configs)


@config_api_bp.route('/konfig', methods=['POST'])
@login_required
def create_configuration():
    """Yeni konfigürasyon oluştur"""
    data = request.json
    
    if not data or 'KonfigAdi' not in data:
        return jsonify({'error': 'Konfigürasyon adı gerekli'}), 400
    
    model = ConfigurationModel(mysql)
    new_id = model.create(data['KonfigAdi'])
    
    record_log('konfig_list', new_id, 'Konfig', '-', data['KonfigAdi'], LogType.CREATE.value)
    
    return jsonify({'KonfigID': new_id, 'KonfigAdi': data['KonfigAdi']}), 201


@config_api_bp.route('/konfig/<int:config_id>', methods=['PUT'])
@login_required
def update_configuration(config_id):
    """Konfigürasyon güncelle"""
    data = request.json
    
    if not data or 'KonfigAdi' not in data:
        return jsonify({'error': 'Konfigürasyon adı gerekli'}), 400
    
    model = ConfigurationModel(mysql)
    existing = model.get_by_id(config_id)
    
    if not existing:
        return jsonify({'error': 'Konfigürasyon bulunamadı'}), 404
    
    model.update(config_id, data['KonfigAdi'])
    
    record_log('konfig_list', config_id, 'KonfigAdi', 
               existing['KonfigAdi'], data['KonfigAdi'], LogType.UPDATE.value)
    
    return jsonify({'ok': True})


@config_api_bp.route('/konfig/<int:config_id>/check-usage', methods=['GET'])
@login_required
def check_config_usage(config_id):
    """Konfigürasyonun isterde kullanılıp kullanılmadığını kontrol et"""
    model = ConfigurationModel(mysql)
    existing = model.get_by_id(config_id)
    
    if not existing:
        return jsonify({'error': 'Konfigürasyon bulunamadı'}), 404
    
    # Check if configuration is used in any requirements
    used_in_requirements = model.get_requirements_using_config(config_id)
    
    return jsonify({
        'KonfigAdi': existing['KonfigAdi'],
        'isUsed': len(used_in_requirements) > 0,
        'details': used_in_requirements
    })


@config_api_bp.route('/konfig/<int:config_id>', methods=['DELETE'])
@login_required
def delete_configuration(config_id):
    """Konfigürasyon sil"""
    model = ConfigurationModel(mysql)
    existing = model.get_by_id(config_id)
    
    if not existing:
        return jsonify({'error': 'Konfigürasyon bulunamadı'}), 404
    
    model.delete(config_id)
    
    record_log('konfig_list', config_id, 'Konfig', existing['KonfigAdi'], '-', LogType.DELETE.value)
    
    return jsonify({'ok': True})
