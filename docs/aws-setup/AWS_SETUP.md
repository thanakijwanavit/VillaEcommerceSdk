# GitHub Actions AWS Setup Guide

This guide shows you how to configure GitHub Actions to deploy to AWS using OIDC (OpenID Connect) authentication. This is the secure, recommended method that doesn't require storing AWS access keys.

## Prerequisites

- AWS CLI installed and configured
- AWS account with permissions to create IAM roles and policies
- GitHub repository access

## Step 1: Create OIDC Identity Provider in AWS

GitHub Actions uses OIDC to authenticate with AWS. First, create an OIDC identity provider:

### Option A: Using AWS Console

1. Go to **IAM Console** → **Identity providers** → **Add provider**
2. Select **OpenID Connect**
3. Provider URL: `https://token.actions.githubusercontent.com`
4. Audience: `sts.amazonaws.com`
5. Click **Add provider**

### Option B: Using AWS CLI

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1 \
  --region us-east-1
```

**Note**: The thumbprint may need to be updated. Get the latest from:
```bash
openssl s_client -servername token.actions.githubusercontent.com -showcerts -connect token.actions.githubusercontent.com:443 < /dev/null 2>/dev/null | openssl x509 -fingerprint -noout -sha1 | tr ':' ' ' | awk '{print $2}'
```

## Step 2: Create IAM Role for GitHub Actions

Create an IAM role that GitHub Actions can assume:

### Create Trust Policy

Save this as `github-actions-trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::YOUR_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_USERNAME/YOUR_REPO_NAME:*"
        }
      }
    }
  ]
}
```

**Replace:**
- `YOUR_ACCOUNT_ID` with your AWS account ID
- `YOUR_GITHUB_USERNAME` with your GitHub username or organization
- `YOUR_REPO_NAME` with your repository name (e.g., `VillaEcommerceSdk`)

### Create the Role

```bash
# Get your AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Replace placeholders in trust policy
sed -i.bak "s/YOUR_ACCOUNT_ID/$ACCOUNT_ID/g" github-actions-trust-policy.json
sed -i.bak "s/YOUR_GITHUB_USERNAME/YOUR_ACTUAL_USERNAME/g" github-actions-trust-policy.json
sed -i.bak "s/YOUR_REPO_NAME/VillaEcommerceSdk/g" github-actions-trust-policy.json

# Create the role
aws iam create-role \
  --role-name GitHubActionsDeployRole \
  --assume-role-policy-document file://github-actions-trust-policy.json \
  --description "Role for GitHub Actions to deploy infrastructure"
```

## Step 3: Attach Required Permissions

The role needs permissions to deploy CloudFormation stacks and manage S3:

### Create Policy Document

Save this as `github-actions-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "s3:*",
        "iam:CreatePolicy",
        "iam:AttachRolePolicy",
        "iam:AttachUserPolicy",
        "iam:GetPolicy",
        "iam:GetRole",
        "iam:ListRoles",
        "iam:ListPolicies",
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    }
  ]
}
```

### Attach Policy to Role

```bash
# Create the policy
aws iam put-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-name GitHubActionsDeployPolicy \
  --policy-document file://github-actions-policy.json
```

**Or use an inline policy:**

```bash
aws iam put-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-name GitHubActionsDeployPolicy \
  --policy-document file://github-actions-policy.json
```

**Or attach AWS managed policies (more restrictive):**

```bash
# For CloudFormation
aws iam attach-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-arn arn:aws:iam::aws:policy/AWSCloudFormationFullAccess

# For S3
aws iam attach-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# For IAM (to create policies)
aws iam attach-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-arn arn:aws:iam::aws:policy/IAMFullAccess
```

## Step 4: Get Role ARN

```bash
aws iam get-role \
  --role-name GitHubActionsDeployRole \
  --query 'Role.Arn' \
  --output text
```

Copy this ARN - you'll need it for GitHub secrets.

## Step 5: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `AWS_ROLE_ARN`
5. Value: The ARN from Step 4 (e.g., `arn:aws:iam::123456789012:role/GitHubActionsDeployRole`)
6. Click **Add secret**

## Step 6: Update Workflow (if needed)

The workflow should already be configured correctly. Verify it uses:

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
    aws-region: ${{ github.event.inputs.region || env.AWS_REGION }}
```

## Step 7: Test the Setup

1. Go to **Actions** tab in GitHub
2. Select **Deploy S3 Cache Bucket** workflow
3. Click **Run workflow**
4. Fill in parameters (or use defaults)
5. Click **Run workflow**

The workflow should now authenticate with AWS using OIDC and deploy your stack.

## Troubleshooting

### Error: "Not authorized to perform sts:AssumeRole"

**Solution**: Check the trust policy:
- Verify the OIDC provider ARN is correct
- Ensure the repository name matches exactly (case-sensitive)
- Check the condition in the trust policy

### Error: "Access Denied" when deploying

**Solution**: The role needs more permissions:
- Add CloudFormation permissions
- Add S3 permissions
- Add IAM permissions (for creating policies)

### Error: "OIDC provider not found"

**Solution**: Create the OIDC provider first (Step 1)

### Restrict to Specific Branches

To only allow deployments from `main` branch, update the trust policy condition:

```json
"Condition": {
  "StringEquals": {
    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
    "token.actions.githubusercontent.com:ref": "refs/heads/main"
  },
  "StringLike": {
    "token.actions.githubusercontent.com:sub": "repo:YOUR_USERNAME/YOUR_REPO:*"
  }
}
```

### Restrict to Specific Environments

To use GitHub Environments for additional security:

1. Go to **Settings** → **Environments** → **New environment**
2. Name: `production`
3. Add protection rules if needed
4. Update workflow to use environment:

```yaml
environment:
  name: production
```

Then update trust policy to include environment:

```json
"StringEquals": {
  "token.actions.githubusercontent.com:environment": "production"
}
```

## Security Best Practices

1. **Use least privilege**: Only grant necessary permissions
2. **Restrict by repository**: Use specific repository names in trust policy
3. **Use environments**: Add approval requirements for production
4. **Monitor CloudTrail**: Track all assume role operations
5. **Rotate regularly**: Review and update policies periodically

## Quick Reference Commands

```bash
# Get AWS Account ID
aws sts get-caller-identity --query Account --output text

# Get Role ARN
aws iam get-role --role-name GitHubActionsDeployRole --query 'Role.Arn' --output text

# Test assume role (from GitHub Actions context)
aws sts assume-role-with-web-identity \
  --role-arn arn:aws:iam::ACCOUNT_ID:role/GitHubActionsDeployRole \
  --role-session-name github-actions-test \
  --web-identity-token-file /path/to/token

# List OIDC providers
aws iam list-open-id-connect-providers

# View trust policy
aws iam get-role --role-name GitHubActionsDeployRole --query 'Role.AssumeRolePolicyDocument'
```

## Alternative: Using AWS Access Keys (Not Recommended)

If you can't use OIDC, you can use access keys (less secure):

1. Create IAM user with deployment permissions
2. Create access key
3. Add to GitHub secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
4. Update workflow to use:

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1
```

**Note**: OIDC is preferred as it doesn't require storing long-lived credentials.

