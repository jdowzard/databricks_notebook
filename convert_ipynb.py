#!/usr/bin/env python3
"""
Jupyter Notebook to Databricks Notebook Converter
Converts .ipynb files to .py format compatible with Databricks
"""

import json
import sys
from pathlib import Path


def convert_ipynb_to_databricks_py(ipynb_path, output_path=None):
    """
    Convert a Jupyter notebook (.ipynb) to Databricks Python format (.py)

    Args:
        ipynb_path: Path to input .ipynb file
        output_path: Path to output .py file (optional, defaults to same name with .py)

    Returns:
        Path to the converted .py file
    """
    ipynb_path = Path(ipynb_path)

    if not ipynb_path.exists():
        raise FileNotFoundError(f"Notebook not found: {ipynb_path}")

    # Read the notebook
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Prepare output path
    if output_path is None:
        output_path = ipynb_path.with_suffix('.py')
    else:
        output_path = Path(output_path)

    # Convert cells
    py_lines = []

    # Add Databricks header
    py_lines.append("# Databricks notebook source")

    for i, cell in enumerate(notebook.get('cells', [])):
        cell_type = cell.get('cell_type')
        source = cell.get('source', [])

        # Ensure source is a list of lines
        if isinstance(source, str):
            source = source.splitlines(keepends=True)

        # Add separator between cells (except before first cell)
        if i > 0:
            py_lines.append("\n# COMMAND ----------\n")
        else:
            py_lines.append("")

        if cell_type == 'markdown':
            # Convert markdown cell to Databricks magic comment
            py_lines.append("# MAGIC %md")
            for line in source:
                # Remove trailing newline and add MAGIC prefix
                line = line.rstrip('\n\r')
                py_lines.append(f"# MAGIC {line}")

        elif cell_type == 'code':
            # Add code cell as-is (strip outputs, we don't need those)
            for line in source:
                # Keep original line including newlines
                py_lines.append(line.rstrip('\n\r'))

        else:
            # Unknown cell type - add as comment
            py_lines.append(f"# Unknown cell type: {cell_type}")

    # Write output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(py_lines))

    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_ipynb.py <notebook.ipynb> [output.py]")
        print("\nConverts Jupyter notebook to Databricks Python format")
        sys.exit(1)

    ipynb_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result_path = convert_ipynb_to_databricks_py(ipynb_path, output_path)
        print(f"✓ Converted: {ipynb_path}")
        print(f"✓ Output: {result_path}")

        # Show preview
        with open(result_path, 'r') as f:
            lines = f.readlines()
            print("\n--- Preview (first 20 lines) ---")
            for i, line in enumerate(lines[:20], 1):
                print(f"{i:3d}: {line.rstrip()}")
            if len(lines) > 20:
                print(f"... ({len(lines) - 20} more lines)")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
