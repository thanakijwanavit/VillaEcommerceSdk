# Deploying Villa SDK Cache Bucket with SAM

This guide shows you how to deploy the S3 bucket for Villa Ecommerce SDK caching using AWS SAM.

## Prerequisites

1. **AWS CLI** installed and configured
2. **SAM CLI** installed (`pip install aws-sam-cli` or via Homebrew)
3. **AWS credentials** configured (via `aws configure` or environment variables)

## Deployment Options

### Option 1: GitHub Actions (Recommended)

The easiest way to deploy is using GitHub Actions:

1. **Set up AWS credentials in GitHub Secrets:**
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add secret: `AWS_ROLE_ARN` (ARN of IAM role for GitHub Actions)

2. **Deploy via GitHub Actions:**
   - Go to Actions tab → "Deploy S3 Cache Bucket"
   - Click "Run workflow"
   - Fill in parameters (or use defaults)
   - Click "Run workflow"

The workflow will:
- Validate the template
- Build and deploy the stack
- Output the policy ARN for attaching to IAM users/roles

### Option 2: Using SAM CLI with samconfig.toml

```bash
cd python

# Build and deploy
sam build
sam deploy --guided
```

The `--guided` flag will prompt you for:
- Stack name: `villa-sdk-cache` (or your choice)
- AWS Region: `us-east-1` (or your preferred region)
- Confirm changes before deploy: `Y`
- Allow SAM CLI IAM role creation: `Y`
- Disable rollback: `N` (recommended)

### Option 3: Deploy with Custom Parameters

```bash
cd python

sam build

sam deploy \
  --stack-name villa-sdk-cache \
  --capabilities CAPABILITY_IAM \
  --region us-east-1 \
  --template template.yaml \
  --parameter-overrides \
    BucketName=villa-ecommerce-sdk-cache \
    EnableVersioning=true \
    EnableLifecycleRules=true \
    CacheRetentionDays=30 \
  --confirm-changeset
```

## Parameters

The template supports the following parameters:

- **BucketName** (default: `villa-ecommerce-sdk-cache`): Name of the S3 bucket
- **EnableVersioning** (default: `true`): Enable versioning on the bucket
- **EnableLifecycleRules** (default: `true`): Enable automatic deletion of old cache files
- **CacheRetentionDays** (default: `30`): Number of days to retain cache files

## What Gets Created

1. **S3 Bucket**: `villa-ecommerce-sdk-cache`
   - Server-side encryption (AES256)
   - Versioning enabled
   - Public access blocked
   - Lifecycle rules (optional)

2. **IAM Managed Policy**: `VillaSDKCacheAccessPolicy`
   - Grants S3 permissions for cache operations
   - Can be attached to IAM users/roles

3. **Bucket Policy**: Allows IAM principals in your account to access the bucket

## After Deployment

### 1. Attach Policy to IAM User

```bash
# Get the policy ARN from stack outputs
POLICY_ARN=$(aws cloudformation describe-stacks \
  --stack-name villa-sdk-cache \
  --query 'Stacks[0].Outputs[?OutputKey==`PolicyArn`].OutputValue' \
  --output text)

# Attach to IAM user
aws iam attach-user-policy \
  --user-name YOUR_IAM_USER \
  --policy-arn $POLICY_ARN
```

### 2. Attach Policy to IAM Role

```bash
# Attach to IAM role (for EC2, Lambda, etc.)
aws iam attach-role-policy \
  --role-name YOUR_IAM_ROLE \
  --policy-arn $POLICY_ARN
```

### 3. Use the Bucket

```python
from villa_ecommerce_sdk import VillaClient

# The bucket name is: villa-ecommerce-sdk-cache
client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")
products_df = client.get_product_list(branch=1000)
```

## View Stack Outputs

```bash
aws cloudformation describe-stacks \
  --stack-name villa-sdk-cache \
  --query 'Stacks[0].Outputs'
```

## Update Stack

To update the stack with new parameters:

```bash
sam build
sam deploy \
  --stack-name villa-sdk-cache \
  --capabilities CAPABILITY_IAM \
  --template template.yaml \
  --parameter-overrides \
    BucketName=villa-ecommerce-sdk-cache \
    CacheRetentionDays=60  # Changed from 30 to 60 days
```

Or use GitHub Actions workflow with updated parameters.

## Delete Stack

To delete the stack and all resources:

```bash
sam delete --stack-name villa-sdk-cache
```

**Warning**: This will delete the bucket and all cached data. Make sure you have backups if needed.

## Troubleshooting

### Error: Bucket name already exists

The bucket name `villa-ecommerce-sdk-cache` must be globally unique. If it's taken:
1. Choose a different name in the `BucketName` parameter
2. Or delete the existing bucket first (if it's yours)

### Error: Insufficient permissions

Ensure your AWS credentials have:
- `s3:CreateBucket`
- `s3:PutBucketPolicy`
- `s3:PutBucketVersioning`
- `iam:CreatePolicy`
- `iam:AttachRolePolicy` (if attaching to roles)

### Error: Stack already exists

If the stack exists, use `sam deploy` to update it, or delete it first:
```bash
aws cloudformation delete-stack --stack-name villa-sdk-cache
```

## Cost Estimation

- **Storage**: ~$0.023 per GB/month
- **Requests**: Minimal (thousands of requests cost cents)
- **Estimated monthly cost**: < $1 for typical usage

## Security Notes

- Bucket has public access blocked
- Encryption enabled by default
- Only IAM principals in your account can access
- Consider adding IP restrictions if accessing from fixed locations

