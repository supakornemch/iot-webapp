<template>
  <div class="container">
    <header>
      <h1>IoT Sensor Dashboard</h1>
      
      <div class="time-controls">
        <button 
          v-for="(label, key) in timeWindows" 
          :key="key"
          :class="{ active: currentWindow === key }"
          @click="fetchData(key)"
        >
          {{ label }}
        </button>
      </div>
    </header>

    <div v-if="loading" class="loading">
      Loading...
    </div>
    <div v-else>
      <div v-if="aggregatedData" class="stats-grid">
        <StatsCard 
          title="Temperature"
          :stats="aggregatedData.temperature"
        />
        <StatsCard 
          title="Humidity"
          :stats="aggregatedData.humidity"
        />
        <StatsCard 
          title="Air Quality"
          :stats="aggregatedData.air_quality"
        />
      </div>

      <div class="chart-section">
        <SensorChart :data="sensorData" />
      </div>

      <div v-if="error" class="error">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import SensorChart from './components/SensorChart.vue';
import StatsCard from './components/StatsCard.vue';
import type { SensorData, AggregatedData } from './types';

const API_BASE_URL = 'http://localhost:8000';

const sensorData = ref<SensorData[]>([]);
const aggregatedData = ref<AggregatedData | null>(null);
const loading = ref(false);
const error = ref('');
const currentWindow = ref('1h');

const timeWindows = {
  '10m': 'Last 10 Minutes',
  '1h': 'Last Hour',
  '24h': 'Last 24 Hours'
};

const fetchData = async (window: string) => {
  loading.value = true;
  error.value = '';
  currentWindow.value = window;
  
  try {
    const [processedResponse, aggregatedResponse] = await Promise.all([
      axios.get(`${API_BASE_URL}/sensor/processed`),
      axios.get(`${API_BASE_URL}/sensor/aggregated?window=${window}`)
    ]);
    
    sensorData.value = processedResponse.data;
    aggregatedData.value = aggregatedResponse.data;
  } catch (e) {
    error.value = 'Error fetching data. Please try again.';
    console.error('Error:', e);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchData('1h');
});
</script>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

header {
  margin-bottom: 2rem;
}

h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.time-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button.active {
  background: #2c3e50;
  color: white;
  border-color: #2c3e50;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.chart-section {
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #dc3545;
  padding: 1rem;
  background: #f8d7da;
  border-radius: 4px;
  margin-top: 1rem;
}
</style>
