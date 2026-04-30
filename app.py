import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Brokerage Calculator",
    page_icon="🌫",
    layout="wide"
)

charges = pd.read_csv("customer_brokerage_rates.csv")

st.title("🌫 Brokerage Calculator")
st.header("Check your Brokerage")

st.subheader("Delivery Calculator")

customerID = st.number_input(
    "Enter Customer ID",
    min_value=1,
    step=1
)

trade_type = st.radio(
    "Trade Type",
    ["Buy", "Sell"],
    horizontal=True
)

amount = st.number_input(
    "Enter Share Price",
    min_value=0.0,
    step=0.05
)

buy_shares = st.number_input(
    "Enter Number of Shares",
    min_value=0,
    step=1
)

exchange = st.radio(
    "Exchange",
    ["NSE", "BSE"],
    horizontal=True
)

customer = charges[charges["Customer_Code"] == int(customerID)]

if customer.empty:
    st.error("Customer ID not found!")
    st.stop()

customer = customer.squeeze()

rate = customer["Delivery_Brokerage_(%)"] / 100

turnover = buy_shares * amount

brokerage = rate * turnover

if exchange == "NSE":
    exch_txn = turnover * 0.0000297
else:
    exch_txn = turnover * 0.00003275

sebi  = turnover * 0.000001
gst   = (brokerage + exch_txn) * 0.18
stamp = turnover * 0.00003 if trade_type == "Buy" else 0   
stt   = turnover * 0.001                               

total_charges = brokerage + stt + exch_txn + sebi + gst + stamp

st.write(f"Customer: {customer['Customer_Name']} | Delivery Rate: {customer['Delivery_Brokerage_(%)']:.2f}%")
st.write(f"Turnover: {turnover:.2f}")
st.write(f"Brokerage: {brokerage:.4f}")
st.write(f"STT: {stt:.4f}")
st.write(f"Exchange Txn Charge: {exch_txn:.4f}")
st.write(f"SEBI Charge: {sebi:.4f}")
st.write(f"GST: {gst:.4f}")
st.write(f"Stamp Duty: {stamp:.4f}")
st.write(f"TOTAL CHARGES: {total_charges:.4f}")
