import json
from typing import Optional

class CacheService:
    @staticmethod
    def calculate_jaccard_similarity(str1: str, str2: str) -> float:
        set1 = set(str1.lower().split())
        set2 = set(str2.lower().split())
        if not set1 or not set2:
            return 0.0
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)

cache_service = CacheService()
