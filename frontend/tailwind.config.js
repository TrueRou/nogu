/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx,vue}",
  ],
  daisyui: {
    themes: [
      {
        nogu: {
          "primary": "#5639AC", // guweb purple colorsets
          "primary-focus": "#714CE0",
          "primary-content": "#ffffff",
          "secondary": "#FF99CC", // guweb pink colorsets
          "secondary-focus": "#FF99CC",
          "secondary-content": "#000000",
          "accent": "#E2E8F0", // white colorsets
          "accent-focus": "#ffffff",
          "accent-content": "#000000",
          "neutral": "#382E32", // osu! darkpink colorsets
          "neutral-focus": "#382E32",
          "neutral-content": "#4A3D42",
          "base-100": "#18171C", // guweb dark colorsets
          "info": "#3abff8",
          "success": "#36d399",
          "warning": "#fbbd23",
          "error": "#f87272",
        },
      },
    ],
  },
  plugins: [require("daisyui")],
}
