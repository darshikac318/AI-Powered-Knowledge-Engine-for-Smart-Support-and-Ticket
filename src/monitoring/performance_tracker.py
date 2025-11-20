import time
from datetime import datetime
from typing import Dict, List
import json
import os

class PerformanceTracker:
    def __init__(self, log_path="data/performance_logs.json"):
        self.log_path = log_path
        self.metrics = []
    
    def track_search(self, query: str, response_time: float, results_count: int):
        metric = {
            'timestamp': datetime.now().isoformat(),
            'operation': 'search',
            'query': query,
            'response_time': response_time,
            'results_count': results_count
        }
        self.metrics.append(metric)
        self._save_metrics()
    
    def track_ticket_operation(self, operation: str, ticket_id: str, duration: float):
        metric = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'ticket_id': ticket_id,
            'duration': duration
        }
        self.metrics.append(metric)
        self._save_metrics()
    
    def _save_metrics(self):
        try:
            existing_data = []
            if os.path.exists(self.log_path):
                with open(self.log_path, 'r') as f:
                    existing_data = json.load(f)
            
            existing_data.extend(self.metrics)
            
            with open(self.log_path, 'w') as f:
                json.dump(existing_data[-1000:], f, indent=2)
            
            self.metrics = []
        except Exception as e:
            print(f"Error saving metrics: {e}")
    
    def get_average_response_time(self) -> float:
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as f:
                data = json.load(f)
            
            search_times = [m['response_time'] for m in data if m['operation'] == 'search']
            
            if search_times:
                return sum(search_times) / len(search_times)
        
        return 0.0
    
    def get_performance_summary(self) -> Dict:
        if not os.path.exists(self.log_path):
            return {
                'total_operations': 0,
                'avg_response_time': 0,
                'total_searches': 0
            }
        
        with open(self.log_path, 'r') as f:
            data = json.load(f)
        
        searches = [m for m in data if m['operation'] == 'search']
        
        return {
            'total_operations': len(data),
            'avg_response_time': sum(m['response_time'] for m in searches) / len(searches) if searches else 0,
            'total_searches': len(searches),
            'recent_operations': data[-10:]
        }