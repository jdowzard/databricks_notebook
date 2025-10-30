# Databricks notebook source

# MAGIC %md
# MAGIC # Test: Jupyter Magics
# MAGIC 
# MAGIC Testing various Jupyter magic commands

# COMMAND ----------

import time
import pandas as pd

# COMMAND ----------

# MAGIC %md
# MAGIC ## Line Magic: %time

# COMMAND ----------

%time sum(range(100))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell Magic: %%time

# COMMAND ----------

%%time
print("Processing...")
result = sum(range(1000000))
time.sleep(0.1)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Matplotlib Magic: %matplotlib inline

# COMMAND ----------

%matplotlib inline
import matplotlib.pyplot as plt

# COMMAND ----------

plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.ylabel('Some numbers')
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Shell command: ! (bang)

# COMMAND ----------

!python --version

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell Magic: %%bash

# COMMAND ----------

%%bash
echo "Hello from bash"
echo "Current directory: $(pwd)"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell Magic: %%writefile

# COMMAND ----------

%%writefile test_file.txt
This is a test file
Created from Jupyter

# COMMAND ----------

# MAGIC %md
# MAGIC ## Final Test

# COMMAND ----------

"Test complete"