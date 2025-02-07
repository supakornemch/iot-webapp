export interface SensorData {
  timestamp: string;
  temperature: number;
  humidity: number;
  air_quality: number;
  is_anomaly: boolean;
}

export interface AggregatedData {
  temperature: MetricStats;
  humidity: MetricStats;
  air_quality: MetricStats;
}

export interface MetricStats {
  mean: number;
  median: number;
  min: number;
  max: number;
}
