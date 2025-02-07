<template>
  <div class="stats-card">
    <h3>{{ title }}</h3>
    <div class="stats-grid">
      <div class="stat-item">
        <span class="label">Mean:</span>
        <span class="value">{{ formatNumber(stats.mean) }}</span>
      </div>
      <div class="stat-item">
        <span class="label">Median:</span>
        <span class="value">{{ formatNumber(stats.median) }}</span>
      </div>
      <div class="stat-item">
        <span class="label">Min:</span>
        <span class="value">{{ formatNumber(stats.min) }}</span>
      </div>
      <div class="stat-item">
        <span class="label">Max:</span>
        <span class="value">{{ formatNumber(stats.max) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { MetricStats } from '../types';

defineProps<{
  title: string;
  stats: MetricStats;
}>();

const formatNumber = (num: number) => num.toFixed(2);
</script>

<style scoped>
.stats-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stats-card h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.label {
  color: #6c757d;
  font-size: 0.9rem;
}

.value {
  font-weight: 600;
  color: #2c3e50;
}
</style>
