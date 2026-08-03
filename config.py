import os
from pathlib import Path

# Base Directory (Project Root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Application Directory Structure
DATA_DIR = BASE_DIR / "data"
CLEANED_DATA_DIR = BASE_DIR / "cleaned_data"
DATABASE_DIR = BASE_DIR / "database"
REPORTS_DIR = BASE_DIR / "reports"
CHARTS_DIR = BASE_DIR / "charts"
ASSETS_DIR = BASE_DIR / "assets"
LOGS_DIR = BASE_DIR / "logs"

# Ensure all directories exist
for directory in [DATA_DIR, CLEANED_DATA_DIR, DATABASE_DIR, REPORTS_DIR, CHARTS_DIR, ASSETS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database Configuration Defaults
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "sales_bi_db"),
}

# SQLite Fallback Path
SQLITE_DB_PATH = DATABASE_DIR / "sales_bi_fallback.db"

# Professional Theme Color Palette for Charts & UI
THEME_COLORS = {
    "primary": "#1E88E5",      # Deep Royal Blue
    "secondary": "#00ACC1",    # Cyan / Teal Accent
    "success": "#4CAF50",      # Vibrant Green
    "warning": "#FFB300",      # Amber Yellow
    "danger": "#E53935",       # Crimson Red
    "dark": "#1A237E",         # Indigo Dark
    "background": "#F4F6F9",   # Neutral Soft Background
    "palette": ["#1E88E5", "#00ACC1", "#4CAF50", "#FFB300", "#AB47BC", "#FF7043", "#26A69A", "#5C6BC0"]
}
