/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      colors: {
        brand: {
          50:  '#eff6ff',
          100: '#dbeafe',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#1a56db',
          700: '#1d4ed8',
          800: '#1e3a8a',
          900: '#1e3463',
        },
        surface: {
          50:  '#f8fafc',
          100: '#f1f5f9',
          800: '#1e2433',
          900: '#0f1117',
          950: '#080b10',
        }
      }
    },
  },
  plugins: [],
}