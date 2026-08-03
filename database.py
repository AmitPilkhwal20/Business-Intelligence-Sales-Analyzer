import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional
import mysql.connector
from src.config import DB_CONFIG, SQLITE_DB_PATH
from src.logger import logger

class DatabaseManager:
    """
    Database Manager for storing dataset metadata, analysis history,
    and report logs. Uses MySQL when available and falls back to SQLite seamlessly.
    """

    def __init__(self):
        self.use_mysql = False
        self._init_db()

    def get_mysql_connection(self):
        """Attempts to connect to MySQL database."""
        try:
            conn = mysql.connector.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"]
            )
            if conn.is_connected():
                return conn
        except Exception:
            return None
        return None

    def get_sqlite_connection(self):
        """Returns SQLite database connection."""
        return sqlite3.connect(SQLITE_DB_PATH)

    def _init_db(self):
        """Initializes database schema in MySQL or SQLite fallback."""
        mysql_conn = self.get_mysql_connection()
        if mysql_conn:
            self.use_mysql = True
            mysql_conn.close()
            logger.info("Database Manager connected to MySQL database.")
            return

        logger.info("MySQL connection unavailable. Initializing SQLite fallback database...")
        self.use_mysql = False
        conn = self.get_sqlite_connection()
        cursor = conn.cursor()

        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS uploaded_datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_type TEXT NOT NULL,
                upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                raw_row_count INTEGER NOT NULL,
                cleaned_row_count INTEGER NOT NULL,
                columns_list TEXT,
                status TEXT DEFAULT 'Cleaned'
            );

            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_name TEXT NOT NULL,
                analysis_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_revenue REAL,
                total_profit REAL,
                total_orders INTEGER,
                avg_order_value REAL,
                profit_margin REAL,
                top_region TEXT,
                top_category TEXT,
                top_product TEXT
            );

            CREATE TABLE IF NOT EXISTS report_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_name TEXT NOT NULL,
                report_type TEXT NOT NULL,
                generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                file_path TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS application_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_level TEXT NOT NULL,
                module_name TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()
        logger.info("SQLite fallback tables initialized successfully.")

    def log_dataset_upload(self, filename: str, file_type: str, raw_rows: int, cleaned_rows: int, columns: List[str]) -> bool:
        """Logs uploaded dataset metadata to database."""
        cols_json = json.dumps(columns)
        try:
            if self.use_mysql:
                conn = self.get_mysql_connection()
                if conn:
                    cursor = conn.cursor()
                    query = """
                        INSERT INTO uploaded_datasets (filename, file_type, raw_row_count, cleaned_row_count, columns_list)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (filename, file_type, raw_rows, cleaned_rows, cols_json))
                    conn.commit()
                    conn.close()
                    return True

            # SQLite fallback
            conn = self.get_sqlite_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO uploaded_datasets (filename, file_type, raw_row_count, cleaned_row_count, columns_list)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (filename, file_type, raw_rows, cleaned_rows, cols_json))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error logging dataset upload: {str(e)}")
            return False

    def log_analysis(self, dataset_name: str, kpis: Dict[str, Any]) -> bool:
        """Logs analysis execution metrics to database."""
        try:
            params = (
                dataset_name,
                float(kpis.get("total_revenue", 0.0)),
                float(kpis.get("total_profit", 0.0)),
                int(kpis.get("total_orders", 0)),
                float(kpis.get("avg_order_value", 0.0)),
                float(kpis.get("profit_margin", 0.0)),
                str(kpis.get("top_region", "N/A")),
                str(kpis.get("top_category", "N/A")),
                str(kpis.get("top_product", "N/A"))
            )

            if self.use_mysql:
                conn = self.get_mysql_connection()
                if conn:
                    cursor = conn.cursor()
                    query = """
                        INSERT INTO analysis_history 
                        (dataset_name, total_revenue, total_profit, total_orders, avg_order_value, profit_margin, top_region, top_category, top_product)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, params)
                    conn.commit()
                    conn.close()
                    return True

            conn = self.get_sqlite_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO analysis_history 
                (dataset_name, total_revenue, total_profit, total_orders, avg_order_value, profit_margin, top_region, top_category, top_product)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error logging analysis history: {str(e)}")
            return False

    def log_report(self, report_name: str, report_type: str, file_path: str) -> bool:
        """Logs generated report to database."""
        try:
            if self.use_mysql:
                conn = self.get_mysql_connection()
                if conn:
                    cursor = conn.cursor()
                    query = "INSERT INTO report_history (report_name, report_type, file_path) VALUES (%s, %s, %s)"
                    cursor.execute(query, (report_name, report_type, file_path))
                    conn.commit()
                    conn.close()
                    return True

            conn = self.get_sqlite_connection()
            cursor = conn.cursor()
            query = "INSERT INTO report_history (report_name, report_type, file_path) VALUES (?, ?, ?)"
            cursor.execute(query, (report_name, report_type, file_path))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error logging report generation: {str(e)}")
            return False

    def get_recent_uploads(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves recent dataset upload logs."""
        try:
            conn = self.get_sqlite_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, filename, file_type, upload_timestamp, raw_row_count, cleaned_row_count, status FROM uploaded_datasets ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            conn.close()
            return [
                {
                    "id": r[0], "filename": r[1], "file_type": r[2],
                    "timestamp": r[3], "raw_rows": r[4], "cleaned_rows": r[5], "status": r[6]
                } for r in rows
            ]
        except Exception as e:
            logger.error(f"Error fetching dataset history: {str(e)}")
            return []

    def get_recent_reports(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves recent report generation logs."""
        try:
            conn = self.get_sqlite_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, report_name, report_type, generated_at, file_path FROM report_history ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            conn.close()
            return [
                {
                    "id": r[0], "name": r[1], "type": r[2], "generated_at": r[3], "path": r[4]
                } for r in rows
            ]
        except Exception as e:
            logger.error(f"Error fetching report history: {str(e)}")
            return []

# Shared Database Manager instance
db_manager = DatabaseManager()
