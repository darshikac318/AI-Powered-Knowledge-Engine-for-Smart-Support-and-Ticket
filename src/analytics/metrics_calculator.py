import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MetricsCalculator:
    def _init_(self):
        self.metrics_cache = {}
    
    def calculate_resolution_times(self, data):
        """Calculate average ticket resolution time and trends"""
        try:
            # Filter resolved tickets
            resolved_data = data[data['resolved_at'].notna()].copy()
            if len(resolved_data) == 0:
                return {
                    'avg_resolution_time': 0,
                    'median_resolution_time': 0,
                    'resolution_rate': 0,
                    'weekly_trends': {}
                }
            
            # Convert to datetime
            resolved_data['created_at'] = pd.to_datetime(resolved_data['created_at'])
            resolved_data['resolved_at'] = pd.to_datetime(resolved_data['resolved_at'])
            
            # Calculate resolution time in hours
            resolved_data['resolution_time_hours'] = (
                resolved_data['resolved_at'] - resolved_data['created_at']
            ).dt.total_seconds() / 3600
            
            # Basic metrics
            avg_resolution_time = resolved_data['resolution_time_hours'].mean()
            median_resolution_time = resolved_data['resolution_time_hours'].median()
            
            # Resolution rate
            total_tickets = len(data)
            resolved_tickets = len(resolved_data)
            resolution_rate = (resolved_tickets / total_tickets) * 100
            
            # Weekly trends
            resolved_data['week'] = resolved_data['created_at'].dt.strftime('%Y-%U')
            weekly_avg = resolved_data.groupby('week')['resolution_time_hours'].mean()
            
            # Priority-based analysis
            priority_analysis = {}
            if 'priority' in resolved_data.columns:
                priority_avg = resolved_data.groupby('priority')['resolution_time_hours'].mean()
                priority_analysis = priority_avg.to_dict()
            
            return {
                'avg_resolution_time': float(avg_resolution_time),
                'median_resolution_time': float(median_resolution_time),
                'resolution_rate': float(resolution_rate),
                'resolved_tickets': resolved_tickets,
                'total_tickets': total_tickets,
                'weekly_trends': weekly_avg.to_dict(),
                'priority_analysis': priority_analysis
            }
            
        except Exception as e:
            print(f"Error calculating resolution times: {e}")
            return {
                'avg_resolution_time': 0,
                'median_resolution_time': 0,
                'resolution_rate': 0,
                'weekly_trends': {},
                'priority_analysis': {}
            }
    
    def calculate_agent_scores(self, data):
        """Calculate agent performance scores"""
        try:
            if 'agent_id' not in data.columns:
                return []
                
            resolved_data = data[data['resolved_at'].notna()].copy()
            if len(resolved_data) == 0:
                return []
            
            # Ensure datetime conversion
            resolved_data['created_at'] = pd.to_datetime(resolved_data['created_at'])
            resolved_data['resolved_at'] = pd.to_datetime(resolved_data['resolved_at'])
            
            # Calculate resolution time
            resolved_data['resolution_time_hours'] = (
                resolved_data['resolved_at'] - resolved_data['created_at']
            ).dt.total_seconds() / 3600
            
            # Group by agent
            agent_groups = resolved_data.groupby('agent_id')
            agent_metrics = []
            
            for agent_id, group in agent_groups:
                metrics = {
                    'agent_id': agent_id,
                    'tickets_resolved': len(group),
                    'avg_resolution_time': group['resolution_time_hours'].mean(),
                    'median_resolution_time': group['resolution_time_hours'].median()
                }
                
                # Add satisfaction if available
                if 'customer_satisfaction' in group.columns:
                    metrics['avg_satisfaction'] = group['customer_satisfaction'].mean()
                
                # Add KB usage if available
                if 'kb_article_used' in group.columns:
                    kb_used = group['kb_article_used'].sum() if group['kb_article_used'].dtype == bool else len(group[group['kb_article_used'] == True])
                    metrics['kb_usage_rate'] = (kb_used / len(group)) * 100
                
                agent_metrics.append(metrics)
            
            # Calculate performance scores
            if agent_metrics:
                df_metrics = pd.DataFrame(agent_metrics)
                
                # Normalize metrics for scoring (0-100 scale)
                max_tickets = df_metrics['tickets_resolved'].max()
                min_time = df_metrics['avg_resolution_time'].min()
                max_time = df_metrics['avg_resolution_time'].max()
                time_range = max_time - min_time if max_time != min_time else 1
                
                for i, metrics in enumerate(agent_metrics):
                    # Volume score (30% weight)
                    volume_score = (metrics['tickets_resolved'] / max_tickets) * 30
                    
                    # Efficiency score (40% weight) - lower time is better
                    efficiency_score = (1 - ((metrics['avg_resolution_time'] - min_time) / time_range)) * 40
                    
                    # Satisfaction score (30% weight) if available
                    if 'avg_satisfaction' in metrics:
                        satisfaction_score = (metrics['avg_satisfaction'] / 5) * 30
                    else:
                        satisfaction_score = 15  # Default middle score
                    
                    metrics['overall_score'] = volume_score + efficiency_score + satisfaction_score
                    metrics['volume_score'] = volume_score
                    metrics['efficiency_score'] = efficiency_score
                    metrics['satisfaction_score'] = satisfaction_score
            
            return agent_metrics
            
        except Exception as e:
            print(f"Error calculating agent scores: {e}")
            return []
    
    def calculate_satisfaction_trends(self, data):
        """Calculate customer satisfaction trends"""
        try:
            if 'customer_satisfaction' not in data.columns:
                return {
                    'avg_satisfaction': 0,
                    'satisfaction_distribution': {},
                    'daily_trends': {},
                    'weekly_trends': {},
                    'agent_satisfaction': {}
                }
            
            valid_data = data[data['customer_satisfaction'].notna()].copy()
            if len(valid_data) == 0:
                return {
                    'avg_satisfaction': 0,
                    'satisfaction_distribution': {},
                    'daily_trends': {},
                    'weekly_trends': {},
                    'agent_satisfaction': {}
                }
            
            # Convert to datetime
            valid_data['created_at'] = pd.to_datetime(valid_data['created_at'])
            
            # Basic statistics
            avg_satisfaction = valid_data['customer_satisfaction'].mean()
            
            # Satisfaction distribution
            satisfaction_distribution = valid_data['customer_satisfaction'].value_counts().sort_index().to_dict()
            
            # Daily trends
            valid_data['date'] = valid_data['created_at'].dt.date
            daily_trends = valid_data.groupby('date')['customer_satisfaction'].mean().to_dict()
            
            # Weekly trends
            valid_data['week'] = valid_data['created_at'].dt.strftime('%Y-%U')
            weekly_trends = valid_data.groupby('week')['customer_satisfaction'].mean().to_dict()
            
            # Agent satisfaction
            agent_satisfaction = {}
            if 'agent_id' in valid_data.columns:
                agent_satisfaction = valid_data.groupby('agent_id')['customer_satisfaction'].mean().to_dict()
            
            return {
                'avg_satisfaction': float(avg_satisfaction),
                'satisfaction_distribution': satisfaction_distribution,
                'daily_trends': {str(k): float(v) for k, v in daily_trends.items()},
                'weekly_trends': weekly_trends,
                'agent_satisfaction': agent_satisfaction
            }
            
        except Exception as e:
            print(f"Error calculating satisfaction trends: {e}")
            return {
                'avg_satisfaction': 0,
                'satisfaction_distribution': {},
                'daily_trends': {},
                'weekly_trends': {},
                'agent_satisfaction': {}
            }
    
    def calculate_kb_usage(self, data):
        """Calculate knowledge base usage statistics"""
        try:
            if 'kb_article_used' not in data.columns:
                return {
                    'usage_rate': 0,
                    'total_uses': 0,
                    'effectiveness': 0,
                    'trends': {}
                }
            
            total_tickets = len(data)
            
            # Calculate usage
            if data['kb_article_used'].dtype == bool:
                kb_used = data['kb_article_used'].sum()
            else:
                kb_used = len(data[data['kb_article_used'] == True])
            
            usage_rate = (kb_used / total_tickets) * 100 if total_tickets > 0 else 0
            
            # Calculate effectiveness (satisfaction when KB used vs not used)
            effectiveness = 0
            if 'customer_satisfaction' in data.columns:
                kb_satisfaction = data[data['kb_article_used'] == True]['customer_satisfaction'].mean()
                no_kb_satisfaction = data[data['kb_article_used'] == False]['customer_satisfaction'].mean()
                
                if not pd.isna(kb_satisfaction) and not pd.isna(no_kb_satisfaction):
                    effectiveness = kb_satisfaction - no_kb_satisfaction
            
            # Usage trends over time
            trends = {}
            if 'created_at' in data.columns:
                data_copy = data.copy()
                data_copy['created_at'] = pd.to_datetime(data_copy['created_at'])
                data_copy['week'] = data_copy['created_at'].dt.strftime('%Y-%U')
                
                weekly_usage = data_copy.groupby('week')['kb_article_used'].apply(
                    lambda x: (x.sum() / len(x)) * 100 if len(x) > 0 else 0
                )
                trends = weekly_usage.to_dict()
            
            return {
                'usage_rate': float(usage_rate),
                'total_uses': int(kb_used),
                'effectiveness': float(effectiveness),
                'trends': trends
            }
            
        except Exception as e:
            print(f"Error calculating KB usage: {e}")
            return {
                'usage_rate': 0,
                'total_uses': 0,
                'effectiveness': 0,
                'trends': {}
            }
    
    def calculate_all_metrics(self, data):
        """Calculate all performance metrics"""
        resolution_metrics = self.calculate_resolution_times(data)
        agent_metrics = self.calculate_agent_scores(data)
        satisfaction_metrics = self.calculate_satisfaction_trends(data)
        kb_metrics = self.calculate_kb_usage(data)
        
        # Overall summary metrics
        summary_metrics = {
            'total_tickets': len(data),
            'resolved_tickets': resolution_metrics['resolved_tickets'],
            'resolution_rate': resolution_metrics['resolution_rate'],
            'avg_resolution_time': resolution_metrics['avg_resolution_time'],
            'avg_satisfaction': satisfaction_metrics['avg_satisfaction'],
            'kb_usage_rate': kb_metrics['usage_rate']
        }
        
        return {
            'resolution_times': resolution_metrics,
            'agent_scores': agent_metrics,
            'satisfaction_trends': satisfaction_metrics,
            'kb_usage': kb_metrics,
            'summary_metrics': summary_metrics
        }
