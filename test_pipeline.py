import sys
from pathlib import Path

from src.config import DATA_DIR, REPORTS_DIR, CHARTS_DIR
from src.cleaning import DataCleaner
from src.database import db_manager
from src.analysis import SalesAnalyzer
from src.visualization import ChartGenerator
from src.report_generator import ReportGenerator

def test_full_pipeline():
    print("=== 1. Testing Raw Data Ingestion ===", flush=True)
    sample_csv = DATA_DIR / "sample_sales_data.csv"
    raw_df = DataCleaner.load_raw_data(sample_csv, "sample_sales_data.csv")
    print(f"Raw DataFrame shape: {raw_df.shape}", flush=True)

    print("\n=== 2. Testing Data Cleaning Pipeline ===", flush=True)
    cleaned_df, audit_report = DataCleaner.clean_dataset(raw_df)
    print(f"Cleaned DataFrame shape: {cleaned_df.shape}", flush=True)
    print(f"Duplicates removed: {audit_report['duplicates_removed']}", flush=True)
    print(f"Missing values handled: {audit_report['missing_values_handled']}", flush=True)

    print("\n=== 3. Testing Database Logging ===", flush=True)
    db_success = db_manager.log_dataset_upload(
        filename="sample_sales_data.csv",
        file_type="CSV",
        raw_rows=audit_report["initial_rows"],
        cleaned_rows=audit_report["final_rows"],
        columns=list(cleaned_df.columns)
    )
    print(f"Database upload log success: {db_success}", flush=True)

    print("\n=== 4. Testing Sales BI Analytics Engine ===", flush=True)
    kpis = SalesAnalyzer.calculate_kpis(cleaned_df)
    print("KPIs:", kpis, flush=True)
    
    monthly_df = SalesAnalyzer.get_monthly_sales(cleaned_df)
    cat_df = SalesAnalyzer.get_category_performance(cleaned_df)
    reg_df = SalesAnalyzer.get_region_performance(cleaned_df)
    prod_dict = SalesAnalyzer.get_product_performance(cleaned_df, top_n=5)
    disc_df = SalesAnalyzer.get_discount_impact(cleaned_df)
    insights = SalesAnalyzer.generate_bi_insights(cleaned_df)

    print("\nGenerated BI Insights:", flush=True)
    for ins in insights:
        print(" -", ins, flush=True)

    print("\n=== 5. Testing Visualization Engine ===", flush=True)
    ChartGenerator.plot_revenue_trend(monthly_df)
    ChartGenerator.plot_category_sales(cat_df)
    ChartGenerator.plot_region_sales(reg_df)
    ChartGenerator.plot_top_products(prod_dict["best"])
    ChartGenerator.plot_category_pie(cat_df)
    ChartGenerator.plot_discount_impact(disc_df)
    print(f"Charts exported to {CHARTS_DIR}", flush=True)

    print("\n=== 6. Testing Report Generation Engine ===", flush=True)
    csv_out = ReportGenerator.export_cleaned_csv(cleaned_df)
    excel_out = ReportGenerator.generate_excel_report(cleaned_df, kpis, monthly_df, cat_df)
    pdf_out = ReportGenerator.generate_pdf_report(cleaned_df, kpis, insights)

    print(f"Cleaned CSV: {csv_out.exists()} ({csv_out})", flush=True)
    print(f"Excel Report: {excel_out.exists()} ({excel_out})", flush=True)
    print(f"PDF Report: {pdf_out.exists()} ({pdf_out})", flush=True)

    print("\n[SUCCESS] Pipeline End-to-End Test PASSED Successfully!", flush=True)

if __name__ == "__main__":
    test_full_pipeline()
