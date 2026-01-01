#!/bin/bash
# Verify OIDC setup for GitHub Actions
# Usage: ./verify-oidc-setup.sh ROLE_ARN GITHUB_USERNAME REPO_NAME

set -e

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <ROLE_ARN> <GITHUB_USERNAME_OR_ORG> <REPO_NAME>"
    echo "Example: $0 arn:aws:iam::394922924679:role/deploy-github-action-wallet2 thanakijwanavit VillaEcommerceSdk"
    exit 1
fi

ROLE_ARN=$1
GITHUB_USERNAME=$2
REPO_NAME=$3
ROLE_NAME=$(echo "$ROLE_ARN" | awk -F'/' '{print $NF}')

echo "🔍 Verifying OIDC Setup..."
echo "Role: $ROLE_NAME"
echo "GitHub: $GITHUB_USERNAME/$REPO_NAME"
echo ""

# Check if role exists
echo "1. Checking if role exists..."
if aws iam get-role --role-name "$ROLE_NAME" &>/dev/null; then
    echo "   ✅ Role exists"
else
    echo "   ❌ Role does not exist!"
    exit 1
fi
echo ""

# Check OIDC provider
echo "2. Checking OIDC provider..."
OIDC_PROVIDER=$(aws iam list-open-id-connect-providers --query "OpenIDConnectProviderList[?contains(Arn, 'token.actions.githubusercontent.com')].Arn" --output text)
if [ -n "$OIDC_PROVIDER" ]; then
    echo "   ✅ OIDC provider exists: $OIDC_PROVIDER"
else
    echo "   ❌ OIDC provider not found!"
    exit 1
fi
echo ""

# Get current trust policy
echo "3. Current trust policy:"
TRUST_POLICY=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.AssumeRolePolicyDocument' --output json)
echo "$TRUST_POLICY" | jq '.'
echo ""

# Check if trust policy allows the repo
EXPECTED_SUB="repo:${GITHUB_USERNAME}/${REPO_NAME}:*"
echo "4. Checking if trust policy allows: $EXPECTED_SUB"
SUB_IN_POLICY=$(echo "$TRUST_POLICY" | jq -r '.Statement[0].Condition.StringLike."token.actions.githubusercontent.com:sub" // empty')

if [ -n "$SUB_IN_POLICY" ]; then
    echo "   Found condition: $SUB_IN_POLICY"
    if [[ "$SUB_IN_POLICY" == *"$GITHUB_USERNAME/$REPO_NAME"* ]]; then
        echo "   ✅ Repository matches"
    else
        echo "   ⚠️  Repository might not match exactly"
        echo "   Expected: $EXPECTED_SUB"
        echo "   Found: $SUB_IN_POLICY"
    fi
else
    echo "   ⚠️  No 'sub' condition found in trust policy"
fi
echo ""

# Check audience
echo "5. Checking audience condition..."
AUD_IN_POLICY=$(echo "$TRUST_POLICY" | jq -r '.Statement[0].Condition.StringEquals."token.actions.githubusercontent.com:aud" // empty')
if [ "$AUD_IN_POLICY" == "sts.amazonaws.com" ]; then
    echo "   ✅ Audience is correct: $AUD_IN_POLICY"
else
    echo "   ⚠️  Audience might be wrong: $AUD_IN_POLICY"
    echo "   Expected: sts.amazonaws.com"
fi
echo ""

# Check principal
echo "6. Checking principal..."
PRINCIPAL=$(echo "$TRUST_POLICY" | jq -r '.Statement[0].Principal.Federated // empty')
if [[ "$PRINCIPAL" == *"oidc-provider/token.actions.githubusercontent.com"* ]]; then
    echo "   ✅ Principal is correct: $PRINCIPAL"
else
    echo "   ⚠️  Principal might be wrong: $PRINCIPAL"
fi
echo ""

# Check role permissions
echo "7. Checking role permissions..."
POLICIES=$(aws iam list-attached-role-policies --role-name "$ROLE_NAME" --query 'AttachedPolicies[].PolicyArn' --output text)
if [ -n "$POLICIES" ]; then
    echo "   ✅ Role has attached policies:"
    echo "$POLICIES" | tr '\t' '\n' | sed 's/^/      - /'
else
    echo "   ⚠️  No attached policies found"
fi

INLINE_POLICIES=$(aws iam list-role-policies --role-name "$ROLE_NAME" --query 'PolicyNames' --output text)
if [ -n "$INLINE_POLICIES" ]; then
    echo "   ✅ Role has inline policies:"
    echo "$INLINE_POLICIES" | tr '\t' '\n' | sed 's/^/      - /'
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "If everything looks correct but it still fails, try:"
echo ""
echo "1. Make sure GitHub Secret AWS_ROLE_ARN matches exactly:"
echo "   $ROLE_ARN"
echo ""
echo "2. Try a more permissive trust policy temporarily (for testing):"
echo "   Run: ./fix-trust-permissive.sh $ROLE_NAME"
echo ""
echo "3. Check CloudTrail logs for detailed error:"
echo "   aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRoleWithWebIdentity --max-results 5"
echo ""

