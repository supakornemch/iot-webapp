<template>
  <div class="chart-wrapper">
    <div class="chart-container">
      <Line v-if="chartData" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import type { SensorData } from '../types';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const props = defineProps<{
  data: SensorData[]
}>();

const chartData = computed(() => ({
  labels: props.data.map(d => new Date(d.timestamp).toLocaleString()),
  datasets: [
    {
      label: 'Temperature (°C)',
      data: props.data.map(d => d.temperature),
      borderColor: '#FF6384',
      backgroundColor: props.data.map(d => d.is_anomaly ? '#FF0000' : '#FF6384'),
      tension: 0.1
    },
    {
      label: 'Humidity (%)',
      data: props.data.map(d => d.humidity),
      borderColor: '#36A2EB',
      backgroundColor: props.data.map(d => d.is_anomaly ? '#FF0000' : '#36A2EB'),
      tension: 0.1
    },
    {
      label: 'Air Quality',
      data: props.data.map(d => d.air_quality),
      borderColor: '#4BC0C0',
      backgroundColor: props.data.map(d => d.is_anomaly ? '#FF0000' : '#4BC0C0'),
      tension: 0.1
    }
  ]
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const,
    },
    title: {
      display: true,
      text: 'Sensor Data Trends'
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
};
</script>

<style scoped>
.chart-wrapper {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart-container {
  height: 400px;
}
</style>
