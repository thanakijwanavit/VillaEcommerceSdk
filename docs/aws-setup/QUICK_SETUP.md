# Quick Setup: GitHub Actions → AWS (No Access Keys!)

This setup uses **OIDC** so GitHub Actions can assume an AWS role directly - **no access keys needed!**

## Quick Setup

```bash
cd .github
./setup-aws-oidc.sh YOUR_GITHUB_USERNAME VillaEcommerceSdk
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub username or organization name.

The script will:
1. Create OIDC provider in AWS
2. Create IAM role for GitHub Actions
3. Attach deployment policy
4. Output the Role ARN

Then add **ONE secret** to GitHub:
- Go to Repository → Settings → Secrets → Actions
- Add secret: `AWS_ROLE_ARN` = (the ARN from script output)

**That's it!** No access keys to manage.

## How It Works

GitHub Actions uses OIDC tokens to assume the AWS IAM role. The role is configured to only work for your specific repository. No long-lived credentials needed!

## Test

1. Go to **Actions** tab
2. Select **Deploy S3 Cache Bucket**
3. Click **Run workflow**

## Detailed Instructions

See [SETUP.md](./SETUP.md) for step-by-step guide.

## Alternative: IAM Access Keys

If you prefer access keys (not recommended), see [AWS_IAM_SETUP.md](./AWS_IAM_SETUP.md).

## Quick Test

After setup, test the workflow:
1. Go to **Actions** tab
2. Select **Deploy S3 Cache Bucket**
3. Click **Run workflow**
4. Use defaults or customize
5. Click **Run workflow**

## Troubleshooting

If you get "Not authorized" errors:
- Verify the Role ARN in GitHub secrets matches the output
- Check the trust policy includes your repo name correctly
- Ensure the OIDC provider was created successfully

See [AWS_SETUP.md](./AWS_SETUP.md) for detailed troubleshooting.
