<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const data = ref([])
const message = ref('Cargando...')

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/data')
    data.value = response.data.items
    message.value = '¡Conexión exitosa!'
  } catch (error) {
    message.value = 'Error conectando con el backend :('
  }
})
</script>

<template>
  <div>
    <h1>{{ message }}</h1>
    <ul>
      <li v-for="item in data" :key="item">{{ item }}</li>
    </ul>
  </div>
</template>