from typing import Dict, Any, List
import pandas as pd
import numpy as np
from src.logger import logger

class SalesAnalyzer:
    """
    Business Intelligence Analytics Engine.
    Computes key performance indicators (KPIs), multi-dimensional breakdowns,
    customer analytics, and automated natural language executive insights.
    """

    @staticmethod
    def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates core business KPIs."""
        if df.empty:
            return {
                "total_revenue": 0.0, "total_profit": 0.0, "total_orders": 0,
                "avg_order_value": 0.0, "avg_profit": 0.0, "profit_margin": 0.0,
                "top_region": "N/A", "top_category": "N/A", "top_product": "N/A"
            }

        sales_col = "sales" if "sales" in df.columns else df.select_dtypes(include=[np.number]).columns[0]
        profit_col = "profit" if "profit" in df.columns else sales_col
        order_col = "order_id" if "order_id" in df.columns else df.columns[0]

        total_revenue = float(df[sales_col].sum())
        total_profit = float(df[profit_col].sum())
        total_orders = int(df[order_col].nunique()) if order_col in df.columns else len(df)
        
        avg_order_value = round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0
        avg_profit = round(total_profit / total_orders, 2) if total_orders > 0 else 0.0
        profit_margin = round((total_profit / total_revenue) * 100, 2) if total_revenue > 0 else 0.0

        # Top Performers
        top_region = df.groupby("region")[sales_col].sum().idxmax() if "region" in df.columns else "N/A"
        top_category = df.groupby("category")[sales_col].sum().idxmax() if "category" in df.columns else "N/A"
        top_product = df.groupby("product_name")[sales_col].sum().idxmax() if "product_name" in df.columns else "N/A"

        return {
            "total_revenue": round(total_revenue, 2),
            "total_profit": round(total_profit, 2),
            "total_orders": total_orders,
            "avg_order_value": avg_order_value,
            "avg_profit": avg_profit,
            "profit_margin": profit_margin,
            "top_region": top_region,
            "top_category": top_category,
            "top_product": top_product
        }

    @staticmethod
    def get_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
        """Computes sales trends grouped by Year-Month."""
        if "order_date" not in df.columns or df.empty:
            return pd.DataFrame()

        temp_df = df.copy()
        temp_df["year_month"] = temp_df["order_date"].dt.to_period("M").astype(str)
        monthly = temp_df.groupby("year_month").agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique") if "order_id" in temp_df.columns else ("sales", "count")
        ).reset_index()
        return monthly

    @staticmethod
    def get_quarterly_sales(df: pd.DataFrame) -> pd.DataFrame:
        """Computes sales trends grouped by Quarter."""
        if "order_date" not in df.columns or df.empty:
            return pd.DataFrame()

        temp_df = df.copy()
        temp_df["quarter"] = temp_df["order_date"].dt.to_period("Q").astype(str)
        quarterly = temp_df.groupby("quarter").agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique") if "order_id" in temp_df.columns else ("sales", "count")
        ).reset_index()
        return quarterly

    @staticmethod
    def get_category_performance(df: pd.DataFrame) -> pd.DataFrame:
        """Computes revenue, profit, and profit margin by Category."""
        if "category" not in df.columns or df.empty:
            return pd.DataFrame()

        cat_perf = df.groupby("category").agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            items_sold=("quantity", "sum") if "quantity" in df.columns else ("sales", "count")
        ).reset_index()

        cat_perf["profit_margin_%"] = np.where(
            cat_perf["revenue"] > 0,
            (cat_perf["profit"] / cat_perf["revenue"]) * 100,
            0.0
        ).round(2)

        return cat_perf.sort_values(by="revenue", ascending=False)

    @staticmethod
    def get_region_performance(df: pd.DataFrame) -> pd.DataFrame:
        """Computes performance grouped by Region."""
        if "region" not in df.columns or df.empty:
            return pd.DataFrame()

        region_perf = df.groupby("region").agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique") if "order_id" in df.columns else ("sales", "count")
        ).reset_index()

        region_perf["profit_margin_%"] = np.where(
            region_perf["revenue"] > 0,
            (region_perf["profit"] / region_perf["revenue"]) * 100,
            0.0
        ).round(2)

        return region_perf.sort_values(by="revenue", ascending=False)

    @staticmethod
    def get_product_performance(df: pd.DataFrame, top_n: int = 10) -> Dict[str, pd.DataFrame]:
        """Identifies Best and Worst performing products by Sales & Profit."""
        prod_col = "product_name" if "product_name" in df.columns else "product_id"
        if prod_col not in df.columns or df.empty:
            return {"best": pd.DataFrame(), "worst": pd.DataFrame()}

        prod_perf = df.groupby(prod_col).agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            units_sold=("quantity", "sum") if "quantity" in df.columns else ("sales", "count")
        ).reset_index()

        best_products = prod_perf.sort_values(by="revenue", ascending=False).head(top_n)
        worst_products = prod_perf.sort_values(by="revenue", ascending=True).head(top_n)

        return {"best": best_products, "worst": worst_products}

    @staticmethod
    def get_customer_segmentation(df: pd.DataFrame) -> pd.DataFrame:
        """Segments customers based on total spend."""
        cust_col = "customer_name" if "customer_name" in df.columns else "customer_id"
        if cust_col not in df.columns or df.empty:
            return pd.DataFrame()

        cust_df = df.groupby([cust_col, "segment"] if "segment" in df.columns else [cust_col]).agg(
            total_spend=("sales", "sum"),
            total_orders=("order_id", "nunique") if "order_id" in df.columns else ("sales", "count"),
            total_profit=("profit", "sum")
        ).reset_index()

        # Define spend tiers
        q75 = cust_df["total_spend"].quantile(0.75) if len(cust_df) > 4 else 1000.0
        q25 = cust_df["total_spend"].quantile(0.25) if len(cust_df) > 4 else 300.0

        def assign_tier(spend):
            if spend >= q75:
                return "VIP / High Value"
            elif spend >= q25:
                return "Medium Value"
            return "Standard Value"

        cust_df["tier"] = cust_df["total_spend"].apply(assign_tier)
        return cust_df.sort_values(by="total_spend", ascending=False)

    @staticmethod
    def get_discount_impact(df: pd.DataFrame) -> pd.DataFrame:
        """Analyzes impact of discount levels on sales volume and profit margin."""
        if "discount" not in df.columns or df.empty:
            return pd.DataFrame()

        temp = df.copy()
        temp["discount_tier"] = pd.cut(
            temp["discount"],
            bins=[-0.01, 0.0, 0.10, 0.20, 0.50, 1.0],
            labels=["0% (No Discount)", "1-10%", "11-20%", "21-50%", ">50%"]
        )

        disc_analysis = temp.groupby("discount_tier", observed=False).agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            order_count=("sales", "count")
        ).reset_index()

        disc_analysis["profit_margin_%"] = np.where(
            disc_analysis["total_sales"] > 0,
            (disc_analysis["total_profit"] / disc_analysis["total_sales"]) * 100,
            0.0
        ).round(2)

        return disc_analysis

    @classmethod
    def generate_bi_insights(cls, df: pd.DataFrame) -> List[str]:
        """
        Generates automated, dynamic executive BI narrative insights.
        """
        if df.empty:
            return ["No data available to generate business insights."]

        insights = []
        kpis = cls.calculate_kpis(df)
        
        # Insight 1: Overall Financial Health
        insights.append(
            f"**Executive Overview**: The business achieved a Total Revenue of **${kpis['total_revenue']:,.2f}** "
            f"with a Net Profit of **${kpis['total_profit']:,.2f}** across **{kpis['total_orders']:,}** orders, "
            f"yielding an overall profit margin of **{kpis['profit_margin']}%**."
        )

        # Insight 2: Peak Revenue Period
        monthly = cls.get_monthly_sales(df)
        if not monthly.empty:
            peak_month_row = monthly.loc[monthly["revenue"].idxmax()]
            insights.append(
                f"**Peak Performance Month**: **{peak_month_row['year_month']}** generated the highest monthly revenue of "
                f"**${peak_month_row['revenue']:,.2f}** with **${peak_month_row['profit']:,.2f}** in profit."
            )

        # Insight 3: Category Performance
        cat_perf = cls.get_category_performance(df)
        if not cat_perf.empty:
            top_cat = cat_perf.iloc[0]
            lowest_cat = cat_perf.iloc[-1]
            insights.append(
                f"**Category Leadership**: **{top_cat['category']}** is the top-performing category contributing "
                f"**${top_cat['revenue']:,.2f}** in revenue ({top_cat['profit_margin_%']}% margin). "
                f"Conversely, **{lowest_cat['category']}** is the lowest performing category with **${lowest_cat['revenue']:,.2f}**."
            )

        # Insight 4: Regional Distribution
        region_perf = cls.get_region_performance(df)
        if not region_perf.empty:
            top_reg = region_perf.iloc[0]
            insights.append(
                f"**Regional Dominance**: The **{top_reg['region']}** region leads sales performance with "
                f"**${top_reg['revenue']:,.2f}** revenue and **${top_reg['profit']:,.2f}** profit."
            )

        # Insight 5: Discount Impact Warning/Optimization
        disc_analysis = cls.get_discount_impact(df)
        if not disc_analysis.empty:
            zero_disc = disc_analysis[disc_analysis["discount_tier"] == "0% (No Discount)"]
            high_disc = disc_analysis[disc_analysis["discount_tier"] == "11-20%"]
            if not zero_disc.empty and not high_disc.empty:
                z_margin = zero_disc["profit_margin_%"].values[0]
                h_margin = high_disc["profit_margin_%"].values[0]
                insights.append(
                    f"**Discount Impact Analysis**: Sales with 0% discount maintain a **{z_margin}%** profit margin, "
                    f"whereas 11-20% discounts adjust profit margins to **{h_margin}%**. Optimizing promotional discounting is recommended."
                )

        return insights
