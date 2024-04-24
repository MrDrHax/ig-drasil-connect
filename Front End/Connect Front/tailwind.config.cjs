/** @type {import('tailwindcss').Config} */
const withMT = require("@material-tailwind/react/utils/withMT");

module.exports = withMT({
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    fontFamily: {
      Normal: ['Roboto', 'sans-serif'],
      OpenDyslexic: ['OpenDyslexic3', 'sans-serif'],
    },
    extend: {
      colors:
      {
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
        }
      }
    }
  },
  plugins: [],
});
