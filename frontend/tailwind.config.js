/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': {
          'pink': '#FF99CC',
          'purple': '#5639AC',
          'brighter-purple': '#714CE0',
        },
        'background': {
          'brown': '#18171C',
          'brighter-brown': '#382E32'
        },
      },
    },
  },
  plugins: [],
}
