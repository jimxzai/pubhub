import type { Config } from 'tailwindcss'
import typography from '@tailwindcss/typography'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Gospel of John theme colors
        primary: {
          50: '#fdf8f6',
          100: '#f2e8e5',
          200: '#eaddd7',
          300: '#e0cec7',
          400: '#d2bab0',
          500: '#bfa094',
          600: '#a18072',
          700: '#977669',
          800: '#846358',
          900: '#43302b',
        },
        // Scripture highlight colors
        scripture: {
          light: '#fefce8',
          DEFAULT: '#fef08a',
          dark: '#ca8a04',
        },
      },
      fontFamily: {
        chinese: ['Noto Serif TC', 'serif'],
        english: ['Crimson Text', 'serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '80ch',
            color: '#1f2937',
            a: {
              color: '#846358',
              '&:hover': {
                color: '#43302b',
              },
            },
            blockquote: {
              borderLeftColor: '#846358',
              fontStyle: 'italic',
            },
          },
        },
      },
    },
  },
  plugins: [typography],
}

export default config
