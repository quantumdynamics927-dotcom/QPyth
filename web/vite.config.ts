import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/bloch': 'http://localhost:8000',
      '/qrng': 'http://localhost:8000',
      '/bell': 'http://localhost:8000',
      '/hadamard': 'http://localhost:8000',
      '/teleport': 'http://localhost:8000',
      '/vqe_h2': 'http://localhost:8000',
    }
  }
})
