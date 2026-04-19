"""
Pano (Dashboard) Modeli - Raporlar ve İstatistikler
"""
from app.models.base import BaseModel


class DashboardModel(BaseModel):
    """Pano Veri Yönetimi Modeli"""
    
    def get_summary(self):
        """
        Tüm platformlar için özet raporunu döndür
        
        Returns:
            dict: Platform özet bilgileri
        """
        cur = self.get_dict_cursor()
        
        cur.execute("SELECT * FROM platform_list WHERE HavuzMu=0 ORDER BY PlatformAdi")
        platforms = cur.fetchall()
        
        summary = []
        
        for platform in platforms:
            pid = platform['PlatformID']
            
            # TGD sayısı (Seviye 1)
            cur.execute("""
                SELECT COUNT(DISTINCT n.NodeID) AS toplam
                FROM ister_node n 
                JOIN seviye_tanim s ON n.SeviyeID=s.SeviyeID
                WHERE n.PlatformID=%s AND s.SeviyeNo=1
            """, (pid,))
            tgd_count = (cur.fetchone() or {}).get('toplam', 0)
            
            # SGÖ sayısı (Seviye 2)
            cur.execute("""
                SELECT COUNT(DISTINCT n.NodeID) AS toplam
                FROM ister_node n 
                JOIN seviye_tanim s ON n.SeviyeID=s.SeviyeID
                WHERE n.PlatformID=%s AND s.SeviyeNo=2
            """, (pid,))
            sgo_count = (cur.fetchone() or {}).get('toplam', 0)
            
            # Test metrikleri
            cur.execute("""
                SELECT ts.Sonuc, COUNT(*) AS sayi 
                FROM test_sonuc ts
                JOIN test_asama ta ON ts.TestAsamaID=ta.TestAsamaID
                WHERE ta.PlatformID=%s 
                GROUP BY ts.Sonuc
            """, (pid,))
            
            test_summary = {r['Sonuc']: r['sayi'] for r in cur.fetchall()}
            successful = test_summary.get('Basarili', 0)
            failed = test_summary.get('Hatali', 0)
            total_tests = successful + failed
            
            success_rate = (successful / total_tests * 100) if total_tests > 0 else 0
            
            summary.append({
                'PlatformID': pid,
                'PlatformAdi': platform['PlatformAdi'],
                'TGDSayi': tgd_count,
                'SGOSayi': sgo_count,
                'ToplamTest': total_tests,
                'BasariliTest': successful,
                'HataliTest': failed,
                'BasariOrani': round(success_rate, 1)
            })
        
        cur.close()
        return summary
    
    def get_platform_traceability(self, platform_id):
        """
        Platform için traceability metrikleri hesapla
        
        Args:
            platform_id: Platform ID'si
            
        Returns:
            list: Test metrikleri ile birlikte ister listesi
        """
        cur = self.get_dict_cursor()
        
        # Tüm isterleri getir
        cur.execute("""
            SELECT n.NodeID, n.Icerik, n.ParentID, s.SeviyeAdi, s.SeviyeNo, 
                   k.KonfigAdi, ty.YontemAdi AS TestYontemiAdi
            FROM ister_node n
            JOIN seviye_tanim s ON n.SeviyeID=s.SeviyeID
            LEFT JOIN konfig_list k ON n.KonfigID=k.KonfigID
            LEFT JOIN test_yontemi ty ON n.TestYontemiID=ty.TestYontemiID
            WHERE n.PlatformID=%s 
            ORDER BY s.SeviyeNo, n.NodeID
        """, (platform_id,))
        
        nodes = cur.fetchall()
        
        # Test sonuçlarını getir
        cur.execute("""
            SELECT ts.NodeID, ts.Sonuc, ta.AsamaAdi
            FROM test_sonuc ts 
            JOIN test_asama ta ON ts.TestAsamaID=ta.TestAsamaID
            WHERE ta.PlatformID=%s
        """, (platform_id,))
        
        test_results = cur.fetchall()
        result_map = {}
        for result in test_results:
            if result['NodeID'] not in result_map:
                result_map[result['NodeID']] = []
            result_map[result['NodeID']].append(result)
        
        # Her node için metrik hesapla
        node_map = {n['NodeID']: n for n in nodes}
        
        def calculate_metrics(node_id):
            """Recursively calculate metrics"""
            children = [n for n in nodes if n['ParentID'] == node_id]
            
            if not children:  # Leaf node: en alt seviye
                results_list = result_map.get(node_id, [])
                if not results_list:
                    return {
                        'toplam': 0,
                        'basarili': 0,
                        'hatali': 0,
                        'durum': 'test_yok'
                    }
                
                successful = sum(1 for r in results_list if r['Sonuc'] == 'Basarili')
                failed = sum(1 for r in results_list if r['Sonuc'] == 'Hatali')
                
                durumu = 'basarili' if failed == 0 and successful > 0 else \
                        'hatali' if failed > 0 else 'test_yok'
                
                return {
                    'toplam': len(results_list),
                    'basarili': successful,
                    'hatali': failed,
                    'durum': durumu
                }
            else:
                # Parent node: çocukların metrikleri topla
                child_metrics = [calculate_metrics(c['NodeID']) for c in children]
                
                toplam = sum(m['toplam'] for m in child_metrics)
                basarili = sum(m['basarili'] for m in child_metrics)
                hatali = sum(m['hatali'] for m in child_metrics)
                
                durumu = 'test_yok' if toplam == 0 else \
                        'basarili' if hatali == 0 else \
                        'hatali' if basarili == 0 else 'kismi'
                
                return {
                    'toplam': toplam,
                    'basarili': basarili,
                    'hatali': hatali,
                    'durum': durumu
                }
        
        # Tüm nodes için metrik ekle
        for node in nodes:
            node['metrik'] = calculate_metrics(node['NodeID'])
            node['test_sonuclari'] = result_map.get(node['NodeID'], [])
        
        cur.close()
        return nodes
