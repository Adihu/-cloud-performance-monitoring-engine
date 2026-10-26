"""
Multi-Node Cloud Performance Monitoring Engine
Module: Telemetry Ingestion (Real Hardware Metrics)
Author: Deep Raj
Course: BCA (Cloud Computing & Virtualization)
"""

import datetime
import importlib
import sqlite3
import time

try:
  psutil = importlib.import_module("psutil")
except ModuleNotFoundError as exc:
  if exc.name != "psutil":
    raise
  psutil = None

# --- 1. DATABASE INITIALIZATION ---
DB_NAME = "cluster_metrics.db"


def init_db():
  """Creates the SQLite database table with real hardware metric schema."""
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        server_name TEXT,
        cpu_usage REAL,
        memory_usage REAL,
        disk_usage REAL,
        status TEXT
    )
    """)
  conn.commit()
  conn.close()


# --- 2. CLUSTER METRIC COLLECTION ---
NODES = ["Web-Server-01", "Database-Node", "API-Gateway"]


def log_cluster_telemetry():
  """Collects real hardware telemetry via psutil and logs data for simulated cluster nodes."""
  if psutil is None:
    raise RuntimeError("Missing dependency: install psutil with 'python -m pip install psutil'.")

  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()

  # Fetch real hardware metrics from system
  real_cpu = psutil.cpu_percent(interval=0.5)
  real_memory = psutil.virtual_memory().percent
  real_disk = psutil.disk_usage('/').percent

  for node in NODES:
    # Health status based on usage thresholds
    if real_cpu > 80.0 or real_memory > 85.0:
      status = "WARNING: High Spike"
    else:
      status = "System Normal"

    cursor.execute(
        """
        INSERT INTO logs (server_name, cpu_usage, memory_usage, disk_usage, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (node, real_cpu, real_memory, real_disk, status),
    )

  conn.commit()
  conn.close()
  print(
      f"[LOGS SAVED] Time: {datetime.datetime.now().strftime('%H:%M:%S')} | CPU:"
      f" {real_cpu}% | RAM: {real_memory}% | Disk: {real_disk}%"
  )


# --- 3. MAIN EXECUTION ---
if __name__ == "__main__":
  init_db()
  print("=== Starting Real Hardware Telemetry Ingestion ===")

  for i in range(1, 6):
    print(f"Cycle {i}/5...")
    log_cluster_telemetry()
    time.sleep(1)

  print("\n=== Ingestion Completed Successfully ===")