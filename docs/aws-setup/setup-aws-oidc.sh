#!/bin/bash
# Quick setup script for GitHub Actions OIDC with AWS
# Usage: ./setup-aws-oidc.sh YOUR_GITHUB_USERNAME YOUR_REPO_NAME

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <GITHUB_USERNAME_OR_ORG> <REPO_NAME>"
    echo "Example: $0 myusername VillaEcommerceSdk"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME=$2

echo "🚀 Setting up GitHub Actions OIDC with AWS..."
echo "GitHub: $GITHUB_USERNAME/$REPO_NAME"
echo ""

# Get AWS Account ID
echo "📋 Getting AWS Account ID..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "AWS Account ID: $ACCOUNT_ID"
echo ""

# Step 1: Create OIDC Provider
echo "🔐 Step 1: Creating OIDC Identity Provider..."
OIDC_PROVIDER_EXISTS=$(aws iam list-open-id-connect-providers --query "OpenIDConnectProviderList[?contains(Arn, 'token.actions.githubusercontent.com')]" --output text)

if [ -z "$OIDC_PROVIDER_EXISTS" ]; then
    echo "Creating OIDC provider..."
    aws iam create-open-id-connect-provider \
        --url https://token.actions.githubusercontent.com \
        --client-id-list sts.amazonaws.com \
        --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1 \
        --region us-east-1 || echo "⚠️  OIDC provider may already exist or thumbprint needs update"
else
    echo "✅ OIDC provider already exists"
fi
echo ""

# Step 2: Create Trust Policy
echo "📝 Step 2: Creating IAM Role Trust Policy..."
TRUST_POLICY=$(cat <<EOF
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
          "token.actions.githubusercontent.com:sub": "repo:${GITHUB_USERNAME}/${REPO_NAME}:*"
        }
      }
    }
  ]
}
EOF
)

echo "$TRUST_POLICY" > /tmp/github-actions-trust-policy.json
echo "✅ Trust policy created"
echo ""

# Step 3: Create IAM Role
echo "👤 Step 3: Creating IAM Role..."
ROLE_NAME="GitHubActionsDeployRole"

# Check if role exists
if aws iam get-role --role-name "$ROLE_NAME" &>/dev/null; then
    echo "⚠️  Role $ROLE_NAME already exists. Updating trust policy..."
    aws iam update-assume-role-policy \
        --role-name "$ROLE_NAME" \
        --policy-document file:///tmp/github-actions-trust-policy.json
else
    echo "Creating role $ROLE_NAME..."
    aws iam create-role \
        --role-name "$ROLE_NAME" \
        --assume-role-policy-document file:///tmp/github-actions-trust-policy.json \
        --description "Role for GitHub Actions to deploy infrastructure"
fi
echo "✅ Role created/updated"
echo ""

# Step 4: Create and Attach Policy
echo "🔑 Step 4: Creating and attaching IAM Policy..."
POLICY_DOCUMENT=$(cat <<EOF
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
EOF
)

echo "$POLICY_DOCUMENT" > /tmp/github-actions-policy.json

aws iam put-role-policy \
    --role-name "$ROLE_NAME" \
    --policy-name GitHubActionsDeployPolicy \
    --policy-document file:///tmp/github-actions-policy.json
echo "✅ Policy attached"
echo ""

# Step 5: Get Role ARN
echo "📋 Step 5: Getting Role ARN..."
ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text)
echo ""
echo "✅ Setup Complete!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📌 Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Add this Role ARN to GitHub Secrets:"
echo "   Repository → Settings → Secrets and variables → Actions → New repository secret"
echo ""
echo "   Name:  AWS_ROLE_ARN"
echo "   Value: $ROLE_ARN"
echo ""
echo "2. Test the workflow:"
echo "   Go to Actions tab → Deploy S3 Cache Bucket → Run workflow"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Role ARN: $ROLE_ARN"
echo ""

# Cleanup
rm -f /tmp/github-actions-trust-policy.json /tmp/github-actions-policy.json

