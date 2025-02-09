<template>
  <div class="p-5 bg-white rounded-lg shadow">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-semibold text-gray-800">Sensor Data Trends</h3>
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-600">Data Points:</span>
        <select v-model="selectedDataPoints" class="px-3 py-1 border rounded text-sm bg-white">
          <option value="10">10 points</option>
          <option value="50">50 points</option>
          <option value="100">100 points</option>
          <option value="250">250 points</option>
          <option value="500">500 points</option>
        </select>
      </div>
    </div>
    <div class="relative h-96">
      <div v-motion="{
        initial: { opacity: 0, x: 20 },
        enter: { opacity: 1, x: 0 },
        leave: { opacity: 0, x: -20 },
        transition: { duration: 300 }
      }" class="absolute inset-0">
        <Line :data="chartData" :options="chartOptions" class="h-full" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/// <reference types="vue" />
import { computed, ref, onMounted, onUnmounted, watch } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import axios from 'axios';
import type { SensorData } from '../types';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const props = defineProps<{
  data: SensorData[] | any;
  timeWindow: string;  // Add new prop
}>();

const API_BASE_URL = 'http://localhost:8000';
const localData = ref<SensorData[]>([]);
const ws = ref<WebSocket | null>(null);

const emit = defineEmits(['dataUpdated']);

const selectedDataPoints = ref(100);

// Add function to fetch filtered data
const fetchFilteredData = async () => {
  try {
    const startDate = getStartDate();
    const endDate = new Date().toISOString();

    const response = await axios.get(`${API_BASE_URL}/sensor/processed`, {
      params: {
        page: 1,
        size: 1000,  // Increase size to get more data points
        start_date: startDate,
        end_date: endDate
      }
    });

    // Sort data by timestamp to ensure correct chart display
    localData.value = response.data.items.sort((a: SensorData, b: SensorData) =>
      new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    );
  } catch (error) {
    console.error('Error fetching filtered data:', error);
  }
};

// Add function to calculate start date based on time window
const getStartDate = () => {
  const now = new Date();
  switch (props.timeWindow) {
    case '10m':
      return new Date(now.getTime() - 10 * 60 * 1000).toISOString();
    case '1h':
      return new Date(now.getTime() - 60 * 60 * 1000).toISOString();
    case '24h':
      return new Date(now.getTime() - 24 * 60 * 60 * 1000).toISOString();
    default:
      return new Date(now.getTime() - 60 * 60 * 1000).toISOString();
  }
};

// Watch for immediate time window changes
watch(() => props.timeWindow, async (_newWindow) => {
  // Trigger exit animation
  await new Promise(resolve => setTimeout(resolve, 150));
  await fetchFilteredData();
  // Enter animation will be handled by v-motion
}, { immediate: true });

// Update WebSocket handler
onMounted(() => {
  fetchFilteredData();

  ws.value = new WebSocket('ws://localhost:8000/sensor/ws');

  ws.value.onmessage = async (event: { data: string; }) => {
    const newData = JSON.parse(event.data);
    const startDate = new Date(getStartDate());
    const newDataDate = new Date(newData.timestamp);

    // Only add new data if it falls within the selected time window
    if (newDataDate >= startDate) {
      localData.value.push(newData);
      // Remove old data outside the time window
      localData.value = localData.value.filter((d: { timestamp: string | number | Date; }) =>
        new Date(d.timestamp) >= startDate
      );
      // Sort to maintain order
      localData.value.sort((a: { timestamp: string | number | Date; }, b: { timestamp: string | number | Date; }) =>
        new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
      );
    }
  };
});

onUnmounted(() => {
  if (ws.value) {
    ws.value.close();
  }
});

// Update aggregateDataPoints function to handle 'all' option
const aggregateDataPoints = (data: SensorData[]) => {
  const targetPoints = selectedDataPoints.value;
  if (targetPoints === -1 || data.length <= targetPoints) return data;

  const chunkSize = Math.ceil(data.length / targetPoints);
  const aggregated: SensorData[] = [];

  for (let i = 0; i < data.length; i += chunkSize) {
    const chunk = data.slice(i, i + chunkSize);
    const avgPoint = {
      timestamp: chunk[Math.floor(chunk.length / 2)].timestamp, // Use middle timestamp
      temperature: chunk.reduce((sum, d) => sum + (d.temperature || 0), 0) / chunk.length,
      humidity: chunk.reduce((sum, d) => sum + (d.humidity || 0), 0) / chunk.length,
      air_quality: chunk.reduce((sum, d) => sum + (d.air_quality || 0), 0) / chunk.length,
      is_anomaly: chunk.some(d => d.is_anomaly) // Mark as anomaly if any point in chunk is anomaly
    };
    aggregated.push(avgPoint);
  }

  return aggregated;
};

// Update chartData computed property
const chartData = computed(() => {
  const aggregatedData = aggregateDataPoints(localData.value);

  return {
    labels: aggregatedData.map(d => new Date(d.timestamp).toLocaleString()),
    datasets: [
      {
        label: 'Temperature (°C)',
        data: aggregatedData.map(d => d.temperature),
        borderColor: '#FF6384',
        backgroundColor: aggregatedData.map(d => d.is_anomaly ? '#FF0000' : 'rgba(255, 99, 132, 0.2)'),
        pointRadius: aggregatedData.map(d => d.is_anomaly ? 6 : 3),
        pointStyle: aggregatedData.map(d => d.is_anomaly ? 'triangle' : 'circle'),
        borderWidth: 2
      },
      {
        label: 'Humidity (%)',
        data: aggregatedData.map(d => d.humidity),
        borderColor: '#36A2EB',
        backgroundColor: aggregatedData.map(d => d.is_anomaly ? '#FF0000' : 'rgba(54, 162, 235, 0.2)'),
        pointRadius: aggregatedData.map(d => d.is_anomaly ? 6 : 3),
        pointStyle: aggregatedData.map(d => d.is_anomaly ? 'triangle' : 'circle'),
        borderWidth: 2
      },
      {
        label: 'Air Quality',
        data: aggregatedData.map(d => d.air_quality),
        borderColor: '#4BC0C0',
        backgroundColor: aggregatedData.map(d => d.is_anomaly ? '#FF0000' : 'rgba(75, 192, 192, 0.2)'),
        pointRadius: aggregatedData.map(d => d.is_anomaly ? 6 : 3),
        pointStyle: aggregatedData.map(d => d.is_anomaly ? 'triangle' : 'circle'),
        borderWidth: 2
      }
    ]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 300
  },
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: 'Sensor Data Trends'
    },
    tooltip: {
      callbacks: {
        label: (context: any) => {
          const dataIndex = context.dataIndex;
          const dataPoint = localData.value[dataIndex];
          let label = context.dataset.label + ': ' + context.formattedValue;
          if (dataPoint?.is_anomaly) {
            label += ' (ANOMALY)';
          }
          return label;
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
};
</script>
