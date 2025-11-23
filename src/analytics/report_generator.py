import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class ReportGenerator:
    def _init_(self):
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_daily_summary(self, data, report_date=None):
        """Generate daily summary report"""
        if report_date is None:
            report_date = datetime.now()
        
        # Filter data for the specific day
        daily_data = self._filter_data_by_period(data, report_date, 'daily')
        
        # Calculate metrics
        from .metrics_calculator import MetricsCalculator
        calculator = MetricsCalculator()
        metrics = calculator.calculate_all_metrics(daily_data)
        
        # Generate report structure
        report = {
            'report_type': 'daily_summary',
            'report_date': report_date.strftime('%Y-%m-%d'),
            'generated_at': datetime.now().isoformat(),
            'period_metrics': {
                'total_tickets': len(daily_data),
                'resolved_tickets': metrics['resolution_times']['resolved_tickets'],
                'new_tickets': len(daily_data[daily_data['created_at'].notna()]),
                'resolution_rate': metrics['resolution_times']['resolution_rate']
            },
            'performance_metrics': {
                'avg_resolution_time': metrics['resolution_times']['avg_resolution_time'],
                'avg_satisfaction': metrics['satisfaction_trends']['avg_satisfaction'],
                'kb_usage_rate': metrics['kb_usage']['usage_rate']
            },
            'key_insights': self._generate_daily_insights(metrics, daily_data),
            'top_performers': self._get_top_performers(metrics['agent_scores'], 3),
            'recommendations': self._generate_daily_recommendations(metrics)
        }
        
        # Save report
        filename = f"daily_report_{report_date.strftime('%Y%m%d')}.json"
        self._save_report(report, filename)
        
        return report
    
    def generate_weekly_report(self, data, start_date=None):
        """Generate weekly analytics report"""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=7)
        
        # Filter data for the week
        weekly_data = self._filter_data_by_period(data, start_date, 'weekly')
        
        # Calculate metrics
        from .metrics_calculator import MetricsCalculator
        calculator = MetricsCalculator()
        metrics = calculator.calculate_all_metrics(weekly_data)
        
        # Generate trends analysis
        trends = self._analyze_weekly_trends(data, start_date)
        
        report = {
            'report_type': 'weekly_analytics',
            'report_period': {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': (start_date + timedelta(days=6)).strftime('%Y-%m-%d')
            },
            'generated_at': datetime.now().isoformat(),
            'summary_metrics': metrics['summary_metrics'],
            'detailed_analysis': {
                'resolution_analysis': metrics['resolution_times'],
                'satisfaction_analysis': metrics['satisfaction_trends'],
                'kb_usage_analysis': metrics['kb_usage']
            },
            'agent_performance': {
                'top_performers': self._get_top_performers(metrics['agent_scores'], 5),
                'performance_breakdown': metrics['agent_scores']
            },
            'trends_comparison': trends,
            'weekly_insights': self._generate_weekly_insights(metrics, trends),
            'action_items': self._generate_weekly_recommendations(metrics, trends)
        }
        
        # Save report
        filename = f"weekly_report_{start_date.strftime('%Y%m%d')}.json"
        self._save_report(report, filename)
        
        return report
    
    def generate_monthly_report(self, data, month_date=None):
        """Generate monthly performance report"""
        if month_date is None:
            month_date = datetime.now().replace(day=1)
        
        # Filter data for the month
        monthly_data = self._filter_data_by_period(data, month_date, 'monthly')
        
        # Calculate metrics
        from .metrics_calculator import MetricsCalculator
        calculator = MetricsCalculator()
        metrics = calculator.calculate_all_metrics(monthly_data)
        
        # Generate comprehensive analysis
        monthly_trends = self._analyze_monthly_trends(data, month_date)
        
        report = {
            'report_type': 'monthly_performance',
            'report_period': month_date.strftime('%Y-%m'),
            'generated_at': datetime.now().isoformat(),
            'executive_summary': self._generate_executive_summary(metrics, monthly_data),
            'performance_metrics': metrics['summary_metrics'],
            'departmental_analysis': {
                'resolution_performance': self._analyze_resolution_performance(metrics['resolution_times']),
                'customer_satisfaction': self._analyze_satisfaction_performance(metrics['satisfaction_trends']),
                'knowledge_base_impact': self._analyze_kb_impact(metrics['kb_usage'])
            },
            'agent_performance_review': {
                'ranking': self._rank_agents(metrics['agent_scores']),
                'improvement_areas': self._identify_improvement_areas(metrics['agent_scores']),
                'recognition_list': self._get_top_performers(metrics['agent_scores'], 10)
            },
            'strategic_insights': self._generate_strategic_insights(metrics, monthly_trends),
            'quarterly_planning': self._generate_quarterly_recommendations(metrics, monthly_trends)
        }
        
        # Save report
        filename = f"monthly_report_{month_date.strftime('%Y%m')}.json"
        self._save_report(report, filename)
        
        return report
    
    def _filter_data_by_period(self, data, date, period_type):
        """Filter data based on period type"""
        if 'created_at' not in data.columns:
            return data
            
        data_copy = data.copy()
        data_copy['created_at'] = pd.to_datetime(data_copy['created_at'])
        
        if period_type == 'daily':
            target_date = date.date()
            return data_copy[data_copy['created_at'].dt.date == target_date]
            
        elif period_type == 'weekly':
            end_date = date + timedelta(days=6)
            return data_copy[
                (data_copy['created_at'].dt.date >= date.date()) & 
                (data_copy['created_at'].dt.date <= end_date.date())
            ]
            
        elif period_type == 'monthly':
            next_month = date.replace(day=28) + timedelta(days=4)
            next_month = next_month.replace(day=1)
            return data_copy[
                (data_copy['created_at'].dt.date >= date.date()) & 
                (data_copy['created_at'].dt.date < next_month.date())
            ]
        
        return data_copy
    
    def _analyze_weekly_trends(self, data, start_date):
        """Analyze weekly trends compared to previous week"""
        prev_week_start = start_date - timedelta(days=7)
        
        current_week_data = self._filter_data_by_period(data, start_date, 'weekly')
        prev_week_data = self._filter_data_by_period(data, prev_week_start, 'weekly')
        
        from .metrics_calculator import MetricsCalculator
        calculator = MetricsCalculator()
        
        current_metrics = calculator.calculate_all_metrics(current_week_data)
        prev_metrics = calculator.calculate_all_metrics(prev_week_data)
        
        trends = {}
        
        # Resolution time trend
        current_res_time = current_metrics['resolution_times']['avg_resolution_time']
        prev_res_time = prev_metrics['resolution_times']['avg_resolution_time']
        trends['resolution_time_trend'] = self._calculate_trend(current_res_time, prev_res_time, 'decrease')
        
        # Satisfaction trend
        current_sat = current_metrics['satisfaction_trends']['avg_satisfaction']
        prev_sat = prev_metrics['satisfaction_trends']['avg_satisfaction']
        trends['satisfaction_trend'] = self._calculate_trend(current_sat, prev_sat, 'increase')
        
        # KB usage trend
        current_kb = current_metrics['kb_usage']['usage_rate']
        prev_kb = prev_metrics['kb_usage']['usage_rate']
        trends['kb_usage_trend'] = self._calculate_trend(current_kb, prev_kb, 'increase')
        
        return trends
    
    def _analyze_monthly_trends(self, data, month_date):
        """Analyze monthly trends"""
        # This would compare with previous months and identify seasonal patterns
        return {
            'resolution_time_trend': 'stable',
            'satisfaction_trend': 'improving',
            'volume_trend': 'increasing',
            'kb_adoption_trend': 'growing'
        }
    
    def _calculate_trend(self, current, previous, desired_direction):
        """Calculate trend direction"""
        if previous == 0:
            return 'neutral'
        
        change = ((current - previous) / previous) * 100
        
        if abs(change) < 5:
            return 'stable'
        elif (desired_direction == 'increase' and change > 0) or (desired_direction == 'decrease' and change < 0):
            return 'improving'
        else:
            return 'declining'
    
    def _get_top_performers(self, agent_scores, top_n=5):
        """Get top performing agents"""
        if not agent_scores:
            return []
        
        sorted_agents = sorted(agent_scores, key=lambda x: x.get('overall_score', 0), reverse=True)
        return sorted_agents[:top_n]
    
    def _generate_daily_insights(self, metrics, data):
        """Generate daily insights"""
        insights = []
        
        resolution_rate = metrics['resolution_times']['resolution_rate']
        if resolution_rate < 50:
            insights.append("Low resolution rate detected - consider allocating more resources")
        
        avg_satisfaction = metrics['satisfaction_trends']['avg_satisfaction']
        if avg_satisfaction < 3.0:
            insights.append("Customer satisfaction below target - review recent interactions")
        
        return insights
    
    def _generate_weekly_insights(self, metrics, trends):
        """Generate weekly insights"""
        insights = []
        
        if trends.get('resolution_time_trend') == 'declining':
            insights.append("Resolution times are increasing - investigate bottlenecks")
        
        if trends.get('satisfaction_trend') == 'improving':
            insights.append("Customer satisfaction showing positive trend - maintain current practices")
        
        kb_usage = metrics['kb_usage']['usage_rate']
        if kb_usage < 30:
            insights.append("Knowledge base usage is low - promote KB articles in agent responses")
        
        return insights
    
    def _generate_strategic_insights(self, metrics, trends):
        """Generate strategic monthly insights"""
        insights = []
        
        # Analyze resolution efficiency
        res_time = metrics['resolution_times']['avg_resolution_time']
        if res_time > 48:
            insights.append("Strategic initiative needed to reduce resolution times across the board")
        
        # Analyze customer satisfaction
        satisfaction = metrics['satisfaction_trends']['avg_satisfaction']
        if satisfaction > 4.2:
            insights.append("Excellent customer satisfaction achieved - document best practices")
        
        # Analyze resource allocation
        agent_performance = metrics['agent_scores']
        if agent_performance:
            score_variance = np.std([agent.get('overall_score', 0) for agent in agent_performance])
            if score_variance > 20:
                insights.append("High variance in agent performance - implement targeted training")
        
        return insights
    
    def _generate_daily_recommendations(self, metrics):
        """Generate daily recommendations"""
        recommendations = []
        
        if metrics['resolution_times']['resolution_rate'] < 60:
            recommendations.append("Prioritize backlog clearance in the morning standup")
        
        if metrics['satisfaction_trends']['avg_satisfaction'] < 3.5:
            recommendations.append("Conduct quality assurance review on recent tickets")
        
        return recommendations
    
    def _generate_weekly_recommendations(self, metrics, trends):
        """Generate weekly action items"""
        recommendations = []
        
        if trends.get('resolution_time_trend') == 'declining':
            recommendations.append("Review and optimize ticket assignment process")
        
        if metrics['kb_usage']['usage_rate'] < 40:
            recommendations.append("Run KB usage training session for agents")
        
        return recommendations
    
    def _generate_quarterly_recommendations(self, metrics, trends):
        """Generate quarterly planning recommendations"""
        return [
            "Evaluate and update knowledge base content based on usage patterns",
            "Plan targeted training programs based on agent performance analysis",
            "Review and optimize support workflow processes",
            "Set quarterly goals for customer satisfaction and resolution metrics"
        ]
    
    def _generate_executive_summary(self, metrics, data):
        """Generate executive summary for monthly report"""
        return {
            'total_volume': len(data),
            'key_achievements': self._identify_achievements(metrics),
            'critical_metrics': {
                'customer_satisfaction': metrics['satisfaction_trends']['avg_satisfaction'],
                'operational_efficiency': metrics['resolution_times']['avg_resolution_time'],
                'knowledge_adoption': metrics['kb_usage']['usage_rate']
            }
        }
    
    def _identify_achievements(self, metrics):
        """Identify key achievements for the period"""
        achievements = []
        
        if metrics['satisfaction_trends']['avg_satisfaction'] >= 4.0:
            achievements.append("Maintained high customer satisfaction standards")
        
        if metrics['kb_usage']['usage_rate'] >= 50:
            achievements.append("Achieved strong knowledge base adoption")
        
        if metrics['resolution_times']['resolution_rate'] >= 80:
            achievements.append("Excellent ticket resolution rate maintained")
        
        return achievements
    
    def _analyze_resolution_performance(self, resolution_metrics):
        """Analyze resolution performance in detail"""
        return {
            'efficiency_rating': 'Good' if resolution_metrics['avg_resolution_time'] < 24 else 'Needs Improvement',
            'bottleneck_analysis': self._identify_bottlenecks(resolution_metrics),
            'improvement_opportunities': ['Automate common responses', 'Optimize escalation process']
        }
    
    def _analyze_satisfaction_performance(self, satisfaction_metrics):
        """Analyze satisfaction performance in detail"""
        return {
            'trend_analysis': 'Positive' if satisfaction_metrics['avg_satisfaction'] >= 4.0 else 'Monitoring Required',
            'key_drivers': ['Response time', 'Solution quality', 'Agent communication'],
            'improvement_areas': ['Follow-up process', 'Knowledge consistency']
        }
    
    def _analyze_kb_impact(self, kb_metrics):
        """Analyze knowledge base impact"""
        return {
            'adoption_level': 'High' if kb_metrics['usage_rate'] >= 60 else 'Moderate',
            'effectiveness': 'Positive' if kb_metrics['effectiveness'] > 0 else 'Neutral',
            'growth_opportunities': ['Expand article coverage', 'Improve search functionality']
        }
    
    def _rank_agents(self, agent_scores):
        """Rank agents by performance"""
        if not agent_scores:
            return []
        
        ranked_agents = sorted(agent_scores, key=lambda x: x.get('overall_score', 0), reverse=True)
        for i, agent in enumerate(ranked_agents):
            agent['rank'] = i + 1
        
        return ranked_agents
    
    def _identify_improvement_areas(self, agent_scores):
        """Identify common improvement areas across agents"""
        areas = []
        
        if agent_scores:
            avg_resolution_time = np.mean([agent.get('avg_resolution_time', 0) for agent in agent_scores])
            if avg_resolution_time > 24:
                areas.append("Resolution time optimization")
            
            avg_satisfaction = np.mean([agent.get('avg_satisfaction', 0) for agent in agent_scores if 'avg_satisfaction' in agent])
            if avg_satisfaction < 4.0:
                areas.append("Customer communication skills")
        
        return areas
    
    def _identify_bottlenecks(self, resolution_metrics):
        """Identify potential bottlenecks in resolution process"""
        bottlenecks = []
        
        if resolution_metrics['avg_resolution_time'] > 48:
            bottlenecks.append("Initial response time")
        
        if 'priority_analysis' in resolution_metrics:
            for priority, time in resolution_metrics['priority_analysis'].items():
                if time > 72:  # 3 days
                    bottlenecks.append(f"{priority} priority handling")
        
        return bottlenecks if bottlenecks else ["No major bottlenecks identified"]
    
    def _save_report(self, report, filename):
        """Save report to file"""
        filepath = os.path.join(self.reports_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
