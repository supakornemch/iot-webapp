<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
    <div class="bg-white p-4 rounded-lg shadow">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-600">Temperature</h3>
          <p :class="[
            'text-3xl font-bold', 
            currentData?.is_anomaly ? 'text-red-600' : 'text-gray-900'
          ]">
            {{ formatValue(currentData?.temperature) }}°C
          </p>
        </div>
        <div class="text-4xl" :class="currentData?.is_anomaly ? 'text-red-500' : 'text-gray-400'">
          🌡️
        </div>
      </div>
    </div>

    <div class="bg-white p-4 rounded-lg shadow">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-600">Humidity</h3>
          <p :class="[
            'text-3xl font-bold', 
            currentData?.is_anomaly ? 'text-red-600' : 'text-gray-900'
          ]">
            {{ formatValue(currentData?.humidity) }}%
          </p>
        </div>
        <div class="text-4xl" :class="currentData?.is_anomaly ? 'text-red-500' : 'text-gray-400'">
          💧
        </div>
      </div>
    </div>

    <div class="bg-white p-4 rounded-lg shadow">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-600">Air Quality</h3>
          <p :class="[
            'text-3xl font-bold', 
            currentData?.is_anomaly ? 'text-red-600' : 'text-gray-900'
          ]">
            {{ formatValue(currentData?.air_quality) }}
          </p>
        </div>
        <div class="text-4xl" :class="currentData?.is_anomaly ? 'text-red-500' : 'text-gray-400'">
          🌬️
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { SensorData } from '../types';

defineProps<{
  currentData: SensorData | null;
}>();

const formatValue = (value: number | null | undefined) => {
  if (value == null) return '-';
  return value.toFixed(2);
};
</script>
