"""
İster Onay API Controller'ı (Blueprint)
"""
from flask import Blueprint, request, jsonify, session
from app.utils.auth import login_required
from app.utils.database import mysql, get_dict_cursor
from app.utils.logging import record_log, LogType

ister_onay_api_bp = Blueprint('ister_onay_api', __name__, url_prefix='/api')


# ── İSTER ONAY ────────────────────────────────────────────────────────────────

@ister_onay_api_bp.route('/ister_onay/<int:node_id>', methods=['GET'])
@login_required
def get_ister_onay(node_id):
    """
    Belirli bir node'un onay durumunu döndürür.
    Query param: platform_id (zorunlu)
    """
    platform_id = request.args.get('platform_id')

    if not platform_id:
        return jsonify({'error': 'platform_id parametresi gerekli'}), 400

    cur = get_dict_cursor()
    cur.execute(
        "SELECT * FROM ister_onay WHERE NodeID=%s AND PlatformID=%s",
        (node_id, platform_id)
    )
    row = cur.fetchone()
    cur.close()

    # Kayıt yoksa varsayılan (onaysız) yapıyı döndür
    if not row:
        return jsonify({
            'NodeID': node_id,
            'PlatformID': int(platform_id),
            'OnayDurumu': 0
        })

    return jsonify(row)


@ister_onay_api_bp.route('/ister_onay', methods=['POST'])
@login_required
def save_ister_onay():
    """
    İster onay durumunu kaydeder veya günceller.
    Body: { NodeID, PlatformID, OnayDurumu }
      - OnayDurumu=1 → onaylı; onaylayan kullanıcı ve tarih de kaydedilir
      - OnayDurumu=0 → onay kaldırılır
    """
    data = request.json

    if not data:
        return jsonify({'error': 'İstek gövdesi boş'}), 400

    node_id     = data.get('NodeID')
    platform_id = data.get('PlatformID')

    if node_id is None or platform_id is None:
        return jsonify({'error': 'NodeID ve PlatformID zorunludur'}), 400

    cur = mysql.connection.cursor()

    if data.get('OnayDurumu'):
        cur.execute(
            """INSERT INTO ister_onay (NodeID, PlatformID, OnayDurumu, OnaylayanID, OnayTarihi)
               VALUES (?, ?, 1, ?, CURRENT_TIMESTAMP)
               ON CONFLICT(NodeID, PlatformID) DO UPDATE SET
                 OnayDurumu  = 1,
                 OnaylayanID = excluded.OnaylayanID,
                 OnayTarihi  = CURRENT_TIMESTAMP""",
            (node_id, platform_id, session['kullanici_id'])
        )
    else:
        cur.execute(
            """INSERT INTO ister_onay (NodeID, PlatformID, OnayDurumu)
               VALUES (?, ?, 0)
               ON CONFLICT(NodeID, PlatformID) DO UPDATE SET OnayDurumu = 0""",
            (node_id, platform_id)
        )

    mysql.connection.commit()
    cur.close()

    record_log(
        'ister_onay', node_id, 'İster Onayları',
        '-', str(data.get('OnayDurumu', 0)),
        LogType.UPDATE.value
    )

    return jsonify({'ok': True})