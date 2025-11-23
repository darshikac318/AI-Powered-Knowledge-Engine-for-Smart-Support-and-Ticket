import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
import os

class DashboardGenerator:
    def _init_(self):
        plt.style.use('default')
        sns.set_palette("husl")

    def create_performance_dashboard(self, data):
        """Create comprehensive performance dashboard with multiple visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Customer Support Analytics Dashboard', fontsize=16, fontweight='bold')

        # 1. Agent Performance Scores
        agent_scores = self._calculate_agent_scores(data)
        self._plot_agent_performance(agent_scores, axes[0, 0])

        # 2. Resolution Time Trends
        resolution_times = self._calculate_resolution_times(data)
        self._plot_resolution_trends(resolution_times, axes[0, 1])

        # 3. Customer Satisfaction
        satisfaction_data = self._calculate_satisfaction_trends(data)
        self._plot_satisfaction_trends(satisfaction_data, axes[1, 0])

        # 4. Knowledge Base Usage
        kb_usage = self._calculate_kb_usage(data)
        self._plot_kb_usage(kb_usage, axes[1, 1])

        plt.tight_layout()
        return fig
