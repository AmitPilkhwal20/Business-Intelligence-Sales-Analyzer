from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
from src.config import CHARTS_DIR, THEME_COLORS
from src.logger import logger

class ChartGenerator:
    """
    Visualization Engine using Matplotlib and Seaborn.
    Generates high-resolution publication-quality charts and exports PNG files to `charts/`.
    """

    @staticmethod
    def _apply_custom_style(ax: plt.Axes, title: str, xlabel: str, ylabel: str):
        """Applies modern aesthetic styling to Matplotlib axes."""
        ax.set_title(title, fontsize=14, fontweight="bold", pad=15, color="#1A237E")
        ax.set_xlabel(xlabel, fontsize=11, fontweight="bold", labelpad=8, color="#333333")
        ax.set_ylabel(ylabel, fontsize=11, fontweight="bold", labelpad=8, color="#333333")
        ax.grid(True, linestyle="--", alpha=0.5, color="#CCCCCC")
        ax.set_axisbelow(True)
        
        # Format Y-axis as currency if relevant
        if any(term in ylabel.lower() for term in ["revenue", "sales", "profit", "value", "$"]):
            formatter = ticker.FuncFormatter(lambda x, pos: f"${x:,.0f}" if x >= 1000 else f"${x:,.2f}")
            ax.yaxis.set_major_formatter(formatter)

    @classmethod
    def plot_revenue_trend(cls, monthly_df: pd.DataFrame, save_name: str = "revenue_trend.png") -> plt.Figure:
        """Plots Monthly Revenue and Profit Trend line chart."""
        fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
        if monthly_df.empty:
            ax.text(0.5, 0.5, "No Data Available", ha="center", va="center", fontsize=14)
            return fig

        ax.plot(monthly_df["year_month"], monthly_df["revenue"], marker="o", linewidth=2.5, 
                color=THEME_COLORS["primary"], label="Revenue")
        ax.plot(monthly_df["year_month"], monthly_df["profit"], marker="s", linewidth=2.0, 
                color=THEME_COLORS["success"], linestyle="--", label="Profit")
        
        ax.fill_between(monthly_df["year_month"], monthly_df["revenue"], alpha=0.15, color=THEME_COLORS["primary"])
        
        cls._apply_custom_style(ax, "Monthly Revenue & Profit Trends", "Month", "Amount ($)")
        plt.xticks(rotation=45, ha="right", fontsize=9)
        ax.legend(frameon=True, facecolor="white", edgecolor="none")
        plt.tight_layout()

        fig.savefig(CHARTS_DIR / save_name, bbox_inches="tight")
        return fig

    @classmethod
    def plot_category_sales(cls, cat_df: pd.DataFrame, save_name: str = "category_sales.png") -> plt.Figure:
        """Plots Bar chart for Sales by Product Category."""
        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
        if cat_df.empty:
            ax.text(0.5, 0.5, "No Data Available", ha="center", va="center", fontsize=14)
            return fig

        bars = ax.bar(cat_df["category"], cat_df["revenue"], color=THEME_COLORS["palette"][:len(cat_df)], width=0.55)
        cls._apply_custom_style(ax, "Revenue Breakdown by Product Category", "Category", "Revenue ($)")
        
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"${height:,.0f}",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=9, fontweight="bold")

        plt.tight_layout()
        fig.savefig(CHARTS_DIR / save_name, bbox_inches="tight")
        return fig

    @classmethod
    def plot_region_sales(cls, region_df: pd.DataFrame, save_name: str = "region_sales.png") -> plt.Figure:
        """Plots Horizontal Bar chart for Regional Performance."""
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
        if region_df.empty:
            ax.text(0.5, 0.5, "No Data Available", ha="center", va="center", fontsize=14)
            return fig

        bars = ax.barh(region_df["region"], region_df["revenue"], color=THEME_COLORS["secondary"], height=0.55)
        cls._apply_custom_style(ax, "Regional Sales Performance", "Revenue ($)", "Region")
        ax.invert_yaxis()  # Top region on top

        for bar in bars:
            width = bar.get_width()
            ax.annotate(f"${width:,.0f}",
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(6, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=9, fontweight="bold")

        plt.tight_layout()
        fig.savefig(CHARTS_DIR / save_name, bbox_inches="tight")
        return fig

    @classmethod
    def plot_top_products(cls, best_prod_df: pd.DataFrame, save_name: str = "top_products.png") -> plt.Figure:
        """Plots Top 10 Best Selling Products."""
        fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
        if best_prod_df.empty:
            ax.text(0.5, 0.5, "No Data Available", ha="center", va="center", fontsize=14)
            return fig

        prod_col = "product_name" if "product_name" in best_prod_df.columns else best_prod_df.columns[0]
        bars = ax.barh(best_prod_df[prod_col], best_prod_df["revenue"], color=THEME_COLORS["primary"], height=0.6)
        cls._apply_custom_style(ax, "Top 10 Best Selling Products", "Revenue ($)", "Product Name")
        ax.invert_yaxis()

        for bar in bars:
            width = bar.get_width()
            ax.annotate(f"${width:,.0f}",
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(6, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=8, fontweight="bold")

        plt.tight_layout()
        fig.savefig(CHARTS_DIR / save_name, bbox_inches="tight")
        return fig

    @classmethod
    def plot_category_pie(cls, cat_df: pd.DataFrame, save_name: str = "category_pie.png") -> plt.Figure:
        """Plots Donut chart showing Category Revenue share."""
        fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
        if cat_df.empty:
            ax.text(0.5, 0.5, "No Data Available", ha="center", va="center", fontsize=14)
            return fig

        wedges, texts, autotexts = ax.pie(
            cat_df["revenue"],
            labels=cat_df["category"],
            autopct="%1.1f%%",
            startangle=140,
            colors=THEME_COLORS["palette"][:len(cat_df)],
            wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2)
        )
        
        plt.setp(autotexts, size=10, weight="bold", color="white")
        ax.set_title("Revenue Share by Category", fontsize=14, fontweight="bold", pad=15, color="#1A237E")
        plt.tight_layout()
        
        fig.savefig(CHARTS_DIR / save_name, bbox_inches="tight")
        return fig

    @classmethod
    def plot_discount_impact(cls, disc_df: pd.DataFrame, save_name: str = "discount_impact.png") -> plt.Figure:
        """Plots Dual-axis chart for Discount Tiers: Revenue (Bar) & Profit Margin % (Line)."""
        fig, ax1 = plt.subplots(figsize=(9, 5), dpi=300)
        if disc_df.empty:
            ax1.text(0.5, 0.5, "No Data Available", ha="center", va="center", fontsize=14)
            return fig

        ax2 = ax1.twinx()
        
        # Bars for Sales
        bars = ax1.bar(disc_df["discount_tier"].astype(str), disc_df["total_sales"], 
                       color=THEME_COLORS["secondary"], alpha=0.7, width=0.45, label="Total Sales")
        
        # Line for Profit Margin %
        line = ax2.plot(disc_df["discount_tier"].astype(str), disc_df["profit_margin_%"], 
                        color=THEME_COLORS["danger"], marker="o", linewidth=2.5, label="Profit Margin %")

        cls._apply_custom_style(ax1, "Discount Level Impact on Sales & Profit Margin", "Discount Tier", "Total Sales ($)")
        ax2.set_ylabel("Profit Margin (%)", fontsize=11, fontweight="bold", color=THEME_COLORS["danger"], labelpad=8)
        ax2.yaxis.set_major_formatter(ticker.PercentFormatter())
        ax2.grid(False)

        plt.tight_layout()
        fig.savefig(CHARTS_DIR / save_name, bbox_inches="tight")
        return fig
