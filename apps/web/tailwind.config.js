/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ink: "#14213d",
        paper: "#f4efe6",
        sand: "#e8dfd0",
        forest: "#1f6f5b",
        clay: "#c45c26",
        slate: "#4a5568",
      },
      fontFamily: {
        display: ["var(--font-display)", "Georgia", "serif"],
        sans: ["var(--font-sans)", "Segoe UI", "sans-serif"],
      },
      boxShadow: {
        soft: "0 12px 40px rgba(20, 33, 61, 0.08)",
      },
    },
  },
  plugins: [],
};
