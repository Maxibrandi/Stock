import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue' // <-- Corregido con el paquete oficial sin comillas extras

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,       // Permite que Docker exponga el puerto correctamente
    port: 5173,
    watch: {
      usePolling: true // Clave para que refresque los cambios en caliente dentro de Docker
    }
  }
})