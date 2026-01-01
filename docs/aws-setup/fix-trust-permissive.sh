#!/bin/bash
# Create a more permissive trust policy for testing
# WARNING: This allows ANY GitHub repository. Use only for testing!
# Usage: ./fix-trust-permissive.sh ROLE_NAME

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <ROLE_NAME>"
    echo "Example: $0 deploy-github-action-wallet2"
    exit 1
fi

ROLE_NAME=$1

echo "⚠️  WARNING: This will create a permissive trust policy that allows ANY GitHub repository!"
echo "Use this only for testing, then restrict it to your specific repo."
echo ""
read -p "Continue? [y/N]: " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Get account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create permissive trust policy
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
        }
      }
    }
  ]
}
EOF
)

echo "$TRUST_POLICY" > /tmp/permissive-trust-policy.json

echo "🔄 Updating trust policy..."
aws iam update-assume-role-policy \
    --role-name "$ROLE_NAME" \
    --policy-document file:///tmp/permissive-trust-policy.json

echo "✅ Trust policy updated (permissive mode)"
echo ""
echo "⚠️  Remember to restrict this to your specific repository after testing!"
echo ""

rm -f /tmp/permissive-trust-policy.json

