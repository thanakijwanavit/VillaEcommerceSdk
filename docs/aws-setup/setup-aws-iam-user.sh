#!/bin/bash
# Setup script for GitHub Actions using AWS IAM Access Keys
# Creates an IAM user specifically for GitHub Actions with appropriate permissions
# Usage: ./setup-aws-iam-user.sh YOUR_GITHUB_USERNAME YOUR_REPO_NAME

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <GITHUB_USERNAME_OR_ORG> <REPO_NAME>"
    echo "Example: $0 myusername VillaEcommerceSdk"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME=$2
IAM_USER_NAME="github-actions-${REPO_NAME,,}"

echo "🚀 Setting up AWS IAM User for GitHub Actions..."
echo "GitHub: $GITHUB_USERNAME/$REPO_NAME"
echo "IAM User: $IAM_USER_NAME"
echo ""

# Get AWS Account ID
echo "📋 Getting AWS Account ID..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "AWS Account ID: $ACCOUNT_ID"
echo ""

# Step 1: Create IAM User
echo "👤 Step 1: Creating IAM User..."
if aws iam get-user --user-name "$IAM_USER_NAME" &>/dev/null; then
    echo "⚠️  User $IAM_USER_NAME already exists"
else
    echo "Creating IAM user: $IAM_USER_NAME..."
    aws iam create-user \
        --user-name "$IAM_USER_NAME" \
        --tags \
            Key=Purpose,Value=GitHubActions \
            Key=Repository,Value="${GITHUB_USERNAME}/${REPO_NAME}" \
            Key=ManagedBy,Value=Script
    echo "✅ User created"
fi
echo ""

# Step 2: Create Policy Document
echo "🔑 Step 2: Creating IAM Policy..."
POLICY_DOCUMENT=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CloudFormationAccess",
      "Effect": "Allow",
      "Action": [
        "cloudformation:CreateStack",
        "cloudformation:UpdateStack",
        "cloudformation:DeleteStack",
        "cloudformation:DescribeStacks",
        "cloudformation:DescribeStackEvents",
        "cloudformation:DescribeStackResources",
        "cloudformation:GetTemplate",
        "cloudformation:ValidateTemplate",
        "cloudformation:CreateChangeSet",
        "cloudformation:DescribeChangeSet",
        "cloudformation:ExecuteChangeSet",
        "cloudformation:DeleteChangeSet",
        "cloudformation:ListStacks",
        "cloudformation:ListStackResources"
      ],
      "Resource": "*"
    },
    {
      "Sid": "S3Access",
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:DeleteBucket",
        "s3:GetBucketLocation",
        "s3:GetBucketVersioning",
        "s3:PutBucketVersioning",
        "s3:GetBucketEncryption",
        "s3:PutBucketEncryption",
        "s3:GetBucketPolicy",
        "s3:PutBucketPolicy",
        "s3:DeleteBucketPolicy",
        "s3:GetBucketPublicAccessBlock",
        "s3:PutBucketPublicAccessBlock",
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket",
        "s3:HeadObject",
        "s3:PutBucketLifecycleConfiguration",
        "s3:GetBucketLifecycleConfiguration"
      ],
      "Resource": "*"
    },
    {
      "Sid": "IAMPolicyManagement",
      "Effect": "Allow",
      "Action": [
        "iam:CreatePolicy",
        "iam:GetPolicy",
        "iam:ListPolicies",
        "iam:AttachRolePolicy",
        "iam:AttachUserPolicy",
        "iam:GetRole",
        "iam:ListRoles",
        "iam:PutRolePolicy",
        "iam:GetRolePolicy"
      ],
      "Resource": "*"
    },
    {
      "Sid": "STSGetCallerIdentity",
      "Effect": "Allow",
      "Action": [
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    }
  ]
}
EOF
)

POLICY_NAME="GitHubActionsDeployPolicy-${REPO_NAME}"
echo "$POLICY_DOCUMENT" > /tmp/github-actions-policy.json

# Check if policy exists
POLICY_ARN=$(aws iam list-policies --scope Local --query "Policies[?PolicyName=='${POLICY_NAME}'].Arn" --output text 2>/dev/null || echo "")

if [ -z "$POLICY_ARN" ]; then
    echo "Creating policy: $POLICY_NAME..."
    POLICY_ARN=$(aws iam create-policy \
        --policy-name "$POLICY_NAME" \
        --policy-document file:///tmp/github-actions-policy.json \
        --description "Policy for GitHub Actions deployment of ${REPO_NAME}" \
        --query 'Policy.Arn' \
        --output text)
    echo "✅ Policy created: $POLICY_ARN"
else
    echo "⚠️  Policy already exists. Updating..."
    aws iam create-policy-version \
        --policy-arn "$POLICY_ARN" \
        --policy-document file:///tmp/github-actions-policy.json \
        --set-as-default || echo "Using existing policy version"
    echo "✅ Policy updated: $POLICY_ARN"
fi
echo ""

# Step 3: Attach Policy to User
echo "🔗 Step 3: Attaching Policy to User..."
aws iam attach-user-policy \
    --user-name "$IAM_USER_NAME" \
    --policy-arn "$POLICY_ARN"
echo "✅ Policy attached to user"
echo ""

# Step 4: Create Access Key
echo "🔐 Step 4: Creating Access Key..."
# Check if access key already exists
EXISTING_KEYS=$(aws iam list-access-keys --user-name "$IAM_USER_NAME" --query 'AccessKeyMetadata[].AccessKeyId' --output text 2>/dev/null || echo "")

if [ -n "$EXISTING_KEYS" ]; then
    echo "⚠️  Access key already exists for this user."
    echo "Existing key IDs: $EXISTING_KEYS"
    echo ""
    read -p "Do you want to create a new access key? (old keys will remain active) [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping access key creation. Using existing keys."
        echo ""
        echo "To get existing access key secret, use:"
        echo "aws iam get-user --user-name $IAM_USER_NAME"
        echo ""
        echo "Note: AWS doesn't allow retrieving existing secrets. You'll need to create a new key if you don't have the secret."
        exit 0
    fi
fi

ACCESS_KEY_OUTPUT=$(aws iam create-access-key --user-name "$IAM_USER_NAME")
ACCESS_KEY_ID=$(echo "$ACCESS_KEY_OUTPUT" | grep -oP '(?<="AccessKeyId": ")[^"]*')
SECRET_ACCESS_KEY=$(echo "$ACCESS_KEY_OUTPUT" | grep -oP '(?<="SecretAccessKey": ")[^"]*')

echo "✅ Access key created"
echo ""

# Step 5: Display Results
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📌 Add these to GitHub Secrets:"
echo "   Repository → Settings → Secrets and variables → Actions → New repository secret"
echo ""
echo "   Secret 1:"
echo "   Name:  AWS_ACCESS_KEY_ID"
echo "   Value: $ACCESS_KEY_ID"
echo ""
echo "   Secret 2:"
echo "   Name:  AWS_SECRET_ACCESS_KEY"
echo "   Value: $SECRET_ACCESS_KEY"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "IAM User: $IAM_USER_NAME"
echo "Policy ARN: $POLICY_ARN"
echo ""
echo "⚠️  IMPORTANT: Save the Secret Access Key now - you cannot retrieve it later!"
echo ""

# Cleanup
rm -f /tmp/github-actions-policy.json

