-- Business Intelligence Sales Analyzer Database Schema
-- Compatible with MySQL 8.0+

CREATE DATABASE IF NOT EXISTS sales_bi_db;
USE sales_bi_db;

-- 1. Table: Uploaded Dataset Metadata
CREATE TABLE IF NOT EXISTS uploaded_datasets (
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
CREATE TABLE IF NOT EXISTS analysis_history (
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
CREATE TABLE IF NOT EXISTS report_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_name VARCHAR(255) NOT NULL,
    report_type VARCHAR(50) NOT NULL, -- 'CSV', 'EXCEL', 'PDF'
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(500) NOT NULL
);

-- 4. Table: Application Audit Logs
CREATE TABLE IF NOT EXISTS application_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_level VARCHAR(20) NOT NULL,
    module_name VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
