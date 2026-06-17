import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: '0.0.0.0',
    // Allowed hosts block uses environment variable for security (configure via .env)
    allowedHosts: [
      process.env.VITE_NGROK_HOST || 'localhost'
    ],
    // HMR configuration prevents WebSocket connection errors over HTTPS
    hmr: process.env.VITE_NGROK_HOST ? {
      host: process.env.VITE_NGROK_HOST,
      clientPort: 443,
      protocol: 'wss'
    } : undefined
  }
})