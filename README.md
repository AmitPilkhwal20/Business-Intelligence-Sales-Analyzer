# 📊 Business Intelligence Sales Analyzer

An end-to-end, production-ready **Business Intelligence Sales Analyzer** built with **Python**, **Streamlit**, **Pandas**, **Matplotlib**, **MySQL**, **ReportLab**, and **OpenPyXL**.

Designed for enterprise-level sales data ingestion, automated data cleaning, multi-dimensional KPI analytics, dynamic business intelligence narrative insights, visual chart exports, and executive report downloads (CSV, Excel, PDF).

---

## 🌟 Key Features

### 1. File Ingestion & Automated Data Cleaning Engine
- Supports **CSV** and **Excel (.xlsx, .xls)** datasets.
- Automatically standardizes headers to `snake_case`.
- Trims whitespace from text fields and removes exact duplicate records.
- Converts date strings to native `datetime64` types.
- Imputes missing numerical values with median figures and missing text values with `"Unknown"`.
- Generates a full **Data Cleaning Audit Report** visible in the UI.

### 2. Multi-Dimensional KPI & Sales Analytics
- **Financial Metrics**: Total Revenue, Net Profit, Total Orders, Average Order Value (AOV), Profit Margin %.
- **Time-Series Analysis**: Monthly, Quarterly, and Yearly trends.
- **Dimensional Breakdowns**: Performance by Category, Sub-Category, Region, City, and Customer Segment.
- **Product Analytics**: Top 10 Best Selling and Worst Performing Products.
- **Discount Impact Analysis**: Evaluates discount tier effectiveness against profit margins.

### 3. Automated Executive BI Insights Engine
- Generates human-readable narrative bullet points summarizing peak revenue months, category leadership, regional dominance, and promotional discounting risks.

### 4. Interactive Streamlit Dashboard
- **Executive Overview**: High-impact KPI metric cards and visual summary.
- **Interactive Global Filters**: Filter whole dashboard dynamically by Year, Region, Category, and Product.
- **Data Cleaning Explorer**: Real-time search and filter tool over cleaned datasets.
- **Chart Exports**: Matplotlib figures automatically rendered and saved to `charts/`.

### 5. Multi-Format Report Exporter
- **Cleaned CSV Export**: Exports cleaned dataset to `cleaned_data/`.
- **Styled Excel Report (`OpenPyXL`)**: Multi-tab workbook containing an executive summary KPI card grid, formatted numbers, colored headers, and cleaned raw data tab.
- **Executive PDF Summary (`ReportLab`)**: Formatted document with KPI grids, automated BI narrative bullet points, embedded chart images, and top products table.

### 6. Flexible Database Engine (MySQL + SQLite Fallback)
- Connects to **MySQL 8.0+** using `mysql-connector-python`.
- Features an **automatic SQLite fallback** (`database/sales_bi_fallback.db`) ensuring zero-setup execution if a MySQL service is not running locally.
- Logs dataset uploads, analysis execution history, and report generation events.

---

## 📂 Project Architecture

```
Business-Intelligence-Sales-Analyzer/
├── data/                       # Sample and uploaded raw datasets
│   └── sample_sales_data.csv   # Auto-generated 1,200+ row dataset
├── cleaned_data/               # Output directory for cleaned CSVs
├── database/                   # Database files and SQLite fallback
│   └── sales_bi_fallback.db
├── reports/                    # Generated Excel (.xlsx) and PDF reports
├── charts/                     # Saved PNG chart images (300 DPI)
├── assets/                     # UI visual assets and styling
├── logs/                       # Application execution log files
├── src/
│   ├── __init__.py
│   ├── config.py               # Global settings, paths, and color palettes
│   ├── logger.py               # Centralized logging manager
│   ├── cleaning.py             # File ingestion & data cleaning pipeline
│   ├── database.py             # MySQL connector with SQLite fallback
│   ├── analysis.py             # KPI engine & automated BI insight generator
│   ├── visualization.py        # Matplotlib plotting helper functions
│   └── report_generator.py     # OpenPyXL & ReportLab PDF exporter
├── sample_data_generator.py    # Realistic sales dataset generator script
├── schema.sql                  # MySQL database initialization DDL
├── app.py                      # Main Interactive Streamlit application
├── requirements.txt            # Python dependencies
└── README.md                   # System documentation & setup guide
```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- **Python 3.9+** installed on your system.
- (Optional) **MySQL 8.0+** installed and running locally.

### 2. Clone Repository & Install Dependencies
```bash
git clone https://github.com/your-username/Business-Intelligence-Sales-Analyzer.git
cd Business-Intelligence-Sales-Analyzer

pip install -r requirements.txt
```

### 3. Generate Sample Dataset
Run the sample data generator to populate the `data/` directory:
```bash
python sample_data_generator.py
```

### 4. (Optional) Setup MySQL Database
If using MySQL, execute `schema.sql` in your MySQL Workbench or CLI:
```sql
SOURCE schema.sql;
```
> *Note: If MySQL is not configured, the app automatically switches to SQLite fallback mode seamlessly.*

### 5. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 📑 Generated Reports Preview

| Report Type | Technology | File Location | Description |
| :--- | :--- | :--- | :--- |
| **Cleaned CSV** | `Pandas` | `cleaned_data/cleaned_sales_data.csv` | Standardized dataset ready for downstream ML/BI |
| **Excel Workbook** | `OpenPyXL` | `reports/Sales_BI_Executive_Report.xlsx` | Multi-tab formatted sheet with KPI summary cards |
| **Executive PDF** | `ReportLab` | `reports/Sales_BI_Executive_Report.pdf` | Styled PDF report with charts, KPIs, and BI text |

---

## 💡 Placement & Interview Discussion Points

- **Data Cleaning Strategy**: Used `snake_case` column standardization, median imputation for skewed numerical data, and regex parsing for text fields.
- **Resilient Database Architecture**: Designed a multi-database strategy using standard SQL schema DDL, connecting to MySQL in production while maintaining SQLite fallback for offline developer testing.
- **Reporting Engine Choice**: Utilized `ReportLab` platypus flowables to build multi-element executive PDFs with embedded matplotlib charts rather than basic HTML conversion.
- **Performance Optimization**: Integrated Streamlit session caching and localized data aggregation in `SalesAnalyzer` to handle multi-thousand row datasets in sub-second response times.

---

## 📜 License
Licensed under the [MIT License](LICENSE).
