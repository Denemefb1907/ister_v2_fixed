"""
Karşılaştırma (Comparison) API Controller'ı (Blueprint)
"""
from flask import Blueprint, request, jsonify
import MySQLdb.cursors
from app.models.platform import PlatformModel
from app.models.requirement import RequirementModel
from app.utils.auth import login_required
from app.utils.database import mysql
from app.utils.helpers import calculate_similarity_ratio

comparison_api_bp = Blueprint('comparison_api', __name__, url_prefix='/api')


@comparison_api_bp.route('/karsilastir/dis_liste', methods=['POST'])
@login_required
def compare_to_external_list():
    """Dış liste ile platform isterlerini karşılaştır"""
    data = request.json

    platform_id = data.get('platform_id')
    external_list = data.get('dis_liste', [])
    threshold = data.get('esik', 80)
    level_no = data.get('seviye_no', 2)

    if not platform_id:
        return jsonify({'error': 'platform_id gerekli'}), 400

    req_model = RequirementModel(mysql)

    # HATA #1 DÜZELTMESİ: fetchall eksikti, our_requirements tanımsızdı
    cur = req_model.get_dict_cursor()
    cur.execute("""
        SELECT n.NodeID, n.Icerik, s.SeviyeAdi, s.SeviyeNo
        FROM ister_node n
        JOIN seviye_tanim s ON n.SeviyeID=s.SeviyeID
        WHERE n.PlatformID=%s AND s.SeviyeNo=%s
    """, (platform_id, level_no))
    our_requirements = cur.fetchall()
    cur.close()

    results = []

    for ext_item in external_list:
        ext_text = str(ext_item.get('metin') or '')
        best_match = None
        best_ratio = -1

        for our_req in our_requirements:
            ratio = calculate_similarity_ratio(ext_text, our_req['Icerik'])
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = our_req

        if best_ratio == 100:
            status = 'ayni'
        elif best_ratio >= threshold:
            status = 'benzer'
        else:
            status = 'yeni'

        results.append({
            'dis_metin': ext_text,
            'bizim_id': best_match['NodeID'] if best_match else None,
            'bizim_metin': best_match['Icerik'] if best_match else None,
            'benzerlik': best_ratio,
            'durum': status
        })

    extras = []
    for our_req in our_requirements:
        ratios = [calculate_similarity_ratio(our_req['Icerik'], str(e.get('metin') or '')) for e in external_list]
        best_ratio = max(ratios, default=0)

        if best_ratio < threshold:
            extras.append({
                'bizim_id': our_req['NodeID'],
                'bizim_metin': our_req['Icerik'],
                'durum': 'fazla'
            })

    return jsonify({'sonuclar': results, 'fazlalar': extras})


@comparison_api_bp.route('/karsilastir/havuz', methods=['POST'])
@login_required
def compare_to_pool():
    """Platform isterlerini havuz ile karşılaştır"""
    data = request.json

    platform_id = data.get('platform_id')
    threshold = data.get('esik', 80)
    level_no = data.get('seviye_no', 2)

    if not platform_id:
        return jsonify({'error': 'platform_id gerekli'}), 400

    platform_model = PlatformModel(mysql)
    req_model = RequirementModel(mysql)

    pool = platform_model.get_pool_platform()
    if not pool:
        return jsonify({'error': 'Havuz platformu bulunamadı'}), 404

    pool_id = pool['PlatformID']

    platform_reqs = [r for r in req_model.get_tree(platform_id) if r.get('SeviyeNo') == level_no]
    pool_reqs     = [r for r in req_model.get_tree(pool_id)     if r.get('SeviyeNo') == level_no]

    results = []
    for p_req in platform_reqs:
        best_match = None
        best_ratio = -1
        for pool_req in pool_reqs:
            ratio = calculate_similarity_ratio(p_req['Icerik'], pool_req['Icerik'])
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = pool_req

        status = 'ayni' if best_ratio == 100 else ('benzer' if best_ratio >= threshold else 'farkli')
        results.append({
            'platform_node_id': p_req['NodeID'],
            'platform_metin':   p_req['Icerik'],
            'havuz_id':         best_match['NodeID'] if best_match else None,
            'havuz_metin':      best_match['Icerik'] if best_match else None,
            'benzerlik':        best_ratio,
            'durum':            status
        })

    extras = []
    for pool_req in pool_reqs:
        ratios = [calculate_similarity_ratio(pool_req['Icerik'], p['Icerik']) for p in platform_reqs]
        if max(ratios, default=0) < threshold:
            extras.append({'havuz_id': pool_req['NodeID'], 'havuz_metin': pool_req['Icerik']})

    return jsonify({'sonuclar': results, 'havuzda_fazla': extras})


@comparison_api_bp.route('/ister_node/by_kod', methods=['GET'])
@login_required
def get_requirement_by_code():
    """Havuz koduna göre tüm platformlardaki isterleri döndür"""
    code = request.args.get('kod')
    if not code:
        return jsonify({'error': 'kod gerekli'}), 400

    # HATA #2 DÜZELTMESİ: cursor().__init__() None döndürüyordu + data tanımsızdı
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT n.*, p.PlatformAdi, p.HavuzMu, s.SeviyeAdi, k.KonfigAdi
        FROM ister_node n
        JOIN platform_list p ON n.PlatformID=p.PlatformID
        JOIN seviye_tanim s ON n.SeviyeID=s.SeviyeID
        LEFT JOIN konfig_list k ON n.KonfigID=k.KonfigID
        WHERE n.HavuzKodu=%s
        ORDER BY p.HavuzMu DESC, p.PlatformAdi
    """, (code,))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)


@comparison_api_bp.route('/havuz_kodu/karsilastir', methods=['GET'])
@login_required
def compare_pool_code():
    """Bir havuz kodundaki isterin hangi platformlarda nasıl göründüğünü döndür"""
    code = request.args.get('kod')
    if not code:
        return jsonify({'error': 'kod gerekli'}), 400

    # HATA #3 DÜZELTMESİ: results = cur.fetchall() eksikti
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT n.*, p.PlatformAdi, s.SeviyeAdi
        FROM ister_node n
        JOIN platform_list p ON n.PlatformID=p.PlatformID
        JOIN seviye_tanim s ON n.SeviyeID=s.SeviyeID
        WHERE n.HavuzKodu=%s
    """, (code,))
    results = cur.fetchall()
    cur.close()
    return jsonify(results)
