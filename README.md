# 🪄 Compound Interest Calculator

A modern, responsive, and feature-rich web application to project savings and investment growth over time. This tool visualizes the power of compounding through interactive charts and provides comprehensive data export options.

The latest version introduces an advanced feature that allows users to compare two different interest rates simultaneously.

## ✨ Features

- **Real-time & Automatic Calculation:** Results update instantly as you modify any investment parameters, without requiring a manual submit button.
- **Interest Rate Comparison:** Compare your primary investment projection (Rate 1) with an optional secondary rate (Rate 2) on the same graph.
- **Interactive Visualization:** Dynamic line charts powered by `Chart.js` featuring area shading and cross-rate comparisons.
- **Flexible Compounding:** Options for Annually, Semiannually, Quarterly, Monthly, and Daily compounding frequencies.
- **Responsive Data Table:** A toggleable, detailed breakdown of annual future values (for both rates) and total contributions, optimized with sticky layout for mobile view.
- **Dark Mode Support:** Smooth transition between Light and Dark themes with persistent preference saved in local storage.
- **Input Validation & Safety:** Integrated shake animation alerts and automated limits (e.g., maximum 100 years or 100% interest) to ensure accurate input.
- **Mobile Optimized:** Fully responsive design using Tailwind CSS, ensuring a polished experience on phones, tablets, and desktops.

## 📥 Export Options

This calculator allows users to export their financial projections in multiple formats:

- **Report (PDF):** Generates a professional PDF containing the projection chart followed by a structured annual data table.
- **Excel (XLSX):** Spreadsheet with mapped numeric values and proper financial formatting (`#,##0.00`).
- **Data (CSV):** Clean, comma-separated values with Byte Order Mark (BOM) for seamless integration with Microsoft Excel.
- **Data (JSON):** Clean JSON array payload mapping the exact annual breakdown with programmatic keys.
- **Image (PNG):** High-resolution snapshot of the investment chart featuring a clean solid background, perfect for presentations.
- **Print:** Dedicated direct-to-printer landscape layout functionality optimized for chart viewing.

## 🛠️ Built With

- **Styling:** [Tailwind CSS](https://tailwindcss.com/) (loaded via CDN with customized dark mode utilities)
- **Charts:** [Chart.js](https://www.chartjs.org/)
- **Excel Export:** [SheetJS (XLSX)](https://sheetjs.com/)
- **PDF Generation:** [jsPDF](https://github.com/parallax/jsPDF) & [jsPDF-AutoTable](https://github.com/simonbengtsson/jsPDF-AutoTable)

## 🚀 Installation & Usage

1. Clone or download the project files.
2. Ensure you have an internet connection to load the required library dependencies from CDNs.
3. Open the `index.html` file directly in any modern web browser.
4. No compilation, build processes, or server-side setups are required.

## 📝 Mathematical & Application Logic

The calculator uses an iterative annual loop to calculate compounding growth while accurately distributing regular monthly contributions:

- **For Annual Compounding ($n=1$):**
  $$Balance_{new} = Balance_{current} \times (1 + Rate_{annual}) + YearlyContribution$$

- **For Periodic Compounding ($n > 1$):**
  The yearly contribution is broken down evenly into the selected period frequency ($Contribution / n$) and compounded incrementally using the periodic rate ($Rate_{annual} / n$) throughout each interval.
- **Multi-Rate Processing:**
  If an optional second interest rate is provided, the application mirrors the identical mathematical loop independently to render the comparison data lines and table columns simultaneously.

---

Developed with ❤️ for financial literacy.
