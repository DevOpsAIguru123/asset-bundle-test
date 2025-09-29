# Databricks Asset Bundle - Environment-Specific Deployment

This project demonstrates how to deploy a Python job to different Databricks workspaces with environment-specific output using Databricks Asset Bundles.

## Project Structure

```
asset-bundle-test/
├── databricks.yml                 # Main bundle configuration
├── resources/
│   ├── jobs/
│   │   └── demo_job.yml          # Job definition
│   └── src/
│       └── demo.py               # Python script
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions workflow
└── README.md
```

## Environment-Specific Output

The Python script will display different messages based on the deployment environment:

- **dev**: "Hello World Dev"
- **test**: "Hello World Test"
- **default**: "Hello World Default"

## Setup Instructions

### 1. Update Workspace URLs

In `databricks.yml`, update the workspace URLs for your environments:

```yaml
targets:
  dev:
    workspace:
      host: https://your-dev-workspace.cloud.databricks.com/
  test:
    workspace:
      host: https://your-test-workspace.cloud.databricks.com/
```

### 2. GitHub Secrets Configuration

Add the following secrets to your GitHub repository:

- `DATABRICKS_DEV_HOST`: Your dev workspace URL
- `DATABRICKS_DEV_TOKEN`: Personal access token for dev workspace
- `DATABRICKS_TEST_HOST`: Your test workspace URL  
- `DATABRICKS_TEST_TOKEN`: Personal access token for test workspace

### 3. Branch-Based Deployment

The GitHub Actions workflow deploys based on branch names:

- Push to `dev` branch → deploys to dev environment
- Push to `test` branch → deploys to test environment
- Push to `main` branch → deploys to dev environment (default)

## Local Development

### Prerequisites

- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html) installed
- Databricks workspace access

### Commands

```bash
# Validate the bundle
databricks bundle validate -t dev

# Deploy to dev environment
databricks bundle deploy -t dev

# Deploy to test environment  
databricks bundle deploy -t test

# Run the job
databricks bundle run demo_serverless_job -t dev
```

## How It Works

1. **Variables**: The `databricks.yml` defines environment-specific variables in each target
2. **Environment Variables**: The job configuration passes the variable as an environment variable to the Python script
3. **Python Script**: Reads the `ENVIRONMENT_MESSAGE` environment variable and prints it
4. **GitHub Actions**: Automatically deploys to the appropriate environment based on the branch

## Key Files Explained

### databricks.yml
- Defines two targets: `dev` and `test`
- Each target has its own `environment_message` variable
- Variables are referenced in job configurations using `${var.environment_message}`

### demo_job.yml
- Configures the Spark Python task
- Sets environment variables in the `environments.spec.environment_variables` section
- References the bundle variable using `${var.environment_message}`

### demo.py
- Reads the `ENVIRONMENT_MESSAGE` environment variable
- Falls back to "Hello World Default" if not set
- Prints the appropriate message based on the environment

This approach provides a clean, maintainable way to handle environment-specific configurations in Databricks Asset Bundles.
