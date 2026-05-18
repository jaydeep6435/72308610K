import heapq
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class NotificationPriorityEngine:
    """
    Heap-based Ranking Engine for Notifications.
    Time Complexity: O(n log k) where k is top-k limit.
    Priority Order: Placement > Result > Event
    """
    
    PRIORITY_MAP = {
        "Placement": 3,
        "Result": 2,
        "Event": 1
    }
    
    @classmethod
    def _get_priority_score(cls, type_str: str) -> int:
        return cls.PRIORITY_MAP.get(type_str, 0)
        
    @classmethod
    def get_top_notifications(cls, notifications: list, top_k: int = 10) -> list:
        Log("backend", "info", "service", f"Ranking notifications. Top K = {top_k}")
        
        if not notifications:
            return []
            
        heap = []
        
        for n in notifications:
            # Type Priority Score
            priority_score = cls._get_priority_score(n.get("type", ""))
            
            # Timestamp parsing
            timestamp_str = n.get("timestamp", "")
            try:
                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                ts = dt.timestamp()
            except (ValueError, TypeError):
                ts = 0.0
                
            # Maintain top-k elements using min-heap.
            # Smallest element (lowest priority, oldest timestamp) sits at heap[0]
            heap_item = (priority_score, ts, id(n), n)
            
            if len(heap) < top_k:
                heapq.heappush(heap, heap_item)
            else:
                heapq.heappushpop(heap, heap_item)
                
        # Extract from heap and sort descending (highest priority first, then newest timestamp)
        result = [item[3] for item in sorted(heap, key=lambda x: (x[0], x[1]), reverse=True)]
        
        Log("backend", "debug", "service", f"Notification ranking completed. Yielded {len(result)} items.")
        return result
