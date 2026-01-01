# Troubleshooting OIDC Authentication

## Error: "Not authorized to perform sts:AssumeRoleWithWebIdentity"

This error means the IAM role's trust policy doesn't allow GitHub Actions to assume it. Here's how to fix it:

### Step 1: Verify OIDC Provider Exists

```bash
aws iam list-open-id-connect-providers
```

You should see a provider with URL: `https://token.actions.githubusercontent.com`

If it doesn't exist, create it:

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

### Step 2: Check Your Repository Name

The trust policy must match your **exact** GitHub repository name. Common issues:

- **Case sensitivity**: `VillaEcommerceSdk` vs `villaecommercesdk` - must match exactly
- **Organization vs Username**: Check if it's `username/repo` or `org/repo`
- **Special characters**: Must match exactly

### Step 3: Verify Trust Policy

Get your current trust policy:

```bash
aws iam get-role --role-name GitHubActionsDeployRole \
  --query 'Role.AssumeRolePolicyDocument' \
  --output json
```

It should look like this (replace placeholders):

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
          "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_USERNAME/VillaEcommerceSdk:*"
        }
      }
    }
  ]
}
```

### Step 4: Update Trust Policy

If the repository name is wrong, update it:

```bash
# Get your account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Get your GitHub username/org (check your repo URL)
# Example: https://github.com/thanakijwanavit/VillaEcommerceSdk
# Username: thanakijwanavit
# Repo: VillaEcommerceSdk

# Create updated trust policy
cat > /tmp/trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::${ACCOUNT_ID}:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:thanakijwanavit/VillaEcommerceSdk:*"
        }
      }
    }
  ]
}
EOF

# Update the role
aws iam update-assume-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-document file:///tmp/trust-policy.json
```

**Important**: Replace `thanakijwanavit` with your actual GitHub username/organization name.

### Step 5: Verify Role ARN in GitHub Secrets

1. Get the correct Role ARN:
```bash
aws iam get-role --role-name GitHubActionsDeployRole --query 'Role.Arn' --output text
```

2. Verify it matches GitHub Secrets:
   - Go to Repository → Settings → Secrets → Actions
   - Check `AWS_ROLE_ARN` matches exactly

### Step 6: Test with More Permissive Policy (Temporary)

If still not working, try a more permissive trust policy temporarily to test:

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
        }
      }
    }
  ]
}
```

**Warning**: This allows ANY GitHub repository. Use only for testing, then restrict to your repo.

### Step 7: Check CloudTrail Logs

View recent assume role attempts:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRoleWithWebIdentity \
  --max-results 10 \
  --region ap-southeast-1
```

This will show you what's being requested and why it's failing.

## Common Issues

### Issue: Repository name mismatch

**Symptom**: Error persists after updating trust policy

**Solution**: 
1. Check your GitHub repository URL exactly
2. Format is: `repo:USERNAME_OR_ORG/REPO_NAME:*`
3. Case-sensitive!

### Issue: OIDC provider not found

**Symptom**: Error about OIDC provider

**Solution**: OIDC providers are global (not region-specific). Create it once:

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

### Issue: Thumbprint expired

**Symptom**: OIDC provider creation fails

**Solution**: Get latest thumbprint:

```bash
THUMBPRINT=$(echo | openssl s_client -servername token.actions.githubusercontent.com -showcerts -connect token.actions.githubusercontent.com:443 2>/dev/null | openssl x509 -fingerprint -noout -sha1 | tr ':' ' ' | awk '{print $2}')
echo $THUMBPRINT
```

Then update provider or use the latest thumbprint when creating.

## Quick Fix Script

Run this to fix common issues:

```bash
#!/bin/bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
GITHUB_USER="thanakijwanavit"  # CHANGE THIS
REPO_NAME="VillaEcommerceSdk"  # CHANGE THIS

cat > /tmp/fix-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::${ACCOUNT_ID}:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:${GITHUB_USER}/${REPO_NAME}:*"
        }
      }
    }
  ]
}
EOF

aws iam update-assume-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-document file:///tmp/fix-trust-policy.json

echo "✅ Trust policy updated"
echo "Repository: ${GITHUB_USER}/${REPO_NAME}"
```

## Still Not Working?

1. **Double-check repository name**: Go to your GitHub repo, copy the exact path
2. **Verify OIDC provider ARN**: Must match exactly in trust policy
3. **Check IAM permissions**: Your AWS user needs `iam:UpdateAssumeRolePolicy`
4. **Try the workflow again**: After updating trust policy, rerun the workflow

