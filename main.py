import streamlit as st

def calculate_stop_loss(entry, risk_percentage, position):
    if position == "Long":
        return round(entry * (1 - risk_percentage / 100), 3)
    elif position == "Short":
        return round(entry * (1 + risk_percentage / 100), 3)
    else:
        raise ValueError("Invalid position type")

def calculate_take_profit(entry, reward_percentage, position):
    if position == "Long":
        return round(entry * (1 + reward_percentage / 100), 3)
    elif position == "Short":
        return round(entry * (1 - reward_percentage / 100), 3)
    else:
        raise ValueError("Invalid position type")

def calculate_percentage_from_price(entry, sl_or_tp):
    return round(((sl_or_tp - entry) / entry) * 100, 3)

def calculate_price_from_percentage(entry, percentage):
    return round(entry * (1 + percentage / 100), 3)

def calculate_liquidation(entry, quantity, initial_balance, is_usdt, position):
    if is_usdt:
        output = quantity / initial_balance
    else:
        output = (quantity * entry) / initial_balance
    
    if output == 0:
        return float('inf')  # Return infinity if output is zero to handle division by zero

    output2 = 100 / output
    
    if position == "Long":
        liquidation_price = round((100 - output2) / 100 * entry, 3)
    elif position == "Short":
        liquidation_price = round(((100 - output2) / 100 + 1) * entry, 3)

    return liquidation_price

st.title("Crypto Futures Calculator")

col1, col2 = st.columns(2)
with col1:
    entry = st.number_input("Entry Price (USDT)", min_value=0.0, step=0.01)
with col2:
    initial_balance = st.number_input("Initial Balance (USDT)", min_value=0.0, step=0.01)

col3, col4 = st.columns(2)
with col3:
    quantity = st.number_input("Quantity", min_value=0.0, step=0.01)
with col4:
    quantity_type = st.selectbox("Quantity Type", ["Units", "USDT"])
    is_usdt = quantity_type == "USDT"

col5, col6 = st.columns(2)
with col5:
    position = st.selectbox("Position", ["Long", "Short"])
with col6:
    leverage = st.number_input("Leverage", min_value=1, step=1)

col7, col8 = st.columns(2)

# Option to enter either Risk/Reward percentages or SL/TP prices
risk_reward_selected = st.radio("Select input method:", ("Risk/Reward (%)", "SL/TP (USDT)"))

if risk_reward_selected == "Risk/Reward (%)":
    with col7:
        risk_percentage = st.number_input("Risk Percentage (%)", min_value=0.0, step=0.01)
    with col8:
        reward_percentage = st.number_input("Reward Percentage (%)", min_value=0.0, step=0.01)

    # Calculate SL and TP based on risk/reward percentages
    if st.button("Calculate"):
        stop_loss = calculate_stop_loss(entry, risk_percentage, position)
        take_profit = calculate_take_profit(entry, reward_percentage, position)
        sl_percentage = risk_percentage
        tp_percentage = reward_percentage

        st.write(f"Stop Loss Price: {stop_loss:.3f} USDT ({sl_percentage:.3f}%)")
        st.write(f"Take Profit Price: {take_profit:.3f} USDT ({tp_percentage:.3f}%)")

elif risk_reward_selected == "SL/TP (USDT)":
    with col7:
        sl_price = st.number_input("Stop Loss Price (USDT)", min_value=0.0, step=0.01)
    with col8:
        tp_price = st.number_input("Take Profit Price (USDT)", min_value=0.0, step=0.01)

    # Calculate risk/reward percentages based on SL and TP prices
    if st.button("Calculate"):
        sl_percentage = calculate_percentage_from_price(entry, sl_price)
        tp_percentage = calculate_percentage_from_price(entry, tp_price)
        stop_loss = sl_price if position == "Long" else calculate_stop_loss(entry, sl_percentage, position)
        take_profit = tp_price if position == "Long" else calculate_take_profit(entry, tp_percentage, position)

        st.write(f"Stop Loss Price: {stop_loss:.3f} USDT ({sl_percentage:.3f}%)")
        st.write(f"Take Profit Price: {take_profit:.3f} USDT ({tp_percentage:.3f}%)")

# Calculate liquidation price
liquidation_price = calculate_liquidation(entry, quantity, initial_balance, is_usdt, position)
st.write(f"Liquidation Price: {liquidation_price:.3f} USDT")
