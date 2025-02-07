<template>
  <div class="max-w-6xl mx-auto p-5">
    <!-- Dashboard Header -->
    <header v-motion="{ initial: { opacity: 0, y: -50 }, enter: { opacity: 1, y: 0, transition: { duration: 0.5 } } }" 
            class="mb-8 pb-4 border-b border-gray-200">
      <h1 class="text-3xl font-bold text-gray-800 mb-4">IoT Sensor Dashboard</h1>
      <div class="flex justify-between items-center">
        <div class="text-sm text-gray-500">
          Last updated: {{ new Date().toLocaleString() }}
        </div>
        <div class="flex space-x-4">
          <button 
            v-for="(label, key) in timeWindows" 
            :key="key"
            :class="['px-4 py-2 border rounded transition-colors duration-300', 
                     currentWindow === key ? 'bg-gray-800 text-white border-gray-800' : 'bg-white text-gray-800 border-gray-300']"
            @click="fetchData(key)"
          >
            {{ label }}
          </button>
        </div>
      </div>
    </header>

    <div v-if="loading" class="text-center py-8 text-gray-600">
      <div class="animate-spin text-4xl mb-4">⚙️</div>
      Loading...
    </div>
    
    <div v-else>
      <!-- Real-time Monitoring Section -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-gray-700 mb-4">Real-time Sensor Values</h2>
        <CurrentValues 
          :current-data="currentSensorData"
        />
      </section>

      <!-- Statistical Analysis Section -->
      <section class="mb-8" v-if="aggregatedData">
        <h2 class="text-xl font-semibold text-gray-700 mb-4">Statistical Analysis</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <StatsCard 
            title="Temperature"
            :stats="aggregatedData.temperature"
            :has-anomaly="hasAnomalyInLastMinute('temperature')"
          />
          <StatsCard 
            title="Humidity"
            :stats="aggregatedData.humidity"
            :has-anomaly="hasAnomalyInLastMinute('humidity')"
          />
          <StatsCard 
            title="Air Quality"
            :stats="aggregatedData.air_quality"
            :has-anomaly="hasAnomalyInLastMinute('air_quality')"
          />
        </div>
      </section>

      <!-- Trend Analysis Section -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-gray-700 mb-4">Trend Analysis</h2>
        <div class="bg-white rounded-lg shadow">
          <SensorChart 
            :data="sensorData" 
            :time-window="currentWindow"
          />
        </div>
      </section>

      <!-- Error Messages -->
      <div v-if="error" 
           class="fixed bottom-4 right-4 text-red-600 bg-red-100 p-4 rounded-lg shadow-lg border border-red-200">
        <div class="flex items-center">
          <span class="mr-2">⚠️</span>
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import SensorChart from './components/SensorChart.vue';
import StatsCard from './components/StatsCard.vue';
import CurrentValues from './components/CurrentValues.vue';
import type { SensorData, AggregatedData } from './types';

const API_BASE_URL = 'http://localhost:8000';

const sensorData = ref<SensorData[]>([]);
const aggregatedData = ref<AggregatedData | null>(null);
const loading = ref(false);
const error = ref('');
const currentWindow = ref('1h');
const currentSensorData = ref<SensorData | null>(null);

// Add WebSocket connection handling
const ws = ref<WebSocket | null>(null);

const timeWindows = {
  '10m': 'Last 10 Minutes',
  '1h': 'Last Hour',
  '24h': 'Last 24 Hours'
};

const fetchAggregatedData = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/sensor/aggregated?window=${currentWindow.value}`);
    aggregatedData.value = response.data;
  } catch (e) {
    console.error('Error fetching aggregated data:', e);
  }
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
    
    sensorData.value = processedResponse.data.items;
    aggregatedData.value = aggregatedResponse.data;
  } catch (e) {
    error.value = 'Error fetching data. Please try again.';
    console.error('Error:', e);
  } finally {
    loading.value = false;
  }
};

const hasAnomalyInLastMinute = (metric: string) => {
  if (!sensorData.value?.length) return false;
  const oneMinuteAgo = new Date(Date.now() - 60000);
  return sensorData.value.some(d => 
    new Date(d.timestamp) >= oneMinuteAgo && 
    d.is_anomaly && 
    d[metric as keyof typeof d] != null
  );
};

const setupWebSocket = () => {
  ws.value = new WebSocket('ws://localhost:8000/sensor/ws');
  
  ws.value.onopen = () => {
    console.log('WebSocket Connected');
  };
  
  ws.value.onmessage = (event) => {
    const newData = JSON.parse(event.data);
    currentSensorData.value = newData;
  };

  ws.value.onerror = (error) => {
    console.error('WebSocket Error:', error);
  };

  ws.value.onclose = () => {
    console.log('WebSocket Disconnected');
    // Try to reconnect after 5 seconds
    setTimeout(setupWebSocket, 5000);
  };
};

onMounted(() => {
  fetchData('1h');
  setupWebSocket();
  
  // Add interval for aggregated data
  const intervalId = setInterval(fetchAggregatedData, 5000);
  
  onUnmounted(() => {
    clearInterval(intervalId);
    if (ws.value) {
      ws.value.close();
    }
  });
});
</script>

<!-- Removed the style block; styling is now handled via Tailwind CSS utility classes -->
