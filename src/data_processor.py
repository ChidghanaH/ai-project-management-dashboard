"""Data Processing Module for Project Management Dashboard.

Handles ETL operations: Extract, Transform, and Load project data
from various sources. Includes validation, cleaning, and aggregation.

"""

import logging
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)


class DataProcessor:
    """Process and validate project data for analytics."""
    
    def __init__(self):
        """Initialize data processor."""
        self.validation_errors = []
        logger.info("DataProcessor initialized")
    
    def load_project_data(self, file_path: str) -> pd.DataFrame:
        """Load project data from CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            DataFrame with project data
        """
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} records from {file_path}")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def validate_required_fields(self, df: pd.DataFrame, 
                                required_fields: List[str]) -> bool:
        """Validate that all required columns exist.
        
        Args:
            df: DataFrame to validate
            required_fields: List of required column names
            
        Returns:
            True if all fields present, False otherwise
        """
        missing = set(required_fields) - set(df.columns)
        if missing:
            msg = f"Missing required fields: {missing}"
            logger.error(msg)
            self.validation_errors.append(msg)
            return False
        return True
    
    def clean_missing_values(self, df: pd.DataFrame,
                            fill_numeric: float = 0,
                            fill_text: str = "Unknown") -> pd.DataFrame:
        """Handle missing values in DataFrame.
        
        Args:
            df: Input DataFrame
            fill_numeric: Value for numeric columns
            fill_text: Value for text columns
            
        Returns:
            DataFrame with missing values handled
        """
        df_clean = df.copy()
        
        for col in df_clean.columns:
            if df_clean[col].dtype in ['int64', 'float64']:
                df_clean[col].fillna(fill_numeric, inplace=True)
            else:
                df_clean[col].fillna(fill_text, inplace=True)
        
        logger.info(f"Handled missing values in {len(df_clean)} records")
        return df_clean
    
    def normalize_dates(self, df: pd.DataFrame, 
                       date_columns: List[str]) -> pd.DataFrame:
        """Convert date columns to datetime format.
        
        Args:
            df: Input DataFrame
            date_columns: List of column names to convert
            
        Returns:
            DataFrame with normalized dates
        """
        df_norm = df.copy()
        
        for col in date_columns:
            if col in df_norm.columns:
                df_norm[col] = pd.to_datetime(df_norm[col], errors='coerce')
        
        return df_norm
    
    def calculate_derived_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived metrics from base data.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with additional calculated fields
        """
        df_calc = df.copy()
        
        # Calculate budget variance if columns exist
        if 'budget' in df_calc.columns and 'actual_cost' in df_calc.columns:
            df_calc['budget_variance'] = df_calc['budget'] - df_calc['actual_cost']
        
        # Calculate percentage complete
        if 'tasks_completed' in df_calc.columns and 'total_tasks' in df_calc.columns:
            df_calc['completion_percentage'] = (
                df_calc['tasks_completed'] / df_calc['total_tasks'] * 100
            ).round(2)
        
        return df_calc
    
    def filter_by_status(self, df: pd.DataFrame, 
                        status: str) -> pd.DataFrame:
        """Filter projects by status.
        
        Args:
            df: Input DataFrame
            status: Status to filter by (Active, Completed, On-Hold)
            
        Returns:
            Filtered DataFrame
        """
        if 'status' in df.columns:
            return df[df['status'] == status]
        return df
    
    def aggregate_by_department(self, df: pd.DataFrame) -> Dict:
        """Aggregate project metrics by department.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with department-level aggregations
        """
        if 'department' not in df.columns:
            return {}
        
        aggregation = {}
        for dept in df['department'].unique():
            dept_data = df[df['department'] == dept]
            aggregation[dept] = {
                'project_count': len(dept_data),
                'avg_completion': dept_data['completion_percentage'].mean() if 'completion_percentage' in df.columns else 0,
                'total_budget': dept_data['budget'].sum() if 'budget' in df.columns else 0,
            }
        
        return aggregation
    
    def validate_data_quality(self, df: pd.DataFrame) -> float:
        """Calculate data quality score (0-100).
        
        Args:
            df: Input DataFrame
            
        Returns:
            Data quality percentage
        """
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        quality_score = ((total_cells - missing_cells) / total_cells) * 100
        
        logger.info(f"Data quality score: {quality_score:.1f}%")
        return round(quality_score, 1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    processor = DataProcessor()
    
    # Example: Process sample data
    sample_data = pd.DataFrame({
        'project_id': ['PROJ-001', 'PROJ-002'],
        'status': ['Active', 'Active'],
        'budget': [100000, 150000],
        'actual_cost': [85000, 140000],
    })
    
    processed = processor.calculate_derived_fields(sample_data)
    print(processed)
