# Quick Start: Deploy Villa SDK Cache Bucket

## Deployment Options

### Option 1: GitHub Actions (Easiest)

1. Go to **Actions** tab → **Deploy S3 Cache Bucket**
2. Click **Run workflow**
3. Use defaults or customize parameters
4. Click **Run workflow**

### Option 2: SAM CLI

```bash
cd python
sam build && sam deploy --guided
```

When prompted:
- Stack name: `villa-sdk-cache`
- Region: `us-east-1` (or your preferred region)
- Confirm changes: `Y`
- Allow SAM CLI IAM role creation: `Y`

## What Gets Created

✅ S3 Bucket: `villa-ecommerce-sdk-cache`
- Encryption enabled
- Versioning enabled  
- Public access blocked
- Lifecycle rules (30-day retention)

✅ IAM Policy: `VillaSDKCacheAccessPolicy`
- Ready to attach to your IAM users/roles

## After Deployment

### 1. Get the Policy ARN

```bash
aws cloudformation describe-stacks \
  --stack-name villa-sdk-cache \
  --query 'Stacks[0].Outputs[?OutputKey==`PolicyArn`].OutputValue' \
  --output text
```

### 2. Attach to Your IAM User

```bash
aws iam attach-user-policy \
  --user-name YOUR_USERNAME \
  --policy-arn <POLICY_ARN_FROM_STEP_1>
```

### 3. Use the SDK

```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")
products_df = client.get_product_list(branch=1000)
```

## Files Created

- `template.yaml` - SAM template for deployment
- `.github/workflows/deploy-s3-cache.yml` - GitHub Actions workflow
- `samconfig.toml` - SAM configuration (optional)
- `DEPLOY.md` - Detailed deployment guide
- `S3_SETUP.md` - Manual setup guide (alternative to SAM)

## Need Help?

See `DEPLOY.md` for detailed instructions and troubleshooting.

