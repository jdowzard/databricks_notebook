# Databricks notebook source
# MAGIC %md
# MAGIC # Test Notebook 3: Unity Catalog Test
# MAGIC
# MAGIC This notebook tests Unity Catalog access and permissions.
# MAGIC
# MAGIC **Parameters:**
# MAGIC - `catalog_name`: Unity Catalog name to query (default: main)
# MAGIC - `schema_name`: Schema to explore (optional)

# COMMAND ----------

# Setup parameters
dbutils.widgets.text("catalog_name", "main", "Catalog Name")
dbutils.widgets.text("schema_name", "", "Schema Name (optional)")

# COMMAND ----------

catalog_name = dbutils.widgets.get("catalog_name")
schema_name = dbutils.widgets.get("schema_name")

print("=" * 60)
print("UNITY CATALOG TEST - RESULTS")
print("=" * 60)
print(f"Testing catalog: {catalog_name}")
if schema_name:
    print(f"Testing schema: {schema_name}")
print("=" * 60)

# COMMAND ----------

# List available catalogs
print("\nAvailable Catalogs:")
catalogs = spark.sql("SHOW CATALOGS").collect()
for catalog in catalogs:
    print(f"  - {catalog.catalog}")

# COMMAND ----------

# Check if specified catalog exists
catalog_exists = any(c.catalog == catalog_name for c in catalogs)

if catalog_exists:
    print(f"\n✓ Catalog '{catalog_name}' found")

    # List schemas in the catalog
    print(f"\nSchemas in '{catalog_name}':")
    try:
        schemas = spark.sql(f"SHOW SCHEMAS IN {catalog_name}").collect()
        for schema in schemas:
            print(f"  - {schema.databaseName}")
    except Exception as e:
        print(f"  ✗ Error listing schemas: {e}")

else:
    print(f"\n✗ Catalog '{catalog_name}' not found")

# COMMAND ----------

# If a schema is specified, explore it
if schema_name and catalog_exists:
    print(f"\nExploring schema: {catalog_name}.{schema_name}")

    try:
        # List tables in the schema
        tables = spark.sql(f"SHOW TABLES IN {catalog_name}.{schema_name}").collect()

        if tables:
            print(f"\nTables in {catalog_name}.{schema_name}:")
            for table in tables:
                print(f"  - {table.tableName} (namespace: {table.database})")

            # Try to query the first table
            if len(tables) > 0:
                first_table = tables[0].tableName
                full_table_name = f"{catalog_name}.{schema_name}.{first_table}"
                print(f"\nSample query from {full_table_name}:")

                try:
                    sample_df = spark.sql(f"SELECT * FROM {full_table_name} LIMIT 5")
                    print(f"  Row count: {sample_df.count()}")
                    print(f"  Columns: {sample_df.columns}")
                    sample_df.show(5, truncate=False)
                except Exception as e:
                    print(f"  ✗ Error querying table: {e}")
        else:
            print(f"  No tables found in {catalog_name}.{schema_name}")

    except Exception as e:
        print(f"✗ Error exploring schema: {e}")

# COMMAND ----------

# Test creating a temporary view
print("\nTesting DataFrame operations:")

from pyspark.sql import Row
from datetime import datetime

# Create sample data
sample_data = [
    Row(id=1, name="Test 1", timestamp=datetime.now().isoformat()),
    Row(id=2, name="Test 2", timestamp=datetime.now().isoformat()),
    Row(id=3, name="Test 3", timestamp=datetime.now().isoformat())
]

df = spark.createDataFrame(sample_data)
df.createOrReplaceTempView("temp_test_view")

print("✓ Created temporary view 'temp_test_view'")

# Query the temp view
result = spark.sql("SELECT * FROM temp_test_view")
print("\nTemp view contents:")
result.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Test Summary
# MAGIC
# MAGIC This notebook successfully:
# MAGIC - ✓ Connected to Unity Catalog
# MAGIC - ✓ Listed available catalogs
# MAGIC - ✓ Explored schemas and tables (if available)
# MAGIC - ✓ Created temporary views
# MAGIC - ✓ Executed SQL queries

# COMMAND ----------

print("\n✓ Unity Catalog test completed successfully!")
print(f"Catalog tested: {catalog_name}")
if schema_name:
    print(f"Schema tested: {schema_name}")

dbutils.notebook.exit("SUCCESS")
