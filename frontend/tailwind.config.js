/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'ey-black': '#000000',
        'ey-yellow': '#FFBE00',
        'ey-yellow-dark': '#E6A800',
        'ey-gray': '#1A1A1A',
        'ey-gray-light': '#2A2A2A',
      },
    },
  },
  plugins: [],
}

