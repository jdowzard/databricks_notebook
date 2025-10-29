# databricks_notebook

Generalizable Databricks notebook runner using serverless compute.

## Overview

This repo provides a CLI wrapper for running any Databricks notebook using serverless compute, supporting:
- Notebooks from GitHub repos
- Notebooks from Databricks workspace
- Dynamic requirements.txt dependencies
- Parameterized execution

## Project Structure

```
databricks_notebook/
├── bin/
│   └── run-notebook.sh          # CLI wrapper script
├── notebooks/
│   ├── test_simple.py           # Test: Simple notebook with parameters
│   ├── test_with_deps.py        # Test: Notebook with dependencies
│   └── test_unity_catalog.py   # Test: Notebook accessing Unity Catalog
├── templates/
│   └── job-config-template.json # JSON config template
├── requirements.txt             # Shared dependencies
└── notebooks/requirements-test.txt # Test-specific dependencies
```

## Usage

### Run GitHub repo notebook

```bash
./bin/run-notebook.sh \
  --notebook-path "notebooks/test_simple" \
  --git-url "https://github.com/jdowzard/databricks_notebook" \
  --git-branch "master" \
  --params '{"date": "2025-01-15", "mode": "test"}'
```

### Run with requirements.txt

```bash
./bin/run-notebook.sh \
  --notebook-path "notebooks/test_with_deps" \
  --requirements "requirements.txt" \
  --git-url "https://github.com/jdowzard/databricks_notebook" \
  --git-branch "master"
```

### Run workspace notebook

```bash
./bin/run-notebook.sh \
  --notebook-path "/Users/your.email@company.com/my_notebook" \
  --params '{"param1": "value1"}'
```

## Test Cases

1. **Simple notebook**: Basic parameter passing, no dependencies
2. **With dependencies**: Uses requirements.txt for pip packages
3. **Unity Catalog**: Accesses tables to verify permissions

## Configuration

Uses Databricks CLI profile `exploration` by default (CD49 workspace).

Set environment variable to use different profile:
```bash
export DATABRICKS_PROFILE=exploration
```

## How It Works

Uses `databricks jobs submit` API with:
- **Serverless compute** (no cluster configuration needed)
- **git_source** for GitHub repo notebooks
- **environments** array for pip dependencies
- **base_parameters** for runtime arguments
