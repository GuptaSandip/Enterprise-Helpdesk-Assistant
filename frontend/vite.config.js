import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../static',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/ask':     { target: 'http://localhost:8000', changeOrigin: true },
      '/tickets': { target: 'http://localhost:8000', changeOrigin: true },
      '/health':  { target: 'http://localhost:8000', changeOrigin: true },
      '/session': { target: 'http://localhost:8000', changeOrigin: true },
    }
  }
})