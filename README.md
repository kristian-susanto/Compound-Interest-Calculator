# 🪄 Compound Interest Calculator

A modern, responsive, and feature-rich web application to project savings and investment growth over time. This tool visualizes the power of compounding through interactive charts and provides comprehensive data export options.

## ✨ Features

- **Real-time Calculation:** Results update instantly as you modify investment parameters.
- **Interactive Visualization:** Dynamic line charts powered by `Chart.js` with area shading for better data distinction.
- **Currency Flexibility:** Support for Yuan (¥), US Dollar ($), Rupiah (Rp), and generic symbols.
- **Flexible Compounding:** Options for Annual, Semiannual, Quarterly, Monthly, and Daily compounding frequencies.
- **Dark Mode Support:** Smooth transition between Light and Dark themes with persistent local storage.
- **Data Table View:** A toggleable detailed breakdown of annual future values and total contributions.
- **Mobile Optimized:** Fully responsive design using Tailwind CSS, ensuring a great experience on phones, tablets, and desktops.

## 📥 Export Options

This calculator goes beyond simple viewing by allowing users to take their data with them:

- **PDF Report:** Professional document containing the growth chart and a detailed data table.
- **Excel (XLSX):** Properly formatted spreadsheet with numeric types and thousand separators.
- **CSV:** Clean, comma-separated values with BOM (Byte Order Mark) for perfect encoding in Microsoft Excel.
- **Image (PNG/SVG):** High-resolution snapshots of your projection for presentations or sharing.
- **Print:** Direct-to-printer functionality optimized for landscape chart viewing.

## 🛠️ Built With

- **Styling:** [Tailwind CSS](https://tailwindcss.com/)
- **Charts:** [Chart.js](https://www.chartjs.org/)
- **Excel Export:** [SheetJS (XLSX)](https://sheetjs.com/)
- **PDF Generation:** [jsPDF](https://github.com/parallax/jsPDF) & [jsPDF-AutoTable](https://github.com/simonbengtsson/jsPDF-AutoTable)

## 🚀 Installation & Usage

1.  Clone or download the repository.
2.  Ensure you have an internet connection (to load dependencies from CDN).
3.  Open the `index.html` file in any modern web browser.
4.  No build process or server-side setup is required.

## 📝 Mathematical Logic

The calculator uses an iterative approach to account for monthly contributions and compounding frequencies:

- **For Annual Compounding ($n=1$):**
  $$Balance_{new} = Balance_{current} \times (1 + Rate) + AnnualContribution$$

- **For Periodic Compounding ($n > 1$):**
  The yearly contribution is divided by the compounding frequency and applied at each interval using the periodic rate ($Rate / n$).

---

Developed with ❤️ for financial literacy.
