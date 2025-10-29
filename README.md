# databricks_notebook

Generalizable Databricks notebook runner using serverless compute.

## Overview

This repo provides a CLI wrapper for running any Databricks notebook using serverless compute, supporting:
- **Local notebook files** (automatically uploaded and cleaned up)
- Notebooks from GitHub repos
- Notebooks from Databricks workspace
- Dynamic requirements.txt dependencies
- Parameterized execution

## Project Structure

```
databricks_notebook/
├── bin/
│   ├── run-notebook.sh          # CLI wrapper script (Linux/macOS)
│   ├── run-notebook.ps1         # PowerShell script (Windows)
│   └── run-notebook.bat         # Batch wrapper (Windows)
├── notebooks/
│   ├── test_simple.py           # Test: Simple notebook with parameters
│   ├── test_with_deps.py        # Test: Notebook with dependencies
│   └── test_unity_catalog.py   # Test: Notebook accessing Unity Catalog
├── docs/
│   └── index.html               # Full documentation
├── requirements.txt             # Shared dependencies
└── notebooks/requirements-test.txt # Test-specific dependencies
```

## Usage

### Run local notebook file

**Linux/macOS:**
```bash
./bin/run-notebook.sh \
  --notebook-path "./my_local_notebook.py" \
  --params '{"date": "2025-10-30", "mode": "test"}' \
  --wait
```

**Windows (PowerShell):**
```powershell
.\bin\run-notebook.ps1 `
  -NotebookPath ".\my_local_notebook.py" `
  -Params '{"date": "2025-10-30", "mode": "test"}' `
  -Wait
```

**Note:** Local notebooks are automatically uploaded to your workspace (`/Users/your.email/.tmp/`), executed, and then cleaned up when using the `--wait` flag. Without `--wait`, manual cleanup is required.

### Run GitHub repo notebook

**Linux/macOS:**
```bash
./bin/run-notebook.sh \
  --notebook-path "notebooks/test_simple" \
  --git-url "https://github.com/jdowzard/databricks_notebook" \
  --git-branch "master" \
  --params '{"date": "2025-01-15", "mode": "test"}'
```

**Windows (PowerShell):**
```powershell
.\bin\run-notebook.ps1 `
  -NotebookPath "notebooks/test_simple" `
  -GitUrl "https://github.com/jdowzard/databricks_notebook" `
  -GitBranch "master" `
  -Params '{"date": "2025-01-15", "mode": "test"}'
```

**Windows (Command Prompt):**
```cmd
bin\run-notebook.bat --notebook-path "notebooks/test_simple" --git-url "https://github.com/jdowzard/databricks_notebook" --git-branch "master" --params "{\"date\": \"2025-01-15\", \"mode\": \"test\"}"
```

### Run with requirements.txt

**Linux/macOS:**
```bash
./bin/run-notebook.sh \
  --notebook-path "notebooks/test_with_deps" \
  --requirements "requirements.txt" \
  --git-url "https://github.com/jdowzard/databricks_notebook" \
  --git-branch "master"
```

**Windows (PowerShell):**
```powershell
.\bin\run-notebook.ps1 `
  -NotebookPath "notebooks/test_with_deps" `
  -Requirements "requirements.txt" `
  -GitUrl "https://github.com/jdowzard/databricks_notebook" `
  -GitBranch "master"
```

### Run workspace notebook

**Linux/macOS:**
```bash
./bin/run-notebook.sh \
  --notebook-path "/Users/your.email@company.com/my_notebook" \
  --params '{"param1": "value1"}'
```

**Windows (PowerShell):**
```powershell
.\bin\run-notebook.ps1 `
  -NotebookPath "/Users/your.email@company.com/my_notebook" `
  -Params '{"param1": "value1"}'
```

## Test Cases

1. **Simple notebook**: Basic parameter passing, no dependencies
2. **With dependencies**: Uses requirements.txt for pip packages
3. **Unity Catalog**: Accesses tables to verify permissions

## Configuration

Uses Databricks CLI profile `exploration` by default (CD49 workspace).

Set environment variable to use different profile:

**Linux/macOS:**
```bash
export DATABRICKS_PROFILE=exploration
```

**Windows (PowerShell):**
```powershell
$env:DATABRICKS_PROFILE="exploration"
```

**Windows (Command Prompt):**
```cmd
set DATABRICKS_PROFILE=exploration
```

## How It Works

Uses `databricks jobs submit` API with:
- **Serverless compute** (no cluster configuration needed)
- **git_source** for GitHub repo notebooks
- **environments** array for pip dependencies
- **base_parameters** for runtime arguments
