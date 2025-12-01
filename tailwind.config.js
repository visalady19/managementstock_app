module.exports = {
  content: [
    "./shared_templates/**/*.html",

    "./accounts/templates/**/*.html",
    "./dashboard/templates/**/*.html",
    "./inventory/templates/**/*.html",
    "./transaksi_masuk/templates/**/*.html",
    "./transaksi_keluar/templates/**/*.html",

    // jika ada template umum di root
    "./**/templates/**/*.html",
  ],

  theme: {
    extend: {},
  },

  plugins: [],
}
