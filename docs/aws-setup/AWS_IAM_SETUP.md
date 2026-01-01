# AWS IAM Access Keys Setup for GitHub Actions

This guide shows you how to set up AWS IAM access keys for GitHub Actions deployment.

## Quick Setup (Automated)

```bash
cd .github
./setup-aws-iam-user.sh YOUR_GITHUB_USERNAME VillaEcommerceSdk
```

The script will:
1. Create an IAM user: `github-actions-villaecommercesdk`
2. Create and attach a policy with necessary permissions
3. Generate access keys
4. Output the keys for GitHub secrets

## Manual Setup

### Step 1: Create IAM User

```bash
aws iam create-user \
  --user-name github-actions-villaecommercesdk \
  --tags \
    Key=Purpose,Value=GitHubActions \
    Key=Repository,Value=YOUR_USERNAME/VillaEcommerceSdk
```

### Step 2: Create IAM Policy

Create a policy file `github-actions-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CloudFormationAccess",
      "Effect": "Allow",
      "Action": [
        "cloudformation:*",
        "s3:*",
        "iam:CreatePolicy",
        "iam:GetPolicy",
        "iam:ListPolicies",
        "iam:AttachRolePolicy",
        "iam:AttachUserPolicy",
        "iam:GetRole",
        "iam:ListRoles",
        "iam:PutRolePolicy",
        "iam:GetRolePolicy",
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    }
  ]
}
```

Create the policy:

```bash
aws iam create-policy \
  --policy-name GitHubActionsDeployPolicy \
  --policy-document file://github-actions-policy.json \
  --description "Policy for GitHub Actions deployment"
```

### Step 3: Attach Policy to User

```bash
POLICY_ARN=$(aws iam list-policies --scope Local \
  --query "Policies[?PolicyName=='GitHubActionsDeployPolicy'].Arn" \
  --output text)

aws iam attach-user-policy \
  --user-name github-actions-villaecommercesdk \
  --policy-arn $POLICY_ARN
```

### Step 4: Create Access Keys

```bash
aws iam create-access-key \
  --user-name github-actions-villaecommercesdk
```

**Save both keys immediately** - you cannot retrieve the secret key later!

### Step 5: Add to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add two secrets:

   **Secret 1:**
   - Name: `AWS_ACCESS_KEY_ID`
   - Value: (Access Key ID from Step 4)

   **Secret 2:**
   - Name: `AWS_SECRET_ACCESS_KEY`
   - Value: (Secret Access Key from Step 4)

## Test the Setup

1. Go to **Actions** tab in GitHub
2. Select **Deploy S3 Cache Bucket** workflow
3. Click **Run workflow**
4. The workflow should now authenticate and deploy

## Security Best Practices

1. **Rotate keys regularly**: Create new keys every 90 days
2. **Use least privilege**: Only grant necessary permissions
3. **Monitor usage**: Check CloudTrail logs regularly
4. **Tag resources**: Tag IAM user with repository info
5. **Delete unused keys**: Remove old access keys

## Rotating Access Keys

### Create New Key

```bash
# Create new access key
aws iam create-access-key --user-name github-actions-villaecommercesdk

# Update GitHub secrets with new keys
# Then delete old key after verifying new one works
```

### Delete Old Key

```bash
aws iam delete-access-key \
  --user-name github-actions-villaecommercesdk \
  --access-key-id OLD_ACCESS_KEY_ID
```

## Troubleshooting

### Error: Access Denied

- Verify access keys are correct in GitHub secrets
- Check IAM user has policy attached
- Verify policy permissions are sufficient

### Error: Invalid Access Key

- Keys are case-sensitive
- Ensure no extra spaces in GitHub secrets
- Verify keys haven't been deleted in AWS

### List Access Keys

```bash
aws iam list-access-keys --user-name github-actions-villaecommercesdk
```

### View Attached Policies

```bash
aws iam list-attached-user-policies --user-name github-actions-villaecommercesdk
```

## Alternative: Using AWS Managed Policies

If you prefer AWS managed policies:

```bash
# CloudFormation
aws iam attach-user-policy \
  --user-name github-actions-villaecommercesdk \
  --policy-arn arn:aws:iam::aws:policy/AWSCloudFormationFullAccess

# S3
aws iam attach-user-policy \
  --user-name github-actions-villaecommercesdk \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# IAM (for creating policies)
aws iam attach-user-policy \
  --user-name github-actions-villaecommercesdk \
  --policy-arn arn:aws:iam::aws:policy/IAMFullAccess
```

**Note**: Managed policies are broader than needed. Custom policy is more secure.

## Comparison: IAM Keys vs OIDC

| Feature | IAM Access Keys | OIDC |
|---------|----------------|------|
| Setup Complexity | Simple | Moderate |
| Security | Good (with rotation) | Better (no long-lived keys) |
| Key Management | Manual rotation | Automatic |
| Best For | Quick setup | Production/Enterprise |

For production, consider migrating to OIDC (see `AWS_SETUP.md`).

