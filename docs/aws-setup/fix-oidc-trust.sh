#!/bin/bash
# Quick fix script for OIDC trust policy issues
# Usage: ./fix-oidc-trust.sh YOUR_GITHUB_USERNAME YOUR_REPO_NAME

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <GITHUB_USERNAME_OR_ORG> <REPO_NAME>"
    echo "Example: $0 thanakijwanavit VillaEcommerceSdk"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME=$2
ROLE_NAME="GitHubActionsDeployRole"

echo "🔧 Fixing OIDC Trust Policy..."
echo "GitHub: $GITHUB_USERNAME/$REPO_NAME"
echo ""

# Get AWS Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "AWS Account ID: $ACCOUNT_ID"
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
echo "📝 Creating updated trust policy..."
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

echo "$TRUST_POLICY" > /tmp/fix-trust-policy.json
echo "✅ Trust policy created"
echo ""
echo "Trust policy will allow: repo:${GITHUB_USERNAME}/${REPO_NAME}:*"
echo ""

# Check if role exists
if aws iam get-role --role-name "$ROLE_NAME" &>/dev/null; then
    echo "🔄 Updating existing role trust policy..."
    aws iam update-assume-role-policy \
        --role-name "$ROLE_NAME" \
        --policy-document file:///tmp/fix-trust-policy.json
    echo "✅ Trust policy updated"
else
    echo "❌ Role $ROLE_NAME does not exist!"
    echo "Run the full setup script first: ./setup-aws-oidc.sh $GITHUB_USERNAME $REPO_NAME"
    exit 1
fi
echo ""

# Get Role ARN
ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Fix Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Role ARN: $ROLE_ARN"
echo ""
echo "📌 Verify this Role ARN matches your GitHub Secret:"
echo "   Repository → Settings → Secrets → Actions → AWS_ROLE_ARN"
echo ""
echo "If it doesn't match, update the secret with: $ROLE_ARN"
echo ""

# Cleanup
rm -f /tmp/fix-trust-policy.json

