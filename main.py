import streamlit as st

def calculate_stop_loss(entry, stop_loss, quantity, is_usdt):
    if is_usdt:
        quantity = quantity / entry
    return (entry - stop_loss) * quantity

def calculate_take_profit(entry, take_profit, quantity, is_usdt):
    if is_usdt:
        quantity = quantity / entry
    return (take_profit - entry) * quantity

def calculate_liquidation(entry, quantity, initial_balance, is_usdt, position):
    if is_usdt:
        output = quantity / initial_balance
    else:
        output = (quantity * entry) / initial_balance
    
    output2 = 100 / output
    
    if position == "Long":
        liquidation_price = (100 - output2) / 100 * entry
    elif position == "Short":
        liquidation_price = ((output2) / 100 + 0.95) * entry

    return liquidation_price

st.title("Crypto Futures Calculator")

col1, col2 = st.columns(2)
with col1:
    entry = st.number_input("Entry Price (USDT)", min_value=0.0, step=0.01)
with col2:
    initial_balance = st.number_input("Initial Balance (USDT)", min_value=0.0, step=0.01)

col3, col4 = st.columns(2)
with col3:
    stop_loss = st.number_input("Stop Loss Price (USDT)", min_value=0.0, step=0.01)
with col4:
    take_profit = st.number_input("Take Profit Price (USDT)", min_value=0.0, step=0.01)

col5, col6 = st.columns(2)
with col5:
    quantity = st.number_input("Quantity", min_value=0.0, step=0.01)
with col6:
    quantity_type = st.selectbox("Quantity Type", ["Units", "USDT"])
    is_usdt = quantity_type == "USDT"

col7, col8 = st.columns(2)
with col7:
    position = st.selectbox("Position", ["Long", "Short"])
with col8:
    leverage = st.number_input("Leverage", min_value=1, step=1)

# maintenance_margin_rate = st.number_input("Maintenance Margin Rate", min_value=0.0, max_value=1.0, step=0.001)

if st.button("Calculate"):
    stop_loss_value = calculate_stop_loss(entry, stop_loss, quantity, is_usdt)
    take_profit_value = calculate_take_profit(entry, take_profit, quantity, is_usdt)
    liquidation_price = calculate_liquidation(entry, quantity, initial_balance, is_usdt, position)

    col3, col4 = st.columns(2)
    with col3:
        st.write(f"Stop Loss Value: {stop_loss_value:.2f} USDT")
    with col4:
        st.write(f"Take Profit Value: {take_profit_value:.2f} USDT")

    st.write(f"Liquidation Price: {liquidation_price:.2f} USDT")
