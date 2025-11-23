import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class VisualizationUtils:
    def _init_(self):
        plt.style.use('default')
        self.color_palette = sns.color_palette("husl", 8)
        
    def create_agent_performance_chart(self, agent_data, ax=None):
        """Create agent performance bar chart"""
        if not agent_data:
            return None
            
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        agents = [f"Agent {item['agent_id']}" for item in agent_data]
        scores = [item.get('overall_score', 0) for item in agent_data]
        
        bars = ax.bar(agents, scores, color=self.color_palette[0], alpha=0.7)
        ax.set_title('Agent Performance Scores', fontweight='bold', fontsize=14)
        ax.set_ylabel('Performance Score', fontweight='bold')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=10)
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        return ax
    
    def create_resolution_time_trend(self, resolution_data, ax=None):
        """Create resolution time trend line chart"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
        
        weekly_trends = resolution_data.get('weekly_trends', {})
        if not weekly_trends:
            ax.text(0.5, 0.5, 'No resolution time data available', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            ax.set_title('Resolution Time Trends')
            return ax
        
        # Get last 8 weeks for better visualization
        weeks = list(weekly_trends.keys())[-8:]
        times = [weekly_trends[week] for week in weeks]
        
        ax.plot(weeks, times, marker='o', linewidth=2, markersize=6, 
               color=self.color_palette[1], label='Avg Resolution Time')
        ax.set_title('Weekly Resolution Time Trends', fontweight='bold', fontsize=14)
        ax.set_xlabel('Week', fontweight='bold')
        ax.set_ylabel('Resolution Time (hours)', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        return ax
    
    def create_satisfaction_trend_chart(self, satisfaction_data, ax=None):
        """Create customer satisfaction trend chart"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
        
        daily_trends = satisfaction_data.get('daily', {})
        if not daily_trends:
            ax.text(0.5, 0.5, 'No satisfaction data available', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            ax.set_title('Customer Satisfaction Trends')
            return ax
        
        # Get last 14 days
        dates = sorted(daily_trends.keys())[-14:]
        scores = [daily_trends[date] for date in dates]
        
        ax.plot(dates, scores, marker='s', linewidth=2, markersize=4, 
               color=self.color_palette[2], label='Satisfaction Score')
        ax.set_title('Customer Satisfaction Trends (Last 14 Days)', fontweight='bold', fontsize=14)
        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Satisfaction Score', fontweight='bold')
        ax.set_ylim(1, 5)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        return ax
    
    def create_kb_usage_pie_chart(self, kb_data, ax=None):
        """Create knowledge base usage pie chart"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        
        usage_rate = kb_data.get('usage_rate', 0)
        
        labels = ['KB Articles Used', 'Direct Support']
        sizes = [usage_rate, 100 - usage_rate]
        colors = [self.color_palette[3], self.color_palette[4]]
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                         startangle=90, textprops={'fontsize': 12})
        ax.set_title('Knowledge Base Usage Distribution', fontweight='bold', fontsize=14)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        return ax
    
    def create_performance_comparison(self, agent_scores, ax=None):
        """Create radar chart for agent performance comparison"""
        if not agent_scores or len(agent_scores) < 2:
            return None
            
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
        
        # Select top 3 agents for comparison
        top_agents = sorted(agent_scores, key=lambda x: x.get('overall_score', 0), reverse=True)[:3]
        
        categories = ['Resolution Time', 'Ticket Volume', 'Satisfaction', 'KB Usage']
        num_vars = len(categories)
        
        # Calculate angles for radar chart
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        for i, agent in enumerate(top_agents):
            values = [
                1 - (agent.get('avg_resolution_time', 0) / 72),  # Normalized (72 hours max)
                agent.get('tickets_resolved', 0) / max([a.get('tickets_resolved', 1) for a in top_agents]),
                agent.get('avg_satisfaction', 3) / 5,  # Normalized to 5-point scale
                agent.get('kb_usage_rate', 0) / 100  # Normalized percentage
            ]
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, 
                   label=f"Agent {agent['agent_id']}", color=self.color_palette[i])
            ax.fill(angles, values, alpha=0.1, color=self.color_palette[i])
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1)
        ax.set_title('Agent Performance Comparison', fontweight='bold', fontsize=14)
        ax.legend(loc='upper right')
        
        return ax
    
    def create_satisfaction_distribution(self, satisfaction_data, ax=None):
        """Create satisfaction score distribution chart"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        
        distribution = satisfaction_data.get('satisfaction_distribution', {})
        if not distribution:
            ax.text(0.5, 0.5, 'No satisfaction distribution data', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            ax.set_title('Satisfaction Score Distribution')
            return ax
        
        scores = list(distribution.keys())
        counts = list(distribution.values())
        
        bars = ax.bar(scores, counts, color=self.color_palette[5], alpha=0.7)
        ax.set_title('Customer Satisfaction Distribution', fontweight='bold', fontsize=14)
        ax.set_xlabel('Satisfaction Score', fontweight='bold')
        ax.set_ylabel('Number of Tickets', fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{int(height)}', ha='center', va='bottom', fontsize=10)
        
        return ax
    
    def create_ticket_volume_trend(self, data, ax=None):
        """Create ticket volume trend over time"""
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
        
        if 'created_at' not in data.columns:
            ax.text(0.5, 0.5, 'No date data available', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            ax.set_title('Ticket Volume Trends')
            return ax
        
        data_copy = data.copy()
        data_copy['created_at'] = pd.to_datetime(data_copy['created_at'])
        data_copy['date'] = data_copy['created_at'].dt.date
        
        daily_volume = data_copy.groupby('date').size()
        
        ax.plot(daily_volume.index, daily_volume.values, 
               color=self.color_palette[6], linewidth=2, marker='o', markersize=3)
        ax.set_title('Daily Ticket Volume Trend', fontweight='bold', fontsize=14)
        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Number of Tickets', fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        return ax
