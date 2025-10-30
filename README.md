# databricks_notebook

Generalizable Databricks notebook runner using serverless compute.

## Overview

This repo provides a CLI wrapper for running any Databricks notebook using serverless compute, supporting:
- **Local notebook files** - Python (`.py`) or Jupyter (`.ipynb`) - automatically uploaded and cleaned up
- **Jupyter notebook conversion** - `.ipynb` files automatically converted to Databricks format
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
├── convert_ipynb.py             # Jupyter notebook converter
├── notebooks/
│   ├── test_simple.py           # Test: Simple notebook with parameters
│   ├── test_with_deps.py        # Test: Notebook with dependencies
│   └── test_unity_catalog.py   # Test: Notebook accessing Unity Catalog
├── docs/
│   └── index.html               # Full documentation
├── requirements.txt             # Shared dependencies
└── notebooks/requirements-test.txt # Test-specific dependencies
```

## Setup

### Prerequisites

1. **Databricks CLI** - Install and configure the Databricks CLI:
   ```bash
   # Install Databricks CLI
   pip install databricks-cli

   # Configure with your workspace
   databricks configure --profile my-profile-name
   ```

   You'll be prompted for:
   - **Host**: Your Databricks workspace URL (e.g., `https://dbc-xxx.cloud.databricks.com`)
   - **Authentication**: Choose OAuth (recommended) or Personal Access Token

2. **Python 3** (for .ipynb conversion) - Pre-installed on most systems:
   ```bash
   # macOS
   brew install python3

   # Ubuntu/Debian
   sudo apt-get install python3
   ```

3. **jq** (Linux/macOS only) - JSON processor for bash script:
   ```bash
   # macOS
   brew install jq

   # Ubuntu/Debian
   sudo apt-get install jq
   ```

4. **PowerShell** (Windows only) - Comes pre-installed on Windows 10+

### Profile Configuration

The scripts use Databricks CLI profiles from `~/.databrickscfg`. The profile name can be **anything you choose**:

**Default behaviour**: Uses profile named `exploration`

**To use a different profile**, either:

**Option A**: Use `--profile` flag
```bash
./bin/run-notebook.sh --notebook-path ./my_notebook.py --profile production --wait
```

**Option B**: Set environment variable
```bash
export DATABRICKS_PROFILE=production
./bin/run-notebook.sh --notebook-path ./my_notebook.py --wait
```

**Option C**: Rename your profile to `exploration` in `~/.databrickscfg`

### Using From Another Repository

You can use these scripts from any other project:

**Option 1: Clone & Symlink**
```bash
# Clone once
git clone https://github.com/jdowzard/databricks_notebook.git ~/tools/databricks_notebook

# In your project
cd ~/work/my-project
ln -s ~/tools/databricks_notebook/bin/run-notebook.sh ./
ln -s ~/tools/databricks_notebook/bin/run-notebook.ps1 ./
ln -s ~/tools/databricks_notebook/bin/run-notebook.bat ./
```

**Option 2: Copy Scripts**
```bash
# Just copy the 3 scripts
cp ~/tools/databricks_notebook/bin/run-notebook.* ~/work/my-project/
```

**Option 3: Git Submodule**
```bash
cd ~/work/my-project
git submodule add https://github.com/jdowzard/databricks_notebook.git tools/databricks
# Use: ./tools/databricks/bin/run-notebook.sh
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

### Run Jupyter notebook (.ipynb)

**Linux/macOS:**
```bash
./bin/run-notebook.sh \
  --notebook-path "./analysis.ipynb" \
  --wait
```

**Windows (PowerShell):**
```powershell
.\bin\run-notebook.ps1 `
  -NotebookPath ".\analysis.ipynb" `
  -Wait
```

**How it works:**
- `.ipynb` files are automatically detected and converted to Databricks `.py` format
- Markdown cells → `# MAGIC %md` format
- Code cells preserved as-is
- Both the converted `.py` file and temporary workspace file are cleaned up after execution

**Note:** Some Jupyter features won't work in Databricks (ipywidgets, custom extensions), but execution continues gracefully.

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

This repository includes three test notebooks demonstrating different scenarios:

1. **test_simple.py** - Basic parameter passing, no dependencies
2. **test_with_deps.py** - Uses pip dependencies (pandas, requests, python-dateutil) via `%pip` magic commands
3. **test_unity_catalog.py** - Accesses Unity Catalog tables to verify permissions

Run tests:
```bash
./bin/run-notebook.sh \
  --notebook-path "notebooks/test_simple" \
  --git-url "https://github.com/jdowzard/databricks_notebook" \
  --params '{"date": "2025-10-30", "mode": "test"}' \
  --wait
```

## How It Works

Uses `databricks jobs submit` API with:
- **Serverless compute** (no cluster configuration needed)
- **Local file upload** to `/Users/{username}/.tmp/` for local notebooks
- **git_source** for GitHub repo notebooks
- **base_parameters** for runtime arguments
- **Automatic cleanup** of temporary notebooks when using `--wait`

### Execution Flow

1. **Local notebooks**: Upload to workspace → Execute → Cleanup (with `--wait`)
2. **GitHub notebooks**: Clone repo → Execute on serverless compute
3. **Workspace notebooks**: Execute directly from existing workspace location

## Known Limitations & Edge Cases

### File Types
- **Supported**:
  - Python notebooks (`.py` files with Databricks magic commands)
  - Jupyter notebooks (`.ipynb` - automatically converted)
- **Jupyter conversion support**:
  - ✅ Standard code cells
  - ✅ Markdown cells (tables, LaTeX, HTML)
  - ✅ Jupyter magics (preserved but may not execute: `%time`, `%%bash`, etc.)
  - ⚠️ ipywidgets - Databricks handles gracefully (no execution failure)
  - ❌ Jupyter extensions/custom magics - Not supported
  - ❌ Out-of-order execution - Databricks runs sequentially
- **Not supported**: `.sql`, `.scala`, `.r` files (PRs welcome!)

### Dependencies
- **Notebook tasks**: Must use `%pip install` magic commands within the notebook
- **`--requirements` flag**: Ignored for notebook tasks with serverless compute
- **Limitation**: Databricks API doesn't support `environments` array for notebook tasks

### Authentication
- Requires Databricks CLI configured with valid credentials
- **Token expiration**: Long-running jobs may fail if token expires mid-execution
- **Private GitHub repos**: Databricks workspace must have git credentials configured

### Permissions
- Requires workspace permissions to:
  - Create/delete files in your user directory (`/Users/{username}/`)
  - Submit jobs with serverless compute
  - Access Unity Catalog (if notebooks use it)

### Cleanup
- **With `--wait`**: Automatic cleanup after job completion
- **Without `--wait`**: Manual cleanup required
- **On failure**: Temporary files are cleaned up if job fails
- **Interrupted execution**: If script is killed, temp files may remain - clean up manually:
  ```bash
  databricks workspace delete --profile exploration /Users/your.email/.tmp/notebook-xxxxx.py
  ```

### Performance
- **Cold starts**: First run may take 30-60 seconds for serverless compute provisioning
- **Concurrent runs**: Multiple simultaneous runs are supported
- **Large notebooks**: No size limit, but upload time increases with file size

### Platform-Specific
- **Windows**: Requires PowerShell 5.0+ (comes with Windows 10+)
- **Linux/macOS**: Requires `jq` installed for JSON parsing
- **Line endings**: Scripts handle CRLF/LF automatically

### Error Handling
- **Job failures**: Exit code 1 with error message from Databricks
- **Upload failures**: Script exits immediately with error
- **Network issues**: May require retry - no automatic retry implemented
- **Invalid JSON params**: Databricks will reject the job submission

## Troubleshooting

**"jq: command not found"**
```bash
brew install jq  # macOS
sudo apt-get install jq  # Linux
```

**"databricks: command not found"**
```bash
pip install databricks-cli
databricks configure --profile my-profile
```

**"The parent folder does not exist"**
- First run creates `.tmp` directory automatically
- If error persists, manually create: `databricks workspace mkdirs /Users/your.email/.tmp`

**"No View permissions"**
- Check your workspace permissions
- Try using a different profile with `--profile` flag

**Job stuck in "PENDING"**
- Serverless compute may be provisioning resources
- Check Databricks UI for detailed status
- May take up to 60 seconds for cold start
