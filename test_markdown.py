# Databricks notebook source

# MAGIC %md
# MAGIC # Test: Advanced Markdown Features
# MAGIC 
# MAGIC Testing various markdown capabilities

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tables
# MAGIC 
# MAGIC | Column 1 | Column 2 | Column 3 |
# MAGIC |----------|----------|----------|
# MAGIC | Value 1  | Value 2  | Value 3  |
# MAGIC | Data A   | Data B   | Data C   |

# COMMAND ----------

# MAGIC %md
# MAGIC ## LaTeX Math
# MAGIC 
# MAGIC Inline math: $E = mc^2$
# MAGIC 
# MAGIC Block math:
# MAGIC 
# MAGIC $$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$
# MAGIC 
# MAGIC $$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}$$

# COMMAND ----------

# MAGIC %md
# MAGIC ## Code Blocks
# MAGIC 
# MAGIC ```python
# MAGIC def hello():
# MAGIC     print("Hello, World!")
# MAGIC ```
# MAGIC 
# MAGIC ```bash
# MAGIC ls -la
# MAGIC pwd
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lists
# MAGIC 
# MAGIC ### Unordered
# MAGIC - Item 1
# MAGIC - Item 2
# MAGIC   - Nested item
# MAGIC   - Another nested
# MAGIC - Item 3
# MAGIC 
# MAGIC ### Ordered
# MAGIC 1. First
# MAGIC 2. Second
# MAGIC 3. Third

# COMMAND ----------

# MAGIC %md
# MAGIC ## Links and Images
# MAGIC 
# MAGIC [Click here](https://example.com)
# MAGIC 
# MAGIC ![Alt text](https://via.placeholder.com/150)

# COMMAND ----------

# MAGIC %md
# MAGIC ## HTML
# MAGIC 
# MAGIC <div style="background-color: #f0f0f0; padding: 10px;">
# MAGIC     <h3>Custom HTML</h3>
# MAGIC     <p>This is <strong>HTML</strong> content</p>
# MAGIC </div>

# COMMAND ----------

"Markdown test complete"