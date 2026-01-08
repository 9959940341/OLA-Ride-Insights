import streamlit as st
import pandas as pd

st.set_page_config(page_title="OLA Ride Insights", layout="wide")

st.title("🚕 OLA Ride Insights Dashboard")

# Load data
df = pd.read_csv("OLA_Cleaned_Data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ---------- SIDEBAR ----------
st.sidebar.header("🔍 Filter Options")

start_date = st.sidebar.date_input(
    "Start Date", df["Date"].min().date()
)
end_date = st.sidebar.date_input(
    "End Date", df["Date"].max().date()
)

vehicle_types = st.sidebar.multiselect(
    "Vehicle Type",
    df["Vehicle_Type"].unique(),
    default=df["Vehicle_Type"].unique()
)

booking_status = st.sidebar.multiselect(
    "Booking Status",
    df["Booking_Status"].unique(),
    default=df["Booking_Status"].unique()
)

filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date) &
    (df["Vehicle_Type"].isin(vehicle_types)) &
    (df["Booking_Status"].isin(booking_status))
]

# ---------- KPIs ----------
total_rides = len(filtered_df)
successful_rides = filtered_df[filtered_df["Booking_Status"] == "Success"].shape[0]
total_revenue = filtered_df["Booking_Value"].sum()
success_rate = (successful_rides / total_rides * 100) if total_rides > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("🚗 Total Rides", total_rides)
col2.metric("✅ Successful Rides", successful_rides)
col3.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
col4.metric("📈 Success Rate", f"{success_rate:.2f}%")

# ---------- DATA PREVIEW ----------
st.subheader("📊 Filtered Dataset Preview")
st.dataframe(filtered_df.head())
