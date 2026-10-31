/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          DEFAULT: '#0a0f1d',
          deep: '#030712',
          card: '#111827',
          border: '#1f2937',
          hover: '#1e293b',
          muted: '#94a3b8',
        },
        brand: {
          DEFAULT: '#10b981', // Emerald AI color
          light: '#34d399',
          dark: '#059669',
          glow: 'rgba(16, 185, 129, 0.15)',
        },
        accent: {
          purple: '#8b5cf6',
          blue: '#3b82f6',
          orange: '#f97316',
        }
      },
      fontFamily: {
        mono: ['Fira Code', 'Courier New', 'monospace'],
      }
    },
  },
  plugins: [],
}
