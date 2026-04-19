"""
İster Node (Gereksinim) Modeli
"""
from app.models.base import BaseModel


class RequirementModel(BaseModel):

    def get_tree(self, platform_id, number_filter=''):
        cur = self.get_dict_cursor()
        q = """
        SELECT n.NodeID, n.PlatformID, n.SeviyeID, n.ParentID, n.HavuzNodeID,
               n.KonfigID, n.NodeNumarasi, n.IsterTipi, n.HavuzKodu,
               n.Icerik, n.TestYontemiID, n.DegistirildiMi,
               COALESCE(n.SiraNo, n.NodeID) AS SiraNo,
               s.SeviyeAdi, s.SeviyeNo, k.KonfigAdi, ty.YontemAdi AS TestYontemiAdi,
               (SELECT t2.TaID FROM ta_sgo_baglanti b2
                JOIN ta_dokuman t2 ON b2.TaID=t2.TaID
                WHERE b2.NodeID=n.NodeID LIMIT 1) AS ta_id
        FROM ister_node n
        JOIN seviye_tanim s ON n.SeviyeID=s.SeviyeID
        LEFT JOIN konfig_list k ON n.KonfigID=k.KonfigID
        LEFT JOIN test_yontemi ty ON n.TestYontemiID=ty.TestYontemiID
        WHERE n.PlatformID=%s
        """
        params = [platform_id]
        if number_filter:
            q += " AND n.NodeNumarasi LIKE %s"
            params.append(f'%{number_filter}%')
        q += " ORDER BY n.ParentID IS NULL DESC, n.SiraNo, n.NodeID"

        cur.execute(q, params)
        nodes = cur.fetchall()

        cur.execute("""
            SELECT ts.NodeID, ts.Sonuc, ta.AsamaAdi, ta.TestAsamaID
            FROM test_sonuc ts
            JOIN test_asama ta ON ts.TestAsamaID=ta.TestAsamaID
            WHERE ta.PlatformID=%s
        """, (platform_id,))
        test_results = cur.fetchall()
        cur.close()

        result_map = {}
        for r in test_results:
            nid = r['NodeID']
            if nid not in result_map:
                result_map[nid] = []
            result_map[nid].append(r)

        for node in nodes:
            node['test_sonuclari'] = result_map.get(node['NodeID'], [])

        return nodes

    def create(self, platform_id, level_id, content, **kwargs):
        cur = self.get_dict_cursor()

        ister_type = kwargs.get('IsterTipi', 'G')
        pool_code  = kwargs.get('HavuzKodu', '')

        # HATA #8 DÜZELTMESİ: COUNT yerine MAX kullan
        if not pool_code:
            cur.execute("SELECT HavuzMu FROM platform_list WHERE PlatformID=%s", (platform_id,))
            platform = cur.fetchone()
            if platform and platform.get('HavuzMu'):
                prefix = 'b' if ister_type == 'B' else 'g'
                cur.execute(
                    """SELECT COALESCE(MAX(CAST(SUBSTRING(HavuzKodu,2) AS UNSIGNED)),0) AS mx
                       FROM ister_node WHERE PlatformID=%s AND IsterTipi=%s
                       AND HavuzKodu REGEXP %s""",
                    (platform_id, ister_type, f'^{prefix}[0-9]+$')
                )
                row = cur.fetchone()
                mx = row['mx'] if row else 0
                pool_code = f"{prefix}{mx + 1}"

        parent_id = kwargs.get('ParentID')
        if parent_id:
            cur.execute(
                "SELECT COALESCE(MAX(SiraNo),0)+1 AS sira FROM ister_node WHERE ParentID=%s",
                (parent_id,)
            )
        else:
            cur.execute(
                "SELECT COALESCE(MAX(SiraNo),0)+1 AS sira FROM ister_node WHERE PlatformID=%s AND ParentID IS NULL",
                (platform_id,)
            )
        row = cur.fetchone()
        order_no = (row['sira'] if row else None) or 1

        cur2 = self.get_cursor()
        cur2.execute("""
            INSERT INTO ister_node
            (PlatformID, SeviyeID, ParentID, KonfigID, NodeNumarasi,
             IsterTipi, HavuzKodu, SiraNo, Icerik, TestYontemiID, IlgiliAsamaID, OlusturanID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            platform_id,
            level_id,
            parent_id,
            kwargs.get('KonfigID'),
            kwargs.get('NodeNumarasi', ''),
            ister_type,
            pool_code,
            order_no,
            content,
            kwargs.get('TestYontemiID'),
            kwargs.get('IlgiliAsamaID'),
            kwargs.get('OlusturanID')
        ))
        self.commit()
        new_id = cur2.lastrowid
        cur.close()
        cur2.close()
        return new_id

    def update(self, node_id, old_platform_id=None, **kwargs):
        cur  = self.get_dict_cursor()
        cur2 = self.get_cursor()

        # HATA #7 DÜZELTMESİ: Sadece havuz DIŞI platformlarda DegistirildiMi=1 yap
        is_pool = False
        if old_platform_id:
            cur.execute("SELECT HavuzMu FROM platform_list WHERE PlatformID=%s", (old_platform_id,))
            p = cur.fetchone()
            is_pool = bool(p and p.get('HavuzMu'))
        cur.close()

        updates = []
        values  = []
        for key, value in kwargs.items():
            if key not in ['NodeID']:
                updates.append(f"{key}=%s")
                values.append(value)

        if updates:
            if not is_pool:
                updates.append("DegistirildiMi=1")
            values.append(node_id)
            query = f"UPDATE ister_node SET {', '.join(updates)} WHERE NodeID=%s"
            cur2.execute(query, values)
            self.commit()
        cur2.close()

    def delete(self, node_id):
        cur = self.get_cursor()
        cur.execute("DELETE FROM ister_node WHERE NodeID=%s", (node_id,))
        self.commit()
        cur.close()

    def reorder(self, node_id, direction):
        cur = self.get_dict_cursor()
        cur.execute(
            "SELECT ParentID, PlatformID, SiraNo FROM ister_node WHERE NodeID=%s",
            (node_id,)
        )
        node = cur.fetchone()
        if not node:
            cur.close()
            return

        parent_id   = node['ParentID']
        platform_id = node['PlatformID']
        order_no    = node['SiraNo'] or 0

        if parent_id:
            cur.execute(
                "SELECT NodeID, SiraNo FROM ister_node WHERE ParentID=%s ORDER BY SiraNo, NodeID",
                (parent_id,)
            )
        else:
            cur.execute(
                "SELECT NodeID, SiraNo FROM ister_node WHERE PlatformID=%s AND ParentID IS NULL ORDER BY SiraNo, NodeID",
                (platform_id,)
            )
        siblings = cur.fetchall()

        idx = next((i for i, k in enumerate(siblings) if k['NodeID'] == node_id), -1)
        if idx == -1:
            cur.close()
            return

        target_idx = idx - 1 if direction == 'yukari' else idx + 1
        if target_idx < 0 or target_idx >= len(siblings):
            cur.close()
            return

        target = siblings[target_idx]
        cur2 = self.get_cursor()
        cur2.execute(
            "UPDATE ister_node SET SiraNo=%s WHERE NodeID=%s",
            (target['SiraNo'] or target_idx, node_id)
        )
        cur2.execute(
            "UPDATE ister_node SET SiraNo=%s WHERE NodeID=%s",
            (order_no or idx, target['NodeID'])
        )
        self.commit()
        cur.close()
        cur2.close()
