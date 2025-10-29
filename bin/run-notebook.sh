#!/bin/bash

# Databricks Notebook Runner - Serverless Compute
# Usage: run-notebook.sh --notebook-path <path> [options]

set -e

# Default values
DATABRICKS_PROFILE="${DATABRICKS_PROFILE:-exploration}"
NOTEBOOK_PATH=""
REQUIREMENTS_PATH=""
PARAMS="{}"
GIT_URL=""
GIT_BRANCH="master"
RUN_NAME="Notebook Run $(date +%Y%m%d-%H%M%S)"
WAIT_FOR_COMPLETION=false
VERBOSE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

show_usage() {
    cat << EOF
Databricks Notebook Runner - Serverless Compute

Usage: $0 --notebook-path <path> [options]

Required:
  --notebook-path PATH        Path to notebook (relative for git, absolute for workspace)

Optional:
  --requirements PATH         Path to requirements.txt file (local or workspace)
  --params JSON               JSON string of parameters (default: {})
  --git-url URL              GitHub repository URL
  --git-branch BRANCH        Git branch/tag/commit (default: master)
  --run-name NAME            Custom run name
  --profile PROFILE          Databricks profile (default: exploration)
  --wait                     Wait for run to complete
  --verbose                  Show verbose output

Examples:
  # Run GitHub repo notebook
  $0 --notebook-path "notebooks/test_simple" \\
     --git-url "https://github.com/jdowzard/databricks_notebook" \\
     --params '{"date": "2025-01-15"}'

  # Run with requirements.txt
  $0 --notebook-path "notebooks/test_with_deps" \\
     --requirements "requirements.txt" \\
     --git-url "https://github.com/jdowzard/databricks_notebook"

  # Run workspace notebook
  $0 --notebook-path "/Users/you@company.com/my_notebook"

EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --notebook-path) NOTEBOOK_PATH="$2"; shift 2 ;;
    --requirements) REQUIREMENTS_PATH="$2"; shift 2 ;;
    --params) PARAMS="$2"; shift 2 ;;
    --git-url) GIT_URL="$2"; shift 2 ;;
    --git-branch) GIT_BRANCH="$2"; shift 2 ;;
    --run-name) RUN_NAME="$2"; shift 2 ;;
    --profile) DATABRICKS_PROFILE="$2"; shift 2 ;;
    --wait) WAIT_FOR_COMPLETION=true; shift ;;
    --verbose) VERBOSE=true; shift ;;
    -h|--help) show_usage; exit 0 ;;
    *) log_error "Unknown option: $1"; show_usage; exit 1 ;;
  esac
done

# Validate required args
if [ -z "$NOTEBOOK_PATH" ]; then
  log_error "--notebook-path is required"
  show_usage
  exit 1
fi

log_info "Databricks Profile: $DATABRICKS_PROFILE"
log_info "Notebook Path: $NOTEBOOK_PATH"

# Handle requirements.txt
DEPENDENCIES="[]"
if [ -n "$REQUIREMENTS_PATH" ]; then
  if [ -f "$REQUIREMENTS_PATH" ]; then
    # Local file - need to upload to workspace
    WORKSPACE_REQ_PATH="/Workspace/tmp/requirements-$(date +%s).txt"
    log_info "Uploading $REQUIREMENTS_PATH to $WORKSPACE_REQ_PATH..."

    if databricks workspace import --profile "$DATABRICKS_PROFILE" "$REQUIREMENTS_PATH" "$WORKSPACE_REQ_PATH" --overwrite 2>/dev/null; then
      log_success "Requirements file uploaded"
      DEPENDENCIES="[\"-r $WORKSPACE_REQ_PATH\"]"
    else
      log_warn "Failed to upload requirements.txt, will try to use it from git repo"
      DEPENDENCIES="[\"-r $REQUIREMENTS_PATH\"]"
    fi
  else
    # Assume it's already a workspace/volume/cloud path or relative path in git repo
    log_info "Using requirements path: $REQUIREMENTS_PATH"
    DEPENDENCIES="[\"-r $REQUIREMENTS_PATH\"]"
  fi
fi

# Build JSON config
if [ -n "$GIT_URL" ]; then
  log_info "Mode: GitHub Repository"
  log_info "Git URL: $GIT_URL"
  log_info "Git Branch: $GIT_BRANCH"

  # GitHub repo notebook
  CONFIG=$(cat <<EOF
{
  "run_name": "$RUN_NAME",
  "git_source": {
    "git_url": "$GIT_URL",
    "git_provider": "gitHub",
    "git_branch": "$GIT_BRANCH"
  },
  "tasks": [{
    "task_key": "notebook_task",
    "notebook_task": {
      "notebook_path": "$NOTEBOOK_PATH",
      "base_parameters": $PARAMS
    },
    "environment_key": "default"
  }],
  "environments": [{
    "environment_key": "default",
    "spec": {
      "client": "1",
      "dependencies": $DEPENDENCIES
    }
  }]
}
EOF
)
else
  log_info "Mode: Workspace Notebook"

  # Workspace notebook
  CONFIG=$(cat <<EOF
{
  "run_name": "$RUN_NAME",
  "tasks": [{
    "task_key": "notebook_task",
    "notebook_task": {
      "notebook_path": "$NOTEBOOK_PATH",
      "base_parameters": $PARAMS
    },
    "environment_key": "default"
  }],
  "environments": [{
    "environment_key": "default",
    "spec": {
      "client": "1",
      "dependencies": $DEPENDENCIES
    }
  }]
}
EOF
)
fi

# Show config if verbose
if [ "$VERBOSE" = true ]; then
  log_info "Job configuration:"
  echo "$CONFIG" | jq '.'
fi

# Submit job
log_info "Submitting job to Databricks..."

SUBMIT_RESULT=$(echo "$CONFIG" | databricks jobs submit --profile "$DATABRICKS_PROFILE" --json @/dev/stdin)

if [ $? -ne 0 ]; then
  log_error "Failed to submit job"
  exit 1
fi

# Extract run ID
RUN_ID=$(echo "$SUBMIT_RESULT" | jq -r '.run_id')

log_success "Job submitted successfully!"
log_info "Run ID: $RUN_ID"
log_info "Run Name: $RUN_NAME"

# Get workspace URL
WORKSPACE_URL=$(databricks auth describe --profile "$DATABRICKS_PROFILE" | grep "^Host:" | awk '{print $2}')
log_info "View run: ${WORKSPACE_URL}#job/0/run/${RUN_ID}"

# Wait for completion if requested
if [ "$WAIT_FOR_COMPLETION" = true ]; then
  log_info "Waiting for run to complete..."

  databricks runs wait --profile "$DATABRICKS_PROFILE" --run-id "$RUN_ID"

  # Get final status
  FINAL_STATUS=$(databricks runs get --profile "$DATABRICKS_PROFILE" --run-id "$RUN_ID" | jq -r '.state.result_state')

  if [ "$FINAL_STATUS" = "SUCCESS" ]; then
    log_success "Run completed successfully!"
    exit 0
  else
    log_error "Run failed with status: $FINAL_STATUS"
    exit 1
  fi
else
  log_info "Use --wait to wait for completion, or check status with:"
  echo "  databricks runs get --profile $DATABRICKS_PROFILE --run-id $RUN_ID"
fi
