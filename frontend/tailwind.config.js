/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        neo: {
          bg: '#FAF7F2',
          surface: '#FFFFFF',
          dark: '#121212',
          border: '#000000',
          yellow: '#FEF08A',
          yellowDark: '#FDE047',
          pink: '#FECDD3',
          pinkDark: '#FB7185',
          coral: '#F43F5E',
          purple: '#DDD6FE',
          purpleDark: '#A78BFA',
          mint: '#A7F3D0',
          mintDark: '#34D399',
          blue: '#BAE6FD',
          blueDark: '#38BDF8',
          orange: '#FED7AA',
          orangeDark: '#FB923C',
          navy: '#0F172A'
        }
      },
      boxShadow: {
        'neo-xs': '1.5px 1.5px 0px 0px #000000',
        'neo-sm': '2px 2px 0px 0px #000000',
        'neo': '4px 4px 0px 0px #000000',
        'neo-lg': '6px 6px 0px 0px #000000',
        'neo-xl': '8px 8px 0px 0px #000000',
        'neo-reverse': '-4px 4px 0px 0px #000000',
      },
      borderWidth: {
        '3': '3px',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      }
    },
  },
  plugins: [],
}
