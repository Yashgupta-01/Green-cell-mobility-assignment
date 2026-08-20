import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

st.set_page_config(page_title="Voltage Analysis Dashboard", layout="wide")

st.title("Voltage Data Analysis Dashboard")
st.markdown("Interactive analysis of continuous voltage readings, moving averages, and local extrema.")

st.sidebar.header("Data Source")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Upload a CSV file in the sidebar to visualize and analyze data.")
    st.stop()

# Process Datetime & Moving Averages
df['Timestamp_dt'] = pd.to_datetime(df['Timestamp'], dayfirst=True, format='mixed')
df = df.sort_values('Timestamp_dt')

df['1000 Value MA'] = df['Voltage'].rolling(window=1000).mean()
df['5000 Value MA'] = df['Voltage'].rolling(window=5000).mean()

# 5-Day Moving Average
temp_df = df.set_index('Timestamp_dt')
df['5 Day MA'] = temp_df['Voltage'].rolling('5D').mean().values

# --- TASK A & B: CHART PLOTTING ---
st.header("1. Moving Average Trend Chart")
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(df['Timestamp'], df['Voltage'], color='gray', alpha=0.3, label='Original Values')
ax.plot(df['Timestamp'], df['1000 Value MA'], color='blue', label='1000 Value MA')
ax.plot(df['Timestamp'], df['5000 Value MA'], color='orange', label='5000 Value MA')
ax.plot(df['Timestamp'], df['5 Day MA'], color='red', linewidth=2, label='5 Day MA')

ax.set_title('Voltage with 1000, 5000, and 5-Day Moving Averages', fontsize=14, fontweight='bold')
ax.set_xlabel('Timestamp')
ax.set_ylabel('Voltage')
ax.legend(loc='upper right')
ax.grid(True, linestyle='--', alpha=0.4)
fig.autofmt_xdate()
plt.tight_layout()

st.pyplot(fig)

# --- TASK C: LOCAL PEAKS AND LOWS ---
st.header("2. Local Peaks and Lows")
voltage_val = df['Voltage'].values
peak_idx, _ = find_peaks(voltage_val, distance=100)
low_idx, _ = find_peaks(-voltage_val, distance=100)

peak_df = pd.DataFrame({
    'Timestamp': df['Timestamp'].iloc[peak_idx].values,
    'Voltage': df['Voltage'].iloc[peak_idx].values,
    'Type': 'Local Peak'
})

low_df = pd.DataFrame({
    'Timestamp': df['Timestamp'].iloc[low_idx].values,
    'Voltage': df['Voltage'].iloc[low_idx].values,
    'Type': 'Local Low'
})

extrema_df = pd.concat([peak_df, low_df]).sort_index().reset_index(drop=True)

col1, col2 = st.columns(2)
col1.metric("Local Peaks", len(peak_df))
col2.metric("Local Lows", len(low_df))

st.dataframe(extrema_df, use_container_width=True)

# Export CSV button
st.download_button(
    label="📥 Download Peaks & Lows CSV",
    data=extrema_df.to_csv(index=False),
    file_name="peaks_and_lows.csv",
    mime="text/csv"
)

# --- TASK D: VOLTAGE < 20 INSTANCES ---
st.header("3. Voltage Drops Below 20")
below_20_df = df[df['Voltage'] < 20][['Timestamp', 'Voltage']].reset_index(drop=True)

if len(below_20_df) == 0:
    st.success(f"No instances found where Voltage dropped below 20. (Dataset Minimum: {df['Voltage'].min()})")
else:
    st.warning(f"Found {len(below_20_df)} instances where Voltage was below 20:")
    st.dataframe(below_20_df, use_container_width=True)

# --- BONUS TASK: DOWNWARD SLOPE ACCELERATION ---
st.header("4. Downward Slope Acceleration (Bonus)")
df['slope'] = df['Voltage'].diff()
df['acceleration'] = df['slope'].diff()

df['downward'] = df['slope'] < 0
df['cycle_id'] = (~df['downward']).cumsum()

downward_cycles = df[df['downward']].copy()

if not downward_cycles.empty:
    accelerating_points = downward_cycles.loc[
        downward_cycles.groupby('cycle_id')['acceleration'].idxmin()
    ][['Timestamp', 'Voltage', 'slope', 'acceleration']].reset_index(drop=True)

    accelerating_points = accelerating_points[accelerating_points['acceleration'] < -2]
    st.write(f"Identified **{len(accelerating_points)}** downward cycles exhibiting slope acceleration:")
    st.dataframe(accelerating_points, use_container_width=True)
