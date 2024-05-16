/** @type {import('tailwindcss').Config} */
const withMT = require("@material-tailwind/react/utils/withMT");

module.exports = withMT({
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    fontFamily: {
      Normal: ['Roboto', 'sans-serif'],
      OpenDyslexic: ['OpenDyslexic3', 'sans-serif'],
      OpenDyslexicBold: ['Opendyslexic3-Bold', 'sans-serif'],
    },
    extend: {
      colors:
      {
        green2: {
          50: '#f1f8f2',
          100: '#d6e9d7',
          200: '#b8d9bb',
          300: '#99c9a0',
          400: '#7ab984',
          500: '#5ca968',
          600: '#4b8d57',
          700: '#299e2d',
          800: '#295335',
          900: '#173624',
        },
        
        dark: {
          primary: '#333',
          white: "#FFF",
          dark: "#000",
          green: "#00FF00",
          orange: "#FFA500",
          red: "#f44336",
          pink: "#ec407a",

        },
        light: {
          primary: '#FFF',
          white: "#FFF",
          dark: "#000",
          green: "#00FF00",
          orange: "#FFA500",
          red: "#f44336",
          pink: "#ec407a",
        },
        global: {
          accent: '#F00',
          white: "#FFF",
          dark: "#000",
          green: "#00FF00",
          orange: "#FFA500",
          red: "#f44336",
          pink: "#ec407a",
          bgray: "#bf360c"
        }
      }
    }
  },
  plugins: [],
});
