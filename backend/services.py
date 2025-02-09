import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Optional
import math

def detect_anomalies_iqr(values: List[float], multiplier: float = 1.5) -> List[bool]:
    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    lower_bound = q1 - (multiplier * iqr)
    upper_bound = q3 + (multiplier * iqr)
    return [val < lower_bound or val > upper_bound for val in values]

def is_anomaly(value: float, recent_values: List[float]) -> bool:
    if len(recent_values) < 10:  # Need minimum points for IQR
        return False
    
    values_with_current = recent_values + [value]
    anomalies = detect_anomalies_iqr(values_with_current)
    return anomalies[-1]  # Return result for current value

def clean_float(value: float) -> Optional[float]:
    """Clean float values for JSON serialization"""
    if value is None or math.isnan(value) or math.isinf(value):
        return None
    return float(value)

def safe_aggregate(series):
    """Safely calculate aggregates handling empty series and non-JSON-compliant values"""
    if series.empty:
        return {
            'mean': None,
            'median': None,
            'min': None,
            'max': None
        }
        
    # Handle NaN and Inf values
    clean_series = series.replace([np.inf, -np.inf], np.nan).dropna()
    
    if clean_series.empty:
        return {
            'mean': None,
            'median': None,
            'min': None,
            'max': None
        }
    
    return {
        'mean': clean_float(clean_series.mean()),
        'median': clean_float(clean_series.median()),
        'min': clean_float(clean_series.min()),
        'max': clean_float(clean_series.max())
    }

def calculate_aggregates(df: pd.DataFrame, window: str) -> Dict:
    if df.empty:
        return {
            'temperature': safe_aggregate(pd.Series([])),
            'humidity': safe_aggregate(pd.Series([])),
            'air_quality': safe_aggregate(pd.Series([])),
            'window': window,
            'count': 0
        }
    
    return {
        'temperature': safe_aggregate(df['temperature'].dropna()),
        'humidity': safe_aggregate(df['humidity'].dropna()),
        'air_quality': safe_aggregate(df['air_quality'].dropna()),
        'window': window,
        'count': len(df)
    }
