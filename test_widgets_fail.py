# Databricks notebook source

# MAGIC %md
# MAGIC # Test: ipywidgets WITHOUT error handling
# MAGIC 
# MAGIC Will this break the notebook execution?

# COMMAND ----------

print("Starting test...")

# COMMAND ----------

# Direct import without try/except - this will fail if ipywidgets not installed
import ipywidgets as widgets
from IPython.display import display

# COMMAND ----------

# Create a slider widget
slider = widgets.IntSlider(value=50, min=0, max=100)
display(slider)

# COMMAND ----------

# This cell should never execute if widgets fail
print("If you see this, widgets worked!")