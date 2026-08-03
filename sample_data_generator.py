import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from src.config import DATA_DIR
from src.logger import logger

def generate_sample_sales_data(num_records: int = 1200) -> pd.DataFrame:
    """
    Generates a realistic multi-region enterprise sales dataset.
    """
    logger.info(f"Generating {num_records} sample sales dataset records...")
    
    random.seed(42)
    np.random.seed(42)

    categories_subcategories = {
        "Technology": [
            ("TEC-PH-100", "Smartphones", 499.99),
            ("TEC-LA-200", "Laptops", 899.99),
            ("TEC-MO-300", "Monitors", 249.99),
            ("TEC-AC-400", "Wireless Accessories", 49.99)
        ],
        "Office Supplies": [
            ("OFF-PA-100", "Paper & Stationery", 12.50),
            ("OFF-BI-200", "Binders & Storage", 24.99),
            ("OFF-AR-300", "Art Supplies", 18.00),
            ("OFF-AP-400", "Office Appliances", 129.99)
        ],
        "Furniture": [
            ("FUR-CH-100", "Executive Chairs", 199.99),
            ("FUR-TA-200", "Conference Tables", 450.00),
            ("FUR-BO-300", "Bookcases", 150.00),
            ("FUR-FU-400", "Desk Furnishings", 35.00)
        ]
    }

    regions_cities = {
        "North": ["New York", "Boston", "Philadelphia", "Chicago"],
        "South": ["Atlanta", "Miami", "Dallas", "Houston"],
        "East": ["Washington DC", "Baltimore", "Richmond", "Charlotte"],
        "West": ["Los Angeles", "San Francisco", "Seattle", "Denver"]
    }

    segments = ["Consumer", "Corporate", "Home Office"]
    customer_names = [
        "Liam Smith", "Olivia Johnson", "Noah Williams", "Emma Brown", 
        "James Jones", "Ava Garcia", "William Miller", "Sophia Davis",
        "Benjamin Rodriguez", "Isabella Martinez", "Lucas Hernandez", "Mia Lopez",
        "Henry Gonzalez", "Charlotte Wilson", "Alexander Anderson", "Amelia Thomas"
    ]

    start_date = datetime(2023, 1, 1)
    
    records = []
    for i in range(1, num_records + 1):
        order_id = f"ORD-2023-{i:05d}"
        days_offset = random.randint(0, 500)
        order_date = start_date + timedelta(days=days_offset)
        ship_date = order_date + timedelta(days=random.randint(1, 5))
        
        region = random.choice(list(regions_cities.keys()))
        city = random.choice(regions_cities[region])
        customer_name = random.choice(customer_names)
        customer_id = f"CUST-{hash(customer_name) % 9000 + 1000}"
        segment = random.choice(segments)
        
        category = random.choice(list(categories_subcategories.keys()))
        prod_info = random.choice(categories_subcategories[category])
        product_id, sub_category, base_price = prod_info
        product_name = f"{category} - {sub_category} Model {random.randint(1, 5)}"
        
        quantity = random.randint(1, 10)
        discount = round(random.choice([0.0, 0.05, 0.10, 0.15, 0.20]), 2)
        
        # Calculate raw sales and realistic profit margin
        gross_sales = round(base_price * quantity * (1 - discount), 2)
        margin_pct = random.uniform(0.12, 0.35) if random.random() > 0.10 else -0.05 # Occasional negative profit item
        profit = round(gross_sales * margin_pct, 2)

        records.append({
            "Order ID": order_id,
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Ship Date": ship_date.strftime("%Y-%m-%d"),
            "Customer ID": customer_id,
            "Customer Name": customer_name,
            "Segment": segment,
            "Country": "United States",
            "City": f"  {city}  ", # Intentional spaces to test cleaning engine
            "Region": region,
            "Product ID": product_id,
            "Category": category,
            "Sub-Category": sub_category,
            "Product Name": product_name,
            "Unit Price": base_price,
            "Quantity": quantity,
            "Discount": discount,
            "Sales": gross_sales,
            "Profit": profit
        })

    df = pd.DataFrame(records)
    
    # Introduce 5 duplicate rows to test cleaning module
    duplicates = df.iloc[:5].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Introduce 3 missing values in non-critical columns
    df.loc[12, "Customer Name"] = None
    df.loc[45, "City"] = np.nan

    csv_path = DATA_DIR / "sample_sales_data.csv"
    excel_path = DATA_DIR / "sample_sales_data.xlsx"

    df.to_csv(csv_path, index=False)
    df.to_excel(excel_path, index=False, engine="openpyxl")
    
    logger.info(f"Sample dataset saved to: {csv_path}")
    logger.info(f"Sample dataset saved to: {excel_path}")
    
    return df

if __name__ == "__main__":
    generate_sample_sales_data()
