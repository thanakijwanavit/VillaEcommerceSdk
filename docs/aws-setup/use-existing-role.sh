#!/bin/bash
# Use existing IAM role for GitHub Actions
# Usage: ./use-existing-role.sh ROLE_ARN GITHUB_USERNAME REPO_NAME

set -e

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <ROLE_ARN> <GITHUB_USERNAME_OR_ORG> <REPO_NAME>"
    echo "Example: $0 arn:aws:iam::394922924679:role/deploy-github-action-wallet2 thanakijwanavit VillaEcommerceSdk"
    exit 1
fi

ROLE_ARN=$1
GITHUB_USERNAME=$2
REPO_NAME=$3

# Extract role name from ARN
ROLE_NAME=$(echo "$ROLE_ARN" | awk -F'/' '{print $NF}')
ACCOUNT_ID=$(echo "$ROLE_ARN" | awk -F':' '{print $5}')

echo "🔧 Configuring existing IAM role for GitHub Actions..."
echo "Role ARN: $ROLE_ARN"
echo "Role Name: $ROLE_NAME"
echo "GitHub: $GITHUB_USERNAME/$REPO_NAME"
echo ""

# Verify role exists
if ! aws iam get-role --role-name "$ROLE_NAME" &>/dev/null; then
    echo "❌ Error: Role $ROLE_NAME does not exist!"
    exit 1
fi

echo "✅ Role exists"
echo ""

# Verify OIDC provider exists
echo "📋 Checking OIDC Provider..."
OIDC_PROVIDER=$(aws iam list-open-id-connect-providers --query "OpenIDConnectProviderList[?contains(Arn, 'token.actions.githubusercontent.com')].Arn" --output text)

if [ -z "$OIDC_PROVIDER" ]; then
    echo "⚠️  OIDC provider not found. Creating..."
    aws iam create-open-id-connect-provider \
        --url https://token.actions.githubusercontent.com \
        --client-id-list sts.amazonaws.com \
        --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
    echo "✅ OIDC provider created"
else
    echo "✅ OIDC provider exists: $OIDC_PROVIDER"
fi
echo ""

# Create updated trust policy
echo "📝 Updating trust policy..."
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

echo "$TRUST_POLICY" > /tmp/update-trust-policy.json

# Update trust policy
echo "🔄 Updating role trust policy..."
aws iam update-assume-role-policy \
    --role-name "$ROLE_NAME" \
    --policy-document file:///tmp/update-trust-policy.json

echo "✅ Trust policy updated"
echo ""

# Check if role has necessary permissions
echo "📋 Checking role permissions..."
POLICIES=$(aws iam list-attached-role-policies --role-name "$ROLE_NAME" --query 'AttachedPolicies[].PolicyArn' --output text)
INLINE_POLICIES=$(aws iam list-role-policies --role-name "$ROLE_NAME" --query 'PolicyNames' --output text)

if [ -z "$POLICIES" ] && [ -z "$INLINE_POLICIES" ]; then
    echo "⚠️  Warning: Role has no policies attached!"
    echo "You may need to attach policies for CloudFormation, S3, and IAM permissions."
    echo ""
    echo "Example:"
    echo "  aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AWSCloudFormationFullAccess"
    echo "  aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess"
    echo "  aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/IAMFullAccess"
else
    echo "✅ Role has policies attached"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Configuration Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📌 Add this Role ARN to GitHub Secrets:"
echo "   Repository → Settings → Secrets and variables → Actions → New repository secret"
echo ""
echo "   Name:  AWS_ROLE_ARN"
echo "   Value: $ROLE_ARN"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Cleanup
rm -f /tmp/update-trust-policy.json

