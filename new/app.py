import sqlite3
import pandas as pd
import psutil
import streamlit as st
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Cloud Performance Monitoring Engine",
    page_icon="☁️",
    layout="wide",
)

# --- Header Section ---
st.title("☁️ Multi-Node Cloud Performance Monitoring Engine")
st.markdown(
    "**BCA Portfolio Project** | Real-time System Telemetry & Resource Tracking"
)
st.markdown("---")

# --- Initialize SQLite Database ---
conn = sqlite3.connect("system_metrics.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        cpu_usage REAL,
        ram_usage REAL,
        disk_usage REAL
    )
"""
)
conn.commit()


# --- Sidebar Controls ---
st.sidebar.header("⚙️ Control Panel")
refresh_rate = st.sidebar.slider(
    "Refresh Interval (seconds)", min_value=1, max_value=10, value=2
)
auto_refresh = st.sidebar.checkbox("Enable Live Stream", value=True)

if st.sidebar.button("🧹 Clear Database Logs"):
    cursor.execute("DELETE FROM metrics")
    conn.commit()
    st.sidebar.success("Logs cleared!")

# --- Capture Current Metrics ---
cpu = psutil.cpu_percent(interval=None)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage("/").percent

# Insert into database for logging history
cursor.execute(
    """
    INSERT INTO metrics (cpu_usage, ram_usage, disk_usage)
    VALUES (?, ?, ?)
""",
    (cpu, ram, disk),
)
conn.commit()

# --- Top Metric Cards ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="💻 CPU Usage", value=f"{cpu}%", delta=f"Node 1 (Local)"
    )
with col2:
    st.metric(label="🧠 RAM Usage", value=f"{ram}%", delta=f"Active Memory")
with col3:
    st.metric(label="💾 Disk Usage", value=f"{disk}%", delta=f"C: Drive")

st.markdown("---")

# --- Live Charts Section ---
st.subheader("📈 Real-Time Telemetry Trend")

# Load data from SQLite
df = pd.read_sql_query(
    "SELECT timestamp, cpu_usage, ram_usage, disk_usage FROM metrics ORDER BY id DESC LIMIT 50",
    conn,
)

if not df.empty:
    # Reverse so it flows chronologically left-to-right
    df = df.iloc[::-1]

    # Display line charts for CPU, RAM, and Disk
    st.line_chart(
        df.set_index("timestamp")[["cpu_usage", "ram_usage", "disk_usage"]]
    )

    st.subheader("📋 Recent Database Logs")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Waiting for telemetry data...")

# --- Auto-refresh trigger ---
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()