import sqlite3
import pandas as pd

DB_PATH = "food_waste.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def setup_database():
    conn = get_connection()

    for table, file in [
        ("providers", "data/providers_data.csv"),
        ("receivers", "data/receivers_data.csv"),
        ("food_listings", "data/food_listings_data.csv"),
        ("claims", "data/claims_data.csv")
    ]:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        df.to_sql(table, conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

QUERIES = {
    "Q1: Providers & Receivers per City": """
        SELECT p.City,
               COUNT(DISTINCT p.Provider_ID) AS Providers,
               COUNT(DISTINCT r.Receiver_ID) AS Receivers
        FROM providers p
        LEFT JOIN receivers r ON p.City = r.City
        GROUP BY p.City ORDER BY Providers DESC LIMIT 15
    """,
    "Q2: Provider Type with Most Food": """
        SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
        FROM food_listings
        GROUP BY Provider_Type ORDER BY Total_Quantity DESC
    """,
    "Q3: Contact Info of Providers by City": """
        SELECT Name, Type, City, Contact, Address
        FROM providers ORDER BY City LIMIT 50
    """,
    "Q4: Receivers Who Claimed the Most Food": """
        SELECT r.Name, r.Type, r.City, COUNT(c.Claim_ID) AS Total_Claims
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        GROUP BY r.Receiver_ID ORDER BY Total_Claims DESC LIMIT 10
    """,
    "Q5: Total Quantity of Food Available": """
        SELECT SUM(Quantity) AS Total_Food_Available FROM food_listings
    """,
    "Q6: City with Highest Food Listings": """
        SELECT Location AS City, COUNT(*) AS Listings, SUM(Quantity) AS Total_Qty
        FROM food_listings
        GROUP BY Location ORDER BY Listings DESC LIMIT 15
    """,
    "Q7: Most Common Food Types": """
        SELECT Food_Type, COUNT(*) AS Count, SUM(Quantity) AS Total_Qty
        FROM food_listings
        GROUP BY Food_Type ORDER BY Count DESC
    """,
    "Q8: Claims Per Food Item": """
        SELECT f.Food_Name, f.Food_Type, f.Meal_Type,
               COUNT(c.Claim_ID) AS Total_Claims
        FROM food_listings f
        LEFT JOIN claims c ON f.Food_ID = c.Food_ID
        GROUP BY f.Food_ID ORDER BY Total_Claims DESC LIMIT 15
    """,
    "Q9: Provider with Most Successful Claims": """
        SELECT p.Name, p.Type, p.City,
               COUNT(c.Claim_ID) AS Successful_Claims
        FROM providers p
        JOIN food_listings f ON p.Provider_ID = f.Provider_ID
        JOIN claims c ON f.Food_ID = c.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Provider_ID ORDER BY Successful_Claims DESC LIMIT 10
    """,
    "Q10: Claim Status Percentage": """
        SELECT Status,
               COUNT(*) AS Count,
               ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM claims), 2) AS Percentage
        FROM claims GROUP BY Status
    """,
    "Q11: Avg Quantity Claimed per Receiver": """
        SELECT r.Name, r.Type,
               ROUND(AVG(f.Quantity), 2) AS Avg_Qty_Claimed
        FROM receivers r
        JOIN claims c ON r.Receiver_ID = c.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY r.Receiver_ID ORDER BY Avg_Qty_Claimed DESC LIMIT 10
    """,
    "Q12: Most Claimed Meal Type": """
        SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Times_Claimed
        FROM food_listings f
        JOIN claims c ON f.Food_ID = c.Food_ID
        GROUP BY f.Meal_Type ORDER BY Times_Claimed DESC
    """,
    "Q13: Total Food Donated per Provider": """
        SELECT p.Name, p.Type, p.City,
               SUM(f.Quantity) AS Total_Donated
        FROM providers p
        JOIN food_listings f ON p.Provider_ID = f.Provider_ID
        GROUP BY p.Provider_ID ORDER BY Total_Donated DESC LIMIT 10
    """,
    "Q14: Food Expiring Soon (within 30 days from earliest date)": """
        SELECT Food_Name, Quantity, Expiry_Date, Location, Food_Type
        FROM food_listings
        ORDER BY Expiry_Date ASC LIMIT 20
    """,
    "Q15: Monthly Claim Trends": """
        SELECT SUBSTR(Timestamp, 1, 7) AS Month,
               COUNT(*) AS Total_Claims,
               SUM(CASE WHEN Status='Completed' THEN 1 ELSE 0 END) AS Completed,
               SUM(CASE WHEN Status='Pending' THEN 1 ELSE 0 END) AS Pending,
               SUM(CASE WHEN Status='Cancelled' THEN 1 ELSE 0 END) AS Cancelled
        FROM claims
        GROUP BY Month ORDER BY Month
    """
}

def run_query(query):
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    setup_database()
    print("DB ready!")
    for title, q in QUERIES.items():
        print(f"\n{title}")
        print(run_query(q).to_string(index=False))