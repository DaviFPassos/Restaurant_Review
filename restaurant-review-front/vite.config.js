import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: '0.0.0.0',
    // O proxy intercala as chamadas locais e de túnel diretamente para o contêiner Go
    proxy: {
      '/api': {
        target: 'http://gateway-service:8080',
        changeOrigin: true,
        secure: false,
      }
    },
    // Alinha curingas para aceitar qualquer subdomínio ngrok dinâmico com segurança
    allowedHosts: [
      'localhost',
      '.ngrok-free.dev',
      '.ngrok-free.app'
    ],
    // HMR garante estabilidade via túneis criptografados de WebSocket
    hmr: {
      clientPort: 443,
      protocol: 'wss'
    }
  }
})