# 🪄 Compound Interest Calculator

An interactive web application based on Streamlit to calculate investment projections using compound interest. This application allows users to visualize asset growth over time with various custom parameters.

## ✨ Key Features

- Multi-Currency: Supports Indonesian Rupiah (Rp), US Dollar ($), and Yuan (¥).
- Flexible Input: Set the initial investment, monthly contribution, term, and estimated interest.
- Interest Frequency: Choose from daily, monthly, quarterly, and annual compounding options.
- Interactive Visualization: Dynamic line charts using Plotly.
- Data Export: Download the full report in PDF format (including graphs and tables) or export raw data to Excel.

## Folder Structure

```
Compound-Interest-Calculator/
│
├── .gitignore
├── Home.py
├── README.MD
└── requirements.txt
```

## 🚀 How to Run

### 1. Clone Repository

```bash
git clone https://github.com/kristian-susanto/LSTM-Stock-Price-Prediction.git
cd LSTM-Stock-Price-Prediction
```

### 2. Dependency Installation

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows
```

Once the virtual environment is active, install all dependencies in one of the following ways:
Using the requirements.txt file:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit pandas plotly fpdf2 kaleido xlsxwriter
```

### 3. Run Streamlit Application

```bash
streamlit run Home.py
```

If you find it annoying to see error messages (like "unclean kill") every time you run an application, you can run Streamlit without trying to automatically open a browser with the following command:

```bash
streamlit run app.py --server.headless true
```

The application will automatically open in the browser at http://localhost:8501.

Made with Streamlit & Python.
