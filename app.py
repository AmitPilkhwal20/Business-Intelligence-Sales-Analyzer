import os
from pathlib import Path
import streamlit as st
import pandas as pd

# Page Configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Business Intelligence Sales Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.config import DATA_DIR, THEME_COLORS
from src.logger import logger
from src.cleaning import DataCleaner
from src.database import db_manager
from src.analysis import SalesAnalyzer
from src.visualization import ChartGenerator
from src.report_generator import ReportGenerator

# Custom CSS for Modern UI & Custom Styling
st.markdown("""
    <style>
    /* Main Background & Font Settings */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* KPI Card Box Styling */
    .kpi-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F4F6F9 100%);
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 5px solid #1E88E5;
        margin-bottom: 15px;
    }
    .kpi-title {
        font-size: 13px;
        font-weight: 700;
        color: #6C757D;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 800;
        color: #1A237E;
    }
    .kpi-subtext {
        font-size: 12px;
        font-weight: 600;
        margin-top: 4px;
    }
    .success-sub { color: #2E7D32; }
    .primary-sub { color: #1E88E5; }

    /* Custom BI Insight Box */
    .bi-insight-box {
        background-color: #E3F2FD;
        border-left: 5px solid #1E88E5;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .bi-insight-title {
        font-size: 16px;
        font-weight: 800;
        color: #0D47A1;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    st.sidebar.image("https://img.icons8.com/color/96/combo-chart.png", width=70)
    st.sidebar.title("BI Sales Analyzer")
    st.sidebar.caption("Enterprise Analytics & Reporting Platform")
    st.sidebar.markdown("---")

    # 1. Dataset Selection / Upload Section
    st.sidebar.header("📁 Data Source")
    data_option = st.sidebar.radio("Select Data Input:", ["Use Sample Dataset", "Upload Custom File"])
    
    raw_df = None
    file_name = "sample_sales_data.csv"

    if data_option == "Use Sample Dataset":
        sample_path = DATA_DIR / "sample_sales_data.csv"
        if not sample_path.exists():
            from sample_data_generator import generate_sample_sales_data
            generate_sample_sales_data()
        
        raw_df = DataCleaner.load_raw_data(sample_path, "sample_sales_data.csv")
    else:
        uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx", "xls"])
        if uploaded_file is not None:
            file_name = uploaded_file.name
            raw_df = DataCleaner.load_raw_data(uploaded_file, file_name)

    if raw_df is None or raw_df.empty:
        st.warning("Please upload a sales dataset or select the sample dataset to begin analysis.")
        return

    # 2. Data Cleaning Execution
    cleaned_df, audit_report = DataCleaner.clean_dataset(raw_df)
    
    # Log metadata to DB
    db_manager.log_dataset_upload(
        filename=file_name,
        file_type=Path(file_name).suffix.upper(),
        raw_rows=audit_report["initial_rows"],
        cleaned_rows=audit_report["final_rows"],
        columns=list(cleaned_df.columns)
    )

    # 3. Interactive Filter Panel in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Global Filters")

    filtered_df = cleaned_df.copy()

    # Filter: Year
    if "order_date" in filtered_df.columns:
        years = sorted(filtered_df["order_date"].dt.year.dropna().unique())
        selected_years = st.sidebar.multiselect("Select Year(s)", options=years, default=years)
        if selected_years:
            filtered_df = filtered_df[filtered_df["order_date"].dt.year.isin(selected_years)]

    # Filter: Region
    if "region" in filtered_df.columns:
        regions = sorted(filtered_df["region"].dropna().unique())
        selected_regions = st.sidebar.multiselect("Select Region(s)", options=regions, default=regions)
        if selected_regions:
            filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]

    # Filter: Category
    if "category" in filtered_df.columns:
        categories = sorted(filtered_df["category"].dropna().unique())
        selected_categories = st.sidebar.multiselect("Select Category(ies)", options=categories, default=categories)
        if selected_categories:
            filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

    # DB Connection Status Indicator
    st.sidebar.markdown("---")
    db_status = "MySQL Server" if db_manager.use_mysql else "SQLite (Fallback)"
    st.sidebar.info(f"🟢 **Database Engine**: {db_status}")

    # 4. Main Dashboard Header
    st.title("📈 Business Intelligence Sales Analyzer")
    st.markdown(f"**Dataset**: `{file_name}` | **Filtered Records**: `{len(filtered_df):,}` / `{len(cleaned_df):,}`")

    # 5. Core KPIs Calculation
    kpis = SalesAnalyzer.calculate_kpis(filtered_df)
    db_manager.log_analysis(file_name, kpis)

    # 6. Tab Navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Overview",
        "📈 Sales & Trend Analytics",
        "🔍 Data Cleaning Audit",
        "📥 Export Reports",
        "📜 System & DB History"
    ])

    # -------------------------------------------------------------
    # TAB 1: EXECUTIVE OVERVIEW
    # -------------------------------------------------------------
    with tab1:
        st.subheader("Key Performance Indicators")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-title">Total Revenue</div>
                    <div class="kpi-value">${kpis['total_revenue']:,.2f}</div>
                    <div class="kpi-subtext primary-sub">Gross Sales</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="kpi-card" style="border-left-color: #4CAF50;">
                    <div class="kpi-title">Total Profit</div>
                    <div class="kpi-value">${kpis['total_profit']:,.2f}</div>
                    <div class="kpi-subtext success-sub">Net Profit</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="kpi-card" style="border-left-color: #00ACC1;">
                    <div class="kpi-title">Total Orders</div>
                    <div class="kpi-value">{kpis['total_orders']:,}</div>
                    <div class="kpi-subtext primary-sub">Completed Orders</div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div class="kpi-card" style="border-left-color: #FFB300;">
                    <div class="kpi-title">Avg Order Value</div>
                    <div class="kpi-value">${kpis['avg_order_value']:,.2f}</div>
                    <div class="kpi-subtext primary-sub">AOV per Transaction</div>
                </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
                <div class="kpi-card" style="border-left-color: #AB47BC;">
                    <div class="kpi-title">Profit Margin</div>
                    <div class="kpi-value">{kpis['profit_margin']}%</div>
                    <div class="kpi-subtext success-sub">Overall Margin</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Automated BI Narrative Insights
        st.subheader("💡 Business Intelligence Executive Insights")
        bi_insights = SalesAnalyzer.generate_bi_insights(filtered_df)
        
        insight_html = "<div class='bi-insight-box'>"
        for insight in bi_insights:
            formatted_insight = insight.replace("**", "<b>", 1).replace("**", "</b>", 1)
            insight_html += f"<p style='margin-bottom:6px; font-size:14px; color:#1565C0;'>• {formatted_insight}</p>"
        insight_html += "</div>"
        st.markdown(insight_html, unsafe_allow_html=True)

        # Main Charts Grid
        c1, c2 = st.columns([6, 4])
        with c1:
            monthly_df = SalesAnalyzer.get_monthly_sales(filtered_df)
            fig_trend = ChartGenerator.plot_revenue_trend(monthly_df)
            st.pyplot(fig_trend)

        with c2:
            cat_df = SalesAnalyzer.get_category_performance(filtered_df)
            fig_pie = ChartGenerator.plot_category_pie(cat_df)
            st.pyplot(fig_pie)

    # -------------------------------------------------------------
    # TAB 2: SALES & TREND ANALYTICS
    # -------------------------------------------------------------
    with tab2:
        st.subheader("Multi-Dimensional Business Performance")
        
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            cat_df = SalesAnalyzer.get_category_performance(filtered_df)
            fig_cat = ChartGenerator.plot_category_sales(cat_df)
            st.pyplot(fig_cat)

        with row1_col2:
            reg_df = SalesAnalyzer.get_region_performance(filtered_df)
            fig_reg = ChartGenerator.plot_region_sales(reg_df)
            st.pyplot(fig_reg)

        row2_col1, row2_col2 = st.columns(2)
        with row2_col1:
            prod_dict = SalesAnalyzer.get_product_performance(filtered_df, top_n=10)
            fig_prod = ChartGenerator.plot_top_products(prod_dict["best"])
            st.pyplot(fig_prod)

        with row2_col2:
            disc_df = SalesAnalyzer.get_discount_impact(filtered_df)
            fig_disc = ChartGenerator.plot_discount_impact(disc_df)
            st.pyplot(fig_disc)

    # -------------------------------------------------------------
    # TAB 3: DATA CLEANING AUDIT
    # -------------------------------------------------------------
    with tab3:
        st.subheader("Automated Data Cleaning Audit Log")
        
        ac1, ac2, ac3, ac4 = st.columns(4)
        ac1.metric("Raw Rows", audit_report["initial_rows"])
        ac2.metric("Cleaned Rows", audit_report["final_rows"])
        ac3.metric("Duplicates Removed", audit_report["duplicates_removed"])
        ac4.metric("Missing Values Imputed", audit_report["missing_values_handled"])

        st.markdown("---")
        st.subheader("Standardized Column Mapping")
        cols_df = pd.DataFrame(audit_report["columns_standardized"], columns=["Original Column", "Standardized snake_case"])
        st.dataframe(cols_df, use_container_width=True)

        st.markdown("---")
        st.subheader("Interactive Cleaned Dataset Explorer")
        search_query = st.text_input("Search Dataset", placeholder="Filter by product, region, customer...")
        
        display_df = cleaned_df.copy()
        if search_query:
            mask = display_df.astype(str).apply(lambda row: row.str.contains(search_query, case=False).any(), axis=1)
            display_df = display_df[mask]

        st.dataframe(display_df, use_container_width=True, height=400)

    # -------------------------------------------------------------
    # TAB 4: EXPORT REPORTS
    # -------------------------------------------------------------
    with tab4:
        st.subheader("Download Production Reports")
        st.write("Generate and download executive reports in CSV, Excel, and PDF formats.")

        monthly_df = SalesAnalyzer.get_monthly_sales(filtered_df)
        cat_df = SalesAnalyzer.get_category_performance(filtered_df)

        r_col1, r_col2, r_col3 = st.columns(3)

        # 1. CSV Download
        with r_col1:
            st.markdown("### 📄 Cleaned CSV")
            csv_path = ReportGenerator.export_cleaned_csv(filtered_df)
            with open(csv_path, "rb") as f:
                st.download_button(
                    label="Download Cleaned CSV",
                    data=f.read(),
                    file_name="cleaned_sales_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        # 2. Excel Download
        with r_col2:
            st.markdown("### 📊 Styled Excel Report")
            excel_path = ReportGenerator.generate_excel_report(filtered_df, kpis, monthly_df, cat_df)
            with open(excel_path, "rb") as f:
                st.download_button(
                    label="Download Excel Report (.xlsx)",
                    data=f.read(),
                    file_name="Sales_BI_Executive_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

        # 3. PDF Download
        with r_col3:
            st.markdown("### 📑 Executive PDF Summary")
            pdf_path = ReportGenerator.generate_pdf_report(filtered_df, kpis, bi_insights)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download Executive PDF Report",
                    data=f.read(),
                    file_name="Sales_BI_Executive_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

    # -------------------------------------------------------------
    # TAB 5: SYSTEM & DATABASE HISTORY
    # -------------------------------------------------------------
    with tab5:
        st.subheader("Database Metadata & Report Logs")
        
        hist_tab1, hist_tab2 = st.tabs(["Uploaded Datasets Log", "Generated Reports Log"])
        
        with hist_tab1:
            recent_uploads = db_manager.get_recent_uploads()
            if recent_uploads:
                st.dataframe(pd.DataFrame(recent_uploads), use_container_width=True)
            else:
                st.info("No upload history recorded yet.")

        with hist_tab2:
            recent_reports = db_manager.get_recent_reports()
            if recent_reports:
                st.dataframe(pd.DataFrame(recent_reports), use_container_width=True)
            else:
                st.info("No report history recorded yet.")

if __name__ == "__main__":
    main()
