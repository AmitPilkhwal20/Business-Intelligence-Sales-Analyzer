
📊 Business Intelligence Sales Analyzer
A Production-Quality, Enterprise-Grade Sales Data Cleaning, BI Analytics & Automated Reporting Platform

PythonStreamlitPandasMySQLReportLabLicense

📌 Table of Contents
Executive Summary
Key Features
System Architecture & Data Flow
Project Directory Structure
Database Schema & Multi-Engine Strategy
Installation & Quickstart Guide
Multi-Format Report Generation
Placement Interview Discussion & Q&A
License & Author
🎯 Executive Summary
The Business Intelligence Sales Analyzer is an end-to-end analytics platform designed to solve real-world sales reporting challenges faced by modern organizations. It automates the raw sales data ingestion pipeline, performs multi-stage data cleaning, calculates core financial KPIs, generates dynamic natural-language executive insights, renders publication-grade Matplotlib charts, and exports multi-format reports (CSV, styled Excel, and executive PDF).

Built using Python 3, Streamlit, Pandas, MySQL, ReportLab, and OpenPyXL, the project adheres to clean modular architecture, object-oriented design principles, robust error handling, and thread-safe logging.

🌟 Key Features
1. 🧹 Automated Data Cleaning Engine
Ingests CSV and Excel (.xlsx, .xls) files up to thousands of rows.
Converts column headers automatically into standard snake_case.
Removes exact duplicate records and trims leading/trailing whitespace.
Imputes missing numerical values with column medians and missing text fields with "Unknown".
Casts date fields to native datetime64 types.
Generates a full Data Cleaning Audit Log with before/after row counts.
2. 📈 Multi-Dimensional Sales Analytics Engine
Core KPIs: Total Revenue, Net Profit, Total Orders, Average Order Value (AOV), Profit Margin %.
Time-Series Breakdowns: Monthly, Quarterly, and Yearly trends.
Dimensional Aggregations: Region, City, Category, Sub-Category, and Customer Segments.
Product Ranking: Top 10 Best Selling and Worst Performing Products by revenue and volume.
Discount Impact Analysis: Measures promotional discount levels against net profit margins.
3. 💡 Automated BI Executive Insights Engine
Dynamically generates human-readable executive summaries in natural language.
Highlights peak performance months, category profit leaders, regional market dominance, and discount margin risks.
4. 🖥️ Interactive Streamlit Dashboard UI
Vibrant KPI metric cards with period growth indicators.
Global dynamic sidebar filters for Year, Region, Category, and Product.
Live dataset explorer with real-time keyword searching and filtering.
High-res Matplotlib chart rendering embedded directly in UI tabs.
5. 📑 Multi-Format Report Exporter
Cleaned CSV Export: Ready for downstream Machine Learning or ETL pipelines.
Styled Excel Report (OpenPyXL): Multi-tab workbook with KPI card blocks, formatted currency cells, and raw cleaned data.
Executive PDF Report (ReportLab): Styled document containing KPI summary grids, narrative BI text, embedded visual chart images, and top product tables.
6. 🛢️ Resilient Dual-Database Architecture
Connects to MySQL 8.0+ for production deployments.
Features automatic SQLite fallback (database/sales_bi_fallback.db) for zero-configuration testing.
Logs dataset metadata uploads, analysis execution runs, and report generation events.
🏗️ System Architecture & Data Flow
Mermaid diagram
📂 Project Directory Structure

Business-Intelligence-Sales-Analyzer/
├── data/                       # Raw input sales datasets
│   ├── sample_sales_data.csv   # Auto-generated 1,200+ row dataset
│   └── sample_sales_data.xlsx  # Excel sample dataset
├── cleaned_data/               # Output folder for cleaned CSV exports
├── database/                   # Database scripts and fallback database
│   └── sales_bi_fallback.db   # Auto-initialized SQLite fallback DB
├── reports/                    # Generated Excel (.xlsx) and PDF reports
├── charts/                     # Exported PNG chart images (300 DPI)
├── assets/                     # UI visual assets and styling
├── logs/                       # Rotating application execution log files
│   └── app.log
├── src/                        # Modular source code
│   ├── __init__.py
│   ├── config.py               # Path management, DB defaults & theme colors
│   ├── logger.py               # Centralized logging manager
│   ├── cleaning.py             # Data validation & auto-cleaning pipeline
│   ├── database.py             # MySQL connector with SQLite fallback
│   ├── analysis.py             # KPI engine & automated BI insight generator
│   ├── visualization.py        # Matplotlib visualization plotting engine
│   └── report_generator.py     # OpenPyXL Excel & ReportLab PDF exporter
├── sample_data_generator.py    # Realistic sales sample dataset generator script
├── schema.sql                  # MySQL database initialization DDL
├── app.py                      # Main Streamlit interactive dashboard UI
├── requirements.txt            # Python dependencies
└── README.md                   # System documentation & setup guide
🛢️ Database Schema & Multi-Engine Strategy
The application uses standard SQL DDL compatible with MySQL 8.0+ and SQLite 3:

sql

-- 1. Table: Uploaded Dataset Metadata
CREATE TABLE uploaded_datasets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    raw_row_count INT NOT NULL,
    cleaned_row_count INT NOT NULL,
    columns_list TEXT,
    status VARCHAR(50) DEFAULT 'Cleaned'
);
-- 2. Table: Analysis History & Key Metrics
CREATE TABLE analysis_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dataset_name VARCHAR(255) NOT NULL,
    analysis_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_revenue DECIMAL(15, 2),
    total_profit DECIMAL(15, 2),
    total_orders INT,
    avg_order_value DECIMAL(10, 2),
    profit_margin DECIMAL(5, 2),
    top_region VARCHAR(100),
    top_category VARCHAR(100),
    top_product VARCHAR(255)
);
-- 3. Table: Generated Reports Audit Log
CREATE TABLE report_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_name VARCHAR(255) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(500) NOT NULL
);
⚡ Installation & Quickstart Guide
1. Prerequisites
Python 3.9 or higher installed.
Git installed on your machine.
(Optional) MySQL 8.0+ running locally.
2. Clone Repository & Install Dependencies
bash

git clone https://github.com/YOUR_USERNAME/Business-Intelligence-Sales-Analyzer.git
cd Business-Intelligence-Sales-Analyzer
pip install -r requirements.txt
3. Generate Sample Dataset
Run the data generator to create realistic 1,200+ row sales files in data/:

bash

python sample_data_generator.py
4. Launch the Streamlit Interactive Dashboard
bash

streamlit run app.py
Open http://localhost:8501 in your browser.

📊 Multi-Format Report Generation
Report Type	Technology Stack	Destination Path	Key Highlights
Cleaned CSV	Pandas	cleaned_data/cleaned_sales_data.csv	Standardized snake_case headers, clean data types
Excel Report	OpenPyXL	reports/Sales_BI_Executive_Report.xlsx	Multi-tab sheet, styled KPI cards, formatted numbers
Executive PDF	ReportLab	reports/Sales_BI_Executive_Report.pdf	Formatted Document, KPI table, embedded chart images
🎓 Placement Interview Discussion & Q&A
Q1: Why use an SQLite fallback alongside MySQL?
Answer: In software engineering, resilience and portability are critical. Using an abstraction layer in DatabaseManager allows production environments to connect to a centralized MySQL server while enabling developers or interviewers to run and evaluate the application offline without installing MySQL.

Q2: How is data cleaning implemented for enterprise edge cases?
Answer: DataCleaner uses a multi-step pipeline: regex sanitization for snake_case column headers, whitespace string stripping, datetime64 coercion for date columns, median imputation for numeric missing values, and explicit duplicate removal.

Q3: Why choose ReportLab over HTML-to-PDF conversion tools?
Answer: Tools relying on browser headless rendering (like pdfkit or wkhtmltopdf) introduce heavy external C++ system dependencies. ReportLab is a pure Python flowable engine that renders high-precision vector PDFs programmatically with full layout control.

📜 License & Author
Author: Built with Python & Streamlit
License: Licensed under the 
MIT License
