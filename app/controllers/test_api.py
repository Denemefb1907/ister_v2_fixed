"""
Test API Controller'ı (Blueprint)
"""
from flask import Blueprint, request, jsonify, session
from app.models.test import TestModel
from app.utils.auth import login_required
from app.utils.database import mysql
from app.utils.logging import record_log, LogType

test_api_bp = Blueprint('test_api', __name__, url_prefix='/api')


# ── TEST AŞAMALARI ────────────────────────────────────────────────────────

@test_api_bp.route('/platform/<int:platform_id>/test_asama', methods=['GET'])
@login_required
def get_test_phases(platform_id):
    """Platform'un test aşamalarını döndür"""
    model = TestModel(mysql)
    phases = model.get_phases(platform_id)
    return jsonify(phases)


@test_api_bp.route('/platform/<int:platform_id>/test_asama', methods=['POST'])
@login_required
def create_test_phase(platform_id):
    """Yeni test aşaması oluştur"""
    data = request.json
    
    if not data or 'AsamaAdi' not in data:
        return jsonify({'error': 'Aşama adı gerekli'}), 400
    
    model = TestModel(mysql)
    new_id = model.create_phase(platform_id, data['AsamaAdi'])
    
    # Aşama bilgisini getir
    phases = model.get_phases(platform_id)
    new_phase = next((p for p in phases if p['TestAsamaID'] == new_id), {})
    
    return jsonify({
        'TestAsamaID': new_id,
        'AsamaNo': new_phase.get('AsamaNo', 0),
        'AsamaAdi': data['AsamaAdi']
    }), 201


@test_api_bp.route('/test_asama/<int:phase_id>', methods=['PUT'])
@login_required
def update_test_phase(phase_id):
    """Test aşamasını güncelle"""
    data = request.json
    
    if not data or 'AsamaAdi' not in data:
        return jsonify({'error': 'Aşama adı gerekli'}), 400
    
    model = TestModel(mysql)
    model.update_phase(phase_id, data['AsamaAdi'])
    
    return jsonify({'ok': True})


@test_api_bp.route('/test_asama/<int:phase_id>', methods=['DELETE'])
@login_required
def delete_test_phase(phase_id):
    """Test aşamasını sil"""
    model = TestModel(mysql)
    model.delete_phase(phase_id)
    
    return jsonify({'ok': True})


# ── TEST SONUÇLARI ────────────────────────────────────────────────────────

@test_api_bp.route('/test_sonuc', methods=['GET'])
@login_required
def get_test_results():
    """Test sonuçlarını döndür"""
    platform_id = request.args.get('platform_id')
    phase_id = request.args.get('asama_id')
    
    if not platform_id:
        return jsonify({'error': 'platform_id gerekli'}), 400
    
    model = TestModel(mysql)
    results = model.get_results(platform_id, phase_id)
    
    return jsonify(results)


@test_api_bp.route('/test_sonuc/girilmemis', methods=['GET'])
@login_required
def get_untested_nodes():
    """Test sonucu girilmemiş isterleri döndür"""
    platform_id = request.args.get('platform_id')
    phase_id = request.args.get('asama_id')
    
    if not platform_id:
        return jsonify({'error': 'platform_id gerekli'}), 400
    
    model = TestModel(mysql)
    nodes = model.get_untested_nodes(platform_id, phase_id)
    
    return jsonify(nodes)


@test_api_bp.route('/test_sonuc', methods=['POST'])
@login_required
def save_test_result():
    """Test sonucunu kaydet"""
    data = request.json
    
    required_fields = ['NodeID', 'TestAsamaID', 'Sonuc']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} gerekli'}), 400
    
    model = TestModel(mysql)
    
    model.save_result(
        node_id=data['NodeID'],
        phase_id=data['TestAsamaID'],
        result=data['Sonuc'],
        explanation=data.get('Aciklama', ''),
        user_id=session.get('kullanici_id')
    )
    
    record_log(
        'test_sonuc',
        data['NodeID'],
        'Sonuc',
        '',
        data['Sonuc'],
        LogType.CREATE.value
    )
    
    return jsonify({'ok': True}), 201


# ── TEST YÖNTEMLERİ ───────────────────────────────────────────────────────────

@test_api_bp.route('/test_yontemi', methods=['GET'])
@login_required
def get_test_methods():
    """Test yöntemleri listesini döndür"""
    from app.utils.database import get_dict_cursor
    
    cur = get_dict_cursor()
    cur.execute("SELECT * FROM test_yontemi ORDER BY YontemAdi")
    methods = cur.fetchall()
    cur.close()
    
    return jsonify(methods)
