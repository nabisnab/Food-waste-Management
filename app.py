import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from database import setup_database, run_query, QUERIES, DB_PATH

st.set_page_config(page_title="Local Food Wastage Management System", page_icon="🍱", layout="wide")

setup_database()

def get_conn():
    return sqlite3.connect(DB_PATH)

# ---- SIDEBAR ----
st.sidebar.title("🍱 Food Waste Manager")
page = st.sidebar.radio("Navigate", [
    "🏠 Home", "📋 View Data", "🔍 SQL Query Results", "📊 Charts & EDA", "✏️ CRUD Operations"
])

# ============================================================
# HOME
# ============================================================
if page == "🏠 Home":
    st.title("🍱 Local Food Wastage Management System")
    st.markdown("### Connecting surplus food providers to those in need")

    col1, col2, col3, col4 = st.columns(4)
    conn = get_conn()
    total_providers = pd.read_sql("SELECT COUNT(*) as c FROM providers", conn).iloc[0,0]
    total_receivers = pd.read_sql("SELECT COUNT(*) as c FROM receivers", conn).iloc[0,0]
    total_food = pd.read_sql("SELECT SUM(Quantity) as c FROM food_listings", conn).iloc[0,0]
    total_claims = pd.read_sql("SELECT COUNT(*) as c FROM claims", conn).iloc[0,0]
    completed = pd.read_sql("SELECT COUNT(*) as c FROM claims WHERE Status='Completed'", conn).iloc[0,0]
    conn.close()

    col1.metric("🏪 Providers", f"{total_providers:,}")
    col2.metric("🤝 Receivers", f"{total_receivers:,}")
    col3.metric("🥘 Food Units Available", f"{int(total_food):,}")
    col4.metric("📦 Completed Claims", f"{completed:,}")

    st.markdown("---")
    col_a, col_b = st.columns(2)
    col_a.markdown("""
    **How it works:**
    - 🏪 **Providers** (restaurants, grocery stores, supermarkets, caterers) list surplus food
    - 🤝 **Receivers** (NGOs, shelters, charities, individuals) claim the food
    - 🗄️ **SQL Database** stores all food details and locations
    - 📊 **This app** enables filtering, CRUD operations, and data visualization
    """)
    col_b.markdown("""
    **Pages in this app:**
    - 📋 **View Data** — Browse all 4 tables with filters
    - 🔍 **SQL Query Results** — All 15 analysis queries
    - 📊 **Charts & EDA** — Interactive visualizations
    - ✏️ **CRUD Operations** — Add / Update / Delete food listings
    """)

# ============================================================
# VIEW DATA
# ============================================================
elif page == "📋 View Data":
    st.title("📋 View Data")

    tab1, tab2, tab3, tab4 = st.tabs(["🏪 Providers", "🤝 Receivers", "🥘 Food Listings", "📦 Claims"])
    conn = get_conn()

    with tab1:
        st.subheader("Food Providers")
        df = pd.read_sql("SELECT * FROM providers", conn)
        col1, col2 = st.columns(2)
        city_f = col1.multiselect("Filter by City", sorted(df["City"].dropna().unique()), key="prov_city")
        type_f = col2.multiselect("Filter by Type", sorted(df["Type"].dropna().unique()), key="prov_type")
        if city_f: df = df[df["City"].isin(city_f)]
        if type_f: df = df[df["Type"].isin(type_f)]
        st.write(f"Showing {len(df)} records")
        st.dataframe(df, use_container_width=True, height=400)

    with tab2:
        st.subheader("Food Receivers")
        df = pd.read_sql("SELECT * FROM receivers", conn)
        col1, col2 = st.columns(2)
        city_f = col1.multiselect("Filter by City", sorted(df["City"].dropna().unique()), key="rec_city")
        type_f = col2.multiselect("Filter by Type", sorted(df["Type"].dropna().unique()), key="rec_type")
        if city_f: df = df[df["City"].isin(city_f)]
        if type_f: df = df[df["Type"].isin(type_f)]
        st.write(f"Showing {len(df)} records")
        st.dataframe(df, use_container_width=True, height=400)

    with tab3:
        st.subheader("Food Listings")
        df = pd.read_sql("SELECT * FROM food_listings", conn)
        col1, col2, col3 = st.columns(3)
        city_f = col1.multiselect("City", sorted(df["Location"].dropna().unique()), key="fl_city")
        ftype_f = col2.multiselect("Food Type", sorted(df["Food_Type"].dropna().unique()), key="fl_ftype")
        meal_f = col3.multiselect("Meal Type", sorted(df["Meal_Type"].dropna().unique()), key="fl_meal")
        if city_f: df = df[df["Location"].isin(city_f)]
        if ftype_f: df = df[df["Food_Type"].isin(ftype_f)]
        if meal_f: df = df[df["Meal_Type"].isin(meal_f)]
        st.write(f"Showing {len(df)} records")
        st.dataframe(df, use_container_width=True, height=400)

    with tab4:
        st.subheader("Claims")
        df = pd.read_sql("SELECT * FROM claims", conn)
        status_f = st.multiselect("Filter by Status", sorted(df["Status"].dropna().unique()), key="cl_status")
        if status_f: df = df[df["Status"].isin(status_f)]
        st.write(f"Showing {len(df)} records")
        st.dataframe(df, use_container_width=True, height=400)

    conn.close()

# ============================================================
# SQL QUERY RESULTS
# ============================================================
elif page == "🔍 SQL Query Results":
    st.title("🔍 SQL Query Results")
    st.markdown("All 15 analysis queries with results from your real dataset")

    for title, query in QUERIES.items():
        with st.expander(f"**{title}**"):
            df = run_query(query)
            st.code(query.strip(), language="sql")
            st.dataframe(df, use_container_width=True)
            st.caption(f"{len(df)} rows returned")

# ============================================================
# CHARTS & EDA
# ============================================================
elif page == "📊 Charts & EDA":
    st.title("📊 Charts & Exploratory Data Analysis")

    col1, col2 = st.columns(2)

    df1 = run_query(QUERIES["Q10: Claim Status Percentage"])
    fig1 = px.pie(df1, names="Status", values="Count", title="Claim Status Distribution",
                  color_discrete_sequence=["#4CAF50","#FF7043","#FFC107"])
    col1.plotly_chart(fig1, use_container_width=True)

    df2 = run_query(QUERIES["Q2: Provider Type with Most Food"])
    fig2 = px.bar(df2, x="Provider_Type", y="Total_Quantity", title="Food Quantity by Provider Type",
                  color="Total_Quantity", color_continuous_scale="Greens", text="Total_Quantity")
    fig2.update_traces(textposition="outside")
    col2.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    df3 = run_query(QUERIES["Q12: Most Claimed Meal Type"])
    fig3 = px.bar(df3, x="Meal_Type", y="Times_Claimed", title="Claims by Meal Type",
                  color="Meal_Type", color_discrete_sequence=px.colors.qualitative.Pastel,
                  text="Times_Claimed")
    fig3.update_traces(textposition="outside")
    col3.plotly_chart(fig3, use_container_width=True)

    df4 = run_query(QUERIES["Q7: Most Common Food Types"])
    fig4 = px.pie(df4, names="Food_Type", values="Total_Qty", title="Food Availability by Type")
    col4.plotly_chart(fig4, use_container_width=True)

    col5, col6 = st.columns(2)

    df5 = run_query(QUERIES["Q6: City with Highest Food Listings"]).head(10)
    fig5 = px.bar(df5, x="City", y="Listings", title="Top 10 Cities by Food Listings",
                  color="Listings", color_continuous_scale="Blues")
    fig5.update_xaxes(tickangle=35)
    col5.plotly_chart(fig5, use_container_width=True)

    df6 = run_query(QUERIES["Q13: Total Food Donated per Provider"])
    fig6 = px.bar(df6, x="Name", y="Total_Donated", title="Top Providers by Food Donated",
                  color="Total_Donated", color_continuous_scale="Oranges")
    fig6.update_xaxes(tickangle=35)
    col6.plotly_chart(fig6, use_container_width=True)

    st.subheader("📈 Monthly Claim Trends")
    df7 = run_query(QUERIES["Q15: Monthly Claim Trends"])
    fig7 = px.line(df7, x="Month", y=["Total_Claims","Completed","Pending","Cancelled"],
                   title="Monthly Claims Breakdown", markers=True)
    st.plotly_chart(fig7, use_container_width=True)

    st.subheader("🏆 Top 10 Receivers by Claims")
    df8 = run_query(QUERIES["Q4: Receivers Who Claimed the Most Food"])
    fig8 = px.bar(df8, x="Name", y="Total_Claims", color="Type",
                  title="Top Receivers", text="Total_Claims")
    fig8.update_xaxes(tickangle=35)
    fig8.update_traces(textposition="outside")
    st.plotly_chart(fig8, use_container_width=True)

# ============================================================
# CRUD OPERATIONS
# ============================================================
elif page == "✏️ CRUD Operations":
    st.title("✏️ CRUD Operations")
    tab1, tab2, tab3 = st.tabs(["➕ Add Food Listing", "✏️ Update Quantity", "🗑️ Delete Listing"])

    with tab1:
        st.subheader("Add New Food Listing")
        conn = get_conn()
        providers_df = pd.read_sql("SELECT Provider_ID, Name, City, Type FROM providers", conn)
        max_id = pd.read_sql("SELECT MAX(Food_ID) as m FROM food_listings", conn).iloc[0,0]
        conn.close()

        with st.form("add_food"):
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1, value=10)
            expiry = st.date_input("Expiry Date")
            provider_name = st.selectbox("Provider", providers_df["Name"].tolist())
            food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
            submitted = st.form_submit_button("➕ Add Food Listing")

            if submitted and food_name.strip():
                conn = get_conn()
                prow = providers_df[providers_df["Name"] == provider_name].iloc[0]
                conn.execute("""
                    INSERT INTO food_listings
                    (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (int(max_id)+1, food_name, quantity, str(expiry),
                      int(prow["Provider_ID"]), prow["Type"], prow["City"], food_type, meal_type))
                conn.commit()
                conn.close()
                st.success(f"✅ '{food_name}' added successfully!")
            elif submitted:
                st.error("Please enter a food name.")

    with tab2:
        st.subheader("Update Food Quantity")
        conn = get_conn()
        df = pd.read_sql("SELECT Food_ID, Food_Name, Quantity, Location, Food_Type FROM food_listings ORDER BY Food_ID", conn)
        conn.close()

        options = df["Food_Name"].tolist()
        food_choice = st.selectbox("Select Food Item (by name)", options, key="upd_food")
        rows = df[df["Food_Name"] == food_choice]
        if len(rows) > 1:
            food_id = st.selectbox("Multiple entries found — pick Food_ID",
                                   rows["Food_ID"].tolist(), key="upd_id")
            row = rows[rows["Food_ID"] == food_id].iloc[0]
        else:
            row = rows.iloc[0]

        st.info(f"📍 Location: **{row['Location']}** | 🥘 Type: **{row['Food_Type']}** | 📦 Current Qty: **{row['Quantity']}**")
        new_qty = st.number_input("New Quantity", min_value=0, value=int(row["Quantity"]))
        if st.button("✅ Update Quantity"):
            conn = get_conn()
            conn.execute("UPDATE food_listings SET Quantity=? WHERE Food_ID=?", (new_qty, int(row["Food_ID"])))
            conn.commit()
            conn.close()
            st.success(f"✅ Quantity updated to {new_qty}!")

    with tab3:
        st.subheader("Delete Food Listing")
        conn = get_conn()
        df = pd.read_sql("SELECT Food_ID, Food_Name, Quantity, Location FROM food_listings ORDER BY Food_ID", conn)
        conn.close()

        food_id_del = st.number_input("Enter Food_ID to delete", min_value=1, step=1)
        match = df[df["Food_ID"] == food_id_del]
        if not match.empty:
            row = match.iloc[0]
            st.warning(f"⚠️ You are about to delete: **{row['Food_Name']}** | Qty: {row['Quantity']} | Location: {row['Location']}")
            if st.button("🗑️ Confirm Delete", type="primary"):
                conn = get_conn()
                conn.execute("DELETE FROM food_listings WHERE Food_ID=?", (int(food_id_del),))
                conn.commit()
                conn.close()
                st.success(f"✅ Food item {food_id_del} deleted!")
        elif food_id_del:
            st.error("No food item found with that ID.")