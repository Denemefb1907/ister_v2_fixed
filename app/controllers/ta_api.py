"""
TA Dokuman (Traceability Matrix) API Controller'ı (Blueprint)
"""
from flask import Blueprint, request, jsonify
from app.models.ta import TAModel
from app.utils.auth import login_required
from app.utils.database import mysql
from app.utils.logging import record_log, LogType

ta_api_bp = Blueprint('ta_api', __name__, url_prefix='/api')


@ta_api_bp.route('/platform/<int:platform_id>/ta', methods=['GET'])
@login_required
def get_ta_list(platform_id):
    """Platform'un TA dokümanlarını döndür"""
    model = TAModel(mysql)
    tas = model.get_all(platform_id)
    return jsonify(tas)


@ta_api_bp.route('/ta/<int:ta_id>', methods=['GET'])
@login_required
def get_ta_detail(ta_id):
    """TA dokümanı detaylarını döndür"""
    model = TAModel(mysql)
    ta = model.get_by_id(ta_id)
    
    if not ta:
        return jsonify({'error': 'TA bulunamadı'}), 404
    
    return jsonify(ta)


@ta_api_bp.route('/platform/<int:platform_id>/ta', methods=['POST'])
@login_required
def create_ta(platform_id):
    """Yeni TA dokümanı oluştur"""
    data = request.json
    
    model = TAModel(mysql)
    new_id = model.create(
        platform_id=platform_id,
        left_system=data.get('SolSistemAdi', ''),
        right_system=data.get('SagSistemAdi', '')
    )
    
    record_log(
        'ta_dokuman',
        platform_id,
        'Platform',
        '-',
        data.get('SolSistemAdi', ''),
        LogType.CREATE.value
    )
    
    tas = model.get_all(platform_id)
    new_ta = next((t for t in tas if t.get('TaID') == new_id or t.get('TaID') is None), {})
    
    return jsonify({
        'TaID': new_id,
        'SiraNo': new_ta.get('SiraNo', 0)
    }), 201


@ta_api_bp.route('/ta/<int:ta_id>', methods=['PUT'])
@login_required
def update_ta(ta_id):
    """TA dokümanını güncelle"""
    data = request.json
    
    # TA verilerini al
    data_list = data.get('veriler', []) if data else None
    
    model = TAModel(mysql)
    old_ta = model.get_by_id(ta_id)
    
    if not old_ta:
        return jsonify({'error': 'TA bulunamadı'}), 404
    
    model.update(
        ta_id=ta_id,
        left_system=data.get('SolSistemAdi', ''),
        right_system=data.get('SagSistemAdi', ''),
        data_list=data_list
    )
    
    record_log(
        'ta_dokuman',
        ta_id,
        'Platform',
        old_ta.get('SolSistemAdi', ''),
        data.get('SolSistemAdi', ''),
        LogType.UPDATE.value
    )
    
    return jsonify({'ok': True})


@ta_api_bp.route('/ta/<int:ta_id>/sgo_bagla', methods=['POST'])
@login_required
def link_sgo_to_ta(ta_id):
    """TA'ya SGÖ isterini bağla"""
    data = request.json
    
    if not data or 'NodeID' not in data:
        return jsonify({'error': 'NodeID gerekli'}), 400
    
    model = TAModel(mysql)
    
    try:
        model.link_sgo(ta_id, data['NodeID'])
        return jsonify({'ok': True}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@ta_api_bp.route('/ta/<int:ta_id>/sgo_bag_kaldir/<int:node_id>', methods=['DELETE'])
@login_required
def unlink_sgo_from_ta(ta_id, node_id):
    """TA'dan SGÖ isterinin bağlantısını kaldır"""
    model = TAModel(mysql)
    model.unlink_sgo(ta_id, node_id)
    
    return jsonify({'ok': True})


@ta_api_bp.route('/export/ta_dokuman/<int:ta_id>', methods=['GET'])
@login_required
def export_ta(ta_id):
    """TA dokümanını export et"""
    model = TAModel(mysql)
    ta = model.get_by_id(ta_id)
    
    if not ta:
        return jsonify({'error': 'TA bulunamadı'}), 404
    
    return jsonify(ta)
