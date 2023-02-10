/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.vue", "./src/**/*.js"],
  theme: {
    extend: {
      screens: {
        xs: "480px",
      },
    },
  },
  plugins: [],
};
