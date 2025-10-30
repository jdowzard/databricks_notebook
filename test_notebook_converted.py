# Databricks notebook source

# MAGIC %md
# MAGIC # Test Jupyter Notebook
# MAGIC 
# MAGIC This notebook tests various features that might cause conversion issues:
# MAGIC - Markdown cells
# MAGIC - Code cells
# MAGIC - Jupyter magics
# MAGIC - Outputs

# COMMAND ----------

# Standard imports
import pandas as pd
import numpy as np
from datetime import datetime

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test Parameters
# MAGIC 
# MAGIC Setting up some test parameters

# COMMAND ----------

test_date = "2025-10-30"
test_mode = "test"
print(f"Test date: {test_date}")

# COMMAND ----------

# Create a simple DataFrame
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['Sydney', 'Melbourne', 'Brisbane']
}
df = pd.DataFrame(data)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Display Data
# MAGIC 
# MAGIC Let's look at our data

# COMMAND ----------

df.head()

# COMMAND ----------

# Some processing
total_rows = len(df)
print("Processing complete!")
print(f"Total rows: {total_rows}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Final Results
# MAGIC 
# MAGIC Summary of our test

# COMMAND ----------

result = {
    'status': 'success',
    'rows': total_rows,
    'date': test_date
}
result