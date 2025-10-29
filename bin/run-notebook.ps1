#!/usr/bin/env pwsh
# Databricks Notebook Runner - Serverless Compute
# Usage: run-notebook.ps1 -NotebookPath <path> [options]

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$NotebookPath,

    [Parameter(Mandatory=$false)]
    [string]$Requirements = "",

    [Parameter(Mandatory=$false)]
    [string]$Params = "{}",

    [Parameter(Mandatory=$false)]
    [string]$GitUrl = "",

    [Parameter(Mandatory=$false)]
    [string]$GitBranch = "master",

    [Parameter(Mandatory=$false)]
    [string]$RunName = "",

    [Parameter(Mandatory=$false)]
    [string]$Profile = "",

    [Parameter(Mandatory=$false)]
    [switch]$Wait,

    [Parameter(Mandatory=$false)]
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# Default values
if (-not $Profile) {
    $Profile = if ($env:DATABRICKS_PROFILE) { $env:DATABRICKS_PROFILE } else { "exploration" }
}

if (-not $RunName) {
    $RunName = "Notebook Run " + (Get-Date -Format "yyyyMMdd-HHmmss")
}

# Helper functions for colored output
function Write-Info {
    param([string]$Message)
    Write-Host "ℹ " -ForegroundColor Blue -NoNewline
    Write-Host $Message
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ " -ForegroundColor Green -NoNewline
    Write-Host $Message
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "✗ " -ForegroundColor Red -NoNewline
    Write-Host $Message
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ " -ForegroundColor Yellow -NoNewline
    Write-Host $Message
}

# Cleanup function for temporary notebook
function Cleanup-TempNotebook {
    param(
        [string]$Profile,
        [string]$TempPath,
        [bool]$ShouldCleanup
    )

    if ($ShouldCleanup -and $TempPath) {
        Write-Info "Cleaning up temporary notebook..."
        try {
            databricks workspace delete --profile $Profile $TempPath 2>$null
            Write-Success "Temporary notebook deleted: $TempPath"
        }
        catch {
            Write-Warning "Failed to delete temporary notebook: $TempPath"
        }
    }
}

Write-Info "Databricks Profile: $Profile"
Write-Info "Notebook Path: $NotebookPath"

# Handle local notebook files
$TempNotebookPath = ""
$CleanupNotebook = $false

# Check if notebook path is a local file
if (Test-Path $NotebookPath -PathType Leaf) {
    Write-Info "Mode: Local Notebook File"
    Write-Info "Detected local notebook, uploading to workspace..."

    # Get current user for workspace path
    $CurrentUser = (databricks current-user me --profile $Profile -o json | ConvertFrom-Json).userName

    # Ensure .tmp directory exists
    $TmpDir = "/Users/$CurrentUser/.tmp"
    databricks workspace mkdirs --profile $Profile $TmpDir 2>$null | Out-Null

    # Generate temp workspace path
    $Timestamp = [int][double]::Parse((Get-Date -UFormat %s))
    $Basename = Split-Path -Leaf $NotebookPath
    $TempNotebookPath = "$TmpDir/notebook-$Timestamp-$Basename"

    # Upload notebook to workspace
    try {
        databricks workspace import --profile $Profile --file $NotebookPath --language PYTHON --format SOURCE --overwrite $TempNotebookPath 2>&1 | Out-Null
        Write-Success "Notebook uploaded to: $TempNotebookPath"
        $NotebookPath = $TempNotebookPath
        $CleanupNotebook = $true
    }
    catch {
        Write-ErrorMsg "Failed to upload local notebook to workspace"
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit 1
    }
}

# Handle requirements.txt
$Dependencies = "[]"
if ($Requirements) {
    if (Test-Path $Requirements) {
        # Local file - need to upload to workspace
        $Timestamp = [int][double]::Parse((Get-Date -UFormat %s))
        $WorkspaceReqPath = "/Workspace/tmp/requirements-$Timestamp.txt"
        Write-Info "Uploading $Requirements to $WorkspaceReqPath..."

        try {
            databricks workspace import --profile $Profile --file $Requirements --format AUTO --overwrite $WorkspaceReqPath 2>$null
            Write-Success "Requirements file uploaded"
            $Dependencies = "[`"-r $WorkspaceReqPath`"]"
        }
        catch {
            Write-Warning "Failed to upload requirements.txt, will try to use it from git repo"
            $Dependencies = "[`"-r $Requirements`"]"
        }
    }
    else {
        # Assume it's already a workspace/volume/cloud path or relative path in git repo
        Write-Info "Using requirements path: $Requirements"
        $Dependencies = "[`"-r $Requirements`"]"
    }
}

# Build JSON config
# Note: For notebook tasks with serverless compute, we cannot use the environments array
# Dependencies must be installed via %pip magic commands in the notebook itself
if ($GitUrl) {
    Write-Info "Mode: GitHub Repository"
    Write-Info "Git URL: $GitUrl"
    Write-Info "Git Branch: $GitBranch"

    if ($Requirements) {
        Write-Warning "Note: requirements.txt will be ignored for notebook tasks"
        Write-Warning "Use %pip magic commands in your notebook instead"
    }

    # GitHub repo notebook
    $Config = @{
        run_name = $RunName
        git_source = @{
            git_url = $GitUrl
            git_provider = "gitHub"
            git_branch = $GitBranch
        }
        tasks = @(
            @{
                task_key = "notebook_task"
                notebook_task = @{
                    notebook_path = $NotebookPath
                    base_parameters = $Params | ConvertFrom-Json
                }
            }
        )
    } | ConvertTo-Json -Depth 10 -Compress
}
else {
    Write-Info "Mode: Workspace Notebook"

    if ($Requirements) {
        Write-Warning "Note: requirements.txt will be ignored for notebook tasks"
        Write-Warning "Use %pip magic commands in your notebook instead"
    }

    # Workspace notebook
    $Config = @{
        run_name = $RunName
        tasks = @(
            @{
                task_key = "notebook_task"
                notebook_task = @{
                    notebook_path = $NotebookPath
                    base_parameters = $Params | ConvertFrom-Json
                }
            }
        )
    } | ConvertTo-Json -Depth 10 -Compress
}

# Show config if verbose
if ($Verbose) {
    Write-Info "Job configuration:"
    $Config | ConvertFrom-Json | ConvertTo-Json -Depth 10
}

# Submit job
Write-Info "Submitting job to Databricks..."

try {
    # Create temp file for JSON config
    $TempFile = New-TemporaryFile
    $Config | Out-File -FilePath $TempFile.FullName -Encoding UTF8

    # Submit job
    $SubmitResult = Get-Content $TempFile.FullName | databricks jobs submit --profile $Profile --json '@/dev/stdin' | ConvertFrom-Json

    Remove-Item $TempFile.FullName -Force
}
catch {
    Write-ErrorMsg "Failed to submit job"
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Extract run ID and URL
$RunId = $SubmitResult.run_id
$RunPageUrl = $SubmitResult.run_page_url

Write-Success "Job submitted successfully!"
Write-Info "Run ID: $RunId"
Write-Info "Run Name: $RunName"
Write-Info "View run: $RunPageUrl"

# Wait for completion if requested
if ($Wait) {
    Write-Info "Waiting for run to complete..."

    # Poll for completion
    while ($true) {
        $RunStatus = databricks jobs get-run --profile $Profile $RunId -o json | ConvertFrom-Json
        $Status = $RunStatus.state.life_cycle_state

        if ($Status -in @("TERMINATED", "SKIPPED", "INTERNAL_ERROR")) {
            break
        }

        Write-Host "." -NoNewline
        Start-Sleep -Seconds 5
    }

    Write-Host ""

    # Get final status
    $FinalRunStatus = databricks jobs get-run --profile $Profile $RunId -o json | ConvertFrom-Json
    $FinalStatus = $FinalRunStatus.state.result_state

    if ($FinalStatus -eq "SUCCESS") {
        Write-Success "Run completed successfully!"
        Cleanup-TempNotebook -Profile $Profile -TempPath $TempNotebookPath -ShouldCleanup $CleanupNotebook
        exit 0
    }
    else {
        Write-ErrorMsg "Run failed with status: $FinalStatus"
        $StateMsg = $FinalRunStatus.state.state_message
        if ($StateMsg) {
            Write-ErrorMsg "Error message: $StateMsg"
        }
        Cleanup-TempNotebook -Profile $Profile -TempPath $TempNotebookPath -ShouldCleanup $CleanupNotebook
        exit 1
    }
}
else {
    Write-Info "Use -Wait to wait for completion, or check status with:"
    Write-Host "  databricks jobs get-run --profile $Profile $RunId"
    Write-Warning "Note: Temporary notebook will not be cleaned up without -Wait flag"
    if ($CleanupNotebook) {
        Write-Warning "Manual cleanup required: databricks workspace delete --profile $Profile $TempNotebookPath"
    }
}
