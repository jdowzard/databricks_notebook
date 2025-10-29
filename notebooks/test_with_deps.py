# Databricks notebook source
# MAGIC %md
# MAGIC # Test Notebook 2: Dependencies Test
# MAGIC
# MAGIC This notebook tests running with external dependencies using %pip magic commands.
# MAGIC
# MAGIC **Dependencies:**
# MAGIC - pandas
# MAGIC - requests
# MAGIC - python-dateutil
# MAGIC
# MAGIC **Parameters:**
# MAGIC - `sample_size`: Number of sample records to generate
# MAGIC - `test_url`: URL to test HTTP requests

# COMMAND ----------

# Install dependencies using %pip magic command
# MAGIC %pip install pandas requests python-dateutil

# COMMAND ----------

# MAGIC %md
# MAGIC **Note:** After installing packages with %pip, we need to restart the Python process

# COMMAND ----------

# Restart Python to use newly installed packages
dbutils.library.restartPython()

# COMMAND ----------

# Setup parameters
dbutils.widgets.text("sample_size", "10", "Sample Size")
dbutils.widgets.text("test_url", "https://api.github.com", "Test URL")

# COMMAND ----------

# Test pandas import (from requirements.txt)
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests

print("=" * 60)
print("DEPENDENCIES TEST - RESULTS")
print("=" * 60)
print(f"✓ pandas version: {pd.__version__}")
print(f"✓ numpy version: {np.__version__}")
print(f"✓ requests version: {requests.__version__}")
print("=" * 60)

# COMMAND ----------

# Get parameters
sample_size = int(dbutils.widgets.get("sample_size"))
test_url = dbutils.widgets.get("test_url")

print(f"\nGenerating {sample_size} sample records...")

# Create sample data using pandas
dates = pd.date_range(start='2025-01-01', periods=sample_size, freq='D')
df_pandas = pd.DataFrame({
    'date': dates,
    'value': np.random.randn(sample_size),
    'category': np.random.choice(['A', 'B', 'C'], sample_size),
    'created_at': datetime.now()
})

print("\nSample Pandas DataFrame:")
print(df_pandas.head())
print(f"\nDataFrame shape: {df_pandas.shape}")
print(f"DataFrame columns: {df_pandas.columns.tolist()}")

# COMMAND ----------

# Test dateutil functionality
current_date = datetime.now()
future_date = current_date + relativedelta(months=3)
past_date = current_date - relativedelta(years=1)

print(f"\nDate calculations using python-dateutil:")
print(f"Current date: {current_date.strftime('%Y-%m-%d')}")
print(f"3 months from now: {future_date.strftime('%Y-%m-%d')}")
print(f"1 year ago: {past_date.strftime('%Y-%m-%d')}")

# COMMAND ----------

# Test requests library
print(f"\nTesting HTTP request to: {test_url}")
try:
    response = requests.get(test_url, timeout=10)
    print(f"✓ Request successful!")
    print(f"  Status code: {response.status_code}")
    print(f"  Response time: {response.elapsed.total_seconds():.2f}s")
except requests.RequestException as e:
    print(f"✗ Request failed: {e}")

# COMMAND ----------

# Convert pandas DataFrame to Spark DataFrame
spark_df = spark.createDataFrame(df_pandas)
print("\nConverted to Spark DataFrame:")
spark_df.show(5)
spark_df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test Summary
# MAGIC
# MAGIC This notebook successfully:
# MAGIC - ✓ Installed dependencies from requirements.txt
# MAGIC - ✓ Imported pandas, requests, python-dateutil
# MAGIC - ✓ Created sample data using pandas
# MAGIC - ✓ Made HTTP requests using requests library
# MAGIC - ✓ Used dateutil for date calculations
# MAGIC - ✓ Converted pandas DataFrame to Spark DataFrame

# COMMAND ----------

print("\n✓ Dependencies test completed successfully!")
print(f"Sample size: {sample_size}")
print(f"Test URL: {test_url}")
print(f"All required packages loaded and functional")

dbutils.notebook.exit("SUCCESS")
