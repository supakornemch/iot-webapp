import pandas as pd
import numpy as np
from scipy import stats

def detect_anomalies(df, column, threshold=3):
    z_scores = np.abs(stats.zscore(df[column].dropna()))
    anomalies = z_scores > threshold
    return anomalies

def clean_and_process_data(data_df):
    # Remove duplicates
    data_df = data_df.drop_duplicates()
    
    # Handle missing values with forward fill
    data_df = data_df.fillna(method='ffill')
    
    # Detect anomalies for each sensor
    for column in ['temperature', 'humidity', 'air_quality']:
        data_df[f'{column}_anomaly'] = detect_anomalies(data_df, column)
    
    return data_df

def calculate_aggregates(data_df, window):
    return {
        'temperature': {
            'mean': data_df['temperature'].mean(),
            'median': data_df['temperature'].median(),
            'min': data_df['temperature'].min(),
            'max': data_df['temperature'].max()
        },
        'humidity': {
            'mean': data_df['humidity'].mean(),
            'median': data_df['humidity'].median(),
            'min': data_df['humidity'].min(),
            'max': data_df['humidity'].max()
        },
        'air_quality': {
            'mean': data_df['air_quality'].mean(),
            'median': data_df['air_quality'].median(),
            'min': data_df['air_quality'].min(),
            'max': data_df['air_quality'].max()
        }
    }
