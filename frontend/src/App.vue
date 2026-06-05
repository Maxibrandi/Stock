<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Estados de la aplicación
const prendas = ref([])
const message = ref('Cargando inventario...')
const messageType = ref('info')

// URL Base del Backend
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Campos del formulario (Incluyendo Tela y Stock Mínimo)
const nuevoNombre = ref('')
const nuevoCodigo = ref('')
const nuevaCategoria = ref('')
const nuevoTalle = ref('m')
const nuevoTipoTela = ref('Algodón') // ¡Agregado!
const nuevoPrecio = ref(15000)
const nuevoStockActual = ref(0)
const nuevoStockMinimo = ref(2)      // ¡Agregado!

// Obtener prendas (GET)
const obtenerPrendas = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/prendas/`)
    prendas.value = response.data
    if (prendas.value.length === 0) {
      message.value = 'No hay prendas en el inventario.'
      messageType.value = 'info'
    } else {
      message.value = '¡Inventario actualizado!'
      messageType.value = 'success'
    }
  } catch (error) {
    console.error(error)
    message.value = 'Error al traer las prendas.'
    messageType.value = 'error'
  }
}

// Crear prenda (POST)
const agregarPrenda = async () => {
  if (!nuevoNombre.value || !nuevoCodigo.value || !nuevaCategoria.value) {
    message.value = 'Por favor, completa los campos obligatorios (*).'
    messageType.value = 'error'
    return
  }

  try {
    const payload = {
      nombre: nuevoNombre.value,
      codigo_barras: nuevoCodigo.value,
      categoria: nuevaCategoria.value,
      talle: nuevoTalle.value,
      tipo_tela: nuevoTipoTela.value, // ¡Enviado al backend!
      precio: parseFloat(nuevoPrecio.value) || 0.0,
      stock_actual: parseInt(nuevoStockActual.value) || 0,
      stock_minimo: parseInt(nuevoStockMinimo.value) || 0  // ¡Enviado al backend!
    }

    await axios.post(`${API_URL}/api/prendas/`, payload)

    message.value = '¡Prenda registrada con éxito!'
    messageType.value = 'success'

    // Resetear formulario
    nuevoNombre.value = ''
    nuevoCodigo.value = ''
    nuevaCategoria.value = ''
    nuevoTalle.value = 'm'
    nuevoTipoTela.value = 'Algodón'
    nuevoPrecio.value = 15000
    nuevoStockActual.value = 0
    nuevoStockMinimo.value = 2

    await obtenerPrendas()
  } catch (error) {
    console.error(error)
    if (error.response?.status === 422) {
      const detalles = error.response.data.detail
      message.value = `Error SQLModel: ${detalles[0].loc[1]} - ${detalles[0].msg}`
    } else {
      message.value = 'Error al procesar el formulario.'
    }
    messageType.value = 'error'
  }
}

onMounted(() => {
  obtenerPrendas()
})
</script>

<template>
  <div class="min-h-screen bg-gray-100 p-6 font-sans">
    <div class="max-w-7xl mx-auto">

      <header class="mb-8 flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 tracking-tight">Sistema de Control de Stock</h1>
          <p class="text-sm text-gray-500 mt-1">Gestión operativa integral</p>
        </div>

        <div :class="[
          'px-4 py-2 rounded-lg text-sm font-semibold border transition-all duration-300',
          messageType === 'success' ? 'bg-green-50 text-green-700 border-green-200' : '',
          messageType === 'error' ? 'bg-red-50 text-red-700 border-red-200' : '',
          messageType === 'info' ? 'bg-blue-50 text-blue-700 border-blue-200' : ''
        ]">
          {{ message }}
        </div>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">

        <section class="bg-white p-6 rounded-xl shadow-sm border border-gray-200 h-fit">
          <h2 class="text-xl font-bold text-gray-700 mb-6 border-b pb-2">Registrar Prenda</h2>

          <form @submit.prevent="agregarPrenda" class="space-y-4">
            <div>
              <label class="block text-xs font-bold uppercase text-gray-500 mb-1">Nombre *</label>
              <input v-model="nuevoNombre" type="text" placeholder="Ej: Remera Boxy Fit" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-gray-50" />
            </div>

            <div>
              <label class="block text-xs font-bold uppercase text-gray-500 mb-1">Código de Barras *</label>
              <input v-model="nuevoCodigo" type="text" placeholder="Ej: 779123456789" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-gray-50" />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold uppercase text-gray-500 mb-1">Categoría *</label>
                <input v-model="nuevaCategoria" type="text" placeholder="Ej: Remeras" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-gray-50" />
              </div>
              <div>
                <label class="block text-xs font-bold uppercase text-gray-500 mb-1">Tipo de Tela</label>
                <input v-model="nuevoTipoTela" type="text" placeholder="Ej: Algodón" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-gray-50" />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold uppercase text-gray-500 mb-1">Talle *</label>
                <select v-model="nuevoTalle" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-gray-50 uppercase font-semibold">
                  <option value="xs">XS</option>
                  <option value="s">S</option>
                  <option value="m">M</option>
                  <option value="l">L</option>
                  <option value="xl">XL</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-bold uppercase text-gray-500 mb-1">Precio ($) *</label>
                <input v-model="nuevoPrecio" type="number" step="0.01" min="0.01" class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-gray-50" />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4 bg-blue-50 p-3 rounded-lg border border-blue-100">
              <div>
                <label class="block text-xs font-bold uppercase text-blue-700 mb-1">Stock Inicial *</label>
                <input v-model="nuevoStockActual" type="number" min="0" class="w-full px-3 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white font-bold" />
              </div>
              <div>
                <label class="block text-xs font-bold uppercase text-blue-700 mb-1">Mínimo Alerta *</label>
                <input v-model="nuevoStockMinimo" type="number" min="0" class="w-full px-3 py-2 border border-blue-200 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white font-bold" />
              </div>
            </div>

            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 rounded-lg transition-colors shadow-md shadow-blue-100">
              Guardar Prenda
            </button>
          </form>
        </section>

        <section class="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-gray-200">
          <h2 class="text-xl font-bold text-gray-700 mb-6 border-b pb-2">Inventario en Depósito</h2>

          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-gray-50 text-gray-500 uppercase text-xs tracking-wider border-b">
                  <th class="py-3 px-4 font-semibold">Prenda</th>
                  <th class="py-3 px-4 font-semibold">Categoría</th>
                  <th class="py-3 px-4 font-semibold text-center">Talle</th>
                  <th class="py-3 px-4 font-semibold">Tela</th>
                  <th class="py-3 px-4 font-semibold text-right">Precio</th>
                  <th class="py-3 px-4 font-semibold text-center bg-blue-50 text-blue-700 w-28">Stock Actual</th>
                  <th class="py-3 px-4 font-semibold text-center text-gray-400 w-24">Mín. Alerta</th>
                </tr>
              </thead>
              <tbody class="divide-y text-gray-700 text-sm">
                <tr v-for="prenda in prendas" :key="prenda.id" class="hover:bg-gray-50 transition-colors">
                  <td class="py-3.5 px-4">
                    <span class="font-medium text-gray-900 block">{{ prenda.nombre }}</span>
                    <span class="text-xs font-mono text-gray-400 block mt-0.5">{{ prenda.codigo_barras }}</span>
                  </td>
                  <td class="py-3.5 px-4 text-gray-500">{{ prenda.categoria }}</td>
                  <td class="py-3.5 px-4 text-center">
                    <span class="bg-gray-100 text-gray-800 font-bold px-2 py-0.5 rounded text-xs uppercase">
                      {{ prenda.talle }}
                    </span>
                  </td>
                  <td class="py-3.5 px-4 text-gray-500 italic">{{ prenda.tipo_tela || '-' }}</td>
                  <td class="py-3.5 px-4 text-right font-semibold text-gray-900">${{ prenda.precio.toLocaleString('es-AR') }}</td>

                  <td class="py-3.5 px-4 text-center bg-blue-50/50">
                    <span :class="[
                      'px-2.5 py-1 rounded-full font-bold text-xs border shadow-sm',
                      prenda.stock_actual <= prenda.stock_minimo
                        ? 'bg-red-100 text-red-700 border-red-200'
                        : 'bg-green-100 text-green-700 border-green-200'
                    ]">
                      {{ prenda.stock_actual }} u.
                    </span>
                  </td>

                  <td class="py-3.5 px-4 text-center text-gray-400 font-semibold">{{ prenda.stock_minimo }} u.</td>
                </tr>
              </tbody>
            </table>

            <div v-if="prendas.length === 0" class="text-center py-12 text-gray-400 italic">
              No hay prendas registradas en este momento.
            </div>
          </div>
        </section>

      </div>
    </div>
  </div>
</template>