# Databricks notebook source

# MAGIC %md
# MAGIC # Test: ipywidgets (Interactive Widgets)
# MAGIC 
# MAGIC Testing if widgets break or are handled gracefully

# COMMAND ----------

# Standard imports that should work
import pandas as pd
print("Standard imports work")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Try importing ipywidgets

# COMMAND ----------

try:
    import ipywidgets as widgets
    from IPython.display import display
    print("ipywidgets imported successfully")
    WIDGETS_AVAILABLE = True
except ImportError as e:
    print(f"ipywidgets not available: {e}")
    WIDGETS_AVAILABLE = False

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create a widget (if available)

# COMMAND ----------

if WIDGETS_AVAILABLE:
    # Create a simple slider
    slider = widgets.IntSlider(
        value=50,
        min=0,
        max=100,
        step=1,
        description='Test:'
    )
    display(slider)
    print("Widget created successfully")
else:
    print("Widgets not available, skipping widget creation")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Continue with normal code

# COMMAND ----------

# This should work regardless of widgets
data = {'value': [1, 2, 3], 'name': ['A', 'B', 'C']}
df = pd.DataFrame(data)
print("DataFrame created successfully")
print(df)

# COMMAND ----------

result = "Test completed - widgets " + ("worked" if WIDGETS_AVAILABLE else "were skipped")
print(result)