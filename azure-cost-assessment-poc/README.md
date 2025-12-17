# Azure Cost Assessment - Simplified Version

## Overview
Simplified Azure cost assessment tool with just 2 Python files for easy deployment and usage.

## Files
- **azure_cost_assessment.py** - Main assessment tool (single file with all functionality)
- **assessment_config.py** - Configuration and options

## Quick Start

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Configure Azure Credentials
Create a `.env` file in this directory with your Azure credentials:
```
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
```

### 3. Assign Permissions
Your Service Principal needs these roles on your subscription:
- **Reader** - To view subscription and resources
- **Cost Management Reader** - To read cost data

**Using Azure Portal:**
1. Go to Azure Portal → Subscriptions → Your Subscription
2. Click "Access control (IAM)" → "Add role assignment"
3. Assign both roles to your Service Principal

**Using Azure CLI:**
```powershell
az login

az role assignment create --assignee YOUR_CLIENT_ID --role "Reader" --scope /subscriptions/YOUR_SUBSCRIPTION_ID

az role assignment create --assignee YOUR_CLIENT_ID --role "Cost Management Reader" --scope /subscriptions/YOUR_SUBSCRIPTION_ID
```

### 4. Run Assessment
```powershell
python azure_cost_assessment.py
```

## Output
Results are saved in the `output/` directory:
- `cost_assessment_TIMESTAMP.json` - Detailed analysis in JSON format
- `cost_report_TIMESTAMP.txt` - Human-readable report with recommendations

## Customization

Edit `assessment_config.py` to customize:
- Analysis period (default: 30 days)
- Cost breakdown options
- Optimization thresholds
- Report formats

### Example Configurations:
```python
# Quick 7-day scan
from assessment_config import get_quick_scan_config
config = get_quick_scan_config()

# Dev/Test environment
from assessment_config import get_dev_test_config
config = get_dev_test_config()

# Production environment
from assessment_config import get_production_config
config = get_production_config()
```

## What It Does

1. **Connects to Azure** - Authenticates using Service Principal
2. **Collects Cost Data** - Retrieves cost information for specified period
3. **Analyzes Costs** - Breaks down by service and resource group
4. **Generates Recommendations** - Provides optimization suggestions
5. **Creates Reports** - Saves detailed analysis and recommendations

## Troubleshooting

**"AuthorizationFailed" error:**
- Ensure your Service Principal has both Reader and Cost Management Reader roles
- Wait 2-5 minutes for permissions to propagate after assignment

**"No cost data retrieved":**
- Check that your subscription has actual costs in the analysis period
- Verify your credentials are correct in `.env` file

**"Missing Azure credentials":**
- Ensure `.env` file exists and contains all required variables
- Check for typos in environment variable names

## Support
For issues, check the error messages in the console output and refer to the troubleshooting section above.
