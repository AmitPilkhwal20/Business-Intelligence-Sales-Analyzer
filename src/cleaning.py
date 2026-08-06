import re
from pathlib import Path
from typing import Tuple, Dict, Any, Union
import pandas as pd
import numpy as np
from src.logger import logger

class DataCleaner:
    """
    Automated Data Validation & Data Cleaning Engine for Sales Datasets.
    Handles CSV/Excel ingestion, column normalization, type casting,
    missing value imputation, duplicate removal, and text trimming.
    """

    @staticmethod
    def standardize_column_name(col_name: str) -> str:
        """Converts column headers to standardized snake_case."""
        col_name = str(col_name).strip()
        col_name = re.sub(r"[^\w\s]", "", col_name) # Remove punctuation
        col_name = re.sub(r"\s+", "_", col_name)     # Replace spaces with underscores
        return col_name.lower()

    @classmethod
    def load_raw_data(cls, file_path_or_buffer: Union[str, Path, Any], filename: str) -> pd.DataFrame:
        """
        Loads raw dataset from file path or uploaded file object (.csv, .xlsx, .xls).
        """
        logger.info(f"Ingesting raw file: {filename}")
        ext = Path(filename).suffix.lower()

        try:
            if ext == ".csv":
                df = pd.read_csv(file_path_or_buffer)
            elif ext in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path_or_buffer, engine="openpyxl")
            else:
                raise ValueError(f"Unsupported file format '{ext}'. Only CSV and Excel files are accepted.")
            
            if df.empty:
                raise ValueError("Uploaded file is empty.")
                
            return df
        except Exception as e:
            logger.error(f"Failed to load file {filename}: {str(e)}")
            raise e

    @classmethod
    def clean_dataset(cls, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Executes automated multi-step data cleaning pipeline.
        Returns cleaned DataFrame and cleaning audit report dictionary.
        """
        logger.info("Executing automated data cleaning pipeline...")
        initial_rows, initial_cols = df.shape
        audit_report = {
            "initial_rows": initial_rows,
            "initial_cols": initial_cols,
            "duplicates_removed": 0,
            "missing_values_handled": 0,
            "columns_standardized": [],
            "date_columns_converted": [],
            "numeric_columns_converted": []
        }

        # Step 1: Standardize Column Names
        original_cols = list(df.columns)
        df.columns = [cls.standardize_column_name(col) for col in df.columns]
        audit_report["columns_standardized"] = list(zip(original_cols, list(df.columns)))

        # Step 2: Remove Exact Duplicate Records
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            df = df.drop_duplicates().reset_index(drop=True)
            logger.info(f"Removed {duplicate_count} duplicate records.")
        audit_report["duplicates_removed"] = int(duplicate_count)

        # Step 3: Trim Whitespace from String/Object Columns
        for col in df.select_dtypes(include=["object", "string"]).columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": np.nan, "None": np.nan, "": np.nan})

        # Step 4: Handle Missing Values
        missing_count_before = df.isna().sum().sum()
        for col in df.columns:
            if df[col].isna().sum() > 0:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna("Unknown")
        audit_report["missing_values_handled"] = int(missing_count_before)

        # Step 5: Detect & Convert Date Columns
        date_candidates = ["order_date", "ship_date", "date", "transaction_date"]
        for col in df.columns:
            if any(candidate in col for candidate in date_candidates) or "date" in col:
                try:
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                    audit_report["date_columns_converted"].append(col)
                except Exception as e:
                    logger.warning(f"Could not convert column '{col}' to datetime: {str(e)}")

        # Step 6: Detect & Convert Numeric Columns (Sales, Profit, Quantity, Discount, Price)
        numeric_keywords = ["sales", "profit", "quantity", "discount", "price", "unit_price", "amount", "revenue"]
        for col in df.columns:
            if any(kw in col for kw in numeric_keywords):
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
                    audit_report["numeric_columns_converted"].append(col)
                except Exception as e:
                    logger.warning(f"Could not convert column '{col}' to numeric: {str(e)}")

        final_rows, final_cols = df.shape
        audit_report["final_rows"] = final_rows
        audit_report["final_cols"] = final_cols

        logger.info(f"Data cleaning complete. Cleaned shape: {final_rows} rows x {final_cols} columns.")
        return df, audit_report
