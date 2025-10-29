# Databricks notebook source
# MAGIC %md
# MAGIC # Test Notebook 1: Simple Parameter Test
# MAGIC
# MAGIC This notebook tests basic parameter passing without any external dependencies.
# MAGIC
# MAGIC **Parameters:**
# MAGIC - `date`: Test date parameter
# MAGIC - `mode`: Execution mode (test/prod)
# MAGIC - `message`: Optional message to display

# COMMAND ----------

# Import widgets for parameter handling
dbutils.widgets.text("date", "2025-01-01", "Date")
dbutils.widgets.text("mode", "test", "Mode")
dbutils.widgets.text("message", "Hello from Databricks!", "Message")

# COMMAND ----------

# Get parameter values
date_param = dbutils.widgets.get("date")
mode_param = dbutils.widgets.get("mode")
message_param = dbutils.widgets.get("message")

print("=" * 60)
print("SIMPLE PARAMETER TEST - RESULTS")
print("=" * 60)
print(f"Date Parameter: {date_param}")
print(f"Mode Parameter: {mode_param}")
print(f"Message Parameter: {message_param}")
print("=" * 60)

# COMMAND ----------

# Test basic PySpark functionality (no external dependencies)
from datetime import datetime
from pyspark.sql import Row

# Create a simple DataFrame
data = [
    Row(timestamp=datetime.now().isoformat(), parameter="date", value=date_param),
    Row(timestamp=datetime.now().isoformat(), parameter="mode", value=mode_param),
    Row(timestamp=datetime.now().isoformat(), parameter="message", value=message_param)
]

df = spark.createDataFrame(data)
print("\nParameter DataFrame:")
df.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test Summary
# MAGIC
# MAGIC This notebook successfully:
# MAGIC - ✓ Received parameters via dbutils.widgets
# MAGIC - ✓ Executed on serverless compute
# MAGIC - ✓ Used built-in PySpark without external dependencies

# COMMAND ----------

# Return success status
print("\n✓ Simple parameter test completed successfully!")
print(f"Execution mode: {mode_param}")
print(f"Test date: {date_param}")

dbutils.notebook.exit("SUCCESS")
