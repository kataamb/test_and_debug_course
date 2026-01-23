import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: true,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // ваш FastAPI бэкенд
        changeOrigin: true,
        secure: false,
        // Если ваш бэкенд ожидает пути без /api, раскомментируйте:
        // rewrite: (path) => path.replace(/^\/api/, '')
      },
      
      '/physics.wasm': {
        target: 'http://localhost:5173/src/wasm',
        changeOrigin: true,
        rewrite: (path) => '/physics.wasm',
        configure: (proxy, options) => {
          proxy.on('proxyRes', (proxyRes, req, res) => {
            proxyRes.headers['content-type'] = 'application/wasm'
          })
        }
      }
      
    }
  }
})
