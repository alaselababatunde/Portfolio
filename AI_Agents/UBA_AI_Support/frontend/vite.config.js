import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        proxy: {
            '/chat': {
                target: 'http://localhost:7860',
                changeOrigin: true,
            },
            '/assets': {
                target: 'http://localhost:7860',
                changeOrigin: true,
            }
        }
    }
})
