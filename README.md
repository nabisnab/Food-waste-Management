# 🍱 Local Food Wastage Management System

A data-driven web application built with **Python**, **SQL (SQLite)**, and **Streamlit** that connects surplus food providers to those in need — reducing food waste and fighting food insecurity.

---

## 📌 Problem Statement

Every day, restaurants, supermarkets, and households discard surplus food while many people struggle with food insecurity. This system provides a structured platform to:

- Allow food providers to list surplus food
- Allow NGOs and individuals to claim available food
- Store and analyze all data using SQL
- Visualize trends and insights through an interactive web app

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core logic and data processing |
| SQLite (via `sqlite3`) | Database storage and SQL queries |
| Pandas | Data loading and manipulation |
| Streamlit | Web application interface |
| Plotly | Interactive charts and visualizations |

---

## 📁 Project Structure

```
food_project/
│
├── app.py               # Main Streamlit application
├── database.py          # Database setup and all 15 SQL queries
│
├── data/
│   ├── providers_data.csv
│   ├── receivers_data.csv
│   ├── food_listings_data.csv
│   └── claims_data.csv
│
└── food_waste.db        # Auto-generated SQLite database
```

---

## 📊 Dataset Description

### 1. Providers (`providers_data.csv`)
Food donors — restaurants, grocery stores, supermarkets, catering services.

| Column | Type | Description |
|---|---|---|
| Provider_ID | Integer | Unique identifier |
| Name | String | Name of the provider |
| Type | String | Restaurant / Grocery Store / Supermarket / Catering Service |
| Address | String | Physical address |
| City | String | City of the provider |
| Contact | String | Phone number |

### 2. Receivers (`receivers_data.csv`)
Food recipients — NGOs, shelters, charities, individuals.

| Column | Type | Description |
|---|---|---|
| Receiver_ID | Integer | Unique identifier |
| Name | String | Name of the receiver |
| Type | String | NGO / Shelter / Charity / Individual |
| City | String | City of the receiver |
| Contact | String | Phone number |

### 3. Food Listings (`food_listings_data.csv`)
Available food items listed by providers.

| Column | Type | Description |
|---|---|---|
| Food_ID | Integer | Unique identifier |
| Food_Name | String | Name of the food item |
| Quantity | Integer | Available quantity |
| Expiry_Date | Date | Expiry date of the food |
| Provider_ID | Integer | Reference to the provider |
| Provider_Type | String | Type of provider |
| Location | String | City where food is available |
| Food_Type | String | Vegetarian / Non-Vegetarian / Vegan |
| Meal_Type | String | Breakfast / Lunch / Dinner / Snacks |

### 4. Claims (`claims_data.csv`)
Records of food claims made by receivers.

| Column | Type | Description |
|---|---|---|
| Claim_ID | Integer | Unique identifier |
| Food_ID | Integer | Reference to food item |
| Receiver_ID | Integer | Reference to the receiver |
| Status | String | Pending / Completed / Cancelled |
| Timestamp | Datetime | When the claim was made |

---

## ⚙️ Setup & Installation

### 1. Clone or download the project
```bash
cd food_project
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
python -m pip install streamlit pandas plotly
```

### 4. Run the app
```bash
python -m streamlit run app.py
```

Open your browser at **http://localhost:8501**

> The `food_waste.db` file is created automatically on first run — no manual database setup needed.

---

## 🖥️ App Pages

### 🏠 Home
Dashboard showing key metrics — total providers, receivers, food units available, and completed claims.

### 📋 View Data
Browse all 4 datasets with live filters by city, type, food type, and meal type.

### 🔍 SQL Query Results
All 15 SQL analysis queries displayed with their code and output:

1. Providers & Receivers per City
2. Provider Type with Most Food
3. Contact Info of Providers by City
4. Receivers Who Claimed the Most Food
5. Total Quantity of Food Available
6. City with Highest Food Listings
7. Most Common Food Types
8. Claims Per Food Item
9. Provider with Most Successful Claims
10. Claim Status Percentage
11. Avg Quantity Claimed per Receiver
12. Most Claimed Meal Type
13. Total Food Donated per Provider
14. Food Expiring Soon
15. Monthly Claim Trends

### 📊 Charts & EDA
Interactive visualizations including:
- Claim status distribution (pie chart)
- Food quantity by provider type (bar chart)
- Claims by meal type (bar chart)
- Top cities by food listings (bar chart)
- Top providers by donation (bar chart)
- Monthly claim trends (line chart)
- Top receivers by claims (bar chart)

### ✏️ CRUD Operations
- **Add** new food listings via a form
- **Update** quantity of existing food items
- **Delete** food listings by ID

---

## 💡 Key Insights the App Reveals

- Which cities have the most surplus food available
- Which provider types contribute the most food
- What percentage of claims are completed vs pending vs cancelled
- Which meal types are claimed the most
- Monthly trends in food distribution
- Top receivers and providers by activity

---

## 🎯 Skills Demonstrated

- **Python** — data processing, database integration, app logic
- **SQL** — 15 analytical queries using JOINs, GROUP BY, aggregations, subqueries
- **Streamlit** — multi-page interactive web app with filters and forms
- **Data Analysis** — trend identification, EDA, insight generation
- **Plotly** — interactive charts and visualizations

---

## 📚 Domain

Food Management | Waste Reduction | Social Good
