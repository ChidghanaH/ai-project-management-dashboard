"""Project Analytics Module - Core KPI calculations and metrics.

This module handles all project performance metrics, KPI calculations,
and trend analysis. It processes raw project data and generates insights
for dashboards and reporting.

Author: Chidghana Hemantharaju
License: MIT
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)

# Constants for KPI thresholds
SCHEDULE_THRESHOLD_YELLOW = 0.95
SCHEDULE_THRESHOLD_RED = 0.85
COST_THRESHOLD_YELLOW = 0.90
COST_THRESHOLD_RED = 0.75
RISK_SCORE_HIGH = 75
RISK_SCORE_MEDIUM = 50


@dataclass
class ProjectMetrics:
    """Data class for project KPIs and metrics."""
    project_id: str
    schedule_performance_index: float
    cost_performance_index: float
    budget_variance: float
    schedule_variance: float
    risk_score: float
    team_utilization: float
    completion_percentage: float
    health_status: str  # Green, Yellow, Red
    calculated_at: datetime


class ProjectAnalytics:
    """Main analytics engine for project management dashboard.
    
    Handles calculation of KPIs, trend analysis, and performance metrics
    based on project data from multiple sources.
    """
    
    def __init__(self, project_data: Optional[pd.DataFrame] = None):
        """Initialize analytics engine.
        
        Args:
            project_data: DataFrame with project information
        """
        self.project_data = project_data
        self.metrics_cache = {}
        logger.info("ProjectAnalytics initialized")
    
    def calculate_schedule_performance_index(self, 
                                            earned_value: float,
                                            planned_value: float) -> float:
        """Calculate Schedule Performance Index (SPI).
        
        SPI = Earned Value / Planned Value
        SPI > 1.0 indicates ahead of schedule
        SPI < 1.0 indicates behind schedule
        
        Args:
            earned_value: Actual work completed (in story points or hours)
            planned_value: Planned work for period
            
        Returns:
            SPI value
        """
        if planned_value == 0:
            logger.warning("Planned value is zero, cannot calculate SPI")
            return 0.0
        
        spi = earned_value / planned_value
        logger.debug(f"Calculated SPI: {spi:.2f}")
        return round(spi, 3)
    
    def calculate_cost_performance_index(self,
                                        earned_value: float,
                                        actual_cost: float) -> float:
        """Calculate Cost Performance Index (CPI).
        
        CPI = Earned Value / Actual Cost
        CPI > 1.0 indicates under budget
        CPI < 1.0 indicates over budget
        
        Args:
            earned_value: Value of work completed (USD)
            actual_cost: Actual cost spent (USD)
            
        Returns:
            CPI value
        """
        if actual_cost == 0:
            logger.warning("Actual cost is zero, cannot calculate CPI")
            return 0.0
        
        cpi = earned_value / actual_cost
        logger.debug(f"Calculated CPI: {cpi:.2f}")
        return round(cpi, 3)
    
    def calculate_project_health(self, 
                                spi: float, 
                                cpi: float,
                                risk_score: float) -> Tuple[str, int]:
        """Determine overall project health status.
        
        Combines schedule, cost, and risk metrics into single health status.
        
        Args:
            spi: Schedule Performance Index
            cpi: Cost Performance Index  
            risk_score: Project risk score (0-100)
            
        Returns:
            Tuple of (health_status, health_percentage)
        """
        score = 0
        
        # Schedule component (40% weight)
        if spi >= 1.0:
            score += 40
        elif spi >= SCHEDULE_THRESHOLD_YELLOW:
            score += 25
        elif spi >= SCHEDULE_THRESHOLD_RED:
            score += 10
        
        # Cost component (40% weight)
        if cpi >= 1.0:
            score += 40
        elif cpi >= COST_THRESHOLD_YELLOW:
            score += 25
        elif cpi >= COST_THRESHOLD_RED:
            score += 10
        
        # Risk component (20% weight)
        risk_adjustment = max(0, 20 * (1 - risk_score / 100))
        score += risk_adjustment
        
        # Determine status
        if score >= 75:
            status = "Green"
        elif score >= 50:
            status = "Yellow"
        else:
            status = "Red"
        
        logger.info(f"Project health: {status} ({score:.0f}%)")
        return status, int(score)
    
    def calculate_risk_score(self, 
                            schedule_variance: float,
                            cost_variance: float,
                            risk_factors: List[float]) -> float:
        """Calculate composite risk score for project.
        
        Uses variance and other risk factors to produce 0-100 risk score.
        Higher score = higher risk.
        
        Args:
            schedule_variance: Absolute schedule variance
            cost_variance: Absolute cost variance
            risk_factors: List of individual risk factor scores
            
        Returns:
            Risk score 0-100
        """
        base_score = 0
        
        # Schedule risk (30% weight)
        schedule_risk = min(100, abs(schedule_variance) * 10)
        base_score += schedule_risk * 0.3
        
        # Cost risk (30% weight)
        cost_risk = min(100, abs(cost_variance) * 10)
        base_score += cost_risk * 0.3
        
        # Other factors (40% weight)
        if risk_factors:
            avg_factors = np.mean(risk_factors)
            base_score += avg_factors * 0.4
        
        final_score = min(100, base_score)
        logger.debug(f"Calculated risk score: {final_score:.1f}")
        return round(final_score, 1)
    
    def calculate_metrics(self, project_id: str, **kwargs) -> ProjectMetrics:
        """Calculate all metrics for a project.
        
        Args:
            project_id: Unique project identifier
            **kwargs: Project data (ev, pv, ac, sv, cv, etc.)
            
        Returns:
            ProjectMetrics dataclass with all calculated values
        """
        try:
            ev = kwargs.get('earned_value', 0)
            pv = kwargs.get('planned_value', 100)
            ac = kwargs.get('actual_cost', 0)
            sv = kwargs.get('schedule_variance', 0)
            cv = kwargs.get('cost_variance', 0)
            completion = kwargs.get('completion_percentage', 0)
            utilization = kwargs.get('team_utilization', 0)
            
            # Calculate indices
            spi = self.calculate_schedule_performance_index(ev, pv)
            cpi = self.calculate_cost_performance_index(ev, ac) if ac > 0 else 1.0
            
            # Calculate risk
            risk_factors = kwargs.get('risk_factors', [])
            risk_score = self.calculate_risk_score(sv, cv, risk_factors)
            
            # Determine health
            health_status, _ = self.calculate_project_health(spi, cpi, risk_score)
            
            # Create metrics object
            metrics = ProjectMetrics(
                project_id=project_id,
                schedule_performance_index=spi,
                cost_performance_index=cpi,
                budget_variance=cv,
                schedule_variance=sv,
                risk_score=risk_score,
                team_utilization=utilization,
                completion_percentage=completion,
                health_status=health_status,
                calculated_at=datetime.now()
            )
            
            # Cache the result
            self.metrics_cache[project_id] = metrics
            logger.info(f"Calculated metrics for project {project_id}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            raise
    
    def get_project_metrics(self, project_id: str) -> Optional[ProjectMetrics]:
        """Retrieve cached metrics for project.
        
        Args:
            project_id: Unique project identifier
            
        Returns:
            ProjectMetrics or None if not found
        """
        return self.metrics_cache.get(project_id)
    
    def calculate_portfolio_metrics(self, projects: List[Dict]) -> Dict:
        """Calculate aggregate metrics across project portfolio.
        
        Args:
            projects: List of project data dictionaries
            
        Returns:
            Dictionary with portfolio-level metrics
        """
        if not projects:
            logger.warning("No projects provided for portfolio analysis")
            return {}
        
        portfolio_metrics = {
            'total_projects': len(projects),
            'avg_health_score': 0,
            'at_risk_count': 0,
            'avg_budget_utilization': 0,
            'avg_schedule_health': 0,
        }
        
        health_scores = []
        utilizations = []
        schedule_indices = []
        
        for proj in projects:
            metrics = self.calculate_metrics(proj['id'], **proj.get('data', {}))
            health_scores.append(metrics.risk_score)
            utilizations.append(metrics.team_utilization)
            schedule_indices.append(metrics.schedule_performance_index)
            
            if metrics.health_status == 'Red':
                portfolio_metrics['at_risk_count'] += 1
        
        portfolio_metrics['avg_health_score'] = np.mean(health_scores) if health_scores else 0
        portfolio_metrics['avg_budget_utilization'] = np.mean(utilizations) if utilizations else 0
        portfolio_metrics['avg_schedule_health'] = np.mean(schedule_indices) if schedule_indices else 0
        
        logger.info(f"Calculated portfolio metrics for {len(projects)} projects")
        return portfolio_metrics


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    analytics = ProjectAnalytics()
    
    # Calculate metrics for a sample project
    sample_metrics = analytics.calculate_metrics(
        project_id="PROJ-001",
        earned_value=750,
        planned_value=800,
        actual_cost=120000,
        schedule_variance=-50,
        cost_variance=-5000,
        completion_percentage=93.75,
        team_utilization=0.85,
        risk_factors=[25, 30, 20]
    )
    
    print(f"Project Status: {sample_metrics.health_status}")
    print(f"Schedule Performance: {sample_metrics.schedule_performance_index}")
    print(f"Cost Performance: {sample_metrics.cost_performance_index}")
    print(f"Risk Score: {sample_metrics.risk_score}")
