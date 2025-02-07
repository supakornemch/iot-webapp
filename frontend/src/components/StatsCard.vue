<template>
  <div v-motion="{ initial: { opacity: 0, scale: 0.8 }, enter: { opacity: 1, scale: 1, transition: { duration: 0.5 } } }" 
       class="bg-white p-4 rounded-lg shadow">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-semibold text-gray-800">{{ title }}</h3>
      <div v-if="hasAnomaly" class="px-2 py-1 bg-red-100 text-red-600 text-sm rounded-full animate-pulse">
        Anomaly Detected
      </div>
    </div>
    <div class="grid grid-cols-2 gap-2">
      <div class="flex justify-between p-2 bg-gray-100 rounded"
           :class="{ 'bg-red-50': isAnomalyValue(stats.mean) }">
        <span class="text-sm text-gray-600">Mean:</span>
        <span class="font-medium" :class="{ 'text-red-600': isAnomalyValue(stats.mean), 'text-gray-800': !isAnomalyValue(stats.mean) }">
          {{ formatNumber(stats.mean) }}
        </span>
      </div>
      <div class="flex justify-between p-2 bg-gray-100 rounded">
        <span class="text-sm text-gray-600">Median:</span>
        <span class="font-medium text-gray-800">{{ formatNumber(stats.median) }}</span>
      </div>
      <div class="flex justify-between p-2 bg-gray-100 rounded">
        <span class="text-sm text-gray-600">Min:</span>
        <span class="font-medium text-gray-800">{{ formatNumber(stats.min) }}</span>
      </div>
      <div class="flex justify-between p-2 bg-gray-100 rounded">
        <span class="text-sm text-gray-600">Max:</span>
        <span class="font-medium text-gray-800">{{ formatNumber(stats.max) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { MetricStats } from '../types';

const props = defineProps<{
  title: string;
  stats: MetricStats;
  hasAnomaly?: boolean;
}>();

const formatNumber = (num: number | null) => {
  return num != null ? num.toFixed(2) : '-';
};

const isAnomalyValue = (value: number | null): boolean => {
  if (!value || !props.stats) return false;
  const threshold = 2; // Standard deviations
  const mean = props.stats.mean;
  const range = props.stats.max - props.stats.min;
  const standardDev = range / 4; // Approximate standard deviation
  return Math.abs(value - mean) > threshold * standardDev;
};
</script>
