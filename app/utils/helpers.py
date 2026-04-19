"""
Yardımcı Fonksiyonlar
"""


def levenshtein_distance(s1, s2):
    """
    Levenshtein mesafesini hesapla (iki string arasındaki fark)
    """
    if not s1:
        return len(s2 or '')
    if not s2:
        return len(s1 or '')
    
    s1 = str(s1).lower()
    s2 = str(s2).lower()
    
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    
    prev = list(range(len(s2) + 1))
    
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(
                prev[j] + (0 if c1 == c2 else 1),
                curr[j] + 1,
                prev[j + 1] + 1
            ))
        prev = curr
    
    return prev[-1]


def calculate_similarity_ratio(s1, s2):
    """
    İki string arasındaki benzerlik oranını yüzde olarak hesapla
    
    Returns:
        float: 0-100 arasında benzerlik yüzdesi
    """
    if not s1 and not s2:
        return 100.0
    if not s1 or not s2:
        return 0.0
    
    max_len = max(len(str(s1)), len(str(s2)))
    if max_len == 0:
        return 100.0
    
    distance = levenshtein_distance(s1, s2)
    ratio = (1 - distance / max_len) * 100
    
    return round(ratio, 1)
