module.exports = {
  purge: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      width: {
        "full-with-margins": "calc(100% - 30px)",
      },
      backgroundImage: (theme) => ({
        "koi-fish-pond": "url('/src/assets/KoiFishPond.png')",
        "knight-hacks-logo": "url('/src/assets/knightHacksLogo_WHITE.svg')",
      }),
      backgroundColor: (theme) => ({
        "landing-transparent": "rgba(191, 219, 254, 0.2)",
        "menu-transparent": "rgba(96, 165, 250, 0.6)",
      }),
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
