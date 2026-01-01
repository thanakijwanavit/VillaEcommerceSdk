# GitHub Actions → AWS Setup (No Access Keys Required)

This setup uses **OIDC (OpenID Connect)** so GitHub Actions can assume an AWS IAM role directly - **no access keys needed!**

## Quick Setup (Automated)

```bash
cd .github
./setup-aws-oidc.sh YOUR_GITHUB_USERNAME VillaEcommerceSdk
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub username or organization name.

The script will:
1. ✅ Create OIDC identity provider in AWS
2. ✅ Create IAM role for GitHub Actions
3. ✅ Attach deployment policy to the role
4. ✅ Output the Role ARN

## Step-by-Step Instructions

### Step 1: Run the Setup Script

```bash
cd .github
./setup-aws-oidc.sh YOUR_GITHUB_USERNAME VillaEcommerceSdk
```

**Example:**
```bash
./setup-aws-oidc.sh myusername VillaEcommerceSdk
```

The script will output something like:
```
Role ARN: arn:aws:iam::123456789012:role/GitHubActionsDeployRole
```

### Step 2: Add Role ARN to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add one secret:
   - **Name**: `AWS_ROLE_ARN`
   - **Value**: `arn:aws:iam::123456789012:role/GitHubActionsDeployRole` (from script output)
5. Click **Add secret**

**That's it!** No access keys needed.

## How It Works

1. **OIDC Provider**: AWS trusts GitHub's identity provider
2. **IAM Role**: GitHub Actions assumes this role using OIDC tokens
3. **Trust Policy**: Role only allows your specific GitHub repository
4. **No Keys**: Everything uses temporary credentials automatically

## Test the Setup

1. Go to **Actions** tab in GitHub
2. Select **Deploy S3 Cache Bucket** workflow
3. Click **Run workflow**
4. Fill in parameters (or use defaults)
5. Click **Run workflow**

The workflow will:
- Authenticate with AWS using OIDC (no keys!)
- Assume the IAM role
- Deploy your S3 bucket

## Manual Setup (If Script Doesn't Work)

See [AWS_SETUP.md](./AWS_SETUP.md) for detailed manual instructions.

## Security Benefits

✅ **No long-lived credentials** - uses temporary tokens  
✅ **Automatic rotation** - tokens expire after each run  
✅ **Repository-specific** - role only works for your repo  
✅ **Auditable** - all actions logged in CloudTrail  

## Troubleshooting

### Error: "Not authorized to perform sts:AssumeRole"

**Check:**
1. Role ARN in GitHub secrets is correct
2. OIDC provider was created successfully
3. Trust policy includes your exact repository name (case-sensitive)

### Error: "OIDC provider not found"

**Solution:** Run the setup script again or create manually:
```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

### Verify Setup

```bash
# Check OIDC provider exists
aws iam list-open-id-connect-providers

# Check role exists
aws iam get-role --role-name GitHubActionsDeployRole

# View trust policy
aws iam get-role --role-name GitHubActionsDeployRole \
  --query 'Role.AssumeRolePolicyDocument'
```

## What Gets Created

- **OIDC Provider**: `token.actions.githubusercontent.com`
- **IAM Role**: `GitHubActionsDeployRole`
- **Policy**: Attached to role with CloudFormation, S3, and IAM permissions
- **Trust Policy**: Only allows your GitHub repository

## Next Steps

After setup, your GitHub Actions workflow will automatically:
- Authenticate with AWS (no keys!)
- Deploy infrastructure
- Clean up after itself

No secrets to rotate, no keys to manage! 🎉

